#!/usr/bin/env python3
"""
Simple test script to test emotion detection through API
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from routes.analysis import enhance_emotion_analysis
from processing.robust_emotion_analysis import analyze_emotion_robust
import json

def test_api_emotion_detection():
    """Test the emotion detection as it would work through the API"""
    
    test_cases = [
        "I'm so happy!",
        "I am really excited!",
        "This makes me sad",
        "I'm angry about this",
        "This is frustrating",
        "I love this",
        "Wow, amazing!",
        "That's disgusting",
        "I'm scared",
        "Hello there",
        "The weather is okay"
    ]
    
    print("Testing Emotion Detection API Responses")
    print("=" * 50)
    
    for test_text in test_cases:
        print(f"\nInput: '{test_text}'")
        print("-" * 30)
        
        # Test the enhanced emotion analysis (used in /analyze endpoint)
        enhanced_result = enhance_emotion_analysis(test_text, "neutral")
        print(f"Enhanced Analysis: {enhanced_result['detected_emotion']} (confidence: {enhanced_result['confidence']:.2f})")
        
        # Test the robust emotion analysis (used in /analyze-multimodal endpoint)
        robust_result = analyze_emotion_robust(text=test_text)
        if 'multimodal_analysis' in robust_result:
            multimodal = robust_result['multimodal_analysis']
            print(f"Multimodal Analysis: {multimodal['primary_emotion']} (confidence: {multimodal['confidence']:.2f})")
        
        # Show which method the system would use
        detected_emotion = enhanced_result['detected_emotion']
        if detected_emotion == 'neutral':
            print("⚠️  Would show: NEUTRAL")
        else:
            print(f"✅ Would show: {detected_emotion.upper()}")

def simulate_frontend_request():
    """Simulate what the frontend would get from the API"""
    
    test_text = "I'm so happy!"
    
    print("\n" + "=" * 50)
    print("SIMULATING FRONTEND API CALL")
    print("=" * 50)
    print(f"Request: POST /analyze")
    print(f"Body: {{'transcript': '{test_text}'}}")
    
    # Simulate the analyze endpoint response
    base_tone = "neutral"  # This would come from analyze_audio
    enhanced_emotion = enhance_emotion_analysis(test_text, base_tone)
    improved_analysis = analyze_emotion_robust(text=test_text)
    
    # Create the response structure like the real API
    response = {
        "tone": base_tone,
        "emotion_analysis": enhanced_emotion,
        "improved_emotion_analysis": improved_analysis,
    }
    
    print(f"\nResponse excerpt:")
    print(f"tone: {response['tone']}")
    print(f"emotion_analysis.detected_emotion: {response['emotion_analysis']['detected_emotion']}")
    print(f"emotion_analysis.confidence: {response['emotion_analysis']['confidence']}")
    print(f"improved_emotion_analysis.multimodal_analysis.primary_emotion: {response['improved_emotion_analysis']['multimodal_analysis']['primary_emotion']}")
    print(f"improved_emotion_analysis.multimodal_analysis.confidence: {response['improved_emotion_analysis']['multimodal_analysis']['confidence']}")
    
    # What the frontend should display
    print(f"\n🎯 Frontend should display: {response['emotion_analysis']['detected_emotion'].upper()}")
    print(f"🎯 With confidence: {response['emotion_analysis']['confidence']:.0%}")

if __name__ == "__main__":
    test_api_emotion_detection()
    simulate_frontend_request()
