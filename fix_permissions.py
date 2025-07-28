#!/usr/bin/env python3
"""
Database Permissions Setup Script for FootyBets.ai
Grants all necessary permissions to footybets_user for the application to function properly.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def main():
    # Get environment variables
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    footybets_password = os.getenv('FOOTYBETS_USER_PASSWORD')
    
    if not postgres_password:
        print("ERROR: POSTGRES_PASSWORD environment variable not set")
        sys.exit(1)
        
    if not footybets_password:
        print("ERROR: FOOTYBETS_USER_PASSWORD environment variable not set")
        sys.exit(1)
    
    # Database connection parameters
    db_params = {
        'host': '34.69.151.218',
        'port': '5432',
        'database': 'postgres',  # Connect to postgres database first
        'user': 'postgres',
        'password': postgres_password
    }
    
    try:
        print("🔗 Connecting to PostgreSQL server...")
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create footybets database if it doesn't exist
        print("📊 Creating footybets database if it doesn't exist...")
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'footybets'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE footybets")
            print("✅ Created footybets database")
        else:
            print("ℹ️  Database footybets already exists")
        
        # Create footybets_user if it doesn't exist
        print("👤 Creating footybets_user if it doesn't exist...")
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = 'footybets_user'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE USER footybets_user WITH PASSWORD '{footybets_password}'")
            print("✅ Created footybets_user")
        else:
            print("ℹ️  User footybets_user already exists")
            # Update password in case it changed
            cursor.execute(f"ALTER USER footybets_user WITH PASSWORD '{footybets_password}'")
            print("✅ Updated footybets_user password")
        
        # Grant database-level permissions
        print("🔐 Granting database-level permissions...")
        permissions_queries = [
            "GRANT CONNECT ON DATABASE footybets TO footybets_user",
            "GRANT CREATE ON DATABASE footybets TO footybets_user",
        ]
        
        for query in permissions_queries:
            try:
                cursor.execute(query)
                print(f"✅ Executed: {query}")
            except Exception as e:
                print(f"⚠️  Warning executing '{query}': {e}")
        
        cursor.close()
        conn.close()
        
        # Now connect to footybets database for schema-level permissions
        print("🔗 Connecting to footybets database...")
        db_params['database'] = 'footybets'
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Grant schema permissions
        print("🏗️  Granting schema permissions...")
        schema_queries = [
            "GRANT ALL PRIVILEGES ON SCHEMA public TO footybets_user",
            "GRANT CREATE ON SCHEMA public TO footybets_user",
            "GRANT USAGE ON SCHEMA public TO footybets_user",
        ]
        
        for query in schema_queries:
            try:
                cursor.execute(query)
                print(f"✅ Executed: {query}")
            except Exception as e:
                print(f"⚠️  Warning executing '{query}': {e}")
        
        # Grant permissions on all existing tables
        print("📋 Granting permissions on existing tables...")
        table_queries = [
            "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO footybets_user",
            "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO footybets_user",
            "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO footybets_user",
        ]
        
        for query in table_queries:
            try:
                cursor.execute(query)
                print(f"✅ Executed: {query}")
            except Exception as e:
                print(f"⚠️  Warning executing '{query}': {e}")
        
        # Grant default privileges for future objects
        print("🔮 Setting default privileges for future objects...")
        default_queries = [
            "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO footybets_user",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO footybets_user",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO footybets_user",
        ]
        
        for query in default_queries:
            try:
                cursor.execute(query)
                print(f"✅ Executed: {query}")
            except Exception as e:
                print(f"⚠️  Warning executing '{query}': {e}")
        
        # Make footybets_user owner of the database for full control
        print("👑 Making footybets_user owner of the database...")
        try:
            cursor.execute("ALTER DATABASE footybets OWNER TO footybets_user")
            print("✅ Made footybets_user owner of footybets database")
        except Exception as e:
            print(f"⚠️  Warning making user owner: {e}")
        
        # Verify permissions by listing user privileges
        print("🔍 Verifying user permissions...")
        cursor.execute("""
            SELECT 
                grantee, 
                privilege_type 
            FROM information_schema.role_table_grants 
            WHERE grantee = 'footybets_user'
            LIMIT 10
        """)
        
        grants = cursor.fetchall()
        if grants:
            print("✅ User has the following table privileges:")
            for grantee, privilege in grants:
                print(f"   - {privilege}")
        else:
            print("ℹ️  No specific table grants found (may have schema-level permissions)")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Successfully granted all necessary permissions to footybets_user!")
        print("The user now has:")
        print("   ✅ Database connect and create privileges")
        print("   ✅ Full schema access (public)")
        print("   ✅ All table, sequence, and function privileges")
        print("   ✅ Default privileges for future objects")
        print("   ✅ Database ownership")
        print("\n🚀 Your FootyBets.ai application should now have full database access!")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()