#!/usr/bin/env python3
"""
Updated Enhancer Script for Salesforce Article & Components based on User Feedback:
1. Card 1 in Col 2 (Joe Williams Profile Card) with background image (/images/melbourne-bourke-street-header.webp).
2. Card 2 in Col 2 (Highlights with Red #990000 header & navigational subheadings).
3. Card 3 in Col 2 (Move Consultation Card to Col 2 as annotated in red).
4. Code Block: 2 Tabs (basic.html | basic.js | InvoiceServiceTest.cls), in 1 SINGLE top row with tabs on left and theme toggle & copy button on right.
5. Center-aligned architecture diagram on deep black background with emerald green text.
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

def highlight_js(code: str) -> str:
    lines = code.split("\n")
    out = []
    for i, line in enumerate(lines, 1):
        l = line
        l = l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if "//" in l:
            parts = l.split("//", 1)
            code_part = parts[0]
            comment_part = f'<span style="color:#8B949E; font-style:italic;">//{parts[1]}</span>'
        else:
            code_part = l
            comment_part = ""
        
        kw = ["import", "export", "default", "class", "extends", "get", "if", "else", "return", "this", "const", "let", "var", "function", "new"]
        for k in kw:
            code_part = re.sub(r'\b(' + k + r')\b', r'<span style="color:#FF7B72; font-weight:bold;">\1</span>', code_part)
        
        types = ["LightningElement", "DemoComponent"]
        for t in types:
            code_part = re.sub(r'\b(' + t + r')\b', r'<span style="color:#FFA657; font-weight:bold;">\1</span>', code_part)
        
        funcs = ["updateProgress", "resetProgress", "disconnectedCallback", "toggleProgress", "clearInterval", "setInterval", "bind"]
        for f in funcs:
            code_part = re.sub(r'\b(' + f + r')(?=\()', r'<span style="color:#D2A8FF;">\1</span>', code_part)
            
        code_part = re.sub(r'(".*?")', r'<span style="color:#A5D6FF;">\1</span>', code_part)
        code_part = re.sub(r'\b(\d+)\b', r'<span style="color:#79C0FF;">\1</span>', code_part)
        
        l_final = code_part + comment_part
        out.append(f'<span class="line-number" style="color:#64748B; user-select:none; margin-right:16px; display:inline-block; width:22px; text-align:right;">{i}</span>{l_final}')
    return "\n".join(out)

def highlight_apex(code: str) -> str:
    lines = code.split("\n")
    out = []
    for i, line in enumerate(lines, 1):
        l = line
        l = l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if "//" in l:
            parts = l.split("//", 1)
            code_part = parts[0]
            comment_part = f'<span style="color:#8B949E; font-style:italic;">//{parts[1]}</span>'
        else:
            code_part = l
            comment_part = ""
            
        code_part = re.sub(r'(@\w+)', r'<span style="color:#FFA657; font-weight:bold;">\1</span>', code_part)
        kw = ["private", "public", "class", "static", "void", "new", "return", "with sharing", "without sharing"]
        for k in kw:
            code_part = re.sub(r'\b(' + k + r')\b', r'<span style="color:#FF7B72; font-weight:bold;">\1</span>', code_part)
            
        types = ["Account", "Set", "Id", "List", "fflib_ApexMocks", "IAccountsSelector", "fflib_IDGenerator", "Application", "Test", "InvoiceService"]
        for t in types:
            code_part = re.sub(r'\b(' + t + r')\b', r'<span style="color:#79C0FF; font-weight:bold;">\1</span>', code_part)
            
        code_part = re.sub(r"('.*?')", r'<span style="color:#A5D6FF;">\1</span>', code_part)
        code_part = re.sub(r'\b(\d+)\b', r'<span style="color:#79C0FF;">\1</span>', code_part)
        
        l_final = code_part + comment_part
        out.append(f'<span class="line-number" style="color:#64748B; user-select:none; margin-right:16px; display:inline-block; width:22px; text-align:right;">{i}</span>{l_final}')
    return "\n".join(out)

# Clean 1-Row Tabbed Code Box for Section 2 (basic.html | basic.js | InvoiceServiceTest.cls)
def generate_tabbed_code_box():
    html_raw = """<template>
  <div class="slds-p-bottom_medium">
    <lightning-button label={computedLabel} onclick={toggleProgress}>
    </lightning-button>
  </div>
  <lightning-progress-bar value={progress} size="large">
  </lightning-progress-bar>
</template>"""

    js_raw = """import { LightningElement } from "lwc";

export default class DemoComponent extends LightningElement {
  progress = 50;
  isProgressing = false;

  updateProgress() {
    this.progress = this.progress === 100 ? this.resetProgress() : this.progress + 10;
  }

  resetProgress() {
    this.progress = 0;
    clearInterval(this._interval);
  }

  disconnectedCallback() {
    clearInterval(this._interval);
  }

  get computedLabel() {
    return this.isProgressing ? "Stop" : "Start";
  }

  toggleProgress() {
    if (this.isProgressing) {
      this.isProgressing = false;
      clearInterval(this._interval);
    } else {
      this.isProgressing = true;
      this._interval = setInterval(this.updateProgress.bind(this), 200);
    }
  }
}"""

    apex_raw = """@IsTest
private class InvoiceServiceTest {
    @IsTest
    static void calculateTax_givenCommercialAccount_appliesDiscount() {
        // Given: Instantiate enterprise mock container
        fflib_ApexMocks mocks = new fflib_ApexMocks();
        IAccountsSelector mockSelector = (IAccountsSelector) mocks.mock(IAccountsSelector.class);
        
        Account testAcc = new Account(
            Id = fflib_IDGenerator.generate(Account.SObjectType),
            Tier__c = 'Enterprise'
        );
        
        mocks.startStubbing();
        mocks.when(mockSelector.sObjectType()).thenReturn(Account.SObjectType);
        mocks.when(mockSelector.selectByIdWithContracts(new Set<Id>{ testAcc.Id }))
             .thenReturn(new List<Account>{ testAcc });
        mocks.stopStubbing();
        
        Application.Selector.setMock(mockSelector);

        // When: Execute service orchestration
        Test.startTest();
        InvoiceService.processInvoices(new Set<Id>{ testAcc.Id });
        Test.stopTest();

        // Then: Verify mock interactions & DML integrity
        ((IAccountsSelector) mocks.verify(mockSelector, 1))
            .selectByIdWithContracts(new Set<Id>{ testAcc.Id });
    }
}"""

    return f"""
<div class="code-box-wrapper bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm my-6 font-sans">
  
  <!-- 1-Row Top Header: Tabs on Left, Theme & Copy on Right -->
  <div class="bg-slate-100 border-b border-slate-200 px-4 pt-1 flex items-center justify-between flex-wrap gap-2">
    <!-- Left: Tabs (basic.html | basic.js | InvoiceServiceTest.cls) -->
    <div class="flex items-center gap-1">
      <button type="button" class="subtab-btn active-subtab px-3.5 py-2.5 text-xs font-extrabold border-b-2 border-[#0077c8] text-[#0077c8] cursor-pointer" data-subtarget="tab-sec2-html" onclick="window.switchSubTab(event, 'tab-sec2-html')">
        basic.html
      </button>
      <button type="button" class="subtab-btn px-3.5 py-2.5 text-xs font-bold text-slate-600 hover:text-slate-900 cursor-pointer" data-subtarget="tab-sec2-js" onclick="window.switchSubTab(event, 'tab-sec2-js')">
        basic.js
      </button>
      <button type="button" class="subtab-btn px-3.5 py-2.5 text-xs font-bold text-slate-600 hover:text-slate-900 cursor-pointer" data-subtarget="tab-sec2-apex" onclick="window.switchSubTab(event, 'tab-sec2-apex')">
        InvoiceServiceTest.cls
      </button>
    </div>

    <!-- Right: Theme Switcher & Copy Button (Same 1 Row) -->
    <div class="flex items-center gap-2 py-1.5">
      <button type="button" onclick="window.toggleCodeTheme(event)" class="code-theme-toggle p-1.5 rounded-md hover:bg-slate-200 text-slate-700 text-xs flex items-center gap-1 font-semibold cursor-pointer" title="Toggle Light/Dark Theme">
        <span class="theme-icon">🌙</span> <span class="text-[11px] hidden sm:inline">Theme</span>
      </button>
      <button type="button" onclick="window.copyActiveCode(event)" class="code-copy-btn px-2.5 py-1.5 rounded-md bg-[#0077c8] hover:bg-[#005a9c] text-white text-xs flex items-center gap-1 font-bold shadow-xs transition cursor-pointer" title="Copy to Clipboard">
        <span>📋</span> <span class="copy-label text-[11px]">Copy</span>
      </button>
    </div>
  </div>

  <!-- Multi-Color Syntax Highlighting Viewport -->
  <div class="code-viewport bg-[#071324] text-slate-100 p-5 font-mono text-xs overflow-x-auto leading-relaxed">
    
    <div id="tab-sec2-html" class="subtab-pane">
      <pre><code class="language-html">{highlight_html(html_raw)}</code></pre>
    </div>

    <div id="tab-sec2-js" class="subtab-pane hidden">
      <pre><code class="language-javascript">{highlight_js(js_raw)}</code></pre>
    </div>

    <div id="tab-sec2-apex" class="subtab-pane hidden">
      <pre><code class="language-apex">{highlight_apex(apex_raw)}</code></pre>
    </div>

  </div>

</div>
"""

# Clean 1-Row Single Code Box for Section 1 (mcp-config.json)
def generate_mcp_config_box():
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
<div class="code-box-wrapper bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm my-6 font-sans">
  
  <!-- 1-Row Top Header: Tab on Left, Theme & Copy on Right -->
  <div class="bg-slate-100 border-b border-slate-200 px-4 pt-1 flex items-center justify-between flex-wrap gap-2">
    <div class="flex items-center gap-1">
      <span class="px-3.5 py-2.5 text-xs font-extrabold border-b-2 border-[#0077c8] text-[#0077c8] flex items-center gap-1.5">
        <span class="text-[#0077c8] font-mono">&lt;&gt;</span>
        <span>mcp-config.json</span>
      </span>
    </div>
    <div class="flex items-center gap-2 py-1.5">
      <button type="button" onclick="window.toggleCodeTheme(event)" class="code-theme-toggle p-1.5 rounded-md hover:bg-slate-200 text-slate-700 text-xs flex items-center gap-1 font-semibold cursor-pointer" title="Toggle Light/Dark Theme">
        <span class="theme-icon">🌙</span> <span class="text-[11px] hidden sm:inline">Theme</span>
      </button>
      <button type="button" onclick="window.copyActiveCode(event)" class="code-copy-btn px-2.5 py-1.5 rounded-md bg-[#0077c8] hover:bg-[#005a9c] text-white text-xs flex items-center gap-1 font-bold shadow-xs transition cursor-pointer" title="Copy to Clipboard">
        <span>📋</span> <span class="copy-label text-[11px]">Copy</span>
      </button>
    </div>
  </div>

  <div class="code-viewport bg-[#071324] text-slate-100 p-5 font-mono text-xs overflow-x-auto leading-relaxed">
    <pre><code class="language-json">{highlight_json(json_raw)}</code></pre>
  </div>
</div>
"""

def generate_centered_architecture_diagram():
    return """
<div class="ascii-diagram-container" style="background:#06111C; border:1px solid #1e293b; border-radius:14px; padding:24px; margin:28px 0; display:flex; justify-content:center; text-align:center; overflow-x:auto;">
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
<div class="ascii-diagram-container" style="background:#06111C; border:1px solid #1e293b; border-radius:14px; padding:24px; margin:28px 0; display:flex; justify-content:center; text-align:center; overflow-x:auto;">
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
    
    mcp_box = generate_mcp_config_box()
    tabbed_code = generate_tabbed_code_box()
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
