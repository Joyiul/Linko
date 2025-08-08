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
        Enhanced formality analysis with improved accuracy and confidence scoring
        """
        import re  # Explicit import to fix scoping issue
        
        if not text or not text.strip():
            return {
                'formality_level': 'unknown',
                'confidence': 0.0,
                'details': {},
                'indicators': []
            }
        
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Enhanced scoring system with weighted categories
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
        
        # Enhanced formal pattern detection
        for word in self.formal_patterns['academic_words']:
            if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                formal_score += 4  # Higher weight for exact word matches
                indicators['formal'].append(f"Academic word: '{word}'")
        
        for phrase in self.formal_patterns['formal_phrases']:
            if phrase in text_lower:
                formal_score += 6  # Higher weight for formal phrases
                indicators['formal'].append(f"Formal phrase: '{phrase}'")
        
        for pattern in self.formal_patterns['formal_structures']:
            if re.search(pattern, text_lower, re.IGNORECASE):
                formal_score += 5  # Higher weight for formal structures
                indicators['formal'].append(f"Formal structure detected")
        
        # Enhanced grammar and punctuation analysis
        sentence_count = len([s for s in text.split('.') if s.strip()])
        if sentence_count > 0:
            avg_words_per_sentence = word_count / sentence_count
            if avg_words_per_sentence > 15:  # Complex sentences indicate formality
                formal_score += 3
                indicators['formal'].append("Complex sentence structure")
        
        # Check for proper capitalization
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        proper_caps = sum(1 for s in sentences if s and s[0].isupper())
        if sentences and proper_caps / len(sentences) > 0.8:
            formal_score += 2
            indicators['formal'].append("Proper capitalization")
        
        # Enhanced informal pattern detection
        for word in self.informal_patterns['contractions']:
            if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                informal_score += 3
                indicators['informal'].append(f"Contraction: '{word}'")
        
        for phrase in self.informal_patterns['informal_phrases']:
            if phrase in text_lower:
                informal_score += 4
                indicators['informal'].append(f"Informal phrase: '{phrase}'")
        
        for word in self.informal_patterns['filler_words']:
            if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                informal_score += 2
                indicators['informal'].append(f"Filler word: '{word}'")
        
        # Enhanced casual/slang detection
        for word in self.casual_patterns['slang_words']:
            if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                casual_score += 5  # High weight for slang
                indicators['casual'].append(f"Slang: '{word}'")
        
        for word in self.casual_patterns['internet_slang']:
            if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                casual_score += 6  # Very high weight for internet slang
                indicators['casual'].append(f"Internet slang: '{word}'")
        
        for word in self.casual_patterns['intensifiers']:
            if word in text_lower:
                casual_score += 4
                indicators['casual'].append(f"Casual intensifier: '{word}'")
        
        # Enhanced professional language detection
        for word in self.professional_patterns['business_terms']:
            if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                professional_score += 5
                indicators['professional'].append(f"Business term: '{word}'")
        
        for phrase in self.professional_patterns['corporate_phrases']:
            if phrase in text_lower:
                professional_score += 6
                indicators['professional'].append(f"Corporate phrase: '{phrase}'")
        
        # Additional analysis factors
        # Check for excessive punctuation (indicates casualness)
        if text.count('!') > 2 or text.count('?') > 2:
            casual_score += 2
            indicators['casual'].append("Excessive punctuation")
        
        # Check for ALL CAPS (usually casual/emotional)
        caps_words = [word for word in text.split() if word.isupper() and len(word) > 2]
        if len(caps_words) > 1:
            casual_score += 3
            indicators['casual'].append("Multiple caps words")
        
        # Check for emoji usage (casual indicator)
        import re
        emoji_pattern = re.compile("["
                                 "\U0001F600-\U0001F64F"  # emoticons
                                 "\U0001F300-\U0001F5FF"  # symbols & pictographs
                                 "\U0001F680-\U0001F6FF"  # transport & map symbols
                                 "\U0001F1E0-\U0001F1FF"  # flags
                                 "]+", flags=re.UNICODE)
        if emoji_pattern.findall(text):
            casual_score += 3
            indicators['casual'].append("Contains emojis")
        
        # Normalize scores by text length for better accuracy
        length_factor = min(word_count / 10, 3)  # Cap the length factor
        formal_score = formal_score * length_factor / word_count if word_count > 0 else 0
        informal_score = informal_score * length_factor / word_count if word_count > 0 else 0
        casual_score = casual_score * length_factor / word_count if word_count > 0 else 0
        professional_score = professional_score * length_factor / word_count if word_count > 0 else 0
        
        # Enhanced decision logic with better thresholds
        scores = {
            'formal': formal_score,
            'professional': professional_score,
            'informal': informal_score,
            'casual': casual_score
        }
        
        max_score = max(scores.values())
        dominant_style = max(scores, key=scores.get)
        
        # Improved confidence calculation
        if max_score > 0.5:
            confidence = min(0.7 + (max_score - 0.5) * 0.4, 0.95)
        elif max_score > 0.2:
            confidence = 0.5 + (max_score - 0.2) * 0.6
        else:
            confidence = max_score * 2.5
        
        # Determine final formality level with better logic
        if dominant_style == 'formal' and formal_score > 0.3:
            formality_level = 'formal'
        elif dominant_style == 'professional' and professional_score > 0.3:
            formality_level = 'professional'
        elif dominant_style == 'casual' and casual_score > 0.4:
            formality_level = 'casual'
        elif dominant_style == 'informal' and informal_score > 0.2:
            formality_level = 'informal'
        else:
            formality_level = 'neutral'
            confidence = max(confidence, 0.4)  # Minimum confidence for neutral
        
        return {
            'formality_level': formality_level,
            'confidence': confidence,
            'details': {
                'scores': scores,
                'word_count': word_count,
                'dominant_indicators': len(indicators[dominant_style]) if dominant_style in indicators else 0,
                'formality_distribution': {
                    key: round(score / max(sum(scores.values()), 1) * 100, 1) 
                    for key, score in scores.items()
                }
            },
            'indicators': indicators[formality_level] if formality_level in indicators else [],
            'all_indicators': indicators,
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
