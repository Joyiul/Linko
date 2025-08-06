import os
import shutil
import hashlib
import wave
import pandas as pd
from datetime import datetime
import json

class AudioDatasetProtector:
    """
    Advanced audio dataset protection with corruption detection and recovery
    """
    
    def __init__(self, audio_dir=None):
        self.audio_dir = audio_dir or "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files"
        self.backup_dir = f"/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.labels_file = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_labels.csv"
        
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
    
    def validate_wav_file(self, file_path):
        """Validate WAV file integrity"""
        try:
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size < 1024:  # Less than 1KB
                return False, "File too small"
            if file_size > 100 * 1024 * 1024:  # More than 100MB
                return False, "File too large"
            
            # Try to open with wave module
            with wave.open(file_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                
                if frames == 0:
                    return False, "No audio frames"
                if sample_rate < 8000 or sample_rate > 48000:
                    return False, f"Unusual sample rate: {sample_rate}"
                if channels < 1 or channels > 2:
                    return False, f"Unusual channel count: {channels}"
                    
            return True, "Valid"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def create_backup(self):
        """Create comprehensive backup of audio dataset"""
        print("🛡️ Creating comprehensive audio dataset backup...")
        
        # Create backup directory
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Backup all audio files with validation
        valid_files = 0
        corrupted_files = 0
        total_files = 0
        file_info = {}
        
        print(f"📁 Backing up files to: {self.backup_dir}")
        
        for filename in os.listdir(self.audio_dir):
            if filename.endswith('.wav'):
                total_files += 1
                source_path = os.path.join(self.audio_dir, filename)
                backup_path = os.path.join(self.backup_dir, filename)
                
                # Validate file before backup
                is_valid, validation_msg = self.validate_wav_file(source_path)
                
                if is_valid:
                    # Copy file and create checksum
                    shutil.copy2(source_path, backup_path)
                    checksum = self.create_checksum(source_path)
                    
                    file_info[filename] = {
                        'status': 'valid',
                        'checksum': checksum,
                        'size': os.path.getsize(source_path),
                        'backed_up': True
                    }
                    valid_files += 1
                else:
                    file_info[filename] = {
                        'status': 'corrupted',
                        'error': validation_msg,
                        'size': os.path.getsize(source_path),
                        'backed_up': False
                    }
                    corrupted_files += 1
                    print(f"❌ Corrupted file: {filename} - {validation_msg}")
        
        # Backup labels file
        if os.path.exists(self.labels_file):
            shutil.copy2(self.labels_file, os.path.join(self.backup_dir, 'audio_labels_backup.csv'))
            print("✅ Labels file backed up")
        
        # Save file information
        info_file = os.path.join(self.backup_dir, 'file_info.json')
        with open(info_file, 'w') as f:
            json.dump(file_info, f, indent=2)
        
        # Create summary report
        summary = {
            'backup_date': datetime.now().isoformat(),
            'total_files': total_files,
            'valid_files': valid_files,
            'corrupted_files': corrupted_files,
            'integrity_percentage': (valid_files / total_files * 100) if total_files > 0 else 0,
            'backup_location': self.backup_dir
        }
        
        summary_file = os.path.join(self.backup_dir, 'backup_summary.json')
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 Backup Summary:")
        print(f"   - Total files: {total_files}")
        print(f"   - Valid files: {valid_files}")
        print(f"   - Corrupted files: {corrupted_files}")
        print(f"   - Integrity: {summary['integrity_percentage']:.1f}%")
        print(f"   - Backup location: {self.backup_dir}")
        
        return summary
    
    def verify_integrity(self, backup_dir=None):
        """Verify current files against backup checksums"""
        backup_dir = backup_dir or self.backup_dir
        info_file = os.path.join(backup_dir, 'file_info.json')
        
        if not os.path.exists(info_file):
            print("❌ No backup information found")
            return False
        
        with open(info_file, 'r') as f:
            backup_info = json.load(f)
        
        print("🔍 Verifying file integrity...")
        
        changed_files = []
        missing_files = []
        
        for filename, info in backup_info.items():
            if info['status'] == 'valid':
                current_path = os.path.join(self.audio_dir, filename)
                
                if os.path.exists(current_path):
                    current_checksum = self.create_checksum(current_path)
                    if current_checksum != info['checksum']:
                        changed_files.append(filename)
                        print(f"⚠️  Changed: {filename}")
                else:
                    missing_files.append(filename)
                    print(f"❌ Missing: {filename}")
        
        if not changed_files and not missing_files:
            print("✅ All files verified - no corruption detected!")
            return True
        else:
            print(f"\n📊 Integrity Check Results:")
            print(f"   - Changed files: {len(changed_files)}")
            print(f"   - Missing files: {len(missing_files)}")
            return False
    
    def restore_from_backup(self, backup_dir=None):
        """Restore files from backup"""
        backup_dir = backup_dir or self.backup_dir
        
        if not os.path.exists(backup_dir):
            print(f"❌ Backup directory not found: {backup_dir}")
            return False
        
        print(f"🔄 Restoring files from: {backup_dir}")
        
        # Restore audio files
        restored_count = 0
        for filename in os.listdir(backup_dir):
            if filename.endswith('.wav'):
                source_path = os.path.join(backup_dir, filename)
                target_path = os.path.join(self.audio_dir, filename)
                shutil.copy2(source_path, target_path)
                restored_count += 1
        
        # Restore labels file
        backup_labels = os.path.join(backup_dir, 'audio_labels_backup.csv')
        if os.path.exists(backup_labels):
            shutil.copy2(backup_labels, self.labels_file)
            print("✅ Labels file restored")
        
        print(f"✅ Restored {restored_count} audio files")
        return True

def protect_audio_dataset():
    """Main function to protect audio dataset"""
    print("🛡️ Audio Dataset Protection System")
    print("=" * 50)
    
    protector = AudioDatasetProtector()
    
    # Create backup
    summary = protector.create_backup()
    
    # Save protector instance info for later use
    protection_info = {
        'last_backup': summary['backup_date'],
        'backup_location': summary['backup_location'],
        'file_count': summary['total_files'],
        'integrity': summary['integrity_percentage']
    }
    
    info_file = '/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/protection_info.json'
    with open(info_file, 'w') as f:
        json.dump(protection_info, f, indent=2)
    
    print(f"\n🎉 Protection system activated!")
    print(f"📄 Protection info saved to: {info_file}")
    
    return protector

if __name__ == "__main__":
    protect_audio_dataset()
