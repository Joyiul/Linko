from flask import Blueprint, request, jsonify
from processing.audio_analysis import analyze_audio
from processing.slang_detect import detect_slang

analysis_routes = Blueprint("analysis_routes", __name__)

@analysis_routes.route("/analyze", methods=["POST"])
def analyze_file():
    data = request.get_json()
    transcript = data.get("transcript", "")
    
    tone_result = analyze_audio(transcript)
    slang_result = detect_slang(transcript)

    return jsonify({
        "tone": tone_result,
        "slang": slang_result
    })
