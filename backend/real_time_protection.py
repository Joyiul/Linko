import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
from datetime import datetime

class AudioFileProtectionHandler(FileSystemEventHandler):
    """Real-time protection for audio files"""
    
    def __init__(self, audio_dir, backup_dir):
        self.audio_dir = audio_dir
        self.backup_dir = backup_dir
        self.protected_files = set()
        self.load_protected_files()
    
    def load_protected_files(self):
        """Load list of files that should be protected"""
        protection_file = os.path.join(os.path.dirname(self.audio_dir), 'protection_info.json')
        if os.path.exists(protection_file):
            with open(protection_file, 'r') as f:
                info = json.load(f)
                # Load all .wav files as protected
                for filename in os.listdir(self.audio_dir):
                    if filename.endswith('.wav'):
                        self.protected_files.add(filename)
    
    def on_deleted(self, event):
        """Handle file deletion"""
        if not event.is_directory and event.src_path.endswith('.wav'):
            filename = os.path.basename(event.src_path)
            if filename in self.protected_files:
                print(f"🚨 ALERT: Protected audio file deleted: {filename}")
                self.restore_file(filename)
    
    def on_modified(self, event):
        """Handle file modification"""
        if not event.is_directory and event.src_path.endswith('.wav'):
            filename = os.path.basename(event.src_path)
            if filename in self.protected_files:
                print(f"⚠️  ALERT: Protected audio file modified: {filename}")
                # Could add checksum verification here
    
    def restore_file(self, filename):
        """Restore a deleted file from backup"""
        backup_path = os.path.join(self.backup_dir, filename)
        target_path = os.path.join(self.audio_dir, filename)
        
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, target_path)
            print(f"✅ Restored {filename} from backup")
        else:
            print(f"❌ Backup not found for {filename}")

def start_real_time_protection():
    """Start real-time file protection"""
    audio_dir = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets/audio_files"
    
    # Find most recent backup
    base_dir = "/Users/keiralie/Documents/GitHub/ImmigrantSlangster/backend/Datasets"
    backup_dirs = [d for d in os.listdir(base_dir) if d.startswith('audio_backup_')]
    
    if not backup_dirs:
        print("❌ No backup found. Please run protection first.")
        return
    
    latest_backup = max(backup_dirs, key=lambda d: os.path.getctime(os.path.join(base_dir, d)))
    backup_dir = os.path.join(base_dir, latest_backup)
    
    print(f"🛡️ Starting real-time protection...")
    print(f"📁 Monitoring: {audio_dir}")
    print(f"🔄 Backup source: {backup_dir}")
    
    event_handler = AudioFileProtectionHandler(audio_dir, backup_dir)
    observer = Observer()
    observer.schedule(event_handler, audio_dir, recursive=False)
    observer.start()
    
    try:
        print("✅ Real-time protection active. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Real-time protection stopped.")
    
    observer.join()

if __name__ == "__main__":
    start_real_time_protection()
