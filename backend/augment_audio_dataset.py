import os
import librosa
import soundfile as sf
import numpy as np
import pandas as pd
from pathlib import Path

def augment_audio(audio_path, output_dir, base_filename):
    """
    Augment a single audio file with multiple variations
    """
    try:
        # Load the audio file
        y, sr = librosa.load(audio_path)
        
        augmented_files = []
        
        # Original file
        original_name = f"{base_filename}_original.wav"
        sf.write(os.path.join(output_dir, original_name), y, sr)
        augmented_files.append(original_name)
        
        # 1. Pitch shifting variations
        for pitch_shift in [-2, -1, 1, 2]:  # semitones
            y_pitch = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_shift)
            pitch_name = f"{base_filename}_pitch{pitch_shift:+d}.wav"
            sf.write(os.path.join(output_dir, pitch_name), y_pitch, sr)
            augmented_files.append(pitch_name)
        
        # 2. Speed variations
        for speed in [0.8, 0.9, 1.1, 1.2]:
            y_speed = librosa.effects.time_stretch(y, rate=speed)
            speed_name = f"{base_filename}_speed{speed:.1f}.wav"
            sf.write(os.path.join(output_dir, speed_name), y_speed, sr)
            augmented_files.append(speed_name)
        
        # 3. Add subtle noise
        for noise_level in [0.005, 0.01]:
            noise = np.random.normal(0, noise_level, len(y))
            y_noise = y + noise
            # Normalize to prevent clipping
            y_noise = y_noise / np.max(np.abs(y_noise))
            noise_name = f"{base_filename}_noise{noise_level:.3f}.wav"
            sf.write(os.path.join(output_dir, noise_name), y_noise, sr)
            augmented_files.append(noise_name)
        
        # 4. Volume variations
        for volume in [0.7, 1.3]:
            y_vol = y * volume
            # Normalize to prevent clipping
            y_vol = np.clip(y_vol, -1.0, 1.0)
            vol_name = f"{base_filename}_vol{volume:.1f}.wav"
            sf.write(os.path.join(output_dir, vol_name), y_vol, sr)
            augmented_files.append(vol_name)
        
        return augmented_files
        
    except Exception as e:
        print(f"Error augmenting {audio_path}: {e}")
        return []

def augment_dataset():
    """
    Augment the entire audio dataset
    """
    # Paths
    original_audio_dir = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files"
    augmented_audio_dir = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files_augmented"
    labels_csv = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_labels.csv"
    
    # Create augmented directory
    os.makedirs(augmented_audio_dir, exist_ok=True)
    
    # Load original labels
    df = pd.read_csv(labels_csv)
    
    # New augmented labels list
    augmented_labels = []
    
    print("🎵 Starting audio dataset augmentation...")
    
    total_files = len(df)
    for idx, row in df.iterrows():
        filename = row['filename']
        label = row['label']
        
        print(f"📁 Processing {idx+1}/{total_files}: {filename}")
        
        # Original file path
        original_path = os.path.join(original_audio_dir, filename)
        
        if not os.path.exists(original_path):
            print(f"❌ File not found: {original_path}")
            continue
        
        # Base filename without extension
        base_filename = os.path.splitext(filename)[0]
        
        # Augment the audio file
        augmented_files = augment_audio(original_path, augmented_audio_dir, base_filename)
        
        # Add labels for all augmented files
        for aug_file in augmented_files:
            augmented_labels.append({
                'filename': aug_file,
                'label': label,
                'original_file': filename
            })
        
        print(f"✅ Created {len(augmented_files)} variations")
    
    # Save augmented labels
    augmented_df = pd.DataFrame(augmented_labels)
    augmented_csv_path = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_labels_augmented.csv"
    augmented_df.to_csv(augmented_csv_path, index=False)
    
    print(f"\n🎉 Augmentation complete!")
    print(f"📊 Original dataset: {len(df)} files")
    print(f"📊 Augmented dataset: {len(augmented_df)} files")
    print(f"📊 Improvement factor: {len(augmented_df) / len(df):.1f}x")
    print(f"💾 Augmented files saved to: {augmented_audio_dir}")
    print(f"📝 Augmented labels saved to: {augmented_csv_path}")
    
    # Show label distribution
    print(f"\n📈 Label distribution in augmented dataset:")
    print(augmented_df['label'].value_counts().sort_index())

if __name__ == "__main__":
    augment_dataset()
