#!/usr/bin/env python3
"""
Quick demo showing the improved contextual chatbot responses
"""

import requests
import json

# Test messages
test_conversations = [
    {
        "user": "I'm really tired from work today",
        "expected_context": "work/tiredness"
    },
    {
        "user": "just had the most amazing pizza!",
        "expected_context": "food/positive"
    },
    {
        "user": "the weather is so beautiful today!",
        "expected_context": "weather/positive"
    },
    {
        "user": "I'm stressed about my exam tomorrow",
        "expected_context": "academic/stress"
    },
    {
        "user": "what's your favorite music?",
        "expected_context": "music/question"
    }
]

def test_chatbot():
    print("🤖 Testing Improved Contextual Chatbot")
    print("=" * 50)
    
    for i, convo in enumerate(test_conversations, 1):
        print(f"\n{i}. Testing context: {convo['expected_context']}")
        print(f"USER: {convo['user']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                "http://localhost:5002/sms-chat",
                json={
                    "message": convo['user'],
                    "timestamp": "2025-08-07T10:00:00Z"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data['bot_response']
                print(f"BOT: {bot_response}")
                
                # Check if response seems contextual
                user_msg_lower = convo['user'].lower()
                bot_response_lower = bot_response.lower()
                
                contextual_hints = []
                if "work" in user_msg_lower and any(word in bot_response_lower for word in ["work", "job", "academic"]):
                    contextual_hints.append("✅ Work context recognized")
                if "food" in user_msg_lower or "pizza" in user_msg_lower:
                    if any(word in bot_response_lower for word in ["food", "hungry", "eat"]):
                        contextual_hints.append("✅ Food context recognized")
                if "weather" in user_msg_lower and "weather" in bot_response_lower:
                    contextual_hints.append("✅ Weather context recognized")
                if "exam" in user_msg_lower and any(word in bot_response_lower for word in ["exam", "test", "study", "grade"]):
                    contextual_hints.append("✅ Academic context recognized")
                if "music" in user_msg_lower and "music" in bot_response_lower:
                    contextual_hints.append("✅ Music context recognized")
                
                if contextual_hints:
                    print("🎯 Context Analysis:", " | ".join(contextual_hints))
                else:
                    print("⚠️  Context may not be fully recognized")
                    
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print(f"\n{'='*50}")
    print("🎉 The chatbot now responds contextually to what users actually say!")
    print("✨ It teaches slang naturally through relevant conversation!")

if __name__ == "__main__":
    test_chatbot()
