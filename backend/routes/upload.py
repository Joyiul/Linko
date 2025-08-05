import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename 
from processing.speech_to_text import transcribe_audio
from processing.audio_analysis import analyze_audio
from processing.slang_detect import detect_slang

upload_routes = Blueprint('upload_routes', __name__)

UPLOAD_FOLDER = 'backend/uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4', 'avi', 'mov', 'flac', 'm4a', 'ogg'}

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
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return jsonify({'message': 'File uploaded successfully', 'filename': filename})

@upload_routes.route('/upload-and-analyze', methods=['POST'])
def upload_and_analyze():
    """Upload audio file and perform speech-to-text + analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Supported: wav, mp3, mp4, avi, mov, flac, m4a, ogg'}), 400
    
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
    
    # Analyze the transcript
    tone_result = analyze_audio(transcript)
    slang_result = detect_slang(transcript)
    
    return jsonify({
        'filename': filename,
        'transcript': transcript,
        'analysis': {
            'tone': tone_result,
            'slang': slang_result
        }
    })
    