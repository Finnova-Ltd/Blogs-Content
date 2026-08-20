#!/usr/bin/env python3
import os
import re
import subprocess

PROCRM_APP_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
SITE_JS_PATH = os.path.join(PROCRM_APP_DIR, "src/data/site.js")

print("Updating article images in site.js...")
with open(SITE_JS_PATH, "r", encoding="utf-8") as f:
    site_js = f.read()

# 1. Fix Cyber Liability Insurance image (replace man photo with glowing cyber shield)
old_ins_img = 'image: "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80"'
new_ins_img = 'image: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?auto=format&fit=crop&w=800&q=80"'
if old_ins_img in site_js:
    site_js = site_js.replace(old_ins_img, new_ins_img)
    print("✅ Replaced Cyber Liability Insurance image with cyber shield")

# 2. Fix Phishing Guide image (replace duplicate with neon cyber lock & email security)
old_phish_pattern = r'(slug: "phishing-attacks-social-engineering-asd-acsc-defense-guide".*?image: ")[^"]+(")'
site_js = re.sub(
    old_phish_pattern,
    r'\1https://images.unsplash.com/photo-1563089145-599997674d42?auto=format&fit=crop&w=800&q=80\2',
    site_js,
    flags=re.DOTALL
)
print("✅ Updated Phishing Guide image to dedicated cyber security lock")

# 3. Fix AI-Enabled Cyber Attacks image to AI neural network
old_ai_pattern = r'(slug: "defending-against-ai-enabled-cyber-attacks-smb-guide".*?image: ")[^"]+(")'
site_js = re.sub(
    old_ai_pattern,
    r'\1https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80\2',
    site_js,
    flags=re.DOTALL
)
print("✅ Updated AI Cyber Attacks image to AI neural network")

# 4. Fix Incident Response image to Cyber Security Operations Center (SOC)
old_ir_pattern = r'(slug: "cyber-security-incident-response-guidelines-asd-ism".*?image: ")[^"]+(")'
site_js = re.sub(
    old_ir_pattern,
    r'\1https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80\2',
    site_js,
    flags=re.DOTALL
)
print("✅ Updated Incident Response image to SOC center")

with open(SITE_JS_PATH, "w", encoding="utf-8") as f:
    f.write(site_js)
print("✅ Saved site.js successfully!")

print("Building procrm-app...")
res = subprocess.run(["npm", "run", "build"], cwd=PROCRM_APP_DIR, capture_output=True, text=True)
print("Build stdout:", res.stdout)
if res.returncode != 0:
    print("Build stderr:", res.stderr)
    exit(1)
print("✅ Build succeeded!")
