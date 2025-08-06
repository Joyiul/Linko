#!/bin/bash

# 🛡️ Audio Dataset Protection Script
# This script creates backups and validates audio files to prevent corruption

AUDIO_DIR="/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files"
BACKUP_DIR="/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_backup_$(date +%Y%m%d_%H%M%S)"
LABELS_FILE="/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_labels.csv"

echo "🛡️ Starting Audio Dataset Protection..."

# 1. Create timestamped backup
echo "📁 Creating backup at: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
cp -r "$AUDIO_DIR"/* "$BACKUP_DIR/"
echo "✅ Backup created with $(find "$BACKUP_DIR" -name "*.wav" | wc -l) audio files"

# 2. Validate audio file integrity
echo "🔍 Validating audio file integrity..."
corrupted_files=0
total_files=0

for wav_file in "$AUDIO_DIR"/*.wav; do
    if [ -f "$wav_file" ]; then
        total_files=$((total_files + 1))
        
        # Check if file size is reasonable (>1KB and <100MB)
        file_size=$(stat -f%z "$wav_file" 2>/dev/null || echo 0)
        
        if [ "$file_size" -lt 1024 ] || [ "$file_size" -gt 104857600 ]; then
            echo "⚠️  Suspicious file size: $(basename "$wav_file") ($file_size bytes)"
            corrupted_files=$((corrupted_files + 1))
        fi
        
        # Check file header (WAV files should start with RIFF)
        if ! head -c 4 "$wav_file" | grep -q "RIFF"; then
            echo "❌ Invalid WAV header: $(basename "$wav_file")"
            corrupted_files=$((corrupted_files + 1))
        fi
    fi
done

echo "📊 Validation complete:"
echo "   - Total files checked: $total_files"
echo "   - Corrupted files found: $corrupted_files"
echo "   - Integrity: $((100 - (corrupted_files * 100 / total_files)))%"

# 3. Create integrity checksum
echo "🔐 Creating integrity checksums..."
find "$AUDIO_DIR" -name "*.wav" -exec shasum -a 256 {} \; > "$BACKUP_DIR/checksums.sha256"
echo "✅ Checksums saved to $BACKUP_DIR/checksums.sha256"

# 4. Backup labels file
if [ -f "$LABELS_FILE" ]; then
    cp "$LABELS_FILE" "$BACKUP_DIR/audio_labels_backup.csv"
    echo "✅ Labels file backed up"
fi

# 5. Create restoration script
cat > "$BACKUP_DIR/restore.sh" << 'EOF'
#!/bin/bash
echo "🔄 Restoring audio files from backup..."
RESTORE_TARGET="/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files"
BACKUP_SOURCE="$(dirname "$0")"

echo "   Source: $BACKUP_SOURCE"
echo "   Target: $RESTORE_TARGET"

read -p "Are you sure you want to restore? This will overwrite current files. (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cp -r "$BACKUP_SOURCE"/*.wav "$RESTORE_TARGET/"
    if [ -f "$BACKUP_SOURCE/audio_labels_backup.csv" ]; then
        cp "$BACKUP_SOURCE/audio_labels_backup.csv" "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_labels.csv"
    fi
    echo "✅ Files restored successfully!"
else
    echo "❌ Restore cancelled"
fi
EOF

chmod +x "$BACKUP_DIR/restore.sh"
echo "✅ Restoration script created at $BACKUP_DIR/restore.sh"

echo "🎉 Protection complete! Backup location: $BACKUP_DIR"
