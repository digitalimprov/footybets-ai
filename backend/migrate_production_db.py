#!/usr/bin/env python3
"""
Script to migrate the production PostgreSQL database
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Production database URL - Cloud SQL format
DATABASE_URL = "postgresql://footybets_user:footybets_password@34.69.151.218:5432/footybets"

def migrate_production_database():
    """Remove first_name and last_name columns from users table"""
    
    print("🔧 Migrating production database...")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Connected to production database")
        
        # Check if columns exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            AND column_name IN ('first_name', 'last_name')
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"Found columns: {existing_columns}")
        
        if 'first_name' in existing_columns:
            print("🗑️ Removing first_name column...")
            cursor.execute("ALTER TABLE users DROP COLUMN first_name")
            print("✅ Removed first_name column")
        
        if 'last_name' in existing_columns:
            print("🗑️ Removing last_name column...")
            cursor.execute("ALTER TABLE users DROP COLUMN last_name")
            print("✅ Removed last_name column")
        
        # Verify the changes
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position
        """)
        
        columns = [row[0] for row in cursor.fetchall()]
        print(f"✅ Updated table structure: {columns}")
        
        cursor.close()
        conn.close()
        
        print("🎉 Production database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = migrate_production_database()
    sys.exit(0 if success else 1) 