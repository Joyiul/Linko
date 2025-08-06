from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import json

learning_library_bp = Blueprint('learning_library', __name__)

# Directory to store uploaded learning videos
LEARNING_UPLOAD_FOLDER = 'learning_videos'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_directory():
    """Ensure the learning videos directory exists"""
    if not os.path.exists(LEARNING_UPLOAD_FOLDER):
        os.makedirs(LEARNING_UPLOAD_FOLDER)

@learning_library_bp.route('/upload', methods=['POST'])
def upload_learning_video():
    """Upload a video to the learning library"""
    try:
        ensure_upload_directory()
        
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Please upload MP4, AVI, MOV, MKV, or WEBM files.'}), 400
        
        # Get metadata from form
        title = request.form.get('title', 'Untitled Video')
        emotion = request.form.get('emotion', 'neutral')
        difficulty = request.form.get('difficulty', 'beginner')
        speaker_accent = request.form.get('speaker_accent', 'unknown')
        speaker_gender = request.form.get('speaker_gender', 'unknown')
        description = request.form.get('description', '')
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{file_id}.{file_extension}"
        
        # Save file
        filepath = os.path.join(LEARNING_UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # Create metadata entry
        video_metadata = {
            'id': file_id,
            'title': title,
            'emotion': emotion,
            'difficulty': difficulty,
            'speaker_accent': speaker_accent,
            'speaker_gender': speaker_gender,
            'description': description,
            'filename': unique_filename,
            'original_filename': filename,
            'upload_date': datetime.now().isoformat(),
            'file_size': os.path.getsize(filepath),
            'analyzed': False
        }
        
        # Save metadata to JSON file (in production, use a database)
        metadata_file = os.path.join(LEARNING_UPLOAD_FOLDER, 'videos_metadata.json')
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                metadata_list = json.load(f)
        else:
            metadata_list = []
        
        metadata_list.append(video_metadata)
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata_list, f, indent=2)
        
        return jsonify({
            'message': 'Video uploaded successfully',
            'video_id': file_id,
            'metadata': video_metadata
        }), 201
        
    except Exception as e:
        print(f"Error uploading learning video: {str(e)}")
        return jsonify({'error': 'Failed to upload video'}), 500

@learning_library_bp.route('/videos', methods=['GET'])
def get_learning_videos():
    """Get all videos in the learning library"""
    try:
        metadata_file = os.path.join(LEARNING_UPLOAD_FOLDER, 'videos_metadata.json')
        
        if not os.path.exists(metadata_file):
            return jsonify({'videos': []}), 200
        
        with open(metadata_file, 'r') as f:
            videos = json.load(f)
        
        # Filter by query parameters if provided
        emotion_filter = request.args.get('emotion')
        difficulty_filter = request.args.get('difficulty')
        accent_filter = request.args.get('accent')
        
        if emotion_filter:
            videos = [v for v in videos if v.get('emotion') == emotion_filter]
        
        if difficulty_filter:
            videos = [v for v in videos if v.get('difficulty') == difficulty_filter]
        
        if accent_filter:
            videos = [v for v in videos if v.get('speaker_accent') == accent_filter]
        
        return jsonify({'videos': videos}), 200
        
    except Exception as e:
        print(f"Error fetching learning videos: {str(e)}")
        return jsonify({'error': 'Failed to fetch videos'}), 500

@learning_library_bp.route('/analyze/<video_id>', methods=['POST'])
def analyze_learning_video(video_id):
    """Analyze a video from the learning library"""
    try:
        # Load video metadata
        metadata_file = os.path.join(LEARNING_UPLOAD_FOLDER, 'videos_metadata.json')
        
        if not os.path.exists(metadata_file):
            return jsonify({'error': 'Video not found'}), 404
        
        with open(metadata_file, 'r') as f:
            videos = json.load(f)
        
        video = next((v for v in videos if v['id'] == video_id), None)
        if not video:
            return jsonify({'error': 'Video not found'}), 404
        
        # For now, return mock analysis data
        # In production, this would process the video file
        analysis_result = {
            'video_id': video_id,
            'emotion_detected': video['emotion'],
            'confidence': 0.85 + (hash(video_id) % 15) / 100,  # Mock confidence
            'tone_characteristics': {
                'pitch': 'Medium',
                'speed': 'Normal',
                'volume': 'Moderate',
                'clarity': 'Clear'
            },
            'learning_points': [
                f"Notice the {video['emotion']} emotion expressed through facial expressions",
                "Pay attention to the vocal tone and pitch variations",
                "Observe body language and gestures",
                f"This is a {video['difficulty']}-level example suitable for practice"
            ],
            'transcript': f"[Mock transcript for {video['title']} - In production, this would contain the actual speech-to-text transcript]",
            'analysis_date': datetime.now().isoformat()
        }
        
        # Mark video as analyzed
        for v in videos:
            if v['id'] == video_id:
                v['analyzed'] = True
                v['last_analysis'] = analysis_result['analysis_date']
                break
        
        # Save updated metadata
        with open(metadata_file, 'w') as f:
            json.dump(videos, f, indent=2)
        
        return jsonify({
            'message': 'Video analyzed successfully',
            'analysis': analysis_result
        }), 200
        
    except Exception as e:
        print(f"Error analyzing learning video: {str(e)}")
        return jsonify({'error': 'Failed to analyze video'}), 500

@learning_library_bp.route('/video/<video_id>', methods=['DELETE'])
def delete_learning_video(video_id):
    """Delete a video from the learning library"""
    try:
        metadata_file = os.path.join(LEARNING_UPLOAD_FOLDER, 'videos_metadata.json')
        
        if not os.path.exists(metadata_file):
            return jsonify({'error': 'Video not found'}), 404
        
        with open(metadata_file, 'r') as f:
            videos = json.load(f)
        
        video = next((v for v in videos if v['id'] == video_id), None)
        if not video:
            return jsonify({'error': 'Video not found'}), 404
        
        # Remove video file
        video_path = os.path.join(LEARNING_UPLOAD_FOLDER, video['filename'])
        if os.path.exists(video_path):
            os.remove(video_path)
        
        # Remove from metadata
        videos = [v for v in videos if v['id'] != video_id]
        
        with open(metadata_file, 'w') as f:
            json.dump(videos, f, indent=2)
        
        return jsonify({'message': 'Video deleted successfully'}), 200
        
    except Exception as e:
        print(f"Error deleting learning video: {str(e)}")
        return jsonify({'error': 'Failed to delete video'}), 500
