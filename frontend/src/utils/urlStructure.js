// SEO-optimized URL structure for FootyBets.ai
export const urlStructure = {
  // Main pages
  home: '/',
  dashboard: '/dashboard',
  
  // Tips and predictions (most important for SEO)
  tips: {
    index: '/afl-betting-tips',
    round: (roundNumber) => `/afl-betting-tips/round-${roundNumber}`,
    season: (season) => `/afl-betting-tips/${season}`,
    team: (teamSlug) => `/afl-betting-tips/team/${teamSlug}`,
    upcoming: '/afl-betting-tips/upcoming',
    today: '/afl-betting-tips/today',
    weekend: '/afl-betting-tips/weekend'
  },
  
  // Individual game predictions (SEO gold)
  game: {
    detail: (homeTeam, awayTeam, round, season) => 
      `/afl-prediction/${homeTeam}-vs-${awayTeam}-round-${round}-${season}`,
    tips: (homeTeam, awayTeam, round, season) => 
      `/afl-betting-tips/${homeTeam}-vs-${awayTeam}-round-${round}-${season}`,
    analysis: (homeTeam, awayTeam, round, season) => 
      `/afl-analysis/${homeTeam}-vs-${awayTeam}-round-${round}-${season}`
  },
  
  // Team pages
  team: {
    predictions: (teamSlug) => `/afl-team/${teamSlug}/predictions`,
    tips: (teamSlug) => `/afl-team/${teamSlug}/betting-tips`,
    stats: (teamSlug) => `/afl-team/${teamSlug}/statistics`,
    history: (teamSlug) => `/afl-team/${teamSlug}/history`
  },
  
  // Analytics and stats
  analytics: {
    index: '/afl-analytics',
    performance: '/afl-analytics/performance',
    accuracy: '/afl-analytics/accuracy',
    trends: '/afl-analytics/trends',
    comparison: '/afl-analytics/comparison'
  },
  
  // Games and fixtures
  games: {
    index: '/afl-fixtures',
    upcoming: '/afl-fixtures/upcoming',
    results: '/afl-fixtures/results',
    season: (season) => `/afl-fixtures/${season}`,
    round: (round, season) => `/afl-fixtures/${season}/round-${round}`
  },
  
  // Predictions (AI-focused)
  predictions: {
    index: '/ai-predictions',
    upcoming: '/ai-predictions/upcoming',
    accuracy: '/ai-predictions/accuracy',
    generate: '/ai-predictions/generate'
  },
  
  // Admin (hidden from SEO)
  admin: {
    login: '/admin/login',
    scraping: '/admin/scraping',
    dashboard: '/admin/dashboard',
    analytics: '/admin/analytics',
    settings: '/admin/settings'
  }
};

// URL generation helpers
export const generateGameUrl = (game) => {
  if (!game) return null;
  
  const homeTeam = game.home_team_name?.toLowerCase().replace(/\s+/g, '-');
  const awayTeam = game.away_team_name?.toLowerCase().replace(/\s+/g, '-');
  const round = game.round_number;
  const season = game.season;
  
  return urlStructure.game.detail(homeTeam, awayTeam, round, season);
};

export const generateTipsUrl = (game) => {
  if (!game) return null;
  
  const homeTeam = game.home_team_name?.toLowerCase().replace(/\s+/g, '-');
  const awayTeam = game.away_team_name?.toLowerCase().replace(/\s+/g, '-');
  const round = game.round_number;
  const season = game.season;
  
  return urlStructure.game.tips(homeTeam, awayTeam, round, season);
};

export const generateTeamSlug = (teamName) => {
  return teamName?.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
};

// SEO-friendly title generation
export const generateSEOTitle = (type, data) => {
  switch (type) {
    case 'game':
      return `${data.homeTeam} vs ${data.awayTeam} - Round ${data.round} ${data.season} AFL Prediction & Betting Tips`;
    case 'tips':
      return `AFL Betting Tips Round ${data.round} ${data.season} - Expert Predictions & Analysis`;
    case 'team':
      return `${data.teamName} AFL Betting Tips & Predictions ${data.season}`;
    case 'round':
      return `Round ${data.round} AFL Betting Tips ${data.season} - AI Predictions & Expert Analysis`;
    default:
      return 'AFL Betting Tips & Predictions - AI-Powered Analysis';
  }
};

// SEO-friendly description generation
export const generateSEODescription = (type, data) => {
  switch (type) {
    case 'game':
      return `Get AI-powered AFL prediction for ${data.homeTeam} vs ${data.awayTeam} Round ${data.round}. Expert betting tips, predicted scores, and analysis.`;
    case 'tips':
      return `Round ${data.round} AFL betting tips and predictions for ${data.season}. AI-powered analysis with expert betting recommendations.`;
    case 'team':
      return `${data.teamName} AFL betting tips and predictions for ${data.season}. Get expert analysis and AI predictions.`;
    default:
      return 'Get AI-powered AFL betting tips and predictions. Expert analysis, confidence scores, and betting recommendations.';
  }
};

// Canonical URL generation
export const generateCanonicalUrl = (path) => {
  const baseUrl = 'https://footybets.ai';
  return `${baseUrl}${path}`;
}; 