/**
 * Multi-Tenant Cloudflare Worker Content & Analytics API
 * Handles fast article queries with stale-while-revalidate Edge Caching and D1 reads.
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    // CORS Headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // 1. GET /api/articles?site=ezmortgage&limit=20&category=all
      if (pathname === '/api/articles' && request.method === 'GET') {
        const siteId = url.searchParams.get('site') || 'ezmortgage';
        const limit = Math.min(parseInt(url.searchParams.get('limit') || '20'), 100);
        const category = url.searchParams.get('category');

        let query = `SELECT id, site_id, slug, title, category, author, date, iso_date, read_time, excerpt, image_url, views, likes 
                     FROM articles_hot 
                     WHERE site_id = ? AND status = 'published'`;
        const params = [siteId];

        if (category && category !== 'all') {
          query += ` AND category = ?`;
          params.push(category);
        }

        query += ` ORDER BY created_at DESC LIMIT ?`;
        params.push(limit);

        const { results } = await env.DB.prepare(query).bind(...params).all();

        return new Response(JSON.stringify({ success: true, site: siteId, count: results.length, data: results }), {
          headers: {
            ...corsHeaders,
            'Content-Type': 'application/json',
            // Edge Caching: 1 hr fresh, 24 hr edge cache, stale-while-revalidate background refresh
            'Cache-Control': 'public, max-age=3600, s-maxage=86400, stale-while-revalidate=86400',
          },
        });
      }

      // 2. POST /api/analytics/view
      if (pathname === '/api/analytics/view' && request.method === 'POST') {
        const body = await request.json();
        const { siteId, slug } = body;

        if (!siteId || !slug) {
          return new Response(JSON.stringify({ error: 'Missing siteId or slug' }), { status: 400, headers: corsHeaders });
        }

        // Asynchronous non-blocking increment in D1
        ctx.waitUntil(
          env.DB.prepare('UPDATE articles_hot SET views = views + 1 WHERE site_id = ? AND slug = ?')
            .bind(siteId, slug)
            .run()
        );

        return new Response(JSON.stringify({ success: true, message: 'View recorded' }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      return new Response(JSON.stringify({ message: 'Content & Analytics API Active' }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });

    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }
  },
};
