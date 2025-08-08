import re
import numpy as np
import os
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SarcasmDetector:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize OpenAI client for sarcasm highlighting
        self.client = None
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if self.api_key:
            try:
                import openai
                openai.api_key = self.api_key
                self.client = openai
                print("✅ OpenAI client initialized for sarcasm highlighting")
            except ImportError:
                print("⚠️ OpenAI package not installed. Using rule-based highlighting.")
                self.client = None
        else:
            print("⚠️ OPENAI_API_KEY not found. Using rule-based sarcasm highlighting.")
        
        # Sarcasm indicators and patterns
        self.sarcasm_phrases = [
            # Work/employment sarcasm
            "work 40 hours just to be poor",
            "work 40 hours just to be broke",
            "work full time just to be poor",
            "love working for peanuts",
            "live to work",
            "work to die",
            "working for free",
            "can't afford to live",
            "work all day and still broke",
            "work harder for less money",
            "thanks for the poverty wage",
            "love being overworked and underpaid",
            "great benefits like poverty",
            "amazing salary of nothing",
            
            # General sarcastic expressions
            "just great",
            "now great",
            "great im stuck",
            "great i'm stuck", 
            "oh wonderful",
            "how lovely",
            "that's perfect",
            "exactly what i wanted",
            "couldn't be better", 
            "living the dream",
            "what a surprise",
            "how shocking",
            "well that's fantastic",
            "oh joy",
            "thrilled about",
            "love it when",
            "my favorite thing",
            "brilliant idea",
            "genius move",
            "real smart",
            "very helpful",
            "super useful",
            "absolutely perfect",
            "couldn't ask for more",
            "just peachy",
            "fan-freaking-tastic",
            "oh how nice",
            "what fun",
            
            # Frustration patterns (stuck, problems, issues)
            "great now im stuck",
            "great now i'm stuck", 
            "perfect im stuck",
            "perfect i'm stuck",
            "wonderful im stuck", 
            "wonderful i'm stuck",
            "lovely im stuck",
            "lovely i'm stuck",
            "amazing im stuck",
            "amazing i'm stuck",
            "fantastic im stuck",
            "fantastic i'm stuck",
            "great my problem",
            "perfect my issue",
            "wonderful my trouble",
            "brilliant now what",
            "excellent now im",
            "excellent now i'm",
            "marvelous im stuck",
            "marvelous i'm stuck",
            
            # Computer/tech problems
            "perfect my computer crashed",
            "perfect computer crashed",
            "great my computer",
            "wonderful crashed again",
            "amazing it broke",
            "fantastic broken again",
            "lovely it's broken",
            "brilliant crashed",
            "excellent broken",
            
            # Work overtime sarcasm  
            "love working overtime",
            "love overtime",
            "enjoy working late",
            "love extra hours",
            "love unpaid work",
            "enjoy unpaid overtime",
            "love working for free",
            "enjoy free work",
            
            # Contradiction patterns
            "yeah right",
            "sure thing",
            "of course",
            "obviously",
            "clearly",
            "definitely",
            "absolutely",
            "totally",
            "for sure",
            
            # Economic/financial sarcasm
            "rich enough to afford",
            "rolling in money",
            "swimming in cash",
            "financially stable",
            "easy to pay for",
            "such good pay",
            "amazing benefits",
            "great compensation",
            "love paying bills",
            "so affordable",
            "cheap enough for me",
            "within my budget",
            
            # Modern work culture sarcasm
            "work life balance",
            "competitive salary",
            "family friendly workplace",
            "flexible schedule",
            "great company culture",
            "exciting opportunity",
            "growth potential"
        ]
        
        # Sarcasm keywords that often appear in sarcastic contexts
        self.sarcasm_keywords = [
            "just", "exactly", "really", "totally", "absolutely", 
            "definitely", "clearly", "obviously", "sure", "yeah",
            "oh", "wow", "amazing", "perfect", "brilliant", "genius",
            "love", "adore", "enjoy", "thrilled", "excited", "fantastic"
        ]
        
        # Contrasting sentiment patterns (positive words with negative context)
        self.positive_words_negative_context = [
            "great", "amazing", "wonderful", "perfect", "fantastic", 
            "excellent", "brilliant", "awesome", "love", "enjoy",
            "thrilled", "excited", "happy", "pleased", "delighted"
        ]
        
        # Economic hardship indicators
        self.economic_hardship_terms = [
            "poor", "broke", "can't afford", "no money", "struggling", 
            "paycheck to paycheck", "minimum wage", "low pay", "underpaid",
            "cheap", "expensive", "costs too much", "can't buy", "bills",
            "debt", "loans", "rent", "mortgage", "groceries"
        ]
        
        # Work/job related negative contexts
        self.work_negative_terms = [
            "40 hours", "overtime", "overworked", "understaffed", "stress",
            "burnout", "toxic", "boss", "management", "quit", "fired",
            "unemployment", "job search", "interview", "resume", "benefits"
        ]

    def detect_sarcasm(self, text):
        """
        Enhanced main sarcasm detection function with improved accuracy
        Returns: dict with sarcasm_detected (bool), confidence (float), reasons (list)
        """
        if not text or not text.strip():
            return {
                'sarcasm_detected': False,
                'confidence': 0.0,
                'reasons': [],
                'sarcasm_type': None,
                'highlighted_text': text
            }
        
        text_lower = text.lower().strip()
        reasons = []
        confidence_score = 0.0
        sarcasm_type = None
        
        # 1. Enhanced direct sarcastic phrases detection
        phrase_matches = self._check_sarcastic_phrases(text_lower)
        if phrase_matches:
            confidence_score += 0.8  # Increased confidence for explicit phrases
            reasons.extend([f"Sarcastic phrase detected: '{phrase}'" for phrase in phrase_matches])
            sarcasm_type = "explicit_phrase"
        
        # 2. Enhanced positive-negative contradiction pattern
        contradiction_score = self._check_contradiction_pattern(text_lower)
        if contradiction_score > 0:
            confidence_score += contradiction_score * 1.2  # Boost contradiction detection
            reasons.append("Positive words used in negative context (contradiction pattern)")
            if not sarcasm_type:
                sarcasm_type = "contradiction"
        
        # 3. Enhanced economic sarcasm (work/money related)
        economic_score = self._check_economic_sarcasm(text_lower)
        if economic_score > 0:
            confidence_score += economic_score * 1.1  # Slight boost for economic sarcasm
            reasons.append("Economic hardship expressed with positive language")
            if not sarcasm_type:
                sarcasm_type = "economic"
        
        # 4. Enhanced exclamation mark sarcasm
        exclamation_score = self._check_exclamation_sarcasm(text)
        if exclamation_score > 0:
            confidence_score += exclamation_score * 1.3  # Higher boost for exclamation sarcasm
            reasons.append("Positive words with exclamation marks in negative context")
            if not sarcasm_type:
                sarcasm_type = "exclamation"
        
        # 5. NEW: Check for repetitive sarcasm patterns
        repetitive_score = self._check_repetitive_sarcasm(text_lower)
        if repetitive_score > 0:
            confidence_score += repetitive_score
            reasons.append("Repetitive positive language suggesting sarcasm")
            if not sarcasm_type:
                sarcasm_type = "repetitive"
        
        # 6. NEW: Check for context-based sarcasm (time indicators)
        temporal_score = self._check_temporal_sarcasm(text_lower)
        if temporal_score > 0:
            confidence_score += temporal_score
            reasons.append("Timing-based sarcasm detected (again, still, always)")
            if not sarcasm_type:
                sarcasm_type = "temporal"
        
        # 7. NEW: Check for emotional escalation sarcasm
        escalation_score = self._check_emotional_escalation(text_lower)
        if escalation_score > 0:
            confidence_score += escalation_score
            reasons.append("Emotional escalation pattern detected")
            if not sarcasm_type:
                sarcasm_type = "escalation"
        
        # Normalize confidence score
        confidence_score = min(confidence_score, 1.0)
        
        # Enhanced decision threshold with context awareness
        is_sarcastic = confidence_score >= 0.4  # Lowered threshold for better detection
        
        # Apply highlighting if sarcasm detected (no recursion now)
        highlighted_text = text
        if is_sarcastic:
            highlight_result = self.highlight_sarcastic_text(text)
            highlighted_text = highlight_result.get('highlighted_text', text)
        
        return {
            'sarcasm_detected': is_sarcastic,
            'confidence': confidence_score,
            'reasons': reasons,
            'sarcasm_type': sarcasm_type,
            'highlighted_text': highlighted_text
        }
        
        # 4. Sentiment analysis check
        sentiment_score = self._check_sentiment_contradiction(text)
        if sentiment_score > 0:
            confidence_score += sentiment_score
            reasons.append("Sentiment analysis suggests ironic usage")
        
        # 5. Check for specific work-related sarcasm
        work_score = self._check_work_sarcasm(text_lower)
        if work_score > 0:
            confidence_score += work_score
            reasons.append("Work-related sarcasm detected")
            if not sarcasm_type:
                sarcasm_type = "work_related"
        
        # 6. Check for frustrated sarcasm patterns
        frustrated_score = self._check_frustrated_sarcasm(text_lower)
        if frustrated_score > 0:
            confidence_score += frustrated_score
            reasons.append("Frustrated sarcasm detected - positive word followed by negative situation")
            if not sarcasm_type:
                sarcasm_type = "frustrated"
        
        # 7. Check for exclamation-emphasized sarcasm (e.g., "Perfect!" with problems)
        exclamation_score = self._check_exclamation_sarcasm(text)
        if exclamation_score > 0:
            confidence_score += exclamation_score
            reasons.append("Exclamation-emphasized sarcasm detected")
            if not sarcasm_type:
                sarcasm_type = "frustrated"
        
        # 8. Punctuation and capitalization patterns
        punctuation_score = self._check_punctuation_patterns(text)
        if punctuation_score > 0:
            confidence_score += punctuation_score
            reasons.append("Punctuation patterns suggest sarcasm")
        
        # Normalize confidence score
        confidence_score = min(confidence_score, 1.0)
        
        # Determine if sarcasm is detected
        sarcasm_detected = confidence_score >= 0.4
        
        return {
            'sarcasm_detected': sarcasm_detected,
            'confidence': confidence_score,
            'reasons': reasons,
            'sarcasm_type': sarcasm_type,
            'original_text': text
        }

    def _check_sarcastic_phrases(self, text_lower):
        """Check for direct sarcastic phrases"""
        matches = []
        for phrase in self.sarcasm_phrases:
            if phrase in text_lower:
                matches.append(phrase)
        return matches

    def _check_contradiction_pattern(self, text_lower):
        """Check for positive words in negative contexts"""
        score = 0.0
        
        # Check if positive words appear with negative economic terms
        has_positive = any(word in text_lower for word in self.positive_words_negative_context)
        has_negative_context = any(term in text_lower for term in self.economic_hardship_terms)
        
        if has_positive and has_negative_context:
            score += 0.5
        
        # Check for specific contradictory patterns
        if "love" in text_lower and any(term in text_lower for term in ["poor", "broke", "struggling"]):
            score += 0.3
        
        if "great" in text_lower and any(term in text_lower for term in ["can't afford", "no money", "broke"]):
            score += 0.3
            
        return score

    def _check_economic_sarcasm(self, text_lower):
        """Check for economic/financial sarcasm"""
        score = 0.0
        
        # Specific economic sarcasm patterns
        economic_sarcasm_patterns = [
            ("work", "40", "poor"),
            ("work", "hours", "broke"),
            ("job", "pays", "nothing"),
            ("minimum", "wage", "rich"),
            ("paycheck", "paycheck", "wealthy"),
        ]
        
        for pattern in economic_sarcasm_patterns:
            if all(word in text_lower for word in pattern):
                score += 0.4
                break
        
        # The specific case: "work 40 hours just to be poor"
        if "work" in text_lower and "40" in text_lower and "poor" in text_lower:
            score += 0.6
        
        if "work" in text_lower and "hours" in text_lower and any(term in text_lower for term in ["poor", "broke", "struggling"]):
            score += 0.5
            
        return score

    def _check_frustrated_sarcasm(self, text_lower):
        """Check for frustrated sarcasm patterns like 'now, great. im stuck.'"""
        score = 0.0
        
        # Positive words followed by negative situations
        frustrated_patterns = [
            # Stuck patterns
            ("great", "stuck"),
            ("perfect", "stuck"), 
            ("wonderful", "stuck"),
            ("amazing", "stuck"),
            ("fantastic", "stuck"),
            ("lovely", "stuck"),
            ("brilliant", "stuck"),
            ("excellent", "stuck"),
            ("marvelous", "stuck"),
            
            # Problem patterns
            ("great", "problem"),
            ("perfect", "issue"),
            ("wonderful", "trouble"),
            ("amazing", "broken"),
            ("fantastic", "wrong"),
            ("lovely", "error"),
            ("brilliant", "failed"),
            ("excellent", "messed"),
            
            # General frustration
            ("great", "now"),
            ("perfect", "now"),
            ("wonderful", "now"),
            ("amazing", "now"),
        ]
        
        for positive, negative in frustrated_patterns:
            if positive in text_lower and negative in text_lower:
                # Check if they appear close together (within reasonable distance)
                pos_index = text_lower.find(positive)
                neg_index = text_lower.find(negative)
                if abs(pos_index - neg_index) < 50:  # Within 50 characters
                    score += 0.6
                    break
        
        # Specific pattern: "now" + comma/period + positive word + "im/i'm" + negative
        import re
        patterns = [
            r"now[,.]?\s*(great|perfect|wonderful|amazing|fantastic)\s*(im?'?m?)\s*(stuck|broken|lost|confused|screwed)",
            r"(great|perfect|wonderful|amazing|fantastic)[,.]?\s*(im?'?m?)\s*(stuck|broken|lost|confused|screwed)",
            r"(great|perfect|wonderful|amazing|fantastic)[,.]?\s*now\s*(im?'?m?)\s*(stuck|broken|lost|confused|screwed)"
        ]
        
        for pattern in patterns:
            if re.search(pattern, text_lower):
                score += 0.7
                break
        
        # Check for sequence: positive word + problem expression
        problem_words = ["stuck", "broken", "lost", "confused", "screwed", "messed", "failed", "wrong", "error", "trouble", "problem", "issue"]
        positive_words = ["great", "perfect", "wonderful", "amazing", "fantastic", "lovely", "brilliant", "excellent", "marvelous", "awesome"]
        
        # Look for any positive word followed by any problem word within a short distance
        for pos_word in positive_words:
            if pos_word in text_lower:
                pos_index = text_lower.find(pos_word)
                for prob_word in problem_words:
                    if prob_word in text_lower:
                        prob_index = text_lower.find(prob_word)
                        # If problem word comes after positive word within 30 chars
                        if 0 < prob_index - pos_index < 30:
                            score += 0.5
                            break
                if score > 0:
                    break
        
        return score

    def _check_exclamation_sarcasm(self, text):
        """Check for sarcasm using exclamation marks with positive words in negative contexts"""
        import re
        score = 0.0
        
        # Look for positive words followed by exclamation marks
        positive_exclamation_patterns = [
            r'(Perfect|Great|Wonderful|Amazing|Fantastic|Brilliant|Excellent|Awesome)!',
            r'(perfect|great|wonderful|amazing|fantastic|brilliant|excellent|awesome)!'
        ]
        
        for pattern in positive_exclamation_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                match_pos = match.start()
                # Check context around the exclamation
                context_window = 80  # characters before and after
                context_start = max(0, match_pos - context_window)
                context_end = min(len(text), match_pos + context_window)
                context = text[context_start:context_end].lower()
                
                # Negative context indicators
                negative_words = [
                    "crashed", "broken", "stuck", "problem", "issue", "error", "failed", 
                    "trouble", "wrong", "bad", "terrible", "awful", "hate", "annoying",
                    "frustrated", "angry", "upset", "disappointed", "again", "still",
                    "always", "never works", "not working", "stopped", "freeze", "lag"
                ]
                
                # If positive exclamation appears near negative context, it's likely sarcastic
                if any(neg_word in context for neg_word in negative_words):
                    score += 0.6
                    break
        
        return score

    def _check_work_sarcasm(self, text_lower):
        """Check for work-related sarcasm"""
        score = 0.0
        
        # Work + positive word + negative reality
        has_work_terms = any(term in text_lower for term in self.work_negative_terms)
        has_positive = any(word in text_lower for word in self.positive_words_negative_context)
        has_negative = any(term in text_lower for term in self.economic_hardship_terms)
        
        if has_work_terms and has_positive and has_negative:
            score += 0.4
        
        return score

    def _check_sentiment_contradiction(self, text):
        """Use VADER to check for sentiment contradictions"""
        scores = self.vader_analyzer.polarity_scores(text)
        
        # Look for mixed sentiment (high positive but also negative)
        if scores['pos'] > 0.3 and scores['neg'] > 0.2:
            return 0.2
        
        # Very positive sentiment but with negative keywords
        text_lower = text.lower()
        if scores['pos'] > 0.5 and any(term in text_lower for term in self.economic_hardship_terms):
            return 0.3
            
        return 0.0

    def _check_punctuation_patterns(self, text):
        """Check punctuation patterns that suggest sarcasm"""
        score = 0.0
        
        # Multiple exclamation marks
        if text.count('!') >= 2:
            score += 0.1
        
        # All caps words (indicates emphasis/sarcasm)
        caps_words = re.findall(r'\b[A-Z]{2,}\b', text)
        if caps_words:
            score += 0.1
        
        # Quotation marks around positive words (air quotes)
        quoted_positives = re.findall(r'"([^"]*)"', text)
        for quoted in quoted_positives:
            if any(word in quoted.lower() for word in self.positive_words_negative_context):
                score += 0.1
                
        return score

    def get_sarcasm_explanation(self, sarcasm_result):
        """Generate a human-readable explanation of detected sarcasm"""
        if not sarcasm_result['sarcasm_detected']:
            return "No sarcasm detected. The message appears to be literal."
        
        explanation = f"🎭 **Sarcasm detected!** (Confidence: {sarcasm_result['confidence']:.1%})\n\n"
        
        if sarcasm_result['sarcasm_type'] == 'economic':
            explanation += "This appears to be **economic sarcasm** - the speaker is expressing frustration about financial struggles using positive language ironically.\n\n"
        elif sarcasm_result['sarcasm_type'] == 'work_related':
            explanation += "This appears to be **work-related sarcasm** - expressing dissatisfaction with job conditions using ironic positive language.\n\n"
        elif sarcasm_result['sarcasm_type'] == 'frustrated':
            explanation += "This appears to be **frustrated sarcasm** - the speaker is using positive words sarcastically while describing a negative situation or being stuck.\n\n"
        elif sarcasm_result['sarcasm_type'] == 'contradiction':
            explanation += "This uses **contradictory language** - positive words in a negative context to express the opposite meaning.\n\n"
        elif sarcasm_result['sarcasm_type'] == 'explicit_phrase':
            explanation += "This contains **explicit sarcastic phrases** commonly used to express irony.\n\n"
        else:
            explanation += "This contains **sarcastic language patterns** that suggest ironic meaning.\n\n"
        
        explanation += "**Why this is sarcasm:**\n"
        for reason in sarcasm_result['reasons']:
            explanation += f"• {reason}\n"
        
        explanation += "\n**What they really mean:** The speaker is expressing the opposite of what they're literally saying - they're frustrated, not actually happy about their situation."
        
        return explanation
    
    def _check_repetitive_sarcasm(self, text_lower):
        """Detect repetitive positive language that suggests sarcasm"""
        score = 0.0
        positive_words = ["great", "perfect", "wonderful", "amazing", "fantastic", "excellent", "brilliant", "awesome"]
        
        # Count how many positive words appear
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        # If multiple positive words appear, likely sarcastic
        if positive_count >= 3:
            score += 0.4
        elif positive_count >= 2:
            score += 0.3
        
        # Check for repeated words (e.g., "great great" or "perfect, just perfect")
        import re
        for word in positive_words:
            pattern = r'\b' + word + r'\b.*\b' + word + r'\b'
            if re.search(pattern, text_lower):
                score += 0.3
                break
        
        return score
    
    def _check_temporal_sarcasm(self, text_lower):
        """Detect sarcasm based on temporal indicators"""
        score = 0.0
        temporal_indicators = ["again", "still", "always", "every time", "once again", "yet again", "as usual"]
        positive_words = ["great", "perfect", "wonderful", "amazing", "fantastic", "excellent", "brilliant", "awesome", "love"]
        
        has_temporal = any(indicator in text_lower for indicator in temporal_indicators)
        has_positive = any(word in text_lower for word in positive_words)
        
        if has_temporal and has_positive:
            score += 0.5  # Strong indicator of sarcasm
        
        return score
    
    def _check_emotional_escalation(self, text_lower):
        """Detect emotional escalation patterns that suggest sarcasm"""
        score = 0.0
        
        # Check for intensification words with positive words
        intensifiers = ["so", "very", "really", "extremely", "absolutely", "totally", "completely"]
        positive_words = ["great", "perfect", "wonderful", "amazing", "fantastic", "excellent", "brilliant", "awesome", "happy", "thrilled", "excited"]
        
        for intensifier in intensifiers:
            for positive in positive_words:
                if f"{intensifier} {positive}" in text_lower:
                    # Check if there's negative context nearby
                    negative_context = ["problem", "issue", "broken", "crashed", "failed", "error", "stuck", "trouble", "wrong", "bad"]
                    if any(neg in text_lower for neg in negative_context):
                        score += 0.4
                        break
        
        return score

    def highlight_sarcastic_text(self, text):
        """
        Use LLM to identify and highlight sarcastic segments in the text
        Returns text with sarcastic parts marked for red highlighting
        """
        if not text or not text.strip():
            return {
                'highlighted_text': text,
                'sarcastic_segments': [],
                'method': 'none'
            }
        
        # Skip the initial detection check to avoid recursion
        # Instead, apply rule-based highlighting directly
        
        # Try LLM-powered highlighting first
        if self.client:
            return self._llm_highlight_sarcasm(text)
        else:
            return self._rule_based_highlight_sarcasm(text)
    
    def _llm_highlight_sarcasm(self, text):
        """Use LLM to identify specific sarcastic segments"""
        try:
            prompt = f"""
You are an expert at detecting sarcasm in text. Your task is to identify the EXACT words or phrases that are being used sarcastically in the given text.

TEXT TO ANALYZE: "{text}"

Instructions:
1. Identify any words, phrases, or sentences that are being used sarcastically (meaning the opposite of what they literally say)
2. Return ONLY the sarcastic segments - not explanations or context
3. If multiple sarcastic segments exist, list each one separately
4. Be precise - only highlight the specific sarcastic words/phrases, not surrounding text
5. If no sarcasm is found, return an empty list

Examples:
- Text: "Oh great, now I'm stuck" → Sarcastic segments: ["great"]
- Text: "I work 40 hours just to be poor" → Sarcastic segments: ["just to be poor"] (the irony is in this phrase)
- Text: "Perfect! My computer crashed again" → Sarcastic segments: ["Perfect"]
- Text: "I love working overtime for no extra pay" → Sarcastic segments: ["love"]

Format your response as JSON:
{{
    "sarcastic_segments": ["segment1", "segment2", ...],
    "confidence": 0.8
}}

Focus on identifying the specific words/phrases being used ironically or sarcastically.
"""

            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert sarcasm detection system. Return only JSON responses with identified sarcastic text segments."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.2
            )
            
            result = response.choices[0].message.content
            
            # Parse JSON response
            if "{" in result and "}" in result:
                json_start = result.find("{")
                json_end = result.rfind("}") + 1
                json_str = result[json_start:json_end]
                parsed = json.loads(json_str)
                
                sarcastic_segments = parsed.get("sarcastic_segments", [])
                confidence = parsed.get("confidence", 0.8)
                
                # Highlight the text
                highlighted_text = self._apply_highlighting(text, sarcastic_segments)
                
                return {
                    'highlighted_text': highlighted_text,
                    'sarcastic_segments': sarcastic_segments,
                    'confidence': confidence,
                    'method': 'llm_powered'
                }
            else:
                # Fallback to rule-based if LLM response is malformed
                return self._rule_based_highlight_sarcasm(text)
                
        except Exception as e:
            print(f"Error in LLM sarcasm highlighting: {e}")
            return self._rule_based_highlight_sarcasm(text)
    
    def _rule_based_highlight_sarcasm(self, text):
        """Fallback rule-based sarcasm highlighting"""
        sarcastic_segments = []
        text_lower = text.lower()
        
        # Check for explicit sarcastic phrases - improved detection
        for phrase in self.sarcasm_phrases:
            phrase_lower = phrase.lower()
            
            # Create flexible pattern that handles punctuation
            import re
            # Replace spaces with flexible spacing that allows for punctuation
            flexible_phrase = re.escape(phrase_lower).replace(r'\ ', r'[\s,]*')
            pattern = r'\b' + flexible_phrase + r'\b'
            
            # Find all matches using the flexible pattern
            matches = re.finditer(pattern, text_lower)
            
            for match in matches:
                start_pos = match.start()
                end_pos = match.end()
                
                # Extract the actual phrase from the original text (preserving case)
                original_phrase = text[start_pos:end_pos]
                
                # Clean up any extra punctuation from the captured phrase
                cleaned_phrase = re.sub(r'^[^\w]+|[^\w]+$', '', original_phrase)
                
                if cleaned_phrase and cleaned_phrase not in sarcastic_segments:
                    sarcastic_segments.append(cleaned_phrase)
        
        # Check for positive words in negative contexts with enhanced patterns
        positive_negative_patterns = [
            # Computer/tech problems
            ("perfect", ["computer", "crashed", "broken", "error", "failed", "freeze"]),
            ("great", ["computer", "crashed", "broken", "error", "failed", "freeze"]),
            ("wonderful", ["crashed", "broken", "error", "failed"]),
            ("amazing", ["crashed", "broken", "error", "failed"]),
            ("fantastic", ["crashed", "broken", "error", "failed"]),
            
            # Work sarcasm
            ("love", ["working", "overtime", "unpaid", "extra hours", "late", "free"]),
            ("enjoy", ["working", "overtime", "unpaid", "extra hours", "late", "free"]),
            ("adore", ["working", "overtime", "unpaid", "extra hours"]),
            
            # General frustration
            ("perfect", ["stuck", "broken", "problem", "issue", "trouble"]),
            ("great", ["stuck", "broken", "problem", "issue", "trouble"]),
            ("wonderful", ["stuck", "broken", "problem", "issue", "trouble"]),
            ("amazing", ["stuck", "broken", "problem", "issue", "trouble"]),
            ("fantastic", ["stuck", "broken", "problem", "issue", "trouble"]),
            ("brilliant", ["stuck", "broken", "problem", "issue", "trouble"]),
            ("excellent", ["stuck", "broken", "problem", "issue", "trouble"]),
            
            # Economic sarcasm
            ("love", ["poor", "broke", "expensive", "bills", "debt"]),
            ("enjoy", ["poor", "broke", "expensive", "bills", "debt"]),
            ("great", ["poor", "broke", "expensive", "bills", "debt"]),
            ("perfect", ["poor", "broke", "expensive", "bills", "debt"]),
        ]
        
        for pos_word, neg_contexts in positive_negative_patterns:
            if pos_word in text_lower:
                pos_index = text_lower.find(pos_word)
                
                # Check if any negative context words appear nearby
                for neg_word in neg_contexts:
                    if neg_word in text_lower:
                        neg_index = text_lower.find(neg_word)
                        # Check if they're within reasonable distance (100 characters)
                        if abs(pos_index - neg_index) < 100:
                            # Extract the actual positive word preserving case
                            actual_word = self._extract_word_from_text(text, pos_word, pos_index)
                            if actual_word and actual_word not in sarcastic_segments:
                                sarcastic_segments.append(actual_word)
                            break
        
        # Check for exclamation mark emphasis on positive words (often sarcastic)
        import re
        exclamation_patterns = [
            r'(Perfect|Great|Wonderful|Amazing|Fantastic|Brilliant|Excellent|Love|Awesome)!',
            r'(perfect|great|wonderful|amazing|fantastic|brilliant|excellent|love|awesome)!'
        ]
        
        for pattern in exclamation_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                word_with_exclamation = match.group(1)
                # Check if this appears in a negative context
                match_pos = match.start()
                context_before = text[max(0, match_pos-50):match_pos]
                context_after = text[match_pos:min(len(text), match_pos+50)]
                
                negative_indicators = ["crashed", "broken", "stuck", "problem", "issue", "error", "failed", "trouble"]
                if any(indicator in context_before.lower() or indicator in context_after.lower() for indicator in negative_indicators):
                    if word_with_exclamation not in sarcastic_segments:
                        sarcastic_segments.append(word_with_exclamation)
        
        # Apply highlighting
        highlighted_text = self._apply_highlighting(text, sarcastic_segments)
        
        return {
            'highlighted_text': highlighted_text,
            'sarcastic_segments': sarcastic_segments,
            'confidence': 0.7 if sarcastic_segments else 0.0,
            'method': 'rule_based'
        }
    
    def _extract_word_from_text(self, text, word_lower, approximate_index):
        """Extract the actual word from text preserving original case"""
        # Look for word boundaries around the approximate index
        import re
        pattern = re.compile(re.escape(word_lower), re.IGNORECASE)
        match = pattern.search(text, approximate_index - 5, approximate_index + len(word_lower) + 5)
        if match:
            return match.group(0)
        return None
    
    def _apply_highlighting(self, text, sarcastic_segments):
        """Apply prominent red highlighting to sarcastic segments"""
        if not sarcastic_segments:
            return text
        
        highlighted_text = text
        
        # Sort segments by length (longest first) to avoid partial replacements
        sorted_segments = sorted(set(sarcastic_segments), key=len, reverse=True)
        
        for segment in sorted_segments:
            # Use case-insensitive search to find the segment
            import re
            # Create a more flexible pattern that handles word boundaries
            pattern = re.compile(r'\b' + re.escape(segment) + r'\b', re.IGNORECASE)
            
            def replace_func(match):
                # Enhanced red highlighting with multiple visual cues
                return f'<span style="color: #DC3545; font-weight: bold; background-color: rgba(220, 53, 69, 0.1); padding: 2px 4px; border-radius: 3px; text-decoration: underline; text-decoration-style: wavy;">{match.group(0)}</span>'
            
            highlighted_text = pattern.sub(replace_func, highlighted_text)
        
        return highlighted_text

    def get_sarcasm_explanation(self, sarcasm_result):
        """Generate a human-readable explanation of detected sarcasm with reactions"""
        if not sarcasm_result['sarcasm_detected']:
            return "No sarcasm detected. The message appears to be literal."
        
        confidence_level = sarcasm_result['confidence']
        
        # Add reaction based on confidence and type
        if confidence_level >= 0.8:
            explanation = f"🎭 **Strong sarcasm detected!** (Confidence: {confidence_level:.1%}) 🔥\n\n"
        elif confidence_level >= 0.6:
            explanation = f"🎭 **Sarcasm detected!** (Confidence: {confidence_level:.1%}) 👀\n\n"
        else:
            explanation = f"🎭 **Possible sarcasm detected** (Confidence: {confidence_level:.1%}) 🤔\n\n"
        
        # Add specific reactions based on sarcasm type
        if sarcasm_result['sarcasm_type'] == 'economic':
            explanation += "💸 **Economic sarcasm detected!** - This person is expressing financial frustration using ironic positive language. They're probably struggling with money but saying the opposite of what they mean.\n\n"
        elif sarcasm_result['sarcasm_type'] == 'work_related':
            explanation += "💼 **Work-related sarcasm detected!** - Someone's expressing job dissatisfaction through ironic language. They're likely frustrated with their work situation.\n\n"
        elif sarcasm_result['sarcasm_type'] == 'frustrated':
            explanation += "😤 **Frustrated sarcasm detected!** - This person is using positive words sarcastically while dealing with a negative situation. They're clearly annoyed!\n\n"
        elif sarcasm_result['sarcasm_type'] == 'contradiction':
            explanation += "🔄 **Contradictory sarcasm detected!** - The speaker is using positive words in a negative context to express the opposite meaning.\n\n"
        elif sarcasm_result['sarcasm_type'] == 'explicit_phrase':
            explanation += "📢 **Explicit sarcastic phrases detected!** - This contains commonly used sarcastic expressions.\n\n"
        else:
            explanation += "🗣️ **Sarcastic language patterns detected!** - The text contains ironic meaning patterns.\n\n"
        
        explanation += "**🔍 Why this is sarcasm:**\n"
        for reason in sarcasm_result['reasons']:
            explanation += f"• ⚡ {reason}\n"
        
        # Add contextual reaction
        if 'work' in str(sarcasm_result['reasons']).lower():
            explanation += "\n💡 **Context clue:** This appears to be work-related frustration expressed sarcastically."
        elif 'poor' in str(sarcasm_result['reasons']).lower() or 'money' in str(sarcasm_result['reasons']).lower():
            explanation += "\n💡 **Context clue:** This seems to be about financial struggles expressed ironically."
        elif 'stuck' in str(sarcasm_result['reasons']).lower() or 'problem' in str(sarcasm_result['reasons']).lower():
            explanation += "\n💡 **Context clue:** This appears to be frustration with a technical or personal problem."
        
        explanation += "\n\n🎯 **What they really mean:** The speaker is expressing the opposite of what they're literally saying - they're frustrated, disappointed, or upset, not actually happy about their situation!"
        
        return explanation

# Create a global instance
sarcasm_detector = SarcasmDetector()

def detect_sarcasm(text):
    """Convenience function for sarcasm detection"""
    return sarcasm_detector.detect_sarcasm(text)

def get_sarcasm_explanation(text):
    """Get full sarcasm analysis with explanation"""
    result = sarcasm_detector.detect_sarcasm(text)
    explanation = sarcasm_detector.get_sarcasm_explanation(result)
    
    return {
        'analysis': result,
        'explanation': explanation
    }

def highlight_sarcastic_text(text):
    """Convenience function for sarcasm highlighting"""
    return sarcasm_detector.highlight_sarcastic_text(text)

def get_comprehensive_sarcasm_analysis(text):
    """Get complete sarcasm analysis including detection, explanation, and highlighting"""
    detection_result = sarcasm_detector.detect_sarcasm(text)
    highlighting_result = sarcasm_detector.highlight_sarcastic_text(text)
    explanation = sarcasm_detector.get_sarcasm_explanation(detection_result)
    
    return {
        'sarcasm_detected': detection_result['sarcasm_detected'],
        'confidence': detection_result['confidence'],
        'sarcasm_type': detection_result['sarcasm_type'],
        'reasons': detection_result['reasons'],
        'highlighted_text': highlighting_result['highlighted_text'],
        'sarcastic_segments': highlighting_result['sarcastic_segments'],
        'highlighting_method': highlighting_result['method'],
        'explanation': explanation,
        'original_text': text
    }
