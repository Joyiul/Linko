import os
from scipy.io import wavfile
import librosa

audio_dir = 'backend/Datasets/audio_files'

print("Testing all audio files:")
print("=" * 50)

for filename in os.listdir(audio_dir):
    if filename.endswith('.wav'):
        file_path = os.path.join(audio_dir, filename)
        print(f"\nTesting: {filename}")
        
        # Test with scipy first (simpler)
        try:
            sr, y = wavfile.read(file_path)
            print(f"  ✓ Scipy: SR={sr}, Length={len(y)}, Type={y.dtype}")
        except Exception as e:
            print(f"  ✗ Scipy failed: {e}")
            
        # Test with librosa
        try:
            y, sr = librosa.load(file_path, sr=None)
            print(f"  ✓ Librosa: SR={sr}, Length={len(y)}")
        except Exception as e:
            print(f"  ✗ Librosa failed: {type(e).__name__}")
