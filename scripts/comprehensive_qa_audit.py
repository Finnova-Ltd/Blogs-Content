import os
import json
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.text_parts = []
        self.ignore_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside', 'form'}
        self.current_ignore = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.ignore_tags:
            self.current_ignore += 1

    def handle_endtag(self, tag):
        if tag.lower() in self.ignore_tags:
            self.current_ignore = max(0, self.current_ignore - 1)

    def handle_data(self, data):
        if self.current_ignore == 0:
            cleaned = data.strip()
            if cleaned:
                self.text_parts.append(cleaned)

    def get_text(self):
        return ' '.join(self.text_parts)

def extract_clean_text(html_content: str) -> str:
    parser = TextExtractor()
    parser.feed(html_content)
    return parser.get_text()

sites = [
    {
        'name': 'Finnova (finnova.org.au)',
        'dir': '/Volumes/Samsung SSD 2TB/03. Documents/Imprtant Repos/Finnova',
        'posts_json': '/Volumes/Samsung SSD 2TB/03. Documents/Imprtant Repos/Finnova/posts.json',
        'blog_dir': '/Volumes/Samsung SSD 2TB/03. Documents/Imprtant Repos/Finnova/pages/blog'
    },
    {
        'name': 'EZ Mortgage Broker (ezmortgagebroker.com.au)',
        'dir': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker',
        'posts_json': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker/posts.json',
        'blog_dir': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezmortgagebroker/pages/blog'
    },
    {
        'name': 'EZ Consultants (ezconsultants.com.au)',
        'dir': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezconsultants.com.au',
        'posts_json': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezconsultants.com.au/public/posts.json',
        'blog_dir': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezconsultants.com.au/pages/blog'
    },
    {
        'name': 'eSignatures Online (esignaturesonline.com.au)',
        'dir': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/eSignaturesonline',
        'posts_json': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/eSignaturesonline/posts.json',
        'blog_dir': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/eSignaturesonline/pages/blog'
    },
    {
        'name': 'Blogs-Content Hub',
        'dir': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/Blogs-Content',
        'posts_json': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/Blogs-Content/posts.json',
        'blog_dir': '/Volumes/Samsung SSD 2TB/03. Documents/GitHub/Blogs-Content/pages/blog'
    }
]

audit_results = {}

canned_phrases = [
    'the reserve bank of australia and major retail banks have updated residential mortgage assessment benchmarks',
    'variable mortgage rates across standard owner-occupier loans are adjusting in line with interbank cash rate trajectories',
    'every 0.25% change shifts average household borrowing limits by approximately 2.5% to 3.0%',
    'on a standard $600,000 mortgage, a 25 bps movement translates to roughly $95',
    'speak with our accredited finance specialists to conduct a comprehensive assessment'
]

toxic_patterns = [
    r'house-for-sale', r'house-for-rent', r'killed-in', r'stabbing', r'murder',
    r'sentenced-for', r'court-orders-wind-u', r'underpaid-staff', r'gst-fraud',
    r'fight-with-neighbour', r'alleged-affair', r'times-square', r'liquidation'
]

for site in sites:
    sname = site['name']
    audit_results[sname] = {
        'total_html_files': 0,
        'total_posts_json': 0,
        'blank_or_under_250_words': [],
        'canned_boilerplate_templates': [],
        'brand_mismatched': [],
        'toxic_or_irrelevant': [],
        'high_quality_verified': []
    }
    
    # Check posts.json
    if os.path.exists(site['posts_json']):
        try:
            with open(site['posts_json'], 'r', encoding='utf-8') as fp:
                posts_data = json.load(fp)
                audit_results[sname]['total_posts_json'] = len(posts_data) if isinstance(posts_data, list) else 0
        except Exception as e:
            pass
            
    bdir = site['blog_dir']
    if not os.path.exists(bdir):
        continue
        
    html_files = [f for f in os.listdir(bdir) if f.endswith('.html')]
    audit_results[sname]['total_html_files'] = len(html_files)
    
    for fname in sorted(html_files):
        fpath = os.path.join(bdir, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            html = fp.read()
            
        t_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = t_match.group(1).split('|')[0].strip() if t_match else fname
        
        main_content = extract_clean_text(html)
        words = main_content.split()
        word_count = len(words)
        
        canned_match_count = sum(1 for cp in canned_phrases if cp in html.lower())
        
        is_brand_mismatch = False
        if 'finnova' in sname.lower():
            if 'r bakshi' in html.lower() or 'mfaa accredited' in html.lower() or 'lending' in html.lower() or 'mortgage' in html.lower():
                is_brand_mismatch = True
        elif 'ezconsultants' in sname.lower():
            if 'r bakshi' in html.lower() and 'mortgage' in html.lower():
                is_brand_mismatch = True
                
        is_toxic = any(re.search(tp, fname) for tp in toxic_patterns)
        
        item_meta = {
            'file': fname,
            'title': title,
            'word_count': word_count,
            'canned_count': canned_match_count
        }
        
        if is_toxic:
            audit_results[sname]['toxic_or_irrelevant'].append(item_meta)
        elif is_brand_mismatch:
            audit_results[sname]['brand_mismatched'].append(item_meta)
        elif canned_match_count >= 2:
            audit_results[sname]['canned_boilerplate_templates'].append(item_meta)
        elif word_count < 250:
            audit_results[sname]['blank_or_under_250_words'].append(item_meta)
        else:
            audit_results[sname]['high_quality_verified'].append(item_meta)

# Print Detailed Summary
print("\n" + "="*80)
print("📊 COMPREHENSIVE QA AUDIT & CONTENT QUALITY REPORT ACROSS ALL WEBSITES")
print("="*80)

for sname, data in audit_results.items():
    print(f"\n🏢 WEBSITE / REPOSITORY: {sname}")
    print(f"   • Total HTML Files in pages/blog: {data['total_html_files']}")
    print(f"   • Total Posts in posts.json:      {data['total_posts_json']}")
    print(f"   • ❌ Blank / Thin Content (<250 words):   {len(data['blank_or_under_250_words'])}")
    print(f"   • ❌ Canned Boilerplate Templates:        {len(data['canned_boilerplate_templates'])}")
    print(f"   • ❌ Brand Mismatches (Wrong Brand Copy): {len(data['brand_mismatched'])}")
    print(f"   • ❌ Toxic / Real Estate / Crime:         {len(data['toxic_or_irrelevant'])}")
    print(f"   • ✅ High-Quality Verified Articles:      {len(data['high_quality_verified'])}")

# Save Full JSON Audit Log
with open('/Volumes/Samsung SSD 2TB/03. Documents/GitHub/Blogs-Content/audit_report_all_sites.json', 'w', encoding='utf-8') as fp:
    json.dump(audit_results, fp, indent=2)

print("\n💾 Full detailed audit log saved to: Blogs-Content/audit_report_all_sites.json")
