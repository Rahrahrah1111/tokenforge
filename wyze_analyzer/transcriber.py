"""
Speech Transcription Module for Wyze Camera Analyzer
Transcribes human speech from audio using Whisper
"""

import whisper
import torch
from pathlib import Path
from typing import List, Dict, Optional
import logging
import json

logger = logging.getLogger(__name__)


class Transcriber:
    """Transcribes speech from audio files"""
    
    def __init__(self, config: dict):
        self.config = config
        # Transcription config is nested under analysis
        analysis_config = config.get('analysis', {})
        self.transcription_config = analysis_config.get('transcription', {})
        
        self.model_name = self.transcription_config.get('model', 'base')
        self.language = self.transcription_config.get('language', 'en')
        self.device = self.transcription_config.get('device', 'auto')
        self.temperature = self.transcription_config.get('temperature', 0.0)
        self.beam_size = self.transcription_config.get('beam_size', 5)
        self.best_of = self.transcription_config.get('best_of', 5)
        self.patience = self.transcription_config.get('patience', 1.0)
        self.condition_on_previous_text = self.transcription_config.get('condition_on_previous_text', True)
        self.initial_prompt = self.transcription_config.get('initial_prompt', '')
        
        # Load Whisper model
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        try:
            device = self.device
            if device == 'auto':
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
            
            logger.info(f"Loading Whisper model '{self.model_name}' on {device}")
            self.model = whisper.load_model(self.model_name, device=device)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            raise
    
    def transcribe_audio(self, audio_path: Path, 
                        start_time: Optional[float] = None,
                        end_time: Optional[float] = None) -> Dict:
        """Transcribe audio file"""
        if self.model is None:
            raise RuntimeError("Whisper model not loaded")
        
        logger.info(f"Transcribing audio: {audio_path}")
        
        # Prepare transcription options
        options = {
            'language': self.language,
            'temperature': self.temperature,
            'beam_size': self.beam_size,
            'best_of': self.best_of,
            'patience': self.patience,
            'condition_on_previous_text': self.condition_on_previous_text,
        }
        
        if self.initial_prompt:
            options['initial_prompt'] = self.initial_prompt
        
        # Transcribe
        try:
            result = self.model.transcribe(
                str(audio_path),
                **options
            )
            
            # Process result
            transcription = {
                'text': result.get('text', '').strip(),
                'language': result.get('language', self.language),
                'segments': []
            }
            
            # Extract segments with timestamps
            for segment in result.get('segments', []):
                transcription['segments'].append({
                    'start': segment.get('start', 0),
                    'end': segment.get('end', 0),
                    'text': segment.get('text', '').strip(),
                    'no_speech_prob': segment.get('no_speech_prob', 0),
                    'confidence': 1.0 - segment.get('no_speech_prob', 0)
                })
            
            logger.info(f"Transcription complete: {len(transcription['text'])} characters")
            return transcription
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return {
                'text': '',
                'language': self.language,
                'segments': [],
                'error': str(e)
            }
    
    def transcribe_segment(self, audio_path: Path, start_time: float, 
                          end_time: float) -> Dict:
        """Transcribe a specific time segment of audio"""
        # For now, transcribe full audio and filter segments
        # In production, you might want to extract the segment first
        full_transcription = self.transcribe_audio(audio_path)
        
        # Filter segments within time range
        filtered_segments = [
            seg for seg in full_transcription['segments']
            if start_time <= seg['start'] <= end_time or 
               start_time <= seg['end'] <= end_time or
               (seg['start'] <= start_time and seg['end'] >= end_time)
        ]
        
        # Combine text from filtered segments
        text = ' '.join([seg['text'] for seg in filtered_segments])
        
        return {
            'text': text,
            'language': full_transcription['language'],
            'segments': filtered_segments,
            'start_time': start_time,
            'end_time': end_time
        }
    
    def save_transcription(self, transcription: Dict, output_path: Path):
        """Save transcription to file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save as JSON
        json_path = output_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(transcription, f, indent=2, ensure_ascii=False)
        
        # Save as text
        txt_path = output_path.with_suffix('.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(transcription.get('text', ''))
            if transcription.get('segments'):
                f.write('\n\n--- Segments ---\n')
                for seg in transcription['segments']:
                    f.write(f"[{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}\n")
        
        logger.info(f"Saved transcription to {json_path} and {txt_path}")

