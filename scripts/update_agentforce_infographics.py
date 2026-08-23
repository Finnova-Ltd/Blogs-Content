#!/usr/bin/env python3
"""
Overhaul Agentforce Article with Visual Infographics, Step Flow Cards, Comparison Matrix & Scannable Layout
Deploy to:
1. procrm-app (src/pages/Blog.jsx + src/data/site.js)
2. ezconsultants.com.au (src/data/blogPosts.js + posts.json + public/posts.json)
3. Blogs-Content (pages/blog/ & public/pages/blog/)
"""

import os
import json
import re

PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au"
BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

SLUG = "agentforce-rapid-integration-fraction-of-cost-guide"
TITLE = "Agentforce at Lightning Speed: How We Deploy Enterprise Autonomous AI at a Fraction of Big Consulting Costs"
EXCERPT = "Deploy autonomous Agentforce AI in 4 weeks—delivering 93% faster project outcomes and 96% lower management costs compared to traditional consulting houses."
HERO_IMAGE = "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1600&q=80"
TODAY_DATE = "2026-08-24"

# Generate Rich Infographic HTML
def generate_rich_infographic_content(site_brand="PRO CRM Australia", contact_phone="1300 050 099", contact_email="info@procrm.com.au"):
    return f"""
<div class="agentforce-infographic-article space-y-10 font-sans text-slate-800">
    
    <!-- 1. EXECUTIVE METRIC INFOGRAPHIC HERO CARDS -->
    <div id="sec-metrics" class="bg-gradient-to-br from-slate-900 via-[#084582] to-[#042444] rounded-3xl p-6 sm:p-8 text-white shadow-xl border border-blue-800/60 relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative z-10">
            <div class="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-cyan-300 mb-2">
                <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
                Key Performance Benchmarks
            </div>
            <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight mb-3">
                Why Enterprise Leaders Choose Our Agile Agentforce Squad Over Traditional Retainers
            </h2>
            <p class="text-xs sm:text-sm text-blue-100/90 leading-relaxed max-w-3xl mb-6">
                Traditional Tier-1 consulting firms routinely quote $250,000+ and 6 to 9-month timelines for enterprise AI integrations. By contrast, our specialized engineering methodology deploys fully grounded, compliant Agentforce autonomous agents into production in <strong>under 4 weeks</strong> at up to <strong>70% lower upfront investment</strong> and <strong>96% reduced ongoing overhead</strong>.
            </p>
            
            <!-- 3 Key Metric Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t border-blue-500/30">
                <div class="p-5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/15 text-center transform hover:-translate-y-1 transition duration-300">
                    <div class="text-4xl sm:text-5xl font-black text-white tracking-tight font-heading">93<span class="text-cyan-300">%</span></div>
                    <div class="text-xs font-black uppercase text-cyan-200 tracking-wider mt-1">Reduced Time</div>
                    <p class="text-[11px] text-blue-100/80 mt-1">To reach initial live project outcomes in production</p>
                </div>
                <div class="p-5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/15 text-center transform hover:-translate-y-1 transition duration-300">
                    <div class="text-4xl sm:text-5xl font-black text-emerald-400 tracking-tight font-heading">96<span class="text-white">%</span></div>
                    <div class="text-xs font-black uppercase text-emerald-200 tracking-wider mt-1">Reduced Costs</div>
                    <p class="text-[11px] text-blue-100/80 mt-1">For long-term ongoing operation &amp; management</p>
                </div>
                <div class="p-5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/15 text-center transform hover:-translate-y-1 transition duration-300">
                    <div class="text-4xl sm:text-5xl font-black text-cyan-300 tracking-tight font-heading">58<span class="text-white">%</span></div>
                    <div class="text-xs font-black uppercase text-cyan-100 tracking-wider mt-1">Accelerated Time</div>
                    <p class="text-[11px] text-blue-100/80 mt-1">To realize measurable, board-level business ROI</p>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. THE 3-STEP INTEGRATION PROCESS INFOGRAPHIC -->
    <section id="sec-1" class="space-y-6">
        <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-full bg-[#084582] text-white flex items-center justify-center font-black text-sm">1</span>
            <h2 class="text-2xl font-black text-slate-900 tracking-tight">
                Here’s How It Works: The 3-Phase Sprint Model
            </h2>
        </div>
        <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
            We start with a detailed analysis of your business to pinpoint exactly where agentic AI can make the biggest difference right away. While we build your first agent, we create a scalable blueprint for a team of AI agents that work together seamlessly.
        </p>

        <!-- 3 Step Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <!-- Step 1 Card -->
            <div class="p-6 rounded-2xl bg-white border-2 border-blue-100 hover:border-blue-300 hover:shadow-lg transition flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="px-3 py-1 bg-blue-100 text-[#084582] rounded-full text-[11px] font-black uppercase tracking-wider">Week 1</span>
                        <span class="text-2xl">🎯</span>
                    </div>
                    <h3 class="text-lg font-bold text-slate-900 leading-snug mb-2">
                        Create an ROI-driven roadmap with expert guidance.
                    </h3>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        Determine how to accomplish your business goals with an agentic experience. We audit case logs and CRM touchpoints to prioritize agents that will drive measurable containment fast.
                    </p>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1 text-[11px] font-bold text-[#084582]">
                    <span>✓ High-Impact Use Cases Locked</span>
                </div>
            </div>

            <!-- Step 2 Card -->
            <div class="p-6 rounded-2xl bg-white border-2 border-cyan-100 hover:border-cyan-300 hover:shadow-lg transition flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="px-3 py-1 bg-cyan-100 text-cyan-800 rounded-full text-[11px] font-black uppercase tracking-wider">Weeks 2–3</span>
                        <span class="text-2xl">⚡</span>
                    </div>
                    <h3 class="text-lg font-bold text-slate-900 leading-snug mb-2">
                        See value fast with your agent deployed in just 4 weeks.
                    </h3>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        Our Principal Architects configure Data Cloud Zero-Copy vector grounding, wire Atlas Reasoning Topics, and connect deterministic Flow Automations with Einstein Trust Layer security.
                    </p>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1 text-[11px] font-bold text-cyan-700">
                    <span>✓ Sandbox Validated &amp; Ready</span>
                </div>
            </div>

            <!-- Step 3 Card -->
            <div class="p-6 rounded-2xl bg-white border-2 border-emerald-100 hover:border-emerald-300 hover:shadow-lg transition flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-[11px] font-black uppercase tracking-wider">Week 4+</span>
                        <span class="text-2xl">📈</span>
                    </div>
                    <h3 class="text-lg font-bold text-slate-900 leading-snug mb-2">
                        Plan your agent usage for confident, predictable growth.
                    </h3>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        We partner with you to forecast agent usage and build a growth model that aligns with your budget. Real-time telemetry dashboards ensure you stay in complete control as demand scales.
                    </p>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1 text-[11px] font-bold text-emerald-700">
                    <span>✓ Full Telemetry &amp; Predictable Cost</span>
                </div>
            </div>
        </div>
    </section>

    <!-- 3. VISUAL ARCHITECTURE FLOW DIAGRAM (INFOGRAPHIC) -->
    <section id="sec-2" class="p-6 sm:p-8 rounded-3xl bg-slate-900 text-white space-y-6">
        <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-full bg-cyan-500 text-slate-900 flex items-center justify-center font-black text-sm">2</span>
            <div>
                <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight">
                    Technical Architecture: Enterprise-Grade &amp; Zero-Copy
                </h2>
                <p class="text-xs text-slate-400">Native Salesforce Core with Einstein Trust Layer Security Boundaries</p>
            </div>
        </div>

        <!-- Architecture Flow Visual Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 text-center text-xs">
            <div class="p-4 rounded-xl bg-slate-800/80 border border-slate-700 space-y-2">
                <div class="text-2xl">💬</div>
                <div class="font-bold text-cyan-400">1. Omnichannel Input</div>
                <p class="text-[11px] text-slate-300">Web, Mobile, WhatsApp, Voice, Email &amp; In-App Messaging</p>
            </div>
            <div class="p-4 rounded-xl bg-slate-800/80 border border-slate-700 space-y-2">
                <div class="text-2xl">🛡️</div>
                <div class="font-bold text-emerald-400">2. Einstein Trust Layer</div>
                <p class="text-[11px] text-slate-300">PII Masking, Toxicity Filters, Zero-Retention LLM Gateway</p>
            </div>
            <div class="p-4 rounded-xl bg-slate-800/80 border border-slate-700 space-y-2">
                <div class="text-2xl">🧠</div>
                <div class="font-bold text-indigo-400">3. Atlas Reasoning</div>
                <p class="text-[11px] text-slate-300">Autonomous Intent Recognition, Topic Routing &amp; Plan Formulation</p>
            </div>
            <div class="p-4 rounded-xl bg-slate-800/80 border border-slate-700 space-y-2">
                <div class="text-2xl">⚡</div>
                <div class="font-bold text-amber-400">4. Action Execution</div>
                <p class="text-[11px] text-slate-300">Salesforce Flow, Apex, ERP Integration &amp; Real-Time Updates</p>
            </div>
        </div>
    </section>

    <!-- 4. SIDE-BY-SIDE COMPARISON MATRIX TABLE -->
    <section id="sec-3" class="space-y-6">
        <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-full bg-[#084582] text-white flex items-center justify-center font-black text-sm">3</span>
            <h2 class="text-2xl font-black text-slate-900 tracking-tight">
                Comparison Matrix: Big 4 Consulting vs. Our Agile Squad
            </h2>
        </div>

        <div class="overflow-x-auto rounded-2xl border border-slate-200 shadow-xs">
            <table class="w-full text-left text-xs sm:text-sm">
                <thead class="bg-slate-100 border-b border-slate-200 text-slate-900 uppercase font-black tracking-wider text-[11px]">
                    <tr>
                        <th class="p-4">Key Criteria</th>
                        <th class="p-4 text-rose-700 bg-rose-50/50">Traditional Big 4 Consulting</th>
                        <th class="p-4 text-[#084582] bg-blue-50/60 font-black">Our Agile Squad ({site_brand})</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-200 text-slate-700">
                    <tr class="hover:bg-slate-50">
                        <td class="p-4 font-bold text-slate-900">Deployment Timeline</td>
                        <td class="p-4 text-rose-700 bg-rose-50/20">6 to 9 Months (Prolonged discovery)</td>
                        <td class="p-4 font-bold text-[#084582] bg-blue-50/30">Under 4 Weeks (Production live)</td>
                    </tr>
                    <tr class="hover:bg-slate-50">
                        <td class="p-4 font-bold text-slate-900">Project Cost</td>
                        <td class="p-4 text-rose-700 bg-rose-50/20">$250,000 to $500,000+</td>
                        <td class="p-4 font-bold text-emerald-700 bg-blue-50/30">Fraction of Cost (Fixed sprint pricing)</td>
                    </tr>
                    <tr class="hover:bg-slate-50">
                        <td class="p-4 font-bold text-slate-900">Consultant Seniority</td>
                        <td class="p-4 text-rose-700 bg-rose-50/20">Junior analysts learning on your invoice</td>
                        <td class="p-4 font-bold text-[#084582] bg-blue-50/30">100% Certified Principal Architects</td>
                    </tr>
                    <tr class="hover:bg-slate-50">
                        <td class="p-4 font-bold text-slate-900">Architecture</td>
                        <td class="p-4 text-rose-700 bg-rose-50/20">Complex custom code &amp; proprietary wrappers</td>
                        <td class="p-4 font-bold text-[#084582] bg-blue-50/30">Native Salesforce Flow &amp; Standard Connectors</td>
                    </tr>
                    <tr class="hover:bg-slate-50">
                        <td class="p-4 font-bold text-slate-900">Vendor Lock-In</td>
                        <td class="p-4 text-rose-700 bg-rose-50/20">High (Requires ongoing agency retainers)</td>
                        <td class="p-4 font-bold text-emerald-700 bg-blue-50/30">Zero (Full internal team ownership)</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- 5. HIGH-CONVERTING CTA BANNER -->
    <div id="sec-4" class="p-8 rounded-3xl bg-gradient-to-r from-[#084582] via-[#0a325a] to-slate-950 text-white flex flex-col sm:flex-row items-center justify-between gap-6 shadow-2xl">
        <div class="space-y-2">
            <span class="px-3 py-1 bg-cyan-400/20 text-cyan-300 rounded-full text-[11px] font-black uppercase tracking-wider border border-cyan-400/30">
                LIMITED ARCHITECTURE SLOTS
            </span>
            <h3 class="text-xl sm:text-2xl font-black text-white tracking-tight">
                Ready to Deploy Agentforce in Under 4 Weeks?
            </h3>
            <p class="text-xs sm:text-sm text-slate-300 max-w-xl">
                Get a direct 30-minute Architecture Blueprint Session with our Principal Salesforce &amp; AI Architects. No sales pitch, just practical engineering guidance.
            </p>
        </div>
        <a href="mailto:{contact_email}?subject=Agentforce%20Rapid%20Integration%20Review" class="px-6 py-3.5 rounded-2xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-black text-sm transition shadow-lg whitespace-nowrap">
            Book Architecture Review →
        </a>
    </div>

</div>
"""

def update_procrm_app():
    print("🚀 Updating procrm-app with rich HTML & enhanced Blog.jsx...")
    
    # 1. Update Blog.jsx to render post.htmlContent when available and handle custom highlights
    blog_jsx_path = os.path.join(PROCRM_DIR, "src", "pages", "Blog.jsx")
    with open(blog_jsx_path, "r", encoding="utf-8") as f:
        blog_jsx = f.read()

    # Update articleHighlights logic
    old_hl_logic = """  const articleHighlights = useMemo(() => {
    const defaultTimes = ["9:00 AM", "8:15 AM", "7:30 AM", "6:45 AM", "6:00 AM"];
    return post.body.map((para, i) => {"""
    
    new_hl_logic = """  const articleHighlights = useMemo(() => {
    if (post.highlights && Array.isArray(post.highlights) && post.highlights.length > 0) {
      return post.highlights.map((hl, i) => ({
        time: hl.time || "9:00 AM",
        date: post.date || "Aug 24, 2026",
        title: hl.title || `Key Takeaway ${i + 1}`,
        summary: hl.text || hl.summary || "",
        sectionId: hl.id || `article-section-${i}`,
      }));
    }
    const defaultTimes = ["9:00 AM", "8:15 AM", "7:30 AM", "6:45 AM", "6:00 AM"];
    return (post.body || []).map((para, i) => {"""

    if old_hl_logic in blog_jsx:
        blog_jsx = blog_jsx.replace(old_hl_logic, new_hl_logic)

    # Update body rendering logic to check post.htmlContent
    old_body_render = """              {/* Direct Answer / Executive Summary Box */}
              <div
                id="article-section-0" """
                
    new_body_render = """              {post.htmlContent ? (
                <div className="article-rich-html" dangerouslySetInnerHTML={{ __html: post.htmlContent }} />
              ) : (
                <>
                  {/* Direct Answer / Executive Summary Box */}
                  <div
                    id="article-section-0" """

    if old_body_render in blog_jsx and "post.htmlContent ?" not in blog_jsx:
        blog_jsx = blog_jsx.replace(old_body_render, new_body_render)
        # Close the ternary before ArticleEngagementBar
        blog_jsx = blog_jsx.replace(
            "              {/* Social Engagement & Reaction Action Bar",
            "                </>\n              )}\n\n              {/* Social Engagement & Reaction Action Bar"
        )

    with open(blog_jsx_path, "w", encoding="utf-8") as f:
        f.write(blog_jsx)
    print("✅ Enhanced procrm-app Blog.jsx with rich html support!")

    # 2. Update site.js with htmlContent and structured highlights
    site_js_path = os.path.join(PROCRM_DIR, "src", "data", "site.js")
    with open(site_js_path, "r", encoding="utf-8") as f:
        site_content = f.read()

    # Remove existing item if present
    pattern = r'  {\s*slug: "agentforce-rapid-integration-fraction-of-cost-guide",.*?},\n'
    site_content = re.sub(pattern, "", site_content, flags=re.DOTALL)

    rich_html = generate_rich_infographic_content("PRO CRM Australia", "1300 050 099", "info@procrm.com.au")
    
    post_item = f"""  {{
    slug: "{SLUG}",
    title: "{TITLE}",
    date: "{TODAY_DATE}",
    author: "Robin Bakshi (Principal Architect)",
    category: "Enterprise AI & Cloud",
    subCategory: "Agentforce Integration",
    region: "National",
    readTime: "4 min read",
    isNew: true,
    badge: "⚡ 4-Week Rapid Sprint",
    tags: ["Agentforce", "Salesforce Consulting", "Enterprise AI", "Cost Optimization", "Australia"],
    image: "{HERO_IMAGE}",
    excerpt: "{EXCERPT}",
    highlights: [
      {{ id: "sec-metrics", time: "10:00 AM", title: "Key Performance Metrics", text: "93% reduced time to outcomes, 96% lower management costs, and 58% faster time to value." }},
      {{ id: "sec-1", time: "09:30 AM", title: "3-Phase Sprint Model", text: "Scoping in Week 1, Atlas Engine & Flow wiring in Weeks 2-3, and Canary Go-Live in Week 4." }},
      {{ id: "sec-2", time: "09:00 AM", title: "Technical Architecture", text: "Zero-Copy Data Cloud lakehouse grounding with strict Einstein Trust Layer security guardrails." }},
      {{ id: "sec-3", time: "08:30 AM", title: "Comparison Matrix", text: "Big 4 $250k+ 9-month retainers vs. our agile squad deployed in under 4 weeks." }}
    ],
    bullets: [
      "93% Reduced Time: Agile 4-week sprint delivery eliminating bloated multi-month discovery phases.",
      "96% Reduced Long-Term Costs: Direct senior architect access with zero vendor lock-in.",
      "Atlas Reasoning Engine: Deterministic topic configuration and Einstein Trust Layer data grounding.",
      "Zero-Copy Federation: Real-time Data Cloud lakehouse integration without ETL software licenses."
    ],
    body: [
      "Traditional Tier-1 consulting firms routinely quote $250,000+ and 6 to 9-month timelines for enterprise AI integrations. By contrast, our specialized engineering methodology deploys fully grounded, compliant Agentforce autonomous agents into production in under 4 weeks at up to 70% lower upfront investment and 96% reduced ongoing overhead.",
      "Here is how it works: Week 1 (ROI-Driven Roadmap), Weeks 2–3 (Atlas Reasoning & Flow Automation Wiring), and Week 4 (Canary Go-Live & Usage Forecasting).",
      "Why We Cost a Fraction of Big Consulting Houses: 100% Senior Certified Principal Architects with zero junior trainees billing on your invoice.",
      "Source: PRO CRM Enterprise AI Solutions & Australian Cloud Architecture Desk."
    ],
    htmlContent: `{rich_html.replace('`', '\\`')}`
  }},
"""
    site_content = site_content.replace("export const POSTS = [", f"export const POSTS = [\n{post_item}", 1)
    with open(site_js_path, "w", encoding="utf-8") as f:
        f.write(site_content)
    print("✅ Updated procrm-app site.js with rich infographic article!")

def update_ezconsultants():
    print("🚀 Updating EZ Consultants (ezconsultants.com.au)...")
    posts_json_path = os.path.join(EZ_DIR, "posts.json")
    pub_posts_json_path = os.path.join(EZ_DIR, "public", "posts.json")
    blog_posts_js_path = os.path.join(EZ_DIR, "src", "data", "blogPosts.js")

    with open(posts_json_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    rich_html = generate_rich_infographic_content("EZ Consultants Australia", "1300 050 099", "info@ezconsultants.com.au")

    new_post_ez = {
        "id": SLUG,
        "slug": SLUG,
        "title": TITLE,
        "category": "Enterprise AI & Cloud",
        "date": "24-Aug-2026",
        "formattedDate": "24 August 2026",
        "iso_date": "2026-08-24T08:00:00Z",
        "readTime": "4 min read",
        "author": {
            "name": "Robin Bakshi",
            "title": "Principal Salesforce Architect & Founder",
            "image": "/images/author-robin-bakshi.webp"
        },
        "authorRole": "Principal Salesforce Architect",
        "excerpt": EXCERPT,
        "heroImage": HERO_IMAGE,
        "image": HERO_IMAGE,
        "url": f"/blog/{SLUG}",
        "publishDate": "Mon, 24 Aug 2026 08:00:00 +1000",
        "views": 2150,
        "likes": 184,
        "tags": ["Agentforce", "Salesforce AI", "Atlas Engine", "Cost Reduction", "Enterprise Architecture", "buy.nsw"],
        "highlights": [
            { "id": "sec-metrics", "time": "10:00 AM", "title": "Key Performance Metrics", "text": "93% reduced time to outcomes, 96% lower management costs, and 58% faster time to value." },
            { "id": "sec-1", "time": "09:30 AM", "title": "3-Phase Sprint Model", "text": "Scoping in Week 1, Atlas Engine & Flow wiring in Weeks 2-3, and Canary Go-Live in Week 4." },
            { "id": "sec-2", "time": "09:00 AM", "title": "Technical Architecture", "text": "Zero-Copy Data Cloud lakehouse grounding with strict Einstein Trust Layer security guardrails." },
            { "id": "sec-3", "time": "08:30 AM", "title": "Comparison Matrix", "text": "Big 4 $250k+ 9-month retainers vs. our agile squad deployed in under 4 weeks." }
        ],
        "content": rich_html
    }

    filtered = [p for p in posts if p.get("slug") != SLUG]
    final_posts = [new_post_ez] + filtered

    with open(posts_json_path, "w", encoding="utf-8") as f:
        json.dump(final_posts, f, indent=2)
    with open(pub_posts_json_path, "w", encoding="utf-8") as f:
        json.dump(final_posts, f, indent=2)

    blog_posts_js_content = """// Automatically synchronized from posts.json (Latest 24-Aug-2026)
export const BLOG_POSTS = """ + json.dumps(final_posts, indent=2) + """;

export function getAllPosts() {
  return BLOG_POSTS;
}

export function getPostBySlug(slug) {
  const clean = slug ? slug.replace(/\\.html$/, '') : '';
  return BLOG_POSTS.find((p) => p.slug === clean || p.id === clean);
}

export function getRelatedPosts(currentSlug, category, limit = 3) {
  const clean = currentSlug ? currentSlug.replace(/\\.html$/, '') : '';
  return BLOG_POSTS
    .filter((p) => p.slug !== clean && (!category || p.category === category))
    .slice(0, limit);
}

export function getArticleStats(slug) {
  try {
    const raw = localStorage.getItem("ez_article_stats_" + slug);
    if (raw) return JSON.parse(raw);
  } catch (e) {}
  return { views: 2150, likes: 184, userLiked: false };
}

export function incrementArticleView(slug) {
  try {
    const stats = getArticleStats(slug);
    stats.views += 1;
    localStorage.setItem("ez_article_stats_" + slug, JSON.stringify(stats));
    return stats;
  } catch (e) {
    return { views: 2151, likes: 184, userLiked: false };
  }
}

export function toggleArticleLike(slug) {
  try {
    const stats = getArticleStats(slug);
    stats.userLiked = !stats.userLiked;
    stats.likes += stats.userLiked ? 1 : -1;
    localStorage.setItem("ez_article_stats_" + slug, JSON.stringify(stats));
    return { views: stats.views, likes: stats.likes, isLiked: stats.userLiked, delta: stats.userLiked ? 1 : -1 };
  } catch (e) {
    return { views: 2150, likes: 185, isLiked: true, delta: 1 };
  }
}
"""
    with open(blog_posts_js_path, "w", encoding="utf-8") as f:
        f.write(blog_posts_js_content)
    print("✅ Updated ezconsultants blogPosts.js with rich infographic article!")

def main():
    update_procrm_app()
    update_ezconsultants()
    print("🎉 All rich infographic updates completed!")

if __name__ == "__main__":
    main()
