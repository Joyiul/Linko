from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from processing.facial_analysis import analyze_facial_features
from processing.video_analysis import analyze_video_facial_features, analyze_video_with_multimodal

facial_routes = Blueprint('facial', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@facial_routes.route('/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze facial features in uploaded image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({'error': 'Invalid file type. Please upload an image file.'}), 400
        
        # Create uploads directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Analyze facial features
        result = analyze_facial_features(filepath)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify({
            'success': True,
            'facial_analysis': result
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@facial_routes.route('/analyze-video-facial', methods=['POST'])
def analyze_video_facial():
    """Analyze facial features in uploaded video"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            return jsonify({'error': 'Invalid file type. Please upload a video file.'}), 400
        
        # Create uploads directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Analyze video facial features
        result = analyze_video_facial_features(filepath)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify({
            'success': True,
            'video_facial_analysis': result
        })
        
    except Exception as e:
        return jsonify({'error': f'Video analysis failed: {str(e)}'}), 500

@facial_routes.route('/multimodal-analysis', methods=['POST'])
def multimodal_analysis():
    """Perform multimodal analysis (audio + video)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            return jsonify({'error': 'Invalid file type. Please upload a video file.'}), 400
        
        # Get optional audio analysis data from request
        audio_transcript = request.form.get('transcript')
        audio_tone = request.form.get('tone')
        
        # Create uploads directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Perform multimodal analysis
        result = analyze_video_with_multimodal(
            filepath, 
            audio_transcript=audio_transcript, 
            audio_tone=audio_tone
        )
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify({
            'success': True,
            'multimodal_analysis': result
        })
        
    except Exception as e:
        return jsonify({'error': f'Multimodal analysis failed: {str(e)}'}), 500

@facial_routes.route('/facial-model-info', methods=['GET'])
def facial_model_info():
    """Get information about the facial analysis model"""
    try:
        from processing.facial_analysis import facial_analyzer
        
        model_loaded = facial_analyzer.model_loaded
        
        return jsonify({
            'model_loaded': model_loaded,
            'model_status': 'Ready' if model_loaded else 'Not loaded',
            'supported_formats': {
                'images': list(ALLOWED_IMAGE_EXTENSIONS),
                'videos': list(ALLOWED_VIDEO_EXTENSIONS)
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Could not get model info: {str(e)}'}), 500
