"""
Multimodal Analysis combining Audio and Facial Emotion Recognition
This integrates your audio_files_model.py approach with facial emotion analysis
"""

import os
import numpy as np
import pandas as pd
import cv2
import librosa
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from tensorflow.keras.utils import to_categorical
import pickle

class MultimodalEmotionAnalyzer:
    def __init__(self):
        self.audio_model = None
        self.facial_model = None
        self.audio_le = None
        self.facial_le = None
        self.models_loaded = False
        
    def load_models(self):
        """Load both audio and facial emotion models"""
        try:
            # Load audio model (if exists)
            audio_model_path = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained/emotion_model_improved.h5'
            audio_encoder_path = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained/label_encoder.pkl'
            
            if os.path.exists(audio_model_path):
                self.audio_model = load_model(audio_model_path)
                print("✅ Audio emotion model loaded")
                
                if os.path.exists(audio_encoder_path):
                    with open(audio_encoder_path, 'rb') as f:
                        self.audio_le = pickle.load(f)
                    print("✅ Audio label encoder loaded")
            
            # Load facial model
            facial_model_path = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained/facial_emotion_model.h5'
            facial_encoder_path = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained/facial_label_encoder.pkl'
            
            if os.path.exists(facial_model_path):
                self.facial_model = load_model(facial_model_path)
                print("✅ Facial emotion model loaded")
                
                if os.path.exists(facial_encoder_path):
                    with open(facial_encoder_path, 'rb') as f:
                        self.facial_le = pickle.load(f)
                    print("✅ Facial label encoder loaded")
            
            self.models_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False
    
    def extract_audio_features(self, audio_path):
        """Extract MFCC features from audio (similar to your audio_files_model.py)"""
        try:
            y, sr = librosa.load(audio_path)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfcc, axis=1)
            return mfcc_mean.reshape(1, -1)
        except Exception as e:
            print(f"Error extracting audio features: {e}")
            return None
    
    def extract_facial_features(self, image_path):
        """Extract facial features from image"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Convert to grayscale and resize to 48x48
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (48, 48))
            image = image.astype('float32') / 255.0
            
            # Reshape for CNN
            image = image.reshape(1, 48, 48, 1)
            return image
            
        except Exception as e:
            print(f"Error extracting facial features: {e}")
            return None
    
    def predict_audio_emotion(self, audio_path):
        """Predict emotion from audio"""
        if self.audio_model is None:
            return None
        
        features = self.extract_audio_features(audio_path)
        if features is None:
            return None
        
        try:
            prediction = self.audio_model.predict(features)
            predicted_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_idx])
            
            if self.audio_le:
                emotion = self.audio_le.inverse_transform([predicted_idx])[0]
            else:
                emotion = f"emotion_{predicted_idx}"
            
            return {
                'emotion': emotion,
                'confidence': confidence,
                'probabilities': prediction[0].tolist()
            }
            
        except Exception as e:
            print(f"Error predicting audio emotion: {e}")
            return None
    
    def predict_facial_emotion(self, image_path):
        """Predict emotion from facial image"""
        if self.facial_model is None:
            return None
        
        features = self.extract_facial_features(image_path)
        if features is None:
            return None
        
        try:
            prediction = self.facial_model.predict(features)
            predicted_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_idx])
            
            if self.facial_le:
                emotion = self.facial_le.inverse_transform([predicted_idx])[0]
            else:
                emotion = f"emotion_{predicted_idx}"
            
            return {
                'emotion': emotion,
                'confidence': confidence,
                'probabilities': prediction[0].tolist()
            }
            
        except Exception as e:
            print(f"Error predicting facial emotion: {e}")
            return None
    
    def multimodal_analysis(self, audio_path=None, image_path=None, fusion_method='weighted_average'):
        """
        Perform multimodal emotion analysis
        fusion_method: 'weighted_average', 'max_confidence', 'voting'
        """
        results = {
            'audio_analysis': None,
            'facial_analysis': None,
            'multimodal_prediction': None
        }
        
        # Analyze audio
        if audio_path and self.audio_model:
            results['audio_analysis'] = self.predict_audio_emotion(audio_path)
        
        # Analyze facial
        if image_path and self.facial_model:
            results['facial_analysis'] = self.predict_facial_emotion(image_path)
        
        # Fusion strategy
        if results['audio_analysis'] and results['facial_analysis']:
            audio_emotion = results['audio_analysis']['emotion']
            facial_emotion = results['facial_analysis']['emotion']
            audio_conf = results['audio_analysis']['confidence']
            facial_conf = results['facial_analysis']['confidence']
            
            if fusion_method == 'max_confidence':
                if audio_conf >= facial_conf:
                    final_emotion = audio_emotion
                    final_conf = audio_conf
                    dominant_modality = 'audio'
                else:
                    final_emotion = facial_emotion
                    final_conf = facial_conf
                    dominant_modality = 'facial'
                    
            elif fusion_method == 'voting':
                if audio_emotion == facial_emotion:
                    final_emotion = audio_emotion
                    final_conf = (audio_conf + facial_conf) / 2
                    dominant_modality = 'both_agree'
                else:
                    if audio_conf >= facial_conf:
                        final_emotion = audio_emotion
                        final_conf = audio_conf
                        dominant_modality = 'audio'
                    else:
                        final_emotion = facial_emotion
                        final_conf = facial_conf
                        dominant_modality = 'facial'
            
            else:  # weighted_average (default)
                # Simple weighted average based on confidence
                total_weight = audio_conf + facial_conf
                if total_weight > 0:
                    if audio_conf >= facial_conf:
                        final_emotion = audio_emotion
                        final_conf = audio_conf
                        dominant_modality = 'audio'
                    else:
                        final_emotion = facial_emotion  
                        final_conf = facial_conf
                        dominant_modality = 'facial'
                else:
                    final_emotion = 'neutral'
                    final_conf = 0.5
                    dominant_modality = 'fallback'
            
            results['multimodal_prediction'] = {
                'final_emotion': final_emotion,
                'confidence': final_conf,
                'dominant_modality': dominant_modality,
                'agreement': audio_emotion == facial_emotion,
                'fusion_method': fusion_method
            }
        
        elif results['audio_analysis']:
            results['multimodal_prediction'] = {
                'final_emotion': results['audio_analysis']['emotion'],
                'confidence': results['audio_analysis']['confidence'],
                'dominant_modality': 'audio_only',
                'agreement': None,
                'fusion_method': 'single_modality'
            }
        
        elif results['facial_analysis']:
            results['multimodal_prediction'] = {
                'final_emotion': results['facial_analysis']['emotion'],
                'confidence': results['facial_analysis']['confidence'],
                'dominant_modality': 'facial_only',
                'agreement': None,
                'fusion_method': 'single_modality'
            }
        
        return results

def test_multimodal_analysis():
    """Test the multimodal emotion analyzer"""
    print("🤖 Testing Multimodal Emotion Analysis")
    print("=" * 50)
    
    analyzer = MultimodalEmotionAnalyzer()
    
    # Load models
    if not analyzer.load_models():
        print("❌ Failed to load models")
        return
    
    # Test paths (adjust to your actual test files)
    test_audio_path = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files"
    test_image_path = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/archive/test/happy"
    
    # Get a sample audio file
    audio_files = [f for f in os.listdir(test_audio_path) if f.endswith('.wav')][:1]
    image_files = [f for f in os.listdir(test_image_path) if f.endswith('.jpg')][:1]
    
    if audio_files and image_files:
        audio_file = os.path.join(test_audio_path, audio_files[0])
        image_file = os.path.join(test_image_path, image_files[0])
        
        print(f"🎵 Testing audio: {audio_files[0]}")
        print(f"🖼️  Testing image: {image_files[0]}")
        
        # Perform multimodal analysis
        results = analyzer.multimodal_analysis(
            audio_path=audio_file,
            image_path=image_file,
            fusion_method='max_confidence'
        )
        
        print("\n📊 Results:")
        print("-" * 30)
        
        if results['audio_analysis']:
            print(f"🎵 Audio Emotion: {results['audio_analysis']['emotion']} "
                  f"(confidence: {results['audio_analysis']['confidence']:.3f})")
        
        if results['facial_analysis']:
            print(f"😊 Facial Emotion: {results['facial_analysis']['emotion']} "
                  f"(confidence: {results['facial_analysis']['confidence']:.3f})")
        
        if results['multimodal_prediction']:
            mp = results['multimodal_prediction']
            print(f"\n🎯 Final Prediction: {mp['final_emotion']} "
                  f"(confidence: {mp['confidence']:.3f})")
            print(f"🔄 Dominant Modality: {mp['dominant_modality']}")
            print(f"🤝 Agreement: {mp['agreement']}")
    
    else:
        print("❌ No test files found")

if __name__ == "__main__":
    test_multimodal_analysis()
