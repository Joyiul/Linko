import os
import numpy as np
import pandas as pd
import librosa
# keira was here
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns

# data paths 
audio_dir = 'backend/Datasets/audio_files'
label_csv = 'backend/Datasets/audio_labels.csv' 

# loading
df = pd.read_csv(label_csv)
features = []
labels = []

# extracting features
for _, row in df.iterrows():
    file_path = os.path.join(audio_dir, row['filename'])
    if os.path.exists(file_path):
        y, sr = librosa.load(file_path)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        features.append(mfcc_mean)
        labels.append(row['label'])
    else:
        print(f"File not found: {file_path}")

# preparing for data usage
X = np.array(features)
y_raw = np.array(labels)

# labels
le = LabelEncoder()
y_encoded = le.fit_transform(y_raw)
num_classes = len(le.classes_)
y = to_categorical(y_encoded, num_classes=num_classes)

# k-fold
kf = KFold(n_splits=5, shuffle=True, random_state=42)
acc_scores = []
y_true_all = []
y_pred_all = []

for fold, (train_idx, test_idx) in enumerate(kf.split(X)):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # Define model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X.shape[1],)),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train
    model.fit(X_train, y_train, epochs=20, verbose=0)

    # Evaluate
    _, acc = model.evaluate(X_test, y_test, verbose=0)
    acc_scores.append(acc)
    print(f"Fold {fold+1} Accuracy: {acc:.4f}")

    # Predict for confusion matrix
    y_pred_probs = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred_probs, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    y_pred_all.extend(y_pred_classes)
    y_true_all.extend(y_true_classes)

print(f"\nAverage Accuracy: {np.mean(acc_scores):.4f}")

# Confusion matrix
cm = confusion_matrix(y_true_all, y_pred_all)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()
