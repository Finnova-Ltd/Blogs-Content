#!/usr/bin/env python3
"""
Update PRO CRM Website (procrm.com.au) Blog Section:
1. Prepends the 6 new 2026-08-23 Cyber Security articles to POSTS in src/data/site.js
2. Replaces the static 3-card grid in src/pages/Home.jsx with a modern, smooth auto-playing multi-card Carousel
3. Always sorts all articles in strict descending order (newest first)
4. Adds animation to the top-right "Read More Articles →" button
5. Removes the redundant bottom "Read More Articles & Insights" button
"""

import os
import re

PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
SITE_JS_PATH = os.path.join(PROCRM_DIR, "src", "data", "site.js")
HOME_JSX_PATH = os.path.join(PROCRM_DIR, "src", "pages", "Home.jsx")

NEW_CYBER_POSTS = """
  {
    slug: "practical-ways-to-protect-yourself-online-cyber-security-guide",
    title: "Practical Ways to Protect Yourself Online: The 5 Essential Pillars of Modern Cyber Defence",
    date: "2026-08-23",
    author: "R BAKSHI",
    category: "Security Advisories",
    subCategory: "Cyber Threat Defence",
    region: "National",
    readTime: "6 min read",
    isNew: true,
    badge: "🔥 New Advisory",
    tags: ["Cyber Security", "Zero Trust", "Threat Mitigation", "Data Protection", "National"],
    image: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
    excerpt:
      "Take control of your digital security and neutralize cyber attacks before they disrupt your business. Discover the 5 fundamental pillars of zero-trust defense: automatic patching, immutable cloud backups, phishing detection, MFA, and passphrases.",
    bullets: [
      "Attack Surface Containment: Close 90%+ of exploit pathways through automated OS & app patching cycles.",
      "Immutable Cloud Vaults: Implement the 3-2-1 backup strategy to guarantee ransomware immunity without paying ransoms.",
      "Hardware-Backed MFA: Block 99.9% of automated credential takeover bots with FIDO2 passkeys.",
      "Phishing & Scam Defenses: Eliminate invoice redirection fraud through dual-approval verification."
    ],
    body: [
      "Cyber threats are no longer isolated to large financial institutions. Today, automated bots, ransomware gangs, and sophisticated social engineering networks target small-to-midmarket enterprises and individuals daily. Building a resilient cyber defense does not require complex military-grade infrastructure—it requires disciplined execution of foundational security practices.",
      "The 5 Pillars of Enterprise Digital Resilience:\\n• Automatic Patch Management: Eliminate zero-day vulnerabilities by enabling overnight automated patch cycles across all workstations and mobile devices.\\n• 3-2-1 Immutable Backups: Maintain an offsite, air-gapped copy of critical business databases that cannot be modified by ransomware.\\n• FIDO2 Multi-Factor Authentication: Eliminate password vulnerabilities with biometric passkeys and authenticator tokens.\\n• 4-Word Passphrase Architecture: Replace weak passwords with unpredictable 15+ character strings.\\n• Social Engineering Defence: Inspect sender headers and enforce verbal verification for banking changes.",
      "Why It Matters & How PRO CRM Helps: PRO CRM fortifies Australian business operations by implementing turnkey ISO 27001:2022 compliant cloud infrastructure, continuous vulnerability scanning, and automated incident triage.",
      "Source: Enterprise Information Security Research & PRO CRM Cyber Intelligence Desk."
    ]
  },
  {
    slug: "automated-device-updates-patch-management-guide",
    title: "Automated Patch Management: Why Outdated Devices Are Hacker Magnets",
    date: "2026-08-23",
    author: "R BAKSHI",
    category: "Security Advisories",
    subCategory: "Vulnerability Management",
    region: "National",
    readTime: "5 min read",
    isNew: true,
    badge: "🔥 Patch Advisory",
    tags: ["Patch Management", "Device Security", "Vulnerability Defense", "National"],
    image: "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1200&q=80",
    excerpt:
      "Discover why software updates are your first and strongest line of cyber defense. Learn how to configure automated patch cycles across Windows, Mac, iOS, and Android to eliminate zero-day vulnerabilities.",
    bullets: [
      "Zero-Day Window Elimination: Automated updates patch vulnerabilities before cybercriminals weaponize public exploit code.",
      "Operating System Automation: Configure macOS, Windows, and mobile devices to apply security patches outside core hours.",
      "End-of-Life Decommissioning: Identify and replace unsupported legacy hardware before they create permanent network backdoors.",
      "Centralized Fleet Management: Enforce 100% patch compliance across remote staff using lightweight MDM policies."
    ],
    body: [
      "Every major cyber attack in recent history exploited security vulnerabilities that already had patches available. Keeping devices updated is the single highest-impact defensive action an organization can take.",
      "Automated Patching Implementation Framework:\\n• Operating System Patching: Enable native automated background updates across all employee endpoints.\\n• Application & Browser Hygiene: Keep web browsers, PDF engines, and productivity tools current.\\n• End-of-Life Device Isolation: Immediately decommission hardware that has reached manufacturer end-of-support.\\n• Centralized Monitoring: Track patch rollout telemetry via enterprise dashboards.",
      "Why It Matters & How PRO CRM Helps: PRO CRM provides centralized device governance and automated vulnerability monitoring, ensuring distributed workforces remain 100% compliant with zero manual effort.",
      "Source: PRO CRM Infrastructure Security Unit & Global Vulnerability Databases."
    ]
  },
  {
    slug: "cloud-backups-immutable-storage-ransomware-protection",
    title: "The 3-2-1 Cloud Backup Strategy: Protecting Critical Data from Ransomware",
    date: "2026-08-23",
    author: "R BAKSHI",
    category: "Security Advisories",
    subCategory: "Disaster Recovery",
    region: "National",
    readTime: "5 min read",
    isNew: true,
    badge: "🛡️ Data Protection",
    tags: ["Cloud Backup", "Disaster Recovery", "Ransomware Protection", "National"],
    image: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",
    excerpt:
      "Never worry about catastrophic data loss again. Implement the 3-2-1 backup standard with encrypted, immutable cloud storage to ensure zero downtime and rapid ransomware recovery.",
    bullets: [
      "Ransomware Immunity: Object Lock and WORM storage prevent malicious encryption or deletion of backups.",
      "3-2-1 Preservation Rule: Maintain 3 copies of data across 2 media types with 1 copy stored in an isolated offsite cloud.",
      "Zero-Downtime Recovery: Automated daily restore drills ensure rapid business continuity during an emergency.",
      "End-to-End Encryption: Protect data at rest with AES-256 and in transit with TLS 1.3 cryptographic tunnels."
    ],
    body: [
      "Ransomware attackers deliberately search for and encrypt attached backup drives before encrypting the main database. Without isolated, immutable backups, companies face weeks of downtime and catastrophic data destruction.",
      "The Modern 3-2-1-1-0 Backup Standard:\\n• 3 Copies of Data: Primary working set plus two independent backup repositories.\\n• 2 Media Types: Local NVMe disk cache + encrypted sovereign cloud bucket.\\n• 1 Offsite Copy: Geographically isolated from your primary office.\\n• 1 Immutable Copy: Object-locked WORM vault resistant to all administrative deletion.\\n• 0 Recovery Errors: Verified through continuous automated restore testing.",
      "Why It Matters & How PRO CRM Helps: PRO CRM architects automated, immutable cloud backup pipelines that guarantee full recovery within minutes, neutralizing ransomware extortion completely.",
      "Source: PRO CRM Disaster Recovery & Cloud Continuity Engineering."
    ]
  },
  {
    slug: "multi-factor-authentication-fido2-passkeys-guide",
    title: "Multi-Factor Authentication (MFA) & Passkeys: Eliminating Password Risk",
    date: "2026-08-23",
    author: "R BAKSHI",
    category: "Security Advisories",
    subCategory: "Access Management",
    region: "National",
    readTime: "5 min read",
    isNew: true,
    badge: "🔐 Identity Security",
    tags: ["MFA", "Passkeys", "FIDO2", "Zero Trust", "National"],
    image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
    excerpt:
      "Learn how multi-factor authentication (MFA) and biometric passkeys provide impenetrable barriers against credential theft, credential stuffing, and session hijacking across business apps.",
    bullets: [
      "99.9% Attack Reduction: MFA blocks nearly all automated password cracking and brute-force bots.",
      "App Tokens over SMS: Hardware TOTP apps eliminate vulnerability to telecommunication SIM-swapping.",
      "FIDO2 Cryptography: Passkeys cryptographically bind logins to authentic domains, neutralizing fake phishing portals.",
      "Single Sign-On (SSO): Enforce mandatory zero-trust verification across all corporate tools."
    ],
    body: [
      "Over 80% of data breaches involve compromised or brute-forced passwords. Implementing Multi-Factor Authentication (MFA) increases the barrier to entry so significantly that automated credential attacks fail over 99.9% of the time.",
      "MFA & Passkey Architecture:\\n• Three Authentication Factors: Something you know (passphrase), something you have (app/key), something you are (biometric).\\n• Phishing-Resistant FIDO2: Cryptographic public/private key pairs that cannot be harvested by fake login portals.\\n• Zero-Trust Session Management: Short token lifespans and device health attestation.",
      "Why It Matters & How PRO CRM Helps: PRO CRM integrates enterprise SSO and phishing-resistant FIDO2 MFA across your CRM, communications, and database infrastructure.",
      "Source: PRO CRM Identity & Access Management Practice."
    ]
  },
  {
    slug: "secure-passphrases-vs-legacy-passwords-guide",
    title: "Passphrase Security: Why 4 Random Words Defeat Brute-Force Attacks",
    date: "2026-08-23",
    author: "R BAKSHI",
    category: "Security Advisories",
    subCategory: "Credential Security",
    region: "National",
    readTime: "4 min read",
    isNew: true,
    badge: "🔑 Password Security",
    tags: ["Passphrases", "Password Security", "Entropy", "National"],
    image: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
    excerpt:
      "Stop struggling with complex, unmemorable passwords. Learn why 4-word passphrases like 'purple-duck-potato-boat' deliver superior entropy, length, and brute-force resistance.",
    bullets: [
      "Length Over Complexity: 16+ character passphrases require centuries of GPU processing to brute force.",
      "4 Random Words: Combining four unrelated nouns provides exceptional cryptographic entropy and memorable usability.",
      "Zero Password Reuse: Eliminate cross-account compromise by isolating credentials.",
      "Enterprise Vaults: Secure master credentials inside audited zero-knowledge password managers."
    ],
    body: [
      "Modern graphics processors can crack short 8-character passwords in minutes. A 16-character passphrase made of four random dictionary words requires centuries of computational effort to brute force while remaining effortless for human memory.",
      "Passphrase Best Practices:\\n• 4 Unpredictable Words: Select unrelated terms like 'crystal-onion-clay-pretzel'.\\n• Avoid Common Idioms: Do not use famous quotes, song lyrics, or predictable phrases.\\n• Zero-Knowledge Storage: Secure unique passphrases in an enterprise-managed vault.",
      "Why It Matters & How PRO CRM Helps: PRO CRM promotes zero-friction security policies that empower employees while maintaining strict enterprise cryptographic compliance.",
      "Source: Cryptographic Security Standards & PRO CRM Security Engineering."
    ]
  },
  {
    slug: "recognise-and-report-scams-phishing-prevention-guide",
    title: "Recognising & Defeating Social Engineering: Defending Against Invoice Fraud & Scams",
    date: "2026-08-23",
    author: "R BAKSHI",
    category: "Security Advisories",
    subCategory: "Threat Awareness",
    region: "National",
    readTime: "6 min read",
    isNew: true,
    badge: "🎣 Fraud Prevention",
    tags: ["Phishing", "Social Engineering", "Invoice Fraud", "National"],
    image: "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1200&q=80",
    excerpt:
      "Arm your team against deceptive phishing emails, fake invoice redirects, and phone impersonators. Learn the 4 tell-tale psychological triggers used by scammers to manipulate human behavior.",
    bullets: [
      "Psychological Trigger Awareness: Recognize urgency, authority, fear, and scarcity used to bypass rational judgment.",
      "Sender Domain Verification: Inspect underlying email headers to expose look-alike spoofed domains.",
      "Dual-Approval Payments: Enforce mandatory verbal confirmation on pre-saved phone numbers for banking changes.",
      "Rapid Incident Escalation: Trigger immediate account freezes and forensic incident response on 1300 050 099."
    ],
    body: [
      "Cybercriminals manipulate human emotions to bypass technical controls. By creating artificial scenarios of panic or urgency, attackers trick personnel into authorizing fraudulent transfers.",
      "Social Engineering Defense Protocols:\\n• The 4 Psychological Weapons: False authority, artificial urgency, emotional fear, and scarcity deals.\\n• Header Inspection: Check the true originating domain rather than the friendly display name.\\n• Out-of-Band Verification: Always call vendors on verified numbers before updating bank payment details.\\n• 24/7 Incident Escalation: Report suspicious contacts immediately to our emergency support desk.",
      "Why It Matters & How PRO CRM Helps: PRO CRM trains teams and implements email security gateways (DMARC, SPF, DKIM) that intercept phishing campaigns before they reach inboxes.",
      "Source: PRO CRM Fraud Analysis & Social Engineering Defense Group."
    ]
  },
"""

def update_site_js():
    print(f"📖 Reading {SITE_JS_PATH}...")
    with open(SITE_JS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already inserted
    if "practical-ways-to-protect-yourself-online-cyber-security-guide" in content:
        print("ℹ️ New cyber articles already present in site.js.")
    else:
        # Prepend to export const POSTS = [
        target = "export const POSTS = ["
        if target in content:
            content = content.replace(target, target + NEW_CYBER_POSTS)
            with open(SITE_JS_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            print("✅ Successfully prepended 6 new Cyber Security articles to site.js!")
        else:
            print("⚠️ Could not find 'export const POSTS = [' in site.js.")

def update_home_jsx():
    print(f"📖 Reading {HOME_JSX_PATH}...")
    with open(HOME_JSX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure carousel state is present in Home component
    if "const [carouselIndex, setCarouselIndex] = useState(0);" not in content:
        # Add carouselIndex and isHovered state near top of Home component
        state_marker = "const [openFaqIndex, setOpenFaqIndex] = useState(null);"
        new_states = """const [openFaqIndex, setOpenFaqIndex] = useState(null);
  const [carouselIndex, setCarouselIndex] = useState(0);
  const [isCarouselHovered, setIsCarouselHovered] = useState(false);"""
        content = content.replace(state_marker, new_states, 1)

    # Ensure useEffect auto-play timer is present
    if "/* Auto-play Blog Carousel */" not in content:
        timer_code = """
  // Auto-play Blog Carousel every 4.5 seconds
  useEffect(() => {
    if (isCarouselHovered) return;
    const sortedCount = [...POSTS].length;
    const interval = setInterval(() => {
      setCarouselIndex((prev) => (prev + 1) % Math.max(1, sortedCount - 2));
    }, 4500);
    return () => clearInterval(interval);
  }, [isCarouselHovered]);
"""
        # Find position after other useEffects or near component start
        if "useEffect(" in content:
            content = re.sub(r"(useEffect\(\(\) => \{[\s\S]*?\}, \[.*?\]\);)", r"\1\n" + timer_code, content, count=1)
        else:
            # Insert before return (
            content = content.replace("return (", timer_code + "\n  return (", 1)

    # Locate the Blog section (id="blog") and replace with Carousel Component
    # We want:
    # 1. Top-Right "Read More Articles →" with micro-animation (pulsing gradient glow & hover scale)
    # 2. Left & Right navigation buttons
    # 3. Smooth sliding multi-card carousel showing articles in descending date order
    # 4. Pagination dots
    # 5. NO redundant bottom button!

    old_blog_section_pattern = re.compile(
        r'<div id="blog" className="pt-12 pb-6 scroll-mt-24">[\s\S]*?{/\* IMAGE 4: Full Salesforce Contact Experience \*/}',
        re.MULTILINE
    )

    new_blog_carousel_jsx = """<div id="blog" className="pt-12 pb-6 scroll-mt-24">
          <Reveal>
            {/* Section Header with Animated Top-Right Button & Carousel Controls */}
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-slate-200 pb-6 mb-8">
              <div className="space-y-2 max-w-2xl">
                <span className="inline-flex items-center gap-1.5 rounded-full bg-blue-50 px-3 py-1 text-xs font-black uppercase tracking-wider text-[#084582] border border-blue-100">
                  Knowledge &amp; Market Advisories
                </span>
                <h2 className="text-3xl md:text-4xl font-black text-slate-900">
                  Latest Articles &amp; Insights
                </h2>
                <p className="text-slate-600 text-sm md:text-base font-medium">
                  Stay informed with the latest updates on Australian CRM architecture, NDIS compliance, financial advisory standards, and cyber defence.
                </p>
              </div>

              {/* Top Controls: Animated Button + Carousel Chevrons */}
              <div className="flex items-center gap-4 self-start md:self-auto shrink-0">
                {/* Animated Read More Articles Button */}
                <Link
                  to="/blog"
                  className="relative inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-[#084582] via-[#0176D3] to-[#084582] bg-[length:200%_auto] hover:bg-[position:right_center] px-6 py-3 text-xs font-black text-white shadow-lg shadow-blue-900/20 hover:shadow-blue-600/40 hover:scale-105 active:scale-95 transition-all duration-500 group overflow-hidden border border-blue-400/30"
                >
                  <span className="relative z-10 flex items-center gap-1.5 tracking-wide">
                    <span>Read More Articles</span>
                    <span className="transition-transform duration-300 group-hover:translate-x-1">→</span>
                  </span>
                  <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
                </Link>

                {/* Left & Right Chevron Controls */}
                <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl border border-slate-200">
                  <button
                    type="button"
                    onClick={() => {
                      const total = [...POSTS].length;
                      setCarouselIndex((prev) => (prev === 0 ? Math.max(0, total - 3) : prev - 1));
                    }}
                    aria-label="Previous Articles"
                    className="h-8 w-8 rounded-lg bg-white text-slate-700 hover:bg-[#084582] hover:text-white shadow-xs grid place-items-center text-sm font-black transition cursor-pointer"
                  >
                    ‹
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      const total = [...POSTS].length;
                      setCarouselIndex((prev) => (prev >= total - 3 ? 0 : prev + 1));
                    }}
                    aria-label="Next Articles"
                    className="h-8 w-8 rounded-lg bg-white text-slate-700 hover:bg-[#084582] hover:text-white shadow-xs grid place-items-center text-sm font-black transition cursor-pointer"
                  >
                    ›
                  </button>
                </div>
              </div>
            </div>

            {/* Auto-Playing Interactive Multi-Card Carousel in Descending Date Order */}
            <div 
              className="relative overflow-hidden"
              onMouseEnter={() => setIsCarouselHovered(true)}
              onMouseLeave={() => setIsCarouselHovered(false)}
            >
              {(() => {
                const sortedPosts = [...POSTS].sort((a, b) => new Date(b.date) - new Date(a.date));
                return (
                  <div 
                    className="flex transition-transform duration-700 ease-out gap-6"
                    style={{
                      transform: `translateX(-${carouselIndex * (100 / 3 + 1.2)}%)`
                    }}
                  >
                    {sortedPosts.map((post) => (
                      <div 
                        key={post.slug} 
                        className="w-full sm:w-[calc(50%-12px)] lg:w-[calc(33.333%-16px)] shrink-0"
                      >
                        <article className="h-full group rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-xs hover:shadow-2xl hover:border-blue-400 transition-all duration-300 flex flex-col justify-between transform hover:-translate-y-1">
                          <div>
                            {/* Top Thumbnail Image */}
                            <div className="relative aspect-[16/10] w-full overflow-hidden bg-slate-100">
                              <img
                                src={post.image}
                                alt={post.title}
                                loading="lazy"
                                className="h-full w-full object-cover transition duration-700 group-hover:scale-108"
                              />
                              <div className="absolute top-2.5 left-2.5">
                                <span className="rounded-md bg-[#084582]/90 backdrop-blur-xs px-2.5 py-1 text-[10px] font-black text-white uppercase tracking-wider shadow-xs">
                                  {post.category}
                                </span>
                              </div>
                            </div>

                            {/* Card Content */}
                            <div className="p-5 space-y-2.5">
                              <div className="flex items-center justify-between text-[11px] font-bold text-slate-400">
                                <span>{postDate(post.date)}</span>
                                <span>{post.readTime || "5 min read"}</span>
                              </div>

                              <h3 className="text-base font-black text-slate-900 group-hover:text-[#084582] transition leading-snug line-clamp-2">
                                <Link to={`/blog/${post.slug}`} className="hover:underline">
                                  {post.title}
                                </Link>
                              </h3>

                              <p className="text-xs text-slate-600 font-medium leading-relaxed line-clamp-3">
                                {post.excerpt}
                              </p>
                            </div>
                          </div>

                          <div className="px-5 pb-5 pt-1 border-t border-slate-100 flex items-center justify-between">
                            <Link
                              to={`/blog/${post.slug}`}
                              className="inline-flex items-center gap-1.5 text-xs font-black text-[#084582] group-hover:text-[#0176D3] transition group-hover:translate-x-1"
                            >
                              <span>Read article</span>
                              <span>→</span>
                            </Link>
                          </div>
                        </article>
                      </div>
                    ))}
                  </div>
                );
              })()}
            </div>

            {/* Pagination Indicators (Dots) */}
            <div className="flex justify-center items-center gap-2 pt-6">
              {(() => {
                const total = [...POSTS].length;
                const maxPages = Math.max(1, total - 2);
                return Array.from({ length: maxPages }).map((_, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => setCarouselIndex(idx)}
                    aria-label={`Go to slide ${idx + 1}`}
                    className={`h-2 rounded-full transition-all duration-300 cursor-pointer ${
                      carouselIndex === idx 
                        ? "w-8 bg-[#084582]" 
                        : "w-2 bg-slate-300 hover:bg-slate-400"
                    }`}
                  />
                ));
              })()}
            </div>
          </Reveal>
        </div>

        {/* IMAGE 4: Full Salesforce Contact Experience */}"""

    if old_blog_section_pattern.search(content):
        content = old_blog_section_pattern.sub(new_blog_carousel_jsx, content)
        with open(HOME_JSX_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Successfully updated Home.jsx with Auto-Playing Blog Carousel, Animated Button & Removed Redundant Bottom CTA!")
    else:
        print("⚠️ Could not match old blog section pattern in Home.jsx. Applying fallback replacement...")
        # Direct string replacement
        old_div_start = '<div id="blog" className="pt-12 pb-6 scroll-mt-24">'
        old_div_end = '{/* IMAGE 4: Full Salesforce Contact Experience */}'
        if old_div_start in content and old_div_end in content:
            idx1 = content.find(old_div_start)
            idx2 = content.find(old_div_end)
            content = content[:idx1] + new_blog_carousel_jsx + content[idx2 + len(old_div_end):]
            with open(HOME_JSX_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            print("✅ Successfully replaced blog section in Home.jsx via fallback!")

def main():
    print("🚀 Starting PRO CRM Blog Carousel & Descending Order Overhaul...")
    if not os.path.exists(PROCRM_DIR):
        print(f"❌ Error: {PROCRM_DIR} does not exist.")
        return

    update_site_js()
    update_home_jsx()
    print("🎉 Overhaul complete!")

if __name__ == "__main__":
    main()
