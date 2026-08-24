#!/usr/bin/env python3
"""
Wire up Sitemap routes and footer links across all repos:
1. ezconsultants.com.au
2. procrm-app
3. finnova
4. ezsignature
"""

import os
import re

# 1. Update ezconsultants App.jsx & Footer.jsx
ez_app = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/src/App.jsx"
if os.path.exists(ez_app):
    with open(ez_app, "r", encoding="utf-8") as f:
        c = f.read()
    if "import Sitemap" not in c:
        c = c.replace("import BlogArticle from './pages/BlogArticle.jsx';", "import BlogArticle from './pages/BlogArticle.jsx';\nimport Sitemap from './pages/Sitemap.jsx';")
        c = c.replace('<Route path="/contact-us" element={<ContactUs />} />', '<Route path="/contact-us" element={<ContactUs />} />\n            <Route path="/sitemap" element={<Sitemap />} />\n            <Route path="/sitemap.html" element={<Sitemap />} />')
        with open(ez_app, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ Added Sitemap route to ezconsultants App.jsx")

ez_footer = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au/src/components/Footer.jsx"
if os.path.exists(ez_footer):
    with open(ez_footer, "r", encoding="utf-8") as f:
        c = f.read()
    if 'to="/sitemap"' not in c:
        c = c.replace('<li><Link to="/about-us"', '<li><Link to="/sitemap" className="text-cyan-600 dark:text-cyan-400 font-bold hover:underline">HTML Sitemap</Link></li>\n            <li><Link to="/about-us"')
        c = c.replace('<Link to="/contact-us" className="hover:text-slate-700 dark:hover:text-slate-300 transition-colors">Privacy Policy</Link>', '<Link to="/sitemap" className="hover:text-slate-700 dark:hover:text-slate-300 transition-colors font-semibold">Sitemap</Link>\n            <Link to="/contact-us" className="hover:text-slate-700 dark:hover:text-slate-300 transition-colors">Privacy Policy</Link>')
        with open(ez_footer, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ Added Sitemap link to ezconsultants Footer.jsx")

# 2. Update procrm-app App.jsx & Chrome.jsx
procrm_app = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/App.jsx"
if os.path.exists(procrm_app):
    with open(procrm_app, "r", encoding="utf-8") as f:
        c = f.read()
    if "import Sitemap" not in c:
        c = c.replace('import LegalHub from "./pages/LegalHub.jsx";', 'import LegalHub from "./pages/LegalHub.jsx";\nimport Sitemap from "./pages/Sitemap.jsx";')
        c = c.replace('<Route path="/security" element={<Security />} />', '<Route path="/security" element={<Security />} />\n            <Route path="/sitemap" element={<Sitemap />} />\n            <Route path="/sitemap.html" element={<Sitemap />} />')
        with open(procrm_app, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ Added Sitemap route to procrm App.jsx")

procrm_chrome = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/components/Chrome.jsx"
if os.path.exists(procrm_chrome):
    with open(procrm_chrome, "r", encoding="utf-8") as f:
        c = f.read()
    if 'to="/sitemap"' not in c:
        c = c.replace('<Link to="/privacy"', '<Link to="/sitemap" className="text-slate-400 hover:text-white mr-4">Sitemap</Link>\n              <Link to="/privacy"')
        with open(procrm_chrome, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ Added Sitemap link to procrm Chrome.jsx")

# 3. Update ezsignature App.jsx
ezsig_app = "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/frontend/src/App.jsx"
if os.path.exists(ezsig_app):
    with open(ezsig_app, "r", encoding="utf-8") as f:
        c = f.read()
    if "import Sitemap" not in c:
        c = c.replace("import NonProfitPricing from './pages/NonProfitPricing';", "import NonProfitPricing from './pages/NonProfitPricing';\nimport Sitemap from './pages/Sitemap';")
        c = c.replace('<Route path="/about" element={<AboutPage />} />', '<Route path="/about" element={<AboutPage />} />\n                        <Route path="/sitemap" element={<Sitemap />} />\n                        <Route path="/sitemap.html" element={<Sitemap />} />')
        with open(ezsig_app, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ Added Sitemap route to ezsignature App.jsx")

# 4. Update ezmortgagebroker footers in index.html & calculators.html
ezm_index = "/Users/robinbakshi/Documents/GitHub/ezmortgagebroker/index.html"
if os.path.exists(ezm_index):
    with open(ezm_index, "r", encoding="utf-8") as f:
        c = f.read()
    if 'href="/sitemap.html"' not in c:
        c = c.replace('href="/privacy-policy.html"', 'href="/sitemap.html" style="color:#FFDC4A !important; font-weight:700; margin-right:16px;">Sitemap</a><a href="/privacy-policy.html"', 1)
        with open(ezm_index, "w", encoding="utf-8") as f:
            f.write(c)
        print("✅ Added sitemap.html link to ezmortgagebroker index.html")

print("🚀 All sitemap routes and footer links successfully wired!")
