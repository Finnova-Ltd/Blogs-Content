#!/usr/bin/env python3
"""
Ensure Sitemap link is prominently and visibly placed in the footer of all 5 sites:
1. ezsignature.com (eSignaturesonline)
2. procrm.com.au (procrm-app)
3. ezconsultants.com.au
4. ezmortgagebroker.com.au
5. finnova.org.au
"""

import os
import glob

print("🔧 Updating all footers across all 5 sites to visibly display Sitemap link...")

# 1. EZ Signature: frontend/src/components/Footer.jsx
ezsig_footer = "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend/src/components/Footer.jsx"
if os.path.exists(ezsig_footer):
    with open(ezsig_footer, "r", encoding="utf-8") as f:
        c = f.read()
    if 'to="/sitemap"' not in c:
        c = c.replace('<li><Link to="/about">About Us & Governance</Link></li>', '<li><Link to="/about">About Us & Governance</Link></li>\n                        <li><Link to="/sitemap" style={{color: "#60a5fa", fontWeight: "bold"}}>Sitemap (HTML Index)</Link></li>')
        c = c.replace('<p>© 2026 EZ Signature. All rights reserved.', '<p>© 2026 EZ Signature. All rights reserved. <Link to="/sitemap" style={{color: "#93c5fd", textDecoration: "underline", marginLeft: "6px", marginRight: "6px", fontWeight: "600"}}>Sitemap</Link> • ')
        with open(ezsig_footer, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ ezsignature Footer.jsx updated with prominent Sitemap link")

# Also check generate-static-pages.js in eSignaturesonline
ezsig_gen = "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend/scripts/generate-static-pages.js"
if os.path.exists(ezsig_gen):
    with open(ezsig_gen, "r", encoding="utf-8") as f:
        c = f.read()
    if '/sitemap' not in c:
        c = c.replace("'/pricing',", "'/pricing',\n  '/sitemap',")
        with open(ezsig_gen, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ ezsignature generate-static-pages.js updated with /sitemap route")

# 2. EZ Consultants: src/components/Footer.jsx
ezcon_footer = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/src/components/Footer.jsx"
if os.path.exists(ezcon_footer):
    with open(ezcon_footer, "r", encoding="utf-8") as f:
        c = f.read()
    if 'to="/sitemap"' not in c:
        c = c.replace('<Link to="/about-us"', '<Link to="/sitemap" className="text-cyan-600 dark:text-cyan-400 font-semibold hover:underline mr-4">Sitemap</Link>\n            <Link to="/about-us"')
        c = c.replace('<li><Link to="/about-us" className="hover:text-slate-900 dark:hover:text-white transition-colors">About Us</Link></li>', '<li><Link to="/sitemap" className="text-cyan-600 dark:text-cyan-400 font-bold hover:underline">Sitemap</Link></li>\n              <li><Link to="/about-us" className="hover:text-slate-900 dark:hover:text-white transition-colors">About Us</Link></li>')
        with open(ezcon_footer, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ ezconsultants Footer.jsx updated")

# 3. PRO CRM: src/components/Chrome.jsx
procrm_chrome = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/components/Chrome.jsx"
if os.path.exists(procrm_chrome):
    with open(procrm_chrome, "r", encoding="utf-8") as f:
        c = f.read()
    if 'to="/sitemap"' not in c:
        c = c.replace('<Link to="/privacy"', '<Link to="/sitemap" className="text-sky-400 hover:text-white font-semibold mr-4">Sitemap</Link>\n              <Link to="/privacy"')
        with open(procrm_chrome, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ procrm Chrome.jsx updated")

# 4. EZ Mortgage Broker: all html files
ezm_dir = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker"
for f in os.listdir(ezm_dir):
    if f.endswith('.html'):
        p = os.path.join(ezm_dir, f)
        with open(p, "r", encoding="utf-8") as file:
            c = file.read()
        if 'href="/sitemap.html"' not in c and 'href="sitemap.html"' not in c:
            if 'href="/privacy-policy.html"' in c:
                c = c.replace('href="/privacy-policy.html"', 'href="/sitemap.html" style="color:#FFDC4A !important; font-weight:700; margin-right:16px;">Sitemap</a><a href="/privacy-policy.html"')
            elif 'href="privacy-policy.html"' in c:
                c = c.replace('href="privacy-policy.html"', 'href="sitemap.html" style="color:#FFDC4A !important; font-weight:700; margin-right:16px;">Sitemap</a><a href="privacy-policy.html"')
            with open(p, "w", encoding="utf-8") as file:
                file.write(c)
            print(f"✅ ezmortgagebroker {f} updated with sitemap.html link")

# 5. Finnova: all html files
fin_dir = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova"
for f in os.listdir(fin_dir):
    if f.endswith('.html'):
        p = os.path.join(fin_dir, f)
        with open(p, "r", encoding="utf-8") as file:
            c = file.read()
        if 'href="/sitemap.html"' not in c and 'href="sitemap.html"' not in c:
            if 'cookie-policy.html' in c:
                c = c.replace('cookie-policy.html', 'sitemap.html" style="color:#10b981; font-weight:700; margin-right:15px;">Sitemap</a><a href="cookie-policy.html')
            with open(p, "w", encoding="utf-8") as file:
                file.write(c)
            print(f"✅ Finnova {f} updated with sitemap.html link")

print("🚀 Finished updating all footers!")
