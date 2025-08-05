import librosa
import os
import numpy as np

# Test loading one audio file
audio_dir = 'backend/Datasets/audio_files'
test_file = 'OAF_back_neutral.wav'
file_path = os.path.join(audio_dir, test_file)

print(f"Testing file: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")

try:
    # Try different loading methods
    print("Attempting to load with librosa...")
    y, sr = librosa.load(file_path, sr=None)
    print(f"Success! Sample rate: {sr}, Length: {len(y)}")
    print(f"Audio data shape: {y.shape}")
    print(f"Audio data type: {y.dtype}")
    print(f"Audio data range: {np.min(y)} to {np.max(y)}")
    
except Exception as e:
    print(f"Failed to load with librosa: {e}")
    print(f"Error type: {type(e)}")
    
    # Try with different parameters
    try:
        print("Trying with specific sr=22050...")
        y, sr = librosa.load(file_path, sr=22050)
        print(f"Success with sr=22050! Sample rate: {sr}, Length: {len(y)}")
    except Exception as e2:
        print(f"Also failed with sr=22050: {e2}")
        
        # Try scipy if available
        try:
            from scipy.io import wavfile
            print("Trying with scipy.io.wavfile...")
            sr, y = wavfile.read(file_path)
            print(f"Success with scipy! Sample rate: {sr}, Length: {len(y)}")
            print(f"Data type: {y.dtype}")
        except Exception as e3:
            print(f"Also failed with scipy: {e3}")
