#!/usr/bin/env python3
"""
AI Content Style Guide for Footy Bets AI
Defines the tone, style, and voice for all AI-generated content on the website
"""

class FootyContentStyle:
    """
    Style guide for AI-generated content that appeals to AFL betting enthusiasts
    - Smart and knowledgeable about footy
    - Witty and entertaining without being corny
    - Human-sounding, like a knowledgeable mate at the pub
    - Appeals to people who bet on AFL
    """
    
    # Tone characteristics
    TONE_GUIDE = {
        "voice": "knowledgeable footy fan who knows their stuff",
        "attitude": "confident but not arrogant, with a bit of swagger",
        "humor": "witty observations, subtle jokes, footy banter",
        "language": "casual but intelligent, uses footy slang appropriately",
        "appeal": "targets people who understand the game and like to bet"
    }
    
    # Common phrases and expressions
    FOOTY_PHRASES = {
        "introductions": [
            "Righto, let's talk about...",
            "Alright, here's the deal...",
            "Listen up, footy fans...",
            "Here's what's going down...",
            "Let's break this down..."
        ],
        "conclusions": [
            "That's the way the cookie crumbles.",
            "That's footy for you.",
            "You can't argue with the numbers.",
            "The proof is in the pudding.",
            "That's how the cards fell."
        ],
        "emphasis": [
            "Let's be honest",
            "Here's the thing",
            "The bottom line is",
            "At the end of the day",
            "Truth be told"
        ],
        "positive_outcomes": [
            "got the chocolates",
            "took home the bacon",
            "came up trumps",
            "delivered the goods",
            "got the job done"
        ],
        "negative_outcomes": [
            "came up short",
            "didn't quite get there",
            "fell at the final hurdle",
            "missed the mark",
            "wasn't their day"
        ]
    }
    
    # Content templates for different sections
    CONTENT_TEMPLATES = {
        "analysis_intro": [
            "We've crunched the numbers and here's what the data is telling us.",
            "Our AI has been doing the heavy lifting, and here's what it reckons.",
            "Let's dive into the stats and see what's really going on here.",
            "Time to separate the wheat from the chaff with some proper analysis."
        ],
        
        "prediction_intro": [
            "Based on the numbers, here's who we reckon will {action}.",
            "The AI has spoken, and it's backing {subject} to {action}.",
            "If the stats are anything to go by, {subject} should {action}.",
            "Our crystal ball (powered by data) says {subject} will {action}."
        ],
        
        "stat_highlight": [
            "Here's the interesting bit - {stat}.",
            "This is where it gets good - {stat}.",
            "Pay attention to this - {stat}.",
            "This stat tells the story - {stat}."
        ],
        
        "betting_advice": [
            "If you're having a punt, this is worth considering.",
            "For the punters out there, here's something to think about.",
            "If you're putting your money where your mouth is...",
            "For those who like to back their judgment with cash..."
        ],
        
        "disclaimer": [
            "But hey, this is footy - anything can happen.",
            "Remember, this is just what the numbers say - the game isn't played on paper.",
            "Take this with a grain of salt - footy has a way of surprising us.",
            "Past performance doesn't guarantee future results, as they say."
        ]
    }
    
    # Writing rules and guidelines
    WRITING_RULES = {
        "sentence_structure": [
            "Use varied sentence lengths - mix short punchy sentences with longer explanatory ones",
            "Start sentences with action words when possible",
            "Use footy terminology naturally, not forced",
            "Keep paragraphs short and punchy"
        ],
        
        "vocabulary": [
            "Use footy slang appropriately (bloke, reckon, got the goods, etc.)",
            "Avoid overly formal language",
            "Don't be afraid to use contractions",
            "Use active voice over passive voice"
        ],
        
        "tone_balance": [
            "Be confident but not cocky",
            "Show expertise without being condescending",
            "Be entertaining without being silly",
            "Appeal to both casual fans and serious punters"
        ],
        
        "engagement": [
            "Ask rhetorical questions",
            "Use footy analogies and metaphors",
            "Reference current footy culture and trends",
            "Acknowledge the unpredictability of the game"
        ]
    }
    
    @staticmethod
    def generate_intro(topic: str, context: str = "") -> str:
        """Generate an engaging introduction for any topic"""
        import random
        
        intros = [
            f"Righto, let's talk about {topic}. We've crunched the numbers and here's what the data is telling us.",
            f"Alright, here's the deal with {topic}. Our AI has been doing the heavy lifting, and here's what it reckons.",
            f"Listen up, footy fans. When it comes to {topic}, the numbers don't lie.",
            f"Here's what's going down with {topic}. Time to separate the wheat from the chaff with some proper analysis."
        ]
        
        return random.choice(intros)
    
    @staticmethod
    def generate_prediction_text(subject: str, action: str, confidence: str = "medium") -> str:
        """Generate prediction text with appropriate confidence level"""
        import random
        
        if confidence == "high":
            templates = [
                f"The AI is pretty confident that {subject} will {action}.",
                f"Based on the numbers, {subject} should definitely {action}.",
                f"Our crystal ball (powered by data) says {subject} will {action}."
            ]
        elif confidence == "medium":
            templates = [
                f"The AI reckons {subject} will {action}.",
                f"If the stats are anything to go by, {subject} should {action}.",
                f"Our analysis suggests {subject} will {action}."
            ]
        else:  # low confidence
            templates = [
                f"The AI thinks {subject} might {action}.",
                f"There's a chance {subject} could {action}.",
                f"The numbers hint that {subject} may {action}."
            ]
        
        return random.choice(templates)
    
    @staticmethod
    def generate_stat_commentary(stat_name: str, value: str, context: str = "") -> str:
        """Generate commentary about a specific statistic"""
        import random
        
        templates = [
            f"Here's the interesting bit - {stat_name} is sitting at {value}.",
            f"This is where it gets good - {stat_name} shows {value}.",
            f"Pay attention to this - {stat_name} is telling us {value}.",
            f"This stat tells the story - {stat_name} at {value}."
        ]
        
        return random.choice(templates)
    
    @staticmethod
    def generate_conclusion(summary: str) -> str:
        """Generate a conclusion with footy-style ending"""
        import random
        
        conclusions = [
            f"{summary} That's footy for you.",
            f"{summary} You can't argue with the numbers.",
            f"{summary} The proof is in the pudding.",
            f"{summary} That's how the cards fell."
        ]
        
        return random.choice(conclusions)
    
    @staticmethod
    def add_betting_context(text: str) -> str:
        """Add betting context to existing text"""
        import random
        
        betting_additions = [
            " If you're having a punt, this is worth considering.",
            " For the punters out there, here's something to think about.",
            " If you're putting your money where your mouth is, keep this in mind.",
            " For those who like to back their judgment with cash, take note."
        ]
        
        return text + random.choice(betting_additions)
    
    @staticmethod
    def add_disclaimer(text: str) -> str:
        """Add appropriate disclaimer to text"""
        import random
        
        disclaimers = [
            " But hey, this is footy - anything can happen.",
            " Remember, this is just what the numbers say - the game isn't played on paper.",
            " Take this with a grain of salt - footy has a way of surprising us.",
            " Past performance doesn't guarantee future results, as they say."
        ]
        
        return text + random.choice(disclaimers)

# Example usage functions for different content types
def generate_game_analysis_content(game_data: dict) -> str:
    """Generate game analysis content with footy style"""
    style = FootyContentStyle()
    
    content = style.generate_intro(f"the {game_data['home_team']} vs {game_data['away_team']} clash")
    
    # Add game-specific analysis
    if game_data['home_score'] > game_data['away_score']:
        content += f"\n\n{game_data['home_team']} got the chocolates in this one, running out {game_data['home_score']}-{game_data['away_score']} winners."
    else:
        content += f"\n\n{game_data['away_team']} took home the bacon, getting up {game_data['away_score']}-{game_data['home_score']}."
    
    return content

def generate_player_analysis_content(player_data: dict) -> str:
    """Generate player analysis content with footy style"""
    style = FootyContentStyle()
    
    content = style.generate_intro(f"{player_data['name']}'s performance")
    
    # Add player-specific stats
    if player_data.get('goals', 0) > 0:
        content += f"\n\nThe bloke hit the scoreboard with {player_data['goals']} goals, which always gets the umpires' attention."
    
    if player_data.get('disposals', 0) > 25:
        content += f"\n\n{player_data['disposals']} disposals is nothing to sneeze at - that's some serious ball-winning ability."
    
    return content

def generate_season_summary_content(season_data: dict) -> str:
    """Generate season summary content with footy style"""
    style = FootyContentStyle()
    
    content = style.generate_intro(f"the {season_data['season']} season")
    
    # Add season highlights
    if season_data.get('winner'):
        content += f"\n\n{season_data['winner']['name']} took home the Brownlow with {season_data['winner']['votes']} votes - a dominant performance by any measure."
    
    return content 