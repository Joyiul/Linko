import os
import shutil
import hashlib
import wave
import pandas as pd
from datetime import datetime
import json

class ComprehensiveAudioProtector:
    """
    Comprehensive audio dataset protection for all audio files in the dataset
    """
    
    def __init__(self):
        self.base_dir = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets"
        self.audio_dirs = [
            os.path.join(self.base_dir, "audio_files"),
            os.path.join(self.base_dir, "audio_files", "dataverse_files-3"),
            os.path.join(self.base_dir, "audio_files_augmented")
        ]
        self.backup_dir = os.path.join(self.base_dir, f"comprehensive_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.labels_files = [
            os.path.join(self.base_dir, "audio_labels.csv"),
            os.path.join(self.base_dir, "audio_labels_augmented.csv")
        ]
        
    def find_all_audio_files(self):
        """Find all audio files in all directories"""
        all_files = []
        
        for audio_dir in self.audio_dirs:
            if os.path.exists(audio_dir):
                print(f"📁 Scanning: {audio_dir}")
                
                for root, dirs, files in os.walk(audio_dir):
                    for file in files:
                        if file.endswith(('.wav', '.mp3', '.m4a', '.flac')):
                            full_path = os.path.join(root, file)
                            relative_path = os.path.relpath(full_path, self.base_dir)
                            all_files.append({
                                'filename': file,
                                'full_path': full_path,
                                'relative_path': relative_path,
                                'directory': audio_dir,
                                'size': os.path.getsize(full_path)
                            })
        
        print(f"🎵 Found {len(all_files)} audio files total")
        return all_files
    
    def create_checksum(self, file_path):
        """Create SHA-256 checksum for a file"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            print(f"❌ Error creating checksum for {file_path}: {e}")
            return None
    
    def validate_audio_file(self, file_path):
        """Validate audio file integrity"""
        try:
            file_size = os.path.getsize(file_path)
            
            # Basic size checks
            if file_size < 1024:
                return False, "File too small"
            if file_size > 100 * 1024 * 1024:
                return False, "File too large"
            
            # For WAV files, do deeper validation
            if file_path.endswith('.wav'):
                try:
                    with wave.open(file_path, 'rb') as wav_file:
                        frames = wav_file.getnframes()
                        sample_rate = wav_file.getframerate()
                        channels = wav_file.getnchannels()
                        
                        if frames == 0:
                            return False, "No audio frames"
                        if sample_rate < 8000 or sample_rate > 48000:
                            return False, f"Unusual sample rate: {sample_rate}"
                        if channels < 1 or channels > 8:
                            return False, f"Unusual channel count: {channels}"
                except Exception as e:
                    return False, f"WAV validation error: {str(e)}"
            
            return True, "Valid"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def create_comprehensive_backup(self):
        """Create backup of all audio files"""
        print("🛡️ Creating Comprehensive Audio Dataset Backup")
        print("=" * 60)
        
        # Create backup directory structure
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Find all audio files
        all_files = self.find_all_audio_files()
        
        if not all_files:
            print("❌ No audio files found!")
            return None
        
        # Process each file
        backup_info = {}
        stats = {
            'total_files': 0,
            'valid_files': 0,
            'corrupted_files': 0,
            'total_size': 0,
            'backed_up_size': 0
        }
        
        print(f"\n📦 Processing {len(all_files)} files...")
        
        for i, file_info in enumerate(all_files):
            stats['total_files'] += 1
            stats['total_size'] += file_info['size']
            
            if i % 100 == 0:
                print(f"   Progress: {i}/{len(all_files)} ({i/len(all_files)*100:.1f}%)")
            
            # Validate file
            is_valid, validation_msg = self.validate_audio_file(file_info['full_path'])
            
            if is_valid:
                # Create backup directory structure
                backup_file_dir = os.path.join(self.backup_dir, os.path.dirname(file_info['relative_path']))
                os.makedirs(backup_file_dir, exist_ok=True)
                
                # Copy file to backup
                backup_file_path = os.path.join(self.backup_dir, file_info['relative_path'])
                shutil.copy2(file_info['full_path'], backup_file_path)
                
                # Create checksum
                checksum = self.create_checksum(file_info['full_path'])
                
                backup_info[file_info['relative_path']] = {
                    'status': 'valid',
                    'filename': file_info['filename'],
                    'checksum': checksum,
                    'size': file_info['size'],
                    'original_path': file_info['full_path'],
                    'backed_up': True
                }
                
                stats['valid_files'] += 1
                stats['backed_up_size'] += file_info['size']
                
            else:
                backup_info[file_info['relative_path']] = {
                    'status': 'corrupted',
                    'filename': file_info['filename'],
                    'error': validation_msg,
                    'size': file_info['size'],
                    'original_path': file_info['full_path'],
                    'backed_up': False
                }
                stats['corrupted_files'] += 1
                print(f"❌ Corrupted: {file_info['filename']} - {validation_msg}")
        
        # Backup labels files
        labels_backed_up = 0
        for labels_file in self.labels_files:
            if os.path.exists(labels_file):
                backup_labels_path = os.path.join(self.backup_dir, os.path.basename(labels_file))
                shutil.copy2(labels_file, backup_labels_path)
                labels_backed_up += 1
        
        print(f"✅ Backed up {labels_backed_up} label files")
        
        # Save backup information
        backup_metadata = {
            'backup_date': datetime.now().isoformat(),
            'stats': stats,
            'backup_location': self.backup_dir,
            'file_info': backup_info
        }
        
        # Save metadata
        metadata_file = os.path.join(self.backup_dir, 'backup_metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(backup_metadata, f, indent=2)
        
        # Create summary report
        integrity_pct = (stats['valid_files'] / stats['total_files']) * 100 if stats['total_files'] > 0 else 0
        
        print(f"\n📊 Backup Complete!")
        print(f"   - Total files found: {stats['total_files']:,}")
        print(f"   - Valid files: {stats['valid_files']:,}")
        print(f"   - Corrupted files: {stats['corrupted_files']:,}")
        print(f"   - Dataset integrity: {integrity_pct:.1f}%")
        print(f"   - Total size: {stats['total_size'] / (1024*1024):.1f} MB")
        print(f"   - Backed up size: {stats['backed_up_size'] / (1024*1024):.1f} MB")
        print(f"   - Backup location: {self.backup_dir}")
        
        # Create quick restore script
        restore_script = os.path.join(self.backup_dir, 'restore_all.py')
        with open(restore_script, 'w') as f:
            f.write(f'''#!/usr/bin/env python3
import os
import shutil
import json

def restore_all():
    """Restore all files from this backup"""
    backup_dir = "{self.backup_dir}"
    base_dir = "{self.base_dir}"
    
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
    
    print(f"✅ Restored {{restored}} files")

if __name__ == "__main__":
    restore_all()
''')
        
        os.chmod(restore_script, 0o755)
        print(f"📄 Restore script created: {restore_script}")
        
        return backup_metadata

def main():
    """Run comprehensive backup"""
    protector = ComprehensiveAudioProtector()
    backup_info = protector.create_comprehensive_backup()
    
    if backup_info:
        print("\n🎉 Comprehensive protection system activated!")
        print(f"🔒 Your {backup_info['stats']['total_files']:,} audio files are now protected!")
    
    return protector

if __name__ == "__main__":
    main()
