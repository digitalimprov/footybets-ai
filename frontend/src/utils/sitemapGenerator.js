// Utility for generating dynamic sitemaps
export const generateSitemap = (games = [], predictions = []) => {
  const baseUrl = 'https://footybets.ai';
  const currentDate = new Date().toISOString().split('T')[0];
  
  const staticPages = [
    {
      url: '/',
      lastmod: currentDate,
      changefreq: 'daily',
      priority: '1.0'
    },
    {
      url: '/tips',
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.9'
    },
    {
      url: '/predictions',
      lastmod: currentDate,
      changefreq: 'daily',
      priority: '0.8'
    },
    {
      url: '/analytics',
      lastmod: currentDate,
      changefreq: 'weekly',
      priority: '0.7'
    },
    {
      url: '/games',
      lastmod: currentDate,
      changefreq: 'daily',
      priority: '0.8'
    }
  ];

  // Add game pages
  const gamePages = games.map(game => ({
    url: `/games/${game.id}`,
    lastmod: game.updated_at || currentDate,
    changefreq: 'weekly',
    priority: '0.7'
  }));

  // Add prediction pages (if we have dedicated prediction pages)
  const predictionPages = predictions.map(prediction => ({
    url: `/predictions/${prediction.id}`,
    lastmod: prediction.created_at || currentDate,
    changefreq: 'monthly',
    priority: '0.6'
  }));

  const allPages = [...staticPages, ...gamePages, ...predictionPages];

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
Disallow: /login
Disallow: /scraping
Disallow: /admin/
Disallow: /api/
Disallow: /_next/
Disallow: /static/

# Allow important pages
Allow: /
Allow: /tips
Allow: /predictions
Allow: /analytics
Allow: /games

# Sitemap location
Sitemap: https://footybets.ai/sitemap.xml

# Crawl delay (optional)
Crawl-delay: 1`;
}; 