export default {
  // 1. Fetch Handler: allows on-demand /trigger-blog-sync webhook calls
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Health check endpoint
    if (url.pathname === "/" || url.pathname === "/health") {
      return new Response(JSON.stringify({
        status: "healthy",
        service: "jules-autopost-orchestrator",
        version: "1.0.0",
        governed_by: "SEO_CONTENT_QUALITY_GATES.md",
        endpoints: {
          trigger: "POST /trigger-blog-sync",
          health: "GET /health"
        }
      }, null, 2), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }

    // Secure on-demand webhook trigger route
    if (url.pathname === "/trigger-blog-sync") {
      if (request.method !== "POST" && request.method !== "GET") {
        return new Response(JSON.stringify({ error: "Method not allowed. Use POST." }), {
          status: 405,
          headers: { "Content-Type": "application/json" }
        });
      }

      const authHeader = request.headers.get("Authorization");
      if (env.WEBHOOK_SECRET && (!authHeader || authHeader !== `Bearer ${env.WEBHOOK_SECRET}`)) {
        return new Response(JSON.stringify({ error: "Unauthorized. Valid Bearer WEBHOOK_SECRET required." }), {
          status: 401,
          headers: { "Content-Type": "application/json" }
        });
      }

      // Asynchronously dispatch the ingestion and Jules loop without blocking the edge runtime
      ctx.waitUntil(this.triggerPipeline(env));

      return new Response(JSON.stringify({
        status: "queued",
        message: "Autopost quality pipeline and Jules guard successfully dispatched.",
        timestamp: new Date().toISOString()
      }, null, 2), {
        status: 202,
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response(JSON.stringify({ error: "Not Found" }), {
      status: 404,
      headers: { "Content-Type": "application/json" }
    });
  },

  // 2. Central Dispatch Logic
  async triggerPipeline(env) {
    const repos = [
      { owner: "Finnova-Ltd", repo: "ezmortgagebroker", workflow: "daily_rss_publisher.yml" },
      { owner: "Finnova-Ltd", repo: "Blogs-Content", workflow: "daily_rss_publisher.yml" },
      { owner: "Finnova-Ltd", repo: "ezconsultants.com.au", workflow: "daily_rss_publisher.yml" }
    ];

    const ghToken = env.GITHUB_TOKEN || env.GH_TOKEN;
    if (!ghToken) {
      console.warn("No GITHUB_TOKEN configured in worker env. Skipping workflow_dispatch.");
      return;
    }

    for (const r of repos) {
      try {
        const dispatchUrl = `https://api.github.com/repos/${r.owner}/${r.repo}/actions/workflows/${r.workflow}/dispatches`;
        const resp = await fetch(dispatchUrl, {
          method: "POST",
          headers: {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": `Bearer ${ghToken}`,
            "User-Agent": "Cloudflare-Worker-Jules-Orchestrator"
          },
          body: JSON.stringify({ ref: "main" })
        });
        console.log(`Dispatched ${r.repo} workflow: Status ${resp.status}`);
      } catch (err) {
        console.error(`Failed to dispatch ${r.repo}:`, err.message);
      }
    }
  }
};
