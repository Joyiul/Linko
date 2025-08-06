import numpy as np
import pandas as pd
import librosa
import cv2
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow import keras
import pickle
import os
from collections import Counter
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Note: Removing TextBlob to avoid NLTK SSL issues

class ImprovedEmotionAnalyzer:
    def __init__(self):
        """Initialize the improved emotion analyzer with multimodal capabilities"""
        self.facial_model = None
        self.audio_model = None
        self.text_analyzer = SentimentIntensityAnalyzer()
        self.scaler = StandardScaler()
        self.models_loaded = False
        
        # Enhanced emotion mappings
        self.facial_emotions = {
            0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 
            4: 'sad', 5: 'surprise', 6: 'neutral'
        }
        
        # Enhanced audio features for better emotion detection
        self.emotion_audio_features = {
            'happy': {'pitch_mean': 'high', 'energy': 'high', 'tempo': 'fast'},
            'sad': {'pitch_mean': 'low', 'energy': 'low', 'tempo': 'slow'},
            'angry': {'pitch_mean': 'high', 'energy': 'very_high', 'tempo': 'fast'},
            'fear': {'pitch_mean': 'high', 'energy': 'medium', 'tempo': 'variable'},
            'disgust': {'pitch_mean': 'low', 'energy': 'medium', 'tempo': 'slow'},
            'surprise': {'pitch_mean': 'very_high', 'energy': 'high', 'tempo': 'fast'},
            'neutral': {'pitch_mean': 'medium', 'energy': 'medium', 'tempo': 'medium'}
        }
        
        # Enhanced text patterns with context
        self.enhanced_text_patterns = {
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
            }
        }
        
    def extract_enhanced_audio_features(self, audio_path):
        """Extract comprehensive audio features for emotion detection"""
        try:
            # Load audio
            y, sr = librosa.load(audio_path, duration=5.0)
            
            # Basic features
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfcc, axis=1)
            mfcc_std = np.std(mfcc, axis=1)
            
            # Prosodic features (emotion-relevant)
            # Pitch features
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_values = pitches[pitches > 0]
            pitch_mean = np.mean(pitch_values) if len(pitch_values) > 0 else 0
            pitch_std = np.std(pitch_values) if len(pitch_values) > 0 else 0
            
            # Energy features
            rms = librosa.feature.rms(y=y)[0]
            energy_mean = np.mean(rms)
            energy_std = np.std(rms)
            
            # Tempo and rhythm
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            
            # Spectral features
            spectral_centroids = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
            
            # Harmonic and percussive components
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            harmonic_mean = np.mean(y_harmonic**2)
            percussive_mean = np.mean(y_percussive**2)
            
            # Chroma and tonnetz features
            chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr))
            
            # Combine all features
            feature_vector = np.concatenate([
                mfcc_mean, mfcc_std,  # 26 features
                [pitch_mean, pitch_std, energy_mean, energy_std, tempo],  # 5 features
                [spectral_centroids, spectral_rolloff, zero_crossing_rate],  # 3 features
                [harmonic_mean, percussive_mean, chroma, tonnetz]  # 4 features
            ])  # Total: 38 features
            
            return feature_vector
            
        except Exception as e:
            print(f"Error extracting audio features: {e}")
            return np.zeros(38)  # Return zero vector if extraction fails
    
    def analyze_text_sentiment_advanced(self, text):
        """Advanced text sentiment analysis with context awareness"""
        if not text.strip():
            return {'emotion': 'neutral', 'confidence': 0.3, 'details': {}}
        
        # VADER sentiment analysis
        vader_scores = self.text_analyzer.polarity_scores(text)
        
        # Simple polarity analysis (replacing TextBlob)
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'happy', 'joy']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'sad', 'angry', 'disgusting', 'horrible']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Calculate simple polarity
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words > 0:
            polarity = (positive_count - negative_count) / total_sentiment_words
        else:
            polarity = 0
        
        # Enhanced pattern matching
        emotion_scores = {}
        
        for emotion, patterns in self.enhanced_text_patterns.items():
            score = 0
            
            # Keyword matching
            for keyword in patterns['keywords']:
                if keyword in text_lower:
                    score += 1
            
            # Phrase matching (higher weight)
            for phrase in patterns['phrases']:
                if phrase in text_lower:
                    score += 2
            
            # Intensity modifiers
            for keyword in patterns['keywords']:
                if keyword in text_lower:
                    for intensity in patterns['intensity_words']:
                        if intensity in text_lower and abs(text_lower.index(intensity) - text_lower.index(keyword)) < 10:
                            score += 1  # Boost score for intensity modifiers
            
            emotion_scores[emotion] = score
        
        # Determine primary emotion
        if max(emotion_scores.values()) > 0:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(emotion_scores[primary_emotion] * 0.15, 0.9)
        else:
            # Fall back to VADER analysis
            if vader_scores['compound'] >= 0.5:
                primary_emotion = 'happy'
                confidence = vader_scores['compound']
            elif vader_scores['compound'] <= -0.5:
                primary_emotion = 'sad'
                confidence = abs(vader_scores['compound'])
            else:
                primary_emotion = 'neutral'
                confidence = 0.4
        
        return {
            'emotion': primary_emotion,
            'confidence': confidence,
            'details': {
                'vader_scores': vader_scores,
                'polarity': polarity,
                'emotion_scores': emotion_scores
            }
        }
    
    def analyze_facial_emotion_enhanced(self, image_or_frame):
        """Enhanced facial emotion analysis with preprocessing"""
        try:
            # Load facial model if not loaded
            if self.facial_model is None:
                model_path = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained/facial_emotion_model.h5'
                if os.path.exists(model_path):
                    self.facial_model = keras.models.load_model(model_path)
                else:
                    return {'emotion': 'neutral', 'confidence': 0.2, 'error': 'Facial model not found'}
            
            # Preprocess image
            if isinstance(image_or_frame, str):
                image = cv2.imread(image_or_frame)
            else:
                image = image_or_frame
            
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Face detection for better accuracy
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                # Use full image if no face detected
                face_roi = gray
            else:
                # Use the largest face
                largest_face = max(faces, key=lambda x: x[2] * x[3])
                x, y, w, h = largest_face
                face_roi = gray[y:y+h, x:x+w]
            
            # Resize to model input size
            face_resized = cv2.resize(face_roi, (48, 48))
            face_normalized = face_resized.astype('float32') / 255.0
            face_batch = face_normalized.reshape(1, 48, 48, 1)
            
            # Predict emotion
            predictions = self.facial_model.predict(face_batch, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class])
            
            emotion = self.facial_emotions.get(predicted_class, 'neutral')
            
            return {
                'emotion': emotion,
                'confidence': confidence,
                'all_predictions': {self.facial_emotions[i]: float(predictions[0][i]) for i in range(len(self.facial_emotions))}
            }
            
        except Exception as e:
            print(f"Error in facial emotion analysis: {e}")
            return {'emotion': 'neutral', 'confidence': 0.2, 'error': str(e)}
    
    def multimodal_emotion_fusion(self, text_result, audio_features=None, facial_result=None):
        """Intelligent fusion of multimodal emotion analysis"""
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        emotion_scores = {emotion: 0 for emotion in emotions}
        total_weight = 0
        
        # Text analysis (weight: 0.4)
        if text_result and text_result['confidence'] > 0.3:
            text_weight = 0.4 * text_result['confidence']
            emotion_scores[text_result['emotion']] += text_weight
            total_weight += text_weight
        
        # Facial analysis (weight: 0.4)
        if facial_result and facial_result['confidence'] > 0.3:
            facial_weight = 0.4 * facial_result['confidence']
            emotion_scores[facial_result['emotion']] += facial_weight
            total_weight += facial_weight
        
        # Audio analysis (weight: 0.2) - simplified for now
        if audio_features is not None:
            # Basic audio emotion inference based on features
            # This is simplified - in a full implementation, you'd have a trained audio model
            audio_weight = 0.2
            emotion_scores['neutral'] += audio_weight  # Default to neutral for now
            total_weight += audio_weight
        
        # Normalize scores
        if total_weight > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] /= total_weight
        
        # Find the emotion with highest score
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[primary_emotion]
        
        # Apply confidence boosting for consistent results across modalities
        modality_agreement = 0
        if text_result and facial_result:
            if text_result['emotion'] == facial_result['emotion']:
                modality_agreement = 1
                confidence = min(confidence * 1.3, 0.95)  # Boost confidence for agreement
        
        return {
            'primary_emotion': primary_emotion,
            'confidence': confidence,
            'emotion_scores': emotion_scores,
            'modality_agreement': modality_agreement,
            'components': {
                'text': text_result,
                'facial': facial_result,
                'audio': 'processed' if audio_features is not None else None
            }
        }

# Global analyzer instance
improved_analyzer = ImprovedEmotionAnalyzer()

def analyze_multimodal_emotion(text=None, audio_path=None, image_path_or_frame=None):
    """Main function for improved multimodal emotion analysis"""
    try:
        results = {}
        
        # Analyze text
        text_result = None
        if text:
            text_result = improved_analyzer.analyze_text_sentiment_advanced(text)
            results['text_analysis'] = text_result
        
        # Analyze facial emotion
        facial_result = None
        if image_path_or_frame is not None:
            facial_result = improved_analyzer.analyze_facial_emotion_enhanced(image_path_or_frame)
            results['facial_analysis'] = facial_result
        
        # Extract audio features
        audio_features = None
        if audio_path and os.path.exists(audio_path):
            audio_features = improved_analyzer.extract_enhanced_audio_features(audio_path)
            results['audio_features_extracted'] = len(audio_features) > 0
        
        # Perform multimodal fusion
        fusion_result = improved_analyzer.multimodal_emotion_fusion(
            text_result, audio_features, facial_result
        )
        results['multimodal_analysis'] = fusion_result
        
        return results
        
    except Exception as e:
        print(f"Error in multimodal emotion analysis: {e}")
        return {
            'error': str(e),
            'fallback_emotion': 'neutral',
            'fallback_confidence': 0.3
        }
