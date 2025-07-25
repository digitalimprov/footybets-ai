#!/usr/bin/env python3
"""
Web Content Generator for Brownlow Medal Results
Generates SEO-friendly HTML pages for Brownlow Medal predictions and results
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generate_html_template(title: str, meta_description: str, content: str, canonical_url: str = None) -> str:
    """Generate HTML template with SEO optimization"""
    if not canonical_url:
        canonical_url = "https://footybets.ai/brownlow-medal-predictions"
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="Brownlow Medal, Brownlow Medal Predictor, AFL, Australian Football, player statistics, predictions, AI analysis, football betting, Brownlow votes, AFL betting">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{meta_description}">
    <link rel="canonical" href="{canonical_url}">
    
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        .brownlow-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .brownlow-table th, .brownlow-table td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        .brownlow-table th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        .brownlow-table tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .brownlow-table tr:hover {{
            background-color: #e8f4fd;
        }}
        .vote-3 {{ background-color: #ffd700; font-weight: bold; }}
        .vote-2 {{ background-color: #c0c0c0; font-weight: bold; }}
        .vote-1 {{ background-color: #cd7f32; font-weight: bold; }}
        .game-result {{
            background: #ecf0f1;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        .stat-item {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }}
        .round-navigation {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .round-nav-button {{
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
        }}
        .round-nav-button:hover {{
            background-color: #2980b9;
            text-decoration: none;
        }}
        .round-nav-button.disabled {{
            background-color: #bdc3c7;
            cursor: not-allowed;
        }}
        .breadcrumb {{
            background-color: #f8f9fa;
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .breadcrumb a {{
            color: #3498db;
        }}
        .disclaimer {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-style: italic;
        }}
        .stat-value {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        .winner {{
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
        
        <div class="footer">
            <p>© 2025 Footy Bets AI - AI-Powered AFL Analysis</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </div>
</body>
</html>"""

def generate_season_overview_page(season_data: Dict) -> str:
    """Generate the main season overview page"""
    season = season_data['season']
    player_standings = season_data['player_standings']
    winner = season_data['winner']
    
    # Generate content
    content = f"""
    <div class="breadcrumb">
        <a href="/brownlow-medal-predictions">Brownlow Medal Predictions</a> > {season} Season
    </div>
    
    <h1>{season} Brownlow Medal Predictor & Results</h1>
    
    <div class="disclaimer">
        <strong>📝 Important Note:</strong> These predictions were generated using AI analysis of historical data and were not made before the rounds were played. They are used to train and validate our AI prediction models for future seasons. The analysis shows how our AI would have predicted the Brownlow votes based on player statistics.
    </div>
    
    <p>Righto, let's talk about the {season} Brownlow Medal race. We've crunched the numbers, analyzed every disposal, tackle, and goal, and our AI has spat out some predictions that'll either make you look like a genius at the pub or have you questioning everything you know about footy.</p>
    
    <p>This isn't your mate's hot take from the couch – we've got the data to back it up. Every game, every player, every stat that matters when the umpires are scribbling down their votes.</p>
    
    <h2>🏆 The AI's Pick for Brownlow Glory</h2>
    """
    
    if winner:
        content += f"""
        <div class="winner">
            <h3>🏅 {winner['player_name']}</h3>
            <p><strong>{winner['team']}</strong></p>
            <p><strong>{winner['votes']} votes</strong></p>
            <p><em>Our Gemini AI reckons this bloke's got the goods. {winner['votes']} votes is nothing to sneeze at – that's some serious consistency across the season.</em></p>
        </div>
        """
    
    content += """
    <h2>📊 The Ladder – Who's In The Mix</h2>
    <p>Here's how our AI sees the Brownlow race playing out. These are the blokes who've been tearing it up week in, week out:</p>
    <table class="brownlow-table">
        <thead>
            <tr>
                <th>Position</th>
                <th>Player</th>
                <th>Team</th>
                <th>Total Votes</th>
                <th>Games Voted</th>
                <th>Best Performance</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for player in player_standings[:10]:  # Top 10
        content += f"""
            <tr>
                <td>{player['rank']}</td>
                <td>{player['player_name']}</td>
                <td>{player['team']}</td>
                <td><strong>{player['total_votes']}</strong></td>
                <td>{player['games_with_votes']}</td>
                <td>{player['vote_breakdown']['3']}x3, {player['vote_breakdown']['2']}x2, {player['vote_breakdown']['1']}x1</td>
            </tr>
        """
    
        content += """
    </tbody>
    </table>
    
    <h2>📋 Round-by-Round Breakdown</h2>
    <p>Want to see how the votes stack up each week? Click through to see who our AI reckons got the chocolates in each round:</p>
    <ul>
    """
    
    # Add round links
    for round_num in season_data['round_results'].keys():
        content += f'<li><a href="brownlow-{season}-round-{round_num}.html">Round {round_num} Predictions</a></li>\n'
    
    content += """
    </ul>
    
    <h2>🤖 How Our AI Works Its Magic</h2>
    <p>Alright, here's the science bit. Our AI doesn't just throw darts at a board – it's analyzing everything that matters when the umpires are making their calls:</p>
    <ul>
        <li><strong>Disposals:</strong> The bread and butter. Kicks, handballs, and how clean they are</li>
        <li><strong>Goals & Behinds:</strong> The scoreboard impact. Nothing gets the umpires' attention like hitting the scoreboard</li>
        <li><strong>Tackles & Clearances:</strong> The grunt work. The stuff that doesn't always show up in the highlights but wins games</li>
        <li><strong>Inside 50s & Rebound 50s:</strong> The pressure acts. Getting the ball forward and stopping it coming back</li>
        <li><strong>Contested Possessions:</strong> The hard stuff. When the game's on the line, who's getting the ball?</li>
        <li><strong>Team Performance:</strong> The winning factor. Umpires love a winner, let's be honest</li>
    </ul>
    
    <p>Plus, we've thrown in some bonus points for the blokes who go big when it matters – 30+ disposal games, multiple goals, that sort of thing. Because that's what gets you noticed on Brownlow night.</p>
    """
    
    return generate_html_template(
        f"{season} Brownlow Medal Predictor & Results | Footy Bets AI",
        f"Complete {season} Brownlow Medal predictor analysis, round-by-round voting predictions, and final standings. AI-powered Brownlow Medal predictor for AFL betting.",
        content,
        f"https://footybets.ai/brownlow-medal-predictions/{season}"
    )

def generate_round_page(season_data: Dict, round_num: int) -> str:
    """Generate a page for a specific round with SEO-friendly navigation"""
    season = season_data['season']
    
    if round_num not in season_data['round_results']:
        return ""
    
    games = season_data['round_results'][round_num]
    
    # Get all available rounds for navigation
    all_rounds = sorted(season_data['round_results'].keys())
    
    all_rounds = sorted(all_rounds)
    current_round_index = all_rounds.index(round_num) if round_num in all_rounds else -1
    
    # Generate navigation
    nav_content = '<div class="round-navigation">'
    
    # Previous round button
    if current_round_index > 0:
        prev_round = all_rounds[current_round_index - 1]
        nav_content += f'<a href="brownlow-{season}-round-{prev_round}.html" class="round-nav-button">← Round {prev_round}</a>'
    else:
        nav_content += '<span class="round-nav-button disabled">← Previous Round</span>'
    
    # Current round indicator
    nav_content += f'<span><strong>Round {round_num}</strong></span>'
    
    # Next round button
    if current_round_index < len(all_rounds) - 1:
        next_round = all_rounds[current_round_index + 1]
        nav_content += f'<a href="brownlow-{season}-round-{next_round}.html" class="round-nav-button">Round {next_round} →</a>'
    else:
        nav_content += '<span class="round-nav-button disabled">Next Round →</span>'
    
    nav_content += '</div>'
    
    content = f"""
    <div class="breadcrumb">
        <a href="/brownlow-medal-predictions">Brownlow Medal Predictions</a> > 
        <a href="brownlow-{season}.html">{season} Season</a> > 
        Round {round_num}
    </div>
    
    <h1>{season} Brownlow Medal Predictor Round {round_num}</h1>
    
    <div class="disclaimer">
        <strong>📝 Important Note:</strong> These predictions were generated using AI analysis of historical data and were not made before Round {round_num} was played. They are used to train and validate our AI prediction models for future seasons.
    </div>
    
    {nav_content}
    
    <p>Round {round_num} of {season} – this is where the Brownlow race really heats up. Our AI has crunched the numbers and here's who it reckons got the umpires' attention this week.</p>
    
    <h2>🎮 Round {round_num} – Who Got The Votes?</h2>
    """
    
    for game_data in games:
        game = game_data['game']
        votes = game_data['votes']
        
        content += f"""
        <div class="game-result">
            <h3>{game['home_team']} {game['home_score']} - {game['away_score']} {game['away_team']}</h3>
            
            <h4>🏆 The Votes – Who Got The Chocolates?</h4>
            <table class="brownlow-table">
                <thead>
                    <tr>
                        <th>Position</th>
                        <th>Player</th>
                        <th>Team</th>
                        <th>Votes</th>
                        <th>Reasoning</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for i, vote in enumerate(votes):
            vote_class = f"vote-{vote['votes']}"
            
            content += f"""
                <tr class="{vote_class}">
                    <td>{i+1}</td>
                    <td>{vote['player_name']}</td>
                    <td>{vote['team_name']}</td>
                    <td><strong>{vote['votes']}</strong></td>
                    <td>{vote.get('reasoning', 'Gemini AI analysis')}</td>
                </tr>
            """
        
        content += """
                </tbody>
            </table>
        </div>
        """
    
    content += f"""
    <h2>📊 Round {round_num} Wrap</h2>
    <p>That's {len(games)} games down for Round {round_num}. Some blokes made their case for the Brownlow, others might want to forget this week ever happened. That's footy.</p>
    
    <p><a href="brownlow-{season}.html">← Back to {season} Season Overview</a></p>
    """
    
    return generate_html_template(
        f"{season} Brownlow Medal Predictor Round {round_num} | Footy Bets AI",
        f"Round {round_num} Brownlow Medal predictor analysis for {season}. AI-powered Brownlow vote predictions for each game.",
        content,
        f"https://footybets.ai/brownlow-medal-predictions/{season}/round-{round_num}"
    )

def generate_all_web_content():
    """Generate all web content for Brownlow Medal results"""
    print("🌐 Generating Brownlow Medal Web Content")
    print("=" * 50)
    
    # Look for Gemini Brownlow analysis files
    analysis_files = []
    for file in os.listdir('.'):
        if file.startswith('gemini_brownlow_analysis_') and file.endswith('.json'):
            analysis_files.append(file)
    
    if not analysis_files:
        print("❌ No Gemini Brownlow analysis files found")
        print("💡 Run the Gemini Brownlow analyzer first to generate analysis files")
        return
    
    # Use the most recent file for each season
    season_files = {}
    for file in analysis_files:
        # Extract season from filename: gemini_brownlow_analysis_2024_20250725_123456.json
        parts = file.replace('.json', '').split('_')
        if len(parts) >= 4:
            season = int(parts[3])  # 2024
            season_files[season] = file
    
    if not season_files:
        print("❌ No valid Gemini Brownlow analysis files found")
        return
    
    print(f"📊 Found analysis files for seasons: {list(season_files.keys())}")
    
    # Load all season data
    all_results = {}
    for season, filename in season_files.items():
        with open(filename, 'r', encoding='utf-8') as f:
            all_results[season] = json.load(f)
    
    # Create output directory
    output_dir = "brownlow_web_content"
    os.makedirs(output_dir, exist_ok=True)
    
    total_pages = 0
    
    for season, season_data in all_results.items():
        print(f"\n📊 Generating content for {season} season...")
        
        # Generate season overview page
        season_html = generate_season_overview_page(season_data)
        season_filename = f"{output_dir}/brownlow-{season}.html"
        
        with open(season_filename, 'w', encoding='utf-8') as f:
            f.write(season_html)
        
        print(f"  ✅ Created: brownlow-{season}.html")
        total_pages += 1
        
        # Generate round pages
        for round_num in season_data['round_results'].keys():
            round_html = generate_round_page(season_data, round_num)
            
            if round_html:
                round_filename = f"{output_dir}/brownlow-{season}-round-{round_num}.html"
                
                with open(round_filename, 'w', encoding='utf-8') as f:
                    f.write(round_html)
                
                print(f"  ✅ Created: brownlow-{season}-round-{round_num}.html")
                total_pages += 1
    
    # Generate index page
    index_content = """
    <h1>🏆 Brownlow Medal Predictor & Results</h1>
    
    <div class="disclaimer">
        <strong>📝 Important Note:</strong> These predictions were generated using AI analysis of historical data and were not made before the rounds were played. They are used to train and validate our AI prediction models for future seasons. The analysis shows how our AI would have predicted the Brownlow votes based on player statistics.
    </div>
    
    <p>Welcome to the ultimate Brownlow Medal analysis – where AI meets footy smarts. We've crunched the numbers from 2020-2024 to give you the inside scoop on who should've won the Brownlow, who got robbed, and who the umpires might've been watching a bit too closely.</p>
    
    <p>This isn't just some algorithm spitting out random numbers. We've analyzed every disposal, tackle, goal, and clearance to predict how the Brownlow voting should've played out. Whether you're a punter looking for an edge or just a footy tragic who loves a good debate, you've come to the right place.</p>
    
    <h2>📊 Season Results – The Good, The Bad, and The Controversial</h2>
    <ul>
    """
    
    for season in sorted(all_results.keys(), reverse=True):
        season_data = all_results[season]
        winner = season_data['winner'] if 'winner' in season_data else None
        
        index_content += f"""
        <li>
            <a href="brownlow-{season}.html"><strong>{season} Season</strong></a>
            {f" - Our Gemini AI reckons {winner['player_name']} ({winner['team']}) should've taken home the chocolates with {winner['votes']} votes" if winner else ""}
        </li>
        """
    
    index_content += """
    </ul>
    
    <h2>🤖 How We Work Our Magic</h2>
    <p>Alright, let's get technical for a minute. Our AI doesn't just pick names out of a hat – it's analyzing everything that matters when the umpires are making their calls:</p>
    <ul>
        <li><strong>Disposal Efficiency:</strong> It's not just about getting the ball, it's about what you do with it</li>
        <li><strong>Scoreboard Impact:</strong> Goals and behinds – the stuff that gets you noticed</li>
        <li><strong>Defensive Pressure:</strong> Tackles, clearances, the grunt work that wins games</li>
        <li><strong>Midfield Dominance:</strong> The engine room players who control the tempo</li>
        <li><strong>Winning Factor:</strong> Let's face it, umpires love a winner</li>
        <li><strong>Historical Patterns:</strong> What's worked in the past and what the umpires tend to notice</li>
    </ul>
    
    <p>We've fed it years of Brownlow voting data, player statistics, and game outcomes. The result? Predictions that are as close as you'll get to having a crystal ball for the Brownlow Medal.</p>
    
    <p>Whether you're using this for your footy tipping, having a punt, or just settling arguments at the pub, you've got the data to back up your claims. No more "I reckon" – now you can say "the AI reckons" and actually have something to show for it.</p>
    """
    
    index_html = generate_html_template(
        "Brownlow Medal Predictor & Results | Footy Bets AI",
        "AI-powered Brownlow Medal predictor for AFL seasons 2020-2024. Complete round-by-round voting predictions and final standings. The ultimate Brownlow Medal predictor for AFL betting.",
        index_content,
        "https://footybets.ai/brownlow-medal-predictions"
    )
    
    with open(f"{output_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"\n🎉 Web content generation complete!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📄 Total pages generated: {total_pages + 1}")
    print(f"🌐 Main index: {output_dir}/index.html")

if __name__ == "__main__":
    generate_all_web_content() 