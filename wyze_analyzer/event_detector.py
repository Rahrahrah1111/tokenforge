"""
Event Detection Module for Wyze Camera Analyzer
Detects and categorizes events in video footage
"""

import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """Represents a detected event"""
    event_id: str
    event_type: str
    start_time: float
    end_time: float
    confidence: float
    description: str
    video_path: str
    frame_indices: List[int]
    metadata: Dict


class EventDetector:
    """Detects events in video footage"""
    
    def __init__(self, config: dict):
        self.config = config
        # Event detection config is nested under analysis
        analysis_config = config.get('analysis', {})
        self.event_config = analysis_config.get('event_detection', {})
        self.motion_threshold = self.event_config.get('motion_threshold', 0.3)
        self.min_duration = self.event_config.get('min_event_duration', 2)
        self.max_duration = self.event_config.get('max_event_duration', 300)
        self.detection_method = self.event_config.get('detection_method', 'frame_diff')
        
        # Background subtractor for motion detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=True
        )
        
        # Previous frame for frame differencing
        self.prev_frame = None
        
    def detect_motion_frame_diff(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """Detect motion using frame differencing"""
        if frame1 is None or frame2 is None:
            return 0.0
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) if len(frame1.shape) == 3 else frame1
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY) if len(frame2.shape) == 3 else frame2
        
        # Calculate difference
        diff = cv2.absdiff(gray1, gray2)
        
        # Apply threshold
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        # Calculate motion percentage
        motion_pixels = np.sum(thresh > 0)
        total_pixels = thresh.size
        motion_ratio = motion_pixels / total_pixels
        
        return motion_ratio
    
    def detect_motion_bg_subtraction(self, frame: np.ndarray) -> float:
        """Detect motion using background subtraction"""
        fg_mask = self.bg_subtractor.apply(frame)
        
        # Calculate motion percentage
        motion_pixels = np.sum(fg_mask > 0)
        total_pixels = fg_mask.size
        motion_ratio = motion_pixels / total_pixels
        
        return motion_ratio
    
    def detect_motion_optical_flow(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """Detect motion using optical flow"""
        if frame1 is None or frame2 is None:
            return 0.0
        
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) if len(frame1.shape) == 3 else frame1
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY) if len(frame2.shape) == 3 else frame2
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(
            gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        # Calculate magnitude of flow vectors
        magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        
        # Threshold for significant motion
        motion_mask = magnitude > 2.0
        motion_ratio = np.sum(motion_mask) / magnitude.size
        
        return motion_ratio
    
    def detect_motion(self, frame: np.ndarray, prev_frame: Optional[np.ndarray] = None) -> float:
        """Detect motion in frame using configured method"""
        if self.detection_method == 'frame_diff':
            if prev_frame is None:
                return 0.0
            return self.detect_motion_frame_diff(prev_frame, frame)
        elif self.detection_method == 'optical_flow':
            if prev_frame is None:
                return 0.0
            return self.detect_motion_optical_flow(prev_frame, frame)
        elif self.detection_method == 'bg_subtraction':
            return self.detect_motion_bg_subtraction(frame)
        else:
            # Default to frame diff
            if prev_frame is None:
                return 0.0
            return self.detect_motion_frame_diff(prev_frame, frame)
    
    def categorize_event(self, event_type: str, motion_data: Dict, 
                        audio_data: Optional[Dict] = None) -> str:
        """Categorize event based on detected features"""
        categories = {
            'motion': 'Motion detected',
            'human_detection': 'Human detected',
            'vehicle': 'Vehicle detected',
            'animal': 'Animal detected',
            'sound_detection': 'Sound detected',
            'speech_detection': 'Speech detected',
            'package_delivery': 'Package delivery',
            'door_opening': 'Door activity',
            'night_vision': 'Night vision mode'
        }
        
        # Basic categorization logic
        description = categories.get(event_type, 'Event detected')
        
        # Add details based on motion data
        if motion_data.get('intensity', 0) > 0.7:
            description += ' - High activity'
        elif motion_data.get('intensity', 0) < 0.2:
            description += ' - Low activity'
        
        # Add audio information
        if audio_data and audio_data.get('has_speech', False):
            description += ' - Contains speech'
        
        return description
    
    def detect_events_in_video(self, video_processor, video_path: Path, 
                              start_time: float = 0, end_time: Optional[float] = None) -> List[Event]:
        """Detect events in a video file"""
        events = []
        current_event = None
        frame_index = 0
        prev_frame = None
        
        logger.info(f"Detecting events in {video_path}")
        
        for frame, timestamp in video_processor.extract_frames(video_path, start_time, end_time):
            # Detect motion
            motion_ratio = self.detect_motion(frame, prev_frame)
            
            # Check if motion exceeds threshold
            if motion_ratio >= self.motion_threshold:
                if current_event is None:
                    # Start new event
                    current_event = {
                        'start_time': timestamp,
                        'start_frame': frame_index,
                        'max_motion': motion_ratio,
                        'frame_indices': [frame_index]
                    }
                else:
                    # Continue current event
                    current_event['max_motion'] = max(current_event['max_motion'], motion_ratio)
                    current_event['frame_indices'].append(frame_index)
                    current_event['end_time'] = timestamp
            else:
                if current_event is not None:
                    # End current event
                    duration = current_event.get('end_time', timestamp) - current_event['start_time']
                    
                    if duration >= self.min_duration:
                        # Create event object
                        event = Event(
                            event_id=f"event_{int(current_event['start_time'])}_{frame_index}",
                            event_type='motion',
                            start_time=current_event['start_time'],
                            end_time=current_event.get('end_time', timestamp),
                            confidence=current_event['max_motion'],
                            description=self.categorize_event('motion', {
                                'intensity': current_event['max_motion']
                            }),
                            video_path=str(video_path),
                            frame_indices=current_event['frame_indices'],
                            metadata={
                                'motion_intensity': current_event['max_motion'],
                                'duration': duration
                            }
                        )
                        events.append(event)
                    
                    current_event = None
            
            prev_frame = frame.copy()
            frame_index += 1
        
        # Handle event that extends to end of video
        if current_event is not None:
            duration = current_event.get('end_time', timestamp) - current_event['start_time']
            if duration >= self.min_duration:
                event = Event(
                    event_id=f"event_{int(current_event['start_time'])}_{frame_index}",
                    event_type='motion',
                    start_time=current_event['start_time'],
                    end_time=current_event.get('end_time', timestamp),
                    confidence=current_event['max_motion'],
                    description=self.categorize_event('motion', {
                        'intensity': current_event['max_motion']
                    }),
                    video_path=str(video_path),
                    frame_indices=current_event['frame_indices'],
                    metadata={
                        'motion_intensity': current_event['max_motion'],
                        'duration': duration
                    }
                )
                events.append(event)
        
        logger.info(f"Detected {len(events)} events in {video_path}")
        return events

