#!/usr/bin/env python3
"""
Test script to verify emotion detection improvements
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from processing.robust_emotion_analysis import analyze_emotion_robust
from routes.analysis import enhance_emotion_analysis

def test_emotion_detection():
    """Test emotion detection with various phrases"""
    
    test_phrases = [
        "I'm so happy!",
        "I am really excited about this!",
        "This makes me incredibly happy",
        "I'm feeling great today",
        "I love this so much!",
        "I'm really angry about this",
        "This is so frustrating",
        "I'm quite sad today",
        "I feel terrible about this",
        "I'm extremely worried",
        "This is amazing!",
        "Wow, that's incredible!",
        "This is disgusting",
        "I'm so grossed out",
        "That's just okay",
        "It's fine, I guess",
        "Hello, how are you?",  # Should be neutral
        "The weather is nice today"  # Should be neutral or positive
    ]
    
    print("=" * 60)
    print("EMOTION DETECTION TEST RESULTS")
    print("=" * 60)
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n{i}. Testing: '{phrase}'")
        print("-" * 40)
        
        # Test robust emotion analysis
        robust_result = analyze_emotion_robust(text=phrase)
        if 'text_analysis' in robust_result:
            text_analysis = robust_result['text_analysis']
            print(f"   Robust Analysis:")
            print(f"   • Emotion: {text_analysis['emotion']}")
            print(f"   • Confidence: {text_analysis['confidence']:.2f}")
            print(f"   • Method: {text_analysis['details'].get('method', 'unknown')}")
            if 'emotion_scores' in text_analysis['details']:
                scores = text_analysis['details']['emotion_scores']
                top_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"   • Top emotions: {top_emotions}")
        
        # Test enhanced emotion analysis (legacy)
        enhanced_result = enhance_emotion_analysis(phrase, "neutral")
        print(f"   Enhanced Analysis:")
        print(f"   • Emotion: {enhanced_result['detected_emotion']}")
        print(f"   • Confidence: {enhanced_result['confidence']:.2f}")
        print(f"   • Method: {enhanced_result.get('detection_method', 'legacy')}")
        
        # Check if multimodal analysis exists
        if 'multimodal_analysis' in robust_result:
            multimodal = robust_result['multimodal_analysis']
            print(f"   Multimodal Analysis:")
            print(f"   • Primary emotion: {multimodal['primary_emotion']}")
            print(f"   • Confidence: {multimodal['confidence']:.2f}")

def test_specific_case():
    """Test the specific case mentioned by user"""
    test_text = "I'm so happy!"
    
    print("\n" + "=" * 60)
    print(f"SPECIFIC TEST: '{test_text}'")
    print("=" * 60)
    
    # Test robust analysis
    result = analyze_emotion_robust(text=test_text)
    print("\nRobust Emotion Analysis:")
    print(f"Result: {result}")
    
    # Test enhanced analysis
    enhanced = enhance_emotion_analysis(test_text, "neutral")
    print(f"\nEnhanced Emotion Analysis:")
    print(f"Result: {enhanced}")
    
    # Expected vs Actual
    print(f"\nExpected: happy")
    if 'text_analysis' in result:
        actual_robust = result['text_analysis']['emotion']
        print(f"Actual (Robust): {actual_robust}")
        print(f"✓ Correct!" if actual_robust == 'happy' else "✗ Incorrect")
    
    actual_enhanced = enhanced['detected_emotion']
    print(f"Actual (Enhanced): {actual_enhanced}")
    print(f"✓ Correct!" if actual_enhanced == 'happy' else "✗ Incorrect")

if __name__ == "__main__":
    test_specific_case()
    test_emotion_detection()
