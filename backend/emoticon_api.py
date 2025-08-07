"""
API Integration for Emoticon Emotion Analysis
Provides Flask routes to integrate emoticon analysis with the existing backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the backend directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from processing.emoticon_analysis import EmoticonEmotionAnalyzer
from processing.multimodal_emoticon_analysis import MultimodalEmotionAnalyzer

app = Flask(__name__)
CORS(app)

# Initialize analyzers
emoticon_analyzer = EmoticonEmotionAnalyzer()
multimodal_analyzer = MultimodalEmotionAnalyzer()


@app.route('/api/emoticon/analyze', methods=['POST'])
def analyze_emoticons():
    """
    Analyze emoticons in text and return emotion indicators
    
    Expected JSON input:
    {
        "text": "I'm so happy today! 😊😀🎉",
        "include_intensity": true (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text field is required'}), 400
        
        text = data['text']
        include_intensity = data.get('include_intensity', False)
        
        if include_intensity:
            # Use multimodal analyzer for comprehensive analysis
            result = multimodal_analyzer.analyze_comprehensive_emotion(text, include_intensity=True)
            
            # Flatten the result for easier API consumption
            response = {
                'emoticons_found': result['raw_analysis']['emoticons_found'],
                'total_emoticons': result['raw_analysis']['total_emoticons'],
                'dominant_emotion': {
                    'emotion': result['raw_analysis']['dominant_emotion'].emotion,
                    'confidence': result['raw_analysis']['dominant_emotion'].confidence
                } if result['raw_analysis']['dominant_emotion'] else None,
                'sentiment': result['raw_analysis']['sentiment'],
                'emotion_scores': result['raw_analysis']['emotion_scores'],
                'intensity_scores': result['intensity_scores'],
                'categorized_emotions': result['categorized_emotions'],
                'emotional_complexity': result['emotional_complexity'],
                'summary': result['summary'],
                'recommendations': result['recommendations']
            }
        else:
            # Use basic emoticon analyzer
            result = emoticon_analyzer.analyze_text(text)
            
            response = {
                'emoticons_found': result['emoticons_found'],
                'total_emoticons': result['total_emoticons'],
                'dominant_emotion': {
                    'emotion': result['dominant_emotion'].emotion,
                    'confidence': result['dominant_emotion'].confidence
                } if result['dominant_emotion'] else None,
                'sentiment': result['sentiment'],
                'emotion_scores': result['emotion_scores']
            }
        
        return jsonify({
            'success': True,
            'data': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/emoticon/suggest', methods=['POST'])
def suggest_emoticons():
    """
    Suggest emoticons for a target emotion
    
    Expected JSON input:
    {
        "target_emotion": "happy",
        "current_text": "I'm feeling great" (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'target_emotion' not in data:
            return jsonify({'error': 'target_emotion field is required'}), 400
        
        target_emotion = data['target_emotion']
        current_text = data.get('current_text', '')
        
        suggestions = multimodal_analyzer.suggest_emoticons_for_mood(target_emotion, current_text)
        
        return jsonify({
            'success': True,
            'data': suggestions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/emoticon/conversation-flow', methods=['POST'])
def analyze_conversation_flow():
    """
    Analyze emotional flow in a conversation
    
    Expected JSON input:
    {
        "messages": [
            "Having a rough morning 😞",
            "But things are looking up! ☺️",
            "Just got some great news! 😊🎉"
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({'error': 'messages field is required'}), 400
        
        messages = data['messages']
        
        if not isinstance(messages, list):
            return jsonify({'error': 'messages must be a list'}), 400
        
        result = multimodal_analyzer.analyze_conversation_flow(messages)
        
        # Simplify the response for API consumption
        simplified_analyses = []
        for analysis in result['message_analyses']:
            simplified_analyses.append({
                'message_index': analysis['message_index'],
                'text': analysis['text'],
                'dominant_emotion': {
                    'emotion': analysis['analysis']['raw_analysis']['dominant_emotion'].emotion,
                    'confidence': analysis['analysis']['raw_analysis']['dominant_emotion'].confidence
                } if analysis['analysis']['raw_analysis']['dominant_emotion'] else None,
                'sentiment': analysis['analysis']['raw_analysis']['sentiment'],
                'overall_mood': analysis['analysis']['summary']['overall_mood']
            })
        
        response = {
            'message_analyses': simplified_analyses,
            'emotion_timeline': result['emotion_timeline'],
            'trends': result['trends'],
            'conversation_summary': result['conversation_summary']
        }
        
        return jsonify({
            'success': True,
            'data': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/emoticon/emotions-list', methods=['GET'])
def get_supported_emotions():
    """
    Get list of all supported emotions and their associated emoticons
    """
    try:
        # Get all unique emotions from the emoticon map
        all_emotions = {}
        
        for emoticon, emotions in emoticon_analyzer.emoticon_map.items():
            for emotion, confidence in emotions.items():
                if emotion not in all_emotions:
                    all_emotions[emotion] = {
                        'emoticons': [],
                        'weight': emoticon_analyzer.emotion_weights.get(emotion, 0.5)
                    }
                all_emotions[emotion]['emoticons'].append({
                    'emoticon': emoticon,
                    'confidence': confidence
                })
        
        # Sort emoticons by confidence for each emotion
        for emotion_data in all_emotions.values():
            emotion_data['emoticons'].sort(key=lambda x: x['confidence'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': {
                'total_emotions': len(all_emotions),
                'total_emoticons': len(emoticon_analyzer.emoticon_map),
                'emotions': all_emotions
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/emoticon/health', methods=['GET'])
def health_check():
    """Health check endpoint for emoticon analysis service"""
    return jsonify({
        'success': True,
        'service': 'Emoticon Emotion Analysis',
        'status': 'running',
        'capabilities': [
            'Basic emoticon analysis',
            'Multimodal emotion analysis',
            'Conversation flow analysis',
            'Emoticon suggestions',
            'Emotion intensity scoring'
        ]
    })


# Example usage documentation
@app.route('/api/emoticon/docs', methods=['GET'])
def api_documentation():
    """
    API documentation for emoticon analysis endpoints
    """
    docs = {
        'service': 'Emoticon Emotion Analysis API',
        'version': '1.0.0',
        'description': 'Comprehensive emoticon-to-emotion mapping and analysis service',
        'endpoints': {
            'POST /api/emoticon/analyze': {
                'description': 'Analyze emoticons in text and return emotion indicators',
                'input': {
                    'text': 'string (required) - Text to analyze',
                    'include_intensity': 'boolean (optional) - Include intensity analysis'
                },
                'example_input': {
                    'text': "I'm so happy today! 😊😀🎉",
                    'include_intensity': True
                }
            },
            'POST /api/emoticon/suggest': {
                'description': 'Get emoticon suggestions for a target emotion',
                'input': {
                    'target_emotion': 'string (required) - Target emotion',
                    'current_text': 'string (optional) - Current text for context'
                },
                'example_input': {
                    'target_emotion': 'happy',
                    'current_text': 'Having a great day'
                }
            },
            'POST /api/emoticon/conversation-flow': {
                'description': 'Analyze emotional flow in a conversation',
                'input': {
                    'messages': 'array (required) - List of messages in chronological order'
                },
                'example_input': {
                    'messages': [
                        "Having a rough morning 😞",
                        "But things are looking up! ☺️"
                    ]
                }
            },
            'GET /api/emoticon/emotions-list': {
                'description': 'Get list of all supported emotions and their emoticons'
            },
            'GET /api/emoticon/health': {
                'description': 'Health check for the service'
            }
        },
        'supported_features': {
            'emotions_supported': 141,
            'emoticons_supported': 104,
            'analysis_types': [
                'Basic emotion detection',
                'Sentiment analysis (positive/negative/neutral)',
                'Emotion intensity scoring',
                'Emotional complexity assessment',
                'Conversation flow analysis',
                'Mood balancing recommendations'
            ]
        }
    }
    
    return jsonify(docs)


if __name__ == '__main__':
    print("🚀 Starting Emoticon Emotion Analysis API...")
    print("📚 API Documentation available at: /api/emoticon/docs")
    print("🔍 Health check available at: /api/emoticon/health")
    print("=" * 50)
    
    app.run(debug=True, port=5001, host='0.0.0.0')
