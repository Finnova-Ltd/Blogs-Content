#!/usr/bin/env python3
"""
Generate Standalone HTML Page for Agentforce Infographic Article
"""

import os
import html

BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"
PAGES_DIR = os.path.join(BLOGS_DIR, "pages", "blog")
PUB_PAGES_DIR = os.path.join(BLOGS_DIR, "public", "pages", "blog")
os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(PUB_PAGES_DIR, exist_ok=True)

SLUG = "agentforce-rapid-integration-fraction-of-cost-guide"
TITLE = "Agentforce at Lightning Speed: How We Deploy Enterprise Autonomous AI at a Fraction of Big Consulting Costs"
EXCERPT = "Deploy autonomous Agentforce AI in 4 weeks—delivering 93% faster project outcomes and 96% lower management costs compared to traditional consulting houses."

PAGE_HTML = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(TITLE)} | PRO CRM Australia &amp; EZ Consultants</title>
    <meta name="description" content="{html.escape(EXCERPT)}">
    <link rel="canonical" href="https://procrm.com.au/blog/{SLUG}">
    
    <!-- Google Fonts: Roboto & Outfit -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400&display=swap" rel="stylesheet">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #1e293b;
            background-color: #f8fafc;
        }}
        h1, h2, h3, h4, .font-heading {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        .fixed-sidebar {{
            position: sticky;
            top: 90px;
            max-height: calc(100vh - 110px);
            overflow-y: auto;
            scrollbar-width: thin;
        }}
        .fixed-sidebar::-webkit-scrollbar {{
            width: 4px;
        }}
        .fixed-sidebar::-webkit-scrollbar-thumb {{
            background: rgba(148, 163, 184, 0.4);
            border-radius: 4px;
        }}
        #readingProgress {{
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(to right, #0052FF, #00C9FF);
            z-index: 10000;
            width: 0%;
            transition: width 0.1s ease-out;
        }}
        .hl-spine {{
            position: relative;
            padding-left: 20px;
            border-left: 2px solid #e2e8f0;
        }}
        .hl-dot {{
            position: absolute;
            left: -25px;
            top: 4px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #990000;
            box-shadow: 0 0 0 2px #fff, 0 0 0 4px #fee2e2;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between">
    <!-- Reading Progress Bar -->
    <div id="readingProgress"></div>

    <!-- Header Navigation -->
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

    <!-- Hero Header -->
    <section class="bg-gradient-to-b from-[#07182c] to-[#0d233a] text-white py-12 lg:py-16 px-4 sm:px-6">
        <div class="max-w-7xl mx-auto space-y-6">
            <div class="flex items-center gap-3 text-xs font-semibold uppercase tracking-wider text-cyan-400">
                <span class="bg-cyan-500/10 border border-cyan-400/30 px-3 py-1 rounded-full">⚡ 4-Week Rapid Sprint</span>
                <span>•</span>
                <span class="text-slate-300">24 August 2026</span>
                <span>•</span>
                <span class="text-slate-300">4 min read</span>
            </div>

            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white leading-tight font-heading max-w-5xl">
                {html.escape(TITLE)}
            </h1>

            <p class="text-slate-300 text-base sm:text-lg leading-relaxed max-w-4xl font-normal">
                {html.escape(EXCERPT)}
            </p>

            <div class="flex items-center gap-3 text-xs text-slate-300 pt-2">
                <span>By <strong class="text-white">Robin Bakshi</strong> (Principal Salesforce Architect &amp; Founder)</span>
                <span>•</span>
                <span>ISO 27001:2022 Certified &amp; buy.nsw Approved</span>
            </div>
        </div>
    </section>

    <!-- Main Content (2-Column Grid) -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 py-12 grid grid-cols-1 lg:grid-cols-12 gap-10">
        <!-- Col 1: Article Content with Visual Infographics -->
        <article class="lg:col-span-8 bg-white p-6 sm:p-10 rounded-2xl border border-slate-200 shadow-sm space-y-10">
            
            <!-- 1. EXECUTIVE METRIC INFOGRAPHIC HERO CARDS -->
            <div id="sec-metrics" class="bg-gradient-to-br from-slate-900 via-[#084582] to-[#042444] rounded-3xl p-6 sm:p-8 text-white shadow-xl border border-blue-800/60 relative overflow-hidden">
                <div class="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-cyan-300 mb-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
                    Key Performance Benchmarks
                </div>
                <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight mb-3 font-heading">
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

            <!-- 2. THE 3-STEP INTEGRATION PROCESS INFOGRAPHIC -->
            <section id="sec-1" class="space-y-6">
                <div class="flex items-center gap-3">
                    <span class="w-8 h-8 rounded-full bg-[#084582] text-white flex items-center justify-center font-black text-sm">1</span>
                    <h2 class="text-2xl font-black text-slate-900 tracking-tight font-heading">
                        Here’s How It Works: The 3-Phase Sprint Model
                    </h2>
                </div>
                <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
                    We start with a detailed analysis of your business to pinpoint exactly where agentic AI can make the biggest difference right away. While we build your first agent, we create a scalable blueprint for a team of AI agents that work together seamlessly.
                </p>

                <!-- 3 Step Cards Grid -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
                    <div class="p-6 rounded-2xl bg-white border-2 border-blue-100 hover:border-blue-300 hover:shadow-lg transition flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-4">
                                <span class="px-3 py-1 bg-blue-100 text-[#084582] rounded-full text-[11px] font-black uppercase tracking-wider">Week 1</span>
                                <span class="text-2xl">🎯</span>
                            </div>
                            <h3 class="text-base font-bold text-slate-900 leading-snug mb-2 font-heading">
                                Create an ROI-driven roadmap with expert guidance.
                            </h3>
                            <p class="text-xs text-slate-600 leading-relaxed">
                                Determine how to accomplish your business goals with an agentic experience. We audit case logs and CRM touchpoints to prioritize agents that drive measurable containment fast.
                            </p>
                        </div>
                        <div class="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1 text-[11px] font-bold text-[#084582]">
                            <span>✓ High-Impact Use Cases Locked</span>
                        </div>
                    </div>

                    <div class="p-6 rounded-2xl bg-white border-2 border-cyan-100 hover:border-cyan-300 hover:shadow-lg transition flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-4">
                                <span class="px-3 py-1 bg-cyan-100 text-cyan-800 rounded-full text-[11px] font-black uppercase tracking-wider">Weeks 2–3</span>
                                <span class="text-2xl">⚡</span>
                            </div>
                            <h3 class="text-base font-bold text-slate-900 leading-snug mb-2 font-heading">
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

                    <div class="p-6 rounded-2xl bg-white border-2 border-emerald-100 hover:border-emerald-300 hover:shadow-lg transition flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-4">
                                <span class="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-[11px] font-black uppercase tracking-wider">Week 4+</span>
                                <span class="text-2xl">📈</span>
                            </div>
                            <h3 class="text-base font-bold text-slate-900 leading-snug mb-2 font-heading">
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
                        <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight font-heading">
                            Technical Architecture: Enterprise-Grade &amp; Zero-Copy
                        </h2>
                        <p class="text-xs text-slate-400">Native Salesforce Core with Einstein Trust Layer Security Boundaries</p>
                    </div>
                </div>

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
                    <h2 class="text-2xl font-black text-slate-900 tracking-tight font-heading">
                        Comparison Matrix: Big 4 Consulting vs. Our Agile Squad
                    </h2>
                </div>

                <div class="overflow-x-auto rounded-2xl border border-slate-200 shadow-xs">
                    <table class="w-full text-left text-xs sm:text-sm">
                        <thead class="bg-slate-100 border-b border-slate-200 text-slate-900 uppercase font-black tracking-wider text-[11px]">
                            <tr>
                                <th class="p-4">Key Criteria</th>
                                <th class="p-4 text-rose-700 bg-rose-50/50">Traditional Big 4 Consulting</th>
                                <th class="p-4 text-[#084582] bg-blue-50/60 font-black">Our Agile Squad</th>
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
                    <h3 class="text-xl sm:text-2xl font-black text-white tracking-tight font-heading">
                        Ready to Deploy Agentforce in Under 4 Weeks?
                    </h3>
                    <p class="text-xs sm:text-sm text-slate-300 max-w-xl">
                        Get a direct 30-minute Architecture Blueprint Session with our Principal Salesforce &amp; AI Architects. No sales pitch, just practical engineering guidance.
                    </p>
                </div>
                <a href="mailto:info@procrm.com.au?subject=Agentforce%20Rapid%20Integration%20Review" class="px-6 py-3.5 rounded-2xl bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-black text-sm transition shadow-lg whitespace-nowrap">
                    Book Architecture Review →
                </a>
            </div>

        </article>

        <!-- Col 2: Sticky Highlights & Contact Sidebar -->
        <aside class="lg:col-span-4 space-y-6">
            <div class="fixed-sidebar space-y-6">
                
                <!-- Highlights Card -->
                <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
                    <div class="bg-[#990000] text-white px-5 py-3.5 flex items-center justify-between">
                        <h3 class="text-sm font-bold tracking-tight text-white font-heading">Highlights</h3>
                        <span class="text-[10px] font-extrabold uppercase tracking-widest text-white/90">IN THIS ARTICLE</span>
                    </div>
                    <div class="p-5 space-y-4 text-xs font-sans">
                        <div class="text-slate-500 font-semibold">— 24 August 2026</div>
                        <div class="hl-spine space-y-4">
                            <div class="relative cursor-pointer" onclick="document.getElementById('sec-metrics').scrollIntoView({{behavior:'smooth'}})">
                                <span class="hl-dot"></span>
                                <div class="text-[10px] font-bold text-[#990000] uppercase">10:00 AM</div>
                                <div class="font-bold text-slate-900 leading-snug">Key Performance Metrics</div>
                                <p class="text-slate-500 text-[11px] mt-0.5">93% faster outcomes, 96% lower costs, 58% faster ROI.</p>
                            </div>
                            <div class="relative cursor-pointer" onclick="document.getElementById('sec-1').scrollIntoView({{behavior:'smooth'}})">
                                <span class="hl-dot"></span>
                                <div class="text-[10px] font-bold text-[#990000] uppercase">09:30 AM</div>
                                <div class="font-bold text-slate-900 leading-snug">3-Phase Sprint Model</div>
                                <p class="text-slate-500 text-[11px] mt-0.5">Scoping in Wk 1, Wiring in Wks 2–3, Go-Live in Wk 4.</p>
                            </div>
                            <div class="relative cursor-pointer" onclick="document.getElementById('sec-2').scrollIntoView({{behavior:'smooth'}})">
                                <span class="hl-dot"></span>
                                <div class="text-[10px] font-bold text-[#990000] uppercase">09:00 AM</div>
                                <div class="font-bold text-slate-900 leading-snug">Technical Architecture</div>
                                <p class="text-slate-500 text-[11px] mt-0.5">Zero-Copy Data Cloud and Einstein Trust Layer.</p>
                            </div>
                            <div class="relative cursor-pointer" onclick="document.getElementById('sec-3').scrollIntoView({{behavior:'smooth'}})">
                                <span class="hl-dot"></span>
                                <div class="text-[10px] font-bold text-[#990000] uppercase">08:30 AM</div>
                                <div class="font-bold text-slate-900 leading-snug">Comparison Matrix</div>
                                <p class="text-slate-500 text-[11px] mt-0.5">Big 4 $250k+ 9-month retainers vs. our 4-week sprint.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Contact Box -->
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

            </div>
        </aside>
    </main>

    <!-- Footer -->
    <footer class="bg-[#07182c] border-t border-slate-800 text-slate-400 py-8 px-4 text-center text-xs">
        <p>&copy; 2026 PRO CRM Australia &amp; EZ Consultants. All rights reserved. · <a href="/rss.xml" class="text-cyan-400 hover:underline">RSS Feed</a></p>
    </footer>

    <script>
        window.addEventListener('scroll', () => {{
            const total = document.documentElement.scrollHeight - window.innerHeight;
            if (total > 0) {{
                const pct = (window.scrollY / total) * 100;
                document.getElementById('readingProgress').style.width = pct + '%';
            }}
        }});
    </script>
</body>
</html>
"""

page_path = os.path.join(PAGES_DIR, f"{SLUG}.html")
pub_page_path = os.path.join(PUB_PAGES_DIR, f"{SLUG}.html")

with open(page_path, "w", encoding="utf-8") as f:
    f.write(PAGE_HTML)
with open(pub_page_path, "w", encoding="utf-8") as f:
    f.write(PAGE_HTML)

print(f"✅ Created rich infographic standalone HTML page: {page_path}")
