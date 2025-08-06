#!/usr/bin/env python3
"""
Comprehensive emotion accuracy testing script
This script tests the improved emotion analysis against various test cases
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from processing.improved_emotion_analysis import analyze_multimodal_emotion
from processing.audio_analysis import analyze_audio
from processing.facial_analysis import analyze_facial_features
import json

def test_emotion_accuracy():
    """Test improved emotion detection with various test cases"""
    
    # Test cases with expected emotions
    test_cases = [
        # Happy emotions
        {"text": "I am so happy and excited about this amazing opportunity! This is fantastic!", "expected": "happy"},
        {"text": "What a wonderful day! I feel absolutely fantastic and full of joy.", "expected": "happy"},
        {"text": "I love this so much! This is the best thing ever!", "expected": "happy"},
        
        # Sad emotions  
        {"text": "I am really sad and feel quite down today. I'm feeling very depressed.", "expected": "sad"},
        {"text": "This is so painful and hurtful. I feel terrible and miserable.", "expected": "sad"},
        {"text": "I'm crying because I feel so lonely and hurt by what happened.", "expected": "sad"},
        
        # Angry emotions
        {"text": "I am extremely angry and furious about this situation! This is totally unacceptable!", "expected": "angry"},
        {"text": "I'm so pissed off and mad at what they did. This really irritates me!", "expected": "angry"},
        {"text": "I hate this so much! I'm really annoyed and fed up with everything!", "expected": "angry"},
        
        # Fear emotions
        {"text": "I'm really scared and afraid of what might happen. I'm so nervous and anxious.", "expected": "fear"},
        {"text": "This is terrifying! I'm quite worried and feel panic setting in.", "expected": "fear"},
        {"text": "I'm frightened by this situation and feel very anxious about it.", "expected": "fear"},
        
        # Surprise emotions
        {"text": "Wow! This is absolutely incredible and totally unexpected!", "expected": "surprise"},
        {"text": "Oh my! I'm so surprised and shocked by this amazing news!", "expected": "surprise"},
        {"text": "Unbelievable! This is quite astonishing and really surprising!", "expected": "surprise"},
        
        # Disgust emotions
        {"text": "This is disgusting and revolting! I feel sick and it's totally gross.", "expected": "disgust"},
        {"text": "That's absolutely horrible and nasty. This is really awful and revolting.", "expected": "disgust"},
        {"text": "Yuck! This is so gross and makes me feel quite sick.", "expected": "disgust"},
        
        # Neutral emotions
        {"text": "The meeting is scheduled for 3 PM. Please bring the documents.", "expected": "neutral"},
        {"text": "According to the data, the results show standard performance metrics.", "expected": "neutral"},
        {"text": "The weather today is typical for this time of year.", "expected": "neutral"},
    ]
    
    print("🧪 Testing Improved Emotion Analysis")
    print("=" * 50)
    
    # Test old vs new system
    old_correct = 0
    new_correct = 0
    total_tests = len(test_cases)
    
    detailed_results = []
    
    for i, test_case in enumerate(test_cases):
        text = test_case["text"]
        expected = test_case["expected"]
        
        print(f"\n📝 Test {i+1}: {text[:50]}...")
        print(f"🎯 Expected: {expected}")
        
        # Old system (basic audio analysis)
        old_result = analyze_audio(text)
        print(f"🔴 Old System: {old_result}")
        
        # New system (improved multimodal)
        new_analysis = analyze_multimodal_emotion(text=text)
        new_result = new_analysis.get('multimodal_analysis', {}).get('primary_emotion', 'neutral')
        new_confidence = new_analysis.get('multimodal_analysis', {}).get('confidence', 0)
        print(f"🟢 New System: {new_result} (confidence: {new_confidence:.2f})")
        
        # Check accuracy
        old_match = old_result.lower() == expected.lower()
        new_match = new_result.lower() == expected.lower()
        
        if old_match:
            old_correct += 1
            print("🔴 Old: ✅ CORRECT")
        else:
            print("🔴 Old: ❌ INCORRECT")
            
        if new_match:
            new_correct += 1
            print("🟢 New: ✅ CORRECT")
        else:
            print("🟢 New: ❌ INCORRECT")
        
        # Store detailed results
        detailed_results.append({
            'test_id': i+1,
            'text': text,
            'expected': expected,
            'old_result': old_result,
            'new_result': new_result,
            'new_confidence': new_confidence,
            'old_correct': old_match,
            'new_correct': new_match,
            'improvement': new_match and not old_match
        })
    
    # Calculate final scores
    old_accuracy = (old_correct / total_tests) * 100
    new_accuracy = (new_correct / total_tests) * 100
    improvement = new_accuracy - old_accuracy
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    print(f"🔴 Old System Accuracy: {old_correct}/{total_tests} = {old_accuracy:.1f}%")
    print(f"🟢 New System Accuracy: {new_correct}/{total_tests} = {new_accuracy:.1f}%")
    print(f"📈 Improvement: +{improvement:.1f} percentage points")
    
    if improvement > 0:
        print(f"🎉 SUCCESS! The new system is {improvement:.1f}% more accurate!")
    elif improvement == 0:
        print("📊 No change in accuracy.")
    else:
        print(f"⚠️  The new system is {abs(improvement):.1f}% less accurate.")
    
    # Show improvement breakdown
    improvements = [r for r in detailed_results if r['improvement']]
    if improvements:
        print(f"\n✨ Improved Cases ({len(improvements)}):")
        for result in improvements:
            print(f"  • Test {result['test_id']}: '{result['text'][:40]}...'")
            print(f"    Expected: {result['expected']} | Old: {result['old_result']} → New: {result['new_result']}")
    
    # Save detailed results
    output_file = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/emotion_accuracy_test_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'summary': {
                'total_tests': total_tests,
                'old_accuracy': old_accuracy,
                'new_accuracy': new_accuracy,
                'improvement': improvement
            },
            'detailed_results': detailed_results
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    return new_accuracy > old_accuracy

if __name__ == "__main__":
    test_emotion_accuracy()
