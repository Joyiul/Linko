"""
Demo script showing integration of emoticon analysis with existing backend systems
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from processing.emoticon_analysis import EmoticonEmotionAnalyzer
from processing.multimodal_emoticon_analysis import MultimodalEmotionAnalyzer
import json


def demo_social_media_analysis():
    """Demo analyzing social media posts with emoticons"""
    print("📱 SOCIAL MEDIA EMOTION ANALYSIS DEMO")
    print("=" * 50)
    
    analyzer = MultimodalEmotionAnalyzer()
    
    # Simulate social media posts
    posts = [
        {
            "user": "student_user",
            "content": "Final exam season 😰📚 So stressed but gotta push through! 💪😤",
            "context": "academic_stress"
        },
        {
            "user": "happy_user",
            "content": "Just graduated! 🎓🎉🥳 Best day of my life! Thank you to everyone who supported me ❤️😊",
            "context": "celebration"
        },
        {
            "user": "frustrated_user",
            "content": "Traffic jam again 😠🚗 Why does this always happen when I'm already late? 😤⏰",
            "context": "daily_frustration"
        },
        {
            "user": "romantic_user",
            "content": "Date night with my amazing partner 😍❤️💕 So lucky to have you in my life! 🥰✨",
            "context": "relationship"
        }
    ]
    
    for i, post in enumerate(posts, 1):
        print(f"\n📝 Post {i} ({post['context']})")
        print(f"User: {post['user']}")
        print(f"Content: '{post['content']}'")
        
        analysis = analyzer.analyze_comprehensive_emotion(post['content'])
        
        print(f"\n🎭 Analysis Results:")
        print(f"   Emoticons found: {analysis['raw_analysis']['emoticons_found']}")
        
        if analysis['raw_analysis']['dominant_emotion']:
            dominant = analysis['raw_analysis']['dominant_emotion']
            print(f"   Dominant emotion: {dominant.emotion} (confidence: {dominant.confidence:.0%})")
        
        print(f"   Overall mood: {analysis['summary']['overall_mood']}")
        print(f"   Energy level: {analysis['summary']['energy_level']}")
        print(f"   Emotional complexity: {analysis['emotional_complexity']['level']}")
        
        # Show top recommendations
        if analysis['recommendations']:
            print(f"   Top recommendation: {analysis['recommendations'][0]}")


def demo_chat_moderation():
    """Demo using emoticon analysis for chat moderation"""
    print("\n\n🛡️ CHAT MODERATION DEMO")
    print("=" * 50)
    
    analyzer = MultimodalEmotionAnalyzer()
    
    # Simulate chat messages that might need moderation
    chat_messages = [
        "This is so stupid! 😠😡🤬",
        "I hate everything right now 😢💔😭",
        "You're all idiots! 🙄😤",
        "Having a great time chatting with everyone! 😊🎉",
        "Thanks for helping me out 🙏😊❤️"
    ]
    
    for i, message in enumerate(chat_messages, 1):
        print(f"\n💬 Message {i}: '{message}'")
        
        analysis = analyzer.analyze_comprehensive_emotion(message)
        
        # Check for potentially problematic emotions
        emotion_scores = analysis['raw_analysis']['emotion_scores']
        sentiment = analysis['raw_analysis']['sentiment']
        
        # Moderation flags
        high_anger = emotion_scores.get('angry', 0) > 0.7 or emotion_scores.get('furious', 0) > 0.5
        high_negativity = sentiment['negative'] > 0.8
        extreme_sadness = emotion_scores.get('sad', 0) > 0.8 and emotion_scores.get('crying', 0) > 0.7
        
        moderation_flags = []
        if high_anger:
            moderation_flags.append("⚠️ High anger detected")
        if high_negativity:
            moderation_flags.append("⚠️ Very negative sentiment")
        if extreme_sadness:
            moderation_flags.append("💙 User may need support")
        
        if moderation_flags:
            print(f"   🚨 Moderation alerts: {', '.join(moderation_flags)}")
            print(f"   📊 Negativity score: {sentiment['negative']:.0%}")
        else:
            print(f"   ✅ Message appears positive/neutral")
            print(f"   📊 Positivity score: {sentiment['positive']:.0%}")


def demo_conversation_insights():
    """Demo analyzing conversation flow for insights"""
    print("\n\n💬 CONVERSATION FLOW ANALYSIS DEMO")
    print("=" * 50)
    
    analyzer = MultimodalEmotionAnalyzer()
    
    # Simulate a customer service conversation
    conversation = [
        "Hi, I'm having trouble with my order 😟",
        "It was supposed to arrive yesterday but nothing came 😞",
        "I really need this for an important event tomorrow 😰",
        "Thank you for looking into this! 🙏",
        "Oh wow, you found it! It's out for delivery now 😊",
        "Thank you so much for your help! 😍❤️ Excellent service! 🌟"
    ]
    
    print("📞 Customer Service Conversation Analysis")
    
    flow_analysis = analyzer.analyze_conversation_flow(conversation)
    
    print(f"\n📈 Conversation Metrics:")
    print(f"   Total messages: {len(conversation)}")
    print(f"   Emotional stability: {flow_analysis['trends']['trend']}")
    print(f"   Stability score: {flow_analysis['trends']['stability_score']:.2f}")
    print(f"   Overall tone: {flow_analysis['conversation_summary']['overall_tone']}")
    
    print(f"\n🎭 Emotional Journey:")
    for entry in flow_analysis['emotion_timeline']:
        message = conversation[entry['index']]
        print(f"   Message {entry['index'] + 1}: {entry['emotion']} ({entry['confidence']:.0%}) - '{message}'")
    
    # Customer satisfaction inference
    final_sentiment = flow_analysis['message_analyses'][-1]['analysis']['raw_analysis']['sentiment']
    if final_sentiment['positive'] > 0.7:
        print(f"\n✅ Customer satisfaction: HIGH (final positivity: {final_sentiment['positive']:.0%})")
    elif final_sentiment['positive'] > 0.4:
        print(f"\n🟡 Customer satisfaction: MODERATE (final positivity: {final_sentiment['positive']:.0%})")
    else:
        print(f"\n❌ Customer satisfaction: LOW (final positivity: {final_sentiment['positive']:.0%})")


def demo_emoticon_recommendations():
    """Demo emoticon suggestions for different scenarios"""
    print("\n\n💡 EMOTICON RECOMMENDATION DEMO")
    print("=" * 50)
    
    analyzer = MultimodalEmotionAnalyzer()
    
    scenarios = [
        {
            "context": "Congratulating a friend",
            "target_emotion": "celebrating",
            "current_text": "Congratulations on your new job!"
        },
        {
            "context": "Comforting someone",
            "target_emotion": "empathetic",
            "current_text": "I'm sorry to hear you're going through a tough time"
        },
        {
            "context": "Expressing excitement",
            "target_emotion": "excited",
            "current_text": "Can't wait for the concert tonight!"
        },
        {
            "context": "Showing appreciation",
            "target_emotion": "grateful",
            "current_text": "Thank you for all your help with the project"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 Scenario: {scenario['context']}")
        print(f"   Current text: '{scenario['current_text']}'")
        print(f"   Target emotion: {scenario['target_emotion']}")
        
        # Get suggestions (fallback to 'happy' if target emotion not found)
        try:
            suggestions = analyzer.suggest_emoticons_for_mood(scenario['target_emotion'], scenario['current_text'])
            print(f"   Recommended emoticons: {suggestions['primary_suggestions'][:3]}")
            print(f"   Alternative options: {suggestions['alternative_suggestions'][:3]}")
        except:
            # Fallback for emotions not in our dataset
            suggestions = analyzer.suggest_emoticons_for_mood('happy', scenario['current_text'])
            print(f"   Fallback recommendations: {suggestions['primary_suggestions'][:3]}")


def demo_integration_with_existing_system():
    """Demo how emoticon analysis integrates with existing emotion detection"""
    print("\n\n🔗 INTEGRATION WITH EXISTING SYSTEMS DEMO")
    print("=" * 50)
    
    analyzer = MultimodalEmotionAnalyzer()
    
    # Simulate text with both words and emoticons
    mixed_content = [
        {
            "text": "I am feeling absolutely devastated and heartbroken 😢💔",
            "context": "Strong text emotion + matching emoticons"
        },
        {
            "text": "Everything is terrible and awful 😊🎉",
            "context": "Negative text + positive emoticons (sarcasm?)"
        },
        {
            "text": "Having an okay day I guess 😍❤️🥳",
            "context": "Neutral text + very positive emoticons"
        }
    ]
    
    for item in mixed_content:
        print(f"\n📝 Analysis: {item['context']}")
        print(f"   Text: '{item['text']}'")
        
        analysis = analyzer.analyze_comprehensive_emotion(item['text'])
        
        print(f"   Emoticon sentiment: {analysis['raw_analysis']['sentiment']}")
        if analysis['emotional_complexity']['conflicting_emotions']:
            print(f"   ⚠️ Conflicting emotions detected - possible sarcasm or mixed feelings")
        
        print(f"   Complexity level: {analysis['emotional_complexity']['level']}")
        print(f"   Overall assessment: {analysis['summary']['emotional_state']}")


if __name__ == "__main__":
    print("🎭 EMOTICON EMOTION ANALYSIS - COMPREHENSIVE DEMO")
    print("=" * 60)
    print("This demo shows how emoticon analysis can enhance your existing emotion detection system")
    print("=" * 60)
    
    try:
        demo_social_media_analysis()
        demo_chat_moderation()
        demo_conversation_insights()
        demo_emoticon_recommendations()
        demo_integration_with_existing_system()
        
        print("\n\n🎉 ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("\n📋 SUMMARY OF CAPABILITIES:")
        print("✅ Advanced emoticon-to-emotion mapping (104 emoticons, 141 emotions)")
        print("✅ Comprehensive sentiment analysis with intensity scoring")
        print("✅ Conversation flow analysis and emotional journey tracking")
        print("✅ Smart emoticon recommendations for target moods")
        print("✅ Chat moderation and content filtering capabilities")
        print("✅ Integration with existing text-based emotion detection")
        print("✅ API endpoints ready for frontend integration")
        
        print("\n🔧 NEXT STEPS:")
        print("1. Test the API endpoints by running: python emoticon_api.py")
        print("2. Integrate with your existing emotion analysis pipeline")
        print("3. Connect to frontend for real-time emoticon analysis")
        print("4. Customize emotion categories for your specific use case")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
