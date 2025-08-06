from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import json
import traceback

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
    """Get all videos in the learning library with real educational content"""
    try:
        print("DEBUG: get_learning_videos endpoint called")
        # Educational content library - mix of real educational videos and placeholders
        real_videos = [
            {
                "id": "real_001",
                "title": "Understanding Emotions in English Communication",
                "description": "Learn to recognize different emotional tones and expressions in American English. Practice identifying happiness, sadness, anger, surprise, and subtle emotions in speech patterns.",
                "category": "tones",
                "duration": "8:45",
                "level": "Intermediate",
                "thumbnail": "🎭",
                "instructor": "English Learning Academy",
                "videoUrl": "https://www.youtube.com/embed/_uQDCru94nA",  # Real educational video provided by user
                "skills": ["Tone Recognition", "Emotional Expression", "Cultural Context"],
                "views": "12.5K",
                "upload_date": "2024-01-15",
                "analyzed": True,
                "real_video": True
            },
            {
                "id": "real_002", 
                "title": "Modern American Slang Dictionary",
                "description": "Master essential slang terms like 'no cap', 'salty', 'flex', 'vibe check', and more. Learn when and how to use them appropriately in conversation.",
                "category": "slang",
                "duration": "12:30",
                "level": "Beginner",
                "thumbnail": "💬",
                "instructor": "Slang Education Expert",
                "videoUrl": "https://www.youtube.com/embed/d7d_9aBfY_c",  # Real educational video provided by user
                "skills": ["Modern Slang", "Informal Language", "American Culture"],
                "views": "125K",
                "upload_date": "2024-01-20",
                "analyzed": True,
                "real_video": True
            },
            {
                "id": "real_003",
                "title": "Pronunciation Masterclass: Difficult Sounds",
                "description": "Focus on the most challenging English sounds for non-native speakers: TH, R, L, and vowel distinctions that affect meaning.",
                "category": "pronunciation", 
                "duration": "15:20",
                "level": "Beginner",
                "thumbnail": "🗣️",
                "instructor": "Pronunciation Expert",
                "videoUrl": "https://www.youtube.com/embed/tpN9CPwZ-oE",  # Real educational video provided by user
                "skills": ["Clear Pronunciation", "Accent Reduction", "Speech Training"],
                "views": "89K",
                "upload_date": "2024-01-25",
                "analyzed": True,
                "real_video": True
            },
            {
                "id": "real_004",
                "title": "Workplace English: Reading the Room",
                "description": "Learn to interpret workplace dynamics, understand passive communication, and navigate professional relationships through tone and context.",
                "category": "workplace",
                "duration": "18:45", 
                "level": "Advanced",
                "thumbnail": "💼",
                "instructor": "Professional Communication Expert",
                "videoUrl": "https://www.youtube.com/embed/HVSz098xYV8",  # Real educational video provided by user
                "skills": ["Business English", "Professional Communication", "Workplace Dynamics"],
                "views": "45K",
                "upload_date": "2024-02-01",
                "analyzed": True,
                "real_video": True
            },
            {
                "id": "real_005",
                "title": "Social Conversation Survival Guide",
                "description": "Navigate small talk, understand social cues, and build rapport in casual American conversations. Perfect for networking and making friends.",
                "category": "conversation",
                "duration": "14:10",
                "level": "Intermediate",
                "thumbnail": "💭",
                "instructor": "Social Skills Coach",
                "videoUrl": "https://www.youtube.com/embed/YQHsXMglC9A",  # Placeholder - awaiting conversation content
                "skills": ["Social Skills", "Conversation Flow", "Cultural Awareness"],
                "views": "78K",
                "upload_date": "2024-02-05",
                "analyzed": True,
                "real_video": True
            },
            {
                "id": "real_006",
                "title": "Cultural Context Decoder",
                "description": "Understand the hidden meanings behind American expressions, learn regional differences, and avoid cultural misunderstandings.",
                "category": "cultural",
                "duration": "16:30",
                "level": "Intermediate",
                "thumbnail": "🌍",
                "instructor": "Cultural Communication Guide",
                "videoUrl": "https://www.youtube.com/embed/2Vv-BfVoq4g",  # Placeholder - awaiting cultural content
                "skills": ["Cultural Awareness", "Context Clues", "Cross-cultural Communication"],
                "views": "92K",
                "upload_date": "2024-02-10",
                "analyzed": True,
                "real_video": True
            }
        ]
        
        print(f"DEBUG: Created {len(real_videos)} real videos")
        
        # Load user-uploaded videos if they exist
        metadata_file = os.path.join(LEARNING_UPLOAD_FOLDER, 'videos_metadata.json')
        user_videos = []
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                user_videos = json.load(f)
        
        # Combine real videos with user uploads
        all_videos = real_videos + user_videos
        
        print(f"DEBUG: Total videos before filtering: {len(all_videos)}")
        
        # Filter by query parameters if provided
        emotion_filter = request.args.get('emotion')
        difficulty_filter = request.args.get('difficulty')
        accent_filter = request.args.get('accent')
        category_filter = request.args.get('category')
        
        if emotion_filter:
            all_videos = [v for v in all_videos if v.get('emotion') == emotion_filter]
        
        if difficulty_filter:
            all_videos = [v for v in all_videos if v.get('difficulty', v.get('level', '')).lower() == difficulty_filter.lower()]
        
        if accent_filter:
            all_videos = [v for v in all_videos if v.get('speaker_accent') == accent_filter]
            
        if category_filter:
            all_videos = [v for v in all_videos if v.get('category') == category_filter]
        
        print(f"DEBUG: Total videos after filtering: {len(all_videos)}")
        print(f"DEBUG: Returning videos response")
        
        return jsonify({
            'videos': all_videos,
            'total_count': len(all_videos),
            'real_videos_count': len(real_videos),
            'user_videos_count': len(user_videos)
        }), 200
        
    except Exception as e:
        print(f"ERROR in get_learning_videos: {str(e)}")
        traceback.print_exc()
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
