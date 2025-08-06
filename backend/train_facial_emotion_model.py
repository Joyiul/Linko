import os
import numpy as np
import pandas as pd
import cv2
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import pickle

# Data paths
train_dir = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/archive/train'
test_dir = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/archive/test'
model_save_path = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained/facial_emotion_model.h5'
encoder_save_path = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained/facial_label_encoder.pkl'

# Image parameters
IMG_HEIGHT = 48
IMG_WIDTH = 48
BATCH_SIZE = 32
EPOCHS = 50

def load_images_and_labels(data_dir, max_images_per_class=None):
    """Load images and labels from directory structure"""
    images = []
    labels = []
    
    emotion_folders = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    
    for emotion in emotion_folders:
        emotion_path = os.path.join(data_dir, emotion)
        if os.path.exists(emotion_path):
            image_files = [f for f in os.listdir(emotion_path) if f.lower().endswith('.jpg')]
            
            # Limit images per class if specified (for faster training during development)
            if max_images_per_class:
                image_files = image_files[:max_images_per_class]
            
            print(f"Loading {len(image_files)} images from {emotion} folder...")
            
            for img_file in image_files:
                img_path = os.path.join(emotion_path, img_file)
                try:
                    # Load and preprocess image
                    img = cv2.imread(img_path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
                        img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                        img = img.astype('float32') / 255.0  # Normalize
                        
                        images.append(img)
                        labels.append(emotion)
                        
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")
                    continue
    
    return np.array(images), np.array(labels)

def create_cnn_model(num_classes, input_shape=(IMG_HEIGHT, IMG_WIDTH, 1)):
    """Create CNN model for facial emotion recognition"""
    model = Sequential([
        # First Convolutional Block
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        BatchNormalization(),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Dropout(0.25),
        
        # Second Convolutional Block
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Dropout(0.25),
        
        # Third Convolutional Block
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        Dropout(0.25),
        
        # Dense layers
        Flatten(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_facial_emotion_model(use_full_dataset=False, max_images_per_class=1000):
    """Train facial emotion recognition model similar to audio model structure"""
    print("Loading facial emotion dataset...")
    
    # Load training data
    if use_full_dataset:
        X_train, y_train_raw = load_images_and_labels(train_dir)
        X_test, y_test_raw = load_images_and_labels(test_dir)
    else:
        # Use subset for faster development/testing
        X_train, y_train_raw = load_images_and_labels(train_dir, max_images_per_class)
        X_test, y_test_raw = load_images_and_labels(test_dir, max_images_per_class//4)
    
    print(f"Loaded {len(X_train)} training images and {len(X_test)} test images")
    
    # Reshape for CNN (add channel dimension)
    X_train = X_train.reshape(X_train.shape[0], IMG_HEIGHT, IMG_WIDTH, 1)
    X_test = X_test.reshape(X_test.shape[0], IMG_HEIGHT, IMG_WIDTH, 1)
    
    # Encode labels
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train_raw)
    y_test_encoded = le.transform(y_test_raw)
    
    num_classes = len(le.classes_)
    y_train = to_categorical(y_train_encoded, num_classes=num_classes)
    y_test = to_categorical(y_test_encoded, num_classes=num_classes)
    
    print(f"Emotion classes: {list(le.classes_)}")
    print(f"Number of classes: {num_classes}")
    
    # Data augmentation
    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Create model
    model = create_cnn_model(num_classes)
    print("\nModel Architecture:")
    model.summary()
    
    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-6)
    ]
    
    # Train model
    print("\nStarting training...")
    history = model.fit(
        datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_test, y_test),
        callbacks=callbacks,
        verbose=1
    )
    
    # Final evaluation
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nFinal Test Accuracy: {test_accuracy:.4f}")
    
    # Confusion matrix
    y_pred_probs = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred_probs, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    
    cm = confusion_matrix(y_true_classes, y_pred_classes)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=le.classes_, yticklabels=le.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Facial Emotion Recognition - Confusion Matrix')
    plt.tight_layout()
    plt.savefig('/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained/facial_confusion_matrix.png')
    plt.show()
    
    # Save model and label encoder
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")
    
    with open(encoder_save_path, 'wb') as f:
        pickle.dump(le, f)
    print(f"Label encoder saved to {encoder_save_path}")
    
    return model, le, history, test_accuracy

def k_fold_evaluation(max_images_per_class=500):
    """Perform K-fold cross validation similar to the audio model"""
    print("Performing K-fold cross validation on facial emotion dataset...")
    
    # Load combined dataset
    X_train, y_train_raw = load_images_and_labels(train_dir, max_images_per_class)
    X_test, y_test_raw = load_images_and_labels(test_dir, max_images_per_class//4)
    
    # Combine train and test for k-fold
    X = np.concatenate([X_train, X_test])
    y_raw = np.concatenate([y_train_raw, y_test_raw])
    
    # Reshape for CNN
    X = X.reshape(X.shape[0], IMG_HEIGHT, IMG_WIDTH, 1)
    
    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_raw)
    num_classes = len(le.classes_)
    y = to_categorical(y_encoded, num_classes=num_classes)
    
    print(f"Dataset size: {len(X)} images")
    print(f"Emotion classes: {list(le.classes_)}")
    
    # K-fold cross validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    acc_scores = []
    y_true_all = []
    y_pred_all = []
    
    for fold, (train_idx, test_idx) in enumerate(kf.split(X)):
        print(f"\nTraining Fold {fold+1}/5...")
        
        X_train_fold, X_test_fold = X[train_idx], X[test_idx]
        y_train_fold, y_test_fold = y[train_idx], y[test_idx]
        
        # Create model for this fold
        model = create_cnn_model(num_classes)
        
        # Train with early stopping
        early_stop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)
        
        model.fit(X_train_fold, y_train_fold, 
                 epochs=20, 
                 validation_data=(X_test_fold, y_test_fold),
                 callbacks=[early_stop],
                 verbose=0)
        
        # Evaluate
        _, acc = model.evaluate(X_test_fold, y_test_fold, verbose=0)
        acc_scores.append(acc)
        print(f"Fold {fold+1} Accuracy: {acc:.4f}")
        
        # Collect predictions for confusion matrix
        y_pred_probs = model.predict(X_test_fold, verbose=0)
        y_pred_classes = np.argmax(y_pred_probs, axis=1)
        y_true_classes = np.argmax(y_test_fold, axis=1)
        y_pred_all.extend(y_pred_classes)
        y_true_all.extend(y_true_classes)
    
    print(f"\nAverage Accuracy across 5 folds: {np.mean(acc_scores):.4f} ± {np.std(acc_scores):.4f}")
    
    # Overall confusion matrix
    cm = confusion_matrix(y_true_all, y_pred_all)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=le.classes_, yticklabels=le.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('K-Fold Cross Validation - Confusion Matrix')
    plt.tight_layout()
    plt.savefig('/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained/facial_kfold_confusion_matrix.png')
    plt.show()
    
    return acc_scores, le

if __name__ == "__main__":
    print("Facial Emotion Recognition Model Training")
    print("=" * 50)
    
    # Choice of training method
    choice = input("Choose training method:\n1. Full dataset training\n2. Subset training (faster)\n3. K-fold validation\nEnter choice (1-3): ")
    
    if choice == "1":
        print("Training on full dataset...")
        model, le, history, accuracy = train_facial_emotion_model(use_full_dataset=True)
    elif choice == "2":
        print("Training on subset for development...")
        model, le, history, accuracy = train_facial_emotion_model(use_full_dataset=False, max_images_per_class=1000)
    elif choice == "3":
        print("Performing K-fold cross validation...")
        acc_scores, le = k_fold_evaluation(max_images_per_class=500)
    else:
        print("Training on subset (default)...")
        model, le, history, accuracy = train_facial_emotion_model(use_full_dataset=False, max_images_per_class=1000)
