#!/usr/bin/env python3
import os
import re
import time

PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
rss_path = os.path.join(PROCRM_DIR, "public", "rss.xml")
feed_path = os.path.join(PROCRM_DIR, "public", "feed.xml")

with open(rss_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add a timestamp to the top item guid to make it 100% unique for Make.com
ts = int(time.time())
content = re.sub(r'<guid isPermaLink="true">https://procrm.com.au/blog/agentforce-multi-agent-governance-playbook-2026.*?</guid>',
                 f'<guid isPermaLink="true">https://procrm.com.au/blog/agentforce-multi-agent-governance-playbook-2026?v={ts}</guid>',
                 content)

with open(rss_path, "w", encoding="utf-8") as f:
    f.write(content)
with open(feed_path, "w", encoding="utf-8") as f:
    f.write(content)

os.system(f'cd "{PROCRM_DIR}" && git commit -am "Force trigger RSS for Make.com test" && git push origin main')
print(f"✅ Updated RSS feed GUID with timestamp {ts} and pushed to GitHub!")
