#!/usr/bin/env python3
"""
Multi-Season Brownlow Analysis Script
Analyzes multiple AFL seasons using Gemini AI and generates web content
"""

import sys
import os
import time
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_brownlow_analyzer import GeminiBrownlowAnalyzer
from generate_brownlow_web_content import generate_all_web_content

def analyze_multiple_seasons():
    """Analyze multiple seasons and generate web content"""
    print("🏆 Multi-Season Brownlow Medal Analysis")
    print("=" * 60)
    
    # Seasons to analyze
    seasons = [2020, 2021, 2022, 2023, 2024]
    
    # Initialize Gemini analyzer
    try:
        analyzer = GeminiBrownlowAnalyzer()
        print("✅ Gemini AI analyzer initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Gemini analyzer: {str(e)}")
        print("💡 Make sure GEMINI_API_KEY environment variable is set")
        return False
    
    # Analyze each season
    successful_seasons = []
    
    for season in seasons:
        print(f"\n🎮 Analyzing {season} season...")
        print("-" * 40)
        
        try:
            # Analyze the season
            results = analyzer.analyze_season_brownlow(season)
            
            if results and 'winner' in results:
                # Save results
                filename = analyzer.save_results(results)
                successful_seasons.append(season)
                
                winner = results['winner']
                print(f"✅ {season} analysis completed!")
                print(f"🏆 Predicted winner: {winner['player_name']} ({winner['team']}) with {winner['votes']} votes")
                print(f"💾 Results saved to: {filename}")
            else:
                print(f"❌ {season} analysis failed - no results generated")
                
        except Exception as e:
            print(f"❌ Error analyzing {season} season: {str(e)}")
            continue
        
        # Add delay between seasons to respect API limits
        if season != seasons[-1]:  # Don't delay after the last season
            print("⏳ Waiting 5 seconds before next season...")
            time.sleep(5)
    
    # Summary
    print(f"\n🎉 Multi-season analysis completed!")
    print(f"✅ Successfully analyzed {len(successful_seasons)} seasons: {successful_seasons}")
    
    if successful_seasons:
        print(f"\n🌐 Generating web content for all seasons...")
        try:
            generate_all_web_content()
            print(f"✅ Web content generation completed!")
        except Exception as e:
            print(f"❌ Error generating web content: {str(e)}")
            return False
    else:
        print("❌ No seasons were successfully analyzed")
        return False
    
    return True

def main():
    """Main function"""
    print("🤖 Multi-Season Brownlow Medal Analysis with Gemini AI")
    print("=" * 70)
    
    success = analyze_multiple_seasons()
    
    if success:
        print(f"\n🎉 All tasks completed successfully!")
        print(f"📁 Check the 'brownlow_web_content' directory for generated pages")
        print(f"📊 Analysis files are saved in the current directory")
    else:
        print(f"\n❌ Some tasks failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 