from flask import Blueprint, request, jsonify
from processing.audio_analysis import analyze_audio
from processing.slang_detect import detect_slang, enhanced_detector
from processing.robust_emotion_analysis import analyze_emotion_robust
from processing.sarcasm_detection import detect_sarcasm, get_sarcasm_explanation, get_comprehensive_sarcasm_analysis
from processing.text_simplification import simplify_text_for_learners, get_text_readability
import os
import tempfile

analysis_routes = Blueprint("analysis_routes", __name__)

def enhance_emotion_analysis(transcript, base_tone):
    """
    Enhanced emotion detection with improved sensitivity and pattern matching
    """
    transcript_lower = transcript.lower()
    
    # Enhanced emotion patterns with intensity modifiers and phrases
    emotion_patterns = {
        'happy': {
            'keywords': ['happy', 'joy', 'joyful', 'wonderful', 'great', 'awesome', 'fantastic', 'love', 'smile', 'glad', 'cheerful', 'delighted', 'content'],
            'phrases': ["i'm so happy", "so happy", "really happy", "very happy", "feel great", "feeling good", "love this", "this is great", "makes me happy"],
            'intensifiers': ['so', 'very', 'really', 'extremely', 'super', 'totally', 'absolutely', 'incredibly']
        },
        'excited': {
            'keywords': ['excited', 'thrilled', 'ecstatic', 'exhilarated', 'pumped', 'stoked', 'hyped', 'enthusiastic', 'eager'],
            'phrases': ["i'm so excited", "so excited", "really excited", "very excited", "can't wait", "so pumped", "really thrilled", "absolutely thrilled"],
            'intensifiers': ['so', 'very', 'really', 'extremely', 'super', 'totally', 'absolutely', 'incredibly']
        },
        'angry': {
            'keywords': ['angry', 'mad', 'furious', 'rage', 'hate', 'damn', 'shit', 'pissed', 'annoyed', 'irritated', 'frustrated', 'livid', 'frustrating'],
            'phrases': ["i'm angry", "so mad", "really angry", "pissed off", "fed up", "had enough", "makes me angry", "so frustrating", "really frustrating"],
            'intensifiers': ['so', 'very', 'really', 'extremely', 'totally', 'absolutely']
        },
        'sad': {
            'keywords': ['sad', 'depressed', 'cry', 'tears', 'hurt', 'pain', 'lonely', 'miserable', 'upset', 'down', 'heartbroken', 'devastated'],
            'phrases': ["i'm sad", "so sad", "feeling down", "really hurt", "feel terrible", "makes me sad"],
            'intensifiers': ['so', 'very', 'really', 'extremely', 'quite']
        },
        'disappointed': {
            'keywords': ['disappointed', 'disappointment', 'let down', 'dissatisfied', 'unfulfilled', 'disillusioned', 'underwhelmed'],
            'phrases': ["i'm disappointed", "so disappointed", "really disappointed", "let me down", "such a disappointment", "feel disappointed"],
            'intensifiers': ['so', 'very', 'really', 'extremely', 'quite', 'totally']
        },
        'fear': {
            'keywords': ['scared', 'afraid', 'fear', 'nervous', 'anxious', 'worried', 'panic', 'terrified', 'frightened', 'alarmed'],
            'phrases': ["i'm scared", "so scared", "really afraid", "quite nervous", "very anxious", "totally terrified"],
            'intensifiers': ['so', 'very', 'really', 'extremely', 'quite', 'totally']
        },
        'disgust': {
            'keywords': ['disgusting', 'gross', 'sick', 'revolting', 'awful', 'horrible', 'nasty', 'yuck', 'ew', 'disgusted'],
            'phrases': ["so gross", "really disgusting", "quite awful", "totally sick", "makes me sick"],
            'intensifiers': ['so', 'very', 'really', 'extremely', 'quite', 'totally']
        },
        'surprise': {
            'keywords': ['wow', 'amazing', 'unbelievable', 'shocked', 'surprised', 'incredible', 'astonishing', 'unexpected', 'stunned'],
            'phrases': ["oh wow", "so surprised", "really amazing", "quite shocking", "totally unexpected", "can't believe"],
            'intensifiers': ['so', 'very', 'really', 'extremely', 'quite', 'totally']
        },
        'interest': {
            'keywords': ['interested', 'curious', 'intrigued', 'fascinating', 'wonder', 'wondering', 'interesting', 'compelling', 'captivating'],
            'phrases': ["so interesting", "really curious", "quite intrigued", "very interesting", "makes me wonder", "i'm curious", "find it interesting", "want to know"],
            'intensifiers': ['so', 'very', 'really', 'extremely', 'quite', 'totally']
        }
    }
    
    # Calculate emotion scores with improved algorithm
    emotion_scores = {}
    
    for emotion, patterns in emotion_patterns.items():
        score = 0
        
        # Direct keyword matches
        for keyword in patterns['keywords']:
            if keyword in transcript_lower:
                score += 2  # Base score for keyword
                
                # Check for intensity modifiers near the keyword
                for intensifier in patterns['intensifiers']:
                    intensifier_phrase = f"{intensifier} {keyword}"
                    if intensifier_phrase in transcript_lower:
                        score += 3  # Bonus for intensified emotion
        
        # Phrase pattern matches (higher weight)
        for phrase in patterns['phrases']:
            if phrase in transcript_lower:
                score += 5  # High score for complete phrases
        
        # Check for "I'm" constructions
        personal_patterns = [f"i'm {keyword}" for keyword in patterns['keywords'][:5]]  # Top 5 keywords
        for pattern in personal_patterns:
            if pattern in transcript_lower:
                score += 4  # High score for personal statements
        
        emotion_scores[emotion] = score
    
    # Find the strongest emotion
    max_emotion = max(emotion_scores, key=emotion_scores.get) if emotion_scores else 'neutral'
    max_score = emotion_scores.get(max_emotion, 0)
    
    # Lower threshold - even 1 strong indicator should trigger detection
    if max_score >= 2:  # Lowered from 2 to 1 for better sensitivity
        confidence = min(max_score * 0.15, 0.95)  # Scale confidence appropriately
        return {
            'primary_tone': base_tone,
            'detected_emotion': max_emotion,
            'confidence': confidence,
            'emotion_scores': emotion_scores,
            'detection_method': 'enhanced_pattern_matching'
        }
    else:
        # If no strong emotion detected, set neutral
        return {
            'primary_tone': base_tone,
            'detected_emotion': 'neutral',
            'confidence': 0.4,
            'emotion_scores': emotion_scores,
            'detection_method': 'default_neutral'
        }

def get_comprehensive_slang_analysis(transcript):
    """Get detailed slang analysis with categorization"""
    slang_results = detect_slang(transcript)
    
    if not slang_results:
        return {
            'found_terms': {},
            'categories': {},
            'statistics': enhanced_detector.get_slang_statistics(),
            'summary': 'No slang or modern expressions detected.'
        }
    
    # Categorize found terms
    categories = {
        'acronym': [],
        'genz_word': [],
        'genz_slang': [],
        'emoji': []
    }
    
    high_popularity_count = 0
    
    for term, info in slang_results.items():
        term_type = info.get('type', 'unknown')
        popularity = info.get('popularity', 'medium')
        
        if term_type in categories:
            categories[term_type].append({
                'term': term,
                'meaning': info.get('meaning', ''),
                'popularity': popularity,
                'example': info.get('example', ''),
                'name': info.get('name', '')  # For emojis
            })
        
        if popularity == 'high':
            high_popularity_count += 1
    
    # Generate summary
    total_found = len(slang_results)
    summary_parts = []
    
    if categories['genz_word']:
        summary_parts.append(f"{len(categories['genz_word'])} modern slang terms")
    if categories['emoji']:
        summary_parts.append(f"{len(categories['emoji'])} emojis with special meanings")
    if categories['acronym']:
        summary_parts.append(f"{len(categories['acronym'])} abbreviations")
    if categories['genz_slang']:
        summary_parts.append(f"{len(categories['genz_slang'])} Gen Z expressions")
    
    if summary_parts:
        summary = f"Found {total_found} modern expressions: " + ", ".join(summary_parts) + "."
        if high_popularity_count > 0:
            summary += f" {high_popularity_count} are highly popular/trending terms."
    else:
        summary = f"Found {total_found} expressions in modern internet/youth language."
    
    return {
        'found_terms': slang_results,
        'categories': categories,
        'statistics': enhanced_detector.get_slang_statistics(),
        'summary': summary,
        'trends': {
            'total_found': total_found,
            'high_popularity': high_popularity_count,
            'has_emojis': len(categories['emoji']) > 0,
            'has_modern_slang': len(categories['genz_word']) > 0
        }
    }

@analysis_routes.route("/analyze", methods=["POST"])
def analyze_file():
    data = request.get_json()
    transcript = data.get("transcript", "")
    
    # NEW: Use robust emotion analysis
    improved_analysis = analyze_emotion_robust(text=transcript)
    
    # NEW: Comprehensive sarcasm analysis with highlighting
    comprehensive_sarcasm = get_comprehensive_sarcasm_analysis(transcript)
    
    # NEW: Text simplification for better comprehension
    simplified_analysis = simplify_text_for_learners(transcript)
    readability_info = get_text_readability(transcript)
    
    # Get base tone analysis
    base_tone = analyze_audio(transcript)
    
    # Note: We no longer override tone with "Sarcastic" - sarcasm is handled separately through highlighting
    
    # Enhance with more detailed emotion detection (legacy support)
    enhanced_emotion = enhance_emotion_analysis(transcript, base_tone)
    
    # Get comprehensive slang analysis with all datasets
    comprehensive_slang = get_comprehensive_slang_analysis(transcript)

    # Return both old and new analysis for comparison
    return jsonify({
        "tone": base_tone,
        "emotion_analysis": enhanced_emotion,  # Legacy
        "improved_emotion_analysis": improved_analysis,  # NEW - More accurate and robust
        "sarcasm_analysis": {
            'sarcasm_detected': comprehensive_sarcasm['sarcasm_detected'],
            'confidence': comprehensive_sarcasm['confidence'],
            'reasons': comprehensive_sarcasm['reasons'],
            'sarcasm_type': comprehensive_sarcasm['sarcasm_type'],
            'original_text': comprehensive_sarcasm['original_text']
        },  # Legacy format
        "sarcasm_explanation": {
            'analysis': {
                'sarcasm_detected': comprehensive_sarcasm['sarcasm_detected'],
                'confidence': comprehensive_sarcasm['confidence'],
                'reasons': comprehensive_sarcasm['reasons'],
                'sarcasm_type': comprehensive_sarcasm['sarcasm_type'],
                'original_text': comprehensive_sarcasm['original_text']
            },
            'explanation': comprehensive_sarcasm['explanation']
        },  # Legacy format
        "comprehensive_sarcasm_analysis": comprehensive_sarcasm,  # NEW - Complete sarcasm analysis with highlighting
        "text_simplification": simplified_analysis,  # NEW - LLM-powered text simplification
        "readability_analysis": readability_info,  # NEW - Reading level analysis
        "slang": comprehensive_slang['found_terms'],  # Legacy format
        "comprehensive_slang_analysis": comprehensive_slang,  # NEW - Detailed analysis
        "transcript_length": len(transcript.split()),
        "analysis_confidence": "high" if len(transcript.split()) > 10 else "low",
        "recommendation": "Use 'comprehensive_slang_analysis' for detailed modern language insights"
    })

@analysis_routes.route("/analyze-multimodal", methods=["POST"])
def analyze_multimodal():
    """New endpoint for comprehensive multimodal emotion analysis"""
    try:
        # Handle JSON data
        if request.is_json:
            data = request.get_json()
            transcript = data.get("transcript", "")
            
            # Analyze text only for JSON requests
            result = analyze_emotion_robust(text=transcript)
            
        # Handle form data with files
        else:
            transcript = request.form.get("transcript", "")
            audio_file = request.files.get("audio")
            
            # Save uploaded audio file temporarily
            audio_path = None
            
            if audio_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio:
                    audio_file.save(tmp_audio.name)
                    audio_path = tmp_audio.name
            
            # Run multimodal analysis
            result = analyze_emotion_robust(
                text=transcript if transcript else None,
                audio_path=audio_path
            )
            
            # Cleanup temporary file
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
        
        return jsonify({
            "status": "success",
            "analysis": result,
            "timestamp": data.get("timestamp") if request.is_json else None
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "error": str(e),
            "fallback_emotion": "neutral"
        }), 500

@analysis_routes.route("/slang-stats", methods=["GET"])
def get_slang_statistics():
    """Get statistics about the slang database"""
    return jsonify({
        "status": "success",
        "statistics": enhanced_detector.get_slang_statistics(),
        "database_info": {
            "description": "Comprehensive modern language database including Gen Z slang, emojis, and acronyms",
            "sources": [
                "Traditional internet acronyms and abbreviations",
                "Modern Gen Z words and phrases with definitions",
                "Current Gen Z slang terms",
                "Emoji meanings in modern context"
            ]
        }
    })

@analysis_routes.route("/simplify-text", methods=["POST"])
def simplify_text_endpoint():
    """Dedicated endpoint for text simplification"""
    try:
        data = request.get_json()
        text = data.get("text", "")
        
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400
        
        # Simplify the text (single standard version)
        simplified_result = simplify_text_for_learners(text)
        readability_info = get_text_readability(text)
        
        return jsonify({
            "status": "success",
            "original_text": text,
            "simplification": simplified_result,
            "readability": readability_info
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@analysis_routes.route("/test-slang", methods=["POST"])
def test_slang_detection():
    """Test endpoint for slang detection"""
    data = request.get_json()
    test_text = data.get("text", "")
    
    if not test_text:
        return jsonify({"error": "No text provided"}), 400
    
    result = get_comprehensive_slang_analysis(test_text)
    
    return jsonify({
        "status": "success",
        "input_text": test_text,
        "analysis": result
    })
