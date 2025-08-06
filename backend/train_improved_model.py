import os
import numpy as np
import pandas as pd
import librosa
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

def train_improved_emotion_model():
    """
    Train an improved emotion detection model with the augmented dataset
    """
    print("🎯 Training Improved Emotion Detection Model")
    
    # Use the augmented dataset
    audio_dir = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files_augmented'
    label_csv = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_labels_augmented.csv'
    
    # Load labels
    df = pd.read_csv(label_csv)
    print(f"📊 Dataset size: {len(df)} samples")
    print(f"📈 Label distribution:\n{df['label'].value_counts()}")
    
    # Extract features
    features = []
    labels = []
    failed_files = 0
    
    print("\n🎵 Extracting audio features...")
    for idx, row in df.iterrows():
        if idx % 50 == 0:
            print(f"Progress: {idx}/{len(df)} ({idx/len(df)*100:.1f}%)")
            
        file_path = os.path.join(audio_dir, row['filename'])
        if os.path.exists(file_path):
            try:
                # Load audio
                y, sr = librosa.load(file_path, duration=3.0)  # Limit to 3 seconds
                
                # Extract multiple features
                # 1. MFCC features (13 coefficients)
                mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                mfcc_mean = np.mean(mfcc, axis=1)
                mfcc_std = np.std(mfcc, axis=1)
                
                # 2. Spectral features
                spectral_centroids = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
                spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
                zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
                
                # 3. Chroma features
                chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))
                
                # 4. Spectral contrast
                spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr))
                
                # Combine all features
                feature_vector = np.concatenate([
                    mfcc_mean,           # 13 features
                    mfcc_std,            # 13 features  
                    [spectral_centroids, spectral_rolloff, zero_crossing_rate, 
                     chroma, spectral_contrast]  # 5 features
                ])
                
                features.append(feature_vector)
                labels.append(row['label'])
                
            except Exception as e:
                failed_files += 1
                if failed_files <= 5:  # Only print first 5 errors
                    print(f"❌ Error processing {row['filename']}: {e}")
                continue
        else:
            failed_files += 1
    
    print(f"✅ Successfully processed: {len(features)} files")
    print(f"❌ Failed to process: {failed_files} files")
    
    if len(features) == 0:
        print("❌ No features extracted! Check your audio files.")
        return
    
    # Prepare data
    X = np.array(features)
    y_raw = np.array(labels)
    
    print(f"📊 Feature shape: {X.shape}")
    print(f"📊 Unique labels: {np.unique(y_raw)}")
    
    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_raw)
    num_classes = len(le.classes_)
    y = to_categorical(y_encoded, num_classes=num_classes)
    
    print(f"📊 Number of classes: {num_classes}")
    print(f"📊 Classes: {le.classes_}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"📊 Training samples: {len(X_train)}")
    print(f"📊 Testing samples: {len(X_test)}")
    
    # Build improved model
    model = Sequential([
        Dense(128, activation='relu', input_shape=(X.shape[1],)),
        BatchNormalization(),
        Dropout(0.3),
        
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        
        Dense(32, activation='relu'),
        BatchNormalization(),
        Dropout(0.2),
        
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"\n🧠 Model Architecture:")
    model.summary()
    
    # Callbacks for better training
    callbacks = [
        EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.0001)
    ]
    
    # Train model
    print(f"\n🏋️ Training model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=100,
        batch_size=32,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate model
    print(f"\n📊 Evaluating model...")
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"🎯 Test Accuracy: {test_accuracy:.4f}")
    print(f"📉 Test Loss: {test_loss:.4f}")
    
    # Predictions for detailed analysis
    y_pred_probs = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred_probs, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    
    # Classification report
    print(f"\n📈 Classification Report:")
    print(classification_report(y_true_classes, y_pred_classes, target_names=le.classes_))
    
    # Confusion matrix
    cm = confusion_matrix(y_true_classes, y_pred_classes)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=le.classes_, yticklabels=le.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Improved Emotion Detection - Confusion Matrix')
    plt.tight_layout()
    plt.savefig('/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/confusion_matrix_improved.png')
    plt.show()
    
    # Save model and encoders
    model_dir = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/models/trained'
    os.makedirs(model_dir, exist_ok=True)
    
    model.save(os.path.join(model_dir, 'emotion_model_improved.h5'))
    joblib.dump(le, os.path.join(model_dir, 'label_encoder.pkl'))
    
    print(f"\n💾 Model saved to: {model_dir}")
    print(f"🎉 Training complete! Accuracy improved from ~50% to {test_accuracy:.1%}")
    
    return model, le, test_accuracy

if __name__ == "__main__":
    train_improved_emotion_model()
