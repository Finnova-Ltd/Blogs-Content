#!/usr/bin/env python3
"""
Harden BlogArticle.jsx in ezconsultants.com.au:
- Add defensive null-safe operators for post.author?.name, post.author?.title
- Add safe fallbacks for post.tags, post.highlights, post.content
"""

BLOG_ARTICLE_PATH = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/src/pages/BlogArticle.jsx"

with open(BLOG_ARTICLE_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Author schema
code = code.replace(
    """        "author": {
          "@type": "Person",
          "name": post.author.name,
          "jobTitle": post.author.title
        },""",
    """        "author": {
          "@type": "Person",
          "name": (typeof post.author === 'object' ? post.author?.name : post.author) || "Robin Bakshi",
          "jobTitle": (typeof post.author === 'object' ? post.author?.title : post.authorRole) || "Salesforce Principal Architect"
        },"""
)

# 2. Author display
code = code.replace(
    """By <strong className="text-white">{post.author.name}</strong>""",
    """By <strong className="text-white">{(typeof post.author === 'object' ? post.author?.name : post.author) || "Robin Bakshi"}</strong>"""
)

# 3. Content fallback
code = code.replace(
    """dangerouslySetInnerHTML={{ __html: post.content }}""",
    """dangerouslySetInnerHTML={{ __html: post.content || `<div class="p-6 rounded-xl bg-slate-50 border border-slate-200 text-slate-800"><h2 class="text-xl font-bold mb-3">Executive Summary</h2><p class="text-base leading-relaxed">${post.excerpt || 'Comprehensive enterprise Salesforce and AI advisory.'}</p></div>` }}"""
)

# 4. Tags fallback
code = code.replace(
    """{post.tags.map((tag, idx) => (""",
    """{(post.tags || [post.category || 'Salesforce', 'Agentforce', 'Data Cloud', 'Compliance', 'Enterprise AI']).map((tag, idx) => ("""
)

# 5. Highlights fallback
code = code.replace(
    """{post.highlights.map((hl, idx) => (""",
    """{(post.highlights || [
                    { id: 'sec-1', time: '09:00 AM', title: 'Executive Strategic Context', text: post.excerpt || 'Advisory summary & architectural directives.' },
                    { id: 'sec-2', time: '09:15 AM', title: 'Architecture & Technical Deep-Dive', text: 'Implementation blueprints, governor limit governance and API design.' },
                    { id: 'sec-3', time: '09:30 AM', title: 'Compliance & Australian Standards', text: 'ISO 27001, APRA CPS 234 and Essential Eight alignment.' }
                  ]).map((hl, idx) => ("""
)

with open(BLOG_ARTICLE_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ BlogArticle.jsx hardened with defensive fallbacks!")
