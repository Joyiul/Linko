import os
import pandas as pd

# Path to audio files
audio_dir = 'backend/Datasets/audio_files'
output_csv = 'backend/Datasets/audio_labels.csv'

data = []

# Loop through audio files
for filename in os.listdir(audio_dir):
    if filename.endswith('.wav'):
        #change the file name into label
        label = filename.split('_')[-1].replace('.wav', '')
        data.append({'filename': filename, 'label': label})

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv(output_csv, index=False)
print(f"Saved labels to {output_csv}")
