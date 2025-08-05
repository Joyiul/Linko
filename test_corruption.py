import os
from scipy.io import wavfile
import librosa

audio_dir = 'backend/Datasets/audio_files'

print("Testing all audio files:")
print("=" * 60)

corrupted_files = []
working_files = []

for filename in sorted(os.listdir(audio_dir)):
    if filename.endswith('.wav'):
        file_path = os.path.join(audio_dir, filename)
        
        # Test with scipy first (simpler)
        scipy_works = False
        librosa_works = False
        
        try:
            sr, y = wavfile.read(file_path)
            scipy_works = True
        except Exception as e:
            pass
            
        # Test with librosa
        try:
            y, sr = librosa.load(file_path, sr=None)
            librosa_works = True
        except Exception as e:
            pass
        
        if scipy_works and librosa_works:
            print(f"✓ {filename}")
            working_files.append(filename)
        else:
            print(f"✗ {filename} - CORRUPTED")
            corrupted_files.append(filename)

print("\n" + "=" * 60)
print(f"Working files: {len(working_files)}")
print(f"Corrupted files: {len(corrupted_files)}")

if corrupted_files:
    print("\nCorrupted files that need to be replaced:")
    for f in corrupted_files:
        print(f"  - {f}")
