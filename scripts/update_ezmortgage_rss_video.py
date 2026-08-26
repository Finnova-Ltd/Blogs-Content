#!/usr/bin/env python3
import os

EZM_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
gen_script = os.path.join(EZM_DIR, "scripts", "generate_rss_feed.py")

with open(gen_script, "r", encoding="utf-8") as f:
    code = f.read()

OLD_BLOCK = """        item_xml = f\"\"\"    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <description>{desc}</description>
      <category>{category}</category>
      <pubDate>{pub_date}</pubDate>
    </item>\"\"\""""

NEW_BLOCK = """        video_url = p.get('videoUrl', 'https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/ezmortgage_2026_rba_cash_rate___refi_ultimate_avatar.mp4')
        item_xml = f\"\"\"    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <description>{desc}</description>
      <category>{category}</category>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{video_url}" length="15000000" type="video/mp4" />
      <media:content url="{video_url}" medium="video" type="video/mp4" />
    </item>\"\"\""""

if OLD_BLOCK in code:
    code = code.replace(OLD_BLOCK, NEW_BLOCK)
    code = code.replace('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">')
    with open(gen_script, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Updated generate_rss_feed.py with video/mp4 enclosure in ezmortgagebroker")

os.system(f'cd "{EZM_DIR}" && python3 scripts/generate_rss_feed.py && git commit -am "Add video/mp4 enclosures to EZ Mortgage RSS feed" && git push origin main')
print("🚀 EZ Mortgage RSS feed regenerated and pushed with video/mp4!")
