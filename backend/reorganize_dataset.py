#!/usr/bin/env python3

import os
import shutil
from pathlib import Path

def reorganize_audio_files():
    """
    Move all audio files from dataverse_files-3 subdirectory to main audio_files directory
    """
    
    # Paths
    audio_files_dir = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files"
    dataverse_dir = os.path.join(audio_files_dir, "dataverse_files-3")
    
    print("🔄 Reorganizing Audio Dataset Structure")
    print("=" * 50)
    
    if not os.path.exists(dataverse_dir):
        print(f"❌ Directory not found: {dataverse_dir}")
        return False
    
    # Count files before moving
    files_to_move = []
    conflicts = []
    
    print(f"📁 Scanning: {dataverse_dir}")
    
    for item in os.listdir(dataverse_dir):
        source_path = os.path.join(dataverse_dir, item)
        target_path = os.path.join(audio_files_dir, item)
        
        if os.path.isfile(source_path):
            if item.endswith(('.wav', '.mp3', '.m4a', '.flac', '.txt')):
                # Check for conflicts
                if os.path.exists(target_path):
                    # Compare file sizes to see if they're the same
                    source_size = os.path.getsize(source_path)
                    target_size = os.path.getsize(target_path)
                    
                    if source_size == target_size:
                        print(f"🔄 Duplicate found (same size): {item}")
                        conflicts.append({
                            'file': item,
                            'action': 'skip_duplicate',
                            'source_size': source_size,
                            'target_size': target_size
                        })
                    else:
                        print(f"⚠️  Conflict (different sizes): {item}")
                        conflicts.append({
                            'file': item,
                            'action': 'rename_new',
                            'source_size': source_size,
                            'target_size': target_size
                        })
                else:
                    files_to_move.append({
                        'source': source_path,
                        'target': target_path,
                        'filename': item,
                        'size': os.path.getsize(source_path)
                    })
    
    print(f"\n📊 Analysis Results:")
    print(f"   - Files to move: {len(files_to_move)}")
    print(f"   - Conflicts found: {len(conflicts)}")
    
    if conflicts:
        print(f"\n⚠️  Handling Conflicts:")
        for conflict in conflicts:
            if conflict['action'] == 'skip_duplicate':
                print(f"   - Skipping duplicate: {conflict['file']} (same size: {conflict['source_size']} bytes)")
            elif conflict['action'] == 'rename_new':
                print(f"   - Will rename: {conflict['file']} (source: {conflict['source_size']}, target: {conflict['target_size']})")
    
    # Proceed with the move
    if files_to_move or conflicts:
        response = input(f"\n❓ Proceed with moving {len(files_to_move)} files? (y/N): ").lower().strip()
        
        if response != 'y':
            print("❌ Operation cancelled")
            return False
    
    # Move files
    moved_count = 0
    skipped_count = 0
    renamed_count = 0
    
    print(f"\n🚀 Starting file reorganization...")
    
    # Move new files
    for file_info in files_to_move:
        try:
            shutil.move(file_info['source'], file_info['target'])
            moved_count += 1
            if moved_count % 100 == 0:
                print(f"   Progress: {moved_count}/{len(files_to_move)} files moved")
        except Exception as e:
            print(f"❌ Error moving {file_info['filename']}: {e}")
    
    # Handle conflicts
    for conflict in conflicts:
        source_path = os.path.join(dataverse_dir, conflict['file'])
        
        if conflict['action'] == 'skip_duplicate':
            # Just remove the duplicate from dataverse folder
            try:
                os.remove(source_path)
                skipped_count += 1
            except Exception as e:
                print(f"❌ Error removing duplicate {conflict['file']}: {e}")
        
        elif conflict['action'] == 'rename_new':
            # Rename and move the conflicting file
            base_name, ext = os.path.splitext(conflict['file'])
            new_name = f"{base_name}_dataverse{ext}"
            target_path = os.path.join(audio_files_dir, new_name)
            
            try:
                shutil.move(source_path, target_path)
                renamed_count += 1
                print(f"📝 Renamed conflicting file: {conflict['file']} → {new_name}")
            except Exception as e:
                print(f"❌ Error renaming {conflict['file']}: {e}")
    
    # Clean up empty dataverse directory
    try:
        remaining_files = os.listdir(dataverse_dir)
        if not remaining_files:
            os.rmdir(dataverse_dir)
            print(f"🗑️  Removed empty directory: dataverse_files-3")
        else:
            print(f"⚠️  Directory not empty, keeping: {len(remaining_files)} items remain")
            print(f"   Remaining items: {remaining_files[:5]}{'...' if len(remaining_files) > 5 else ''}")
    except Exception as e:
        print(f"❌ Error cleaning up directory: {e}")
    
    # Final summary
    print(f"\n✅ Reorganization Complete!")
    print(f"   - Files moved: {moved_count}")
    print(f"   - Duplicates skipped: {skipped_count}")
    print(f"   - Files renamed: {renamed_count}")
    
    # Update file count
    total_files = len([f for f in os.listdir(audio_files_dir) 
                      if f.endswith(('.wav', '.mp3', '.m4a', '.flac'))])
    
    print(f"\n📁 New audio_files directory:")
    print(f"   - Total audio files: {total_files}")
    print(f"   - Location: {audio_files_dir}")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Run dataset protection: python comprehensive_audio_protection.py")
    print(f"   2. Update your model training to use the new flat structure")
    print(f"   3. Generate new audio labels if needed")
    
    return True

if __name__ == "__main__":
    reorganize_audio_files()
