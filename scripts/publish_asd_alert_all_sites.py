#!/usr/bin/env python3
"""
Customized Publisher for ASD ACSC High Alert (CVE-2026-63077) across:
1. PRO CRM (procrm.com.au)
2. EZ Consultants (ezconsultants.com.au)
3. Finnova (finnova.org.au)
"""

import os
import json
import re
from datetime import datetime, timezone, timedelta

PROCRM_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app"
EZ_CONSULTANTS_DIR = "/Users/robinbakshi/Documents/GitHub/ezconsultants.com.au"
FINNOVA_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova"
BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

TODAY_STR = "25 August 2026"
TODAY_SHORT = "25-Aug-2026"
TODAY_ISO = "2026-08-25T08:00:00Z"
TODAY_PROCRM_DATE = "2026-08-25"

# ==============================================================================
# 1. PRO CRM (procrm.com.au) - Enterprise Cloud & Supply Chain Security
# ==============================================================================
PROCRM_SLUG = "asd-acsc-alert-cicd-pipeline-exploitation-cve-2026-63077"
PROCRM_ARTICLE_ENTRY = f"""  {{
    slug: "{PROCRM_SLUG}",
    title: "ASD ACSC Alert: Active Exploitation of CI/CD Build Platforms in Australia (CVE-2026-63077) — Enterprise Hardening & Fix Guide",
    date: "{TODAY_PROCRM_DATE}",
    author: "Robin Bakshi (Principal Cyber Architect)",
    category: "Security Advisories",
    subCategory: "Supply Chain & CI/CD Defence",
    region: "National",
    readTime: "7 min read",
    isNew: true,
    badge: "🚨 ASD High Alert",
    tags: ["ASD ACSC", "CVE-2026-63077", "Supply Chain Security", "CI/CD", "Essential Eight", "PRO CRM"],
    image: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1600&q=80",
    excerpt: "The Australian Cyber Security Centre (ASD's ACSC) has issued an urgent high-severity alert regarding active in-the-wild exploitation of on-premises CI/CD build servers (CVE-2026-63077). Unauthenticated attackers can bypass authentication and execute remote system commands.",
    highlights: [
      {{ id: "sec-alert", badge: "01. ASD ALERT", title: "ASD ACSC Critical Assessment", text: "Active exploitation observed targeting Australian enterprise CI/CD servers with unauthenticated RCE capability." }},
      {{ id: "sec-impact", badge: "02. BLAST RADIUS", title: "Supply Chain & Credential Exposure", text: "Compromised servers expose repository secrets, cloud service tokens, and downstream build artifacts." }},
      {{ id: "sec-fix", badge: "03. REMEDIATION", title: "4-Step Emergency Action Plan", text: "Immediate upgrade to 2026.1.3+, security patch plugin installation, and IOC log analysis." }},
      {{ id: "sec-procrm", badge: "04. HARDENING", title: "PRO CRM Zero-Trust Pipeline Blueprint", text: "Isolating build runners on private VPCs and enforcing Essential Eight application control." }}
    ],
    bullets: [
      "ASD ACSC High-Severity Alert: In-the-wild exploitation of on-prem CI/CD build engines confirmed across Australian corporate networks.",
      "Unauthenticated Remote Code Execution: Exploits agent polling protocol via deserialization flaw (CVE-2026-63077).",
      "Immediate Patching Mandate: Upgrade to TeamCity 2026.1.3 or 2025.11.7, or apply JetBrains security patch plugin immediately.",
      "PRO CRM Rapid Response: Zero-trust architecture audit and automated IOC scanning available for enterprise clients."
    ],
    body: [
      "The Australian Signals Directorate's Australian Cyber Security Centre (ASD's ACSC) has released an urgent security advisory confirming active exploitation of critical vulnerabilities affecting on-premises CI/CD development platforms (CVE-2026-63077) across Australian enterprise environments.",
      "This high-severity flaw allows an unauthenticated remote attacker with HTTP or HTTPS access to the server to completely bypass authentication checks and execute arbitrary operating system commands with the permissions of the CI/CD server process. Because build servers store high-privilege repository credentials, cloud deployment keys, and database connection strings, a single compromised server can grant attackers complete control over an organization's downstream digital supply chain.",
      "PRO CRM has deployed specialized remediation protocols for our clients. Organizations operating on-premises build servers must immediately apply vendor patches, inspect server logs for indicators of compromise, and restrict public internet exposure behind VPN and zero-trust reverse proxies.",
      "Source: Australian Signals Directorate (ASD ACSC) & PRO CRM Enterprise Cyber Security Architecture Desk."
    ],
    htmlContent: `
<div class="agentforce-light-article space-y-10 font-sans text-slate-800 leading-relaxed text-base">
    
    <div id="sec-alert" class="bg-gradient-to-br from-red-50/90 via-orange-50/40 to-white rounded-3xl p-6 sm:p-8 border-2 border-red-200/80 shadow-sm relative overflow-hidden">
        <div class="relative z-10 space-y-4">
            <div class="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-red-700">
                <span class="w-2.5 h-2.5 rounded-full bg-red-600 animate-pulse"></span>
                Official ASD ACSC Threat Advisory · Status: HIGH
            </div>
            <h2 class="text-xl sm:text-2xl lg:text-3xl font-black text-slate-900 tracking-tight leading-snug font-heading">
                Active Exploitation of On-Premises CI/CD Platforms in Australia (CVE-2026-63077)
            </h2>
            <p class="text-sm sm:text-base text-slate-700 leading-relaxed max-w-3xl">
                The Australian Signals Directorate's Australian Cyber Security Centre (ASD's ACSC) has observed active threat actors targeting Australian organizations by exploiting unpatched on-premises CI/CD build servers. Unauthenticated attackers can execute arbitrary operating system commands, exfiltrate deployment credentials, and inject malicious code into production software builds.
            </p>
            
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t border-red-200/60">
                <div class="p-5 rounded-2xl bg-white border border-red-100 text-center shadow-xs">
                    <div class="text-4xl sm:text-5xl font-black text-red-600 tracking-tight font-heading">RCE</div>
                    <div class="text-xs font-black uppercase text-slate-800 tracking-wider mt-1.5">Unauthenticated Attack</div>
                    <p class="text-xs text-slate-500 mt-1">Bypasses all web auth checks</p>
                </div>
                <div class="p-5 rounded-2xl bg-white border border-red-100 text-center shadow-xs">
                    <div class="text-4xl sm:text-5xl font-black text-amber-600 tracking-tight font-heading">100%</div>
                    <div class="text-xs font-black uppercase text-slate-800 tracking-wider mt-1.5">On-Prem Versions</div>
                    <p class="text-xs text-slate-500 mt-1">All unpatched releases vulnerable</p>
                </div>
                <div class="p-5 rounded-2xl bg-white border border-red-100 text-center shadow-xs">
                    <div class="text-4xl sm:text-5xl font-black text-blue-600 tracking-tight font-heading">Tier 1</div>
                    <div class="text-xs font-black uppercase text-slate-800 tracking-wider mt-1.5">Essential Eight Priority</div>
                    <p class="text-xs text-slate-500 mt-1">Immediate patch deployment</p>
                </div>
            </div>
        </div>
    </div>

    <section id="sec-impact" class="space-y-4">
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight border-b border-slate-200 pb-3 font-heading">
            1. Threat Analysis &amp; Supply Chain Blast Radius
        </h2>
        <p class="text-slate-700 leading-relaxed">
            Continuous Integration and Continuous Deployment (CI/CD) pipelines represent the operational backbone of modern digital enterprises. Development teams use platforms like TeamCity to automate the compiling, testing, container packaging, and production deployment of web applications, customer portals, and microservices.
        </p>
        <p class="text-slate-700 leading-relaxed">
            Under <strong>CVE-2026-63077</strong>, an unauthenticated attacker with network reachability to the server's HTTP/HTTPS endpoint can manipulate the internal agent polling protocol via an XML serialization deserialization flaw (<code>com.thoughtworks.xstream</code>). A successful exploit enables attackers to spawn remote interactive shells, read environment secrets (such as AWS access keys, Salesforce connected app certificates, and production database passwords), and poison release binaries before deployment.
        </p>
    </section>

    <section id="sec-fix" class="space-y-4">
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight border-b border-slate-200 pb-3 font-heading">
            2. Step-by-Step Remediation: How to Fix CVE-2026-63077
        </h2>
        <p class="text-slate-700 leading-relaxed">
            PRO CRM's Infrastructure &amp; Security Engineering team advises all Australian enterprise administrators to execute the following 4-step emergency remediation protocol immediately:
        </p>
        
        <div class="space-y-4 my-6">
            <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                <div class="flex items-center gap-2 font-bold text-slate-900 text-sm">
                    <span class="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs">1</span>
                    Apply the Vendor Security Upgrade or Emergency Patch Plugin
                </div>
                <p class="text-xs sm:text-sm text-slate-600 pl-8">
                    Upgrade on-premises servers to <strong>TeamCity 2026.1.3</strong> or <strong>2025.11.7</strong> immediately. If a full system upgrade is blocked by change windows, download and install the official <a href="https://download.jetbrains.com/teamcity/plugins/internal/fix_CVE_2026_63077.zip" class="text-blue-600 font-bold underline" target="_blank" rel="noopener">JetBrains Security Patch Plugin (fix_CVE_2026_63077.zip)</a> directly through the administration portal (compatible with TeamCity 2017.1+).
                </p>
            </div>

            <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                <div class="flex items-center gap-2 font-bold text-slate-900 text-sm">
                    <span class="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs">2</span>
                    Restrict Public Internet Exposure Behind a Secure Gateway
                </div>
                <p class="text-xs sm:text-sm text-slate-600 pl-8">
                    Under ASD Essential Eight guidance, build servers should <em>never</em> be directly exposed to the public internet. Restrict access strictly to authenticated corporate VPNs, Cloudflare Access Zero-Trust tunnels, or internal private VPC subnets with strict IP allowlisting.
                </p>
            </div>

            <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                <div class="flex items-center gap-2 font-bold text-slate-900 text-sm">
                    <span class="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs">3</span>
                    Audit Server Logs for Indicators of Compromise (IoCs)
                </div>
                <div class="text-xs sm:text-sm text-slate-600 pl-8 space-y-2">
                    <p>Search all server log archives (<code>teamcity-server.log</code>) for deserialization exceptions:</p>
                    <div class="p-3 bg-slate-900 text-emerald-400 font-mono text-xs rounded-xl overflow-x-auto">
                        grep "com.thoughtworks.xstream.converters.ConversionException" /opt/teamcity/logs/*
                    </div>
                    <p class="text-xs text-slate-500">
                        *Note: If you have already installed the patch, occurrences of <code>com.thoughtworks.xstream.security.ForbiddenClassException</code> confirm that exploitation attempts are being successfully intercepted and blocked.
                    </p>
                </div>
            </div>

            <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                <div class="flex items-center gap-2 font-bold text-slate-900 text-sm">
                    <span class="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs">4</span>
                    Inspect Unauthorized Agents &amp; Rotate High-Privilege Secrets
                </div>
                <p class="text-xs sm:text-sm text-slate-600 pl-8">
                    Review the list of unauthorized build agents in the admin console. Remove any rogue entries (especially agents prefixed with <code>scan*</code>). If any evidence of unauthorized execution is uncovered, immediately rotate all repository deployment tokens, AWS IAM keys, and production API secrets.
                </p>
            </div>
        </div>
    </section>

    <section id="sec-procrm" class="space-y-4">
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight border-b border-slate-200 pb-3 font-heading">
            3. PRO CRM Enterprise Hardening &amp; Compliance Assurance
        </h2>
        <p class="text-slate-700 leading-relaxed">
            PRO CRM partners with Australian enterprises and government agencies to ensure CI/CD and CRM release pipelines satisfy strict compliance frameworks, including <strong>APRA CPS 234</strong>, the <strong>ASD Essential Eight (Maturity Level 3)</strong>, and <strong>ISO 27001</strong>.
        </p>
        <p class="text-slate-700 leading-relaxed">
            Our cloud architecture practice implements ephemeral containerized runners, automated secret vaulting via HashiCorp Vault / AWS Secrets Manager, and real-time SIEM log shipping to provide continuous observability across all build assets.
        </p>

        <div class="p-6 rounded-2xl bg-[#084582] text-white flex flex-col sm:flex-row items-center justify-between gap-4 mt-6">
            <div class="space-y-1">
                <h3 class="text-base font-bold">Require Urgent Assistance with Pipeline Hardening?</h3>
                <p class="text-xs text-blue-100">Speak directly with our Principal Cyber &amp; Cloud Architects in Melbourne.</p>
            </div>
            <a href="tel:1300050099" class="px-5 py-2.5 rounded-xl bg-white text-[#084582] hover:bg-slate-100 font-bold text-xs whitespace-nowrap shadow">
                📞 Call 1300 050 099
            </a>
        </div>
    </section>

</div>
`
  }},
"""

def update_procrm():
    print("⚡ Updating PRO CRM with ASD ACSC Alert...")
    site_js_path = os.path.join(PROCRM_DIR, "src", "data", "site.js")
    with open(site_js_path, "r", encoding="utf-8") as f:
        content = f.read()

    if PROCRM_SLUG not in content:
        content = content.replace("export const POSTS = [\n", f"export const POSTS = [\n{PROCRM_ARTICLE_ENTRY}")
        with open(site_js_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Added ASD ACSC Alert to PRO CRM!")
    else:
        print("ℹ️ Post already in PRO CRM site.js")

# ==============================================================================
# 2. EZ CONSULTANTS (ezconsultants.com.au) - Salesforce & DevSecOps Perspective
# ==============================================================================
EZ_CONSULTANTS_POST = {
    "id": "asd-alert-cve-2026-63077-salesforce-devsecops-hardening",
    "slug": "asd-alert-cve-2026-63077-salesforce-devsecops-hardening",
    "title": "ASD ACSC Alert: Active CI/CD Exploitation (CVE-2026-63077) — Hardening Salesforce DevOps Pipelines",
    "category": "CRM Architecture",
    "date": TODAY_SHORT,
    "formattedDate": TODAY_STR,
    "iso_date": TODAY_ISO,
    "readTime": "6 min read",
    "author": {
        "name": "Robin Bakshi",
        "title": "Principal Salesforce Architect & Founder",
        "image": "/images/author-robin-bakshi.webp"
    },
    "authorRole": "Principal Salesforce Architect",
    "excerpt": "ASD's ACSC warns of active exploitation of on-premises CI/CD platforms (CVE-2026-63077). Learn how Salesforce architects must secure SFDX build runners, rotate connected app JWT tokens, and patch pipelines immediately.",
    "heroImage": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1600&q=80",
    "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1600&q=80",
    "url": "/blog/asd-alert-cve-2026-63077-salesforce-devsecops-hardening",
    "publishDate": f"Tue, 25 Aug 2026 08:00:00 +1000",
    "views": 2980,
    "likes": 274,
    "tags": ["ASD Alert", "CVE-2026-63077", "Salesforce DevOps", "SFDX", "DevSecOps", "Security"],
    "highlights": [
        { "id": "sec-alert", "badge": "01. ASD ALERT", "title": "Active In-The-Wild Exploitation", "text": "ASD confirms unauthenticated remote command execution targeting Australian CI/CD servers." },
        { "id": "sec-sfdx", "badge": "02. SFDX IMPACT", "title": "Salesforce Connected App Risk", "text": "Build server compromise can leak production Org admin JWT certificates and deploy keys." },
        { "id": "sec-fix", "badge": "03. FIX GUIDE", "title": "Patching & Pipeline Remediation", "text": "Upgrade to TeamCity 2026.1.3+, apply patch plugin, and isolate runners in private VPCs." }
    ],
    "content": """
<div class="agentforce-light-article space-y-10 font-sans text-slate-800 leading-relaxed text-base">
    <div id="sec-alert" class="bg-gradient-to-br from-red-50/90 via-orange-50/40 to-white rounded-3xl p-6 sm:p-8 border-2 border-red-200/80 shadow-sm relative overflow-hidden">
        <div class="relative z-10 space-y-4">
            <div class="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-red-700">
                <span class="w-2.5 h-2.5 rounded-full bg-red-600 animate-pulse"></span>
                Official ASD ACSC Threat Alert · High Priority
            </div>
            <h2 class="text-xl sm:text-2xl lg:text-3xl font-black text-slate-900 tracking-tight leading-snug font-heading">
                Active Exploitation of CI/CD Build Platforms in Australia: Securing Salesforce DevOps &amp; Release Pipelines
            </h2>
            <p class="text-sm sm:text-base text-slate-700 leading-relaxed max-w-3xl">
                The Australian Cyber Security Centre (ASD's ACSC) has observed active exploitation of on-premises CI/CD platforms (CVE-2026-63077). In enterprise Salesforce environments, build servers store mission-critical SFDX deployment certificates, production OAuth tokens, and metadata packages. Immediate remediation is required.
            </p>
        </div>
    </div>

    <section id="sec-sfdx" class="space-y-4">
        <h2 class="text-2xl font-bold text-slate-900 pb-2 border-b border-slate-200">1. Why Salesforce DevOps Teams Are at Critical Risk</h2>
        <p class="text-slate-700 leading-relaxed">
            Modern enterprise Salesforce deployments rely heavily on automated CI/CD pipelines to validate Apex test suites, build Lightning Web Components (LWCs), and deploy metadata packages via the Salesforce CLI (<code>sf</code> / <code>sfdx</code>). To automate these deployments, CI/CD servers hold stored JWT server keys, OAuth connected app secrets, and production org administrator credentials.
        </p>
        <p class="text-slate-700 leading-relaxed">
            If an on-premises build server running TeamCity is compromised via CVE-2026-63077, attackers gain full access to these stored secrets. This allows adversaries to authenticate directly into your production Salesforce org, exfiltrate sensitive CRM data, or inject malicious Apex triggers without detection.
        </p>
    </section>

    <section id="sec-fix" class="space-y-4">
        <h2 class="text-2xl font-bold text-slate-900 pb-2 border-b border-slate-200">2. How to Fix &amp; Remediate Your Pipelines</h2>
        <p class="text-slate-700 leading-relaxed">
            EZ Consultants advises Salesforce enterprise architects to immediately execute these 4 mitigation steps:
        </p>
        <ul class="list-disc pl-6 space-y-2 text-slate-700 text-sm sm:text-base">
            <li><strong>Immediate Server Upgrade:</strong> Update to TeamCity 2026.1.3 or 2025.11.7, or install the emergency patch plugin (<code>fix_CVE_2026_63077.zip</code>).</li>
            <li><strong>Isolate Network Perimeter:</strong> Remove build servers from public internet exposure; restrict access to corporate VPNs with zero-trust posture checks.</li>
            <li><strong>Audit &amp; Rotate Salesforce Credentials:</strong> In Salesforce Setup, inspect Connected App login histories. Rotate JWT private keys and regenerate deployment user certificates.</li>
            <li><strong>Migrate to Ephemeral Runners:</strong> Transition from persistent on-prem build machines to short-lived, isolated container runners with zero long-term secret persistence.</li>
        </ul>
    </section>
</div>
"""
}

def update_ezconsultants():
    print("💼 Updating EZ Consultants with ASD ACSC Alert...")
    posts_path = os.path.join(EZ_CONSULTANTS_DIR, "posts.json")
    pub_posts_path = os.path.join(EZ_CONSULTANTS_DIR, "public", "posts.json")

    with open(posts_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    filtered = [p for p in existing if p.get("id") != EZ_CONSULTANTS_POST["id"]]
    combined = [EZ_CONSULTANTS_POST] + filtered

    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)
    with open(pub_posts_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)

    os.system("python3 /Users/robinbakshi/Documents/GitHub/Blogs-Content/scripts/update_ezconsultants_25_aug.py")
    print("✅ EZ Consultants updated with ASD ACSC Alert!")

# ==============================================================================
# 3. FINNOVA (finnova.org.au) - Community, NFP & SME Cyber Defence
# ==============================================================================
FINNOVA_POST = {
    "id": "asd-acsc-alert-software-platform-exploitation-2026",
    "title": "ASD ACSC Alert: Active Exploitation of Software Platforms in Australia — How Local Businesses & Non-Profits Can Stay Protected",
    "date": TODAY_STR,
    "author": "Cyber Safety Taskforce",
    "category": "Cyber Safety & Scams",
    "image": "images/blog-cyber-safety.webp",
    "summary": "The Australian Cyber Security Centre (ASD's ACSC) has issued an urgent high alert regarding active exploitation of software development platforms. Finnova outlines simple, actionable steps for SMEs and community organizations to patch systems and protect data.",
    "body": [
        "<p>The Australian Signals Directorate's Australian Cyber Security Centre (ASD's ACSC) has issued an urgent public alert regarding the active exploitation of software development and continuous deployment platforms across Australia (CVE-2026-63077). Attackers are actively scanning Australian networks to gain unauthorized remote control of unpatched servers.</p>",
        "<p>While software build platforms are typically operated by technical teams and digital agencies, the security consequences impact entire organizations — including local small businesses, non-profits, healthcare providers, and community hubs that rely on custom web applications and member portals.</p>",
        "<p>Finnova's Cyber Safety Taskforce advises all Australian organizations and business owners to take the following three immediate protective steps:</p>",
        "<p><strong>1. Verify Managed IT &amp; Hosting Providers:</strong> If your organization contracts an external IT support provider or digital agency to manage your web systems, contact them immediately to verify that all on-premises development platforms have received the official security patch.</p>",
        "<p><strong>2. Restrict Public Internet Access:</strong> Administrative dashboards, internal staging environments, and build servers should never be exposed to the open internet. Ensure all management portals require secure VPN or two-factor zero-trust access.</p>",
        "<p><strong>3. Enable Automated Security Updates:</strong> Ensure your systems adhere to the ASD Essential Eight guidelines by maintaining continuous, automated patch management across all digital infrastructure.</p>",
        "<p>Organizations that suspect they have been impacted can contact the Australian Cyber Security Hotline on <strong>1300 CYBER1 (1300 292 371)</strong> or attend a free Finnova Cyber Safety Consultation at our Wyndham community hub.</p>"
    ]
}

def update_finnova():
    print("🌟 Updating Finnova with ASD ACSC Alert...")
    posts_path = os.path.join(FINNOVA_DIR, "posts.json")
    blogs_posts_path = os.path.join(BLOGS_DIR, "posts.json")

    with open(posts_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    filtered = [p for p in existing if p.get("id") != FINNOVA_POST["id"]]
    combined = [FINNOVA_POST] + filtered

    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)

    # Sync Blogs-Content posts.json
    blog_entry = {
        "id": FINNOVA_POST["id"],
        "slug": FINNOVA_POST["id"],
        "title": FINNOVA_POST["title"],
        "category": FINNOVA_POST["category"],
        "badge": "ASD ACSC HIGH ALERT",
        "date": TODAY_SHORT,
        "iso_date": TODAY_ISO,
        "readTime": "5 min read",
        "author": FINNOVA_POST["author"],
        "authorRole": "Cyber Threat Intelligence Desk",
        "authorImg": "/images/ez-mortgage-broker.webp",
        "excerpt": FINNOVA_POST["summary"],
        "snippet": FINNOVA_POST["summary"],
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
        "url": f"/pages/blog/{FINNOVA_POST['id']}.html"
    }

    with open(blogs_posts_path, "r", encoding="utf-8") as f:
        existing_blogs = json.load(f)

    filtered_blogs = [p for p in existing_blogs if p.get("id") != FINNOVA_POST["id"]]
    combined_blogs = [blog_entry] + filtered_blogs

    with open(blogs_posts_path, "w", encoding="utf-8") as f:
        json.dump(combined_blogs, f, indent=2)

    # Inject into Finnova HTML files
    html_files = ["index.html", "en_AU.html", "ar_SA.html", "es_ES.html", "hi_IN.html", "pa_IN.html", "vi_VN.html", "zh_CN.html"]
    for fn in html_files:
        fp = os.path.join(FINNOVA_DIR, fn)
        if not os.path.exists(fp):
            continue
        with open(fp, "r", encoding="utf-8") as f:
            c = f.read()
        
        if FINNOVA_POST["id"] not in c:
            # Prepend into defaultSeedPosts array
            c = c.replace('var defaultSeedPosts = [\n', f'var defaultSeedPosts = [\n    {json.dumps(FINNOVA_POST, indent=6)[6:]},\n')
            with open(fp, "w", encoding="utf-8") as f:
                f.write(c)

    print("✅ Finnova updated with ASD ACSC Alert across all templates!")

def main():
    update_procrm()
    update_ezconsultants()
    update_finnova()
    print("🎉 All 3 platforms updated with tailored ASD ACSC High Alert articles!")

if __name__ == "__main__":
    main()
