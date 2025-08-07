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
from processing.video_multimodal_analysis import create_video_multimodal_analyzer

# Import the complete multimodal analyzer
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from complete_multimodal_analysis import MultimodalEmotionAnalyzer

facial_routes = Blueprint('facial_routes', __name__)

# Initialize analyzers
facial_analyzer = FacialFeatureAnalyzer()
multimodal_analyzer = MultimodalEmotionAnalyzer()
video_multimodal_analyzer = create_video_multimodal_analyzer(multimodal_analyzer)

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
    """Analyze emotions in uploaded video using multimodal analysis (facial + audio)."""
    try:
        create_upload_folder()
        
        # Debug logging
        print(f"🔍 DEBUG: Request files: {list(request.files.keys())}")
        print(f"🔍 DEBUG: Request form: {dict(request.form)}")
        print(f"🔍 DEBUG: Content type: {request.content_type}")
        
        if 'video' not in request.files:
            print(f"❌ DEBUG: 'video' key not found in files: {list(request.files.keys())}")
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
        
        # Save uploaded video
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Get fusion strategy from request
            fusion_strategy = request.form.get('fusion_strategy', 'weighted_average')
            if fusion_strategy not in ['weighted_average', 'max_confidence', 'voting']:
                fusion_strategy = 'weighted_average'
            
            # Perform enhanced multimodal video analysis
            results = video_multimodal_analyzer.analyze_video_multimodal(
                filepath, 
                fusion_strategy
            )
            
            # Check for errors
            if 'error' in results:
                return jsonify({
                    'success': False,
                    'error': results['error']
                }), 500
            
            # Extract results
            facial_analysis = results.get('facial_analysis', {})
            audio_analysis = results.get('audio_analysis')
            multimodal_fusion = results.get('multimodal_fusion', {})
            video_info = results.get('video_info', {})
            processing_info = results.get('processing_info', {})
            
            # Format response with comprehensive analysis
            response = {
                'success': True,
                'video_info': video_info,
                'processing_info': processing_info,
                'analysis_results': {
                    'final_emotion': multimodal_fusion.get('final_emotion', 'neutral'),
                    'confidence': multimodal_fusion.get('confidence', 0.0),
                    'fusion_method': multimodal_fusion.get('fusion_method', 'unknown'),
                    'modalities_agreement': multimodal_fusion.get('modalities_agreement'),
                    
                    # Facial analysis results
                    'facial_analysis': {
                        'frames_analyzed': facial_analysis.get('frames_analyzed', 0),
                        'faces_detected_total': facial_analysis.get('faces_detected_total', 0),
                        'dominant_emotion': facial_analysis.get('dominant_emotion'),
                        'facial_confidence': facial_analysis.get('confidence'),
                        'emotion_distribution': facial_analysis.get('emotion_distribution', {}),
                        'frame_by_frame': facial_analysis.get('frame_results', [])
                    },
                    
                    # Audio analysis results
                    'audio_analysis': {
                        'analyzed': audio_analysis is not None,
                        'emotion': audio_analysis.get('emotion') if audio_analysis else None,
                        'confidence': audio_analysis.get('confidence') if audio_analysis else None,
                        'analysis_method': audio_analysis.get('analysis_method') if audio_analysis else None,
                        'all_predictions': audio_analysis.get('all_predictions', {}) if audio_analysis else {}
                    },
                    
                    # Multimodal fusion details
                    'multimodal_details': {
                        'facial_contribution': multimodal_fusion.get('facial_contribution'),
                        'audio_contribution': multimodal_fusion.get('audio_contribution'),
                        'fusion_strategy': fusion_strategy,
                        'modalities_used': []
                    }
                }
            }
            
            # Determine which modalities were successfully used
            if facial_analysis.get('faces_detected_total', 0) > 0:
                response['analysis_results']['multimodal_details']['modalities_used'].append('facial')
            if audio_analysis and audio_analysis.get('emotion'):
                response['analysis_results']['multimodal_details']['modalities_used'].append('audio')
            
            # Generate comprehensive summary
            summary_parts = []
            if multimodal_fusion.get('final_emotion'):
                final_emotion = multimodal_fusion['final_emotion']
                confidence = multimodal_fusion.get('confidence', 0)
                summary_parts.append(f"Overall emotion detected: {final_emotion} (confidence: {confidence:.2f})")
            
            if processing_info.get('audio_extracted') and processing_info.get('audio_analyzed'):
                summary_parts.append("Both facial expressions and audio were analyzed for comprehensive results")
            elif facial_analysis.get('faces_detected_total', 0) > 0:
                summary_parts.append("Facial expression analysis completed successfully")
            elif processing_info.get('audio_analyzed'):
                summary_parts.append("Audio emotion analysis completed")
            else:
                summary_parts.append("Video processed - limited emotion detection")
            
            response['summary'] = ". ".join(summary_parts) if summary_parts else "Video analysis completed"
            
            return jsonify(response)
            
        finally:
            # Clean up uploaded video file
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Clean up any temporary files from processing
            video_multimodal_analyzer.cleanup_temp_files()
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Video analysis failed: {str(e)}'
        }), 500

@facial_routes.route('/analyze-video-multimodal', methods=['POST'])
def analyze_video_multimodal():
    """Enhanced video analysis with explicit multimodal processing for research and advanced use cases."""
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
                'error': 'Invalid video file type'
            }), 400
        
        # Save uploaded video
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Get advanced parameters
            fusion_strategy = request.form.get('fusion_strategy', 'weighted_average')
            max_frames = int(request.form.get('max_frames', 30))
            skip_frames = int(request.form.get('skip_frames', 10))
            include_frame_details = request.form.get('include_frame_details', 'true').lower() == 'true'
            
            if fusion_strategy not in ['weighted_average', 'max_confidence', 'voting']:
                fusion_strategy = 'weighted_average'
            
            # Perform comprehensive multimodal analysis
            results = video_multimodal_analyzer.analyze_video_multimodal(
                filepath, 
                fusion_strategy
            )
            
            if 'error' in results:
                return jsonify({
                    'success': False,
                    'error': results['error']
                }), 500
            
            # Enhanced response with detailed breakdown
            facial_analysis = results.get('facial_analysis', {})
            audio_analysis = results.get('audio_analysis')
            multimodal_fusion = results.get('multimodal_fusion', {})
            video_info = results.get('video_info', {})
            processing_info = results.get('processing_info', {})
            
            response = {
                'success': True,
                'analysis_type': 'comprehensive_multimodal',
                'video_metadata': video_info,
                'processing_details': processing_info,
                
                # Final multimodal results
                'final_analysis': {
                    'emotion': multimodal_fusion.get('final_emotion', 'neutral'),
                    'confidence': round(multimodal_fusion.get('confidence', 0.0), 4),
                    'fusion_method': multimodal_fusion.get('fusion_method', 'unknown'),
                    'modalities_agreement': multimodal_fusion.get('modalities_agreement'),
                    'analysis_quality': 'high' if multimodal_fusion.get('confidence', 0) > 0.7 else 'medium' if multimodal_fusion.get('confidence', 0) > 0.4 else 'low'
                },
                
                # Detailed facial analysis
                'facial_emotion_analysis': {
                    'summary': {
                        'frames_processed': facial_analysis.get('frames_analyzed', 0),
                        'total_faces_detected': facial_analysis.get('faces_detected_total', 0),
                        'dominant_emotion': facial_analysis.get('dominant_emotion'),
                        'average_confidence': facial_analysis.get('confidence'),
                        'emotion_distribution': facial_analysis.get('emotion_distribution', {})
                    },
                    'temporal_analysis': facial_analysis.get('frame_results', []) if include_frame_details else []
                },
                
                # Detailed audio analysis
                'audio_emotion_analysis': {
                    'processed': audio_analysis is not None,
                    'emotion_detected': audio_analysis.get('emotion') if audio_analysis else None,
                    'confidence': round(audio_analysis.get('confidence', 0), 4) if audio_analysis else None,
                    'analysis_method': audio_analysis.get('analysis_method') if audio_analysis else None,
                    'emotion_probabilities': audio_analysis.get('all_predictions', {}) if audio_analysis else {}
                },
                
                # Fusion analysis
                'multimodal_fusion_details': {
                    'strategy_used': fusion_strategy,
                    'facial_contribution': multimodal_fusion.get('facial_contribution'),
                    'audio_contribution': multimodal_fusion.get('audio_contribution'),
                    'modalities_analyzed': [],
                    'fusion_confidence': round(multimodal_fusion.get('confidence', 0), 4),
                    'agreement_score': 1.0 if multimodal_fusion.get('modalities_agreement') else 0.0 if multimodal_fusion.get('modalities_agreement') is False else None
                }
            }
            
            # Determine analyzed modalities
            if facial_analysis.get('faces_detected_total', 0) > 0:
                response['multimodal_fusion_details']['modalities_analyzed'].append('facial_expressions')
            if audio_analysis and audio_analysis.get('emotion'):
                response['multimodal_fusion_details']['modalities_analyzed'].append('audio_prosody')
            
            # Research-grade summary
            modalities = response['multimodal_fusion_details']['modalities_analyzed']
            final_emotion = response['final_analysis']['emotion']
            confidence = response['final_analysis']['confidence']
            
            if len(modalities) == 2:
                agreement = "with agreement" if response['multimodal_fusion_details']['agreement_score'] == 1.0 else "with disagreement"
                summary = f"Multimodal analysis using {' and '.join(modalities)} detected {final_emotion} emotion (confidence: {confidence:.2f}) {agreement} between modalities"
            elif len(modalities) == 1:
                summary = f"Single-modality analysis using {modalities[0]} detected {final_emotion} emotion (confidence: {confidence:.2f})"
            else:
                summary = f"Limited analysis completed - {final_emotion} emotion detected with low confidence ({confidence:.2f})"
            
            response['research_summary'] = summary
            
            return jsonify(response)
            
        finally:
            # Cleanup
            if os.path.exists(filepath):
                os.remove(filepath)
            video_multimodal_analyzer.cleanup_temp_files()
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Multimodal video analysis failed: {str(e)}'
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

@facial_routes.route('/upload', methods=['POST'])
def upload_audio():
    """Handle audio file upload and perform speech-to-text conversion."""
    try:
        create_upload_folder()
        
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No audio file selected'
            }), 400
        
        # Save uploaded audio
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # For now, provide a basic transcript as speech-to-text is not implemented
            # In a production system, you would use services like Google Speech-to-Text,
            # Azure Speech Services, or implement Whisper for local processing
            
            transcript = "Audio transcript would appear here in a production system with speech-to-text capabilities."
            
            # Provide encouraging feedback for audio submission
            response = {
                'success': True,
                'transcript': transcript,
                'message': 'Audio received successfully',
                'audio_info': {
                    'filename': file.filename,
                    'size': os.path.getsize(filepath),
                    'format': 'webm'
                }
            }
            
            return jsonify(response)
            
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Audio processing failed: {str(e)}'
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
