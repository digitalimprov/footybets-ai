#!/usr/bin/env python3
"""
Add brownlow_votes column to player_game_stats table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine
from sqlalchemy import text

def add_brownlow_votes_column():
    """Add brownlow_votes column to player_game_stats table"""
    print("🔧 Adding brownlow_votes column to player_game_stats table...")
    
    try:
        db = SessionLocal()
        
        # Check if column already exists
        result = db.execute(text("PRAGMA table_info(player_game_stats)"))
        columns = [row[1] for row in result.fetchall()]
        
        if 'brownlow_votes' in columns:
            print("✅ brownlow_votes column already exists")
            return True
        
        # Add the brownlow_votes column
        db.execute(text("ALTER TABLE player_game_stats ADD COLUMN brownlow_votes INTEGER DEFAULT 0"))
        db.commit()
        
        print("✅ Successfully added brownlow_votes column")
        
        # Verify the column was added
        result = db.execute(text("PRAGMA table_info(player_game_stats)"))
        columns = [row[1] for row in result.fetchall()]
        
        if 'brownlow_votes' in columns:
            print("✅ Column verified successfully")
            return True
        else:
            print("❌ Column was not added properly")
            return False
            
    except Exception as e:
        print(f"❌ Error adding brownlow_votes column: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

def create_brownlow_votes_table():
    """Create a separate table for Brownlow votes if needed"""
    print("🏆 Creating Brownlow votes table...")
    
    try:
        db = SessionLocal()
        
        # Create brownlow_votes table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS brownlow_votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            votes INTEGER NOT NULL DEFAULT 0,
            season INTEGER NOT NULL,
            round_number INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games (id),
            FOREIGN KEY (player_id) REFERENCES players (id),
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )
        """
        
        db.execute(text(create_table_sql))
        db.commit()
        
        # Create indexes for better performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_brownlow_votes_game_id ON brownlow_votes (game_id)",
            "CREATE INDEX IF NOT EXISTS idx_brownlow_votes_player_id ON brownlow_votes (player_id)",
            "CREATE INDEX IF NOT EXISTS idx_brownlow_votes_season ON brownlow_votes (season)",
            "CREATE INDEX IF NOT EXISTS idx_brownlow_votes_round ON brownlow_votes (round_number)"
        ]
        
        for index_sql in indexes:
            db.execute(text(index_sql))
        
        db.commit()
        print("✅ Brownlow votes table created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating Brownlow votes table: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """Main function"""
    print("🏈 Setting up Brownlow votes database structure")
    print("=" * 50)
    
    # Add column to existing table
    success1 = add_brownlow_votes_column()
    
    # Create separate table for Brownlow votes
    success2 = create_brownlow_votes_table()
    
    if success1 and success2:
        print("\n🎉 Database setup completed successfully!")
        print("📊 You can now store historical Brownlow votes in the database")
        print("🤖 The AI can learn from actual voting patterns")
        return True
    else:
        print("\n❌ Database setup failed")
        return False

if __name__ == "__main__":
    main() 