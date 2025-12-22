"""
Web Interface for Wyze Camera Analyzer
Provides a web UI for viewing analysis results and managing analysis jobs
"""

from flask import Flask, render_template, jsonify, request, send_file
from pathlib import Path
import json
import logging
from datetime import datetime
from typing import List, Dict

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

logger = logging.getLogger(__name__)


class WebInterface:
    """Web interface for Wyze Analyzer"""
    
    def __init__(self, output_directory: str = './wyze_analysis_output'):
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)
    
    def get_events(self) -> List[Dict]:
        """Get all events from output directory"""
        events = []
        
        # Find all metadata files
        for metadata_file in self.output_directory.rglob('*_metadata.json'):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    event_data = json.load(f)
                    events.append(event_data)
            except Exception as e:
                logger.error(f"Error loading event from {metadata_file}: {e}")
        
        # Sort by start time
        events.sort(key=lambda x: x.get('start_time', 0))
        
        return events
    
    def get_event_by_id(self, event_id: str) -> Dict:
        """Get specific event by ID"""
        for metadata_file in self.output_directory.rglob('*_metadata.json'):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    event_data = json.load(f)
                    if event_data.get('event_id') == event_id:
                        return event_data
            except Exception as e:
                logger.error(f"Error loading event from {metadata_file}: {e}")
        
        return None
    
    def get_events_by_type(self, event_type: str) -> List[Dict]:
        """Get events filtered by type"""
        all_events = self.get_events()
        return [e for e in all_events if e.get('event_type') == event_type]
    
    def get_events_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get events in date range"""
        all_events = self.get_events()
        filtered = []
        
        for event in all_events:
            event_time = datetime.fromtimestamp(event.get('start_time', 0))
            if start_date <= event_time <= end_date:
                filtered.append(event)
        
        return filtered


# Create global interface instance
interface = WebInterface()


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/events')
def api_events():
    """API endpoint to get all events"""
    event_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if event_type:
        events = interface.get_events_by_type(event_type)
    else:
        events = interface.get_events()
    
    # Filter by date if provided
    if start_date and end_date:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        events = interface.get_events_by_date_range(start, end)
    
    return jsonify(events)


@app.route('/api/events/<event_id>')
def api_event(event_id):
    """API endpoint to get specific event"""
    event = interface.get_event_by_id(event_id)
    if event:
        return jsonify(event)
    return jsonify({'error': 'Event not found'}), 404


@app.route('/api/events/<event_id>/video')
def api_event_video(event_id):
    """Serve video file for event"""
    event = interface.get_event_by_id(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    video_path = event.get('files', {}).get('video')
    if video_path and Path(video_path).exists():
        return send_file(video_path, mimetype='video/mp4')
    
    return jsonify({'error': 'Video not found'}), 404


@app.route('/api/events/<event_id>/audio')
def api_event_audio(event_id):
    """Serve audio file for event"""
    event = interface.get_event_by_id(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    audio_path = event.get('files', {}).get('audio')
    if audio_path and Path(audio_path).exists():
        return send_file(audio_path, mimetype='audio/wav')
    
    return jsonify({'error': 'Audio not found'}), 404


@app.route('/api/stats')
def api_stats():
    """Get statistics about analyzed events"""
    events = interface.get_events()
    
    stats = {
        'total_events': len(events),
        'events_by_type': {},
        'events_with_transcription': 0,
        'total_duration': 0,
        'date_range': {
            'start': None,
            'end': None
        }
    }
    
    if events:
        # Events by type
        for event in events:
            event_type = event.get('event_type', 'unknown')
            stats['events_by_type'][event_type] = stats['events_by_type'].get(event_type, 0) + 1
            
            # Transcription count
            if event.get('transcription') and event['transcription'].get('text'):
                stats['events_with_transcription'] += 1
            
            # Duration
            stats['total_duration'] += event.get('duration', 0)
        
        # Date range
        start_times = [e.get('start_time', 0) for e in events]
        stats['date_range']['start'] = datetime.fromtimestamp(min(start_times)).isoformat()
        stats['date_range']['end'] = datetime.fromtimestamp(max(start_times)).isoformat()
    
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

