#!/usr/bin/env python3
import os
import re
import json
import subprocess

PROCRM_APP_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
SITE_JS_PATH = os.path.join(PROCRM_APP_DIR, "src/data/site.js")
BLOG_JSX_PATH = os.path.join(PROCRM_APP_DIR, "src/pages/Blog.jsx")

phishing_post = {
    "slug": "phishing-attacks-social-engineering-asd-acsc-defense-guide",
    "title": "Phishing Attacks & Social Engineering Defense: ASD ACSC Triage & Enterprise Mitigation Guide",
    "date": "2026-08-20",
    "author": "R BAKSHI",
    "category": "Security Advisories",
    "subCategory": "Cyber Security",
    "region": "National",
    "readTime": "6 min read",
    "isNew": True,
    "badge": "🔥 Trending",
    "tags": ["Cyber Security", "Compliance", "ISO 27001", "Zero Trust", "Essential Eight", "National"],
    "image": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80",
    "excerpt": "Learn how Australian organisations recognize, triage, and neutralize advanced phishing attacks, spear-phishing campaigns, QR code lures, and credential harvesting threats using Australian Signals Directorate (ASD) guidelines.",
    "bullets": [
        "Unclicked Phishing Containment: Forward malicious headers to mail filters, submit SMS lures to ACMA, and log with Scamwatch.",
        "Malware Execution Response: Isolate endpoints from local networks, execute EDR scans, preserve forensic RAM, and report via ReportCyber.",
        "Financial Fraud Recall: Immediately trigger banking transaction holds, rotate banking credentials, and engage IDCARE counselors.",
        "PII Exposure Containment: Rotate enterprise tokens, place fraud alerts with credit reporting agencies (Equifax, Experian), and re-verify SSO sessions.",
    ],
    "body": [
        "According to the Australian Signals Directorate’s Australian Cyber Security Centre (ASD’s ACSC), phishing is a pervasive cyber threat where adversaries disguise communications as legitimate banks, government portals, or software providers to manipulate personnel into divulging sensitive credentials, session tokens, or financial payments.",
        "ASD ACSC Incident Triage & Operational Response:\n• Unclicked Phishing Containment: Forward malicious headers to mail filters, submit SMS lures to ACMA, and log with Scamwatch.\n• Malware Execution Response: Isolate endpoints from local networks, execute EDR scans, preserve forensic RAM, and report via ReportCyber.\n• Financial Fraud Recall: Immediately trigger banking transaction holds, rotate banking credentials, and engage IDCARE counselors.\n• PII Exposure Containment: Rotate enterprise tokens, place fraud alerts with credit reporting agencies (Equifax, Experian), and re-verify SSO sessions.",
        "Why It Matters & How PRO CRM Can Help: Relying solely on employee awareness is insufficient against AI-crafted phishing campaigns. PRO CRM implements Essential Eight Maturity Level 2/3 controls—including hardware-backed FIDO2 MFA, continuous zero-trust device attestation, and automated behavioral anomaly detection across your cloud environment.",
        "Source: Australian Signals Directorate (ASD) ACSC Phishing Threat Guidance & Response Protocols.",
    ]
}

def format_post_js(p):
    bullets_js = ",\n".join([f'      "{b}"' for b in p["bullets"]])
    body_js = ",\n".join([f'      {json.dumps(para)}' for para in p["body"]])
    tags_js = ", ".join([f'"{t}"' for t in p["tags"]])
    return f"""  {{
    slug: "{p['slug']}",
    title: "{p['title']}",
    date: "{p['date']}",
    author: "{p['author']}",
    category: "{p['category']}",
    subCategory: "{p['subCategory']}",
    region: "{p['region']}",
    readTime: "{p['readTime']}",
    isNew: true,
    badge: "{p['badge']}",
    tags: [{tags_js}],
    image: "{p['image']}",
    excerpt:
      "{p['excerpt']}",
    bullets: [
{bullets_js}
    ],
    body: [
{body_js}
    ],
  }},"""

# 1. Update site.js with phishing article
print("Updating site.js...")
with open(SITE_JS_PATH, "r", encoding="utf-8") as f:
    site_js = f.read()

if phishing_post["slug"] not in site_js:
    marker = "export const POSTS = [\n"
    idx = site_js.find(marker)
    if idx != -1:
        site_js = site_js[:idx + len(marker)] + format_post_js(phishing_post) + "\n" + site_js[idx + len(marker):]
        with open(SITE_JS_PATH, "w", encoding="utf-8") as f:
            f.write(site_js)
        print("✅ Added Phishing guide post to site.js!")
else:
    print("ℹ️ Post already in site.js.")

# 2. Update Blog.jsx with reduced NeverMissAnAlert font and prominent geometric banner
print("Updating Blog.jsx...")
with open(BLOG_JSX_PATH, "r", encoding="utf-8") as f:
    blog_jsx = f.read()

# Update NeverMissAnAlert component with reduced font and exact rewording
new_alert_comp = """export function NeverMissAnAlert() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email) return;
    setSubmitted(true);
    setTimeout(() => {
      setName("");
      setEmail("");
      setSubmitted(false);
    }, 4000);
  };

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 sm:p-6 shadow-xs my-6 overflow-hidden relative">
      <div className="relative flex flex-col lg:flex-row items-center justify-between gap-5 lg:gap-8">
        
        {/* Left: Compact Illustration + Text */}
        <div className="flex items-center gap-4 max-w-xl">
          <div className="shrink-0 flex items-center justify-center h-14 w-14 sm:h-16 sm:w-16 rounded-2xl bg-gradient-to-br from-rose-50 via-amber-50 to-emerald-50 border border-rose-100 p-2 shadow-2xs">
            <svg viewBox="0 0 100 100" className="h-full w-full">
              <ellipse cx="50" cy="78" rx="42" ry="12" fill="#65b878" />
              <path d="M 32 18 C 30 18 27 22 28 28 L 33 52 C 34 56 38 58 41 57 C 44 56 46 52 45 48 L 40 24 C 39 20 36 18 32 18 Z" fill="#e04860" />
              <circle cx="37" cy="65" r="7" fill="#e04860" />
              <circle cx="70" cy="30" r="5.5" fill="#084582" />
              <path d="M 64 36 L 76 36 L 73 54 L 67 54 Z" fill="#00a3c4" />
              <path d="M 67 54 L 63 74 L 67 74 L 70 60 L 73 74 L 77 74 L 73 54 Z" fill="#082b4c" />
            </svg>
          </div>

          <div className="space-y-0.5">
            <h3 className="text-base sm:text-lg font-black tracking-tight text-[#062c54]">
              Never Miss an Alert
            </h3>
            <p className="text-xs text-slate-500 font-normal leading-relaxed">
              Sign up for the latest cyber security alerts and get information on threats and how to keep yourself secure online.
            </p>
          </div>
        </div>

        {/* Right: Compact Form Input Fields & Button */}
        <div className="w-full lg:w-auto lg:min-w-[420px] space-y-2">
          {submitted ? (
            <div className="rounded-xl bg-emerald-50 border border-emerald-300 p-3 text-emerald-900 font-bold text-xs text-center">
              ✓ Thank you! You are now subscribed to PRO CRM Threat Advisories.
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-2">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <div>
                  <label className="block text-[10px] font-bold text-slate-600 mb-0.5">Your name</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Robin Bakshi"
                    className="w-full rounded-xl border border-slate-300 bg-slate-50/40 px-3 py-1.5 text-xs text-slate-900 placeholder:text-slate-400 focus:border-[#084582] focus:bg-white focus:outline-hidden transition"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-slate-600 mb-0.5">Email <span className="text-rose-500">*</span></label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@company.com.au"
                    className="w-full rounded-xl border border-slate-300 bg-slate-50/40 px-3 py-1.5 text-xs text-slate-900 placeholder:text-slate-400 focus:border-[#084582] focus:bg-white focus:outline-hidden transition"
                  />
                </div>
              </div>

              <div className="flex flex-col sm:flex-row items-center justify-between gap-2 pt-0.5">
                <span className="text-[10px] text-slate-400 leading-tight">
                  This site is protected by reCAPTCHA and Google <a href="/privacy" className="underline hover:text-slate-600">Privacy Policy</a> apply.
                </span>
                <button
                  type="submit"
                  className="w-full sm:w-auto shrink-0 rounded-xl bg-[#062c54] hover:bg-[#084582] px-4 py-2 text-xs font-black text-white shadow-xs transition cursor-pointer"
                >
                  Sign up for alerts
                </button>
              </div>
            </form>
          )}
        </div>

      </div>
    </div>
  );
}"""

alert_pattern = r"export function NeverMissAnAlert\(\) \{[\s\S]*?\n\}"
blog_jsx = re.sub(alert_pattern, new_alert_comp, blog_jsx)
print("✅ Updated NeverMissAnAlert with compact typography and exact rewording")

# Update BlogList Hero Section to prominently use geometric pattern as in Image 4
new_bloglist_hero = """      {/* 1. Hero Header — Prominent Geometric Blue Pattern Banner (Image 4 Style) */}
      <section
        style={{
          background: "linear-gradient(to right, rgba(5, 44, 84, 0.88) 0%, rgba(2, 108, 168, 0.72) 60%, rgba(5, 44, 84, 0.88) 100%), url('/assets/geo-pattern-blue.png') center/cover no-repeat",
        }}
        className="relative overflow-hidden text-white border-b border-blue-900/50 pt-10 pb-8 sm:pt-14 sm:pb-12 shadow-md"
      >
        {/* Ambient Lighting Layer */}
        <div className="absolute inset-0 backdrop-blur-[1px] pointer-events-none" />"""

old_bloglist_hero_pattern = r"\{\/\* 1\. Hero Header — Geometric Blue Pattern Banner Background \*\/\}[\s\S]*?<div className=\"relative mx-auto max-w-\[1560px\]"
blog_jsx = re.sub(old_bloglist_hero_pattern, new_bloglist_hero + "\n\n        <div className=\"relative mx-auto max-w-[1560px]", blog_jsx)
print("✅ Updated BlogList Hero Banner to use prominent Image 4 geometric background")

# Update BlogPost Hero Section to prominently use geometric pattern as in Image 3 & 4
new_blogpost_hero = """      {/* Hero Header Section with Prominent Geometric Pattern & Subtle Blur (Image 3 & 4) */}
      <section
        style={{
          background: "linear-gradient(135deg, rgba(5, 44, 84, 0.86) 0%, rgba(2, 108, 168, 0.70) 50%, rgba(6, 53, 101, 0.88) 100%), url('/assets/geo-pattern-blue.png') center/cover no-repeat",
        }}
        className="relative overflow-hidden text-white border-b border-blue-900/50 shadow-md"
      >
        {/* Background Image Carousel Slides with Smooth Ambient Blur */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {topicImages.map((imgUrl, idx) => (
            <div
              key={idx}
              className={`absolute inset-0 bg-cover bg-center transition-all duration-1000 transform blur-[2px] ${
                idx === activeSlideIndex
                  ? "opacity-60 scale-100"
                  : "opacity-0 scale-105"
              }`}
              style={{ backgroundImage: `url(${imgUrl})` }}
            />
          ))}
        </div>

        {/* Semi-Transparent Brand Navy Gradient Scrim for crisp text contrast */}
        <div
          className="absolute inset-0 pointer-events-none backdrop-blur-[1px]"
          style={{
            background:
              "linear-gradient(135deg, rgba(5, 44, 84, 0.75) 0%, rgba(2, 108, 168, 0.55) 50%, rgba(6, 53, 101, 0.80) 100%)",
          }}
        />"""

old_blogpost_hero_pattern = r"\{\/\* Hero Header Section with Geometric Blue Pattern & Ambient Blur \*\/\}[\s\S]*?<div className=\"relative mx-auto max-w-7xl"
blog_jsx = re.sub(old_blogpost_hero_pattern, new_blogpost_hero + "\n\n        <div className=\"relative mx-auto max-w-7xl", blog_jsx)
print("✅ Updated BlogPost Hero Banner to use prominent Image 3 & 4 geometric background")

with open(BLOG_JSX_PATH, "w", encoding="utf-8") as f:
    f.write(blog_jsx)
print("✅ Saved Blog.jsx successfully!")

print("Building procrm-app...")
res = subprocess.run(["npm", "run", "build"], cwd=PROCRM_APP_DIR, capture_output=True, text=True)
print("Build stdout:", res.stdout)
if res.returncode != 0:
    print("Build stderr:", res.stderr)
    exit(1)
print("✅ Build succeeded!")
