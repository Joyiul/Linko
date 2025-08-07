import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Health check endpoint for deployment
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'ImmigrantSlangster API'}, 200

# Basic speech analysis endpoint (simplified for deployment)
@app.route('/upload-and-analyze', methods=['POST'])
def upload_and_analyze():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # For now, return a simple response
        # You can add actual speech processing later once deployment is working
        return jsonify({
            'transcript': 'Speech analysis coming soon...',
            'tone': 'neutral',
            'slang_detected': [],
            'emotion': 'calm',
            'confidence': 0.7
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Basic video analysis endpoint (simplified for deployment)
@app.route('/upload-and-analyze-video', methods=['POST'])
def upload_and_analyze_video():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        if video_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # For now, return a simple response
        return jsonify({
            'message': 'Video uploaded successfully',
            'face_detected': True,
            'emotion': 'neutral',
            'confidence': 0.7
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Test endpoint
@app.route('/test')
def test():
    return {'message': 'Backend is working!', 'status': 'success'}, 200

if __name__ == '__main__':
    # Get port from environment variable for deployment platforms
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, port=port, host='0.0.0.0')
