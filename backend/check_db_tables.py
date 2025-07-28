#!/usr/bin/env python3
"""
Script to check database tables.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def check_tables():
    """Check what tables exist in the database."""
    
    print("=== Checking Database Tables ===")
    
    # Use production database URL
    production_db_url = "postgresql://footybets_user:footybets_password@34.69.151.218:5432/footybets?sslmode=require"
    print(f"Database URL: {production_db_url}")
    
    try:
        # Create engine and session
        engine = create_engine(production_db_url)
        
        with engine.connect() as conn:
            # Get all tables
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result]
            
            print(f"Found {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
            
            # Check if content table exists
            if 'content' in tables:
                print("\n✅ Content table exists")
            else:
                print("\n❌ Content table does not exist")
                
            # Check if alembic_version table exists
            if 'alembic_version' in tables:
                print("✅ Alembic version table exists")
            else:
                print("❌ Alembic version table does not exist")
                
    except Exception as e:
        print(f"✗ Error checking tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_tables() 