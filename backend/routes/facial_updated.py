#!/usr/bin/env python3
"""
Facial emotion analysis routes for the ImmigrantSlangster backend.
Handles image upload, facial emotion detection, and multimodal analysis integration.
"""

from flask import Blueprint, request, jsonify
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import tempfile
import uuid
from processing.facial_analysis import FacialFeatureAnalyzer

# Import the complete multimodal analyzer
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from complete_multimodal_analysis import MultimodalEmotionAnalyzer

facial_routes = Blueprint('facial_routes', __name__)

# Initialize analyzers
facial_analyzer = FacialFeatureAnalyzer()
multimodal_analyzer = MultimodalEmotionAnalyzer()

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg', 'm4a'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

def allowed_file(filename, extensions):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def create_upload_folder():
    """Ensure upload folder exists."""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@facial_routes.route('/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze facial emotion in uploaded image."""
    try:
        create_upload_folder()
        
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No image file selected'
            }), 400
        
        if not allowed_file(file.filename, ALLOWED_EXTENSIONS):
            return jsonify({
                'success': False,
                'error': 'Invalid image file type'
            }), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Analyze facial emotion using the new multimodal analyzer
            facial_results = multimodal_analyzer.analyze_facial_emotion(filepath)
            
            if not facial_results:
                return jsonify({
                    'success': True,
                    'faces_detected': 0,
                    'message': 'No faces detected in the image',
                    'results': []
                })
            
            # Format results for API response
            formatted_results = []
            for result in facial_results:
                formatted_results.append({
                    'face_id': result['face_id'],
                    'bounding_box': {
                        'x': int(result['bbox'][0]),
                        'y': int(result['bbox'][1]),
                        'width': int(result['bbox'][2]),
                        'height': int(result['bbox'][3])
                    },
                    'emotion': result['emotion'],
                    'confidence': round(result['confidence'], 4),
                    'all_predictions': {k: round(v, 4) for k, v in result['all_predictions'].items()}
                })
            
            return jsonify({
                'success': True,
                'faces_detected': len(facial_results),
                'results': formatted_results,
                'primary_emotion': formatted_results[0]['emotion'] if formatted_results else 'none',
                'primary_confidence': formatted_results[0]['confidence'] if formatted_results else 0.0
            })
            
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@facial_routes.route('/analyze-video', methods=['POST'])
def analyze_video():
    """Analyze facial emotion in uploaded video."""
    try:
        create_upload_folder()
        
        if 'video' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No video file provided'
            }), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No video file selected'
            }), 400
        
        if not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            return jsonify({
                'success': False,
                'error': 'Invalid video file type. Supported formats: mp4, avi, mov, mkv, webm'
            }), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Extract frames from video and analyze each
            import cv2
            
            cap = cv2.VideoCapture(filepath)
            frame_results = []
            frame_count = 0
            max_frames = 30  # Analyze up to 30 frames
            skip_frames = 10  # Skip frames to speed up processing
            
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            current_frame = 0
            while cap.read()[0] and len(frame_results) < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if current_frame % skip_frames == 0:
                    # Save frame temporarily for analysis
                    frame_filename = f"temp_frame_{current_frame}.jpg"
                    frame_filepath = os.path.join(UPLOAD_FOLDER, frame_filename)
                    cv2.imwrite(frame_filepath, frame)
                    
                    try:
                        # Analyze this frame
                        frame_analysis = multimodal_analyzer.analyze_facial_emotion(frame_filepath)
                        
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
            
            if not frame_results:
                return jsonify({
                    'success': True,
                    'message': 'No faces detected in video',
                    'video_info': {
                        'total_frames': total_frames,
                        'fps': fps,
                        'duration_seconds': round(total_frames / fps, 2)
                    },
                    'analysis_results': {
                        'frames_analyzed': 0,
                        'faces_detected_total': 0,
                        'dominant_emotion': 'none',
                        'confidence': 0.0
                    }
                })
            
            # Aggregate results
            all_emotions = [result['primary_emotion'] for result in frame_results]
            all_confidences = [result['confidence'] for result in frame_results]
            
            # Find most common emotion
            from collections import Counter
            emotion_counts = Counter(all_emotions)
            dominant_emotion = emotion_counts.most_common(1)[0][0]
            
            # Calculate average confidence for dominant emotion
            dominant_confidences = [conf for emotion, conf in zip(all_emotions, all_confidences) 
                                  if emotion == dominant_emotion]
            avg_confidence = sum(dominant_confidences) / len(dominant_confidences)
            
            return jsonify({
                'success': True,
                'video_info': {
                    'total_frames': total_frames,
                    'fps': fps,
                    'duration_seconds': round(total_frames / fps, 2)
                },
                'analysis_results': {
                    'frames_analyzed': len(frame_results),
                    'faces_detected_total': sum(r['faces_detected'] for r in frame_results),
                    'dominant_emotion': dominant_emotion,
                    'confidence': round(avg_confidence, 4),
                    'emotion_distribution': dict(emotion_counts),
                    'frame_by_frame': frame_results
                },
                'summary': f"Analyzed {len(frame_results)} frames. Dominant emotion: {dominant_emotion} ({avg_confidence:.1%} confidence)"
            })
            
        finally:
            # Clean up uploaded video file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Video analysis failed: {str(e)}'
        }), 500

@facial_routes.route('/multimodal-analysis', methods=['POST'])
def multimodal_analysis():
    """Perform complete multimodal emotion analysis with image and optional audio."""
    try:
        create_upload_folder()
        
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        image_file = request.files['image']
        audio_file = request.files.get('audio')  # Optional audio file
        
        if image_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No image file selected'
            }), 400
        
        if not allowed_file(image_file.filename, ALLOWED_EXTENSIONS):
            return jsonify({
                'success': False,
                'error': 'Invalid image file type'
            }), 400
        
        # Save image file
        image_filename = secure_filename(f"{uuid.uuid4()}_{image_file.filename}")
        image_filepath = os.path.join(UPLOAD_FOLDER, image_filename)
        image_file.save(image_filepath)
        
        audio_filepath = None
        if audio_file and audio_file.filename != '' and allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
            audio_filename = secure_filename(f"{uuid.uuid4()}_{audio_file.filename}")
            audio_filepath = os.path.join(UPLOAD_FOLDER, audio_filename)
            audio_file.save(audio_filepath)
        
        try:
            # Get fusion strategy from request
            fusion_strategy = request.form.get('fusion_strategy', 'weighted_average')
            if fusion_strategy not in ['weighted_average', 'max_confidence', 'voting']:
                fusion_strategy = 'weighted_average'
            
            # Perform multimodal analysis
            results = multimodal_analyzer.analyze_multimodal(
                image_filepath, 
                audio_filepath, 
                fusion_strategy
            )
            
            if not results:
                return jsonify({
                    'success': False,
                    'error': 'Multimodal analysis failed'
                }), 500
            
            # Format response
            response = {
                'success': True,
                'final_prediction': {
                    'emotion': results['final_prediction']['emotion'],
                    'confidence': round(results['final_prediction']['confidence'], 4),
                    'fusion_method': results['final_prediction']['fusion_method']
                },
                'facial_analysis': {
                    'faces_detected': results['facial_analysis']['faces_detected'],
                    'faces': [{
                        'emotion': face['emotion'],
                        'confidence': round(face['confidence'], 4),
                        'bounding_box': {
                            'x': int(face['bbox'][0]),
                            'y': int(face['bbox'][1]),
                            'width': int(face['bbox'][2]),
                            'height': int(face['bbox'][3])
                        }
                    } for face in results['facial_analysis']['results']]
                },
                'audio_analysis': {
                    'analyzed': audio_filepath is not None,
                    'emotion': results['audio_analysis']['emotion'],
                    'confidence': round(results['audio_analysis']['confidence'], 4) if results['audio_analysis']['confidence'] else None
                },
                'fusion_strategy': fusion_strategy,
                'modalities_used': []
            }
            
            # Determine which modalities were used
            if results['facial_analysis']['faces_detected'] > 0:
                response['modalities_used'].append('facial')
            if results['audio_analysis']['emotion']:
                response['modalities_used'].append('audio')
            
            return jsonify(response)
            
        finally:
            # Clean up uploaded files
            if os.path.exists(image_filepath):
                os.remove(image_filepath)
            if audio_filepath and os.path.exists(audio_filepath):
                os.remove(audio_filepath)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Multimodal analysis failed: {str(e)}'
        }), 500

@facial_routes.route('/facial-test', methods=['GET'])
def facial_test():
    """Test endpoint to verify facial analysis system."""
    try:
        # Test with a sample image from dataset
        test_images = []
        
        # Look for test images in dataset
        dataset_paths = [
            "Datasets/archive/test",
            "archive/test"
        ]
        
        for dataset_path in dataset_paths:
            if os.path.exists(dataset_path):
                for emotion_dir in os.listdir(dataset_path):
                    emotion_path = os.path.join(dataset_path, emotion_dir)
                    if os.path.isdir(emotion_path):
                        images = [f for f in os.listdir(emotion_path) if f.endswith('.jpg')]
                        if images:
                            test_images.append({
                                'path': os.path.join(emotion_path, images[0]),
                                'expected_emotion': emotion_dir
                            })
                            if len(test_images) >= 3:  # Test with first 3 emotions
                                break
                break
        
        if not test_images:
            return jsonify({
                'success': True,
                'message': 'Facial analysis system is loaded but no test images available',
                'system_status': {
                    'facial_model_loaded': multimodal_analyzer.facial_model is not None,
                    'audio_model_loaded': multimodal_analyzer.audio_model is not None,
                    'facial_encoder_loaded': multimodal_analyzer.facial_encoder is not None,
                    'audio_encoder_loaded': multimodal_analyzer.audio_encoder is not None
                }
            })
        
        # Test with available images
        test_results = []
        for test_image in test_images:
            results = multimodal_analyzer.analyze_facial_emotion(test_image['path'])
            
            test_results.append({
                'expected_emotion': test_image['expected_emotion'],
                'faces_detected': len(results),
                'predicted_emotion': results[0]['emotion'] if results else 'none',
                'confidence': round(results[0]['confidence'], 4) if results else 0.0,
                'correct_prediction': results and results[0]['emotion'] == test_image['expected_emotion']
            })
        
        accuracy = sum(1 for r in test_results if r['correct_prediction']) / len(test_results)
        
        return jsonify({
            'success': True,
            'system_status': {
                'facial_model_loaded': multimodal_analyzer.facial_model is not None,
                'audio_model_loaded': multimodal_analyzer.audio_model is not None,
                'facial_encoder_loaded': multimodal_analyzer.facial_encoder is not None,
                'audio_encoder_loaded': multimodal_analyzer.audio_encoder is not None
            },
            'test_results': test_results,
            'accuracy': round(accuracy, 4),
            'message': f'Facial analysis test completed with {accuracy*100:.1f}% accuracy'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Test failed: {str(e)}'
        }), 500

@facial_routes.route('/system-info', methods=['GET'])
def system_info():
    """Get system information and model details."""
    try:
        return jsonify({
            'success': True,
            'system_info': {
                'facial_emotion_recognition': {
                    'model_loaded': multimodal_analyzer.facial_model is not None,
                    'emotions_supported': multimodal_analyzer.facial_emotions,
                    'model_accuracy': '50.65% (trained on 1000 images per class)',
                    'input_size': '48x48 grayscale images',
                    'architecture': 'CNN with BatchNormalization and Dropout'
                },
                'audio_emotion_recognition': {
                    'model_loaded': multimodal_analyzer.audio_model is not None,
                    'emotions_supported': multimodal_analyzer.audio_emotions,
                    'features_used': 'MFCC, Chroma, Mel-spectrogram, Spectral contrast, Tonnetz',
                    'status': 'Functional with fallback encoder'
                },
                'multimodal_fusion': {
                    'strategies_available': ['weighted_average', 'max_confidence', 'voting'],
                    'default_strategy': 'weighted_average',
                    'facial_weight': 0.6,
                    'audio_weight': 0.4
                },
                'api_endpoints': {
                    '/analyze-image': 'Analyze facial emotion in single image',
                    '/multimodal-analysis': 'Complete multimodal analysis with image and audio',
                    '/facial-test': 'Test system with sample images',
                    '/system-info': 'Get system information'
                }
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get system info: {str(e)}'
        }), 500
