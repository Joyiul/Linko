"""
Integration module for combining emoticon analysis with existing emotion detection systems
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processing.emoticon_analysis import EmoticonEmotionAnalyzer
from typing import Dict, List, Optional, Union
import json


class MultimodalEmotionAnalyzer:
    """
    Enhanced emotion analyzer that combines emoticon analysis with existing 
    text-based emotion detection for comprehensive sentiment analysis.
    """
    
    def __init__(self):
        self.emoticon_analyzer = EmoticonEmotionAnalyzer()
        self.emotion_categories = {
            'positive': ['happy', 'joyful', 'excited', 'love', 'content', 'playful', 
                        'celebrating', 'approval', 'grateful', 'peaceful', 'amused'],
            'negative': ['sad', 'angry', 'fearful', 'disgusted', 'frustrated', 
                        'disappointed', 'disapproval', 'anxious', 'worried', 'heartbroken'],
            'neutral': ['neutral', 'thinking', 'confused', 'surprised', 'contemplative', 
                       'analytical', 'indifferent'],
            'energy_levels': {
                'high': ['excited', 'energetic', 'celebrating', 'laughing', 'enthusiastic'],
                'medium': ['happy', 'content', 'playful', 'surprised'],
                'low': ['peaceful', 'tired', 'sleepy', 'calm', 'relaxed']
            }
        }
    
    def analyze_comprehensive_emotion(self, text: str, include_intensity: bool = True) -> Dict[str, any]:
        """
        Perform comprehensive emotion analysis including emoticons, sentiment, and intensity.
        
        Args:
            text (str): Text to analyze
            include_intensity (bool): Whether to include intensity analysis
            
        Returns:
            Dict containing comprehensive emotion analysis
        """
        # Get basic emoticon analysis
        emoticon_result = self.emoticon_analyzer.analyze_text(text)
        
        # Get intensity if requested
        intensity_scores = {}
        if include_intensity:
            intensity_scores = self.emoticon_analyzer.analyze_emotion_intensity(text)
        
        # Categorize emotions
        categorized_emotions = self._categorize_emotions(emoticon_result['emotion_scores'])
        
        # Calculate emotional complexity
        complexity = self._calculate_emotional_complexity(emoticon_result['emotion_scores'])
        
        # Generate emotion summary
        summary = self._generate_emotion_summary(emoticon_result, categorized_emotions, complexity)
        
        return {
            'raw_analysis': emoticon_result,
            'intensity_scores': intensity_scores,
            'categorized_emotions': categorized_emotions,
            'emotional_complexity': complexity,
            'summary': summary,
            'recommendations': self._generate_recommendations(emoticon_result, categorized_emotions)
        }
    
    def _categorize_emotions(self, emotion_scores: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """Categorize emotions into positive, negative, neutral groups."""
        categorized = {
            'positive': {},
            'negative': {},
            'neutral': {},
            'energy_levels': {'high': {}, 'medium': {}, 'low': {}}
        }
        
        for emotion, score in emotion_scores.items():
            # Categorize by sentiment
            if emotion in self.emotion_categories['positive']:
                categorized['positive'][emotion] = score
            elif emotion in self.emotion_categories['negative']:
                categorized['negative'][emotion] = score
            elif emotion in self.emotion_categories['neutral']:
                categorized['neutral'][emotion] = score
            
            # Categorize by energy level
            for energy_level, emotions in self.emotion_categories['energy_levels'].items():
                if emotion in emotions:
                    categorized['energy_levels'][energy_level][emotion] = score
        
        return categorized
    
    def _calculate_emotional_complexity(self, emotion_scores: Dict[str, float]) -> Dict[str, any]:
        """Calculate measures of emotional complexity."""
        if not emotion_scores:
            return {'score': 0, 'level': 'none', 'conflicting_emotions': False}
        
        num_emotions = len(emotion_scores)
        score_variance = self._calculate_variance(list(emotion_scores.values()))
        
        # Check for conflicting emotions (positive and negative simultaneously)
        has_positive = any(emotion in self.emotion_categories['positive'] for emotion in emotion_scores)
        has_negative = any(emotion in self.emotion_categories['negative'] for emotion in emotion_scores)
        conflicting = has_positive and has_negative
        
        # Complexity levels
        if num_emotions <= 2:
            level = 'simple'
        elif num_emotions <= 4:
            level = 'moderate'
        else:
            level = 'complex'
        
        complexity_score = min((num_emotions * 0.2) + (score_variance * 0.5) + (0.3 if conflicting else 0), 1.0)
        
        return {
            'score': complexity_score,
            'level': level,
            'num_emotions': num_emotions,
            'conflicting_emotions': conflicting,
            'variance': score_variance
        }
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of emotion scores."""
        if not values:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
    
    def _generate_emotion_summary(self, emoticon_result: Dict, categorized: Dict, complexity: Dict) -> Dict[str, str]:
        """Generate human-readable emotion summary."""
        summary = {}
        
        # Overall mood
        sentiment = emoticon_result['sentiment']
        if sentiment['positive'] > 0.6:
            summary['overall_mood'] = 'Very Positive'
        elif sentiment['positive'] > 0.4:
            summary['overall_mood'] = 'Positive'
        elif sentiment['negative'] > 0.6:
            summary['overall_mood'] = 'Very Negative'
        elif sentiment['negative'] > 0.4:
            summary['overall_mood'] = 'Negative'
        else:
            summary['overall_mood'] = 'Neutral'
        
        # Dominant emotion description
        if emoticon_result['dominant_emotion']:
            dominant = emoticon_result['dominant_emotion']
            summary['primary_emotion'] = f"{dominant.emotion.title()} (confidence: {dominant.confidence:.0%})"
        else:
            summary['primary_emotion'] = "No clear emotion detected"
        
        # Complexity description
        if complexity['conflicting_emotions']:
            summary['emotional_state'] = "Mixed emotions detected - conflicting feelings present"
        elif complexity['level'] == 'complex':
            summary['emotional_state'] = "Complex emotional state with multiple feelings"
        elif complexity['level'] == 'moderate':
            summary['emotional_state'] = "Moderate emotional expression"
        else:
            summary['emotional_state'] = "Simple, clear emotional expression"
        
        # Energy level
        energy_scores = categorized['energy_levels']
        high_energy = sum(energy_scores['high'].values())
        low_energy = sum(energy_scores['low'].values())
        
        if high_energy > low_energy * 1.5:
            summary['energy_level'] = "High energy"
        elif low_energy > high_energy * 1.5:
            summary['energy_level'] = "Low energy"
        else:
            summary['energy_level'] = "Medium energy"
        
        return summary
    
    def _generate_recommendations(self, emoticon_result: Dict, categorized: Dict) -> List[str]:
        """Generate recommendations based on emotional analysis."""
        recommendations = []
        
        sentiment = emoticon_result['sentiment']
        
        # Sentiment-based recommendations
        if sentiment['negative'] > 0.7:
            recommendations.append("Consider adding more positive emoticons to balance the tone")
            recommendations.append("The message may come across as quite negative")
        
        if sentiment['positive'] > 0.8:
            recommendations.append("Great use of positive emoticons! The message is very uplifting")
        
        # Complexity recommendations
        if len(emoticon_result['emotion_scores']) > 6:
            recommendations.append("Many different emotions detected - consider simplifying for clarity")
        
        # Specific emotion recommendations
        if 'angry' in emoticon_result['emotion_scores'] and emoticon_result['emotion_scores']['angry'] > 0.7:
            recommendations.append("Strong anger detected - consider cooling the tone")
        
        if 'love' in emoticon_result['emotion_scores'] and emoticon_result['emotion_scores']['love'] > 0.8:
            recommendations.append("Strong affection expressed - great for personal messages")
        
        if not emoticon_result['emoticons_found']:
            recommendations.append("Consider adding emoticons to express emotions more clearly")
        
        return recommendations
    
    def suggest_emoticons_for_mood(self, target_mood: str, current_text: str = "") -> Dict[str, List[str]]:
        """
        Suggest emoticons to achieve a target mood.
        
        Args:
            target_mood (str): Desired emotional tone
            current_text (str): Current text to analyze for context
            
        Returns:
            Dict with emoticon suggestions
        """
        # Analyze current text if provided
        current_analysis = None
        if current_text:
            current_analysis = self.emoticon_analyzer.analyze_text(current_text)
        
        # Get suggestions for target mood
        suggestions = self.emoticon_analyzer.get_emotion_suggestions(target_mood)
        
        # Categorize suggestions
        result = {
            'primary_suggestions': suggestions[:3],
            'alternative_suggestions': suggestions[3:6],
            'current_emotions': current_analysis['emotion_scores'] if current_analysis else {},
            'target_mood': target_mood
        }
        
        # Add context-aware suggestions
        if current_analysis and current_analysis['emotion_scores']:
            result['balancing_needed'] = self._analyze_mood_balance(current_analysis, target_mood)
        
        return result
    
    def _analyze_mood_balance(self, current_analysis: Dict, target_mood: str) -> str:
        """Analyze if mood balancing is needed."""
        current_sentiment = current_analysis['sentiment']
        
        positive_targets = ['happy', 'joyful', 'excited', 'love', 'celebrating']
        negative_targets = ['sad', 'angry', 'frustrated', 'disappointed']
        
        if target_mood in positive_targets and current_sentiment['negative'] > 0.5:
            return "Current text is quite negative - adding positive emoticons will help balance"
        elif target_mood in negative_targets and current_sentiment['positive'] > 0.5:
            return "Current text is quite positive - negative emoticons might create mixed signals"
        else:
            return "Target mood aligns well with current text tone"
    
    def analyze_conversation_flow(self, messages: List[str]) -> Dict[str, any]:
        """
        Analyze emotional flow across multiple messages/conversation.
        
        Args:
            messages (List[str]): List of messages in chronological order
            
        Returns:
            Dict containing conversation flow analysis
        """
        message_analyses = []
        emotion_timeline = []
        
        for i, message in enumerate(messages):
            analysis = self.analyze_comprehensive_emotion(message, include_intensity=False)
            message_analyses.append({
                'message_index': i,
                'text': message,
                'analysis': analysis
            })
            
            # Track dominant emotion over time
            if analysis['raw_analysis']['dominant_emotion']:
                emotion_timeline.append({
                    'index': i,
                    'emotion': analysis['raw_analysis']['dominant_emotion'].emotion,
                    'confidence': analysis['raw_analysis']['dominant_emotion'].confidence
                })
        
        # Analyze trends
        trends = self._analyze_emotional_trends(emotion_timeline)
        
        return {
            'message_analyses': message_analyses,
            'emotion_timeline': emotion_timeline,
            'trends': trends,
            'conversation_summary': self._summarize_conversation(message_analyses, trends)
        }
    
    def _analyze_emotional_trends(self, timeline: List[Dict]) -> Dict[str, any]:
        """Analyze trends in emotional timeline."""
        if len(timeline) < 2:
            return {'trend': 'insufficient_data', 'changes': 0}
        
        emotions = [entry['emotion'] for entry in timeline]
        confidences = [entry['confidence'] for entry in timeline]
        
        # Count emotion changes
        changes = sum(1 for i in range(1, len(emotions)) if emotions[i] != emotions[i-1])
        
        # Determine trend
        if changes == 0:
            trend = 'stable'
        elif changes < len(emotions) * 0.3:
            trend = 'mostly_stable'
        elif changes < len(emotions) * 0.7:
            trend = 'variable'
        else:
            trend = 'highly_variable'
        
        # Confidence trend
        if len(confidences) > 1:
            avg_early = sum(confidences[:len(confidences)//2]) / (len(confidences)//2)
            avg_late = sum(confidences[len(confidences)//2:]) / (len(confidences) - len(confidences)//2)
            confidence_trend = 'increasing' if avg_late > avg_early else 'decreasing' if avg_late < avg_early else 'stable'
        else:
            confidence_trend = 'stable'
        
        return {
            'trend': trend,
            'changes': changes,
            'stability_score': 1 - (changes / max(len(emotions) - 1, 1)),
            'confidence_trend': confidence_trend
        }
    
    def _summarize_conversation(self, analyses: List[Dict], trends: Dict) -> Dict[str, str]:
        """Generate summary of conversation emotional flow."""
        total_messages = len(analyses)
        
        # Count overall sentiment distribution
        positive_count = sum(1 for a in analyses if a['analysis']['summary']['overall_mood'] in ['Positive', 'Very Positive'])
        negative_count = sum(1 for a in analyses if a['analysis']['summary']['overall_mood'] in ['Negative', 'Very Negative'])
        
        summary = {
            'total_messages': str(total_messages),
            'emotional_stability': trends['trend'],
            'overall_tone': 'Positive' if positive_count > negative_count else 'Negative' if negative_count > positive_count else 'Mixed'
        }
        
        if trends['changes'] > total_messages * 0.5:
            summary['conversation_flow'] = "Highly dynamic conversation with frequent emotional shifts"
        elif trends['changes'] > total_messages * 0.2:
            summary['conversation_flow'] = "Moderately dynamic with some emotional variation"
        else:
            summary['conversation_flow'] = "Stable emotional tone throughout conversation"
        
        return summary


# Example usage and integration testing
if __name__ == "__main__":
    print("🚀 MULTIMODAL EMOTION ANALYZER - INTEGRATION TESTING")
    print("=" * 60)
    
    analyzer = MultimodalEmotionAnalyzer()
    
    # Test single message analysis
    test_message = "Just got the promotion I've been working towards! 🎉😊🥳 So grateful and excited for this new chapter! 🙏❤️"
    
    print(f"\n📱 Analyzing: '{test_message}'")
    result = analyzer.analyze_comprehensive_emotion(test_message)
    
    print(f"\n📊 Summary:")
    for key, value in result['summary'].items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n💡 Recommendations:")
    for rec in result['recommendations']:
        print(f"   • {rec}")
    
    # Test mood suggestions
    print(f"\n🎭 Emoticon suggestions for 'excited' mood:")
    suggestions = analyzer.suggest_emoticons_for_mood('excited')
    print(f"   Primary: {suggestions['primary_suggestions']}")
    print(f"   Alternatives: {suggestions['alternative_suggestions']}")
    
    # Test conversation flow
    conversation = [
        "Having a rough morning 😞",
        "But things are looking up! ☺️",
        "Just got some great news! 😊🎉",
        "So excited I can barely contain myself! 😍🤩"
    ]
    
    print(f"\n💬 Conversation Flow Analysis:")
    flow_result = analyzer.analyze_conversation_flow(conversation)
    
    print(f"   Emotional Trend: {flow_result['trends']['trend']}")
    print(f"   Stability Score: {flow_result['trends']['stability_score']:.2f}")
    print(f"   Overall Assessment: {flow_result['conversation_summary']['conversation_flow']}")
    
    print(f"\n✅ Integration testing completed successfully!")
