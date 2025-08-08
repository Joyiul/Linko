import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename 
from processing.speech_to_text import transcribe_audio
from processing.audio_analysis import analyze_audio
from processing.slang_detect import detect_slang
from processing.robust_emotion_analysis import analyze_emotion_robust

upload_routes = Blueprint('upload_routes', __name__)

# Use absolute path for uploads folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4', 'avi', 'mov', 'flac', 'm4a', 'ogg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_routes.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Supported: wav, mp3, mp4, avi, mov, flac, m4a, ogg'}), 400
    
    # Ensure uploads directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return jsonify({'message': 'File uploaded successfully', 'filename': filename})

@upload_routes.route('/upload-and-analyze', methods=['POST'])
def upload_and_analyze():
    """Upload audio file and perform speech-to-text + analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Supported: wav, mp3, mp4, avi, mov, flac, m4a, ogg'}), 400
        
        # Ensure uploads directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Convert speech to text
        transcription_result = transcribe_audio(filepath)
        
        if 'error' in transcription_result:
            return jsonify({
                'error': transcription_result['error'],
                'filename': filename
            }), 500
        
        transcript = transcription_result['transcript']
        
        # Perform comprehensive analysis (same as /analyze endpoint)
        import requests
        try:
            # Call the comprehensive analyze endpoint internally
            analysis_response = requests.post('http://localhost:5002/analyze', 
                                            json={'transcript': transcript},
                                            timeout=30)
            
            if analysis_response.status_code == 200:
                comprehensive_analysis = analysis_response.json()
                
                return jsonify({
                    'filename': filename,
                    'transcript': transcript,
                    'analysis': comprehensive_analysis  # Complete analysis with tone, emotion, formality, etc.
                })
            else:
                # Fallback to basic analysis if comprehensive fails
                tone_result = analyze_audio(transcript)
                slang_result = detect_slang(transcript)
                robust_analysis = analyze_emotion_robust(text=transcript, audio_path=filepath)
                
                return jsonify({
                    'filename': filename,
                    'transcript': transcript,
                    'analysis': {
                        'tone': tone_result,
                        'slang': slang_result,
                        'robust_emotion': robust_analysis
                    },
                    'recommendation': 'Basic analysis used - comprehensive analysis failed'
                })
                
        except Exception as analysis_error:
            print(f"Comprehensive analysis failed: {analysis_error}")
            # Fallback to basic analysis
            tone_result = analyze_audio(transcript)
            slang_result = detect_slang(transcript)
            robust_analysis = analyze_emotion_robust(text=transcript, audio_path=filepath)
            
            return jsonify({
                'filename': filename,
                'transcript': transcript,
                'analysis': {
                    'tone': tone_result,
                    'slang': slang_result,
                    'robust_emotion': robust_analysis
                },
                'recommendation': 'Basic analysis used due to error'
            })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Analysis failed: {str(e)}',
            'filename': filename if 'filename' in locals() else 'unknown'
        }), 500

@upload_routes.route('/upload-and-analyze-video', methods=['POST'])
def upload_and_analyze_video():
    """Upload video file and perform comprehensive analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Check if it's a video file
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS):
            return jsonify({'error': 'File type not allowed. Supported video formats: mp4, avi, mov, mkv, webm'}), 400
        
        # Ensure uploads directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save file
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Import video analysis
            import cv2
            from processing.robust_emotion_analysis import analyze_emotion_robust
            
            # Extract audio for transcription if possible
            transcript = ""
            audio_tone = "neutral"
            
            try:
                # Try to extract audio from video and transcribe
                from processing.speech_to_text import transcribe_audio
                transcription_result = transcribe_audio(filepath)
                
                if 'transcript' in transcription_result:
                    transcript = transcription_result['transcript']
                    
                    # Analyze the transcript for emotion and slang
                    audio_analysis = analyze_emotion_robust(text=transcript)
                    if audio_analysis and 'predicted_emotion' in audio_analysis:
                        audio_tone = audio_analysis['predicted_emotion']
                        
            except Exception as audio_error:
                print(f"Audio extraction failed: {audio_error}")
                # Continue without audio analysis
            
            # Perform video facial analysis
            cap = cv2.VideoCapture(filepath)
            
            if not cap.isOpened():
                return jsonify({'error': 'Could not open video file'}), 500
                
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            # Analyze a few key frames
            frame_results = []
            frames_to_analyze = min(10, max(1, int(total_frames / 30)))  # Analyze up to 10 key frames
            
            for i in range(frames_to_analyze):
                frame_pos = int((i + 1) * total_frames / (frames_to_analyze + 1))
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
                ret, frame = cap.read()
                
                if ret:
                    # Simple emotion detection from frame (you can enhance this)
                    # For now, we'll do basic analysis
                    timestamp = frame_pos / fps
                    frame_results.append({
                        'frame_number': frame_pos,
                        'timestamp': round(timestamp, 2),
                        'emotion': 'neutral',  # Placeholder - could integrate with facial analysis
                        'confidence': 0.5
                    })
            
            cap.release()
            
            # Combine results
            dominant_emotion = audio_tone if audio_tone != 'neutral' else 'neutral'
            
            # Get slang analysis from transcript
            slang_result = detect_slang(transcript) if transcript else {}
            
            return jsonify({
                'filename': filename,
                'video_info': {
                    'duration_seconds': round(duration, 2),
                    'total_frames': total_frames,
                    'fps': fps
                },
                'transcript': transcript,
                'analysis': {
                    'dominant_emotion': dominant_emotion,
                    'audio_tone': audio_tone,
                    'frames_analyzed': len(frame_results),
                    'frame_results': frame_results,
                    'slang': slang_result
                },
                'message': f'Video analysis completed. Duration: {duration:.1f}s, Emotion: {dominant_emotion}'
            })
        
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Video analysis failed: {str(e)}',
            'filename': filename if 'filename' in locals() else 'unknown'
        }), 500