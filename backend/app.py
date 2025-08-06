import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from routes.upload import upload_routes
from routes.analysis import analysis_routes

app = Flask(__name__)
CORS(app)

#registering the routes
app.register_blueprint(upload_routes)
app.register_blueprint(analysis_routes)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 

    