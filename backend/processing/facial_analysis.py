import numpy as np
import pandas as pd
import cv2
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import os

class FacialFeatureAnalyzer:
    def __init__(self):
        """Initialize facial feature analyzer"""
        self.model = None
        self.label_encoder = None
        self.model_loaded = False
        
    def load_model(self, model_path=None, encoder_path=None):
        """Load pre-trained facial feature model"""
        try:
            if model_path is None:
                model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained', 'facial_model.h5')
            if encoder_path is None:
                encoder_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained', 'facial_label_encoder.pkl')
            
            # Load the model
            if os.path.exists(model_path):
                self.model = keras.models.load_model(model_path)
                print(f"Loaded facial model from {model_path}")
            
            # Load label encoder
            if os.path.exists(encoder_path):
                import pickle
                with open(encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                print(f"Loaded facial label encoder from {encoder_path}")
            
            self.model_loaded = True
            return True
            
        except Exception as e:
            print(f"Error loading facial model: {e}")
            return False
    
    def extract_facial_features(self, image_path_or_array):
        """Extract facial features from image"""
        try:
            # Load image if path is provided
            if isinstance(image_path_or_array, str):
                image = cv2.imread(image_path_or_array)
                if image is None:
                    return None
            else:
                image = image_path_or_array
            
            # Convert to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize to model input size (adjust based on your model requirements)
            image_resized = cv2.resize(image, (224, 224))  # Common size for CNN models
            
            # Normalize pixel values
            image_normalized = image_resized.astype('float32') / 255.0
            
            # Add batch dimension
            image_batch = np.expand_dims(image_normalized, axis=0)
            
            return image_batch
            
        except Exception as e:
            print(f"Error extracting facial features: {e}")
            return None
    
    def predict_facial_features(self, image_path_or_array):
        """Predict facial features/emotions from image"""
        if not self.model_loaded:
            if not self.load_model():
                return {"error": "Model not loaded"}
        
        # Extract features
        features = self.extract_facial_features(image_path_or_array)
        if features is None:
            return {"error": "Could not extract features from image"}
        
        try:
            # Make prediction
            predictions = self.model.predict(features)
            
            # Get the predicted class
            if self.label_encoder:
                predicted_class_idx = np.argmax(predictions[0])
                predicted_class = self.label_encoder.inverse_transform([predicted_class_idx])[0]
                confidence = float(predictions[0][predicted_class_idx])
            else:
                # If no label encoder, return raw predictions
                predicted_class = f"class_{np.argmax(predictions[0])}"
                confidence = float(np.max(predictions[0]))
            
            return {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "all_predictions": predictions[0].tolist()
            }
            
        except Exception as e:
            print(f"Error making prediction: {e}")
            return {"error": f"Prediction failed: {str(e)}"}
    
    def analyze_facial_video_frame(self, frame):
        """Analyze a single video frame for facial features"""
        return self.predict_facial_features(frame)

# Global analyzer instance
facial_analyzer = FacialFeatureAnalyzer()

def analyze_facial_features(image_path_or_array):
    """Main function to analyze facial features"""
    return facial_analyzer.predict_facial_features(image_path_or_array)

def process_facial_dataset(dataset_path, output_path=None):
    """Process a facial feature dataset and extract features"""
    try:
        # Implementation depends on your dataset format
        # This is a template that you can customize
        
        if os.path.isdir(dataset_path):
            # Directory of images
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
                image_files.extend(glob.glob(os.path.join(dataset_path, ext)))
            
            results = []
            for image_file in image_files:
                result = analyze_facial_features(image_file)
                if "error" not in result:
                    results.append({
                        "filename": os.path.basename(image_file),
                        "predicted_class": result["predicted_class"],
                        "confidence": result["confidence"]
                    })
            
            # Save results
            if output_path and results:
                df = pd.DataFrame(results)
                df.to_csv(output_path, index=False)
                print(f"Processed {len(results)} images, saved to {output_path}")
            
            return results
            
    except Exception as e:
        print(f"Error processing facial dataset: {e}")
        return []
