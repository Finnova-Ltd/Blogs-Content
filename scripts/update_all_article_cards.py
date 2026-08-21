#!/usr/bin/env python3
import os
import glob
import re

ROOT_DIR = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
article_dirs = [
    os.path.join(ROOT_DIR, "pages", "blog"),
    os.path.join(ROOT_DIR, "public", "pages", "blog")
]

broker_card_html = """        <!-- 1. Broker Profile Card with Real Portrait & Cover Header Background -->
        <div class="author-profile-box" id="broker-contact-card" style="background:#ffffff; border:1.5px solid #e2e8f0; border-radius:14px; overflow:hidden; text-align:center; box-shadow:0 4px 16px rgba(0,0,0,0.06); margin-bottom:22px; transition:all 0.4s ease;">
          <div class="author-profile-banner" style="height:92px; overflow:hidden; position:relative;">
            <img src="/images/ez-broker-cover-header.jpg" alt="EZ Mortgage Broker Header Cover" style="width:100%; height:100%; object-fit:cover; display:block;">
          </div>
          <div class="author-profile-avatar-wrap" style="width:88px; height:88px; border-radius:50%; background:#ffffff; box-shadow:0 4px 16px rgba(0,0,0,0.18); margin:-44px auto 10px; display:grid; place-items:center; padding:3px; overflow:hidden; position:relative; z-index:2; border:3px solid #ffffff;">
            <img src="/images/r-bakshi.jpeg" alt="R Bakshi - Principal Mortgage Broker" class="author-profile-avatar-img" style="width:100%; height:100%; object-fit:cover; border-radius:50%;" onerror="this.src='/images/ez-mortgage-broker.webp'">
          </div>
          <div class="author-profile-content" style="padding:0 18px 20px;">
            <h3 class="author-profile-name" style="font-size:1.22rem; color:#0A2540; margin:0 0 2px; font-weight:800;">R Bakshi</h3>
            <p class="author-profile-title" style="font-size:0.84rem; color:#64748b; margin:0 0 4px; font-weight:600;">Principal Mortgage Broker</p>
            <p style="font-size:0.75rem; color:#1D4ED8; font-weight:700; margin:0 0 6px;">MFAA Accredited | CRN: 538522</p>
            <div class="author-rating-stars" style="color:#f59e0b; font-size:0.92rem; margin-bottom:16px; font-weight:700;">★★★★★ <span style="color:#64748b; font-weight:600;">(14)</span></div>
            <div class="author-actions-col" style="display:flex; flex-direction:column; gap:8px;">
              <a href="/#contact" class="author-action-btn" style="display:flex; align-items:center; justify-content:center; gap:8px; width:100%; padding:11px 14px; border-radius:8px; font-weight:700; font-size:0.88rem; text-decoration:none; background:#0A2540; color:#ffffff !important;">💬 Book Appointment</a>
              <a href="/#contact" class="author-action-btn" style="display:flex; align-items:center; justify-content:center; gap:8px; width:100%; padding:11px 14px; border-radius:8px; font-weight:700; font-size:0.88rem; text-decoration:none; background:#1D4ED8; color:#ffffff !important;">📱 Send Message</a>
              <a href="tel:1300050099" class="author-action-btn" style="display:flex; align-items:center; justify-content:center; gap:8px; width:100%; padding:11px 14px; border-radius:8px; font-weight:700; font-size:0.88rem; text-decoration:none; background:#00876C; color:#ffffff !important;">📇 Contact Card</a>
            </div>
          </div>
        </div>"""

updated_count = 0
for d in article_dirs:
    if not os.path.exists(d):
        continue
    for fpath in glob.glob(os.path.join(d, "*.html")):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        orig = content
        if "author-profile-box" in content:
            content = re.sub(r'<div class="author-profile-box".*?</div>\s*</div>\s*</div>', broker_card_html, content, count=1, flags=re.DOTALL)
        elif "broker-profile-card" in content:
            content = re.sub(r'<div class="broker-profile-card".*?</div>\s*</div>\s*</div>', broker_card_html, content, count=1, flags=re.DOTALL)
            
        content = content.replace("ez-mortgage-broker.webp\" alt=\"R Bakshi", "r-bakshi.jpeg\" alt=\"R Bakshi")
        content = content.replace("<img class=\"brand-logo\" src=\"/images/r-bakshi.jpeg\"", "<img class=\"brand-logo\" src=\"/images/ez-mortgage-broker.webp\"")
        
        if content != orig:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            updated_count += 1

print(f"✅ Successfully updated broker card with cover header background and large portrait across {updated_count} article pages!")
