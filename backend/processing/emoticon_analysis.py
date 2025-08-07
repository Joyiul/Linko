"""
Emoticon Emotion Analysis Module
Provides comprehensive mapping of emoticons to emotions for text analysis
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class EmotionScore:
    """Represents an emotion with its confidence score"""
    emotion: str
    confidence: float
    emoticon: str


class EmoticonEmotionAnalyzer:
    """
    Advanced emoticon-to-emotion mapping system that analyzes text for emoticons
    and provides emotion indicators with confidence scores.
    """
    
    def __init__(self):
        self.emoticon_map = self._build_emoticon_emotion_map()
        self.emotion_weights = self._build_emotion_weights()
        
    def _build_emoticon_emotion_map(self) -> Dict[str, Dict[str, float]]:
        """
        Comprehensive mapping of emoticons to emotions with confidence scores.
        Each emoticon can map to multiple emotions with different weights.
        """
        return {
            # HAPPY/JOY EMOTICONS
            ':)': {'happy': 0.9, 'friendly': 0.7},
            ':-)': {'happy': 0.9, 'friendly': 0.7},
            '😊': {'happy': 0.95, 'friendly': 0.8, 'content': 0.7},
            '😀': {'happy': 0.9, 'excited': 0.8, 'joyful': 0.9},
            '😃': {'happy': 0.9, 'excited': 0.85, 'energetic': 0.8},
            '😄': {'happy': 0.95, 'joyful': 0.9, 'excited': 0.8},
            '😁': {'happy': 0.9, 'excited': 0.8, 'enthusiastic': 0.85},
            '😆': {'happy': 0.85, 'amused': 0.9, 'laughing': 0.95},
            '😂': {'happy': 0.8, 'amused': 0.95, 'laughing': 0.95, 'joyful': 0.9},
            '🤣': {'amused': 0.95, 'laughing': 0.95, 'happy': 0.9},
            '😍': {'happy': 0.8, 'love': 0.95, 'adoration': 0.9},
            '🥰': {'happy': 0.85, 'love': 0.9, 'affectionate': 0.95},
            '😘': {'happy': 0.8, 'love': 0.85, 'affectionate': 0.8},
            '😗': {'happy': 0.7, 'content': 0.8, 'peaceful': 0.7},
            '☺️': {'happy': 0.8, 'content': 0.9, 'peaceful': 0.8},
            '🙂': {'happy': 0.7, 'content': 0.8, 'neutral': 0.6},
            '🤗': {'happy': 0.8, 'friendly': 0.9, 'welcoming': 0.85},
            
            # SAD/UNHAPPY EMOTICONS
            ':(': {'sad': 0.9, 'unhappy': 0.8},
            ':-(': {'sad': 0.9, 'unhappy': 0.8},
            '😢': {'sad': 0.95, 'crying': 0.9, 'upset': 0.8},
            '😭': {'sad': 0.9, 'crying': 0.95, 'devastated': 0.85},
            '😿': {'sad': 0.9, 'crying': 0.85, 'disappointed': 0.8},
            '😞': {'sad': 0.85, 'disappointed': 0.9, 'dejected': 0.8},
            '😔': {'sad': 0.8, 'disappointed': 0.85, 'pensive': 0.7},
            '😟': {'sad': 0.7, 'worried': 0.85, 'concerned': 0.8},
            '😕': {'sad': 0.6, 'confused': 0.7, 'disappointed': 0.75},
            '🙁': {'sad': 0.8, 'unhappy': 0.85, 'disappointed': 0.7},
            '☹️': {'sad': 0.85, 'unhappy': 0.8, 'frowning': 0.9},
            '😥': {'sad': 0.8, 'relieved': 0.6, 'worried': 0.7},
            
            # ANGRY/FRUSTRATED EMOTICONS
            '>:(': {'angry': 0.9, 'frustrated': 0.8},
            '😠': {'angry': 0.9, 'mad': 0.85, 'frustrated': 0.8},
            '😡': {'angry': 0.95, 'furious': 0.9, 'rage': 0.85},
            '🤬': {'angry': 0.95, 'furious': 0.95, 'swearing': 0.9},
            '😤': {'angry': 0.8, 'frustrated': 0.9, 'huffing': 0.85},
            '😾': {'angry': 0.85, 'grumpy': 0.8, 'annoyed': 0.9},
            '🙄': {'annoyed': 0.85, 'sarcastic': 0.8, 'dismissive': 0.75},
            
            # SURPRISED/SHOCKED EMOTICONS
            ':O': {'surprised': 0.9, 'shocked': 0.8},
            '😮': {'surprised': 0.9, 'shocked': 0.8, 'amazed': 0.7},
            '😯': {'surprised': 0.85, 'amazed': 0.8, 'wondering': 0.7},
            '😲': {'surprised': 0.95, 'shocked': 0.9, 'astonished': 0.85},
            '🤯': {'surprised': 0.8, 'shocked': 0.95, 'mind_blown': 0.95},
            '😱': {'surprised': 0.8, 'shocked': 0.9, 'fearful': 0.85, 'screaming': 0.9},
            
            # FEARFUL/ANXIOUS EMOTICONS
            '😨': {'fearful': 0.9, 'anxious': 0.85, 'scared': 0.8},
            '😰': {'fearful': 0.8, 'anxious': 0.9, 'nervous': 0.85},
            '😱': {'fearful': 0.85, 'terrified': 0.9, 'shocked': 0.8},
            '🫣': {'fearful': 0.7, 'embarrassed': 0.8, 'shy': 0.75},
            
            # DISGUSTED EMOTICONS
            '🤢': {'disgusted': 0.9, 'nauseous': 0.95, 'sick': 0.8},
            '🤮': {'disgusted': 0.95, 'nauseous': 0.95, 'vomiting': 0.95},
            '😷': {'sick': 0.8, 'unwell': 0.85, 'masked': 0.7},
            
            # NEUTRAL/THINKING EMOTICONS
            '😐': {'neutral': 0.9, 'expressionless': 0.85},
            '😑': {'neutral': 0.8, 'expressionless': 0.9, 'unimpressed': 0.7},
            '🤔': {'thinking': 0.9, 'pondering': 0.85, 'contemplative': 0.8},
            '🧐': {'thinking': 0.85, 'analytical': 0.9, 'scrutinizing': 0.8},
            '😶': {'neutral': 0.8, 'speechless': 0.85, 'silent': 0.9},
            
            # CONFUSED EMOTICONS
            '😕': {'confused': 0.8, 'uncertain': 0.75, 'disappointed': 0.6},
            '😵': {'confused': 0.9, 'dizzy': 0.85, 'overwhelmed': 0.8},
            '🤷': {'confused': 0.7, 'indifferent': 0.8, 'shrugging': 0.9},
            '🫤': {'confused': 0.7, 'uncertain': 0.8, 'meh': 0.75},
            
            # PLAYFUL/MISCHIEVOUS EMOTICONS
            ';)': {'playful': 0.9, 'flirty': 0.8, 'winking': 0.95},
            ';-)': {'playful': 0.9, 'flirty': 0.8, 'winking': 0.95},
            '😉': {'playful': 0.9, 'flirty': 0.8, 'winking': 0.95},
            '😜': {'playful': 0.95, 'silly': 0.9, 'teasing': 0.85},
            '😝': {'playful': 0.9, 'silly': 0.95, 'teasing': 0.8},
            '🤪': {'playful': 0.85, 'silly': 0.9, 'crazy': 0.8},
            '😛': {'playful': 0.9, 'silly': 0.8, 'teasing': 0.85},
            '🤭': {'playful': 0.7, 'shy': 0.8, 'giggling': 0.85},
            
            # COOL/CONFIDENT EMOTICONS
            '😎': {'cool': 0.95, 'confident': 0.85, 'relaxed': 0.8},
            '🤓': {'smart': 0.9, 'nerdy': 0.95, 'studious': 0.85},
            
            # SLEEPY/TIRED EMOTICONS
            '😴': {'sleepy': 0.95, 'tired': 0.9, 'peaceful': 0.7},
            '😪': {'sleepy': 0.9, 'tired': 0.95, 'drowsy': 0.85},
            '🥱': {'tired': 0.85, 'bored': 0.8, 'yawning': 0.95},
            
            # HEART/LOVE EMOTICONS
            '❤️': {'love': 0.95, 'affection': 0.9, 'caring': 0.85},
            '💙': {'love': 0.9, 'calm': 0.7, 'peaceful': 0.6},
            '💚': {'love': 0.9, 'nature': 0.7, 'growth': 0.6},
            '💛': {'love': 0.9, 'friendship': 0.85, 'cheerful': 0.7},
            '🧡': {'love': 0.9, 'warm': 0.8, 'energetic': 0.7},
            '💜': {'love': 0.9, 'mysterious': 0.6, 'creative': 0.7},
            '🖤': {'love': 0.8, 'dark': 0.7, 'gothic': 0.8},
            '🤍': {'love': 0.85, 'pure': 0.9, 'innocent': 0.8},
            '💕': {'love': 0.9, 'sweet': 0.85, 'affectionate': 0.9},
            '💖': {'love': 0.95, 'sparkling': 0.8, 'excited': 0.7},
            '💗': {'love': 0.9, 'growing': 0.8, 'developing': 0.7},
            '💘': {'love': 0.95, 'romantic': 0.9, 'struck': 0.8},
            '💝': {'love': 0.9, 'gift': 0.8, 'present': 0.85},
            
            # CELEBRATION/PARTY EMOTICONS
            '🎉': {'celebrating': 0.95, 'party': 0.9, 'festive': 0.85, 'happy': 0.8},
            '🎊': {'celebrating': 0.9, 'party': 0.95, 'confetti': 0.9, 'happy': 0.8},
            '🥳': {'celebrating': 0.95, 'party': 0.9, 'birthday': 0.8, 'happy': 0.85},
            '🍾': {'celebrating': 0.8, 'champagne': 0.9, 'success': 0.7},
            
            # THUMBS/APPROVAL EMOTICONS
            '👍': {'approval': 0.9, 'positive': 0.85, 'good': 0.8},
            '👎': {'disapproval': 0.9, 'negative': 0.85, 'bad': 0.8},
            '👌': {'perfect': 0.9, 'okay': 0.85, 'approval': 0.8},
            '✌️': {'peace': 0.9, 'victory': 0.8, 'positive': 0.7},
            '🤘': {'rock': 0.9, 'cool': 0.8, 'rebellious': 0.7},
            '🙏': {'grateful': 0.9, 'praying': 0.85, 'thankful': 0.8, 'respectful': 0.7},
            
            # CLASSICAL TEXT EMOTICONS
            'XD': {'laughing': 0.9, 'amused': 0.85, 'happy': 0.8},
            'xD': {'laughing': 0.9, 'amused': 0.85, 'happy': 0.8},
            ':P': {'playful': 0.9, 'silly': 0.8, 'teasing': 0.75},
            ':p': {'playful': 0.9, 'silly': 0.8, 'teasing': 0.75},
            '=)': {'happy': 0.8, 'content': 0.7},
            '=(': {'sad': 0.8, 'unhappy': 0.7},
            ':D': {'happy': 0.9, 'excited': 0.8, 'joyful': 0.85},
            ':|': {'neutral': 0.9, 'indifferent': 0.8},
            ':/': {'confused': 0.8, 'uncertain': 0.75, 'skeptical': 0.7},
            ':\\': {'confused': 0.8, 'uncertain': 0.75, 'awkward': 0.7},
            '<3': {'love': 0.95, 'heart': 0.9, 'affection': 0.85},
            '</3': {'heartbroken': 0.95, 'sad': 0.8, 'broken': 0.9},
        }
    
    def _build_emotion_weights(self) -> Dict[str, float]:
        """
        Define weights for different emotion categories to help with overall sentiment analysis.
        """
        return {
            # Primary emotions (high weight)
            'happy': 1.0, 'sad': 1.0, 'angry': 1.0, 'fearful': 1.0, 'surprised': 1.0, 'disgusted': 1.0,
            
            # Secondary emotions (medium-high weight)
            'joyful': 0.9, 'excited': 0.9, 'frustrated': 0.9, 'anxious': 0.9, 'confused': 0.8,
            'love': 0.95, 'content': 0.8, 'playful': 0.8, 'disappointed': 0.85,
            
            # Tertiary emotions (medium weight)
            'amused': 0.7, 'friendly': 0.7, 'cool': 0.6, 'tired': 0.6, 'thinking': 0.5,
            'neutral': 0.3, 'peaceful': 0.6, 'celebrating': 0.8,
            
            # Specific states (lower weight)
            'laughing': 0.6, 'crying': 0.8, 'winking': 0.4, 'approval': 0.6, 'disapproval': 0.6
        }
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """
        Analyze text for emoticons and return comprehensive emotion analysis.
        
        Args:
            text (str): Text to analyze for emoticons
            
        Returns:
            Dict containing emotion analysis results
        """
        if not text:
            return self._empty_result()
        
        # Find all emoticons in text
        found_emoticons = self._extract_emoticons(text)
        
        if not found_emoticons:
            return self._empty_result()
        
        # Calculate emotion scores
        emotion_scores = self._calculate_emotion_scores(found_emoticons)
        
        # Determine dominant emotion
        dominant_emotion = self._get_dominant_emotion(emotion_scores)
        
        # Calculate overall sentiment
        sentiment = self._calculate_sentiment(emotion_scores)
        
        return {
            'emoticons_found': found_emoticons,
            'emotion_scores': emotion_scores,
            'dominant_emotion': dominant_emotion,
            'sentiment': sentiment,
            'total_emoticons': len(found_emoticons),
            'confidence': dominant_emotion.confidence if dominant_emotion else 0.0
        }
    
    def _extract_emoticons(self, text: str) -> List[str]:
        """Extract all recognized emoticons from text."""
        found = []
        
        # Sort emoticons by length (longest first) to avoid partial matches
        sorted_emoticons = sorted(self.emoticon_map.keys(), key=len, reverse=True)
        
        for emoticon in sorted_emoticons:
            if emoticon in text:
                # Count occurrences
                count = text.count(emoticon)
                found.extend([emoticon] * count)
        
        return found
    
    def _calculate_emotion_scores(self, emoticons: List[str]) -> Dict[str, float]:
        """Calculate weighted emotion scores from found emoticons."""
        emotion_totals = defaultdict(float)
        emotion_counts = defaultdict(int)
        
        for emoticon in emoticons:
            emotions = self.emoticon_map.get(emoticon, {})
            for emotion, confidence in emotions.items():
                weight = self.emotion_weights.get(emotion, 0.5)
                emotion_totals[emotion] += confidence * weight
                emotion_counts[emotion] += 1
        
        # Calculate average scores
        emotion_scores = {}
        for emotion, total in emotion_totals.items():
            emotion_scores[emotion] = total / emotion_counts[emotion]
        
        return emotion_scores
    
    def _get_dominant_emotion(self, emotion_scores: Dict[str, float]) -> Optional[EmotionScore]:
        """Determine the dominant emotion from scores."""
        if not emotion_scores:
            return None
        
        dominant = max(emotion_scores.items(), key=lambda x: x[1])
        return EmotionScore(
            emotion=dominant[0],
            confidence=dominant[1],
            emoticon=""  # Could be enhanced to track which emoticon contributed most
        )
    
    def _calculate_sentiment(self, emotion_scores: Dict[str, float]) -> Dict[str, float]:
        """Calculate overall sentiment polarity."""
        positive_emotions = ['happy', 'joyful', 'excited', 'love', 'content', 'playful', 'celebrating', 'approval']
        negative_emotions = ['sad', 'angry', 'fearful', 'disgusted', 'frustrated', 'disappointed', 'disapproval']
        neutral_emotions = ['neutral', 'thinking', 'confused', 'surprised']
        
        positive_score = sum(emotion_scores.get(emotion, 0) for emotion in positive_emotions)
        negative_score = sum(emotion_scores.get(emotion, 0) for emotion in negative_emotions)
        neutral_score = sum(emotion_scores.get(emotion, 0) for emotion in neutral_emotions)
        
        total = positive_score + negative_score + neutral_score
        
        if total == 0:
            return {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
        
        return {
            'positive': positive_score / total,
            'negative': negative_score / total,
            'neutral': neutral_score / total
        }
    
    def _empty_result(self) -> Dict[str, any]:
        """Return empty analysis result."""
        return {
            'emoticons_found': [],
            'emotion_scores': {},
            'dominant_emotion': None,
            'sentiment': {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0},
            'total_emoticons': 0,
            'confidence': 0.0
        }
    
    def get_emotion_suggestions(self, current_emotion: str) -> List[str]:
        """
        Get emoticon suggestions for a given emotion.
        
        Args:
            current_emotion (str): Target emotion
            
        Returns:
            List of emoticons that express this emotion
        """
        suggestions = []
        for emoticon, emotions in self.emoticon_map.items():
            if current_emotion.lower() in emotions:
                suggestions.append(emoticon)
        
        # Sort by confidence score for the emotion
        suggestions.sort(key=lambda x: self.emoticon_map[x].get(current_emotion.lower(), 0), reverse=True)
        return suggestions[:10]  # Return top 10
    
    def analyze_emotion_intensity(self, text: str) -> Dict[str, float]:
        """
        Analyze the intensity of emotions in text based on emoticon frequency and type.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict mapping emotions to intensity scores (0-1)
        """
        analysis = self.analyze_text(text)
        emotion_scores = analysis['emotion_scores']
        total_emoticons = analysis['total_emoticons']
        
        # Intensity is based on both score and frequency
        intensity_scores = {}
        for emotion, score in emotion_scores.items():
            # Factor in frequency - more emoticons = higher intensity
            frequency_boost = min(total_emoticons / 10, 1.0)  # Cap at 1.0
            intensity_scores[emotion] = min(score * (1 + frequency_boost), 1.0)
        
        return intensity_scores


# Example usage and testing
if __name__ == "__main__":
    analyzer = EmoticonEmotionAnalyzer()
    
    # Test cases
    test_texts = [
        "I'm so happy today! 😊😀🎉",
        "This is terrible 😢😭😞",
        "What?! 😲🤯 That's amazing!",
        "I love this so much! 😍❤️💕",
        "Ugh, so frustrated 😤😠",
        "Having a great time at the party! 🥳🎊🍾",
        "Just thinking... 🤔😐",
        "LOL that's hilarious! 😂🤣XD",
        "Not sure about this :/ 🤷",
        "Thanks so much! 🙏😊👍"
    ]
    
    print("=== EMOTICON EMOTION ANALYSIS RESULTS ===\n")
    
    for text in test_texts:
        print(f"Text: '{text}'")
        result = analyzer.analyze_text(text)
        print(f"Emoticons found: {result['emoticons_found']}")
        print(f"Dominant emotion: {result['dominant_emotion'].emotion if result['dominant_emotion'] else 'None'} "
              f"(confidence: {result['dominant_emotion'].confidence if result['dominant_emotion'] else 0:.2f})")
        print(f"Sentiment: Positive: {result['sentiment']['positive']:.2f}, "
              f"Negative: {result['sentiment']['negative']:.2f}, "
              f"Neutral: {result['sentiment']['neutral']:.2f}")
        print(f"Top emotions: {dict(list(result['emotion_scores'].items())[:3])}")
        print("-" * 50)
