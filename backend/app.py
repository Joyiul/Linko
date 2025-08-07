import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from routes.upload import upload_routes
from routes.analysis import analysis_routes
from routes.facial_updated import facial_routes
from routes.learning_library import learning_library_bp

app = Flask(__name__)
CORS(app)

#registering the routes
app.register_blueprint(upload_routes)
app.register_blueprint(analysis_routes)
app.register_blueprint(facial_routes)
app.register_blueprint(learning_library_bp, url_prefix='/learning-library')

# Health check endpoint for deployment
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'ImmigrantSlangster API'}, 200

if __name__ == '__main__':
    # Get port from environment variable for deployment platforms
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, port=port, host='0.0.0.0')