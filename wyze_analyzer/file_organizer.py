"""
File Organization Module for Wyze Camera Analyzer
Organizes analyzed events into categorized folders
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging
import json
import shutil
from dataclasses import asdict

logger = logging.getLogger(__name__)


class FileOrganizer:
    """Organizes analyzed events into folders"""
    
    def __init__(self, config: dict):
        self.config = config
        self.output_config = config.get('output', {})
        self.base_directory = Path(self.output_config.get('base_directory', './wyze_analysis_output'))
        self.folder_structure = self.output_config.get('folder_structure', {})
        self.file_naming = self.output_config.get('file_naming', {})
        
        # Create base directory
        self.base_directory.mkdir(parents=True, exist_ok=True)
    
    def get_event_folder(self, event, video_info: Dict) -> Path:
        """Get folder path for an event based on structure settings"""
        folder_parts = []
        
        # Base directory
        folder_parts.append(self.base_directory)
        
        # By date
        if self.folder_structure.get('by_date', True):
            event_date = datetime.fromtimestamp(event.start_time)
            folder_parts.append(event_date.strftime('%Y'))
            folder_parts.append(event_date.strftime('%m'))
            folder_parts.append(event_date.strftime('%d'))
        
        # By event type
        if self.folder_structure.get('by_event_type', True):
            folder_parts.append(event.event_type)
        
        # By hour
        if self.folder_structure.get('by_hour', False):
            event_date = datetime.fromtimestamp(event.start_time)
            folder_parts.append(event_date.strftime('%H'))
        
        # Create folder path
        folder_path = Path(*folder_parts)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        return folder_path
    
    def get_event_filename(self, event, video_info: Dict, extension: str = '') -> str:
        """Generate filename for event based on naming settings"""
        parts = []
        
        # Timestamp
        if self.file_naming.get('include_timestamp', True):
            event_date = datetime.fromtimestamp(event.start_time)
            parts.append(event_date.strftime('%Y%m%d_%H%M%S'))
        
        # Event type
        if self.file_naming.get('include_event_type', True):
            parts.append(event.event_type)
        
        # Duration
        if self.file_naming.get('include_duration', True):
            duration = int(event.end_time - event.start_time)
            parts.append(f"{duration}s")
        
        # Event ID
        parts.append(event.event_id)
        
        filename = '_'.join(parts)
        if extension:
            filename += extension
        
        return filename
    
    def organize_event(self, event, video_path: Path, video_clip_path: Path,
                      audio_path: Path, transcription: Dict, video_info: Dict) -> Dict:
        """Organize all files for an event"""
        # Get folder and filename
        event_folder = self.get_event_folder(event, video_info)
        base_filename = self.get_event_filename(event, video_info)
        
        # Copy/move files
        organized_files = {}
        
        # Video clip
        if video_clip_path.exists():
            video_dest = event_folder / f"{base_filename}.mp4"
            shutil.copy2(video_clip_path, video_dest)
            organized_files['video'] = str(video_dest)
            logger.info(f"Organized video clip: {video_dest}")
        
        # Audio file
        if audio_path.exists():
            audio_dest = event_folder / f"{base_filename}_audio.wav"
            shutil.copy2(audio_path, audio_dest)
            organized_files['audio'] = str(audio_dest)
        
        # Transcription
        if transcription:
            # JSON transcription
            json_dest = event_folder / f"{base_filename}_transcription.json"
            with open(json_dest, 'w', encoding='utf-8') as f:
                json.dump(transcription, f, indent=2, ensure_ascii=False)
            organized_files['transcription_json'] = str(json_dest)
            
            # Text transcription
            txt_dest = event_folder / f"{base_filename}_transcription.txt"
            with open(txt_dest, 'w', encoding='utf-8') as f:
                f.write(transcription.get('text', ''))
            organized_files['transcription_txt'] = str(txt_dest)
        
        # Event metadata
        metadata = {
            'event_id': event.event_id,
            'event_type': event.event_type,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'duration': event.end_time - event.start_time,
            'confidence': event.confidence,
            'description': event.description,
            'video_source': str(video_path),
            'video_info': video_info,
            'transcription': transcription,
            'files': organized_files,
            'metadata': event.metadata
        }
        
        metadata_dest = event_folder / f"{base_filename}_metadata.json"
        with open(metadata_dest, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)
        organized_files['metadata'] = str(metadata_dest)
        
        logger.info(f"Organized event {event.event_id} to {event_folder}")
        return organized_files
    
    def create_event_log(self, events: List, output_path: Optional[Path] = None) -> Path:
        """Create a CSV log of all events"""
        import csv
        
        if output_path is None:
            output_path = self.base_directory / 'event_log.csv'
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Event ID', 'Event Type', 'Start Time', 'End Time', 
                'Duration (s)', 'Confidence', 'Description', 'Video Path',
                'Has Transcription', 'Transcription Text'
            ])
            
            for event in events:
                writer.writerow([
                    event.event_id,
                    event.event_type,
                    datetime.fromtimestamp(event.start_time).isoformat(),
                    datetime.fromtimestamp(event.end_time).isoformat(),
                    event.end_time - event.start_time,
                    event.confidence,
                    event.description,
                    event.video_path,
                    'Yes' if hasattr(event, 'transcription') and event.transcription else 'No',
                    event.transcription.get('text', '')[:100] if hasattr(event, 'transcription') and event.transcription else ''
                ])
        
        logger.info(f"Created event log: {output_path}")
        return output_path

