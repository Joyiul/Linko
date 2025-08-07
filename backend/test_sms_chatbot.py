#!/usr/bin/env python3
"""
Test SMS Chatbot Integration
Tests the conversational SMS chatbot functionality with cultural slang and idioms
"""
import requests
import json
import time

def test_sms_chatbot():
    """Test the SMS chatbot endpoints"""
    base_url = "http://localhost:5002"
    
    print("🧪 Testing SMS-Style Conversational Chatbot")
    print("=" * 50)
    
    # Test messages to send
    test_messages = [
        "hey there!",
        "I'm excited about learning slang",
        "What does 'no cap' mean?",
        "That's fire! I love this app",
        "This is so slay bestie"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📱 Test {i}: User says '{message}'")
        print("-" * 30)
        
        try:
            # Send message to SMS chatbot
            response = requests.post(f"{base_url}/sms-chat", 
                json={
                    "message": message,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get('bot_response', 'No response')
                print(f"🤖 Bot responds: {bot_response[:200]}{'...' if len(bot_response) > 200 else ''}")
                print(f"✅ Chat type: {data.get('chat_type', 'unknown')}")
                print(f"📚 Learning focus: {data.get('learning_focus', 'unknown')}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
        
        # Small delay between requests
        time.sleep(1)
    
    print("\n" + "=" * 50)
    
    # Test practice suggestion
    print("\n💡 Testing Practice Suggestion Endpoint")
    print("-" * 35)
    
    try:
        response = requests.get(f"{base_url}/practice-suggestion", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            suggestion = data.get('practice_suggestion', {})
            print(f"📝 Scenario: {suggestion.get('scenario', 'N/A')}")
            print(f"💬 Suggested response: {suggestion.get('slang_response', 'N/A')}")
            print(f"📖 Explanation: {suggestion.get('explanation', 'N/A')}")
            print(f"✅ Purpose: {data.get('purpose', 'unknown')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ SMS Chatbot testing complete!")

if __name__ == "__main__":
    test_sms_chatbot()
