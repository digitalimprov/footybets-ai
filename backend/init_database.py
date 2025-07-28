#!/usr/bin/env python3
"""
Script to initialize the PostgreSQL database with proper tables and permissions
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Production database URL
FOOTYBETS_USER_PASSWORD = os.getenv('FOOTYBETS_USER_PASSWORD')
if not FOOTYBETS_USER_PASSWORD:
    print("❌ Error: FOOTYBETS_USER_PASSWORD environment variable not set")
    print("Please run: export FOOTYBETS_USER_PASSWORD='your-footybets-user-password'")
    sys.exit(1)

DATABASE_URL = f"postgresql://footybets_user:{FOOTYBETS_USER_PASSWORD}@34.69.151.218:5432/footybets"

def init_database():
    """Initialize the database with tables and permissions"""
    
    print("🔧 Initializing PostgreSQL database...")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Connected to PostgreSQL database")
        
        # Create tables if they don't exist
        print("📋 Creating database tables...")
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(100) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                phone_number VARCHAR(20),
                is_active BOOLEAN DEFAULT TRUE,
                is_verified BOOLEAN DEFAULT FALSE,
                is_admin BOOLEAN DEFAULT FALSE,
                subscription_tier VARCHAR(50) DEFAULT 'free',
                subscription_expires TIMESTAMP,
                roles JSONB DEFAULT '["user"]',
                permissions JSONB DEFAULT '["read:own", "write:own"]',
                email_verification_token VARCHAR(255),
                password_reset_token VARCHAR(255),
                password_reset_expires TIMESTAMP,
                last_login TIMESTAMP,
                failed_login_attempts INTEGER DEFAULT 0,
                account_locked_until TIMESTAMP,
                api_key_hash VARCHAR(255),
                api_key_created TIMESTAMP,
                api_key_last_used TIMESTAMP,
                privacy_settings JSONB DEFAULT '{}',
                notification_settings JSONB DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_password_change TIMESTAMP
            )
        """)
        
        # Teams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                abbreviation VARCHAR(10) NOT NULL,
                city VARCHAR(100),
                state VARCHAR(100),
                venue VARCHAR(200),
                founded_year INTEGER,
                colors JSONB,
                logo_url VARCHAR(500),
                website_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Games table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id SERIAL PRIMARY KEY,
                season INTEGER NOT NULL,
                round_number INTEGER NOT NULL,
                game_number INTEGER NOT NULL,
                home_team_id INTEGER REFERENCES teams(id),
                away_team_id INTEGER REFERENCES teams(id),
                venue VARCHAR(200),
                game_date TIMESTAMP NOT NULL,
                is_finished BOOLEAN DEFAULT FALSE,
                home_score INTEGER,
                away_score INTEGER,
                home_goals INTEGER,
                away_goals INTEGER,
                home_behinds INTEGER,
                away_behinds INTEGER,
                weather VARCHAR(100),
                temperature DECIMAL(4,1),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Predictions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                game_id INTEGER REFERENCES games(id),
                predicted_winner VARCHAR(100),
                confidence_score DECIMAL(5,2),
                prediction_type VARCHAR(50),
                is_correct BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Content table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                slug VARCHAR(255) UNIQUE NOT NULL,
                content_type VARCHAR(50) NOT NULL,
                content TEXT,
                excerpt TEXT,
                featured_image_url VARCHAR(500),
                author_id INTEGER REFERENCES users(id),
                status VARCHAR(20) DEFAULT 'draft',
                published_at TIMESTAMP,
                meta_title VARCHAR(255),
                meta_description TEXT,
                tags JSONB,
                categories JSONB,
                seo_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                session_token VARCHAR(255) UNIQUE NOT NULL,
                ip_address VARCHAR(45),
                user_agent TEXT,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Security logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_logs (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                action VARCHAR(100) NOT NULL,
                details JSONB,
                ip_address VARCHAR(45),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id SERIAL PRIMARY KEY,
                metric_name VARCHAR(100) NOT NULL,
                metric_value JSONB,
                period VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Database tables created successfully")
        
        # Grant permissions to the app user
        print("🔐 Setting up permissions...")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO footybets_app")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO footybets_app")
        cursor.execute("GRANT USAGE ON SCHEMA public TO footybets_app")
        
        print("✅ Permissions granted successfully")
        
        # Create admin user
        print("👤 Creating admin user...")
        import bcrypt
        hashed_password = bcrypt.hashpw("Admin123!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute("""
            INSERT INTO users (email, username, hashed_password, is_active, is_verified, is_admin, roles, permissions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET
                username = EXCLUDED.username,
                hashed_password = EXCLUDED.hashed_password,
                is_active = EXCLUDED.is_active,
                is_verified = EXCLUDED.is_verified,
                is_admin = EXCLUDED.is_admin,
                roles = EXCLUDED.roles,
                permissions = EXCLUDED.permissions
        """, (
            "gmcintosh1985@gmail.com",
            "admin",
            hashed_password,
            True,
            True,
            True,
            '["admin", "user"]',
            '["read:all", "write:all", "admin:all"]'
        ))
        
        print("✅ Admin user created successfully")
        
        cursor.close()
        conn.close()
        
        print("🎉 Database initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1) 