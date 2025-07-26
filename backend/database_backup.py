#!/usr/bin/env python3
"""
Database backup utility for FootyBets.ai
Provides automated backup functionality for both SQLite and PostgreSQL
"""

import os
import sys
import shutil
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseBackup:
    """Database backup utility"""
    
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
    def backup_sqlite(self, db_path: str = "footybets.db") -> Optional[str]:
        """Backup SQLite database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"footybets_backup_{timestamp}.db"
            backup_path = self.backup_dir / backup_filename
            
            # Copy the database file
            shutil.copy2(db_path, backup_path)
            
            # Get file size
            size_mb = backup_path.stat().st_size / (1024 * 1024)
            
            logger.info(f"✅ SQLite backup created: {backup_filename} ({size_mb:.2f} MB)")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"❌ SQLite backup failed: {e}")
            return None
    
    def backup_postgresql(self, db_url: str) -> Optional[str]:
        """Backup PostgreSQL database using pg_dump"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"footybets_backup_{timestamp}.sql"
            backup_path = self.backup_dir / backup_filename
            
            # Parse database URL
            # Format: postgresql://user:password@host:port/database
            parts = db_url.replace("postgresql://", "").split("@")
            auth = parts[0].split(":")
            host_db = parts[1].split("/")
            host_port = host_db[0].split(":")
            
            user = auth[0]
            password = auth[1] if len(auth) > 1 else ""
            host = host_port[0]
            port = host_port[1] if len(host_port) > 1 else "5432"
            database = host_db[1]
            
            # Set environment variable for password
            env = os.environ.copy()
            env['PGPASSWORD'] = password
            
            # Run pg_dump
            cmd = [
                'pg_dump',
                f'--host={host}',
                f'--port={port}',
                f'--username={user}',
                '--verbose',
                '--clean',
                '--no-owner',
                '--no-privileges',
                f'--file={backup_path}',
                database
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                size_mb = backup_path.stat().st_size / (1024 * 1024)
                logger.info(f"✅ PostgreSQL backup created: {backup_filename} ({size_mb:.2f} MB)")
                return str(backup_path)
            else:
                logger.error(f"❌ PostgreSQL backup failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"❌ PostgreSQL backup failed: {e}")
            return None
    
    def backup_database(self) -> Optional[str]:
        """Backup database based on current configuration"""
        db_url = settings.database_url
        
        if "sqlite" in db_url:
            # Extract SQLite file path
            db_path = db_url.replace("sqlite:///", "")
            return self.backup_sqlite(db_path)
        elif "postgresql" in db_url:
            return self.backup_postgresql(db_url)
        else:
            logger.error(f"❌ Unsupported database type: {db_url}")
            return None
    
    def list_backups(self) -> list:
        """List all available backups"""
        backups = []
        for file in self.backup_dir.glob("footybets_backup_*"):
            stat = file.stat()
            backups.append({
                'filename': file.name,
                'size_mb': stat.st_size / (1024 * 1024),
                'created': datetime.fromtimestamp(stat.st_mtime),
                'path': str(file)
            })
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups
    
    def cleanup_old_backups(self, keep_days: int = 30):
        """Remove backups older than specified days"""
        cutoff_date = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        removed_count = 0
        
        for file in self.backup_dir.glob("footybets_backup_*"):
            if file.stat().st_mtime < cutoff_date:
                file.unlink()
                removed_count += 1
                logger.info(f"🗑️  Removed old backup: {file.name}")
        
        if removed_count > 0:
            logger.info(f"🧹 Cleaned up {removed_count} old backups")
        else:
            logger.info("✨ No old backups to clean up")

def main():
    """Main backup function"""
    backup_util = DatabaseBackup()
    
    print("🔄 Creating database backup...")
    backup_path = backup_util.backup_database()
    
    if backup_path:
        print(f"✅ Backup successful: {backup_path}")
        
        # List recent backups
        print("\n📋 Recent backups:")
        backups = backup_util.list_backups()[:5]
        for backup in backups:
            print(f"  • {backup['filename']} ({backup['size_mb']:.2f} MB) - {backup['created'].strftime('%Y-%m-%d %H:%M')}")
        
        # Cleanup old backups
        print("\n🧹 Cleaning up old backups...")
        backup_util.cleanup_old_backups()
    else:
        print("❌ Backup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 