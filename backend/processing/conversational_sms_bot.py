import random
import json
import os
import pandas as pd
from datetime import datetime

class ConversationalSMSBot:
    def __init__(self):
        """Initialize the SMS-style conversational bot with cultural slang and idioms"""
        
        # Cultural phrases and modern slang for the bot to use
        self.bot_vocabulary = {
            'greetings': [
                "hey there! 👋", "what's good?", "sup bestie!", "hiya!", 
                "yo yo yo!", "hey fam!", "wassup?", "heyyy! ✨", 
                "morning sunshine! ☀️", "hey gorgeous!"
            ],
            'acknowledgments': [
                "I hear you!", "totally get that", "no cap that's real", "fr fr", 
                "periodt!", "that hits different", "you said what you said", 
                "speak your truth!", "say it louder for the people in the back!", 
                "this! 👆", "big mood", "felt that in my soul"
            ],
            'encouragement': [
                "you got this bestie! 💪", "slay queen/king!", "periodt, you're amazing", 
                "that's the energy we need!", "living your best life!", "stay iconic! ✨", 
                "keep serving looks!", "you're doing great sweetie", "main character energy!", 
                "that's so slay of you", "pure excellence!"
            ],
            'excitement': [
                "OMG YESSS! 🔥", "I'm so here for this!", "this is IT!", "OBSESSED!", 
                "no literally OBSESSED", "this slaps!", "chef's kiss 👌", "it's giving main character", 
                "the vibes are immaculate", "absolutely iconic", "this ate and left no crumbs"
            ],
            'agreement': [
                "100% this!", "absolutely!", "facts only!", "no lies detected", 
                "you spilled tea ☕", "period point blank", "say it louder!", 
                "all tea no shade", "you understood the assignment", "this is the way"
            ],
            'sympathy': [
                "oof that's rough buddy", "sending you good vibes 💕", "that's not it chief", 
                "big yikes", "we've all been there hon", "that's a whole mood", 
                "I'm manifesting better days for you ✨", "this too shall pass bestie"
            ],
            'modern_transitions': [
                "anyway...", "but like...", "so basically...", "okay but...", 
                "real talk though...", "on a serious note...", "shifting gears...", 
                "plot twist...", "speaking of which...", "that reminds me..."
            ],
            'cultural_expressions': [
                "it's giving...", "the way I...", "not me...", "the fact that...", 
                "I can't even...", "I'm deceased 💀", "this sends me", "I'm weak", 
                "I'm screaming", "why am I like this", "this is so me"
            ]
        }
        
        # Idioms and their explanations
        self.idioms_database = {
            "spill the tea": "Share the gossip or tell the truth about something",
            "that slaps": "That's really good or impressive",
            "no cap": "No lie, I'm being serious",
            "periodt": "End of discussion, that's final",
            "it's giving...": "It has the vibe of... or it reminds me of...",
            "slay": "Do something really well or look amazing",
            "bet": "Okay, sounds good, or I agree",
            "say less": "I understand completely, you don't need to explain more",
            "vibe check": "Checking how someone is feeling",
            "main character energy": "Acting confident and putting yourself first",
            "rent free": "Something that occupies your thoughts constantly",
            "hits different": "This experience is uniquely good or special",
            "understood the assignment": "Did exactly what was expected, perfectly",
            "chef's kiss": "Perfect, exactly right",
            "left no crumbs": "Did something so well there's nothing left to criticize"
        }
        
        # Conversation starters with slang
        self.conversation_starters = [
            "Girl, you HAVE to try this new coffee shop - it's absolutely sending me! ☕✨",
            "Not me procrastinating my homework again... why am I like this? 😅",
            "The weather is giving main character vibes today, I'm obsessed! 🌤️",
            "Just saw the most chaotic thing at the store, I'm literally deceased 💀",
            "Your fit is serving looks today bestie! Where did you get that? 👗",
            "Real talk, I need to stop buying things I don't need... but like, it was on sale! 🛍️",
            "The way this song has been living rent free in my head all week... 🎵",
            "Okay but can we talk about how good this pizza hits? Chef's kiss! 🍕",
            "Not the wifi acting up when I have a presentation due... technology said no ❌",
            "This movie literally understood the assignment, no cap! 🎬"
        ]
        
        # Load slang from datasets if available
        self._load_slang_databases()
        
        # Conversation state
        self.conversation_history = []
        self.topics_discussed = set()
        
    def _load_slang_databases(self):
        """Load slang from existing datasets"""
        try:
            datasets_path = os.path.join(os.path.dirname(__file__), '..', 'Datasets')
            
            # Load Gen Z slang
            genz_path = os.path.join(datasets_path, 'genz_slang.csv')
            if os.path.exists(genz_path):
                genz_df = pd.read_csv(genz_path)
                if 'term' in genz_df.columns and 'meaning' in genz_df.columns:
                    for _, row in genz_df.head(50).iterrows():
                        self.idioms_database[str(row['term']).lower()] = str(row['meaning'])
            
            # Load general slang
            slang_path = os.path.join(datasets_path, 'slang.csv')
            if os.path.exists(slang_path):
                slang_df = pd.read_csv(slang_path)
                if 'slang' in slang_df.columns and 'meaning' in slang_df.columns:
                    for _, row in slang_df.head(50).iterrows():
                        self.idioms_database[str(row['slang']).lower()] = str(row['meaning'])
                        
        except Exception as e:
            print(f"Note: Could not load slang datasets: {e}")
    
    def analyze_user_message(self, message):
        """Analyze user message and determine response strategy"""
        message_lower = message.lower()
        
        analysis = {
            'contains_slang': [],
            'contains_idioms': [],
            'message_type': 'general',
            'emotional_tone': 'neutral',
            'requires_explanation': False,
            'main_topic': None
        }
        
        # Determine main topic first (more specific matching)
        if any(word in message_lower for word in ['weather', 'sunny', 'rain', 'raining', 'hot', 'cold', 'nice day', 'cloudy']):
            analysis['main_topic'] = 'weather'
        elif any(word in message_lower for word in ['food', 'eat', 'eating', 'hungry', 'lunch', 'dinner', 'pizza', 'coffee', 'restaurant']):
            analysis['main_topic'] = 'food'
        elif any(word in message_lower for word in ['music', 'song', 'artist', 'album', 'listening', 'playlist']):
            analysis['main_topic'] = 'music'
        elif any(word in message_lower for word in ['netflix', 'show', 'movie', 'watch', 'watching', 'series']):
            analysis['main_topic'] = 'entertainment'
        elif any(word in message_lower for word in ['work', 'school', 'class', 'job', 'office', 'working']):
            analysis['main_topic'] = 'work_school'
        elif any(word in message_lower for word in ['tired', 'stressed', 'exhausted', 'sleepy', 'stress']):
            analysis['main_topic'] = 'tired_stressed'
        elif any(word in message_lower for word in ['exam', 'test', 'studying', 'homework', 'assignment']):
            analysis['main_topic'] = 'academic'
        elif any(word in message_lower for word in ['weekend', 'plans', 'free time', 'vacation']):
            analysis['main_topic'] = 'plans'
        
        # Check for slang and idioms
        for term, meaning in self.idioms_database.items():
            if term in message_lower:
                analysis['contains_slang'].append({'term': term, 'meaning': meaning})
                analysis['requires_explanation'] = True
        
        # Determine message type
        question_words = ['what', 'how', 'why', 'when', 'where', 'who']
        if any(word in message_lower for word in question_words):
            analysis['message_type'] = 'question'
        elif any(word in message_lower for word in ['help', 'explain', 'mean']):
            analysis['message_type'] = 'help_request'
        elif any(word in message_lower for word in ['thanks', 'thank', 'appreciate']):
            analysis['message_type'] = 'gratitude'
        elif any(word in message_lower for word in ['hi', 'hello', 'hey', 'sup']):
            analysis['message_type'] = 'greeting'
        
        # Determine emotional tone
        positive_words = ['great', 'awesome', 'love', 'good', 'amazing', 'perfect', 'nice', 'best']
        negative_words = ['bad', 'hate', 'terrible', 'awful', 'wrong', 'confused', 'stressed', 'tired']
        
        if any(word in message_lower for word in positive_words):
            analysis['emotional_tone'] = 'positive'
        elif any(word in message_lower for word in negative_words):
            analysis['emotional_tone'] = 'negative'
        
        return analysis
    
    def generate_sms_response(self, user_message, analysis_data=None):
        """Generate SMS-style response with cultural slang and idioms"""
        
        # Analyze the user's message
        user_analysis = self.analyze_user_message(user_message)
        
        # Store conversation history
        self.conversation_history.append({
            'user_message': user_message,
            'timestamp': datetime.now(),
            'analysis': user_analysis
        })
        
        response_parts = []
        
        # 1. Natural acknowledgment based on what they said
        contextual_response = self._generate_contextual_response(user_message, user_analysis)
        response_parts.append(contextual_response)
        
        # 2. Address any slang they used (if applicable)
        if user_analysis['contains_slang']:
            response_parts.append("btw I see you using some slang! 👀")
            for slang_item in user_analysis['contains_slang'][:2]:  # Limit to 2
                response_parts.append(f"💬 \"{slang_item['term']}\" = {slang_item['meaning']}")
        
        # 3. Continue the conversation naturally while teaching new slang
        follow_up = self._generate_natural_follow_up(user_message, user_analysis)
        if follow_up:
            response_parts.append(follow_up)
        
        # 4. Add slang explanations only if new slang was used
        new_slang_used = self._extract_slang_from_response(" ".join(response_parts))
        if new_slang_used:
            response_parts.append("\\n📚 **Slang breakdown:**")
            for term, meaning in new_slang_used.items():
                response_parts.append(f"• \"{term}\" = {meaning}")
        
        return " ".join(response_parts)
    
    def _generate_contextual_response(self, user_message, analysis):
        """Generate a response that actually relates to what the user said"""
        message_lower = user_message.lower()
        main_topic = analysis.get('main_topic')
        
        # Greeting responses
        if analysis['message_type'] == 'greeting':
            return random.choice(self.bot_vocabulary['greetings'])
        
        # Gratitude responses
        if analysis['message_type'] == 'gratitude':
            return random.choice([
                "aww you're so sweet! no cap that made my day! 💕",
                "bestie you're the best! happy to help! ✨",
                "stop it, you're gonna make me cry! 🥺 glad I could help!"
            ])
        
        # Question responses - actually try to engage with their question
        if analysis['message_type'] == 'question':
            if any(word in message_lower for word in ['how are you', 'how you doing', 'what up']):
                return random.choice([
                    "I'm living my best life! just vibing and helping people learn slang! how about you bestie?",
                    "oh you know, just existing and serving knowledge! 💅 what's good with you?",
                    "honestly thriving! thanks for asking! what's on your mind today?"
                ])
            elif main_topic == 'weather':
                return random.choice([
                    "no cap it's been a pretty good day! the weather's giving main character vibes fr!",
                    "today's been chef's kiss so far! ✨ how's your day treating you?",
                    "honestly the vibes have been immaculate today! what about you?"
                ])
            else:
                return random.choice([
                    "ooh good question! let me think about that...",
                    "that's actually such a vibe! I love when people ask about that!",
                    "okay wait that's actually so interesting to think about!"
                ])
        
        # Help request responses
        if analysis['message_type'] == 'help_request':
            return random.choice([
                "bestie I got you! let me break that down for you!",
                "say less! I'm here to help! ✨",
                "period! helping you learn is literally my favorite thing!"
            ])
        
        # Emotional tone responses
        if analysis['emotional_tone'] == 'positive':
            return random.choice([
                "yesss I love that energy! ✨",
                "okay that's actually so slay of you!",
                "period! the vibes are immaculate! 🔥",
                "no cap that sounds amazing!",
                "I'm so here for this! tell me more!"
            ])
        elif analysis['emotional_tone'] == 'negative':
            return random.choice([
                "oof bestie that sounds rough... sending you good vibes! 💕",
                "aww no that's not it! hope things get better for you!",
                "big yikes! that's definitely not the vibe we want...",
                "oh no! that's giving main character in a sad movie... hope it gets better!"
            ])
        
        # Topic-specific responses using main_topic
        if main_topic == 'work_school':
            return random.choice([
                "ooh work/school talk! I feel you on that!",
                "periodt the academic/work life is really something!",
                "no cap that hits different when you're in the thick of it!"
            ])
        elif main_topic == 'food':
            return random.choice([
                "okay but food talk is my favorite topic! 🍕",
                "bestie the way food just hits different though!",
                "not me getting hungry just thinking about it! 😅"
            ])
        elif main_topic == 'tired_stressed':
            return random.choice([
                "oof the tiredness is real! I feel you bestie!",
                "big mood! being tired is not the vibe!",
                "aww bestie you need some rest! self-care is not selfish!"
            ])
        elif main_topic == 'weather':
            return random.choice([
                "okay but good weather just hits different! ☀️",
                "the weather's giving main character vibes today!",
                "bestie mother nature understood the assignment!"
            ])
        elif main_topic == 'music':
            return random.choice([
                "OMG yes! good music just lives rent free in your head fr!",
                "music that slaps is literally my love language! 🎵",
                "periodt! a good song can literally change your whole vibe!"
            ])
        elif main_topic == 'entertainment':
            return random.choice([
                "okay but binge-watching is literally self-care!",
                "ooh I love a good show recommendation! 📺",
                "the way a good series just hits different though!"
            ])
        elif main_topic == 'academic':
            return random.choice([
                "oof exam stress is not the vibe! sending you good energy! ✨",
                "bestie you got this! manifesting good grades for you!",
                "studying is rough but you're gonna slay that test!"
            ])
        else:
            # Generic but still acknowledging
            return random.choice([
                "okay I see you! that's actually such a mood!",
                "no cap I totally get what you mean!",
                "bestie that's actually so real!",
                "periodt! I hear you on that!"
            ])
    
    def _generate_natural_follow_up(self, user_message, analysis):
        """Generate a natural follow-up that continues the conversation"""
        main_topic = analysis.get('main_topic')
        
        # Ask follow-up questions based on main topic
        if main_topic == 'work_school':
            return random.choice([
                "what's the vibe there? is it giving stressful energy or are you lowkey enjoying it?",
                "ooh spill the tea! what's been going on with that?",
                "I'm manifesting good vibes for you bestie! ✨"
            ])
        elif main_topic == 'food':
            return random.choice([
                "okay but what's your go-to comfort food? I need recommendations!",
                "bestie you're making me hungry just talking about it! 😅",
                "food that hits different is literally the best kind of food!"
            ])
        elif main_topic == 'music':
            return random.choice([
                "OMG what's been on repeat for you lately?",
                "bestie good music is literally everything! what genre slaps for you?",
                "okay but tell me about your current playlist vibe! 🎵"
            ])
        elif main_topic == 'entertainment':
            return random.choice([
                "okay but did it understand the assignment or was it mid?",
                "ooh I love a good binge session! what's giving you life lately?",
                "not me adding more stuff to my watch list! 📺"
            ])
        elif main_topic == 'plans':
            return random.choice([
                "okay but weekend plans that actually slap are *chef's kiss*!",
                "I'm manifesting the most iconic weekend for you! ✨",
                "bestie living your best life is the only vibe we accept!"
            ])
        elif main_topic == 'tired_stressed':
            return random.choice([
                "bestie make sure you're taking care of yourself! self-care is not selfish! 💕",
                "oof sending you good vibes! what usually helps you relax?",
                "you deserve all the rest bestie! what's your go-to chill activity?"
            ])
        elif main_topic == 'weather':
            return random.choice([
                "the weather really sets the whole vibe for the day fr!",
                "okay but what's your favorite weather mood? ☀️",
                "bestie weather that hits different just makes everything better!"
            ])
        elif main_topic == 'academic':
            return random.choice([
                "bestie you're gonna absolutely slay that test! I'm manifesting good grades! ✨",
                "studying is rough but you got this! what subject is giving you trouble?",
                "periodt academic stress is real but you're stronger than you think!"
            ])
        elif analysis['message_type'] == 'question':
            return random.choice([
                "but honestly what's your take on that? I'm curious!",
                "okay but tell me more about that bestie! ✨",
                "that's actually so interesting! I love hearing people's thoughts!"
            ])
        else:
            # Generic follow-ups that still relate to conversation
            return random.choice([
                "that's actually such a vibe! tell me more!",
                "okay but I'm here for this energy! ✨",
                "bestie you always have the most interesting takes!",
                "periodt! what's been on your mind about that lately?"
            ])
    
    def _extract_slang_from_response(self, response_text):
        """Extract slang terms used in the response that need explanation"""
        response_lower = response_text.lower()
        found_slang = {}
        
        # Common slang terms we should explain
        slang_to_explain = {
            "no cap": "no lie, being serious",
            "periodt": "period, end of discussion (emphasis)",
            "bestie": "best friend (friendly term)",
            "vibes": "feelings, atmosphere, or energy",
            "slaps": "is really good or impressive", 
            "hits different": "is uniquely good or special",
            "chef's kiss": "perfect, exactly right",
            "main character": "confident, putting yourself first",
            "say less": "I understand, you don't need to explain more",
            "rent free": "constantly in your thoughts",
            "mid": "mediocre, not great but not terrible",
            "slay": "do something really well",
            "iconic": "memorable and impressive",
            "immaculate": "perfect, flawless",
            "manifesting": "hoping/wishing for something to happen"
        }
        
        for term, meaning in slang_to_explain.items():
            if term in response_lower:
                found_slang[term] = meaning
        
        return found_slang
    
    def _add_slang_explanations(self, response_parts, text):
        """Find and explain slang in the given text"""
        text_lower = text.lower()
        explained_terms = []
        
        for term, meaning in self.idioms_database.items():
            if term in text_lower and term not in explained_terms:
                response_parts.append(f"• \"{term}\" = {meaning}")
                explained_terms.append(term)
                if len(explained_terms) >= 3:  # Limit explanations
                    break
        
        # Add some common cultural expressions
        cultural_terms = {
            "sending me": "making me laugh really hard",
            "obsessed": "really love something",
            "main character": "confident, putting yourself first",
            "vibes": "feelings or atmosphere",
            "bestie": "best friend (friendly way to address someone)",
            "no cap": "no lie, being serious",
            "periodt": "period, end of discussion",
            "chef's kiss": "perfect, exactly right",
            "hits different": "is uniquely good or special"
        }
        
        for term, meaning in cultural_terms.items():
            if term in text_lower and term not in explained_terms:
                response_parts.append(f"• \"{term}\" = {meaning}")
                explained_terms.append(term)
                if len(explained_terms) >= 3:
                    break
    
    def get_practice_suggestion(self):
        """Generate a practice suggestion with new slang"""
        scenarios = [
            {
                "scenario": "You just tried amazing food",
                "slang_response": "This food is absolutely sending me! It hits different! 🔥",
                "explanation": "Use 'sending me' when something is really impressive, and 'hits different' when something is uniquely good"
            },
            {
                "scenario": "Your friend looks great today",
                "slang_response": "Bestie, you're serving looks today! Your outfit understood the assignment! ✨",
                "explanation": "'Serving looks' means looking great, 'understood the assignment' means you did exactly what was expected perfectly"
            },
            {
                "scenario": "You're excited about weekend plans",
                "slang_response": "I'm so here for this! It's giving main character energy! No cap! 💯",
                "explanation": "'I'm so here for this' means you're excited, 'it's giving...' describes the vibe, 'no cap' means no lie"
            },
            {
                "scenario": "Someone tells you good news",
                "slang_response": "OMG periodt! That's so slay of you! I'm literally obsessed! 🙌",
                "explanation": "'Periodt' emphasizes agreement, 'slay' means doing something well, 'obsessed' means you really love it"
            }
        ]
        
        return random.choice(scenarios)

# Global instance
sms_bot = ConversationalSMSBot()

def get_sms_bot_response(user_message, analysis_data=None):
    """Get SMS-style conversational response"""
    return sms_bot.generate_sms_response(user_message, analysis_data)

def get_practice_suggestion():
    """Get a practice suggestion"""
    return sms_bot.get_practice_suggestion()
