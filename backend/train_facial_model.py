import os
import numpy as np
import pandas as pd
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
from tensorflow.keras import layers
import pickle
import glob
from pathlib import Path

class FacialFeatureModelTrainer:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.image_size = (224, 224)  # Default size, can be adjusted
        
    def load_dataset_from_directory(self, dataset_path):
        """
        Load dataset from directory structure:
        dataset_path/
        ├── class1/
        │   ├── image1.jpg
        │   └── image2.jpg
        └── class2/
            ├── image3.jpg
            └── image4.jpg
        """
        images = []
        labels = []
        
        try:
            dataset_path = Path(dataset_path)
            
            # Get all subdirectories (classes)
            class_dirs = [d for d in dataset_path.iterdir() if d.is_dir()]
            
            for class_dir in class_dirs:
                class_name = class_dir.name
                
                # Get all image files in this class directory
                image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
                image_files = []
                
                for ext in image_extensions:
                    image_files.extend(class_dir.glob(ext))
                    image_files.extend(class_dir.glob(ext.upper()))
                
                for image_file in image_files:
                    try:
                        # Load and preprocess image
                        image = cv2.imread(str(image_file))
                        if image is not None:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            image = cv2.resize(image, self.image_size)
                            image = image.astype('float32') / 255.0
                            
                            images.append(image)
                            labels.append(class_name)
                            
                    except Exception as e:
                        print(f"Error loading {image_file}: {e}")
                        continue
            
            print(f"Loaded {len(images)} images from {len(set(labels))} classes")
            return np.array(images), np.array(labels)
            
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None, None
    
    def load_dataset_from_csv(self, csv_path, image_column='image_path', label_column='label', image_base_path=''):
        """
        Load dataset from CSV file:
        CSV should have columns: image_path, label
        """
        images = []
        labels = []
        
        try:
            df = pd.read_csv(csv_path)
            
            for _, row in df.iterrows():
                image_path = os.path.join(image_base_path, row[image_column])
                label = row[label_column]
                
                try:
                    # Load and preprocess image
                    image = cv2.imread(image_path)
                    if image is not None:
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        image = cv2.resize(image, self.image_size)
                        image = image.astype('float32') / 255.0
                        
                        images.append(image)
                        labels.append(label)
                        
                except Exception as e:
                    print(f"Error loading {image_path}: {e}")
                    continue
            
            print(f"Loaded {len(images)} images from CSV")
            return np.array(images), np.array(labels)
            
        except Exception as e:
            print(f"Error loading dataset from CSV: {e}")
            return None, None
    
    def create_model(self, num_classes, input_shape=None):
        """Create CNN model for facial feature classification"""
        if input_shape is None:
            input_shape = (*self.image_size, 3)
        
        model = keras.Sequential([
            # First Convolutional Block
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, 2),
            layers.Dropout(0.25),
            
            # Second Convolutional Block
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, 2),
            layers.Dropout(0.25),
            
            # Third Convolutional Block
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, 2),
            layers.Dropout(0.25),
            
            # Fourth Convolutional Block
            layers.Conv2D(256, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, 2),
            layers.Dropout(0.25),
            
            # Dense layers
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_model(self, X, y, test_size=0.2, epochs=50, batch_size=32, validation_split=0.1):
        """Train the facial feature model"""
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        y_categorical = keras.utils.to_categorical(y_encoded)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_categorical, test_size=test_size, random_state=42, stratify=y_categorical
        )
        
        # Create model
        num_classes = len(self.label_encoder.classes_)
        self.model = self.create_model(num_classes)
        
        print("Model Architecture:")
        self.model.summary()
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=5,
                min_lr=1e-6
            )
        ]
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_split=validation_split,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Accuracy: {test_accuracy:.4f}")
        
        return history, test_accuracy
    
    def save_model(self, model_path=None, encoder_path=None):
        """Save trained model and label encoder"""
        try:
            if model_path is None:
                model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained', 'facial_model.h5')
            if encoder_path is None:
                encoder_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained', 'facial_label_encoder.pkl')
            
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Save model
            self.model.save(model_path)
            print(f"Model saved to {model_path}")
            
            # Save label encoder
            with open(encoder_path, 'wb') as f:
                pickle.dump(self.label_encoder, f)
            print(f"Label encoder saved to {encoder_path}")
            
            return True
            
        except Exception as e:
            print(f"Error saving model: {e}")
            return False

def train_facial_model_from_directory(dataset_path, epochs=50, test_size=0.2):
    """Main function to train a facial feature model from directory structure"""
    
    print("Initializing Facial Feature Model Trainer...")
    trainer = FacialFeatureModelTrainer()
    
    # Load dataset
    print("Loading dataset...")
    X, y = trainer.load_dataset_from_directory(dataset_path)
    
    if X is None or len(X) == 0:
        print("No data loaded. Please check your dataset path and structure.")
        return None
    
    # Train model
    print("Training model...")
    history, accuracy = trainer.train_model(X, y, epochs=epochs, test_size=test_size)
    
    # Save model
    print("Saving model...")
    trainer.save_model()
    
    print(f"Training completed! Final test accuracy: {accuracy:.4f}")
    return trainer

def train_facial_model_from_csv(csv_path, image_base_path='', epochs=50, test_size=0.2):
    """Main function to train a facial feature model from CSV file"""
    
    print("Initializing Facial Feature Model Trainer...")
    trainer = FacialFeatureModelTrainer()
    
    # Load dataset
    print("Loading dataset from CSV...")
    X, y = trainer.load_dataset_from_csv(csv_path, image_base_path=image_base_path)
    
    if X is None or len(X) == 0:
        print("No data loaded. Please check your CSV file and image paths.")
        return None
    
    # Train model
    print("Training model...")
    history, accuracy = trainer.train_model(X, y, epochs=epochs, test_size=test_size)
    
    # Save model
    print("Saving model...")
    trainer.save_model()
    
    print(f"Training completed! Final test accuracy: {accuracy:.4f}")
    return trainer

if __name__ == "__main__":
    # Example usage:
    
    # For directory-based dataset:
    # trainer = train_facial_model_from_directory("path/to/your/facial/dataset")
    
    # For CSV-based dataset:
    # trainer = train_facial_model_from_csv("path/to/your/dataset.csv", "path/to/images/")
    
    print("Facial feature model trainer ready!")
    print("Usage examples:")
    print("1. Directory structure: train_facial_model_from_directory('path/to/dataset')")
    print("2. CSV file: train_facial_model_from_csv('dataset.csv', 'images_folder/')")
