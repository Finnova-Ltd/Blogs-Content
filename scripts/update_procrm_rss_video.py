#!/usr/bin/env python3
import os
import re

PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
rss_gen_path = os.path.join(PROCRM_DIR, "scripts", "generate_rss.js")

with open(rss_gen_path, "r", encoding="utf-8") as f:
    code = f.read()

OLD_ENCLOSURE = """      <enclosure url="${escapeXml(post.image)}" length="0" type="image/jpeg" />
      <media:content url="${escapeXml(post.image)}" medium="image">"""

NEW_ENCLOSURE = """      <enclosure url="${escapeXml(post.videoUrl || 'https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/procrm_pro_crm_autonomous_multi__ultimate_avatar.mp4')}" length="15000000" type="video/mp4" />
      <media:content url="${escapeXml(post.videoUrl || 'https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/procrm_pro_crm_autonomous_multi__ultimate_avatar.mp4')}" medium="video" type="video/mp4">"""

if OLD_ENCLOSURE in code:
    code = code.replace(OLD_ENCLOSURE, NEW_ENCLOSURE)
    with open(rss_gen_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Updated generate_rss.js with video/mp4 enclosure")

os.system(f'cd "{PROCRM_DIR}" && node scripts/generate_rss.js && git commit -am "Update RSS enclosure to video/mp4 for YouTube Shorts automation" && git push origin main')
print("🚀 PRO CRM RSS feed regenerated and pushed with video/mp4!")
