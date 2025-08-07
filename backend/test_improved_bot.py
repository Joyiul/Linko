#!/usr/bin/env python3
"""
Test script for the improved contextual SMS bot
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from processing.conversational_sms_bot import get_sms_bot_response

def test_bot_responses():
    """Test the improved bot with various messages"""
    
    test_messages = [
        "hey how are you doing today?",
        "I'm really tired from work",
        "just had the most amazing pizza!",
        "I'm stressed about my exam tomorrow",
        "what's your favorite music?",
        "I love watching Netflix shows",
        "the weather is so nice today",
        "thanks for helping me learn English!",
        "I'm confused about this slang",
        "what are your weekend plans?"
    ]
    
    print("Testing Improved Contextual SMS Bot")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. USER: {message}")
        print("-" * 30)
        
        try:
            response = get_sms_bot_response(message)
            print(f"BOT: {response}")
        except Exception as e:
            print(f"ERROR: {e}")
        
        print()

if __name__ == "__main__":
    test_bot_responses()
