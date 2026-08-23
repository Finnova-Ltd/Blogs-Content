#!/usr/bin/env python3
"""
Fix articleHighlights in procrm-app/src/pages/Blog.jsx
"""

BLOG_JSX = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/pages/Blog.jsx"

with open(BLOG_JSX, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "  // Dynamic Highlights for THIS article based on paragraph content"
end_marker = "  const handleHighlightSectionClick = (sectionId) => {"

start_pos = content.find(start_marker)
end_pos = content.find(end_marker)

if start_pos != -1 and end_pos != -1:
    clean_highlights_block = """  // Dynamic Highlights for THIS article based on paragraph content
  const articleHighlights = useMemo(() => {
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
    }));
  }, [post]);

"""
    content = content[:start_pos] + clean_highlights_block + content[end_pos:]
    with open(BLOG_JSX, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Fixed articleHighlights in Blog.jsx cleanly!")
else:
    print(f"❌ Markers not found: start_pos={start_pos}, end_pos={end_pos}")
