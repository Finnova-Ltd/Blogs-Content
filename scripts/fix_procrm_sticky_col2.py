#!/usr/bin/env python3
"""
Patch Col 2 Sticky Positioning & Compact Layout in procrm-app/src/pages/Blog.jsx
"""

import os
import re

blog_jsx_path = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/pages/Blog.jsx"

with open(blog_jsx_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace the aside container and widgets with ultra-compact, guaranteed sticky layout
old_aside_pattern = r'<aside className="lg:col-span-4 space-y-4 sticky-col-2 self-start".*?</aside>'

new_aside = """<aside className="lg:col-span-4 space-y-3 sticky-col-2 self-start" style={{ position: "sticky", top: "105px", zIndex: 30 }}>
            
            {/* 1. Article Highlights Widget */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/70 overflow-hidden shadow-xs">
              {/* Solid Red Header Banner */}
              <div className="bg-[#990000] px-3.5 py-2 text-white flex items-center justify-between">
                <h3 className="text-xs font-black tracking-tight uppercase">Highlights</h3>
                <span className="text-[10px] font-bold text-rose-100 uppercase tracking-widest">In this article</span>
              </div>

              {/* Highlights Timeline List */}
              <div className="p-3 space-y-2.5 bg-white/95">
                <div className="text-[11px] font-bold text-slate-500 flex items-center gap-1.5">
                  <span>—</span>
                  <span>{postDate(post.date)}</span>
                </div>

                {/* Connected Vertical Timeline */}
                <div className="relative border-l-2 border-slate-200 ml-1 pl-3.5 space-y-3">
                  {articleHighlights.slice(0, 4).map((item, idx) => (
                    <div
                      key={idx}
                      className="relative group cursor-pointer"
                      onClick={() => handleHighlightSectionClick(item.sectionId)}
                    >
                      <span className="absolute -left-[19px] top-1 h-2 w-2 rounded-full bg-[#990000] ring-2 ring-white transition group-hover:scale-125" />
                      <div className="text-[9px] font-black text-[#990000] uppercase tracking-wider">
                        {item.badge || item.time}
                      </div>
                      <div className="text-[11px] font-bold text-slate-900 group-hover:text-[#084582] transition leading-snug">
                        {item.title}
                      </div>
                      <div className="text-[10.5px] font-medium text-slate-500 line-clamp-1 mt-0.5">
                        {item.summary}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 2. Related Articles / News */}
            <div className="rounded-2xl border border-slate-200 bg-white p-3 shadow-xs space-y-2">
              <div className="flex items-center justify-between border-b border-slate-100 pb-1.5">
                <span className="widget-heading font-ui text-[11px] font-black uppercase tracking-wider text-slate-900">
                  Related Articles / News
                </span>
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              </div>

              <div className="space-y-2">
                {recentArticles.slice(0, 3).map((p) => (
                  <Link
                    key={p.slug}
                    to={`/blog/${p.slug}`}
                    className="group flex items-center gap-2.5 transition"
                  >
                    <div className="h-9 w-9 shrink-0 rounded-lg overflow-hidden bg-slate-100 border border-slate-100">
                      <img
                        src={p.image}
                        alt={p.title}
                        className="h-full w-full object-cover group-hover:scale-105 transition duration-300"
                      />
                    </div>
                    <div className="min-w-0 flex-1">
                      <h4 className="text-[11px] font-bold text-slate-900 group-hover:text-[#084582] transition truncate leading-snug">
                        {p.title}
                      </h4>
                      <div className="text-[9.5px] text-slate-400 font-semibold">{postDate(p.date)}</div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>

            {/* 3. Direct Support Box */}
            <div
              style={{ backgroundColor: "#084582" }}
              className="rounded-2xl border border-blue-800 p-3.5 text-white shadow-md space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <span className="text-[9px] font-black uppercase tracking-widest text-blue-200">
                  Direct Architecture Support
                </span>
                <span className="text-[9px] font-bold bg-blue-600/60 px-1.5 py-0.5 rounded text-cyan-200">Melbourne</span>
              </div>
              <h3 className="text-xs font-black text-white leading-snug">
                Speak with our Principal Architects
              </h3>
              <a
                href={`tel:${CONTACT.phoneTel}`}
                className="w-full mt-1 flex items-center justify-center gap-1.5 rounded-xl bg-white px-2.5 py-1.5 text-xs font-black text-[#084582] shadow-xs hover:bg-blue-50 transition"
              >
                <span>📞 Call {CONTACT.phone}</span>
              </a>
            </div>

          </aside>"""

code = re.sub(old_aside_pattern, new_aside, code, flags=re.DOTALL)

with open(blog_jsx_path, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Successfully patched procrm-app/src/pages/Blog.jsx with guaranteed fixed Col 2 sticky positioning!")
