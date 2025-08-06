#!/usr/bin/env python3
"""
Quick training script for facial emotion recognition model
This uses a small subset for fast development and testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from train_facial_emotion_model import train_facial_emotion_model, k_fold_evaluation

def quick_train():
    """Train a model with a small subset for testing"""
    print("🎭 Quick Facial Emotion Model Training")
    print("=" * 50)
    print("This will train on a small subset (100 images per class) for testing")
    print("For full training, use the main training script")
    
    try:
        # Train with small subset
        model, le, history, accuracy = train_facial_emotion_model(
            use_full_dataset=False, 
            max_images_per_class=100
        )
        
        print(f"\n✅ Training completed successfully!")
        print(f"📊 Final Test Accuracy: {accuracy:.4f}")
        print(f"🎯 Emotion classes: {list(le.classes_)}")
        print("\n🔄 Model and encoder saved to /models/trained/")
        
        return model, le
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return None, None

def test_trained_model():
    """Test the trained model on a sample image"""
    try:
        from processing.facial_analysis import facial_analyzer
        
        # Try to load the model
        success = facial_analyzer.load_model()
        if success:
            print("✅ Model loaded successfully!")
            
            # Test with a sample image
            test_image_path = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/archive/test/happy"
            test_images = os.listdir(test_image_path)
            if test_images:
                sample_image = os.path.join(test_image_path, test_images[0])
                result = facial_analyzer.predict_facial_features(sample_image)
                print(f"🧪 Test prediction: {result}")
            else:
                print("No test images found")
        else:
            print("❌ Model loading failed")
            
    except Exception as e:
        print(f"❌ Testing failed: {e}")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Quick training (small subset)")
    print("2. Test existing model")
    print("3. Both (train then test)")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        quick_train()
    elif choice == "2":
        test_trained_model()
    elif choice == "3":
        model, le = quick_train()
        if model is not None:
            print("\n" + "="*30)
            test_trained_model()
    else:
        print("Starting quick training (default)...")
        quick_train()
