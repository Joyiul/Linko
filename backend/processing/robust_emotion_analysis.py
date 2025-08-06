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

class RobustEmotionAnalyzer:
    def __init__(self):
        """Initialize robust emotion analyzer with error handling"""
        self.text_analyzer = SentimentIntensityAnalyzer()
        self.models_loaded = False
        self.audio_model = None
        self.audio_encoder = None
        
        # Define emotion mappings
        self.emotion_patterns = {
            'angry': {
                'keywords': ['angry', 'mad', 'furious', 'rage', 'hate', 'damn', 'annoyed', 'irritated', 'pissed'],
                'phrases': ['fed up', 'had enough', 'so angry', 'really mad', 'totally pissed'],
                'intensity_words': ['extremely', 'very', 'really', 'so', 'totally']
            },
            'happy': {
                'keywords': ['happy', 'joy', 'excited', 'amazing', 'wonderful', 'great', 'awesome', 'fantastic'],
                'phrases': ['so happy', 'feel great', 'love this', 'amazing day', 'feeling wonderful'],
                'intensity_words': ['extremely', 'very', 'really', 'so', 'absolutely']
            },
            'sad': {
                'keywords': ['sad', 'depressed', 'down', 'hurt', 'pain', 'lonely', 'miserable', 'upset'],
                'phrases': ['feeling down', 'so sad', 'really hurt', 'feel terrible', 'quite depressed'],
                'intensity_words': ['very', 'really', 'extremely', 'quite', 'so']
            },
            'fear': {
                'keywords': ['scared', 'afraid', 'fear', 'nervous', 'anxious', 'worried', 'panic', 'terrified'],
                'phrases': ['so scared', 'really afraid', 'quite nervous', 'very anxious', 'totally terrified'],
                'intensity_words': ['very', 'really', 'extremely', 'quite', 'so', 'totally']
            },
            'disgust': {
                'keywords': ['disgusting', 'gross', 'sick', 'revolting', 'awful', 'horrible', 'nasty'],
                'phrases': ['so gross', 'really disgusting', 'quite awful', 'totally sick'],
                'intensity_words': ['very', 'really', 'extremely', 'quite', 'so', 'totally']
            },
            'surprise': {
                'keywords': ['wow', 'amazing', 'unbelievable', 'shocked', 'surprised', 'incredible'],
                'phrases': ['oh wow', 'so surprised', 'really amazing', 'quite shocking', 'totally unexpected'],
                'intensity_words': ['very', 'really', 'extremely', 'quite', 'so', 'totally']
            },
            'neutral': {
                'keywords': ['okay', 'fine', 'normal', 'regular', 'standard', 'typical'],
                'phrases': ['it is', 'according to', 'based on', 'in general'],
                'intensity_words': []
            }
        }
        
        # Try to load models
        self._load_models()
    
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
        """Robust text-based emotion analysis"""
        if not text or not text.strip():
            return {'emotion': 'neutral', 'confidence': 0.3}
        
        text_lower = text.lower()
        
        # VADER sentiment analysis
        vader_scores = self.text_analyzer.polarity_scores(text)
        
        # Pattern-based emotion scoring
        emotion_scores = {}
        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            
            # Keyword matching
            for keyword in patterns['keywords']:
                if keyword in text_lower:
                    score += 1
            
            # Phrase matching (weighted higher)
            for phrase in patterns['phrases']:
                if phrase in text_lower:
                    score += 2
            
            # Intensity modifiers
            for keyword in patterns['keywords']:
                if keyword in text_lower:
                    for intensity in patterns['intensity_words']:
                        # Check if intensity word is near the emotion keyword
                        if intensity in text_lower:
                            keyword_pos = text_lower.find(keyword)
                            intensity_pos = text_lower.find(intensity)
                            if abs(keyword_pos - intensity_pos) < 30:  # Within 30 characters
                                score += 1
            
            emotion_scores[emotion] = score
        
        # Determine primary emotion
        max_score = max(emotion_scores.values()) if emotion_scores else 0
        
        if max_score > 0:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(max_score * 0.2, 0.9)
        else:
            # Fall back to VADER sentiment
            compound = vader_scores.get('compound', 0)
            if compound >= 0.5:
                primary_emotion = 'happy'
                confidence = min(compound, 0.8)
            elif compound <= -0.5:
                primary_emotion = 'sad'
                confidence = min(abs(compound), 0.8)
            elif vader_scores.get('neu', 0) > 0.7:
                primary_emotion = 'neutral'
                confidence = 0.6
            else:
                primary_emotion = 'neutral'
                confidence = 0.4
        
        return {
            'emotion': primary_emotion,
            'confidence': confidence,
            'details': {
                'vader_scores': vader_scores,
                'emotion_scores': emotion_scores,
                'method': 'pattern_matching' if max_score > 0 else 'vader_fallback'
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
    
    # Analyze audio if provided
    if audio_path:
        audio_result = robust_analyzer.analyze_audio_emotion(audio_path)
        results['audio_analysis'] = audio_result
    
    # Determine overall emotion
    if text and audio_path:
        # Combine both analyses
        text_emotion = results['text_analysis']['emotion']
        audio_emotion = results['audio_analysis']['emotion']
        
        if text_emotion == audio_emotion:
            # Agreement between modalities
            primary_emotion = text_emotion
            confidence = min((results['text_analysis']['confidence'] + results['audio_analysis']['confidence']) / 2 * 1.2, 0.95)
        else:
            # Disagreement - prefer text analysis for now
            primary_emotion = text_emotion
            confidence = results['text_analysis']['confidence'] * 0.8
        
        results['multimodal_analysis'] = {
            'primary_emotion': primary_emotion,
            'confidence': confidence,
            'agreement': text_emotion == audio_emotion
        }
    elif text:
        results['multimodal_analysis'] = {
            'primary_emotion': results['text_analysis']['emotion'],
            'confidence': results['text_analysis']['confidence'],
            'modality': 'text_only'
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
