import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename 

upload_routes = Blueprint('upload_routes', __name__)

UPLOAD_FOLDER = 'uploads'

@upload_routes.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    