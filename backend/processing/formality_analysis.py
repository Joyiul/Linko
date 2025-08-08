import re
import os
import pandas as pd
from collections import Counter

class FormalityAnalyzer:
    def __init__(self):
        """Initialize formality analyzer with comprehensive patterns"""
        
        # Formal language indicators
        self.formal_patterns = {
            'academic_words': [
                'furthermore', 'consequently', 'nevertheless', 'notwithstanding', 'pursuant', 
                'aforementioned', 'subsequent', 'facilitate', 'demonstrate', 'establish',
                'implement', 'analyze', 'evaluate', 'synthesize', 'constitute', 'endeavor',
                'ascertain', 'utilize', 'commence', 'terminate', 'subsequent', 'preliminary',
                'comprehensive', 'substantial', 'significant', 'exemplify', 'illustrate'
            ],
            'formal_phrases': [
                'i would like to', 'i am writing to', 'i would be grateful', 'please find attached',
                'thank you for your consideration', 'i look forward to', 'yours sincerely',
                'yours faithfully', 'dear sir/madam', 'to whom it may concern', 'in accordance with',
                'with regard to', 'pursuant to', 'in compliance with', 'i am pleased to inform',
                'please be advised', 'we regret to inform', 'it has come to our attention'
            ],
            'formal_structures': [
                r'\bi am writing to\b', r'\bplease be advised\b', r'\bi would like to request\b',
                r'\bit is my understanding\b', r'\bi trust this finds you well\b',
                r'\bthank you for your time and consideration\b'
            ],
            'polite_requests': [
                'would you be so kind', 'if you would be so kind', 'i would appreciate',
                'could you please', 'would it be possible', 'i wonder if you might',
                'perhaps you could', 'if it is not too much trouble'
            ]
        }
        
        # Informal language indicators
        self.informal_patterns = {
            'contractions': [
                "won't", "can't", "don't", "doesn't", "didn't", "wasn't", "weren't", "haven't",
                "hasn't", "hadn't", "shouldn't", "wouldn't", "couldn't", "isn't", "aren't",
                "i'm", "you're", "we're", "they're", "it's", "that's", "what's", "who's",
                "i'll", "you'll", "we'll", "they'll", "i'd", "you'd", "we'd", "they'd",
                "i've", "you've", "we've", "they've"
            ],
            'casual_words': [
                'yeah', 'nah', 'yep', 'nope', 'ok', 'okay', 'cool', 'awesome', 'great',
                'nice', 'sweet', 'dude', 'guy', 'folks', 'stuff', 'things', 'kinda',
                'sorta', 'gonna', 'wanna', 'gotta', 'dunno', 'lemme', 'gimme'
            ],
            'informal_phrases': [
                'how are you doing', 'what\'s up', 'how\'s it going', 'see you later',
                'talk to you soon', 'catch you later', 'take care', 'no worries',
                'no problem', 'you bet', 'for sure', 'totally', 'absolutely'
            ],
            'filler_words': [
                'like', 'you know', 'i mean', 'basically', 'literally', 'actually',
                'honestly', 'seriously', 'obviously', 'definitely', 'probably'
            ]
        }
        
        # Very casual/slang indicators
        self.casual_patterns = {
            'slang_words': [
                'bro', 'sis', 'bestie', 'fam', 'squad', 'lit', 'fire', 'sick', 'dope',
                'epic', 'legit', 'sus', 'vibe', 'mood', 'flex', 'salty', 'savage',
                'periodt', 'lowkey', 'highkey', 'deadass', 'fr', 'ngl', 'tbh', 'imo',
                'lol', 'lmao', 'wtf', 'omg', 'brb', 'ttyl', 'dm', 'slide'
            ],
            'internet_slang': [
                'smh', 'fomo', 'yolo', 'tfw', 'mfw', 'irl', 'af', 'goat', 'stan',
                'ship', 'simp', 'karen', 'boomer', 'zoomer', 'cancelled', 'ghosted',
                'finsta', 'spam', 'story', 'post', 'dm', 'slide into dms'
            ],
            'intensifiers': [
                'hella', 'mad', 'crazy', 'insane', 'wild', 'nuts', 'bananas',
                'stupid good', 'dummy thicc', 'lowkey fire', 'no cap'
            ]
        }
        
        # Professional/business language
        self.professional_patterns = {
            'business_terms': [
                'synergy', 'leverage', 'optimize', 'streamline', 'paradigm', 'benchmark',
                'deliverable', 'stakeholder', 'roi', 'kpi', 'metrics', 'actionable',
                'scalable', 'bandwidth', 'circle back', 'touch base', 'reach out',
                'drill down', 'deep dive', 'best practice', 'win-win', 'game changer'
            ],
            'corporate_phrases': [
                'think outside the box', 'low hanging fruit', 'move the needle',
                'let\'s take this offline', 'i\'ll circle back', 'let\'s touch base',
                'we need to ideate', 'let\'s brainstorm', 'action items',
                'going forward', 'at the end of the day', 'it is what it is'
            ]
        }
        
        # Load additional datasets if available
        self._load_additional_patterns()
    
    def _load_additional_patterns(self):
        """Load additional formality patterns from datasets"""
        try:
            # Try to load Gen Z slang from existing dataset
            datasets_path = os.path.join(os.path.dirname(__file__), '..', 'Datasets')
            
            # Load Gen Z slang
            genz_path = os.path.join(datasets_path, 'genz_slang.csv')
            if os.path.exists(genz_path):
                genz_df = pd.read_csv(genz_path)
                if 'term' in genz_df.columns:
                    genz_terms = genz_df['term'].str.lower().tolist()
                    self.casual_patterns['slang_words'].extend(genz_terms[:50])  # Add top 50
            
            # Load general slang
            slang_path = os.path.join(datasets_path, 'slang.csv')
            if os.path.exists(slang_path):
                slang_df = pd.read_csv(slang_path)
                if 'slang' in slang_df.columns:
                    slang_terms = slang_df['slang'].str.lower().tolist()
                    self.casual_patterns['slang_words'].extend(slang_terms[:50])  # Add top 50
                    
        except Exception as e:
            print(f"Note: Could not load additional slang datasets: {e}")
    
    def analyze_formality(self, text):
        """
        Analyze the formality level of given text
        Returns detailed formality analysis
        """
        if not text or not text.strip():
            return {
                'formality_level': 'unknown',
                'confidence': 0.0,
                'details': {},
                'indicators': []
            }
        
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Count different formality indicators
        formal_score = 0
        informal_score = 0
        casual_score = 0
        professional_score = 0
        
        indicators = {
            'formal': [],
            'informal': [],
            'casual': [],
            'professional': []
        }
        
        # Check formal patterns
        for word in self.formal_patterns['academic_words']:
            if word in text_lower:
                formal_score += 3
                indicators['formal'].append(f"Academic word: '{word}'")
        
        for phrase in self.formal_patterns['formal_phrases']:
            if phrase in text_lower:
                formal_score += 5
                indicators['formal'].append(f"Formal phrase: '{phrase}'")
        
        for pattern in self.formal_patterns['formal_structures']:
            if re.search(pattern, text_lower, re.IGNORECASE):
                formal_score += 4
                indicators['formal'].append(f"Formal structure detected")
        
        for phrase in self.formal_patterns['polite_requests']:
            if phrase in text_lower:
                formal_score += 3
                indicators['formal'].append(f"Polite request: '{phrase}'")
        
        # Check informal patterns
        for contraction in self.informal_patterns['contractions']:
            if contraction in text_lower:
                informal_score += 2
                indicators['informal'].append(f"Contraction: '{contraction}'")
        
        for word in self.informal_patterns['casual_words']:
            if word in text_lower:
                informal_score += 2
                indicators['informal'].append(f"Casual word: '{word}'")
        
        for phrase in self.informal_patterns['informal_phrases']:
            if phrase in text_lower:
                informal_score += 3
                indicators['informal'].append(f"Informal phrase: '{phrase}'")
        
        for filler in self.informal_patterns['filler_words']:
            count = len(re.findall(r'\b' + filler + r'\b', text_lower))
            if count > 0:
                informal_score += count * 1
                indicators['informal'].append(f"Filler word: '{filler}' ({count}x)")
        
        # Check casual/slang patterns
        for slang in self.casual_patterns['slang_words']:
            if slang in text_lower:
                casual_score += 3
                indicators['casual'].append(f"Slang: '{slang}'")
        
        for internet_slang in self.casual_patterns['internet_slang']:
            if internet_slang in text_lower:
                casual_score += 4
                indicators['casual'].append(f"Internet slang: '{internet_slang}'")
        
        for intensifier in self.casual_patterns['intensifiers']:
            if intensifier in text_lower:
                casual_score += 2
                indicators['casual'].append(f"Casual intensifier: '{intensifier}'")
        
        # Check professional patterns
        for term in self.professional_patterns['business_terms']:
            if term in text_lower:
                professional_score += 3
                indicators['professional'].append(f"Business term: '{term}'")
        
        for phrase in self.professional_patterns['corporate_phrases']:
            if phrase in text_lower:
                professional_score += 4
                indicators['professional'].append(f"Corporate phrase: '{phrase}'")
        
        # Additional indicators
        # Check sentence structure complexity
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / max(len([s for s in sentences if s.strip()]), 1)
        
        if avg_sentence_length > 20:
            formal_score += 2
            indicators['formal'].append(f"Complex sentences (avg {avg_sentence_length:.1f} words)")
        elif avg_sentence_length < 8:
            casual_score += 1
            indicators['casual'].append(f"Short sentences (avg {avg_sentence_length:.1f} words)")
        
        # Check punctuation patterns
        exclamation_count = text.count('!')
        if exclamation_count > 2:
            casual_score += exclamation_count
            indicators['casual'].append(f"Multiple exclamations ({exclamation_count})")
        
        # Check capitalization patterns
        if text.isupper():
            casual_score += 3
            indicators['casual'].append("ALL CAPS usage")
        elif any(word.isupper() for word in text.split()):
            casual_score += 1
            indicators['casual'].append("Some words in caps")
        
        # Determine formality level
        scores = {
            'formal': formal_score,
            'professional': professional_score,
            'informal': informal_score,
            'casual': casual_score
        }
        
        max_score = max(scores.values())
        total_score = sum(scores.values())
        
        if max_score == 0:
            formality_level = 'neutral'
            confidence = 0.3
        else:
            formality_level = max(scores, key=scores.get)
            confidence = min(max_score / max(total_score, 1) * 1.2, 0.95)
        
        # Detailed breakdown
        details = {
            'scores': scores,
            'total_indicators': sum(len(indicators[key]) for key in indicators),
            'word_count': word_count,
            'avg_sentence_length': avg_sentence_length,
            'formality_distribution': {
                key: round(score / max(total_score, 1) * 100, 1) 
                for key, score in scores.items()
            }
        }
        
        return {
            'formality_level': formality_level,
            'confidence': confidence,
            'details': details,
            'indicators': indicators,
            'summary': self._generate_formality_summary(formality_level, confidence, indicators)
        }
    
    def _generate_formality_summary(self, level, confidence, indicators):
        """Generate a human-readable summary of formality analysis with reactions"""
        # Base summaries with personality
        summaries = {
            'formal': "🎓 **Academic/Formal language detected!** This text uses sophisticated vocabulary, complex sentence structures, and very polite expressions. Perfect for academic or official contexts!",
            'professional': "💼 **Professional/Business language detected!** This text uses corporate terminology and structured communication. Great for workplace environments!",
            'informal': "💬 **Conversational language detected!** This text uses everyday language with contractions and casual expressions. Perfect for friendly conversations!",
            'casual': "😎 **Very casual language detected!** This text uses relaxed slang, informal expressions, and a laid-back tone. Ideal for texting with friends!",
            'neutral': "📝 **Neutral tone detected** - This text maintains a balanced approach without strong formality indicators. Versatile for many situations!"
        }
        
        base_summary = summaries.get(level, "🤔 Formality level unclear.")
        
        # Add confidence level with reactions
        if confidence >= 0.8:
            confidence_desc = " 🎯 (High confidence - very clear indicators!)"
        elif confidence >= 0.6:
            confidence_desc = " ✅ (Good confidence - clear patterns detected)"
        else:
            confidence_desc = " 🔍 (Some indicators found, but not overwhelming)"
        
        # Add key indicators with emojis
        key_indicators = []
        for category, items in indicators.items():
            if items and len(items) > 0:
                emoji_map = {
                    'formal': '🎓',
                    'professional': '💼', 
                    'informal': '💬',
                    'casual': '😎'
                }
                emoji = emoji_map.get(category, '📍')
                key_indicators.append(f"{emoji} {len(items)} {category} indicators")
        
        if key_indicators:
            indicator_summary = f"\n\n**🔍 Found:** {', '.join(key_indicators)}."
        else:
            indicator_summary = ""
        
        # Add appropriate reactions based on formality level
        reactions = {
            'formal': "\n\n📚 **Reaction:** This is excellent for academic papers, official documents, or formal presentations!",
            'professional': "\n\n💼 **Reaction:** Perfect for business emails, reports, or professional communication!",
            'informal': "\n\n😊 **Reaction:** Great for everyday conversations, friendly emails, or casual writing!",
            'casual': "\n\n🤙 **Reaction:** Awesome for texting, social media, or chatting with friends!",
            'neutral': "\n\n⚖️ **Reaction:** This balanced tone works well in most situations!"
        }
        
        reaction = reactions.get(level, "")
        
        return base_summary + confidence_desc + indicator_summary + reaction

# Global instance for easy import
formality_analyzer = FormalityAnalyzer()

def analyze_formality(text):
    """Convenience function for formality analysis"""
    return formality_analyzer.analyze_formality(text)
