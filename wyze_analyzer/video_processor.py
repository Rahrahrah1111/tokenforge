"""
Video Processing Module for Wyze Camera Analyzer
Handles video file reading, frame extraction, and basic processing
"""

import cv2
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import logging
from typing import List, Tuple, Optional, Generator
import json

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Processes video files from Wyze camera"""
    
    def __init__(self, config: dict):
        self.config = config
        analysis_config = config.get('analysis', {})
        self.video_config = analysis_config.get('video', {})
        self.fps = self.video_config.get('fps', 1)
        self.target_resolution = tuple(self.video_config.get('resolution', [1920, 1080]))
        
    def get_video_files(self, source_path: str) -> List[Path]:
        """Get all video files from source path"""
        source = Path(source_path)
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.m4v']
        video_files = []
        
        if source.is_file():
            if source.suffix.lower() in video_extensions:
                video_files.append(source)
        elif source.is_dir():
            for ext in video_extensions:
                video_files.extend(source.rglob(f'*{ext}'))
                video_files.extend(source.rglob(f'*{ext.upper()}'))
        
        # Sort by modification time (oldest first)
        video_files.sort(key=lambda x: x.stat().st_mtime)
        
        logger.info(f"Found {len(video_files)} video files")
        return video_files
    
    def get_video_info(self, video_path: Path) -> dict:
        """Extract metadata from video file"""
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        info = {
            'path': str(video_path),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS),
            'codec': int(cap.get(cv2.CAP_PROP_FOURCC)),
            'file_size': video_path.stat().st_size,
            'modified_time': datetime.fromtimestamp(video_path.stat().st_mtime)
        }
        
        cap.release()
        return info
    
    def extract_frames(self, video_path: Path, start_time: float = 0, 
                      end_time: Optional[float] = None) -> Generator[Tuple[np.ndarray, float], None, None]:
        """Extract frames from video at specified FPS"""
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(video_fps / self.fps) if self.fps > 0 else 1
        
        # Seek to start time
        if start_time > 0:
            start_frame = int(start_time * video_fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frame_number = 0
        current_time = start_time
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Check if we've reached end time
            if end_time and current_time >= end_time:
                break
            
            # Only yield frames at specified interval
            if frame_number % frame_interval == 0:
                # Resize if needed
                if self.target_resolution:
                    frame = cv2.resize(frame, self.target_resolution)
                
                yield frame, current_time
            
            frame_number += 1
            current_time = frame_number / video_fps
        
        cap.release()
    
    def extract_audio(self, video_path: Path, output_path: Path, 
                     start_time: float = 0, duration: Optional[float] = None) -> Path:
        """Extract audio track from video"""
        import subprocess
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Safely access audio config from analysis section
        analysis_config = self.config.get('analysis', {})
        audio_config = analysis_config.get('audio', {})
        sample_rate = audio_config.get('sample_rate', 16000)
        channels = audio_config.get('channels', 1)
        
        cmd = [
            'ffmpeg', '-i', str(video_path),
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit
            '-ar', str(sample_rate),
            '-ac', str(channels),
        ]
        
        if start_time > 0:
            cmd.extend(['-ss', str(start_time)])
        
        if duration:
            cmd.extend(['-t', str(duration)])
        
        cmd.append(str(output_path))
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Extracted audio to {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Error extracting audio: {e.stderr.decode()}")
            raise
    
    def create_video_clip(self, video_path: Path, output_path: Path,
                         start_time: float, duration: float) -> Path:
        """Create a video clip from source video"""
        import subprocess
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            'ffmpeg', '-i', str(video_path),
            '-ss', str(start_time),
            '-t', str(duration),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', 'medium',
            '-crf', '23',
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Created video clip: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Error creating video clip: {e.stderr.decode()}")
            raise
    
    def filter_videos_by_date(self, video_files: List[Path], 
                             start_date: datetime, end_date: datetime) -> List[Path]:
        """Filter video files by date range"""
        filtered = []
        for video_file in video_files:
            try:
                mtime = datetime.fromtimestamp(video_file.stat().st_mtime)
                if start_date <= mtime <= end_date:
                    filtered.append(video_file)
            except Exception as e:
                logger.warning(f"Error checking date for {video_file}: {e}")
        
        logger.info(f"Filtered to {len(filtered)} videos in date range")
        return filtered

