# AI Content System for Footy Bets AI

## Overview

This system provides a consistent, engaging, and footy-focused voice across all AI-generated content on the website. The content is designed to appeal to AFL betting enthusiasts with a smart, witty, and knowledgeable tone.

## Style Guide

### Voice & Tone
- **Voice**: Knowledgeable footy fan who knows their stuff
- **Attitude**: Confident but not arrogant, with a bit of swagger
- **Humor**: Witty observations, subtle jokes, footy banter
- **Language**: Casual but intelligent, uses footy slang appropriately
- **Appeal**: Targets people who understand the game and like to bet

### Key Characteristics
- Smart and knowledgeable about footy
- Witty and entertaining without being corny
- Human-sounding, like a knowledgeable mate at the pub
- Appeals to people who bet on AFL

## Usage Examples

### 1. Game Predictions
```python
from ai_content_generator import FootyContentGenerator

generator = FootyContentGenerator()

prediction_data = {
    'home_team': 'Collingwood',
    'away_team': 'Carlton',
    'predicted_winner': 'Collingwood',
    'predicted_margin': 12,
    'confidence': 'high',
    'key_factors': [
        'Collingwood\'s strong midfield performance',
        'Carlton\'s injury concerns',
        'Recent form trends'
    ]
}

content = generator.generate_prediction_content(prediction_data)
```

**Output**: "Righto, let's talk about the Collingwood vs Carlton clash. We've crunched the numbers and here's what the data is telling us. The AI is pretty confident that Collingwood will get up by 12 points..."

### 2. Player Analysis
```python
player_data = {
    'name': 'Patrick Cripps',
    'team': 'Carlton',
    'recent_form': {'avg_disposals': 28},
    'season_stats': {'goals': 15, 'disposals': 27},
    'last_game': {'opponent': 'Essendon', 'disposals': 32, 'goals': 2}
}

content = generator.generate_player_analysis(player_data)
```

**Output**: "Righto, let's talk about Patrick Cripps's form. We've crunched the numbers and here's what the data is telling us. The bloke's been in ripping form lately, averaging 28 disposals over the last few weeks..."

### 3. Team Analysis
```python
team_data = {
    'name': 'Melbourne',
    'season_record': {'wins': 15, 'losses': 7},
    'recent_form': {'wins': 3, 'games': 5},
    'key_players': [
        {'name': 'Clayton Oliver', 'role': 'Midfield star'},
        {'name': 'Christian Petracca', 'role': 'Forward threat'}
    ]
}

content = generator.generate_team_analysis(team_data)
```

## Content Types

### 1. Predictions
- Game outcome predictions
- Margin predictions
- Player performance predictions
- Team performance predictions

### 2. Analysis
- Player form analysis
- Team season analysis
- Statistical insights
- Trend analysis

### 3. Tips & Betting
- Weekly tips
- Betting advice
- Value bets
- Risk assessments

### 4. News & Updates
- Breaking news
- Injury updates
- Team changes
- Impact analysis

### 5. Brownlow Medal
- Round-by-round predictions
- Season standings
- Player vote analysis
- Historical comparisons

## Implementation Guidelines

### 1. Always Use the Style Guide
```python
# ✅ Good
content = generator.generate_prediction_content(data)

# ❌ Bad
content = "The AI predicts that Team A will win by 10 points."
```

### 2. Include Betting Context
```python
# The generator automatically adds betting context
content = generator.generate_prediction_content(data)
# Automatically includes: "If you're having a punt, this is worth considering."
```

### 3. Add Appropriate Disclaimers
```python
# The generator automatically adds disclaimers
content = generator.generate_prediction_content(data)
# Automatically includes: "But hey, this is footy - anything can happen."
```

### 4. Use SEO Optimization
```python
seo_data = generator.generate_seo_content('prediction', data)
# Returns: meta_title, meta_description, h1_title, content
```

## Content Templates

### Introductions
- "Righto, let's talk about..."
- "Alright, here's the deal..."
- "Listen up, footy fans..."
- "Here's what's going down..."

### Conclusions
- "That's footy for you."
- "You can't argue with the numbers."
- "The proof is in the pudding."
- "That's how the cards fell."

### Emphasis
- "Let's be honest"
- "Here's the thing"
- "The bottom line is"
- "At the end of the day"

### Positive Outcomes
- "got the chocolates"
- "took home the bacon"
- "came up trumps"
- "delivered the goods"

### Negative Outcomes
- "came up short"
- "didn't quite get there"
- "fell at the final hurdle"
- "missed the mark"

## Integration Points

### 1. Frontend Integration
```javascript
// In your React/Vue components
const content = await fetch('/api/generate-content', {
    method: 'POST',
    body: JSON.stringify({
        type: 'prediction',
        data: predictionData
    })
});
```

### 2. API Endpoints
```python
# In your FastAPI routes
@app.post("/api/generate-content")
async def generate_content(request: ContentRequest):
    generator = FootyContentGenerator()
    content = generator.generate_page_content(request.type, request.data)
    return {"content": content}
```

### 3. Database Integration
```python
# Store generated content for caching
content = generator.generate_prediction_content(data)
db.store_generated_content(content, data['game_id'])
```

## Best Practices

### 1. Consistency
- Always use the FootyContentGenerator for AI content
- Don't mix formal and casual tones
- Maintain the footy-focused voice throughout

### 2. Accuracy
- Ensure data is accurate before generating content
- Include confidence levels when appropriate
- Always add disclaimers for predictions

### 3. Engagement
- Use footy analogies and metaphors
- Reference current footy culture and trends
- Acknowledge the unpredictability of the game

### 4. SEO
- Include relevant keywords naturally
- Use proper heading structure
- Optimize meta descriptions and titles

## Content Categories

### High Confidence Content
- Historical analysis
- Statistical trends
- Completed game analysis
- Player career statistics

### Medium Confidence Content
- Season predictions
- Team form analysis
- Player performance predictions
- Betting recommendations

### Low Confidence Content
- Future game predictions
- Injury impact assessments
- Weather-related predictions
- Speculative betting tips

## Monitoring & Improvement

### 1. Content Performance
- Track engagement metrics
- Monitor user feedback
- Analyze conversion rates
- Review SEO performance

### 2. Style Refinement
- Regular review of tone consistency
- Update phrases and expressions
- Refine betting context additions
- Improve disclaimer messaging

### 3. User Feedback
- Collect user comments
- Monitor social media mentions
- Analyze user behavior patterns
- Incorporate user suggestions

## Technical Implementation

### File Structure
```
backend/
├── ai_content_style_guide.py      # Style guide and templates
├── ai_content_generator.py        # Main content generator
├── generate_brownlow_web_content.py # Brownlow-specific content
└── AI_CONTENT_GUIDE.md           # This documentation
```

### Dependencies
- Python 3.9+
- No external dependencies beyond standard library
- Integrates with existing database models
- Compatible with FastAPI/Flask backends

### Performance Considerations
- Content generation is fast (milliseconds)
- Can be cached for static content
- Supports real-time generation for dynamic content
- Minimal memory footprint

## Future Enhancements

### 1. Personalization
- User-specific content preferences
- Team loyalty considerations
- Betting history integration
- Custom content recommendations

### 2. Advanced Analytics
- Content performance tracking
- A/B testing capabilities
- User engagement metrics
- Conversion optimization

### 3. Multi-language Support
- Australian English (current)
- International English variants
- Localized footy terminology
- Cultural adaptation

### 4. Content Types
- Video script generation
- Podcast episode descriptions
- Social media posts
- Email newsletter content

## Support & Maintenance

### Regular Updates
- Monthly style guide reviews
- Quarterly content performance analysis
- Annual tone and voice assessment
- Continuous improvement based on user feedback

### Quality Assurance
- Automated content validation
- Style consistency checks
- SEO optimization verification
- User experience testing

This system ensures that all AI-generated content on the Footy Bets AI website maintains a consistent, engaging, and footy-focused voice that appeals to the target audience of AFL betting enthusiasts. 