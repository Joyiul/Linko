#!/usr/bin/env python3
import os
import shutil
import json

def restore_all():
    """Restore all files from this backup"""
    backup_dir = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/comprehensive_backup_20250805_215249"
    base_dir = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets"
    
    print("🔄 Restoring all audio files...")
    
    # Load metadata
    with open(os.path.join(backup_dir, "backup_metadata.json"), "r") as f:
        metadata = json.load(f)
    
    restored = 0
    for rel_path, info in metadata["file_info"].items():
        if info["backed_up"]:
            backup_file = os.path.join(backup_dir, rel_path)
            target_file = os.path.join(base_dir, rel_path)
            
            # Create target directory
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            
            # Copy file
            shutil.copy2(backup_file, target_file)
            restored += 1
    
    print(f"✅ Restored {restored} files")

if __name__ == "__main__":
    restore_all()
