#!/usr/bin/env python3
"""
Fast Transcription Mode for Wyze Camera Analyzer
Optimized for speed - extracts and transcribes audio from all videos quickly
"""

import argparse
import logging
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
import tempfile
import os
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from tqdm import tqdm
import json
import yaml
from multiprocessing import cpu_count

# Import audio processor for enhancement
from audio_processor import AudioProcessor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('fast_transcribe.log')
    ]
)
logger = logging.getLogger(__name__)


class FastTranscriber:
    """Fast transcription using batch audio processing"""
    
    def __init__(self, use_gpu: bool = True, model_size: str = 'base', 
                 chunk_hours: int = 1, workers: int = None, config_path: str = 'config.yaml',
                 skip_enhancement: bool = False, parallel: int = 1, max_speed: bool = False):
        self.use_gpu = use_gpu
        self.model_size = model_size
        self.chunk_hours = chunk_hours  # Combine videos into N-hour chunks
        self.workers = workers or min(cpu_count(), 4)  # Auto-detect CPU cores
        self.whisper_model = None
        self.skip_enhancement = skip_enhancement
        self.parallel = parallel  # Number of chunks to process in parallel
        self.max_speed = max_speed  # Maximum speed mode - skip all non-essential operations
        
        # Load config and initialize audio processor for enhancement
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except:
            # Default config if file not found
            self.config = {
                'analysis': {
                    'audio': {
                        'sample_rate': 16000,
                        'channels': 1,
                        'bit_depth': 16,
                        'enhancement': {
                            'noise_reduction': True,
                            'amplification': 1.5,
                            'high_pass_filter': 80,
                            'low_pass_filter': 8000,
                            'normalize': True
                        }
                    }
                }
            }
        
        self.audio_processor = AudioProcessor(self.config)
        logger.info("Audio processor initialized for enhancement")
        
    def find_video_files(self, source_path: Path, start_date: datetime = None,
                        end_date: datetime = None) -> List[Path]:
        """Find all video files in source path"""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        video_files = []
        
        source = Path(source_path)
        for ext in video_extensions:
            video_files.extend(source.rglob(f'*{ext}'))
            video_files.extend(source.rglob(f'*{ext.upper()}'))
        
        # Sort by path (Wyze uses YYYYMMDD/HH/MM.mp4 structure)
        video_files.sort(key=lambda x: str(x))
        
        # Filter by date if specified
        if start_date and end_date:
            filtered = []
            for vf in video_files:
                try:
                    # Try to extract date from Wyze path structure: record/YYYYMMDD/HH/MM.mp4
                    parts = str(vf).split('/')
                    file_date = None
                    for part in parts:
                        if len(part) == 8 and part.isdigit():
                            try:
                                file_date = datetime.strptime(part, '%Y%m%d')
                                # Compare dates only (ignore time)
                                if start_date.date() <= file_date.date() <= end_date.date():
                                    filtered.append(vf)
                                break
                            except:
                                pass
                    
                    # If can't parse date from path, use file modification time
                    if file_date is None:
                        mtime = datetime.fromtimestamp(vf.stat().st_mtime)
                        if start_date.date() <= mtime.date() <= end_date.date():
                            filtered.append(vf)
                except Exception as e:
                    # If error, include file anyway to be safe
                    logger.debug(f"Error checking date for {vf}: {e}")
                    filtered.append(vf)
            video_files = filtered
        
        logger.info(f"Found {len(video_files)} video files")
        return video_files
    
    def group_videos_by_hour(self, video_files: List[Path], hours_per_chunk: int = 1) -> dict:
        """Group video files by hour for batch processing"""
        groups = {}
        
        for vf in video_files:
            # Extract date/hour from Wyze path structure: record/YYYYMMDD/HH/MM.mp4
            try:
                parts = str(vf).split('/')
                date_part = None
                hour_part = None
                minute_part = None
                
                for i, part in enumerate(parts):
                    if len(part) == 8 and part.isdigit():
                        date_part = part
                        if i + 1 < len(parts) and len(parts[i+1]) == 2:
                            hour_part = parts[i+1]
                            if i + 2 < len(parts) and len(parts[i+2]) == 2:
                                minute_part = parts[i+2]
                        break
                
                if date_part and hour_part:
                    hour_num = int(hour_part)
                    minute_num = int(minute_part) if minute_part else 0
                    
                    # Group into N-hour chunks
                    if hours_per_chunk >= 1:
                        chunk_hour = (hour_num // hours_per_chunk) * hours_per_chunk
                        key = f"{date_part}_{chunk_hour:02d}"
                    else:
                        # For fractional hours (30min, 15min chunks)
                        total_minutes = hour_num * 60 + minute_num
                        if hours_per_chunk == 0.5:  # 30 minutes
                            chunk_minutes = (total_minutes // 30) * 30
                            chunk_hour = chunk_minutes // 60
                            chunk_min = chunk_minutes % 60
                            key = f"{date_part}_{chunk_hour:02d}_{chunk_min:02d}"
                        elif hours_per_chunk == 0.25:  # 15 minutes
                            chunk_minutes = (total_minutes // 15) * 15
                            chunk_hour = chunk_minutes // 60
                            chunk_min = chunk_minutes % 60
                            key = f"{date_part}_{chunk_hour:02d}_{chunk_min:02d}"
                        elif hours_per_chunk == 0.16666666666666666:  # 10 minutes (1/6 hour)
                            chunk_minutes = (total_minutes // 10) * 10
                            chunk_hour = chunk_minutes // 60
                            chunk_min = chunk_minutes % 60
                            key = f"{date_part}_{chunk_hour:02d}_{chunk_min:02d}"
                        else:
                            key = f"{date_part}_{hour_part}"
                else:
                    key = "unknown"
            except:
                key = "unknown"
            
            if key not in groups:
                groups[key] = []
            groups[key].append(vf)
        
        # Sort files within each group
        for key in groups:
            groups[key].sort(key=lambda x: str(x))
        
        chunk_desc = f"{hours_per_chunk}-hour" if hours_per_chunk >= 1 else f"{int(hours_per_chunk*60)}-minute"
        logger.info(f"Grouped into {len(groups)} {chunk_desc} chunks")
        return groups
    
    def group_videos_by_day(self, video_files: List[Path]) -> dict:
        """Group video files by day for batch processing"""
        groups = {}
        
        for vf in video_files:
            try:
                parts = str(vf).split('/')
                for part in parts:
                    if len(part) == 8 and part.isdigit():
                        key = part
                        break
                else:
                    key = "unknown"
            except:
                key = "unknown"
            
            if key not in groups:
                groups[key] = []
            groups[key].append(vf)
        
        for key in groups:
            groups[key].sort(key=lambda x: str(x))
        
        logger.info(f"Grouped into {len(groups)} daily chunks")
        return groups
    
    def extract_audio_batch(self, video_files: List[Path], output_path: Path) -> bool:
        """Extract and concatenate audio from multiple videos using FFmpeg"""
        if not video_files:
            return False
        
        # Create file list for FFmpeg concat
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            for vf in video_files:
                # Escape single quotes in path
                escaped_path = str(vf).replace("'", "'\\''")
                f.write(f"file '{escaped_path}'\n")
            list_file = f.name
        
        try:
            # Use FFmpeg concat demuxer with optimized settings for speed
            loglevel = 'panic' if self.max_speed else 'error'  # Minimal logging in max speed
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', list_file,
                '-vn',  # No video
                '-acodec', 'pcm_s16le',
                '-ar', '16000',  # 16kHz for Whisper
                '-ac', '1',  # Mono
                '-threads', '0',  # Use all available threads
                '-loglevel', loglevel,  # Minimal logging
                '-fflags', '+fastseek',  # Faster seeking
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=3600)
            
            if result.returncode != 0:
                logger.warning(f"FFmpeg warning: {result.stderr.decode()[:200]}")
            
            return output_path.exists() and output_path.stat().st_size > 0
            
        except subprocess.TimeoutExpired:
            logger.error("Audio extraction timed out")
            return False
        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            return False
        finally:
            os.unlink(list_file)
    
    def load_whisper(self):
        """Load Whisper model"""
        if self.whisper_model is None:
            import whisper
            import torch
            
            device = 'cuda' if self.use_gpu and torch.cuda.is_available() else 'cpu'
            logger.info(f"Loading Whisper model '{self.model_size}' on {device}")
            
            if device == 'cpu' and self.use_gpu:
                logger.warning("GPU requested but CUDA not available, using CPU")
            
            self.whisper_model = whisper.load_model(self.model_size, device=device)
            logger.info("Whisper model loaded")
    
    def quick_speech_check(self, audio_path: Path) -> bool:
        """Quick check if audio likely contains speech (skip transcription if not)"""
        if self.max_speed:
            # In max speed mode, skip the check to save time
            return True
        
        try:
            import librosa
            # In max speed, only check first 5 seconds
            duration = 5.0 if self.max_speed else 10.0
            audio, sr = librosa.load(str(audio_path), sr=16000, duration=duration, mono=True)
            # Calculate energy (faster method)
            rms = librosa.feature.rms(y=audio, frame_length=2048, hop_length=512)[0]
            avg_energy = rms.mean()
            # If very low energy, likely silence
            if avg_energy < 0.001:
                return False
            return True
        except:
            # If check fails, assume there might be speech
            return True
    
    def transcribe_audio(self, audio_path: Path) -> dict:
        """Transcribe audio file using Whisper"""
        self.load_whisper()
        
        # Quick check - skip if likely no speech
        if not self.quick_speech_check(audio_path):
            logger.info(f"Skipping transcription for {audio_path.name} - likely silence")
            return {'text': '', 'segments': [], 'language': 'en', 'skipped': 'silence'}
        
        try:
            # Ultra-fast settings for max speed mode
            no_speech_thresh = 0.7 if self.max_speed else 0.6  # Higher = skip more silence
            logprob_thresh = -0.3 if self.max_speed else -0.5  # Higher = skip more low confidence
            
            result = self.whisper_model.transcribe(
                str(audio_path),
                language='en',
                temperature=0.0,
                beam_size=1,  # Greedy decoding (fastest)
                best_of=1,  # Single pass
                condition_on_previous_text=False,  # Disable to prevent repetition
                initial_prompt=None,  # Remove to prevent hallucinations
                suppress_tokens=[-1],  # Suppress common hallucination tokens
                no_speech_threshold=no_speech_thresh,  # Higher threshold to detect silence
                logprob_threshold=logprob_thresh,  # Higher threshold - skip low confidence
                compression_ratio_threshold=2.4,  # Detect repetitive text
                fp16=False,  # Use FP32 for CPU (faster on CPU)
                verbose=False,  # Less logging for speed
                word_timestamps=False  # Skip word-level timestamps for speed
            )
            
            text = result.get('text', '').strip()
            all_segments = result.get('segments', [])
            
            # Filter segments aggressively - remove repetitive ones
            filtered_segments = []
            seen_phrases = []
            prev_seg_text = None
            
            for seg in all_segments:
                seg_text = seg['text'].strip()
                if not seg_text:
                    continue
                
                # Skip very short segments (likely noise)
                if len(seg_text) < 3:
                    continue
                
                # Normalize text for comparison
                seg_normalized = ' '.join(seg_text.lower().split())
                seg_words = seg_text.split()
                
                # Skip single-word segments that repeat
                if len(seg_words) == 1:
                    # Check if this single word was in recent segments
                    if prev_seg_text and seg_normalized in prev_seg_text.lower():
                        continue
                    # Check if same word appears multiple times in a row
                    if len(filtered_segments) > 0:
                        last_text = filtered_segments[-1]['text'].lower().strip()
                        if last_text == seg_normalized:
                            continue
                
                # Check if segment is too similar to previous segment (adjacent repetition)
                if prev_seg_text:
                    prev_normalized = ' '.join(prev_seg_text.lower().split())
                    if seg_normalized == prev_normalized:
                        continue  # Skip exact duplicates
                    # Check for high similarity with previous
                    if len(seg_normalized) > 5 and len(prev_normalized) > 5:
                        common_words = set(seg_normalized.split()) & set(prev_normalized.split())
                        if len(common_words) / max(len(seg_normalized.split()), len(prev_normalized.split())) > 0.7:
                            continue  # Skip if 70%+ similar to previous
                
                # Check if segment is repetitive within itself
                if len(seg_words) > 2:
                    unique_words = len(set(w.lower() for w in seg_words))
                    if unique_words < len(seg_words) * 0.5:  # Less than 50% unique words
                        continue
                
                # Check against recent seen phrases (last 5)
                is_repetitive = False
                for seen in seen_phrases[-5:]:  # Only check last 5
                    if len(seg_normalized) > 5 and len(seen) > 5:
                        common_words = set(seg_normalized.split()) & set(seen.split())
                        similarity = len(common_words) / max(len(seg_normalized.split()), len(seen.split()))
                        if similarity > 0.75:  # 75%+ similar
                            is_repetitive = True
                            break
                
                if not is_repetitive:
                    filtered_segments.append({
                        'start': seg['start'],
                        'end': seg['end'],
                        'text': seg_text
                    })
                    seen_phrases.append(seg_normalized)
                    prev_seg_text = seg_text
                    # Keep only last 10 unique phrases
                    if len(seen_phrases) > 10:
                        seen_phrases = seen_phrases[-10:]
            
            # Rebuild text from filtered segments
            if filtered_segments:
                text = ' '.join([seg['text'] for seg in filtered_segments])
            else:
                text = ""
                logger.info(f"No valid speech segments found in {audio_path} (likely silence or noise)")
            
            # Final check on full text for excessive repetition
            if text:
                words = text.split()
                if len(words) > 20:
                    # Check for phrase repetition in full text
                    unique_phrases = set()
                    for i in range(len(words) - 3):
                        phrase = ' '.join(words[i:i+4]).lower()
                        unique_phrases.add(phrase)
                    
                    # If too repetitive, clear it
                    if len(unique_phrases) < len(words) / 8:
                        logger.warning(f"Detected excessive repetition in full text for {audio_path}, filtering out")
                        text = ""
                        filtered_segments = []
            
            return {
                'text': text,
                'segments': filtered_segments,
                'language': result.get('language', 'en')
            }
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return {'text': '', 'segments': [], 'error': str(e)}
    
    def process_chunk(self, chunk_name: str, video_files: List[Path], 
                     output_dir: Path) -> dict:
        """Process a chunk of videos (extract audio, enhance, transcribe)"""
        chunk_dir = output_dir / chunk_name
        chunk_dir.mkdir(parents=True, exist_ok=True)
        
        raw_audio_path = chunk_dir / 'audio_raw.wav'
        enhanced_audio_path = chunk_dir / 'audio_enhanced.wav'
        
        # Extract audio
        logger.info(f"Extracting audio for {chunk_name} ({len(video_files)} files)")
        if not self.extract_audio_batch(video_files, raw_audio_path):
            logger.warning(f"Failed to extract audio for {chunk_name}")
            return {'chunk': chunk_name, 'status': 'failed', 'error': 'Audio extraction failed'}
        
        # Enhance audio (noise reduction, amplification, filtering) - optional for speed
        if not self.skip_enhancement:
            logger.info(f"Enhancing audio for {chunk_name} (noise reduction, amplification, filtering)")
            try:
                self.audio_processor.enhance_audio(raw_audio_path, enhanced_audio_path)
                logger.info(f"Audio enhancement complete for {chunk_name}")
                transcription_audio_path = enhanced_audio_path
            except Exception as e:
                logger.warning(f"Audio enhancement failed for {chunk_name}: {e}. Using raw audio.")
                transcription_audio_path = raw_audio_path
        else:
            logger.info(f"Skipping audio enhancement for {chunk_name} (speed mode)")
            transcription_audio_path = raw_audio_path
        
        # Transcribe
        logger.info(f"Transcribing {chunk_name}")
        transcription = self.transcribe_audio(transcription_audio_path)
        
        # Save results
        result = {
            'chunk': chunk_name,
            'video_count': len(video_files),
            'videos': [str(vf) for vf in video_files],
            'transcription': transcription,
            'status': 'completed'
        }
        
        # Save transcription
        transcription_file = chunk_dir / 'transcription.txt'
        with open(transcription_file, 'w') as f:
            f.write(transcription.get('text', ''))
        
        # Save detailed JSON (skip in max speed mode to save I/O time)
        if not self.max_speed:
            with open(chunk_dir / 'transcription.json', 'w') as f:
                json.dump(result, f, indent=2)
        
        # Optionally delete audio files to save space (keep enhanced for reference)
        # raw_audio_path.unlink()
        # enhanced_audio_path.unlink()
        
        return result
    
    def run(self, source_path: str, output_dir: str = './transcriptions',
           start_date: datetime = None, end_date: datetime = None,
           group_by: str = 'hour'):
        """Run fast transcription"""
        source = Path(source_path)
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Fast Transcription Mode")
        logger.info(f"Source: {source}")
        logger.info(f"Output: {output}")
        logger.info(f"Date range: {start_date} to {end_date}")
        logger.info(f"Grouping by: {group_by}")
        
        # Find videos
        video_files = self.find_video_files(source, start_date, end_date)
        
        if not video_files:
            logger.warning("No video files found")
            return
        
        # Group videos
        if group_by == 'day':
            groups = self.group_videos_by_day(video_files)
        elif group_by == '2hour':
            groups = self.group_videos_by_hour(video_files, hours_per_chunk=2)
        elif group_by == '4hour':
            groups = self.group_videos_by_hour(video_files, hours_per_chunk=4)
        elif group_by == '30min':
            groups = self.group_videos_by_hour(video_files, hours_per_chunk=0.5)
        elif group_by == '15min':
            groups = self.group_videos_by_hour(video_files, hours_per_chunk=0.25)
        else:  # hour or default
            groups = self.group_videos_by_hour(video_files, hours_per_chunk=1)
        
        # Estimate time (adjusted for optimizations)
        total_chunks = len(groups)
        if self.skip_enhancement and self.model_size == 'tiny':
            time_per_chunk = 1.0 if self.parallel > 1 else 2.0  # Faster with parallel
            estimated_time = (total_chunks * time_per_chunk) / max(self.parallel, 1)
        else:
            estimated_time = total_chunks * 2
        logger.info(f"Estimated time: {estimated_time:.1f} minutes ({estimated_time/60:.1f} hours)")
        
        # Process chunks (skip already completed ones)
        results = []
        all_text = []
        
        # Get list of chunks to process
        chunks_to_process = []
        for chunk_name in sorted(groups.keys()):
            chunk_dir = output / chunk_name
            transcription_file = chunk_dir / 'transcription.txt'
            
            if transcription_file.exists():
                logger.info(f"Skipping {chunk_name} - already completed")
                # Load existing result
                try:
                    if not self.max_speed:
                        with open(chunk_dir / 'transcription.json', 'r') as f:
                            result = json.load(f)
                    else:
                        # In max speed, just read text file
                        with open(transcription_file, 'r') as f:
                            text = f.read()
                        result = {
                            'chunk': chunk_name,
                            'transcription': {'text': text}
                        }
                    results.append(result)
                    if result.get('transcription', {}).get('text'):
                        all_text.append(f"\n=== {chunk_name} ===\n")
                        all_text.append(result['transcription']['text'])
                    continue
                except:
                    # If can't load, reprocess
                    pass
            
            chunks_to_process.append((chunk_name, groups[chunk_name]))
        
        # Process chunks in parallel if enabled
        if self.parallel > 1 and len(chunks_to_process) > 1:
            logger.info(f"Processing {len(chunks_to_process)} chunks with {self.parallel} parallel workers")
            with ThreadPoolExecutor(max_workers=self.parallel) as executor:
                futures = {
                    executor.submit(self.process_chunk, chunk_name, video_files, output): chunk_name
                    for chunk_name, video_files in chunks_to_process
                }
                
                for future in tqdm(as_completed(futures), total=len(futures), desc="Processing chunks"):
                    chunk_name = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                        if result.get('transcription', {}).get('text'):
                            all_text.append(f"\n=== {chunk_name} ===\n")
                            all_text.append(result['transcription']['text'])
                    except Exception as e:
                        logger.error(f"Error processing {chunk_name}: {e}")
                        results.append({'chunk': chunk_name, 'status': 'error', 'error': str(e)})
        else:
            # Sequential processing
            for chunk_name, video_files in tqdm(chunks_to_process, desc="Processing chunks"):
                try:
                    result = self.process_chunk(chunk_name, video_files, output)
                    results.append(result)
                    
                    if result.get('transcription', {}).get('text'):
                        all_text.append(f"\n=== {chunk_name} ===\n")
                        all_text.append(result['transcription']['text'])
                        
                except Exception as e:
                    logger.error(f"Error processing {chunk_name}: {e}")
                    results.append({'chunk': chunk_name, 'status': 'error', 'error': str(e)})
        
        # Save combined transcription
        with open(output / 'full_transcription.txt', 'w') as f:
            f.write(f"Full Transcription\n")
            f.write(f"Date Range: {start_date} to {end_date}\n")
            f.write(f"Total Chunks: {total_chunks}\n")
            f.write(f"Total Videos: {len(video_files)}\n")
            f.write("=" * 50 + "\n\n")
            f.write('\n'.join(all_text))
        
        # Save summary
        with open(output / 'summary.json', 'w') as f:
            json.dump({
                'source': str(source),
                'date_range': {
                    'start': start_date.isoformat() if start_date else None,
                    'end': end_date.isoformat() if end_date else None
                },
                'total_videos': len(video_files),
                'total_chunks': total_chunks,
                'results': results
            }, f, indent=2)
        
        # Summary
        successful = sum(1 for r in results if r.get('status') == 'completed')
        logger.info(f"\n{'='*50}")
        logger.info(f"Transcription Complete!")
        logger.info(f"Processed: {successful}/{total_chunks} chunks")
        logger.info(f"Results saved to: {output}")
        logger.info(f"Full transcription: {output}/full_transcription.txt")


def main():
    parser = argparse.ArgumentParser(
        description='Fast transcription mode - extracts and transcribes audio quickly'
    )
    parser.add_argument('source', help='Path to video source (SD card)')
    parser.add_argument('--output', '-o', default='./transcriptions',
                       help='Output directory (default: ./transcriptions)')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--model', '-m', default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--group-by', '-g', default='30min',
                       choices=['10min', '15min', '30min', 'hour', '2hour', '4hour', 'day'],
                       help='Group videos by 10min, 15min, 30min, hour, 2-hour, 4-hour, or day chunks (default: 30min)')
    parser.add_argument('--cpu', action='store_true',
                       help='Force CPU mode (no GPU)')
    parser.add_argument('--config', '-c', default='config.yaml',
                       help='Path to config file (default: config.yaml)')
    parser.add_argument('--skip-enhancement', action='store_true',
                       help='Skip audio enhancement for faster processing (may reduce accuracy)')
    parser.add_argument('--parallel', '-p', type=int, default=2,
                       help='Number of chunks to process in parallel (default: 2, max recommended: 4)')
    parser.add_argument('--fast', action='store_true',
                       help='Fast mode: skip enhancement, use tiny model, parallel processing, greedy decoding')
    parser.add_argument('--ultra-fast', action='store_true',
                       help='Ultra-fast mode: all optimizations + skip silent chunks + 15min chunks')
    parser.add_argument('--max-speed', action='store_true',
                       help='MAXIMUM SPEED: all optimizations + max parallel + 10min chunks + minimal I/O')
    
    args = parser.parse_args()
    
    # Parse dates
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d') if args.start_date else None
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d') if args.end_date else None
    
    # Fast mode overrides
    if args.fast:
        args.skip_enhancement = True
        args.model = 'tiny'
        args.parallel = min(4, cpu_count())
        logger.info("🚀 Fast mode enabled: skipping enhancement, using tiny model, parallel processing")
    
    # Ultra-fast mode overrides
    if args.ultra_fast:
        args.skip_enhancement = True
        args.model = 'tiny'
        args.parallel = min(6, cpu_count())
        if args.group_by == '30min':
            args.group_by = '15min'
        logger.info("⚡ Ultra-fast mode enabled: all optimizations + 15min chunks + 6 parallel workers")
    
    # MAX SPEED mode overrides
    if args.max_speed:
        args.skip_enhancement = True
        args.model = 'tiny'
        args.parallel = cpu_count()  # Use ALL CPU cores
        if args.group_by in ['30min', '15min']:
            args.group_by = '10min'  # Even smaller chunks for better parallelization
        logger.info(f"🔥 MAX SPEED mode enabled: ALL optimizations + {args.parallel} parallel workers + 10min chunks + minimal I/O")
    
    # Run
    transcriber = FastTranscriber(
        use_gpu=not args.cpu,
        model_size=args.model,
        config_path=args.config,
        skip_enhancement=args.skip_enhancement,
        parallel=args.parallel,
        max_speed=args.max_speed
    )
    
    transcriber.run(
        args.source,
        args.output,
        start_date,
        end_date,
        args.group_by
    )


if __name__ == '__main__':
    main()

