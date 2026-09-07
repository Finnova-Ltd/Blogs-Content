#!/usr/bin/env python3
"""
Updated Enhancer Script for Salesforce Article & Components based on User Feedback:
1. Tabs should be HTML and JSON.
2. Theme toggle (Light/Dark) and Copy button must be in 1 SINGLE top row (flex-nowrap).
3. Code block background defaults to dark (#071324).
4. Full syntax highlighting across HTML and JSON.
"""

import os
import re
import sys
from pathlib import Path

EZ_DIR = Path("/Volumes/Samsung SSD 2TB/03. Documents/GitHub/ezconsultants.com.au")
BLOG_POSTS_JS = EZ_DIR / "src" / "data" / "blogPosts.js"
BLOG_ARTICLE_JSX = EZ_DIR / "src" / "pages" / "BlogArticle.jsx"
STATIC_BLOG_DIR = EZ_DIR / "pages" / "blog"
PUBLIC_BLOG_DIR = EZ_DIR / "public" / "pages" / "blog"
DIST_BLOG_DIR = EZ_DIR / "dist" / "pages" / "blog"

def highlight_json(code: str) -> str:
    lines = code.split("\n")
    out = []
    for i, line in enumerate(lines, 1):
        l = line
        l = l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        l = re.sub(r'("[\w\-]+")\s*:', r'<span style="color:#79C0FF; font-weight:bold;">\1</span>:', l)
        l = re.sub(r':\s*(".*?")', r': <span style="color:#7EE787;">\1</span>', l)
        l = re.sub(r'(\[|\,)\s*(".*?")', r'\1 <span style="color:#7EE787;">\2</span>', l)
        l = re.sub(r'\b(\d+(\.\d+)?)\b', r'<span style="color:#FFA657;">\1</span>', l)
        l = re.sub(r'\b(true|false|null)\b', r'<span style="color:#FF7B72; font-weight:bold;">\1</span>', l)
        out.append(f'<span class="line-number" style="color:#64748B; user-select:none; margin-right:16px; display:inline-block; width:22px; text-align:right;">{i}</span>{l}')
    return "\n".join(out)

def highlight_html(code: str) -> str:
    lines = code.split("\n")
    out = []
    for i, line in enumerate(lines, 1):
        l = line
        l = l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        l = re.sub(r'(&lt;/?)([\w\-]+)', r'\1<span style="color:#FF7B72; font-weight:bold;">\2</span>', l)
        l = re.sub(r'(/&gt;|&gt;)', r'<span style="color:#FF7B72; font-weight:bold;">\1</span>', l)
        l = re.sub(r'\b([\w\-]+)=', r'<span style="color:#79C0FF;">\1</span>=', l)
        l = re.sub(r'(".*?")', r'<span style="color:#A5D6FF;">\1</span>', l)
        l = re.sub(r'(\{[^}]+\})', r'<span style="color:#FFA657; font-weight:bold;">\1</span>', l)
        out.append(f'<span class="line-number" style="color:#64748B; user-select:none; margin-right:16px; display:inline-block; width:22px; text-align:right;">{i}</span>{l}')
    return "\n".join(out)

# 1-Row Code Box with HTML & JSON Tabs + Dark/Light Toggle + Copy on 1 single row
def generate_mcp_config_box(box_id="mcp-box"):
    html_raw = """<template>
  <lightning-card title="Salesforce MCP Runtime" icon-name="standard:bot">
    <div class="slds-p-around_medium">
      <div class="slds-badge slds-theme_success">
        Connected: tooling-api-v63
      </div>
      <p class="slds-m-top_small">
        Model Context Protocol Server active on stdio endpoint.
      </p>
    </div>
  </lightning-card>
</template>"""

    json_raw = """{
  "mcpServers": {
    "salesforce-tooling": {
      "command": "node",
      "args": ["/opt/mcp/salesforce-server.js"],
      "env": {
        "SF_TARGET_ORG": "scratch-feature-branch",
        "SF_API_VERSION": "63.0"
      }
    }
  }
}"""

    return f"""
<div class="code-box-wrapper" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; overflow:hidden; box-shadow:0 4px 14px rgba(10,37,64,0.06); margin:24px 0; font-family:'Plus Jakarta Sans', sans-serif;">
  
  <!-- 1-Row Top Header: Tabs on Left, Theme & Copy on Right (Strictly 1 Row, flex-nowrap) -->
  <div class="code-box-header" style="background:#f1f5f9; border-bottom:1px solid #e2e8f0; padding:6px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:nowrap; gap:8px;">
    
    <!-- Left: Tabs (HTML | JSON) -->
    <div style="display:flex; align-items:center; gap:6px; flex-shrink:1; overflow-x:auto;">
      <button type="button" class="subtab-btn active-subtab" data-subtarget="{box_id}-json" onclick="window.switchSubTab(event, '{box_id}-json')" style="padding:6px 12px; font-size:12px; font-weight:800; border:none; background:transparent; border-bottom:2px solid #0077c8; color:#0077c8; cursor:pointer; display:flex; align-items:center; gap:5px; white-space:nowrap;">
        <span style="font-family:'JetBrains Mono', monospace; font-size:11px;">&#123;&#125;</span>
        <span>JSON</span>
      </button>
      <button type="button" class="subtab-btn" data-subtarget="{box_id}-html" onclick="window.switchSubTab(event, '{box_id}-html')" style="padding:6px 12px; font-size:12px; font-weight:700; border:none; background:transparent; border-bottom:2px solid transparent; color:#64748b; cursor:pointer; display:flex; align-items:center; gap:5px; white-space:nowrap;">
        <span style="font-family:'JetBrains Mono', monospace; font-size:11px;">&lt;&gt;</span>
        <span>HTML</span>
      </button>
    </div>

    <!-- Right: Theme Switcher & Copy Button (Same 1 Row) -->
    <div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
      <button type="button" onclick="window.toggleCodeTheme(event)" class="code-theme-toggle" title="Toggle Light/Dark Theme" style="padding:6px 10px; border-radius:6px; border:1px solid #cbd5e1; background:#ffffff; color:#334155; font-size:11px; font-weight:700; display:flex; align-items:center; gap:4px; cursor:pointer; white-space:nowrap;">
        <span class="theme-icon">🌙</span> <span class="theme-label" style="font-size:11px;">Dark</span>
      </button>
      <button type="button" onclick="window.copyActiveCode(event)" class="code-copy-btn" title="Copy to Clipboard" style="padding:6px 12px; border-radius:6px; border:none; background:#0077c8; color:#ffffff; font-size:11px; font-weight:800; display:flex; align-items:center; gap:4px; cursor:pointer; white-space:nowrap; box-shadow:0 1px 3px rgba(0,119,200,0.2);">
        <span>📋</span> <span class="copy-label">Copy</span>
      </button>
    </div>
  </div>

  <!-- Multi-Color Syntax Highlighting Viewport (Default: Dark) -->
  <div class="code-viewport" style="background:#071324; color:#f8fafc; padding:18px 20px; font-family:'JetBrains Mono', monospace; font-size:12px; line-height:1.65; overflow-x:auto;">
    
    <div id="{box_id}-json" class="subtab-pane">
      <pre style="margin:0;"><code class="language-json">{highlight_json(json_raw)}</code></pre>
    </div>

    <div id="{box_id}-html" class="subtab-pane" style="display:none;">
      <pre style="margin:0;"><code class="language-html">{highlight_html(html_raw)}</code></pre>
    </div>

  </div>
</div>
"""

# Tabbed Code Box for Section 2 (HTML & JSON Tabs)
def generate_tabbed_code_box(box_id="refactor-box"):
    html_raw = """<template>
  <div class="slds-p-bottom_medium">
    <lightning-button label={computedLabel} onclick={toggleProgress}>
    </lightning-button>
  </div>
  <lightning-progress-bar value={progress} size="large">
  </lightning-progress-bar>
</template>"""

    json_raw = """{
  "refactoringTask": {
    "sourceTrigger": "ContractTrigger.trigger",
    "targetArchitecture": "fflib_ApexMocks / Domain Layer",
    "soqlGovernorLimitCheck": "PASSED (Zero queries in loops)",
    "testCoverageTarget": 0.88,
    "apraCompliance": true
  }
}"""

    return f"""
<div class="code-box-wrapper" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; overflow:hidden; box-shadow:0 4px 14px rgba(10,37,64,0.06); margin:24px 0; font-family:'Plus Jakarta Sans', sans-serif;">
  
  <!-- 1-Row Top Header: Tabs on Left, Theme & Copy on Right (Strictly 1 Row, flex-nowrap) -->
  <div class="code-box-header" style="background:#f1f5f9; border-bottom:1px solid #e2e8f0; padding:6px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:nowrap; gap:8px;">
    
    <!-- Left: Tabs (HTML | JSON) -->
    <div style="display:flex; align-items:center; gap:6px; flex-shrink:1; overflow-x:auto;">
      <button type="button" class="subtab-btn active-subtab" data-subtarget="{box_id}-html" onclick="window.switchSubTab(event, '{box_id}-html')" style="padding:6px 12px; font-size:12px; font-weight:800; border:none; background:transparent; border-bottom:2px solid #0077c8; color:#0077c8; cursor:pointer; display:flex; align-items:center; gap:5px; white-space:nowrap;">
        <span style="font-family:'JetBrains Mono', monospace; font-size:11px;">&lt;&gt;</span>
        <span>HTML</span>
      </button>
      <button type="button" class="subtab-btn" data-subtarget="{box_id}-json" onclick="window.switchSubTab(event, '{box_id}-json')" style="padding:6px 12px; font-size:12px; font-weight:700; border:none; background:transparent; border-bottom:2px solid transparent; color:#64748b; cursor:pointer; display:flex; align-items:center; gap:5px; white-space:nowrap;">
        <span style="font-family:'JetBrains Mono', monospace; font-size:11px;">&#123;&#125;</span>
        <span>JSON</span>
      </button>
    </div>

    <!-- Right: Theme Switcher & Copy Button (Same 1 Row) -->
    <div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
      <button type="button" onclick="window.toggleCodeTheme(event)" class="code-theme-toggle" title="Toggle Light/Dark Theme" style="padding:6px 10px; border-radius:6px; border:1px solid #cbd5e1; background:#ffffff; color:#334155; font-size:11px; font-weight:700; display:flex; align-items:center; gap:4px; cursor:pointer; white-space:nowrap;">
        <span class="theme-icon">🌙</span> <span class="theme-label" style="font-size:11px;">Dark</span>
      </button>
      <button type="button" onclick="window.copyActiveCode(event)" class="code-copy-btn" title="Copy to Clipboard" style="padding:6px 12px; border-radius:6px; border:none; background:#0077c8; color:#ffffff; font-size:11px; font-weight:800; display:flex; align-items:center; gap:4px; cursor:pointer; white-space:nowrap; box-shadow:0 1px 3px rgba(0,119,200,0.2);">
        <span>📋</span> <span class="copy-label">Copy</span>
      </button>
    </div>
  </div>

  <!-- Multi-Color Syntax Highlighting Viewport (Default: Dark) -->
  <div class="code-viewport" style="background:#071324; color:#f8fafc; padding:18px 20px; font-family:'JetBrains Mono', monospace; font-size:12px; line-height:1.65; overflow-x:auto;">
    
    <div id="{box_id}-html" class="subtab-pane">
      <pre style="margin:0;"><code class="language-html">{highlight_html(html_raw)}</code></pre>
    </div>

    <div id="{box_id}-json" class="subtab-pane" style="display:none;">
      <pre style="margin:0;"><code class="language-json">{highlight_json(json_raw)}</code></pre>
    </div>

  </div>
</div>
"""

def generate_centered_architecture_diagram():
    return """
<div class="ascii-diagram-container" style="background:#06111C; border:1px solid #1e293b; border-radius:14px; padding:24px; margin:28px 0; display:flex; justify-content:center; text-align:center; overflow-x:auto; max-width:100%; box-sizing:border-box;">
  <pre style="color:#10b981; font-family:'JetBrains Mono', ui-monospace, monospace; font-size:0.78rem; line-height:1.35; margin:0 auto; display:inline-block; text-align:left;">┌─────────────────────────────────────────────────────────────┐
│                      Cursor / Claude Code                   │
│         (Autonomous Agent: Plans, Reads, Edits, Shells)     │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
        Stdio / SSE                     Native Shell
               │                               │
┌──────────────▼──────────────┐ ┌──────────────▼──────────────┐
│    Salesforce MCP Server    │ │       Salesforce CLI        │
│   (Tooling API, Org Meta)   │ │  (sf project deploy, test)  │
└──────────────┬──────────────┘ └──────────────┬──────────────┘
               │                               │
               └───────────────┬───────────────┘
                               │
                Secure OAuth2 (mTLS / JWT)
                               │
               ┌───────────────▼───────────────┐
               │    Salesforce Scratch Org     │
               │   (Isolated Ephemeral Dev)    │
               └───────────────────────────────┘</pre>
</div>
"""

def generate_centered_cicd_diagram():
    return """
<div class="ascii-diagram-container" style="background:#06111C; border:1px solid #1e293b; border-radius:14px; padding:24px; margin:28px 0; display:flex; justify-content:center; text-align:center; overflow-x:auto; max-width:100%; box-sizing:border-box;">
  <pre style="color:#10b981; font-family:'JetBrains Mono', ui-monospace, monospace; font-size:0.78rem; line-height:1.35; margin:0 auto; display:inline-block; text-align:left;">  ┌────────────────────────────────────────────────────────┐
  │                 Cursor / Claude Code                   │
  └──────────────────────────┬─────────────────────────────┘
                             │
                  1. Local Test Execution
                     (sf apex run test)
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │              Git Feature Branch (Pull Request)         │
  └──────────────────────────┬─────────────────────────────┘
                             │
                  2. GitHub Actions CI Webhook
                             │
                             ▼
┌────────────────────────────────────────────────────────────┐
│                    Automated CI Pipeline                   │
│                                                            │
│  ├── A. Static Code Analysis (PMD / Code Analyzer)         │
│  │   ├── Enforce 'with sharing' keywords                   │
│  │   ├── Scan for SOQL injections & unindexed queries      │
│  │   └── Check CRUD/FLS accessibility checks               │
│  │                                                         │
│  ├── B. Scratch Org Spin-up & Seed                         │
│  │   ├── Deploy delta package via sf project deploy        │
│  │   └── Run 100% test suites (target: >85% coverage)      │
│  │                                                         │
│  └── C. Security & Data Sovereignty Audit                  │
│      ├── Verify no customer PII leaked into local logs     │
│      └── Audit API calls against APRA CPS 234 standards    │
└────────────────────────────┬───────────────────────────────┘
                             │
                 3. Automated Check Passing
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │          Technical Architect Peer Review & Merge       │
  └────────────────────────────────────────────────────────┘</pre>
</div>
"""

def update_blog_posts_js():
    print(f"Updating {BLOG_POSTS_JS}...")
    content_file = BLOG_POSTS_JS.read_text(encoding="utf-8")
    
    mcp_box = generate_mcp_config_box(box_id="sec1-code")
    tabbed_code = generate_tabbed_code_box(box_id="sec2-code")
    arch_diag = generate_centered_architecture_diagram()
    cicd_diag = generate_centered_cicd_diagram()
    
    new_article_content = f"""<div class=\\"summary-card p-6 bg-blue-50 border-l-4 border-[#0077c8] rounded-r-xl mb-8\\"><strong class=\\"text-[#0077c8] block mb-1 text-xs uppercase tracking-wider font-extrabold\\">Executive Advisory Summary</strong><p class=\\"text-slate-800 text-base leading-relaxed m-0\\">For years, enterprise Salesforce backlogs have resembled digital sediment: legacy Workflow Rules half-migrated to Flows, monolithic 2,000-line Apex triggers with zero separation of concerns, and untested batch jobs skirting SOQL limits. The combination of agentic coding IDEs (Claude Code, Cursor) and the Model Context Protocol (MCP) changes this dynamic entirely, enabling autonomous refactoring, live org schema querying, and ephemeral test deployments while strictly enforcing APRA CPS 234 and ISO 27001 data boundaries.</p></div>

<section id=\\"mcp-workspace\\">
<h2 class=\\"text-2xl font-bold text-slate-900 mb-4 border-b border-slate-200 pb-3\\">1. The Architectural Shift: The Agentic Developer Workspace</h2>
<p class=\\"mb-4\\">Traditional LLM coding assistants act as intelligent autocomplete engines: they suggest functions based on the open file. Agentic IDEs behave as autonomous engineers: they parse Abstract Syntax Trees (ASTs), execute terminal commands, crawl dependencies across your repository, and iteratively test their work.</p>

{arch_diag}

<p class=\\"mb-4\\">The catalyst bridging the IDE to the Salesforce platform is <strong>Model Context Protocol (MCP)</strong>. MCP standardizes how local development environments expose tools, resources, and contextual prompts to language models.</p>

<h3 class=\\"text-lg font-bold text-slate-900 mt-6 mb-3\\">Connecting the Org via MCP</h3>
<p class=\\"mb-3\\">Rather than pasting Apex classes and object schema definitions into chat windows, an enterprise MCP server exposes read/write platform operations directly to the agent runtime:</p>

{mcp_box}

<p class=\\"mb-3\\">Through this abstraction, the agent has native access to:</p>
<ul class=\\"list-disc pl-6 space-y-2 mb-6\\">
<li class=\\"leading-relaxed\\"><strong>get_object_metadata(sobjectApiName):</strong> Pulls picklist values, record types, and relationship schemas.</li>
<li class=\\"leading-relaxed\\"><strong>query_tooling_api(soql):</strong> Inspects SymbolTable, ApexClass, and CoverageItem.</li>
<li class=\\"leading-relaxed\\"><strong>fetch_debug_logs(userId):</strong> Ingests platform logs to triage exceptions during local test runs.</li>
</ul>
</section>

<section id=\\"fflib-refactoring\\">
<h2 class=\\"text-2xl font-bold text-slate-900 mt-10 mb-4 border-b border-slate-200 pb-3\\">2. Tackling the Debt: Concrete Remediations</h2>
<p class=\\"mb-4\\">When configured with an understanding of Salesforce architecture, the agent can systematically work down legacy backlogs.</p>

<h3 class=\\"text-lg font-bold text-slate-900 mt-6 mb-3\\">Scenario A: Refactoring Monolithic Triggers to Domain Frameworks (fflib)</h3>
<p class=\\"mb-3\\">Legacy orgs frequently house 1,500-line triggers intermixing SOQL queries, business logic, and DML operations. Below are the decoupled LWC and Apex test mocking patterns generated by the agentic toolchain:</p>

{tabbed_code}

<p class=\\"mb-3\\">Using the agentic toolchain for enterprise refactoring:</p>
<ul class=\\"list-disc pl-6 space-y-2 mb-6\\">
<li class=\\"leading-relaxed\\"><strong>Context Ingestion:</strong> The agent uses MCP to crawl the legacy trigger, its companion test classes, and all referenced SObject fields.</li>
<li class=\\"leading-relaxed\\"><strong>Structural Decomposition:</strong> The agent partitions the logic into enterprise patterns (Trigger Handler dispatch, Domain validation, Selector cached SOQL, and Service orchestration).</li>
<li class=\\"leading-relaxed\\"><strong>Execution:</strong> The agent builds new files, updates references, and verifies that no Governor Limits are introduced via nested loops.</li>
</ul>
</section>

<section id=\\"governance-cicd\\">
<h2 class=\\"text-2xl font-bold text-slate-900 mt-10 mb-4 border-b border-slate-200 pb-3\\">3. Governance, CI/CD, and Compliance (APRA CPS 234 / ISO 27001)</h2>
<p class=\\"mb-4\\">Autonomous code generation without rigorous verification risks generating hallucinations: hallucinated custom fields, bypassing object permissions (<code>with sharing</code>), or ignoring SOQL injection vectors. Deploying agent-generated code directly to persistent sandboxes is strictly prohibited. The deployment model must rely on ephemeral environments and automated static analysis.</p>

{cicd_diag}

<h3 class=\\"text-lg font-bold text-slate-900 mt-6 mb-3\\">Key Guardrails for Autonomous Delivery</h3>
<div class=\\"overflow-x-auto my-4 border border-slate-200 rounded-xl\\">
<table class=\\"w-full text-left text-sm border-collapse\\">
<thead class=\\"bg-[#0A2540] text-white\\">
<tr><th class=\\"p-3 border-b\\">Layer</th><th class=\\"p-3 border-b\\">Tool / Mechanism</th><th class=\\"p-3 border-b\\">Enforcement Standard</th></tr>
</thead>
<tbody>
<tr class=\\"border-b\\"><td class=\\"p-3 font-semibold\\">Static Analysis</td><td class=\\"p-3\\">Code Analyzer / PMD</td><td class=\\"p-3\\">Rejects code missing <code>with sharing</code>, dynamic unescaped SOQL, or hardcoded IDs.</td></tr>
<tr class=\\"border-b bg-slate-50\\"><td class=\\"p-3 font-semibold\\">Ephemeral Test Bed</td><td class=\\"p-3\\">Salesforce Scratch Orgs</td><td class=\\"p-3\\">Must prove clean deployment in pristine org isolated from shared dev environments.</td></tr>
<tr class=\\"border-b\\"><td class=\\"p-3 font-semibold\\">Coverage Floor</td><td class=\\"p-3\\">Apex Test Framework</td><td class=\\"p-3\\">Minimum 85% real branch coverage; zero tolerance for dummy assertions.</td></tr>
<tr><td class=\\"p-3 font-semibold\\">Data Protection</td><td class=\\"p-3\\">MCP Scope Restrictions</td><td class=\\"p-3\\">Prevent LLM access to production data; limit strictly to metadata endpoints for APP compliance.</td></tr>
</tbody>
</table>
</div>
</section>

<section id=\\"engineering-protocol\\">
<h2 class=\\"text-2xl font-bold text-slate-900 mt-10 mb-4 border-b border-slate-200 pb-3\\">4. The New Engineering Protocol</h2>
<p class=\\"mb-4\\">Agentic tooling does not eliminate developers; it elevates them into technical architects and code reviewers. A team of four developers operating with well-configured MCP toolchains and rigid CI/CD validation can deliver the throughput of a 20-person legacy offshore maintenance pod.</p>
<p class=\\"mb-4\\">The organizations clearing multi-year backlogs in 2026 are not writing code line-by-line. They are building the <strong>prompt contexts, MCP boundaries, and automated validation pipelines</strong> that allow autonomous agents to execute safe refactoring at scale.</p>
<div class=\\"p-4 bg-slate-100 border-l-4 border-blue-600 rounded-r-lg text-sm text-slate-800 my-6\\"><strong>💡 Enterprise Architecture Rule:</strong> Under APRA CPS 234 and Australian data sovereignty mandates, agentic tooling must be locked to metadata-only access. Production data synthesis must occur strictly within isolated scratch org sandboxes.</div>
</section>"""

    escaped_content = new_article_content.replace('`', '\\`')
    
    new_highlights = """[
      {
        "id": "mcp-workspace",
        "time": "01. MCP WORKSPACE",
        "title": "Cursor, Claude Code & Tooling API",
        "text": "Direct Tooling API connection via local stdio."
      },
      {
        "id": "fflib-refactoring",
        "time": "02. FFLIB REFACTORING",
        "title": "Apex Mocks, Triggers & Unit Tests",
        "text": "Enterprise pattern decoupling & 85%+ coverage."
      },
      {
        "id": "governance-cicd",
        "time": "03. REGULATORY CI/CD",
        "title": "APRA CPS 234 & ISO 27001 Guardrails",
        "text": "Ephemeral scratch orgs & static analysis."
      }
    ]"""

    content_file = re.sub(
        r'("id":\s*"your-three-year-salesforce-backlog-is-now-this-week-s-sprint"[\s\S]*?"highlights":\s*)\[[\s\S]*?\]',
        r'\1' + new_highlights,
        content_file
    )

    pattern = r'("id":\s*"your-three-year-salesforce-backlog-is-now-this-week-s-sprint"[\s\S]*?"content":\s*)`[\s\S]*?`(\s*[\,\}])'
    content_file = re.sub(pattern, r'\1`' + escaped_content + r'`\2', content_file)
    BLOG_POSTS_JS.write_text(content_file, encoding="utf-8")
    print("✓ blogPosts.js successfully updated.")

if __name__ == "__main__":
    update_blog_posts_js()
