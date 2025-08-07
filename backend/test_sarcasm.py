#!/usr/bin/env python3

"""
Test script for sarcasm detection
Run this to test if the sarcasm detection is working properly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from processing.sarcasm_detection import detect_sarcasm, get_sarcasm_explanation

def test_sarcasm_detection():
    print("🎭 Testing Sarcasm Detection System\n")
    print("=" * 50)
    
    test_cases = [
        # Economic sarcasm (your specific case)
        "I work 40 hours just to be poor",
        "Love working for peanuts",
        "Great job, can't even afford groceries",
        
        # General sarcasm
        "Oh wonderful, exactly what I wanted",
        "This is just perfect",
        "Yeah right, that'll work",
        "Living the dream here",
        
        # Non-sarcastic (should not detect)
        "I love my job and the good pay",
        "This is a normal sentence",
        "I am happy about the promotion",
        "Work is going well today"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\nTest {i}: \"{text}\"")
        print("-" * 40)
        
        result = detect_sarcasm(text)
        
        print(f"Sarcasm Detected: {result['sarcasm_detected']}")
        print(f"Confidence: {result['confidence']:.1%}")
        
        if result['sarcasm_detected']:
            print(f"Type: {result['sarcasm_type']}")
            print("Reasons:")
            for reason in result['reasons']:
                print(f"  • {reason}")
        
        print()

if __name__ == "__main__":
    test_sarcasm_detection()
