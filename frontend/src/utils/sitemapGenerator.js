// Utility for generating dynamic sitemaps with SEO-optimized URLs
import { urlStructure, generateGameUrl, generateTeamSlug } from './urlStructure';

export const generateSitemap = (games = [], predictions = []) => {
  const baseUrl = 'https://footybets.ai';
  const currentDate = new Date().toISOString().split('T')[0];
  const currentSeason = new Date().getFullYear();
  
  const staticPages = [
    {
      url: urlStructure.home,
      lastmod: currentDate,
      changefreq: 'daily',
      priority: '1.0'
    },
    {
      url: urlStructure.tips.index,
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.9'
    },
    {
      url: urlStructure.predictions.index,
      lastmod: currentDate,
      changefreq: 'daily',
      priority: '0.8'
    },
    {
      url: urlStructure.analytics.index,
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.7'
    },
    {
      url: urlStructure.games.index,
      lastmod: currentDate,
      changefreq: 'daily',
      priority: '0.8'
    }
  ];

  // Add round-based tips pages
  const roundPages = [];
  const uniqueRounds = [...new Set(games.map(g => g.round_number))].sort((a, b) => b - a);
  uniqueRounds.forEach(round => {
    roundPages.push({
      url: urlStructure.tips.round(round),
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.8'
    });
  });

  // Add season-based tips pages
  const seasonPages = [];
  const uniqueSeasons = [...new Set(games.map(g => g.season))].sort((a, b) => b - a);
  uniqueSeasons.forEach(season => {
    seasonPages.push({
      url: urlStructure.tips.season(season),
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.7'
    });
  });

  // Add team pages
  const teamPages = [];
  const uniqueTeams = [...new Set(games.flatMap(g => [g.home_team_name, g.away_team_name]))];
  uniqueTeams.forEach(teamName => {
    const teamSlug = generateTeamSlug(teamName);
    teamPages.push({
      url: urlStructure.team.tips(teamSlug),
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.7'
    });
  });

  // Add individual game prediction pages (SEO gold)
  const gamePages = games.map(game => ({
    url: generateGameUrl(game),
    lastmod: game.updated_at || currentDate,
    changefreq: 'weekly',
    priority: '0.8'
  }));

  // Add fixture pages
  const fixturePages = [
    {
      url: urlStructure.games.upcoming,
      lastmod: currentDate,
      changefreq: 'daily',
      priority: '0.7'
    },
    {
      url: urlStructure.games.results,
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.6'
    }
  ];

  // Add season fixture pages
  uniqueSeasons.forEach(season => {
    fixturePages.push({
      url: urlStructure.games.season(season),
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.6'
    });
  });

  // Add round fixture pages
  uniqueRounds.forEach(round => {
    fixturePages.push({
      url: urlStructure.games.round(round, currentSeason),
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.6'
    });
  });

  // Add analytics pages
  const analyticsPages = [
    {
      url: urlStructure.analytics.performance,
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.6'
    },
    {
      url: urlStructure.analytics.accuracy,
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.6'
    },
    {
      url: urlStructure.analytics.trends,
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.6'
    }
  ];

  const allPages = [
    ...staticPages,
    ...roundPages,
    ...seasonPages,
    ...teamPages,
    ...gamePages,
    ...fixturePages,
    ...analyticsPages
  ];

  // Generate XML
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allPages.map(page => `  <url>
    <loc>${baseUrl}${page.url}</loc>
    <lastmod>${page.lastmod}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  return xml;
};

// Generate robots.txt content
export const generateRobotsTxt = () => {
  return `User-agent: *
Allow: /

# Disallow admin and private pages
Disallow: /admin/
Disallow: /login
Disallow: /scraping
Disallow: /api/
Disallow: /_next/
Disallow: /static/

# Allow important SEO pages
Allow: /
Allow: /afl-betting-tips
Allow: /afl-betting-tips/
Allow: /afl-prediction/
Allow: /afl-analysis/
Allow: /afl-team/
Allow: /afl-analytics
Allow: /afl-fixtures
Allow: /ai-predictions

# Legacy routes (redirects)
Allow: /tips
Allow: /predictions
Allow: /analytics
Allow: /games

# Sitemap location
Sitemap: https://footybets.ai/sitemap.xml

# Crawl delay for better server performance
Crawl-delay: 1`;
}; 