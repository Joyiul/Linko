#!/bin/bash

# 🔄 Quick Dataset Integrity Check
# Run this anytime to verify your audio files are safe

echo "🔍 Quick Audio Dataset Integrity Check"
echo "======================================"

BACKUP_DIR="/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/comprehensive_backup_20250805_215249"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Backup directory not found!"
    echo "   Run comprehensive_audio_protection.py first"
    exit 1
fi

echo "✅ Backup found: $(basename "$BACKUP_DIR")"

# Count current files
CURRENT_FILES=$(find /Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files* -name "*.wav" 2>/dev/null | wc -l)
echo "📁 Current audio files: $CURRENT_FILES"

# Check backup info
if [ -f "$BACKUP_DIR/backup_metadata.json" ]; then
    BACKUP_FILES=$(grep -o '"backed_up": true' "$BACKUP_DIR/backup_metadata.json" | wc -l)
    echo "💾 Backed up files: $BACKUP_FILES"
    
    if [ "$CURRENT_FILES" -ge "$BACKUP_FILES" ]; then
        echo "✅ File count looks good!"
    else
        echo "⚠️  File count decreased. Check for missing files."
    fi
else
    echo "⚠️  Backup metadata not found"
fi

echo ""
echo "🛡️ For full protection, run:"
echo "   python comprehensive_audio_protection.py"
