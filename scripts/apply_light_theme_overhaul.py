#!/usr/bin/env python3
"""
Light Theme Overhaul & Clean Highlights Refinement:
1. Replace all dark background boxes with crisp, premium light-theme cards.
2. Remove timestamps from Highlights widget (replace with clean Step/Takeaway badges).
3. Remove inner scrollbar from sidebar (clean sticky layout without cramped scrollbars).
4. Update across procrm-app, ezconsultants.com.au, and Blogs-Content.
"""

import os
import json
import re

PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
EZ_DIR = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au"
BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

SLUG = "agentforce-rapid-integration-fraction-of-cost-guide"
TITLE = "Agentforce at Lightning Speed: How We Deploy Enterprise Autonomous AI at a Fraction of Big Consulting Costs"
EXCERPT = "Discover how agile Salesforce architects deploy autonomous Agentforce AI agents in under 4 weeks—delivering 93% faster project outcomes and 96% lower management costs compared to traditional consulting houses."
HERO_IMAGE = "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1600&q=80"
TODAY_DATE = "2026-08-24"

# 1. Generate 100% Light Theme Rich HTML (No dark boxes)
def generate_light_theme_article_html(site_brand="PRO CRM Australia", contact_phone="1300 050 099", contact_email="info@procrm.com.au"):
    return f"""
<div class="agentforce-light-article space-y-10 font-sans text-slate-800 leading-relaxed text-base">
    
    <!-- 1. EXECUTIVE METRIC HERO INFOGRAPHIC (100% Crisp Light Theme) -->
    <div id="sec-metrics" class="bg-gradient-to-br from-blue-50/90 via-indigo-50/40 to-white rounded-3xl p-6 sm:p-8 border-2 border-blue-200/80 shadow-sm relative overflow-hidden">
        <div class="relative z-10 space-y-4">
            <div class="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-[#084582]">
                <span class="w-2.5 h-2.5 rounded-full bg-[#084582] animate-pulse"></span>
                Executive Briefing &amp; Key Acceleration Benchmarks
            </div>
            <h2 class="text-xl sm:text-2xl lg:text-3xl font-black text-slate-900 tracking-tight leading-snug font-heading">
                Why Enterprise Leaders Choose Our Agile Agentforce Squad Over Traditional Retainers
            </h2>
            <p class="text-sm sm:text-base text-slate-700 leading-relaxed max-w-3xl">
                Traditional Tier-1 consulting firms routinely quote $250,000+ and 6 to 9-month timelines for enterprise AI integrations. By contrast, our specialized engineering methodology deploys fully grounded, compliant Agentforce autonomous agents into production in <strong>under 4 weeks</strong> at up to <strong>70% lower upfront investment</strong> and <strong>96% reduced ongoing overhead</strong>.
            </p>
            
            <!-- 3 Key Metric Cards (Pure White with Crisp Borders) -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t border-blue-200/60">
                <div class="p-5 rounded-2xl bg-white border border-blue-100 text-center shadow-xs hover:shadow-md transition">
                    <div class="text-4xl sm:text-5xl font-black text-[#084582] tracking-tight font-heading">93<span class="text-blue-500">%</span></div>
                    <div class="text-xs font-black uppercase text-slate-800 tracking-wider mt-1.5">Reduced Time</div>
                    <p class="text-xs text-slate-500 mt-1">To reach initial live project outcomes in production</p>
                </div>
                <div class="p-5 rounded-2xl bg-white border border-blue-100 text-center shadow-xs hover:shadow-md transition">
                    <div class="text-4xl sm:text-5xl font-black text-emerald-600 tracking-tight font-heading">96<span class="text-emerald-400">%</span></div>
                    <div class="text-xs font-black uppercase text-slate-800 tracking-wider mt-1.5">Reduced Costs</div>
                    <p class="text-xs text-slate-500 mt-1">For long-term ongoing operation &amp; management</p>
                </div>
                <div class="p-5 rounded-2xl bg-white border border-blue-100 text-center shadow-xs hover:shadow-md transition">
                    <div class="text-4xl sm:text-5xl font-black text-[#0077c8] tracking-tight font-heading">58<span class="text-cyan-500">%</span></div>
                    <div class="text-xs font-black uppercase text-slate-800 tracking-wider mt-1.5">Accelerated Time</div>
                    <p class="text-xs text-slate-500 mt-1">To realize measurable, board-level business ROI</p>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. SECTION 1: THE TRADITIONAL CONSULTING TRAP -->
    <section id="sec-1" class="space-y-4">
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight border-b border-slate-200 pb-3 font-heading">
            1. The Traditional Consulting Trap vs. Agile Agentic AI
        </h2>
        <p class="text-slate-700 leading-relaxed">
            For over two decades, enterprise technology deployments have suffered from a bloated consulting playbook. Traditional system integrators staff engagements with layers of junior analysts who learn on your project invoice, leading to multi-month discovery cycles and fragile custom LLM wrappers.
        </p>
        <p class="text-slate-700 leading-relaxed">
            <strong>Agentforce shifts the paradigm completely.</strong> Because Agentforce is embedded directly within Salesforce Core, the underlying security, data residency, and identity management are already handled natively by the <strong>Einstein Trust Layer</strong>. Rather than spending hundreds of billable hours constructing custom middleware, modern enterprises require senior architects who can ground Data Cloud sources and wire deterministic Flow Automations in days.
        </p>
    </section>

    <!-- 3. SECTION 2: THE 3-PHASE SPRINT MODEL (VISUAL CARDS) -->
    <section id="sec-2" class="space-y-6">
        <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-full bg-[#084582] text-white flex items-center justify-center font-black text-sm">2</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight font-heading">
                Here’s How It Works: The 3-Phase Sprint Model
            </h2>
        </div>
        <p class="text-slate-700 leading-relaxed">
            We start with a detailed analysis of your business to pinpoint exactly where agentic AI can make the biggest difference right away. While we build your first agent, we create a scalable plan for a team of AI agents that work together seamlessly for a truly agentic experience.
        </p>

        <!-- 3 Step Process Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            <!-- Step 1 Card -->
            <div class="p-6 rounded-2xl bg-white border-2 border-blue-100 hover:border-blue-300 hover:shadow-lg transition flex flex-col justify-between">
                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="px-3 py-1 bg-blue-100 text-[#084582] rounded-full text-xs font-black uppercase tracking-wider">Phase 1 (Week 1)</span>
                        <span class="text-2xl">🎯</span>
                    </div>
                    <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug font-heading">
                        Create an ROI-driven roadmap with expert guidance.
                    </h3>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        Determine how to accomplish your goals with an agentic experience. We audit inbound case logs and CRM touchpoints to prioritize agents that drive measurable results, fast.
                    </p>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1 text-xs font-bold text-[#084582]">
                    <span>✓ High-Containment Journeys Locked</span>
                </div>
            </div>

            <!-- Step 2 Card -->
            <div class="p-6 rounded-2xl bg-white border-2 border-cyan-100 hover:border-cyan-300 hover:shadow-lg transition flex flex-col justify-between">
                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="px-3 py-1 bg-cyan-100 text-cyan-800 rounded-full text-xs font-black uppercase tracking-wider">Phase 2 (Weeks 2–3)</span>
                        <span class="text-2xl">⚡</span>
                    </div>
                    <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug font-heading">
                        See value fast with your agent deployed in just 4 weeks.
                    </h3>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        Our Principal Architects configure Data Cloud Zero-Copy vector grounding, wire Atlas Reasoning Topics, and connect deterministic Flow Automations with Einstein Trust Layer guardrails.
                    </p>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1 text-xs font-bold text-cyan-700">
                    <span>✓ Sandbox Validated &amp; Ready</span>
                </div>
            </div>

            <!-- Step 3 Card -->
            <div class="p-6 rounded-2xl bg-white border-2 border-emerald-100 hover:border-emerald-300 hover:shadow-lg transition flex flex-col justify-between">
                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-black uppercase tracking-wider">Phase 3 (Week 4+)</span>
                        <span class="text-2xl">📈</span>
                    </div>
                    <h3 class="text-base sm:text-lg font-bold text-slate-900 leading-snug font-heading">
                        Plan your agent usage for confident, predictable growth.
                    </h3>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        We partner with you to forecast agent usage and build a growth model that aligns with your budget. Real-time telemetry dashboards ensure you stay in complete control as demand scales.
                    </p>
                </div>
                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1 text-xs font-bold text-emerald-700">
                    <span>✓ Full Telemetry &amp; Predictable Cost</span>
                </div>
            </div>
        </div>
    </section>

    <!-- 4. SECTION 3: TECHNICAL ARCHITECTURE (CRISP LIGHT CARD) -->
    <section id="sec-3" class="p-6 sm:p-8 rounded-3xl bg-slate-50 border border-slate-200 space-y-6">
        <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-full bg-[#084582] text-white flex items-center justify-center font-black text-sm">3</span>
            <div>
                <h2 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight font-heading">
                    Technical Architecture: Enterprise-Grade &amp; Zero-Copy
                </h2>
                <p class="text-xs text-slate-500">Native Salesforce Core with Einstein Trust Layer Security Boundaries</p>
            </div>
        </div>

        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
            Unlike fragmented open-source AI frameworks that require exposing your internal customer data to third-party APIs, Agentforce ensures that data never leaves your secure Salesforce perimeter:
        </p>

        <!-- Architecture Flow Visual Grid (Light Cards) -->
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 text-center text-xs">
            <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-2">
                <div class="text-2xl">💬</div>
                <div class="font-bold text-[#084582] text-sm font-heading">1. Omnichannel Input</div>
                <p class="text-[11px] text-slate-500">Web, Mobile, WhatsApp, Voice, Email &amp; In-App Messaging</p>
            </div>
            <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-2">
                <div class="text-2xl">🛡️</div>
                <div class="font-bold text-emerald-700 text-sm font-heading">2. Einstein Trust Layer</div>
                <p class="text-[11px] text-slate-500">PII Masking, Toxicity Filters, Zero-Retention LLM Gateway</p>
            </div>
            <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-2">
                <div class="text-2xl">🧠</div>
                <div class="font-bold text-indigo-700 text-sm font-heading">3. Atlas Reasoning</div>
                <p class="text-[11px] text-slate-500">Autonomous Intent Recognition, Topic Routing &amp; Plan Formulation</p>
            </div>
            <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-2">
                <div class="text-2xl">⚡</div>
                <div class="font-bold text-amber-700 text-sm font-heading">4. Action Execution</div>
                <p class="text-[11px] text-slate-500">Salesforce Flow, Apex, ERP Integration &amp; Real-Time Updates</p>
            </div>
        </div>
    </section>

    <!-- 5. SECTION 4: COMPARISON MATRIX TABLE -->
    <section id="sec-4" class="space-y-6">
        <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-full bg-[#084582] text-white flex items-center justify-center font-black text-sm">4</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight font-heading">
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

    <!-- 6. SECTION 5: GOVERNANCE & AUSTRALIAN COMPLIANCE (LIGHT CARDS) -->
    <section id="sec-5" class="space-y-4">
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight border-b border-slate-200 pb-3 font-heading">
            5. Governance, ISO 27001 &amp; Australian Compliance Standards
        </h2>
        <p class="text-slate-700 leading-relaxed">
            Speed never compromises security. Every Agentforce solution architected by {site_brand} adheres to stringent Australian data sovereignty and regulatory guidelines:
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div class="p-5 rounded-2xl bg-blue-50/70 border border-blue-200 text-slate-800 space-y-2">
                <div class="text-xs font-black uppercase text-[#084582] tracking-wider">APRA CPS 234 &amp; Essential Eight</div>
                <p class="text-xs text-slate-600 leading-relaxed">
                    Deterministic role-level access controls, multi-factor authentication enforcement, and Australian-hosted data residency for banking, insurance, and NDIS providers.
                </p>
            </div>
            <div class="p-5 rounded-2xl bg-emerald-50/70 border border-emerald-200 text-slate-800 space-y-2">
                <div class="text-xs font-black uppercase text-emerald-800 tracking-wider">ISO 27001:2022 Certified Architecture</div>
                <p class="text-xs text-slate-600 leading-relaxed">
                    End-to-end TLS 1.3 encryption, immutable audit trails, and automated prompt toxicity filtering to prevent data leakage and LLM hallucination risk.
                </p>
            </div>
        </div>
    </section>

</div>
"""

# Clean Highlights Definition without fake timestamps
HIGHLIGHTS_DATA = [
    { "id": "sec-metrics", "badge": "01. METRICS", "title": "Key Performance Metrics", "text": "93% reduced time to outcomes, 96% lower management costs, and 58% faster time to value." },
    { "id": "sec-1", "badge": "02. CONTEXT", "title": "Traditional Consulting Trap", "text": "Why $250k+ legacy retainers fail in the rapidly evolving AI landscape." },
    { "id": "sec-2", "badge": "03. ROADMAP", "title": "3-Phase Sprint Model", "text": "Scoping in Week 1, Atlas Engine & Flow wiring in Weeks 2-3, and Canary Go-Live in Week 4." },
    { "id": "sec-3", "badge": "04. ARCHITECTURE", "title": "Technical Architecture", "text": "Zero-Copy Data Cloud lakehouse grounding with strict Einstein Trust Layer security guardrails." },
    { "id": "sec-4", "badge": "05. COMPARISON", "title": "Comparison Matrix", "text": "Big 4 $250k+ 9-month retainers vs. our agile squad deployed in under 4 weeks." }
]

def patch_procrm_blog_jsx():
    print("🛠️ Updating procrm-app Blog.jsx (clean highlights, no timestamps, no inner scrollbar)...")
    blog_jsx_path = os.path.join(PROCRM_DIR, "src", "pages", "Blog.jsx")
    with open(blog_jsx_path, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Update articleHighlights parsing to use item.badge (or clean fallback, NO fake timestamps)
    hl_logic_target = """  const articleHighlights = useMemo(() => {
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

    hl_logic_replacement = """  const articleHighlights = useMemo(() => {
    if (post.highlights && Array.isArray(post.highlights) && post.highlights.length > 0) {
      return post.highlights.map((hl, i) => ({
        badge: hl.badge || `0${i + 1}. KEY POINT`,
        date: post.date || "Aug 24, 2026",
        title: hl.title || `Key Point ${i + 1}`,
        summary: hl.text || hl.summary || "",
        sectionId: hl.id || `article-section-${i}`,
      }));
    }
    return (post.body || []).map((para, i) => ({
      badge: `0${i + 1}. SUMMARY`,
      date: post.date || "Aug 24, 2026",
      title: i === 0 ? "Executive Overview" : `Key Takeaway ${i + 1}`,
      summary: para.slice(0, 110) + "...",
      sectionId: `article-section-${i}`,
    }));"""

    if hl_logic_target in code:
        code = code.replace(hl_logic_target, hl_logic_replacement)

    # 2. Update Aside to be cleanly sticky WITHOUT inner max-h scrollbar
    code = re.sub(
        r'<aside className="lg:col-span-4 space-y-6 lg:sticky.*?>',
        '<aside className="lg:col-span-4 space-y-6 lg:sticky lg:top-[90px] self-start">',
        code
    )

    # 3. Update Highlights Timeline widget JSX (use item.badge instead of red item.time)
    old_hl_widget_jsx = """                      {/* Timestamp in Red */}
                      <div className="text-[11px] font-black text-[#990000] leading-none mb-1">
                        {item.time}
                      </div>"""

    new_hl_widget_jsx = """                      {/* Category Badge Pill (No fake timestamps) */}
                      <div className="text-[10px] font-black text-[#990000] uppercase tracking-wider mb-1">
                        {item.badge || item.time}
                      </div>"""

    if old_hl_widget_jsx in code:
        code = code.replace(old_hl_widget_jsx, new_hl_widget_jsx)

    with open(blog_jsx_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Patched Blog.jsx cleanly!")

def update_procrm_site_js():
    print("📝 Updating procrm-app/src/data/site.js with Light Theme HTML & Clean Highlights...")
    site_js_path = os.path.join(PROCRM_DIR, "src", "data", "site.js")
    with open(site_js_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'  {\s*slug: "agentforce-rapid-integration-fraction-of-cost-guide",.*?},\n'
    content = re.sub(pattern, "", content, flags=re.DOTALL)

    rich_html = generate_light_theme_article_html("PRO CRM Australia", "1300 050 099", "info@procrm.com.au")

    post_item = f"""  {{
    slug: "{SLUG}",
    title: "{TITLE}",
    date: "{TODAY_DATE}",
    author: "Robin Bakshi (Principal Architect)",
    category: "Enterprise AI & Cloud",
    subCategory: "Agentforce Integration",
    region: "National",
    readTime: "6 min read",
    isNew: true,
    badge: "⚡ 4-Week Rapid Sprint",
    tags: ["Agentforce", "Salesforce Consulting", "Enterprise AI", "Cost Optimization", "Australia"],
    image: "{HERO_IMAGE}",
    excerpt: "{EXCERPT}",
    highlights: [
      {{ id: "sec-metrics", badge: "01. METRICS", title: "Key Performance Metrics", text: "93% reduced time to outcomes, 96% lower management costs, and 58% faster time to value." }},
      {{ id: "sec-1", badge: "02. CONTEXT", title: "Traditional Consulting Trap", text: "Why $250k+ legacy retainers fail in the rapidly evolving AI landscape." }},
      {{ id: "sec-2", badge: "03. ROADMAP", title: "3-Phase Sprint Model", text: "Scoping in Week 1, Atlas Engine & Flow wiring in Weeks 2-3, and Canary Go-Live in Week 4." }},
      {{ id: "sec-3", badge: "04. ARCHITECTURE", title: "Technical Architecture", text: "Zero-Copy Data Cloud lakehouse grounding with strict Einstein Trust Layer security guardrails." }},
      {{ id: "sec-4", badge: "05. COMPARISON", title: "Comparison Matrix", text: "Big 4 $250k+ 9-month retainers vs. our agile squad deployed in under 4 weeks." }}
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
    content = content.replace("export const POSTS = [", f"export const POSTS = [\n{post_item}", 1)
    with open(site_js_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Updated procrm-app site.js!")

def update_ezconsultants_repo():
    print("📝 Updating ezconsultants.com.au...")
    posts_json_path = os.path.join(EZ_DIR, "posts.json")
    pub_posts_json_path = os.path.join(EZ_DIR, "public", "posts.json")
    blog_posts_js_path = os.path.join(EZ_DIR, "src", "data", "blogPosts.js")

    with open(posts_json_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    rich_html = generate_light_theme_article_html("EZ Consultants Australia", "1300 050 099", "info@ezconsultants.com.au")

    new_post_ez = {
        "id": SLUG,
        "slug": SLUG,
        "title": TITLE,
        "category": "Enterprise AI & Cloud",
        "date": "24-Aug-2026",
        "formattedDate": "24 August 2026",
        "iso_date": "2026-08-24T08:00:00Z",
        "readTime": "6 min read",
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
        "views": 2580,
        "likes": 224,
        "tags": ["Agentforce", "Salesforce AI", "Atlas Engine", "Cost Reduction", "Enterprise Architecture", "buy.nsw"],
        "highlights": HIGHLIGHTS_DATA,
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
  return { views: 2580, likes: 224, userLiked: false };
}

export function incrementArticleView(slug) {
  try {
    const stats = getArticleStats(slug);
    stats.views += 1;
    localStorage.setItem("ez_article_stats_" + slug, JSON.stringify(stats));
    return stats;
  } catch (e) {
    return { views: 2581, likes: 224, userLiked: false };
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
    return { views: 2580, likes: 225, isLiked: true, delta: 1 };
  }
}
"""
    with open(blog_posts_js_path, "w", encoding="utf-8") as f:
        f.write(blog_posts_js_content)
    print("✅ Updated ezconsultants blogPosts.js & posts.json!")

def update_standalone_html():
    print("📝 Updating standalone HTML in Blogs-Content...")
    pages_dir = os.path.join(BLOGS_DIR, "pages", "blog")
    pub_pages_dir = os.path.join(BLOGS_DIR, "public", "pages", "blog")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(pub_pages_dir, exist_ok=True)

    rich_content = generate_light_theme_article_html("PRO CRM Australia", "1300 050 099", "info@procrm.com.au")

    page_html = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE} | PRO CRM Australia &amp; EZ Consultants</title>
    <meta name="description" content="{EXCERPT}">
    <link rel="canonical" href="https://procrm.com.au/blog/{SLUG}">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif; background-color: #f8fafc; color: #1e293b; }}
        h1, h2, h3, h4, .font-heading {{ font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif; }}
        .hl-spine {{ position: relative; padding-left: 20px; border-left: 2px solid #e2e8f0; }}
        .hl-dot {{ position: absolute; left: -25px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: #990000; box-shadow: 0 0 0 2px #fff, 0 0 0 4px #fee2e2; }}
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between">
    <header class="bg-[#07182c] border-b border-slate-800 text-white sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center gap-2">
                <span class="text-xl font-black tracking-tight text-white font-heading">PRO<span class="text-cyan-400">CRM</span></span>
                <span class="text-xs bg-blue-600/30 text-cyan-300 px-2 py-0.5 rounded-full border border-blue-500/30 font-bold">Enterprise AI</span>
            </a>
            <div class="flex items-center gap-4 text-xs font-semibold">
                <a href="tel:1300050099" class="hidden sm:inline-flex items-center gap-1.5 text-slate-300 hover:text-white">
                    <span>📞 1300 050 099</span>
                </a>
                <a href="mailto:info@procrm.com.au" class="bg-[#0052FF] hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-bold transition">
                    Book Discovery Call
                </a>
            </div>
        </div>
    </header>

    <section class="bg-gradient-to-b from-[#07182c] to-[#0d233a] text-white py-12 lg:py-16 px-4 sm:px-6">
        <div class="max-w-7xl mx-auto space-y-6">
            <div class="flex items-center gap-3 text-xs font-semibold uppercase tracking-wider text-cyan-400">
                <span class="bg-cyan-500/10 border border-cyan-400/30 px-3 py-1 rounded-full">⚡ 4-Week Rapid Sprint</span>
                <span>•</span>
                <span class="text-slate-300">24 August 2026</span>
                <span>•</span>
                <span class="text-slate-300">6 min read</span>
            </div>
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white leading-tight font-heading max-w-5xl">
                {TITLE}
            </h1>
            <p class="text-slate-300 text-base sm:text-lg leading-relaxed max-w-4xl font-normal">
                {EXCERPT}
            </p>
            <div class="flex items-center gap-3 text-xs text-slate-300 pt-2">
                <span>By <strong class="text-white">Robin Bakshi</strong> (Principal Salesforce Architect &amp; Founder)</span>
                <span>•</span>
                <span>ISO 27001:2022 Certified &amp; buy.nsw Approved</span>
            </div>
        </div>
    </section>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 py-12 grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
        <article class="lg:col-span-8 bg-white p-6 sm:p-10 rounded-3xl border border-slate-200 shadow-sm">
            {rich_content}
        </article>

        <aside class="lg:col-span-4 space-y-6 lg:sticky lg:top-[90px] self-start">
            <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
                <div class="bg-[#990000] text-white px-5 py-3.5 flex items-center justify-between">
                    <h3 class="text-sm font-bold tracking-tight text-white font-heading">Highlights</h3>
                    <span class="text-[10px] font-extrabold uppercase tracking-widest text-white/90">IN THIS ARTICLE</span>
                </div>
                <div class="p-5 space-y-4 text-xs font-sans">
                    <div class="text-slate-500 font-semibold">— 24 August 2026</div>
                    <div class="hl-spine space-y-4">
                        <div class="relative cursor-pointer" onclick="document.getElementById('sec-metrics').scrollIntoView({{behavior:'smooth'}})">
                            <span class="hl-dot"></span>
                            <div class="text-[10px] font-bold text-[#990000] uppercase">01. METRICS</div>
                            <div class="font-bold text-slate-900 leading-snug">Key Performance Metrics</div>
                            <p class="text-slate-500 text-[11px] mt-0.5">93% faster outcomes, 96% lower costs, 58% faster ROI.</p>
                        </div>
                        <div class="relative cursor-pointer" onclick="document.getElementById('sec-1').scrollIntoView({{behavior:'smooth'}})">
                            <span class="hl-dot"></span>
                            <div class="text-[10px] font-bold text-[#990000] uppercase">02. CONTEXT</div>
                            <div class="font-bold text-slate-900 leading-snug">Traditional Consulting Trap</div>
                            <p class="text-slate-500 text-[11px] mt-0.5">Why $250k+ legacy retainers fail in modern AI.</p>
                        </div>
                        <div class="relative cursor-pointer" onclick="document.getElementById('sec-2').scrollIntoView({{behavior:'smooth'}})">
                            <span class="hl-dot"></span>
                            <div class="text-[10px] font-bold text-[#990000] uppercase">03. ROADMAP</div>
                            <div class="font-bold text-slate-900 leading-snug">3-Phase Sprint Model</div>
                            <p class="text-slate-500 text-[11px] mt-0.5">Scoping in Wk 1, Wiring in Wks 2–3, Go-Live in Wk 4.</p>
                        </div>
                        <div class="relative cursor-pointer" onclick="document.getElementById('sec-3').scrollIntoView({{behavior:'smooth'}})">
                            <span class="hl-dot"></span>
                            <div class="text-[10px] font-bold text-[#990000] uppercase">04. ARCHITECTURE</div>
                            <div class="font-bold text-slate-900 leading-snug">Technical Architecture</div>
                            <p class="text-slate-500 text-[11px] mt-0.5">Zero-Copy Data Cloud and Einstein Trust Layer.</p>
                        </div>
                        <div class="relative cursor-pointer" onclick="document.getElementById('sec-4').scrollIntoView({{behavior:'smooth'}})">
                            <span class="hl-dot"></span>
                            <div class="text-[10px] font-bold text-[#990000] uppercase">05. COMPARISON</div>
                            <div class="font-bold text-slate-900 leading-snug">Comparison Matrix</div>
                            <p class="text-slate-500 text-[11px] mt-0.5">Big 4 $250k+ 9-month retainers vs. our 4-week sprint.</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bg-[#0A2540] text-white p-6 rounded-2xl shadow-md space-y-3 font-sans">
                <div class="text-[10px] font-extrabold uppercase tracking-widest text-cyan-400">DIRECT ARCHITECT ACCESS</div>
                <h4 class="text-base font-bold leading-snug font-heading">Speak with Australian Salesforce Architects</h4>
                <p class="text-xs text-slate-300 leading-relaxed">
                    Melbourne &amp; Sydney SOC monitoring. 100% Australian data residency guarantee.
                </p>
                <a href="tel:1300050099" class="block text-center w-full py-2.5 rounded-full bg-white text-[#0A2540] hover:bg-slate-100 font-bold text-xs shadow transition">
                    📞 Call 1300 050 099
                </a>
            </div>
        </aside>
    </main>

    <footer class="bg-[#07182c] border-t border-slate-800 text-slate-400 py-8 px-4 text-center text-xs">
        <p>&copy; 2026 PRO CRM Australia &amp; EZ Consultants. All rights reserved. · <a href="/rss.xml" class="text-cyan-400 hover:underline">RSS Feed</a></p>
    </footer>
</body>
</html>"""

    with open(os.path.join(pages_dir, f"{SLUG}.html"), "w", encoding="utf-8") as f:
        f.write(page_html)
    with open(os.path.join(pub_pages_dir, f"{SLUG}.html"), "w", encoding="utf-8") as f:
        f.write(page_html)
    print("✅ Updated standalone HTML files!")

def main():
    patch_procrm_blog_jsx()
    update_procrm_site_js()
    update_ezconsultants_repo()
    update_standalone_html()
    print("🎉 All light-theme and highlights updates completed!")

if __name__ == "__main__":
    main()
