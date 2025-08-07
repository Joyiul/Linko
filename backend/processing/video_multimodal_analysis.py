#!/usr/bin/env python3
"""
Enhanced Video Multimodal Analysis
Combines facial emotion recognition with audio analysis from video files.
"""

import os
import cv2
import numpy as np
import librosa
import tempfile
import subprocess
from typing import Dict, List, Tuple, Optional
import uuid
from collections import Counter
import datetime

class VideoMultimodalAnalyzer:
    """Enhanced video analyzer that processes both facial expressions and audio."""
    
    def __init__(self, multimodal_analyzer):
        self.multimodal_analyzer = multimodal_analyzer
        self.temp_dir = tempfile.gettempdir()
        
    def extract_audio_from_video(self, video_path: str) -> Optional[str]:
        """Extract audio from video file using FFmpeg."""
        try:
            # Create temporary audio file
            audio_filename = f"extracted_audio_{uuid.uuid4().hex}.wav"
            audio_path = os.path.join(self.temp_dir, audio_filename)
            
            # Use FFmpeg to extract audio
            # Check if ffmpeg exists in the backend directory first
            current_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.dirname(current_dir)
            ffmpeg_path = os.path.join(backend_dir, 'ffmpeg')
            
            if not os.path.exists(ffmpeg_path):
                ffmpeg_path = 'ffmpeg'  # Use system ffmpeg
                
            print(f"Using FFmpeg at: {ffmpeg_path}")
            
            cmd = [
                ffmpeg_path,
                '-i', video_path,
                '-vn',  # No video
                '-acodec', 'pcm_s16le',  # Audio codec
                '-ar', '22050',  # Sample rate
                '-ac', '1',  # Mono
                '-y',  # Overwrite output file
                audio_path
            ]
            
            # Run FFmpeg command
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(audio_path):
                print(f"✅ Audio extracted successfully: {audio_path}")
                return audio_path
            else:
                print(f"❌ FFmpeg failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Audio extraction timeout")
            return None
        except Exception as e:
            print(f"❌ Audio extraction error: {str(e)}")
            return None
    
    def analyze_video_frames(self, video_path: str, max_frames: int = 30, skip_frames: int = 10) -> List[Dict]:
        """Analyze facial emotions in video frames."""
        try:
            cap = cv2.VideoCapture(video_path)
            frame_results = []
            
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            current_frame = 0
            while cap.read()[0] and len(frame_results) < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if current_frame % skip_frames == 0:
                    # Save frame temporarily for analysis
                    frame_filename = f"temp_frame_{uuid.uuid4().hex}.jpg"
                    frame_filepath = os.path.join(self.temp_dir, frame_filename)
                    cv2.imwrite(frame_filepath, frame)
                    
                    try:
                        # Analyze this frame using the multimodal analyzer
                        frame_analysis = self.multimodal_analyzer.analyze_facial_emotion(frame_filepath)
                        
                        if frame_analysis:
                            timestamp = current_frame / fps
                            frame_results.append({
                                'frame_number': current_frame,
                                'timestamp': round(timestamp, 2),
                                'faces_detected': len(frame_analysis),
                                'primary_emotion': frame_analysis[0]['emotion'],
                                'confidence': round(frame_analysis[0]['confidence'], 4),
                                'all_faces': [{
                                    'emotion': face['emotion'],
                                    'confidence': round(face['confidence'], 4),
                                    'bounding_box': {
                                        'x': int(face['bbox'][0]),
                                        'y': int(face['bbox'][1]),
                                        'width': int(face['bbox'][2]),
                                        'height': int(face['bbox'][3])
                                    }
                                } for face in frame_analysis]
                            })
                    
                    finally:
                        # Clean up frame file
                        if os.path.exists(frame_filepath):
                            os.remove(frame_filepath)
                
                current_frame += 1
            
            cap.release()
            
            return frame_results, {
                'total_frames': total_frames,
                'fps': fps,
                'duration_seconds': round(total_frames / fps, 2) if fps > 0 else 0
            }
            
        except Exception as e:
            print(f"❌ Video frame analysis error: {str(e)}")
            return [], {}
    
    def analyze_extracted_audio(self, audio_path: str) -> Optional[Dict]:
        """Analyze emotions from extracted audio."""
        try:
            if not os.path.exists(audio_path):
                return None
            
            # Use the multimodal analyzer's audio analysis
            emotion, confidence, all_predictions = self.multimodal_analyzer.analyze_audio_emotion(audio_path)
            
            if emotion:
                return {
                    'emotion': emotion,
                    'confidence': confidence,
                    'all_predictions': all_predictions,
                    'analysis_method': 'audio_features'
                }
            else:
                return None
                
        except Exception as e:
            print(f"❌ Audio analysis error: {str(e)}")
            return None
    
    def fuse_video_multimodal_results(self, facial_results: List[Dict], audio_result: Optional[Dict], 
                                    fusion_strategy: str = 'weighted_average') -> Dict:
        """Fuse facial and audio analysis results from video."""
        try:
            result = {
                'facial_analysis': {
                    'frames_analyzed': len(facial_results),
                    'faces_detected_total': sum(r['faces_detected'] for r in facial_results),
                    'frame_results': facial_results
                },
                'audio_analysis': audio_result,
                'multimodal_fusion': None,
                'fusion_strategy': fusion_strategy
            }
            
            # Calculate dominant facial emotion
            facial_emotion = None
            facial_confidence = 0.0
            
            if facial_results:
                all_emotions = [r['primary_emotion'] for r in facial_results]
                emotion_counts = Counter(all_emotions)
                facial_emotion = emotion_counts.most_common(1)[0][0]
                
                # Calculate average confidence for dominant emotion
                dominant_confidences = [r['confidence'] for r in facial_results 
                                      if r['primary_emotion'] == facial_emotion]
                facial_confidence = sum(dominant_confidences) / len(dominant_confidences)
                
                result['facial_analysis'].update({
                    'dominant_emotion': facial_emotion,
                    'confidence': round(facial_confidence, 4),
                    'emotion_distribution': dict(emotion_counts)
                })
            
            # Perform multimodal fusion if both modalities are available
            if facial_emotion and audio_result and audio_result.get('emotion'):
                audio_emotion = audio_result['emotion']
                audio_confidence = audio_result['confidence']
                
                # Use the existing fusion logic from multimodal analyzer
                final_emotion, final_confidence, fusion_method = self.multimodal_analyzer.fuse_emotions(
                    [{'emotion': facial_emotion, 'confidence': facial_confidence, 'bbox': (0, 0, 0, 0)}],
                    (audio_emotion, audio_confidence, {}),
                    fusion_strategy
                )
                
                result['multimodal_fusion'] = {
                    'final_emotion': final_emotion,
                    'confidence': round(final_confidence, 4),
                    'fusion_method': fusion_method,
                    'modalities_agreement': facial_emotion == audio_emotion,
                    'facial_contribution': facial_emotion,
                    'audio_contribution': audio_emotion
                }
            
            elif facial_emotion and not audio_result:
                # Facial only
                result['multimodal_fusion'] = {
                    'final_emotion': facial_emotion,
                    'confidence': round(facial_confidence, 4),
                    'fusion_method': 'facial_only',
                    'modalities_agreement': None,
                    'facial_contribution': facial_emotion,
                    'audio_contribution': None
                }
            
            elif audio_result and not facial_emotion:
                # Audio only
                result['multimodal_fusion'] = {
                    'final_emotion': audio_result['emotion'],
                    'confidence': round(audio_result['confidence'], 4),
                    'fusion_method': 'audio_only',
                    'modalities_agreement': None,
                    'facial_contribution': None,
                    'audio_contribution': audio_result['emotion']
                }
            
            else:
                # No valid analysis
                result['multimodal_fusion'] = {
                    'final_emotion': 'neutral',
                    'confidence': 0.3,
                    'fusion_method': 'fallback',
                    'modalities_agreement': None,
                    'facial_contribution': None,
                    'audio_contribution': None
                }
            
            return result
            
        except Exception as e:
            print(f"❌ Fusion error: {str(e)}")
            return {
                'facial_analysis': {'frames_analyzed': 0, 'faces_detected_total': 0},
                'audio_analysis': None,
                'multimodal_fusion': {
                    'final_emotion': 'neutral',
                    'confidence': 0.3,
                    'fusion_method': 'error',
                    'error': str(e)
                }
            }
    
    def analyze_video_multimodal(self, video_path: str, fusion_strategy: str = 'weighted_average') -> Dict:
        """Complete multimodal analysis of video file."""
        try:
            print(f"🎥 Starting multimodal video analysis: {video_path}")
            
            # Extract audio from video
            print("🎵 Extracting audio from video...")
            audio_path = self.extract_audio_from_video(video_path)
            
            # Analyze video frames for facial emotions
            print("😊 Analyzing facial emotions in video frames...")
            frame_results, video_info = self.analyze_video_frames(video_path)
            
            # Analyze extracted audio
            audio_result = None
            if audio_path:
                print("🎧 Analyzing audio emotions...")
                audio_result = self.analyze_extracted_audio(audio_path)
                
                # Clean up temporary audio file
                try:
                    os.remove(audio_path)
                except:
                    pass
            else:
                print("⚠️ No audio extracted - proceeding with facial-only analysis")
            
            # Fuse results
            print("🔄 Fusing multimodal results...")
            final_results = self.fuse_video_multimodal_results(
                frame_results, audio_result, fusion_strategy
            )
            
            # Add video metadata
            final_results['video_info'] = video_info
            final_results['processing_info'] = {
                'audio_extracted': audio_path is not None,
                'audio_analyzed': audio_result is not None,
                'facial_frames_analyzed': len(frame_results),
                'analysis_timestamp': datetime.datetime.now().isoformat()
            }
            
            print("✅ Multimodal video analysis completed")
            return final_results
            
        except Exception as e:
            print(f"❌ Multimodal video analysis failed: {str(e)}")
            return {
                'error': f"Multimodal analysis failed: {str(e)}",
                'facial_analysis': {'frames_analyzed': 0, 'faces_detected_total': 0},
                'audio_analysis': None,
                'multimodal_fusion': {
                    'final_emotion': 'neutral',
                    'confidence': 0.3,
                    'fusion_method': 'error'
                }
            }
    
    def cleanup_temp_files(self):
        """Clean up any remaining temporary files."""
        try:
            temp_pattern = os.path.join(self.temp_dir, "temp_frame_*.jpg")
            audio_pattern = os.path.join(self.temp_dir, "extracted_audio_*.wav")
            
            import glob
            for pattern in [temp_pattern, audio_pattern]:
                for file_path in glob.glob(pattern):
                    try:
                        os.remove(file_path)
                    except:
                        pass
        except Exception as e:
            print(f"⚠️ Cleanup warning: {str(e)}")


def create_video_multimodal_analyzer(multimodal_analyzer):
    """Factory function to create a video multimodal analyzer."""
    return VideoMultimodalAnalyzer(multimodal_analyzer)
