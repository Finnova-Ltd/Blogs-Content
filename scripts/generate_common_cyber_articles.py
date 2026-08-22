#!/usr/bin/env python3
"""
Finnova & PRO CRM Common Cyber Security Article Generator
==========================================================
Generates 6 authoritative, unique, zero-government-name cyber security guides
featuring:
1. Google Fonts Roboto typography scale (28px H1, 22px H2, 18px H3, 15.5px body)
2. Permanently fixed / sticky Col 2 sidebar on scroll
3. Interactive 3D Flip Card Cyber Security Tips Widget in Col 2 (6 animated flip cards)
4. Reading Scroll Progress Bar at the top of the viewport
5. Header Background Image Carousel cycling every 6 seconds
6. Complete Schema.org JSON-LD (NewsArticle + FAQPage + Organization)
"""

import os
import json
import re

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_BLOG_DIR = os.path.join(PROJECT_DIR, "pages", "blog")
PUBLIC_BLOG_DIR = os.path.join(PROJECT_DIR, "public", "pages", "blog")
POSTS_JSON_PATH = os.path.join(PROJECT_DIR, "posts.json")

os.makedirs(PAGES_BLOG_DIR, exist_ok=True)
os.makedirs(PUBLIC_BLOG_DIR, exist_ok=True)

# Curated High-Definition Light Cyber Security Carousel Images
HERO_CAROUSEL_IMAGES = [
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=80"
]

INTERACTIVE_FLIP_TIPS = [
    {
        "num": "Tip #1",
        "title": "Think about what you post online",
        "front": "Be mindful about what information you share online and who can access it.",
        "back": "Be mindful about what information you share online and who can access it. Once something is online, it can be nearly impossible to delete. Avoid sharing location tags, ID documents, or workplace badges."
    },
    {
        "num": "Tip #2",
        "title": "Get alerts on new cyber threats",
        "front": "Sign up to our free alert service to stay ahead of active security vulnerabilities.",
        "back": "Sign up to our free threat intelligence alert service. You’ll receive an instant security advisory when our security operations center identifies a new vulnerability or active credential attack."
    },
    {
        "num": "Tip #3",
        "title": "Talk about cyber security with family & staff",
        "front": "Upskill your team and protect vulnerable relatives through ongoing dialogue.",
        "back": "Be generous and assist older relatives with secure device setups. If you manage a business, continuously upskill your staff with simulated phishing training and zero-trust data handling policies."
    },
    {
        "num": "Tip #4",
        "title": "Avoid public Wi-Fi for banking & transactions",
        "front": "Unsecured wireless hotspots expose financial logins and payment tokens.",
        "back": "If you are purchasing items or transferring funds online, never connect via public Wi-Fi. Use only a secure, encrypted home network, trusted enterprise VPN, or mobile cellular data."
    },
    {
        "num": "Tip #5",
        "title": "Report cyber attacks & security incidents immediately",
        "front": "Rapid containment prevents lateral movement and widespread data loss.",
        "back": "If you suspect an account compromise, unauthorized funds transfer, or malware intrusion, report it immediately to your incident response team or call our 24/7 hotline on 1300 050 099."
    },
    {
        "num": "Tip #6",
        "title": "Check sender display name against actual email",
        "front": "Scammers frequently spoof executive names with fraudulent domains.",
        "back": "Phishing emails often disguise their display name as a trusted colleague or vendor. Always inspect the underlying domain headers. If the sender email address doesn't match the company domain, report and delete."
    }
]

ARTICLES = [
    {
        "id": "practical-ways-to-protect-yourself-online-cyber-security-guide",
        "slug": "practical-ways-to-protect-yourself-online-cyber-security-guide",
        "title": "Practical Ways to Protect Yourself Online: The 5 Essential Pillars of Modern Cyber Defence",
        "badge": "CYBER THREAT DEFENCE",
        "category": "Cyber Security",
        "date": "23-Aug-2026",
        "iso_date": "2026-08-23T08:30:00Z",
        "readTime": "6 min read",
        "author": "Finnova Cyber Threat Intelligence Desk",
        "authorRole": "Enterprise Information Security Unit",
        "excerpt": "Take control of your digital security and neutralize cyber attacks before they disrupt your business. Discover the 5 fundamental pillars of zero-trust defense: automatic patching, immutable cloud backups, phishing detection, MFA, and passphrases.",
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
        "toc": [
            {"id": "threat-landscape", "title": "1. The Anatomy of Modern Cyber Attacks"},
            {"id": "device-patching", "title": "2. Automatic Updates: Closing Vulnerability Windows"},
            {"id": "immutable-backups", "title": "3. The 3-2-1 Backup Strategy for Ransomware Immunity"},
            {"id": "zero-trust-mfa", "title": "4. Multi-Factor Authentication & Passphrase Architecture"},
            {"id": "phishing-defense", "title": "5. Spotting Social Engineering & Invoice Spoofing"},
            {"id": "incident-response", "title": "6. Emergency Response Protocol & Rapid Recovery"}
        ],
        "content_html": """
          <p class="article-lead">Cyber threats are no longer isolated to large financial institutions. Today, automated bots, ransomware gangs, and sophisticated social engineering networks target small-to-midmarket enterprises and individuals daily. Building a resilient cyber defense does not require complex military-grade infrastructure—it requires disciplined execution of five foundational security practices.</p>

          <h2 id="threat-landscape">1. The Anatomy of Modern Cyber Attacks</h2>
          <p>Over 88% of data breaches begin with a single preventable weakness: an unpatched application, an employee reusing a compromised password, or a fraudulent email attachment bypassing basic filters. Once inside, malicious payloads execute silently, exfiltrating customer records and encrypting local file servers.</p>

          <div class="article-data-table-wrapper" style="overflow-x:auto; margin:20px 0;">
            <table class="article-data-table" style="width:100%; border-collapse:collapse; text-align:left;">
              <thead>
                <tr style="background:#0A2540; color:#ffffff;">
                  <th style="padding:12px 14px; white-space:nowrap;">Attack Vector</th>
                  <th style="padding:12px 14px; white-space:nowrap;">Primary Vulnerability</th>
                  <th style="padding:12px 14px; white-space:nowrap;">Core Defence Measure</th>
                  <th style="padding:12px 14px;">Mitigation Impact</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;">Ransomware Intrusion</td>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">Unpatched Operating Systems</td>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:700; color:#16a34a;">Automated OS &amp; App Patching</td>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">Closes 90%+ of known exploit pathways</td>
                </tr>
                <tr>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;">Credential Stuffing</td>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">Reused Single-Factor Passwords</td>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:700; color:#16a34a;">FIDO2 Multi-Factor Auth (MFA)</td>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">Blocks 99.9% of automated account takeover bots</td>
                </tr>
                <tr>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;">Invoice Redirection Fraud</td>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">Email Sender Spoofing</td>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:700; color:#16a34a;">Out-of-Band Phone Verification</td>
                  <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">Eliminates payment rerouting losses completely</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h2 id="device-patching">2. Automatic Updates: Closing Vulnerability Windows</h2>
          <p>Software developers continuously release security patches to repair newly identified flaws. When an update notification appears, cybercriminals immediately reverse-engineer the patch to attack systems that have not yet updated.</p>
          <ul>
            <li><strong>Enable Universal Automatic Updates:</strong> Configure operating systems (macOS, Windows, iOS, Android) to download and install security fixes overnight automatically.</li>
            <li><strong>Third-Party Browser &amp; App Hygiene:</strong> Regularly update web browsers, PDF readers, and office productivity suites.</li>
            <li><strong>Retire End-of-Life Hardware:</strong> Devices that no longer receive manufacturer security support must be isolated or decommissioned.</li>
          </ul>

          <h2 id="immutable-backups">3. The 3-2-1 Backup Strategy for Ransomware Immunity</h2>
          <p>A reliable backup is your ultimate guarantee against data extortion. Following the industry-standard <strong>3-2-1 Rule</strong> ensures operational continuity:</p>
          <div style="background:#EFF6FF; border-left:4px solid #1D4ED8; padding:18px 20px; border-radius:0 10px 10px 0; margin:20px 0;">
            <strong style="display:block; color:#1E3A8A; font-size:0.95rem; margin-bottom:6px;">📦 The 3-2-1 Data Preservation Standard</strong>
            <ul style="margin:0; padding-left:20px; color:#1E293B; font-size:0.92rem; line-height:1.6;">
              <li><strong>3 Copies of Data:</strong> Maintain your primary working dataset plus two distinct backup copies.</li>
              <li><strong>2 Different Media Types:</strong> Store data across different mediums (e.g., local encrypted SSD + secure cloud bucket).</li>
              <li><strong>1 Offsite &amp; Immutable Copy:</strong> Maintain an air-gapped or write-once-read-many (WORM) cloud copy that cannot be altered or deleted by ransomware.</li>
            </ul>
          </div>

          <h2 id="zero-trust-mfa">4. Multi-Factor Authentication &amp; Passphrase Architecture</h2>
          <p>Traditional single passwords such as <code>Company2025!</code> are easily cracked by automated dictionaries in seconds. Implementing multi-layered identity assurance stops unauthorized intrusions cold:</p>
          <ul>
            <li><strong>Deploy Multi-Factor Authentication (MFA):</strong> Require an authenticator app (Google Authenticator, Microsoft Authenticator) or physical FIDO2 hardware key (YubiKey) on all email, CRM, and banking portals.</li>
            <li><strong>Transition to 4-Word Passphrases:</strong> Strings of four unpredictable words (e.g. <code>crystal-onion-clay-pretzel</code>) provide 15+ characters of cryptographic strength while remaining effortless for human recall.</li>
          </ul>

          <h2 id="phishing-defense">5. Spotting Social Engineering &amp; Invoice Spoofing</h2>
          <p>Social engineering relies on psychological triggers—urgency, authority, fear, and curiosity—to bypass technical controls:</p>
          <blockquote>
            <p><strong>Golden Security Rule:</strong> Never verify banking details, transfer requests, or password resets using contact details provided inside an unverified email or SMS. Always navigate directly to official websites or call pre-saved phone numbers.</p>
          </blockquote>

          <h2 id="incident-response">6. Emergency Response Protocol &amp; Rapid Recovery</h2>
          <p>If you discover suspicious activity on your device or network, immediately disconnect the affected machine from Wi-Fi and ethernet to prevent lateral spread. Alert your IT security administrator and contact our rapid response hotline on <strong>1300 050 099</strong> for forensic containment.</p>
        """
    },
    {
        "id": "automated-device-updates-patch-management-guide",
        "slug": "automated-device-updates-patch-management-guide",
        "title": "Automated Patch Management: Why Outdated Devices Are Hacker Magnets",
        "badge": "VULNERABILITY MANAGEMENT",
        "category": "Device Security",
        "date": "23-Aug-2026",
        "iso_date": "2026-08-23T08:30:00Z",
        "readTime": "5 min read",
        "author": "Finnova Cyber Threat Intelligence Desk",
        "authorRole": "Infrastructure Security Team",
        "excerpt": "Discover why software updates are your first and strongest line of cyber defense. Learn how to configure automated patch cycles across Windows, Mac, iOS, and Android to eliminate zero-day vulnerabilities.",
        "image": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1200&q=80",
        "toc": [
            {"id": "update-mechanics", "title": "1. How Attackers Exploit Unpatched Software"},
            {"id": "auto-update-setup", "title": "2. Configuring Automated Patch Cycles"},
            {"id": "legacy-risks", "title": "3. The Danger of End-of-Life (EOL) Devices"},
            {"id": "enterprise-patching", "title": "4. Centralized Patch Management for Small Business"}
        ],
        "content_html": """
          <p class="article-lead">Every major cyber attack in recent history—from the global WannaCry outbreak to targeted corporate ransomware attacks—exploited security vulnerabilities that already had patches available. Keeping devices updated is the single highest-impact defensive action an organization can take.</p>

          <h2 id="update-mechanics">1. How Attackers Exploit Unpatched Software</h2>
          <p>When security researchers or vendors discover a system vulnerability, they issue a security advisory alongside a code fix. Criminal syndicates monitor these disclosures to build automated scanning scripts that seek out unpatched IP addresses across the internet.</p>

          <h2 id="auto-update-setup">2. Configuring Automated Patch Cycles</h2>
          <p>Eliminate human error by enabling native automated updates across your device fleet:</p>
          <ul>
            <li><strong>macOS &amp; iOS:</strong> Navigate to <em>Settings &gt; General &gt; Software Update</em> and toggle on <em>Automatically Install Security Responses &amp; System Files</em>.</li>
            <li><strong>Microsoft Windows:</strong> Go to <em>Settings &gt; Windows Update &gt; Advanced Options</em> and enable automatic download and restart outside active business hours.</li>
            <li><strong>Android Devices:</strong> Open <em>Settings &gt; Security &amp; Privacy &gt; System &amp; Updates</em> to verify Google Play system and security patch status.</li>
          </ul>

          <h2 id="legacy-risks">3. The Danger of End-of-Life (EOL) Devices</h2>
          <p>When a phone, laptop, or router reaches its "End of Support" date, the manufacturer ceases publishing security patches. Continuing to connect an EOL device to your business network creates an unfixable security back-door.</p>

          <h2 id="enterprise-patching">4. Centralized Patch Management for Small Business</h2>
          <p>For organisations managing more than five endpoints, deploying a lightweight Mobile Device Management (MDM) or Remote Monitoring &amp; Management (RMM) solution ensures 100% patch compliance across remote and in-office staff.</p>
        """
    },
    {
        "id": "cloud-backups-immutable-storage-ransomware-protection",
        "slug": "cloud-backups-immutable-storage-ransomware-protection",
        "title": "The 3-2-1 Cloud Backup Strategy: Protecting Critical Data from Ransomware",
        "badge": "DISASTER RECOVERY",
        "category": "Data Protection",
        "date": "23-Aug-2026",
        "iso_date": "2026-08-23T08:30:00Z",
        "readTime": "5 min read",
        "author": "Finnova Cyber Threat Intelligence Desk",
        "authorRole": "Cloud Continuity Engineers",
        "excerpt": "Never worry about catastrophic data loss again. Implement the 3-2-1 backup standard with encrypted, immutable cloud storage to ensure zero downtime and rapid ransomware recovery.",
        "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",
        "toc": [
            {"id": "why-backups-fail", "title": "1. Why Connected Backups Fail in Ransomware Attacks"},
            {"id": "the-321-framework", "title": "2. The Modern 3-2-1-1-0 Backup Standard"},
            {"id": "cloud-immutability", "title": "3. Cloud Immutability & Object Lock Technology"},
            {"id": "testing-recovery", "title": "4. Routine Disaster Recovery Drill Protocols"}
        ],
        "content_html": """
          <p class="article-lead">Ransomware attackers deliberately search for and encrypt attached backup drives before encrypting the main database. Without isolated, immutable backups, companies face weeks of downtime and catastrophic data destruction.</p>

          <h2 id="why-backups-fail">1. Why Connected Backups Fail in Ransomware Attacks</h2>
          <p>If an external hard drive or network-attached storage (NAS) is continuously connected to your computer, malware can access and encrypt it in seconds. Backups must be mathematically isolated from the host environment.</p>

          <h2 id="the-321-framework">2. The Modern 3-2-1-1-0 Backup Standard</h2>
          <p>Leading enterprises expand the traditional 3-2-1 rule to include zero-error verification:</p>
          <ul>
            <li><strong>3 Copies of Data:</strong> Primary data plus two independent backups.</li>
            <li><strong>2 Different Media Types:</strong> Local high-speed disk plus remote cloud repository.</li>
            <li><strong>1 Offsite Copy:</strong> Geographically separate from your primary office.</li>
            <li><strong>1 Air-Gapped / Immutable Copy:</strong> Write-Once-Read-Many (WORM) storage that cannot be modified by any credential.</li>
            <li><strong>0 Errors:</strong> Verified through automated daily restore tests.</li>
          </ul>

          <h2 id="cloud-immutability">3. Cloud Immutability &amp; Object Lock Technology</h2>
          <p>By leveraging Object Lock on modern cloud storage providers, data written to the backup vault is locked against alteration or deletion for a predetermined retention period, neutralizing ransomware ransom demands completely.</p>
        """
    },
    {
        "id": "multi-factor-authentication-fido2-passkeys-guide",
        "slug": "multi-factor-authentication-fido2-passkeys-guide",
        "title": "Multi-Factor Authentication (MFA) & Passkeys: Eliminating Password Risk",
        "badge": "IDENTITY SECURITY",
        "category": "Access Management",
        "date": "23-Aug-2026",
        "iso_date": "2026-08-23T08:30:00Z",
        "readTime": "5 min read",
        "author": "Finnova Cyber Threat Intelligence Desk",
        "authorRole": "Identity & Access Architects",
        "excerpt": "Learn how multi-factor authentication (MFA) and biometric passkeys provide impenetrable barriers against credential theft, credential stuffing, and session hijacking across business apps.",
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
        "toc": [
            {"id": "mfa-fundamentals", "title": "1. The Three Authentication Factors"},
            {"id": "authenticator-vs-sms", "title": "2. Why Authenticator Apps Beat SMS Codes"},
            {"id": "passkeys-revolution", "title": "3. The Rise of FIDO2 Passkeys & Biometrics"},
            {"id": "enterprise-enforcement", "title": "4. Mandatory MFA Rollout Checklist"}
        ],
        "content_html": """
          <p class="article-lead">Over 80% of data breaches involve compromised or brute-forced passwords. Implementing Multi-Factor Authentication (MFA) increases the barrier to entry so significantly that automated credential attacks fail over 99.9% of the time.</p>

          <h2 id="mfa-fundamentals">1. The Three Authentication Factors</h2>
          <p>True MFA requires combining at least two independent credential categories:</p>
          <ul>
            <li><strong>Something You Know:</strong> A master passphrase or PIN.</li>
            <li><strong>Something You Have:</strong> An authenticator app token or physical hardware security key.</li>
            <li><strong>Something You Are:</strong> Biometric fingerprint, Touch ID, or facial recognition scan.</li>
          </ul>

          <h2 id="authenticator-vs-sms">2. Why Authenticator Apps Beat SMS Codes</h2>
          <p>SMS-based text message verification is vulnerable to SIM-swapping and telecommunication interception. Using dedicated TOTP authenticator apps (e.g. Google Authenticator, Microsoft Authenticator) generates cryptographic time-based codes locally on your device without transmitting over cellular networks.</p>

          <h2 id="passkeys-revolution">3. The Rise of FIDO2 Passkeys &amp; Biometrics</h2>
          <p>Passkeys replace traditional passwords entirely with public-key cryptography. Because passkeys are cryptographically bound to specific website domains, they are mathematically immune to phishing websites.</p>
        """
    },
    {
        "id": "secure-passphrases-vs-legacy-passwords-guide",
        "slug": "secure-passphrases-vs-legacy-passwords-guide",
        "title": "Passphrase Security: Why 4 Random Words Defeat Brute-Force Attacks",
        "badge": "CREDENTIAL SECURITY",
        "category": "Password Management",
        "date": "23-Aug-2026",
        "iso_date": "2026-08-23T08:30:00Z",
        "readTime": "4 min read",
        "author": "Finnova Cyber Threat Intelligence Desk",
        "authorRole": "Cryptographic Security Unit",
        "excerpt": "Stop struggling with complex, unmemorable passwords. Learn why 4-word passphrases like 'purple-duck-potato-boat' deliver superior entropy, length, and brute-force resistance.",
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
        "toc": [
            {"id": "password-length-entropy", "title": "1. Why Length Trumps Complexity"},
            {"id": "passphrase-creation", "title": "2. The 4-Word Passphrase Method"},
            {"id": "password-managers", "title": "3. Choosing & Securing an Enterprise Password Manager"},
            {"id": "anti-reuse-rules", "title": "4. The Golden Rule of Zero Credential Reuse"}
        ],
        "content_html": """
          <p class="article-lead">For decades, users were told to create short, complex passwords with symbols and numbers like <code>Tr0ub4dor&amp;3</code>. Modern graphics processors (GPUs) can crack an 8-character password in minutes. A 16-character passphrase made of four random dictionary words requires centuries of computational effort to brute force.</p>

          <h2 id="password-length-entropy">1. Why Length Trumps Complexity</h2>
          <p>Each character added to a passphrase exponentially increases the search space. A 16-character passphrase creates over 100 bits of cryptographic entropy, providing insurmountable resistance against offline dictionary attacks.</p>

          <h2 id="passphrase-creation">2. The 4-Word Passphrase Method</h2>
          <p>To create a robust passphrase, select four unrelated, random nouns and join them together: <code>crystal-onion-clay-pretzel</code> or <code>purple-duck-potato-boat</code>. Avoid famous quotes, song lyrics, or predictable personal milestones.</p>
        """
    },
    {
        "id": "recognise-and-report-scams-phishing-prevention-guide",
        "slug": "recognise-and-report-scams-phishing-prevention-guide",
        "title": "Recognising & Defeating Social Engineering: Defending Against Invoice Fraud & Scams",
        "badge": "PHISHING PREVENTION",
        "category": "Threat Awareness",
        "date": "23-Aug-2026",
        "iso_date": "2026-08-23T08:30:00Z",
        "readTime": "6 min read",
        "author": "Finnova Cyber Threat Intelligence Desk",
        "authorRole": "Fraud & Threat Analysis Group",
        "excerpt": "Arm your team against deceptive phishing emails, fake invoice redirects, and phone impersonators. Learn the 4 tell-tale psychological triggers used by scammers to manipulate human behavior.",
        "image": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1200&q=80",
        "toc": [
            {"id": "psychological-triggers", "title": "1. The 4 Psychological Weapons of Scammers"},
            {"id": "email-header-inspection", "title": "2. Inspecting Sender Headers & Fake Domains"},
            {"id": "invoice-fraud-protocol", "title": "3. The Dual-Approval Verification Protocol"},
            {"id": "reporting-scams", "title": "4. Reporting Incidents & Freezing Compromised Accounts"}
        ],
        "content_html": """
          <p class="article-lead">Cybercrime syndicates understand that manipulating human emotions is far easier than hacking cryptographic firewalls. By creating fabricated scenarios of extreme urgency, authority, or financial panic, scammers coerce victims into authorizing fraudulent payments.</p>

          <h2 id="psychological-triggers">1. The 4 Psychological Weapons of Scammers</h2>
          <ul>
            <li><strong>False Authority:</strong> Impersonating bank fraud managers, legal counsel, or senior corporate executives.</li>
            <li><strong>Artificial Urgency:</strong> Demanding payment or password confirmation "within 60 minutes" to prevent account cancellation.</li>
            <li><strong>Emotional Panic:</strong> Fabricating unauthorized credit card charges or legal enforcement notices.</li>
            <li><strong>Scarcity &amp; Greed:</strong> Presenting exclusive discounts, unexpected inheritance claims, or lucrative investment returns.</li>
          </ul>

          <h2 id="email-header-inspection">2. Inspecting Sender Headers &amp; Fake Domains</h2>
          <p>Scammers frequently register look-alike domain names (e.g. <code>pro-crm-support.com</code> instead of <code>procrm.com.au</code>). Train employees to examine the actual sender email address rather than relying on the visible display name.</p>
        """
    }
]

def generate_full_html_page(article):
    toc_links = "".join([f'<a href="#{item["id"]}" style="font-size:0.84rem; color:#0176D3; text-decoration:none; font-weight:500; padding:4px 0; border-bottom:1px dashed #f1f5f9;">{item["title"]}</a>' for item in article["toc"]])

    # Generate 3D Interactive Flip Cards for Col 2
    flip_cards_html = ""
    for tip in INTERACTIVE_FLIP_TIPS:
        flip_cards_html += f"""
        <div class="cyber-flip-card" onclick="this.classList.toggle('flipped')" style="perspective:1000px; cursor:pointer; margin-bottom:14px; user-select:none;">
          <div class="cyber-flip-inner" style="position:relative; width:100%; min-height:115px; text-align:left; transition:transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); transform-style:preserve-3d; border-radius:12px; box-shadow:0 4px 14px rgba(10,37,64,0.06);">
            <!-- Front Face -->
            <div class="cyber-flip-front" style="position:absolute; width:100%; height:100%; -webkit-backface-visibility:hidden; backface-visibility:hidden; background:#ffffff; border:1.5px solid #E2E8F0; border-radius:12px; padding:14px 16px; box-sizing:border-box; display:flex; flex-direction:column; justify-content:space-between;">
              <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                  <span style="font-size:0.72rem; font-weight:800; color:#0176D3; text-transform:uppercase; letter-spacing:0.06em;">{tip['num']}</span>
                  <span style="font-size:0.72rem; font-weight:700; color:#00876C; background:#ECFDF5; padding:2px 6px; border-radius:10px;">Tap to Flip ↻</span>
                </div>
                <h5 style="margin:0 0 4px 0; font-size:0.88rem; font-weight:700; color:#0A2540; line-height:1.35;">{tip['title']}</h5>
                <p style="margin:0; font-size:0.78rem; color:#64748B; line-height:1.4;">{tip['front']}</p>
              </div>
            </div>
            <!-- Back Face -->
            <div class="cyber-flip-back" style="position:absolute; width:100%; height:100%; -webkit-backface-visibility:hidden; backface-visibility:hidden; background:#0A2540; color:#ffffff; border:1.5px solid #0A2540; border-radius:12px; padding:14px 16px; box-sizing:border-box; transform:rotateY(180deg); display:flex; flex-direction:column; justify-content:space-between;">
              <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                  <span style="font-size:0.72rem; font-weight:800; color:#38BDF8; text-transform:uppercase; letter-spacing:0.06em;">⚡ Security Action</span>
                  <span style="font-size:0.7rem; color:#94A3B8;">Tap to Reset ↺</span>
                </div>
                <p style="margin:0; font-size:0.76rem; color:#E2E8F0; line-height:1.45;">{tip['back']}</p>
              </div>
            </div>
          </div>
        </div>
        """

    # Recent articles list
    recent_html = ""
    for ra in ARTICLES[:4]:
        recent_html += f"""
        <a href="/pages/blog/{ra['slug']}.html" style="display:flex; gap:12px; text-decoration:none; align-items:center; padding:8px 0; border-bottom:1px solid #f1f5f9;">
          <img src="{ra['image']}" alt="{ra['title']}" style="width:52px; height:42px; border-radius:6px; object-fit:cover; flex-shrink:0;">
          <div style="min-width:0;">
            <div style="font-size:0.82rem; font-weight:600; color:#0A2540; line-height:1.3; overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">{ra['title']}</div>
            <div style="font-size:0.72rem; color:#94A3B8; margin-top:2px;">{ra['date']}</div>
          </div>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{article['excerpt'][:155]}">
  <title>{article['title']} | Finnova &amp; PRO CRM</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">

  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #F8FAFC;
      color: #0A2540;
      margin: 0;
      padding: 0;
    }}

    /* Reading Scroll Progress Bar */
    #readingProgressBar {{
      position: fixed;
      top: 0;
      left: 0;
      height: 3.5px;
      width: 0%;
      background: linear-gradient(90deg, #0176D3 0%, #00C49F 100%);
      z-index: 99999;
      box-shadow: 0 0 10px rgba(1, 118, 211, 0.7);
      transition: width 0.1s ease-out;
    }}

    .container {{
      max-width: 1380px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    /* Header Hero Section with Background Carousel */
    .article-hero-header {{
      position: relative;
      background: #0A2540;
      color: #ffffff;
      padding: 48px 0 40px;
      overflow: hidden;
      box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }}
    .hero-slide {{
      position: absolute;
      top: -20px; left: -20px; right: -20px; bottom: -20px;
      background-size: cover;
      background-position: center 30%;
      filter: blur(3px) brightness(0.6) saturate(1.1);
      transform: scale(1.04);
      opacity: 0;
      transition: opacity 1.2s ease-in-out;
      z-index: 1;
    }}
    .hero-slide.active {{
      opacity: 1;
    }}
    .hero-overlay {{
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(180deg, rgba(10,37,64,0.82) 0%, rgba(10,37,64,0.96) 100%);
      z-index: 2;
    }}
    .hero-content {{
      position: relative;
      z-index: 3;
    }}

    /* Roboto Typography Scale */
    h1.article-h1 {{
      font-family: 'Roboto', sans-serif;
      font-size: clamp(22px, 2.4vw, 28px);
      font-weight: 700;
      line-height: 1.3;
      margin: 0 0 12px;
      color: #ffffff;
      letter-spacing: -0.01em;
    }}
    .article-lead-p {{
      font-size: 1rem;
      color: #E2E8F0;
      line-height: 1.55;
      max-width: 980px;
      margin: 0 0 18px;
    }}

    .article-body-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 370px;
      gap: 36px;
      margin-top: 36px;
      margin-bottom: 60px;
      align-items: start;
    }}
    @media (max-width: 992px) {{
      .article-body-grid {{
        grid-template-columns: 1fr;
      }}
      .article-sidebar-col {{
        position: static !important;
        max-height: none !important;
      }}
    }}

    /* Main Article Column */
    .article-main-card {{
      background: #ffffff;
      border: 1.5px solid #E2E8F0;
      border-radius: 16px;
      padding: 36px 40px;
      box-shadow: 0 4px 18px rgba(15, 23, 42, 0.03);
      font-size: 15.5px;
      line-height: 1.65;
      color: #334155;
    }}
    .article-main-card h2 {{
      font-size: 22px;
      font-weight: 700;
      line-height: 1.35;
      color: #0A2540;
      margin: 32px 0 14px;
      padding-bottom: 6px;
      border-bottom: 2px solid #E2E8F0;
    }}
    .article-main-card h3 {{
      font-size: 18px;
      font-weight: 600;
      color: #0A2540;
      margin: 24px 0 10px;
    }}
    .article-main-card p, .article-main-card li {{
      font-size: 15.5px;
      line-height: 1.65;
      color: #334155;
      margin-bottom: 16px;
    }}

    /* Permanently Fixed / Sticky Sidebar (Col 2) */
    .article-sidebar-col {{
      position: sticky;
      top: 80px;
      max-height: calc(100vh - 95px);
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
      padding-right: 2px;
    }}
    .article-sidebar-col::-webkit-scrollbar {{
      width: 4px;
    }}
    .article-sidebar-col::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 4px;
    }}

    /* Interactive Flip Card Styles */
    .cyber-flip-card.flipped .cyber-flip-inner {{
      transform: rotateY(180deg);
    }}
  </style>
</head>
<body>

  <!-- Reading Progress Bar -->
  <div id="readingProgressBar"></div>

  <!-- Site Header -->
  <header style="background:#ffffff; border-bottom:1px solid #E2E8F0; padding:12px 0; position:sticky; top:0; z-index:1000;">
    <div class="container" style="display:flex; justify-content:space-between; align-items:center;">
      <a href="/" style="text-decoration:none; font-weight:900; font-size:1.3rem; color:#0A2540; display:flex; align-items:center; gap:8px;">
        <span style="background:#0176D3; color:#ffffff; padding:4px 8px; border-radius:6px; font-size:0.9rem;">🛡️ PRO CRM</span>
        <span style="color:#64748B; font-weight:400; font-size:1.1rem;">·</span>
        <span>Finnova Security</span>
      </a>
      <div style="display:flex; align-items:center; gap:16px;">
        <span style="font-size:0.84rem; color:#16A34A; font-weight:700; display:flex; align-items:center; gap:6px;">
          ● SOC 24/7 Monitoring Active
        </span>
        <a href="tel:1300050099" style="background:#00876C; color:#ffffff; font-weight:800; font-size:0.85rem; padding:8px 16px; border-radius:8px; text-decoration:none; box-shadow:0 2px 8px rgba(0,135,108,0.25);">
          📞 1300 050 099
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Header with Background Image Carousel -->
  <section class="article-hero-header">
    <div class="hero-slide active" style="background-image: url('{HERO_CAROUSEL_IMAGES[0]}');"></div>
    <div class="hero-slide" style="background-image: url('{HERO_CAROUSEL_IMAGES[1]}');"></div>
    <div class="hero-slide" style="background-image: url('{HERO_CAROUSEL_IMAGES[2]}');"></div>
    <div class="hero-slide" style="background-image: url('{HERO_CAROUSEL_IMAGES[3]}');"></div>
    <div class="hero-overlay"></div>

    <div class="container hero-content">
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
        <span style="background:#0176D3; color:#ffffff; padding:4px 12px; border-radius:4px; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em;">
          {article['badge']}
        </span>
        <span style="font-size:0.82rem; color:#CBD5E1;">
          📅 {article['date']} · ⏱️ {article['readTime']} · ✍️ {article['author']}
        </span>
      </div>

      <h1 class="article-h1">{article['title']}</h1>
      <p class="article-lead-p">{article['excerpt']}</p>
    </div>
  </section>

  <!-- Main Content Grid -->
  <main class="container">
    <div class="article-body-grid">
      
      <!-- Col 1: Article Main Content -->
      <article class="article-main-card">
        {article['content_html']}
      </article>

      <!-- Col 2: Permanently Fixed Sidebar with Interactive 3D Flip Tips & Contact Card -->
      <aside class="article-sidebar-col">
        
        <!-- 1. PRO CRM & Finnova Security Operation Details Card -->
        <div style="background:#0A2540; border-radius:14px; padding:20px 18px; color:#ffffff; text-align:center; box-shadow:0 6px 20px rgba(10, 37, 64, 0.15);">
          <div style="font-size:0.72rem; color:#93C5FD; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">
            FINNOVA &amp; PRO CRM SECURITY ADVISORY
          </div>
          <h4 style="margin:0 0 6px 0; font-size:1.05rem; font-weight:800; color:#ffffff;">
            Enterprise Cyber &amp; Compliance Team
          </h4>
          <p style="font-size:0.8rem; color:#CBD5E1; line-height:1.45; margin:0 0 14px 0;">
            Specializing in cloud data protection, zero-trust access control, and emergency incident response.
          </p>
          <div style="background:rgba(255,255,255,0.08); border-radius:8px; padding:10px; font-size:0.75rem; text-align:left; margin-bottom:14px; border:1px solid rgba(255,255,255,0.12);">
            <div><strong>Operations:</strong> Melbourne, Victoria</div>
            <div><strong>Assurance:</strong> ISO 27001 &amp; Tier-1 Data Sovereignty</div>
            <div><strong>Direct Email:</strong> info@procrm.com.au</div>
          </div>
          <a href="tel:1300050099" style="display:block; background:#00876C; color:#ffffff; font-weight:800; font-size:0.88rem; padding:10px; border-radius:8px; text-decoration:none; box-shadow:0 4px 12px rgba(0,135,108,0.3); margin-bottom:8px;">
            📞 Call 1300 050 099
          </a>
          <a href="mailto:info@procrm.com.au" style="display:block; background:#ffffff; color:#0A2540; font-weight:700; font-size:0.82rem; padding:8px; border-radius:8px; text-decoration:none;">
            ✉️ Request Security Assessment
          </a>
        </div>

        <!-- 2. Interactive 3D Flip Card Cyber Security Tips Widget -->
        <div style="background:#ffffff; border:1.5px solid #E2E8F0; border-radius:14px; padding:18px 16px; box-shadow:0 4px 16px rgba(15, 23, 42, 0.04);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #F1F5F9;">
            <h4 style="margin:0; font-size:0.84rem; font-weight:800; color:#0A2540; text-transform:uppercase; letter-spacing:0.06em;">
              Level Up Your Security
            </h4>
            <span style="font-size:0.7rem; color:#1D4ED8; font-weight:700;">Interactive Tips</span>
          </div>
          <p style="font-size:0.78rem; color:#64748B; margin:0 0 12px 0;">
            Tap on any tip below to reveal practical action steps:
          </p>

          {flip_cards_html}
        </div>

        <!-- 3. Table of Contents -->
        <div style="background:#ffffff; border:1.5px solid #E2E8F0; border-radius:14px; padding:16px 18px; box-shadow:0 4px 16px rgba(15, 23, 42, 0.04);">
          <div style="font-size:0.82rem; font-weight:800; color:#0A2540; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;">
            📑 Table of Contents
          </div>
          <div style="display:flex; flex-direction:column; gap:6px;">
            {toc_links}
          </div>
        </div>

        <!-- 4. Recent Security Advisories -->
        <div style="background:#ffffff; border:1.5px solid #E2E8F0; border-radius:14px; padding:16px 18px; box-shadow:0 4px 16px rgba(15, 23, 42, 0.04);">
          <div style="font-size:0.82rem; font-weight:800; color:#0A2540; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;">
            🛡️ Recent Advisories
          </div>
          <div style="display:flex; flex-direction:column;">
            {recent_html}
          </div>
        </div>

      </aside>

    </div>
  </main>

  <!-- Interactive JavaScript for Carousel & Scroll Progress -->
  <script>
    // 1. Scroll Progress Bar
    window.addEventListener('scroll', function() {{
      var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      var scrolled = (winScroll / height) * 100;
      document.getElementById('readingProgressBar').style.width = scrolled + '%';
    }});

    // 2. Auto-cycling Hero Background Carousel
    var slides = document.querySelectorAll('.hero-slide');
    var currentSlide = 0;
    setInterval(function() {{
      if (slides.length > 0) {{
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add('active');
      }}
    }}, 6000);
  </script>

</body>
</html>"""

def main():
    print(f"🚀 Generating 6 Common Cyber Security Guides for PRO CRM & Finnova...")
    generated_count = 0

    for article in ARTICLES:
        html_code = generate_full_html_page(article)
        
        # Write to pages/blog/
        fpath = os.path.join(PAGES_BLOG_DIR, f"{article['slug']}.html")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html_code)

        # Write to public/pages/blog/
        public_fpath = os.path.join(PUBLIC_BLOG_DIR, f"{article['slug']}.html")
        with open(public_fpath, "w", encoding="utf-8") as f:
            f.write(html_code)

        generated_count += 1
        print(f"   ✓ Generated: {article['title']}")

    # Update posts.json with all new cyber security articles
    existing_posts = []
    if os.path.exists(POSTS_JSON_PATH):
        try:
            with open(POSTS_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                existing_posts = data if isinstance(data, list) else data.get("posts", [])
        except Exception:
            existing_posts = []

    # Prepend new cyber articles
    existing_slugs = {p.get("slug") for p in existing_posts}
    for art in reversed(ARTICLES):
        if art["slug"] not in existing_slugs:
            existing_posts.insert(0, {
                "id": art["id"],
                "slug": art["slug"],
                "title": art["title"],
                "category": art["category"],
                "badge": art["badge"],
                "date": art["date"],
                "iso_date": art["iso_date"],
                "readTime": art["readTime"],
                "author": art["author"],
                "authorRole": art["authorRole"],
                "authorImg": "/images/ez-mortgage-broker.webp",
                "excerpt": art["excerpt"],
                "snippet": art["excerpt"],
                "image": art["image"],
                "url": f"/pages/blog/{art['slug']}.html"
            })

    with open(POSTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_posts, f, indent=2)

    print(f"\n🎉 Successfully published {generated_count} Common Cyber Security Articles across PRO CRM & Finnova!")

if __name__ == "__main__":
    main()
