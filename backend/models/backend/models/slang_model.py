import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow import keras

df = pd.read_csv('backend/Datasets/slang.csv')

#original features from the dataset
X_raw = df['word']  
y_raw = df['label']  

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y_raw)

#number of classes 
num_classes = len(le.classes_)

# vectorizing the text
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X_raw).toarray()

#creating arrays for training and testing
X = X_vectorized
y = keras.utils.to_categorical(y_encoded, num_classes=num_classes)

#k-fold cross-validation 
kf = KFold(n_splits=5, shuffle=True, random_state=42)
acc_scores = []
y_true_all = []
y_pred_all = []

# looping through each fold
for fold, (train_idx, test_idx) in enumerate(kf.split(X)):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # Define model
    model = keras.Sequential([
        keras.layers.Input(shape=(X_train.shape[1],)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train
    model.fit(X_train, y_train, epochs=20, verbose=0)

    # Evaluate
    _, acc = model.evaluate(X_test, y_test, verbose=0)
    acc_scores.append(acc)
    print(f"Fold {fold+1} Accuracy: {acc:.4f}")

    # Predict
    y_pred_probs = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred_probs, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)

    # Collect for confusion matrix
    y_pred_all.extend(y_pred_classes)
    y_true_all.extend(y_true_classes)

# Average accuracy
print(f"\nAverage Accuracy: {np.mean(acc_scores):.4f}")

# Confusion matrix
cm = confusion_matrix(y_true_all, y_pred_all)

# Print
print("\nConfusion Matrix:")
print(cm)

# Plot
plt.figure(figsize=(10, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix Heatmap')
plt.show()

print("Total predictions counted in confusion matrix:", cm.sum())
print("Total number of test samples:", len(y_true_all))