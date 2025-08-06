from flask import Blueprint, request, jsonify
from processing.audio_analysis import analyze_audio
from processing.slang_detect import detect_slang

analysis_routes = Blueprint("analysis_routes", __name__)

def enhance_emotion_analysis(transcript, base_tone):
    """
    Enhance emotion detection with additional keyword analysis
    """
    transcript_lower = transcript.lower()
    
    # More detailed emotion keywords
    emotion_patterns = {
        'angry': ['angry', 'mad', 'furious', 'rage', 'hate', 'damn', 'shit', 'pissed', 'annoyed', 'irritated'],
        'happy': ['happy', 'joy', 'excited', 'amazing', 'wonderful', 'great', 'awesome', 'fantastic', 'love', 'smile'],
        'sad': ['sad', 'depressed', 'cry', 'tears', 'hurt', 'pain', 'lonely', 'miserable', 'upset', 'down'],
        'fear': ['scared', 'afraid', 'fear', 'nervous', 'anxious', 'worried', 'panic', 'terrified', 'frightened'],
        'disgust': ['disgusting', 'gross', 'sick', 'revolting', 'awful', 'horrible', 'nasty', 'yuck'],
        'surprise': ['wow', 'amazing', 'unbelievable', 'shocked', 'surprised', 'incredible', 'astonishing'],
        'neutral': ['okay', 'fine', 'normal', 'regular', 'standard', 'typical']
    }
    
    # Count emotion indicators
    emotion_scores = {}
    for emotion, keywords in emotion_patterns.items():
        score = sum(1 for keyword in keywords if keyword in transcript_lower)
        emotion_scores[emotion] = score
    
    # Find the strongest emotion
    max_emotion = max(emotion_scores, key=emotion_scores.get)
    max_score = emotion_scores[max_emotion]
    
    # Only override base tone if we have strong emotion indicators
    if max_score >= 2:  # At least 2 emotion keywords found
        return {
            'primary_tone': base_tone,
            'detected_emotion': max_emotion,
            'confidence': min(max_score * 0.2, 1.0),  # Scale confidence
            'emotion_scores': emotion_scores
        }
    else:
        return {
            'primary_tone': base_tone,
            'detected_emotion': 'neutral',
            'confidence': 0.3,
            'emotion_scores': emotion_scores
        }

@analysis_routes.route("/analyze", methods=["POST"])
def analyze_file():
    data = request.get_json()
    transcript = data.get("transcript", "")
    
    # Get base tone analysis (uses your strong 3,356-sample model)
    base_tone = analyze_audio(transcript)
    
    # Enhance with more detailed emotion detection
    enhanced_emotion = enhance_emotion_analysis(transcript, base_tone)
    
    # Get slang analysis
    slang_result = detect_slang(transcript)

    return jsonify({
        "tone": base_tone,
        "emotion_analysis": enhanced_emotion,
        "slang": slang_result,
        "transcript_length": len(transcript.split()),
        "analysis_confidence": "high" if len(transcript.split()) > 10 else "low"
    })
