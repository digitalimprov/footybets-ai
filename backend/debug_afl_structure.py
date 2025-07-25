#!/usr/bin/env python3
"""
Debug script to examine AFL tables structure for games and player stats
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from bs4 import BeautifulSoup
import json

def debug_afl_structure():
    print("🔍 Debugging AFL Tables structure...")
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    # Step 1: Get all game links for round 1, 2024
    round_url = "https://afltables.com/afl/seas/2024.html"
    print(f"📄 Fetching season page: {round_url}")
    response = session.get(round_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links to game pages (they end with .html and are not the main season page)
    game_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('games/') and href.endswith('.html'):
            game_links.append("https://afltables.com/afl/" + href)
    print(f"Found {len(game_links)} game links in 2024 season.")
    if not game_links:
        print("No game links found!")
        return
    print("First 5 game links:")
    for link in game_links[:5]:
        print(link)

    # Step 2: Fetch the first game page and print the structure of player stats tables
    first_game_url = game_links[0]
    print(f"\nFetching first game page: {first_game_url}")
    game_resp = session.get(first_game_url)
    game_soup = BeautifulSoup(game_resp.text, 'html.parser')

    # Print all tables and their first few rows to inspect structure
    tables = game_soup.find_all('table')
    print(f"Found {len(tables)} tables on the game page.")
    for idx, table in enumerate(tables):
        print(f"\nTable {idx}:")
        rows = table.find_all('tr')
        for r_idx, row in enumerate(rows[:5]):
            print([cell.get_text(strip=True) for cell in row.find_all(['th','td'])])
        if idx >= 2:  # Only print first 3 tables for brevity
            break

if __name__ == "__main__":
    debug_afl_structure() 