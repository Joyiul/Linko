import os
import numpy as np
import pandas as pd
import librosa
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import joblib
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tensorflow as tf
from tensorflow import keras
import traceback
import re

class RobustEmotionAnalyzer:
    def __init__(self):
        """Initialize robust emotion analyzer with enhanced emoji detection"""
        self.text_analyzer = SentimentIntensityAnalyzer()
        self.models_loaded = False
        self.audio_model = None
        self.audio_encoder = None
        
        # Load emoji mappings for tone detection
        self.emoji_emotions = self._load_emoji_mappings()
        
        # Define comprehensive emotion-emoji mappings
        self.emotion_emojis = {
            'happy': ['😊', '😀', '😁', '😄', '😆', '🙂', '😋', '🤗', '😇', '🥰', '😍', '🤩', '😘', '😗', '😙', '😚', '🤭'],
            'excited': ['😃', '😆', '🤩', '🤗', '🎉', '🙌', '👏', '🔥', '⚡', '✨', '💫', '🌟', '🎊', '🥳'],
            'love': ['😍', '🥰', '😘', '💕', '💖', '💗', '💓', '💝', '❤️', '🧡', '💛', '💚', '💙', '💜', '🤍', '🖤'],
            'angry': ['😠', '😡', '🤬', '😤', '💢', '👿', '🔥', '💯', '🤯'],
            'sad': ['😢', '😭', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😪'],
            'disappointed': ['😞', '😔', '😟', '😕', '🙁', '☹️', '😤', '😮‍💨', '😒', '🫤'],
            'fear': ['😨', '😰', '😱', '🤯', '😧', '😦', '😮', '🫢', '🙀', '🫣'],
            'surprise': ['😮', '😯', '😲', '🤯', '😳', '🫢', '🤭', '😱', '🙀', '‼️', '❗', '❓', '❔'],
            'disgust': ['🤢', '🤮', '😷', '🤧', '🤒', '😵', '🤐', '🙄', '😒', '😑'],
            'neutral': ['😐', '😑', '🙂', '😶', '🫤', '😕', '🤷', '🤷‍♀️', '🤷‍♂️'],
            'confused': ['😕', '🤔', '🫤', '😵‍💫', '🤯', '🫨', '😵', '❓', '❔'],
            'laughing': ['😂', '🤣', '😆', '😹', '💀', '☠️', '😄', '😁'],
            'cool': ['😎', '🤠', '🕶️', '😏', '🤘', '👌', '🔥', '💯'],
            'crying': ['😭', '😢', '🥺', '😿', '😾'],
            'sleeping': ['😴', '💤', '🛌', '😪'],
            'sick': ['🤢', '🤮', '😷', '🤧', '🤒', '🥵', '🥶'],
            'party': ['🥳', '🎉', '🎊', '🍾', '🥂', '🍻', '🎈', '🎁'],
            'thinking': ['🤔', '💭', '🧠', '💡', '🔍'],
            'shocked': ['😱', '🤯', '😳', '🫢', '😲', '😮', '😯', '🙀'],
            'embarrassed': ['😳', '😅', '🤭', '🫣', '😊', '🤗', '😌'],
            'flirty': ['😉', '😏', '😘', '😗', '💋', '💕', '🥰', '😍'],
            'sarcastic': ['🙃', '😏', '🙄', '😒', '🤨', '😑']
        }
        
        # Define emotion patterns with enhanced emoji context
        self.emotion_patterns = {
            'happy': {
                'keywords': ['happy', 'joy', 'joyful', 'wonderful', 'great', 'awesome', 'fantastic', 'love', 'smile', 'glad', 'cheerful', 'delighted', 'content'],
                'phrases': ["i'm so happy", "so happy", "really happy", "very happy", "feel great", "feeling good", "love this", "this is great", "makes me happy"],
                'intensity_words': ['extremely', 'very', 'really', 'so', 'absolutely', 'super', 'totally', 'incredibly']
            },
            'excited': {
                'keywords': ['excited', 'thrilled', 'ecstatic', 'exhilarated', 'pumped', 'stoked', 'hyped', 'enthusiastic', 'eager'],
                'phrases': ["i'm so excited", "so excited", "really excited", "very excited", "can't wait", "so pumped", "really thrilled", "absolutely thrilled"],
                'intensity_words': ['extremely', 'very', 'really', 'so', 'absolutely', 'super', 'totally', 'incredibly']
            },
            'angry': {
                'keywords': ['angry', 'mad', 'furious', 'rage', 'hate', 'damn', 'annoyed', 'irritated', 'pissed', 'frustrated', 'livid', 'frustrating'],
                'phrases': ['fed up', 'had enough', 'so angry', 'really mad', 'totally pissed', "i'm angry", "makes me angry", "pissed off", "so frustrating", "really frustrating"],
                'intensity_words': ['extremely', 'very', 'really', 'so', 'totally', 'absolutely']
            },
            'sad': {
                'keywords': ['sad', 'depressed', 'down', 'hurt', 'pain', 'lonely', 'miserable', 'upset', 'heartbroken', 'devastated'],
                'phrases': ['feeling down', 'so sad', 'really hurt', 'feel terrible', 'quite depressed', "i'm sad", "makes me sad", "feel awful"],
                'intensity_words': ['very', 'really', 'extremely', 'quite', 'so', 'totally']
            },
            'disappointed': {
                'keywords': ['disappointed', 'disappointment', 'let down', 'dissatisfied', 'unfulfilled', 'disillusioned', 'underwhelmed'],
                'phrases': ['so disappointed', 'really disappointed', 'let me down', 'quite disappointed', 'feel disappointed', "i'm disappointed", "such a disappointment"],
                'intensity_words': ['very', 'really', 'extremely', 'quite', 'so', 'totally']
            },
            'fear': {
                'keywords': ['scared', 'afraid', 'fear', 'nervous', 'anxious', 'worried', 'panic', 'terrified', 'frightened', 'alarmed'],
                'phrases': ['so scared', 'really afraid', 'quite nervous', 'very anxious', 'totally terrified', "i'm scared", "makes me nervous"],
                'intensity_words': ['very', 'really', 'extremely', 'quite', 'so', 'totally']
            },
            'interest': {
                'keywords': ['interested', 'curious', 'intrigued', 'fascinating', 'wonder', 'wondering', 'interesting', 'compelling', 'captivating', 'intriguing'],
                'phrases': ['so interesting', 'really curious', 'quite intrigued', 'very interesting', 'makes me wonder', "i'm curious", "find it interesting", "want to know"],
                'intensity_words': ['very', 'really', 'quite', 'so', 'extremely', 'totally']
            },
            'disgust': {
                'keywords': ['disgusting', 'gross', 'sick', 'revolting', 'awful', 'horrible', 'nasty', 'yuck', 'ew', 'disgusted'],
                'phrases': ['so gross', 'really disgusting', 'quite awful', 'totally sick', "makes me sick", "that's disgusting"],
                'intensity_words': ['very', 'really', 'extremely', 'quite', 'so', 'totally']
            },
            'surprise': {
                'keywords': ['wow', 'amazing', 'unbelievable', 'shocked', 'surprised', 'incredible', 'astonishing', 'unexpected', 'stunned'],
                'phrases': ['oh wow', 'so surprised', 'really amazing', 'quite shocking', 'totally unexpected', "can't believe", "so unexpected"],
                'intensity_words': ['very', 'really', 'extremely', 'quite', 'so', 'totally']
            },
            'neutral': {
                'keywords': ['okay', 'fine', 'normal', 'regular', 'standard', 'typical', 'according', 'based', 'generally'],
                'phrases': ['it is', 'according to', 'based on', 'in general', 'as usual', 'nothing special'],
                'intensity_words': []
            }
        }
        
        # Try to load models
        self._load_models()
        
        # Load emoji mappings
        self._load_emoji_mappings()
    
    def _load_emoji_mappings(self):
        """Load emoji mappings from CSV dataset"""
        self.emoji_mappings = {}
        try:
            csv_path = os.path.join(os.path.dirname(__file__), '..', 'Datasets', 'genz_emojis.csv')
            if os.path.exists(csv_path):
                import pandas as pd
                df = pd.read_csv(csv_path)
                for _, row in df.iterrows():
                    emoji = row.get('emoji', '')
                    meaning = row.get('meaning', '').lower()
                    if emoji and meaning:
                        # Map emoji to emotional context
                        emotion_context = self._map_meaning_to_emotion(meaning)
                        self.emoji_mappings[emoji] = {
                            'meaning': meaning,
                            'emotion': emotion_context
                        }
        except Exception as e:
            print(f"Warning: Could not load emoji mappings: {e}")
            self.emoji_mappings = {}
    
    def _map_meaning_to_emotion(self, meaning):
        """Map emoji meaning to emotion category"""
        meaning_lower = meaning.lower()
        
        # Map meanings to primary emotions
        if any(word in meaning_lower for word in ['happy', 'joy', 'laugh', 'fun', 'love', 'excited']):
            return 'joy'
        elif any(word in meaning_lower for word in ['sad', 'cry', 'tears', 'depressed', 'down']):
            return 'sadness'
        elif any(word in meaning_lower for word in ['angry', 'mad', 'rage', 'annoyed', 'furious']):
            return 'anger'
        elif any(word in meaning_lower for word in ['scared', 'fear', 'afraid', 'worried', 'nervous']):
            return 'fear'
        elif any(word in meaning_lower for word in ['surprised', 'shock', 'wow', 'amazing']):
            return 'surprise'
        elif any(word in meaning_lower for word in ['disgust', 'gross', 'yuck', 'eww']):
            return 'disgust'
        elif any(word in meaning_lower for word in ['neutral', 'okay', 'fine', 'normal']):
            return 'neutral'
        else:
            return 'neutral'
    
    def detect_emojis_in_text(self, text):
        """Detect emojis in text and return their analysis"""
        import re
        
        # Enhanced emoji pattern to catch more emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001F900-\U0001F9FF"  # supplemental symbols
            "]+", flags=re.UNICODE
        )
        
        found_emojis = emoji_pattern.findall(text)
        emoji_analysis = []
        
        for emoji in found_emojis:
            if emoji in self.emoji_mappings:
                emoji_data = self.emoji_mappings[emoji]
                emoji_analysis.append({
                    'emoji': emoji,
                    'meaning': emoji_data['meaning'],
                    'emotion': emoji_data['emotion']
                })
        
        return emoji_analysis
    
    def analyze_emoji_tone(self, emoji_analysis):
        """Analyze overall tone based on detected emojis"""
        if not emoji_analysis:
            return {'tone': 'neutral', 'confidence': 0.0, 'details': 'No emojis detected'}
        
        # Count emotion categories
        emotion_counts = {}
        for emoji_data in emoji_analysis:
            emotion = emoji_data['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Determine dominant emotion
        if emotion_counts:
            dominant_emotion = max(emotion_counts, key=emotion_counts.get)
            confidence = emotion_counts[dominant_emotion] / len(emoji_analysis)
            
            # Create detailed response
            emoji_list = [f"{data['emoji']} ({data['meaning']})" for data in emoji_analysis]
            details = f"Detected {len(emoji_analysis)} emojis: {', '.join(emoji_list)}"
            
            return {
                'tone': dominant_emotion,
                'confidence': confidence,
                'details': details,
                'emoji_breakdown': emotion_counts
            }
        
        return {'tone': 'neutral', 'confidence': 0.0, 'details': 'No meaningful emojis found'}
    
    def _load_models(self):
        """Load audio emotion models with robust error handling"""
        try:
            model_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained')
            
            # Try to load improved audio model
            audio_model_path = os.path.join(model_dir, 'emotion_model_improved.h5')
            if os.path.exists(audio_model_path):
                print(f"Loading audio model from: {audio_model_path}")
                self.audio_model = keras.models.load_model(audio_model_path)
                print("✓ Audio emotion model loaded successfully")
            
            # Try to load audio label encoder with multiple methods
            encoder_paths = [
                os.path.join(model_dir, 'label_encoder.pkl'),
                os.path.join(model_dir, 'audio_label_encoder.pkl')
            ]
            
            encoder_loaded = False
            for encoder_path in encoder_paths:
                if os.path.exists(encoder_path):
                    try:
                        # Try pickle first
                        with open(encoder_path, 'rb') as f:
                            self.audio_encoder = pickle.load(f)
                        print(f"✓ Audio label encoder loaded from {encoder_path}")
                        encoder_loaded = True
                        break
                    except Exception as e1:
                        try:
                            # Try joblib
                            self.audio_encoder = joblib.load(encoder_path)
                            print(f"✓ Audio label encoder loaded with joblib from {encoder_path}")
                            encoder_loaded = True
                            break
                        except Exception as e2:
                            print(f"Warning: Could not load encoder from {encoder_path} (pickle: {e1}, joblib: {e2})")
            
            if not encoder_loaded:
                print("Warning: Could not load audio label encoder. Creating fallback encoder...")
                self._create_fallback_encoder()
            
            self.models_loaded = True
            
        except Exception as e:
            print(f"Error loading emotion analysis models: {e}")
            traceback.print_exc()
            self._create_fallback_encoder()
    
    def _create_fallback_encoder(self):
        """Create a fallback label encoder for basic emotion categories"""
        self.audio_encoder = LabelEncoder()
        # Standard emotion categories
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.audio_encoder.fit(emotions)
        print("Creating fallback encoder for audio emotions...")
    
    def analyze_text_robust(self, text):
        """Robust text-based emotion analysis with improved sensitivity"""
        if not text or not text.strip():
            return {'emotion': 'neutral', 'confidence': 0.3}
        
        text_lower = text.lower()
        
        # VADER sentiment analysis for baseline
        vader_scores = self.text_analyzer.polarity_scores(text)
        
        # Enhanced pattern-based emotion scoring with higher accuracy
        emotion_scores = {}
        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            
            # Direct keyword matching with context awareness
            for keyword in patterns['keywords']:
                if keyword in text_lower:
                    # Check if keyword is standalone word (not part of another word)
                    import re
                    if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                        score += 5  # Higher score for exact word matches
                    else:
                        score += 2  # Lower score for partial matches
            
            # Phrase matching (weighted much higher for complete expressions)
            for phrase in patterns['phrases']:
                if phrase in text_lower:
                    score += 12  # Much higher score for complete phrases
            
            # Enhanced personal statements with more variations
            personal_indicators = [
                f"i'm {keyword}" for keyword in patterns['keywords'][:8]
            ] + [
                f"i am {keyword}" for keyword in patterns['keywords'][:8]
            ] + [
                f"feeling {keyword}" for keyword in patterns['keywords'][:8]
            ] + [
                f"i feel {keyword}" for keyword in patterns['keywords'][:8]
            ] + [
                f"i'm so {keyword}" for keyword in patterns['keywords'][:5]
            ] + [
                f"really {keyword}" for keyword in patterns['keywords'][:5]
            ] + [
                f"very {keyword}" for keyword in patterns['keywords'][:5]
            ]
            
            for personal in personal_indicators:
                if personal in text_lower:
                    score += 15  # Very high score for personal emotional statements
            
            # Enhanced intensity modifiers with proximity checking
            for keyword in patterns['keywords']:
                if keyword in text_lower:
                    for intensity in patterns['intensity_words']:
                        intensity_patterns = [
                            f"{intensity} {keyword}",
                            f"i'm {intensity} {keyword}",
                            f"feel {intensity} {keyword}",
                            f"{keyword} {intensity}",
                            f"so {intensity} {keyword}",
                            f"really {intensity} {keyword}"
                        ]
                        for pattern in intensity_patterns:
                            if pattern in text_lower:
                                score += 8  # Higher bonus for intensity
            
            # Enhanced exclamation and caps detection
            if '!' in text and emotion != 'neutral':
                excitement_keywords = [kw for kw in patterns['keywords'] if kw in text_lower]
                if excitement_keywords:
                    exclamation_count = text.count('!')
                    score += exclamation_count * 3  # Higher bonus per exclamation
            
            # Caps detection for emotional intensity
            caps_words = [word for word in text.split() if word.isupper() and len(word) > 2]
            if caps_words and emotion != 'neutral':
                for keyword in patterns['keywords']:
                    if any(keyword.upper() in caps_word for caps_word in caps_words):
                        score += 6  # Bonus for caps emotional words
            
            # Emoji boost from emoji analysis
            if hasattr(self, 'emoji_mappings'):
                emoji_analysis = self.detect_emojis_in_text(text)
                emoji_tone = self.analyze_emoji_tone(emoji_analysis)
                if emoji_tone['tone'] == emotion and emoji_tone['confidence'] > 0.5:
                    score += 10  # Strong emoji reinforcement
            
            emotion_scores[emotion] = score
        
        # Enhanced VADER integration
        if vader_scores['compound'] > 0.6:
            emotion_scores['joy'] = emotion_scores.get('joy', 0) + 8
        elif vader_scores['compound'] < -0.6:
            emotion_scores['sadness'] = emotion_scores.get('sadness', 0) + 8
        elif abs(vader_scores['compound']) < 0.1:
            emotion_scores['neutral'] = emotion_scores.get('neutral', 0) + 3
        
        # Determine primary emotion with improved confidence calculation
        max_score = max(emotion_scores.values()) if emotion_scores else 0
        
        if max_score > 0:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            # Improved confidence calculation
            if max_score >= 15:
                confidence = min(0.85 + (max_score - 15) * 0.01, 0.98)
            elif max_score >= 8:
                confidence = 0.65 + (max_score - 8) * 0.02
            elif max_score >= 3:
                confidence = 0.45 + (max_score - 3) * 0.04
            else:
                confidence = 0.25 + max_score * 0.06
        else:
            primary_emotion = 'neutral'
            confidence = 0.4
        
        return {
            'emotion': primary_emotion,
            'confidence': confidence,
            'details': {
                'vader_scores': vader_scores,
                'emotion_scores': emotion_scores,
                'max_score': max_score,
                'method': 'enhanced_pattern_matching' if max_score > 0 else 'vader_fallback',
                'text_length': len(text.split())
            }
        }
    
    def extract_safe_audio_features(self, audio_path):
        """Safely extract audio features with error handling"""
        try:
            # Load audio with librosa
            y, sr = librosa.load(audio_path, duration=5.0, sr=22050)
            
            if len(y) == 0:
                return None
            
            # Extract basic features
            features = []
            
            # MFCC features
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            features.extend(np.mean(mfcc, axis=1))
            features.extend(np.std(mfcc, axis=1))
            
            # Energy features
            rms = librosa.feature.rms(y=y)[0]
            features.append(np.mean(rms))
            features.append(np.std(rms))
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            features.append(np.mean(spectral_centroids))
            
            zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
            features.append(np.mean(zero_crossing_rate))
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features.append(tempo)
            
            return np.array(features)
            
        except Exception as e:
            print(f"Error extracting audio features from {audio_path}: {e}")
            return None
    
    def analyze_audio_emotion(self, audio_path):
        """Analyze audio file for emotion with fallback mechanisms"""
        if not os.path.exists(audio_path):
            return {'emotion': 'neutral', 'confidence': 0.2, 'error': 'Audio file not found'}
        
        try:
            # Extract features
            features = self.extract_safe_audio_features(audio_path)
            
            if features is None:
                return {'emotion': 'neutral', 'confidence': 0.2, 'error': 'Feature extraction failed'}
            
            # If we have a trained model, use it
            if self.audio_model is not None and self.audio_encoder is not None:
                try:
                    # Reshape features for model input
                    features_reshaped = features.reshape(1, -1)
                    
                    # Ensure we have the right number of features
                    if features_reshaped.shape[1] < 31:  # Pad if too few features
                        padding = np.zeros((1, 31 - features_reshaped.shape[1]))
                        features_reshaped = np.hstack([features_reshaped, padding])
                    elif features_reshaped.shape[1] > 31:  # Truncate if too many
                        features_reshaped = features_reshaped[:, :31]
                    
                    # Predict emotion
                    predictions = self.audio_model.predict(features_reshaped, verbose=0)
                    predicted_class_idx = np.argmax(predictions[0])
                    confidence = float(predictions[0][predicted_class_idx])
                    
                    # Map to emotion label
                    if hasattr(self.audio_encoder, 'inverse_transform'):
                        emotion = self.audio_encoder.inverse_transform([predicted_class_idx])[0]
                    else:
                        # Fallback mapping
                        emotion_map = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}
                        emotion = emotion_map.get(predicted_class_idx, 'neutral')
                    
                    return {
                        'emotion': emotion,
                        'confidence': confidence,
                        'method': 'ml_model',
                        'features_extracted': len(features)
                    }
                    
                except Exception as e:
                    print(f"Error using ML model for audio analysis: {e}")
                    # Fall through to rule-based analysis
            
            # Rule-based fallback analysis
            emotion = self._analyze_audio_features_simple(features)
            return {
                'emotion': emotion,
                'confidence': 0.5,
                'method': 'rule_based_fallback',
                'features_extracted': len(features)
            }
            
        except Exception as e:
            print(f"Error in audio emotion analysis: {e}")
            return {'emotion': 'neutral', 'confidence': 0.2, 'error': str(e)}
    
    def _analyze_audio_features_simple(self, features):
        """Simple rule-based audio emotion analysis"""
        try:
            # Basic feature indices (approximate)
            energy_mean = features[26] if len(features) > 26 else 0
            tempo = features[-1] if len(features) > 0 else 120
            spectral_centroid = features[-3] if len(features) > 2 else 1000
            
            # Simple rules
            if energy_mean > 0.1 and tempo > 140:
                return 'happy'
            elif energy_mean < 0.05:
                return 'sad'
            elif energy_mean > 0.15 and spectral_centroid > 2000:
                return 'angry'
            else:
                return 'neutral'
                
        except Exception:
            return 'neutral'

# Global analyzer instance
robust_analyzer = RobustEmotionAnalyzer()

def analyze_emotion_robust(text=None, audio_path=None):
    """Main function for robust emotion analysis"""
    results = {}
    
    # Analyze text if provided
    if text:
        text_result = robust_analyzer.analyze_text_robust(text)
        results['text_analysis'] = text_result
        
        # Add emoji analysis for text
        emoji_analysis = robust_analyzer.detect_emojis_in_text(text)
        emoji_tone = robust_analyzer.analyze_emoji_tone(emoji_analysis)
        results['emoji_analysis'] = emoji_tone
    
    # Analyze audio if provided
    if audio_path:
        audio_result = robust_analyzer.analyze_audio_emotion(audio_path)
        results['audio_analysis'] = audio_result
    
    # Determine overall emotion
    if text and audio_path:
        # Combine text, audio, and emoji analyses
        text_emotion = results['text_analysis']['emotion']
        audio_emotion = results['audio_analysis']['emotion']
        emoji_emotion = results['emoji_analysis']['tone']
        emoji_confidence = results['emoji_analysis']['confidence']
        
        # If emojis detected with high confidence, factor them in
        if emoji_confidence > 0.6:
            # Strong emoji indicators - weight them heavily
            if emoji_emotion == text_emotion or emoji_emotion == audio_emotion:
                # Emoji agrees with one modality
                primary_emotion = emoji_emotion
                confidence = min((results['text_analysis']['confidence'] + results['audio_analysis']['confidence'] + emoji_confidence) / 3 * 1.3, 0.95)
            else:
                # Emoji disagrees - still consider it but lower weight
                primary_emotion = text_emotion  # Prefer text as baseline
                confidence = results['text_analysis']['confidence'] * 0.9
        else:
            # Low emoji confidence - standard text/audio analysis
            if text_emotion == audio_emotion:
                primary_emotion = text_emotion
                confidence = min((results['text_analysis']['confidence'] + results['audio_analysis']['confidence']) / 2 * 1.2, 0.95)
            else:
                primary_emotion = text_emotion
                confidence = results['text_analysis']['confidence'] * 0.8
        
        results['multimodal_analysis'] = {
            'primary_emotion': primary_emotion,
            'confidence': confidence,
            'agreement': {
                'text_audio': text_emotion == audio_emotion,
                'text_emoji': text_emotion == emoji_emotion,
                'audio_emoji': audio_emotion == emoji_emotion
            },
            'emoji_influence': emoji_confidence > 0.6
        }
    elif text:
        # Text-only analysis with emoji enhancement
        text_emotion = results['text_analysis']['emotion']
        emoji_emotion = results['emoji_analysis']['tone']
        emoji_confidence = results['emoji_analysis']['confidence']
        
        if emoji_confidence > 0.7:
            # Strong emoji indicators
            if emoji_emotion == text_emotion:
                # Emoji reinforces text analysis
                primary_emotion = text_emotion
                confidence = min(results['text_analysis']['confidence'] * 1.2, 0.95)
            else:
                # Emoji contradicts text - prefer emoji for tone
                primary_emotion = emoji_emotion
                confidence = max(emoji_confidence, results['text_analysis']['confidence'] * 0.8)
        else:
            # Weak or no emoji signal
            primary_emotion = text_emotion
            confidence = results['text_analysis']['confidence']
        
        results['multimodal_analysis'] = {
            'primary_emotion': primary_emotion,
            'confidence': confidence,
            'modality': 'text_with_emoji',
            'emoji_influence': emoji_confidence > 0.7
        }
    elif audio_path:
        results['multimodal_analysis'] = {
            'primary_emotion': results['audio_analysis']['emotion'],
            'confidence': results['audio_analysis']['confidence'],
            'modality': 'audio_only'
        }
    else:
        results['multimodal_analysis'] = {
            'primary_emotion': 'neutral',
            'confidence': 0.3,
            'error': 'No input provided'
        }
    
    return results
