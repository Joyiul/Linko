"""
Test script for Emoticon Emotion Analysis Module
Demonstrates various use cases and capabilities of the emoticon analyzer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processing.emoticon_analysis import EmoticonEmotionAnalyzer
import json


def test_basic_analysis():
    """Test basic emoticon analysis functionality"""
    analyzer = EmoticonEmotionAnalyzer()
    
    print("🔍 BASIC EMOTICON ANALYSIS TESTS")
    print("=" * 50)
    
    test_cases = [
        ("Simple happiness", "I'm feeling great today! 😊"),
        ("Multiple happy emotions", "So excited! 😀😃😄🎉"),
        ("Sadness", "Feeling down today 😢😞"),
        ("Mixed emotions", "Happy but tired 😊😴"),
        ("Love and affection", "I love you so much! 😍❤️💕"),
        ("Anger and frustration", "This is so annoying! 😠😤"),
        ("Playful teasing", "Just kidding! 😜😉"),
        ("Surprise and shock", "OMG! 😱😲🤯"),
        ("Classical emoticons", "Old school style :) :D XD"),
        ("Heart emotions", "Sending love ❤️💙💚💛🧡💜"),
    ]
    
    for description, text in test_cases:
        print(f"\n📝 {description}")
        print(f"Text: '{text}'")
        
        result = analyzer.analyze_text(text)
        
        print(f"🎭 Emoticons found: {result['emoticons_found']}")
        
        if result['dominant_emotion']:
            print(f"🏆 Dominant emotion: {result['dominant_emotion'].emotion} "
                  f"(confidence: {result['dominant_emotion'].confidence:.2f})")
        
        print(f"📊 Sentiment breakdown:")
        print(f"   Positive: {result['sentiment']['positive']:.2f}")
        print(f"   Negative: {result['sentiment']['negative']:.2f}")
        print(f"   Neutral: {result['sentiment']['neutral']:.2f}")
        
        if result['emotion_scores']:
            top_emotions = dict(sorted(result['emotion_scores'].items(), 
                                     key=lambda x: x[1], reverse=True)[:3])
            print(f"🎯 Top emotions: {top_emotions}")


def test_emotion_suggestions():
    """Test emoticon suggestions for different emotions"""
    analyzer = EmoticonEmotionAnalyzer()
    
    print("\n\n💡 EMOTION SUGGESTION TESTS")
    print("=" * 50)
    
    emotions_to_test = [
        'happy', 'sad', 'angry', 'love', 'surprised', 
        'playful', 'thinking', 'celebrating', 'tired'
    ]
    
    for emotion in emotions_to_test:
        suggestions = analyzer.get_emotion_suggestions(emotion)
        print(f"\n🎭 For '{emotion}' emotion:")
        print(f"   Suggested emoticons: {suggestions[:6]}")  # Show top 6


def test_intensity_analysis():
    """Test emotion intensity analysis"""
    analyzer = EmoticonEmotionAnalyzer()
    
    print("\n\n🌟 EMOTION INTENSITY TESTS")
    print("=" * 50)
    
    intensity_cases = [
        ("Low intensity", "I'm okay 🙂"),
        ("Medium intensity", "Pretty happy today! 😊😀"),
        ("High intensity", "BEST DAY EVER!!! 😍😀😄🎉🥳🎊"),
        ("Overwhelming sadness", "So heartbroken 😢😭😞💔</3"),
        ("Extreme excitement", "OMG YES!!! 😱🤯😍🎉🥳🎊🍾💕"),
    ]
    
    for description, text in intensity_cases:
        print(f"\n📈 {description}")
        print(f"Text: '{text}'")
        
        intensity = analyzer.analyze_emotion_intensity(text)
        regular_analysis = analyzer.analyze_text(text)
        
        print(f"   Total emoticons: {regular_analysis['total_emoticons']}")
        print(f"   Intensity scores: {dict(sorted(intensity.items(), key=lambda x: x[1], reverse=True)[:3])}")


def test_real_world_scenarios():
    """Test with real-world social media style texts"""
    analyzer = EmoticonEmotionAnalyzer()
    
    print("\n\n🌍 REAL-WORLD SCENARIO TESTS")
    print("=" * 50)
    
    real_world_texts = [
        "Just got promoted at work! 🎉😊🥳 So grateful for this opportunity! 🙏",
        "Ugh, stuck in traffic again 😤🚗 Why does this always happen on Mondays? 😞",
        "Movie night with the squad! 🍿😄🎬 Can't wait to see the new Marvel film! 😍",
        "Thanks for the birthday wishes everyone! 🥳🎂💕 Feeling so loved right now ❤️😊",
        "Final exams start tomorrow 😰📚 Wish me luck! 🤞😅",
        "Weekend vibes! 😎🌴☀️ Time to relax and recharge 😌💆‍♀️",
        "My dog just learned a new trick! 🐕😄👏 He's such a good boy! 😍🐾",
        "Rainy day mood 🌧️😔 Perfect for staying in with tea and a book ☕📖😊",
        "Concert was AMAZING! 🎵🎸🤘 Best night ever! 😍🎉",
        "Feeling grateful for family time 👨‍👩‍👧‍👦❤️ Nothing beats home cooking! 😋🏠",
    ]
    
    for i, text in enumerate(real_world_texts, 1):
        print(f"\n📱 Scenario {i}")
        print(f"Text: '{text}'")
        
        result = analyzer.analyze_text(text)
        intensity = analyzer.analyze_emotion_intensity(text)
        
        print(f"🎭 Found {result['total_emoticons']} emoticons: {result['emoticons_found']}")
        
        if result['dominant_emotion']:
            dominant = result['dominant_emotion']
            intensity_score = intensity.get(dominant.emotion, 0)
            print(f"🏆 Dominant: {dominant.emotion} (confidence: {dominant.confidence:.2f}, "
                  f"intensity: {intensity_score:.2f})")
        
        sentiment = result['sentiment']
        overall_sentiment = "Positive" if sentiment['positive'] > sentiment['negative'] else "Negative" if sentiment['negative'] > sentiment['positive'] else "Neutral"
        print(f"📊 Overall sentiment: {overall_sentiment}")


def test_edge_cases():
    """Test edge cases and unusual inputs"""
    analyzer = EmoticonEmotionAnalyzer()
    
    print("\n\n🔍 EDGE CASE TESTS")
    print("=" * 50)
    
    edge_cases = [
        ("Empty text", ""),
        ("No emoticons", "This is just regular text without any emoticons."),
        ("Only emoticons", "😊😢😠😱🤔"),
        ("Repeated emoticons", "😂😂😂😂😂😂😂😂"),
        ("Mixed old and new", "Happy :) but also 😊 and excited :D 😄"),
        ("Conflicting emotions", "Happy 😊 but sad 😢 and angry 😠 at the same time"),
        ("Very long text", "This is a very long text with some emoticons 😊 scattered throughout the content to test how the analyzer handles longer inputs with fewer emoticons relative to text length 🤔"),
    ]
    
    for description, text in edge_cases:
        print(f"\n🧪 {description}")
        print(f"Text: '{text}'")
        
        result = analyzer.analyze_text(text)
        
        if result['total_emoticons'] > 0:
            print(f"✅ Analysis successful: {result['total_emoticons']} emoticons found")
            if result['dominant_emotion']:
                print(f"   Dominant: {result['dominant_emotion'].emotion} "
                      f"(confidence: {result['dominant_emotion'].confidence:.2f})")
        else:
            print("ℹ️  No emoticons detected")


def generate_comprehensive_report():
    """Generate a comprehensive analysis report"""
    analyzer = EmoticonEmotionAnalyzer()
    
    print("\n\n📋 COMPREHENSIVE ANALYZER REPORT")
    print("=" * 50)
    
    # Statistics about the analyzer
    total_emoticons = len(analyzer.emoticon_map)
    all_emotions = set()
    for emotions in analyzer.emoticon_map.values():
        all_emotions.update(emotions.keys())
    
    print(f"\n📊 Analyzer Statistics:")
    print(f"   Total emoticons supported: {total_emoticons}")
    print(f"   Total unique emotions: {len(all_emotions)}")
    print(f"   Emotion categories: {len(analyzer.emotion_weights)}")
    
    print(f"\n🎭 Supported Emotions:")
    emotions_by_weight = sorted(analyzer.emotion_weights.items(), key=lambda x: x[1], reverse=True)
    for emotion, weight in emotions_by_weight[:15]:  # Show top 15
        count = sum(1 for emo_dict in analyzer.emoticon_map.values() if emotion in emo_dict)
        print(f"   {emotion}: {count} emoticons (weight: {weight})")
    
    print(f"\n🏆 Most Expressive Emoticons:")
    # Find emoticons that express the most emotions
    emoticon_emotion_count = [(emoticon, len(emotions)) for emoticon, emotions in analyzer.emoticon_map.items()]
    emoticon_emotion_count.sort(key=lambda x: x[1], reverse=True)
    
    for emoticon, count in emoticon_emotion_count[:10]:
        emotions = list(analyzer.emoticon_map[emoticon].keys())
        print(f"   {emoticon}: {count} emotions ({', '.join(emotions[:3])}{'...' if len(emotions) > 3 else ''})")


if __name__ == "__main__":
    print("🚀 EMOTICON EMOTION ANALYZER - COMPREHENSIVE TESTING")
    print("=" * 60)
    
    try:
        test_basic_analysis()
        test_emotion_suggestions()
        test_intensity_analysis()
        test_real_world_scenarios()
        test_edge_cases()
        generate_comprehensive_report()
        
        print("\n\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("🎉 The Emoticon Emotion Analyzer is ready for use!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
