import subprocess
import logging
import os
import shutil
from pathlib import Path
from datetime import datetime

class SelfRepair:
    def __init__(self):
        self.logger = logging.getLogger('SelfRepair')
        self.backup_dir = "backups"
        Path(self.backup_dir).mkdir(exist_ok=True)
        self.essential_files = [
            "neurofusion_ai.py",
            "requirements.txt",
            "static/js/3d_avatar.js",
            "templates/index.html"
        ]

    def create_backup(self):
        """Create a timestamped backup of essential files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(self.backup_dir) / f"backup_{timestamp}"
        backup_path.mkdir()
        
        for file in self.essential_files:
            try:
                if os.path.isdir(file):
                    shutil.copytree(file, backup_path / file)
                else:
                    shutil.copy2(file, backup_path / file)
            except Exception as e:
                self.logger.error(f"Failed to backup {file}: {str(e)}")
        
        return backup_path

    def repair_corrupted_files(self):
        """Check and repair corrupted files from backups"""
        try:
            backups = sorted(Path(self.backup_dir).iterdir(), key=os.path.getmtime)
            if not backups:
                return False
                
            latest_backup = backups[-1]
            for file in self.essential_files:
                if not Path(file).exists() or os.path.getsize(file) == 0:
                    shutil.copy2(latest_backup / file, file)
                    self.logger.info(f"Restored {file} from backup")
            return True
        except Exception as e:
            self.logger.error(f"Repair failed: {str(e)}")
            return False

    def update_dependencies(self):
        """Automatically update Python dependencies"""
        try:
            result = subprocess.run(
                ["pip", "install", "--upgrade", "-r", "requirements.txt"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.logger.info("Dependencies updated successfully")
                return True
            else:
                self.logger.error(f"Dependency update failed: {result.stderr}")
                return False
        except Exception as e:
            self.logger.error(f"Update process failed: {str(e)}")
            return False