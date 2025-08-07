import os
from typing import Optional, Dict, Any
import json

class TextSimplifier:
    def __init__(self):
        # Initialize OpenAI client
        # Note: You'll need to set OPENAI_API_KEY environment variable
        self.client = None
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if self.api_key:
            try:
                import openai
                openai.api_key = self.api_key
                self.client = openai
                print("✅ OpenAI client initialized successfully")
            except ImportError:
                print("⚠️ OpenAI package not installed. Using fallback method.")
                self.client = None
        else:
            print("⚠️ OPENAI_API_KEY not found. Using rule-based simplification.")
            
    def simplify_text(self, original_text: str) -> Dict[str, Any]:
        """
        Simplify text by replacing idioms, slang, and cultural references with plain English
        
        Args:
            original_text: The text to simplify
            
        Returns:
            Dict with simplified text, explanations, and word substitutions
        """
        if not self.client or not original_text.strip():
            return self._fallback_simplification(original_text)
            
        try:
            # Create simplified prompt
            prompt = self._create_simplification_prompt(original_text)
            
            # Call OpenAI API
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful language learning assistant that specializes in making complex text easier to understand for English learners."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            return self._parse_llm_response(result, original_text)
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._fallback_simplification(original_text)
    
    def _create_simplification_prompt(self, text: str) -> str:
        """Create a prompt for the LLM to simplify text"""
        
        return f"""
You are helping English language learners understand text that contains idioms, slang, cultural references, and complex expressions.

ORIGINAL TEXT: "{text}"

Your task is to:
1. IDENTIFY any idioms, slang, cultural references, or figurative language
2. REPLACE them with clear, literal explanations that anyone can understand
3. EXPLAIN what these expressions really mean in plain English
4. MAINTAIN the original meaning but make it accessible

SPECIFIC FOCUS:
- Replace idioms with their literal meanings (e.g., "break a leg" → "good luck")
- Explain cultural references (e.g., "throwing in the towel" → "giving up, like in boxing")
- Convert slang to standard English (e.g., "that's fire" → "that's really good")
- Clarify sarcasm or implied meanings
- Explain metaphors literally

INSTRUCTIONS:
- Use simple, clear language that anyone can understand
- If the text contains sarcasm, explain what the person really means
- If there are cultural references (sports, history, pop culture), explain them briefly  
- If there are idioms or expressions, replace them with their actual meaning
- If there are slang words, provide the standard English equivalent
- Keep the main message intact but make it universally understandable

Please format your response as JSON with these fields:
{{
    "simplified_text": "The completely rewritten version with all idioms, slang, and cultural references replaced with clear explanations",
    "key_explanations": ["explanation of each idiom/slang/reference you found"],
    "cultural_notes": ["explanation of cultural context if needed"],
    "word_substitutions": {{"slang_word": "standard_english_word", "idiom": "literal_meaning"}}
}}
"""

    def _parse_llm_response(self, response: str, original_text: str) -> Dict[str, Any]:
        """Parse the LLM response into structured data"""
        try:
            # Try to parse as JSON
            if "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
                parsed = json.loads(json_str)
                
                return {
                    "success": True,
                    "original_text": original_text,
                    "simplified_text": parsed.get("simplified_text", original_text),
                    "key_explanations": parsed.get("key_explanations", []),
                    "cultural_notes": parsed.get("cultural_notes", []),
                    "word_substitutions": parsed.get("word_substitutions", {}),
                    "method": "llm_powered"
                }
            else:
                # If not JSON, treat the whole response as simplified text
                return {
                    "success": True,
                    "original_text": original_text,
                    "simplified_text": response.strip(),
                    "key_explanations": [],
                    "cultural_notes": [],
                    "word_substitutions": {},
                    "method": "llm_powered"
                }
                
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return self._fallback_simplification(original_text)
    
    def _fallback_simplification(self, text: str) -> Dict[str, Any]:
        """Fallback method when LLM is not available - focuses on idioms, slang, and cultural references"""
        
        simplified = text
        explanations = []
        substitutions = {}
        cultural_notes = []
        
        # Common idioms and their literal meanings
        idiom_replacements = {
            "break a leg": "good luck",
            "piece of cake": "very easy",
            "spill the beans": "reveal a secret",
            "hit the nail on the head": "be exactly right",
            "bite the bullet": "face a difficult situation",
            "break the ice": "start a conversation",
            "cost an arm and a leg": "be very expensive",
            "costs an arm and a leg": "is very expensive",
            "once in a blue moon": "very rarely",
            "when pigs fly": "never",
            "raining cats and dogs": "raining heavily",
            "the ball is in your court": "it's your decision",
            "kill two birds with one stone": "accomplish two things at once",
            "let the cat out of the bag": "reveal a secret",
            "a blessing in disguise": "something good that seemed bad at first",
            "call it a day": "stop working",
            "cutting corners": "doing something poorly to save time or money",
            "easy as pie": "very easy",
            "hit the books": "study hard",
            "it's not rocket science": "it's not difficult",
            "throw in the towel": "give up",
            "under the weather": "feeling sick",
            "you can't judge a book by its cover": "don't judge based on appearance",
            "threw me under the bus": "betrayed me or blamed me unfairly",
            "throw under the bus": "betray or blame unfairly",
            "hit the fan": "things went very wrong",
            "when it hit the fan": "when things went very wrong",
            "break the bank": "cost too much money",
            "on cloud nine": "very happy",
            "over the moon": "extremely happy",
            "piece of work": "difficult person",
            "pain in the neck": "annoying person or thing",
            "back to square one": "start over from the beginning",
            "barking up the wrong tree": "making a mistake",
            "don't count your chickens before they hatch": "don't assume success too early",
            "every cloud has a silver lining": "there's something good in every bad situation",
            "it's a small world": "people are connected in unexpected ways",
            "the early bird catches the worm": "people who act quickly get the best opportunities"
        }
        
        # Common slang and modern expressions
        slang_replacements = {
            "that's fire": "that's really good",
            "that slaps": "that's excellent", 
            "no cap": "no lie, for real",
            "bet": "okay, sure",
            "salty": "angry or bitter",
            "throw shade": "insult someone",
            "ghost": "ignore someone",
            "flex": "show off",
            "vibe": "feeling or atmosphere",
            "lowkey": "somewhat, secretly",
            "highkey": "obviously, definitely",
            "periodt": "end of discussion",
            "say less": "I understand completely",
            "it hits different": "it feels special or unique",
            "that's sus": "that's suspicious",
            "living rent free": "constantly thinking about something",
            "main character energy": "confident, self-assured behavior",
            "touch grass": "go outside and experience real life",
            "sending me": "making me laugh a lot",
            "this ain't it": "this is wrong or bad",
            "and I oop": "oops, awkward moment",
            "fire": "really good",
            "lit": "exciting or excellent",
            "slaps": "is excellent",
            "bussin": "really good",
            "cringe": "embarrassing or awkward",
            "toxic": "harmful or negative",
            "wholesome": "pure and good",
            "savage": "brutally honest or cool",
            "mood": "relatable feeling",
            "stan": "be a big fan of",
            "tea": "gossip or truth",
            "shade": "insult or criticism",
            "woke": "aware of social issues",
            "basic": "unoriginal or mainstream",
            "extra": "over the top",
            "fam": "close friends",
            "squad": "group of friends",
            "snatched": "looks perfect",
            "iconic": "memorable and impressive",
            "queen": "confident woman",
            "king": "confident man"
        }
        
        # Cultural references that need explanation
        cultural_references = {
            "throwing in the towel": ("giving up", "In boxing, throwing a towel means the fight is over"),
            "jump the shark": ("become ridiculous", "From a TV show where a character literally jumped over a shark"),
            "drinking the kool-aid": ("believing something without question", "Reference to a tragic cult incident"),
            "fifteen minutes of fame": ("brief period of being famous", "From artist Andy Warhol's prediction"),
            "gaslighting": ("manipulating someone to doubt their reality", "From a 1944 movie called 'Gaslight'"),
            "karen": ("entitled, demanding person", "Internet slang for a specific type of behavior"),
            "simp": ("someone who does too much for someone they like", "Internet slang meaning 'simpleton'"),
            "boomer": ("older person, often out of touch", "Refers to Baby Boomer generation")
        }
        
        # Replace idioms first (longer phrases before shorter ones)
        idiom_items = sorted(idiom_replacements.items(), key=lambda x: len(x[0]), reverse=True)
        for idiom, meaning in idiom_items:
            if idiom.lower() in simplified.lower():
                # Use case-insensitive replacement with word boundaries for single words
                import re
                if ' ' in idiom:
                    # For phrases, use exact match
                    pattern = re.escape(idiom)
                else:
                    # For single words, use word boundaries
                    pattern = r'\b' + re.escape(idiom) + r'\b'
                simplified = re.sub(pattern, meaning, simplified, flags=re.IGNORECASE)
                substitutions[idiom] = meaning
                explanations.append(f"'{idiom}' is an idiom that means '{meaning}'")
        
        # Replace slang (longer phrases before shorter ones) 
        slang_items = sorted(slang_replacements.items(), key=lambda x: len(x[0]), reverse=True)
        for slang, meaning in slang_items:
            if slang.lower() in simplified.lower():
                # Use case-insensitive replacement with word boundaries
                import re
                if ' ' in slang:
                    # For phrases, use exact match
                    pattern = re.escape(slang)
                else:
                    # For single words, use word boundaries
                    pattern = r'\b' + re.escape(slang) + r'\b'
                simplified = re.sub(pattern, meaning, simplified, flags=re.IGNORECASE)
                substitutions[slang] = meaning
                explanations.append(f"'{slang}' is modern slang meaning '{meaning}'")
        
        # Handle cultural references
        cultural_items = sorted(cultural_references.items(), key=lambda x: len(x[0]), reverse=True)
        for ref, (meaning, context) in cultural_items:
            if ref.lower() in simplified.lower():
                import re
                simplified = re.sub(re.escape(ref), meaning, simplified, flags=re.IGNORECASE)
                substitutions[ref] = meaning
                cultural_notes.append(f"'{ref}': {context}")
                explanations.append(f"'{ref}' means '{meaning}'")
        
        # Replace complex words with simpler ones
        word_replacements = {
            "utilize": "use",
            "facilitate": "help",
            "commence": "start",
            "terminate": "end",
            "subsequent": "next",
            "prior": "before",
            "consequently": "so",
            "nevertheless": "but",
            "furthermore": "also",
            "regarding": "about",
            "acquire": "get",
            "endeavor": "try",
            "substantial": "large",
            "insufficient": "not enough",
            "approximately": "about",
            "devastating": "very bad",
            "magnificent": "very good",
            "extraordinary": "amazing",
            "comprehend": "understand",
            "demonstrate": "show"
        }
        
        for difficult, simple in word_replacements.items():
            if difficult in simplified.lower():
                simplified = simplified.replace(difficult, simple)
                simplified = simplified.replace(difficult.capitalize(), simple.capitalize())
                substitutions[difficult] = simple
        
        # Detect sarcasm patterns and explain them
        sarcasm_indicators = [
            "just great", "perfect", "wonderful", "exactly what I needed",
            "just what I wanted", "oh wonderful", "that's just perfect"
        ]
        
        for indicator in sarcasm_indicators:
            if indicator.lower() in text.lower():
                explanations.append(f"'{indicator}' might be sarcasm - the person probably means the opposite")
        
        # Check for complex sentences
        if len(text.split()) > 20:
            explanations.append("This is a long sentence - try breaking it into smaller parts")
            
        if ";" in text:
            explanations.append("Semicolons (;) are used to connect related ideas")
            
        # Estimate reading difficulty (simplified)
        word_count = len(text.split())
        if word_count < 15:
            difficulty = "easy"
        elif word_count < 30:
            difficulty = "medium"  
        else:
            difficulty = "hard"
            
        return {
            "success": True,
            "original_text": text,
            "simplified_text": simplified,
            "key_explanations": explanations,
            "cultural_notes": cultural_notes,
            "word_substitutions": substitutions,
            "method": "rule_based_fallback"
        }

    def get_reading_level_info(self, text: str) -> Dict[str, Any]:
        """Analyze the reading level of text"""
        words = text.split()
        sentences = len([s for s in text.split('.') if s.strip()])
        avg_words_per_sentence = len(words) / max(sentences, 1)
        
        # Simple readability estimation
        if avg_words_per_sentence < 10:
            level = "Beginner (A1-A2)"
            color = "#28a745"  # Green
        elif avg_words_per_sentence < 15:
            level = "Intermediate (B1-B2)"  
            color = "#ffc107"  # Yellow
        else:
            level = "Advanced (C1-C2)"
            color = "#dc3545"  # Red
            
        return {
            "level": level,
            "color": color,
            "words": len(words),
            "sentences": sentences,
            "avg_words_per_sentence": round(avg_words_per_sentence, 1)
        }

# Global instance
text_simplifier = TextSimplifier()

def simplify_text_for_learners(text: str) -> Dict[str, Any]:
    """Convenience function for text simplification"""
    return text_simplifier.simplify_text(text)

def get_text_readability(text: str) -> Dict[str, Any]:
    """Get readability analysis of text"""
    return text_simplifier.get_reading_level_info(text)
