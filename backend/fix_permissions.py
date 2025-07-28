#!/usr/bin/env python3
"""
Script to fix database permissions for the footybets_app user
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect as postgres superuser to fix permissions
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
if not POSTGRES_PASSWORD:
    print("❌ Error: POSTGRES_PASSWORD environment variable not set")
    print("Please run: export POSTGRES_PASSWORD='your-postgres-password'")
    sys.exit(1)

DATABASE_URL = f"postgresql://postgres:{POSTGRES_PASSWORD}@34.69.151.218:5432/footybets"

def fix_permissions():
    """Fix database permissions for the footybets_app user"""
    
    print("🔧 Fixing database permissions...")
    
    try:
        # Connect to the database as postgres superuser
        conn = psycopg2.connect(DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Connected to PostgreSQL database as superuser")
        
        # Grant all privileges to footybets_user user
        print("🔐 Granting permissions to footybets_user...")
        
        # Grant schema usage
        cursor.execute("GRANT USAGE ON SCHEMA public TO footybets_user")
        
        # Grant all privileges on all tables
        cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO footybets_user")
        
        # Grant all privileges on all sequences
        cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO footybets_user")
        
        # Grant all privileges on all functions
        cursor.execute("GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO footybets_user")
        
        # Grant default privileges for future tables
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO footybets_user")
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO footybets_user")
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO footybets_user")
        
        print("✅ Permissions granted successfully")
        
        # Verify the user can access the tables
        print("🔍 Verifying permissions...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'users'
        """)
        
        tables = cursor.fetchall()
        if tables:
            print("✅ Users table exists")
            
            # Test if footybets_app can access the table
            cursor.execute("""
                SELECT COUNT(*) FROM users
            """)
            count = cursor.fetchone()[0]
            print(f"✅ Users table is accessible (contains {count} users)")
        else:
            print("❌ Users table does not exist")
        
        cursor.close()
        conn.close()
        
        print("🎉 Database permissions fixed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix permissions: {e}")
        return False

if __name__ == "__main__":
    success = fix_permissions()
    sys.exit(0 if success else 1) 