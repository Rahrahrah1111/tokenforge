#!/usr/bin/env python3
"""
Wyze Camera Analyzer - Main Application
Analyzes video footage, detects events, transcribes speech, and organizes results
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List
import yaml
from tqdm import tqdm
import tempfile

from video_processor import VideoProcessor
from event_detector import EventDetector, Event
from audio_processor import AudioProcessor
from transcriber import Transcriber
from file_organizer import FileOrganizer


class WyzeAnalyzer:
    """Main application class"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize analyzer with configuration"""
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Setup logging
        self._setup_logging()
        
        # Get logger after setup
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.video_processor = VideoProcessor(self.config)
        self.event_detector = EventDetector(self.config)
        self.audio_processor = AudioProcessor(self.config)
        self.transcriber = Transcriber(self.config)
        self.file_organizer = FileOrganizer(self.config)
        
        self.logger.info("Wyze Camera Analyzer initialized")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_file = log_config.get('log_file', './wyze_analyzer.log')
        console_output = log_config.get('console_output', True)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
    
    def analyze_video_source(self, source_path: str, start_date: datetime = None, 
                            end_date: datetime = None) -> List[Event]:
        """Analyze video from source (SD card, API, or cloud)"""
        source_config = self.config.get('video_source', {})
        source_type = source_config.get('source_type', 'sd_card')
        
        self.logger.info(f"Analyzing video source: {source_type}")
        
        if source_type == 'sd_card':
            return self._analyze_sd_card(source_path, start_date, end_date)
        elif source_type == 'api':
            return self._analyze_api(source_path, start_date, end_date)
        elif source_type == 'cloud':
            return self._analyze_cloud(source_path, start_date, end_date)
        else:
            raise ValueError(f"Unknown source type: {source_type}")
    
    def _analyze_sd_card(self, sd_card_path: str, start_date: datetime = None,
                        end_date: datetime = None) -> List[Event]:
        """Analyze videos from SD card"""
        # Get video files
        video_files = self.video_processor.get_video_files(sd_card_path)
        
        if not video_files:
            self.logger.warning(f"No video files found in {sd_card_path}")
            return []
        
        # Filter by date if specified
        if start_date and end_date:
            video_files = self.video_processor.filter_videos_by_date(
                video_files, start_date, end_date
            )
        
        # If no date range specified, use config
        if not start_date or not end_date:
            analysis_days = self.config.get('analysis', {}).get('analysis_period_days', 14)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=analysis_days)
            video_files = self.video_processor.filter_videos_by_date(
                video_files, start_date, end_date
            )
        
        self.logger.info(f"Processing {len(video_files)} video files")
        
        all_events = []
        
        # Process each video
        for video_path in tqdm(video_files, desc="Processing videos"):
            try:
                # Get video info
                video_info = self.video_processor.get_video_info(video_path)
                
                # Detect events
                events = self.event_detector.detect_events_in_video(
                    self.video_processor, video_path
                )
                
                # Process each event
                for event in events:
                    event.video_info = video_info
                    all_events.append(event)
                
            except Exception as e:
                self.logger.error(f"Error processing {video_path}: {e}")
                continue
        
        return all_events
    
    def _analyze_api(self, api_path: str, start_date: datetime = None,
                    end_date: datetime = None) -> List[Event]:
        """Analyze videos from Wyze API"""
        # TODO: Implement Wyze API integration
        self.logger.warning("API source not yet implemented")
        return []
    
    def _analyze_cloud(self, cloud_path: str, start_date: datetime = None,
                      end_date: datetime = None) -> List[Event]:
        """Analyze videos from cloud service"""
        # TODO: Implement cloud service integration
        self.logger.warning("Cloud source not yet implemented")
        return []
    
    def process_events(self, events: List[Event]) -> List[Event]:
        """Process events: extract audio, enhance, transcribe, and organize"""
        self.logger.info(f"Processing {len(events)} events")
        
        processed_events = []
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            for event in tqdm(events, desc="Processing events"):
                try:
                    video_path = Path(event.video_path)
                    
                    # Create video clip for event
                    video_clip_path = temp_path / f"{event.event_id}_clip.mp4"
                    self.video_processor.create_video_clip(
                        video_path,
                        video_clip_path,
                        event.start_time,
                        event.end_time - event.start_time
                    )
                    
                    # Extract audio
                    audio_path = temp_path / f"{event.event_id}_audio.wav"
                    self.video_processor.extract_audio(
                        video_path,
                        audio_path,
                        event.start_time,
                        event.end_time - event.start_time
                    )
                    
                    # Enhance audio
                    enhanced_audio_path = self.audio_processor.enhance_audio(
                        audio_path,
                        temp_path / f"{event.event_id}_enhanced.wav"
                    )
                    
                    # Check if audio has speech
                    audio, sr = self.audio_processor.load_audio(enhanced_audio_path)
                    has_speech = self.audio_processor.has_speech(audio, sr)
                    
                    # Transcribe if speech detected
                    transcription = None
                    if has_speech:
                        transcription = self.transcriber.transcribe_audio(enhanced_audio_path)
                        event.transcription = transcription
                        self.logger.info(f"Transcribed event {event.event_id}: {len(transcription.get('text', ''))} chars")
                    else:
                        self.logger.info(f"No speech detected in event {event.event_id}")
                    
                    # Organize files
                    organized_files = self.file_organizer.organize_event(
                        event,
                        video_path,
                        video_clip_path,
                        enhanced_audio_path,
                        transcription,
                        event.video_info
                    )
                    
                    event.organized_files = organized_files
                    processed_events.append(event)
                    
                except Exception as e:
                    self.logger.error(f"Error processing event {event.event_id}: {e}")
                    continue
        
        return processed_events
    
    def run(self, source_path: str, start_date: datetime = None, 
           end_date: datetime = None):
        """Run full analysis pipeline"""
        self.logger.info("Starting Wyze Camera Analyzer")
        self.logger.info(f"Source: {source_path}")
        self.logger.info(f"Date range: {start_date} to {end_date}")
        
        # Analyze video source
        events = self.analyze_video_source(source_path, start_date, end_date)
        self.logger.info(f"Detected {len(events)} events")
        
        # Process events
        processed_events = self.process_events(events)
        self.logger.info(f"Processed {len(processed_events)} events")
        
        # Create event log
        self.file_organizer.create_event_log(processed_events)
        
        self.logger.info("Analysis complete!")
        self.logger.info(f"Results saved to: {self.file_organizer.base_directory}")
        
        return processed_events


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Wyze Camera Analyzer - Analyze video footage, detect events, and transcribe speech'
    )
    parser.add_argument(
        'source',
        help='Path to video source (SD card path, API endpoint, or cloud URL)'
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--start-date',
        help='Start date for analysis (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--end-date',
        help='End date for analysis (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--days',
        type=int,
        help='Number of days to analyze (default: from config)'
    )
    
    args = parser.parse_args()
    
    # Parse dates
    start_date = None
    end_date = None
    
    if args.days:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=args.days)
    else:
        if args.start_date:
            start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        if args.end_date:
            end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    
    # Create analyzer and run
    analyzer = WyzeAnalyzer(args.config)
    analyzer.run(args.source, start_date, end_date)


if __name__ == '__main__':
    main()

