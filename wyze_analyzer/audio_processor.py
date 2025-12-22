"""
Audio Processing Module for Wyze Camera Analyzer
Handles audio extraction, enhancement, and preparation for transcription
"""

import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Optional, Tuple
import logging
import noisereduce as nr
import librosa
from scipy import signal
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Processes and enhances audio for transcription"""
    
    def __init__(self, config: dict):
        self.config = config
        # Audio config is nested under analysis
        analysis_config = config.get('analysis', {})
        self.audio_config = analysis_config.get('audio', {})
        self.enhancement_config = self.audio_config.get('enhancement', {})
        
        self.sample_rate = self.audio_config.get('sample_rate', 16000)
        self.channels = self.audio_config.get('channels', 1)
        self.bit_depth = self.audio_config.get('bit_depth', 16)
        
        # Enhancement settings
        self.noise_reduction = self.enhancement_config.get('noise_reduction', True)
        self.amplification = self.enhancement_config.get('amplification', 1.5)
        self.high_pass = self.enhancement_config.get('high_pass_filter', 80)
        self.low_pass = self.enhancement_config.get('low_pass_filter', 8000)
        self.normalize = self.enhancement_config.get('normalize', True)
        self.aggressive_noise_reduction = self.enhancement_config.get('aggressive_noise_reduction', False)
    
    def load_audio(self, audio_path: Path) -> Tuple[np.ndarray, int]:
        """Load audio file"""
        try:
            audio, sr = librosa.load(str(audio_path), sr=self.sample_rate, mono=True)
            logger.info(f"Loaded audio: {audio_path}, duration: {len(audio)/sr:.2f}s")
            return audio, sr
        except Exception as e:
            logger.error(f"Error loading audio {audio_path}: {e}")
            raise
    
    def apply_noise_reduction(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Apply noise reduction to audio"""
        if not self.noise_reduction:
            return audio
        
        try:
            # Use noisereduce library
            prop_decrease = 0.95 if self.aggressive_noise_reduction else 0.8
            reduced_noise = nr.reduce_noise(
                y=audio,
                sr=sample_rate,
                stationary=False,
                prop_decrease=prop_decrease
            )
            logger.debug(f"Applied noise reduction (aggressive: {self.aggressive_noise_reduction})")
            return reduced_noise
        except Exception as e:
            logger.warning(f"Error in noise reduction: {e}, using original audio")
            return audio
    
    def apply_filters(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Apply high-pass and low-pass filters"""
        filtered = audio.copy()
        
        # High-pass filter (remove low frequency noise)
        if self.high_pass > 0:
            nyquist = sample_rate / 2
            high_pass_normalized = self.high_pass / nyquist
            b, a = signal.butter(4, high_pass_normalized, btype='high')
            filtered = signal.filtfilt(b, a, filtered)
            logger.debug(f"Applied high-pass filter at {self.high_pass}Hz")
        
        # Low-pass filter (remove high frequency noise)
        nyquist = sample_rate / 2
        if self.low_pass < nyquist:
            low_pass_normalized = self.low_pass / nyquist
            b, a = signal.butter(4, low_pass_normalized, btype='low')
            filtered = signal.filtfilt(b, a, filtered)
            logger.debug(f"Applied low-pass filter at {self.low_pass}Hz")
        
        return filtered
    
    def amplify_audio(self, audio: np.ndarray) -> np.ndarray:
        """Amplify audio signal"""
        if self.amplification == 1.0:
            return audio
        
        amplified = audio * self.amplification
        
        # Prevent clipping
        max_val = np.abs(amplified).max()
        if max_val > 1.0:
            amplified = amplified / max_val
        
        logger.debug(f"Amplified audio by {self.amplification}x")
        return amplified
    
    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """Normalize audio to [-1, 1] range"""
        if not self.normalize:
            return audio
        
        max_val = np.abs(audio).max()
        if max_val > 0:
            normalized = audio / max_val
            logger.debug("Normalized audio")
            return normalized
        return audio
    
    def enhance_audio(self, audio_path: Path, output_path: Optional[Path] = None) -> Path:
        """Apply all enhancement steps to audio"""
        # Load audio
        audio, sr = self.load_audio(audio_path)
        
        # Apply enhancements
        enhanced = audio.copy()
        
        # Noise reduction
        enhanced = self.apply_noise_reduction(enhanced, sr)
        
        # Apply filters
        enhanced = self.apply_filters(enhanced, sr)
        
        # Amplify
        enhanced = self.amplify_audio(enhanced)
        
        # Normalize
        enhanced = self.normalize_audio(enhanced)
        
        # Save enhanced audio
        if output_path is None:
            output_path = audio_path.parent / f"{audio_path.stem}_enhanced.wav"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to int16 for saving
        audio_int16 = (enhanced * 32767).astype(np.int16)
        
        sf.write(str(output_path), audio_int16, sr, subtype='PCM_16')
        logger.info(f"Saved enhanced audio to {output_path}")
        
        return output_path
    
    def detect_speech_segments(self, audio: np.ndarray, sample_rate: int, 
                              threshold: float = 0.01) -> list:
        """Detect segments likely containing speech"""
        # Calculate energy
        frame_length = int(0.025 * sample_rate)  # 25ms frames
        hop_length = int(0.010 * sample_rate)  # 10ms hop
        
        # Calculate RMS energy
        rms = librosa.feature.rms(y=audio, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Find segments above threshold
        speech_mask = rms > threshold
        speech_segments = []
        
        in_speech = False
        start_frame = 0
        
        for i, is_speech in enumerate(speech_mask):
            if is_speech and not in_speech:
                start_frame = i
                in_speech = True
            elif not is_speech and in_speech:
                end_frame = i
                start_time = start_frame * hop_length / sample_rate
                end_time = end_frame * hop_length / sample_rate
                speech_segments.append((start_time, end_time))
                in_speech = False
        
        # Handle case where speech continues to end
        if in_speech:
            end_time = len(audio) / sample_rate
            start_time = start_frame * hop_length / sample_rate
            speech_segments.append((start_time, end_time))
        
        logger.info(f"Detected {len(speech_segments)} speech segments")
        return speech_segments
    
    def has_speech(self, audio: np.ndarray, sample_rate: int) -> bool:
        """Quick check if audio contains speech"""
        segments = self.detect_speech_segments(audio, sample_rate)
        return len(segments) > 0

