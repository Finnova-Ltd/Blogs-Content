import os
import sys
import ast
import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Target scripts to strictly audit for syntax, f-string braces, and timezone localization
TARGET_SCRIPTS = [
    "scripts/fetch_google_alerts.py",
    "scripts/ingest_authority_sources.py",
    "scripts/generate_rss_feed.py",
    "scripts/ingest_salesforce_news.py",
    "scripts/semgrep_runner.py",
    "scripts/agentic_generator_sandbox.py"
]

@pytest.mark.parametrize("script_path", TARGET_SCRIPTS)
def test_python_syntax_and_escaped_braces(script_path):
    """
    Ensures the script is syntactically valid and checks for raw, unescaped
    curly braces within CSS blocks inside f-strings.
    """
    if not os.path.exists(script_path):
        pytest.skip(f"Script {script_path} not found in this repository.")

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Compile check (catches base syntax errors immediately)
    try:
        ast.parse(content, filename=script_path)
    except SyntaxError as e:
        pytest.fail(f"Syntax error detected in {script_path}: {e}")

    # 2. Strict check for @keyframes or raw CSS blocks inside f-strings missing double braces
    if "@keyframes" in content:
        # Real escaped CSS in Python f-strings must use "0% {{"
        bad_css_braces = re.findall(r"(?:\d+%\s*\{[^{])", content)
        assert not bad_css_braces, (
            f"Potential unescaped CSS curly brace found in {script_path}: {bad_css_braces}. "
            f"Ensure loops like @keyframes use double braces \"{{ }}\"."
        )

@pytest.mark.parametrize("script_path", TARGET_SCRIPTS)
def test_timezone_localization_enforcement(script_path):
    """
    Scans scripts to ensure native, timezone-naive datetime.now() calls
    aren't used, avoiding GitHub Actions UTC vs AEST errors.
    """
    if not os.path.exists(script_path):
        pytest.skip(f"Script {script_path} not found in this repository.")

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Disallow naive datetime.now() without explicit tz/timedelta offsets
    if "datetime.now()" in content:
        # Check if localized timezone is imported or used
        has_tz = ("timezone(" in content or "ZoneInfo" in content or "timedelta(hours=10)" in content or "timedelta(hours=11)" in content)
        assert has_tz, (
            f"CRITICAL: Naive datetime.now() call found in {script_path}. "
            f"GitHub Actions runs on UTC. You must localize it to Australian Time (AEST/AEDT UTC+10)."
        )

@pytest.mark.parametrize("script_path", TARGET_SCRIPTS)
def test_semgrep_security_and_governance_rules(script_path):
    """
    Executes AST-based Semgrep security rules (.semgrep.yml) against all production
    and generation scripts, ensuring zero secret leaks and no prohibited calls.
    """
    from pathlib import Path
    from scripts.semgrep_runner import scan_file_ast

    file_p = Path(script_path)
    if not file_p.exists():
        pytest.skip(f"Script {script_path} not found.")

    violations = scan_file_ast(file_p)
    assert not violations, f"Semgrep security rule violations in {script_path}: {violations}"

def test_anti_ai_slop_and_canned_template_guard():
    """
    S-CTS Anti-Cluster & Spam Update Gatekeeper:
    Ensures no canned boilerplate templates, mass-generated thin stubs,
    or raw timestamped slugs exist in posts.json.
    """
    import json
    posts_path = "posts.json"
    if not os.path.exists(posts_path):
        pytest.skip("posts.json not found.")

    with open(posts_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    canned_signature = "The Reserve Bank of Australia" + " and major retail banks have updated residential mortgage assessment benchmarks"
    timestamp_regex = re.compile(r"-\d{9,12}$")

    for p in posts:
        slug = p.get("slug") or p.get("id") or ""
        title = p.get("title") or ""
        body_text = " ".join(p.get("body", [])) if isinstance(p.get("body"), list) else p.get("body", "")

        # 1. No canned boilerplate signature allowed
        assert canned_signature not in body_text, f"Canned template signature found in post {slug}"

        # 2. No raw epoch timestamped slugs
        assert not timestamp_regex.search(slug), f"Raw timestamped slug found in post {slug}"

        # 3. Must have valid title and category
        assert title.strip(), f"Post {slug} has an empty title"
        assert p.get("category"), f"Post {slug} is missing a category"

def test_agentic_generator_sandbox_gatekeeper():
    """
    Verifies that the Agentic Generator Sandbox properly admits safe code/HTML
    and blocks adversarial prompt injections or malicious system payloads.
    """
    from scripts.agentic_generator_sandbox import validate_agent_python_code, validate_agent_html_article

    # 1. Safe code test
    safe_code = "def get_margin(rate, base=0.035):\n    return max(0.0, rate - base)\n"
    valid, errs = validate_agent_python_code(safe_code)
    assert valid, f"Safe code was falsely rejected: {errs}"

    # 2. Malicious payload rejection test
    malicious_code = "import socket\nimport os\nos.system('rm -rf /')\neval('bad()')\n"
    valid_bad, errs_bad = validate_agent_python_code(malicious_code)
    assert not valid_bad, "Adversarial payload was not blocked by sandbox!"
    assert any("os.system" in e for e in errs_bad)
    assert any("socket" in e for e in errs_bad)

    # 3. Thin HTML article rejection test
    thin_html = "<article><h1>Too thin</h1><p>Only five words.</p></article>"
    valid_html, html_errs = validate_agent_html_article(thin_html, min_words=200)
    assert not valid_html, "Thin HTML stub was not blocked by sandbox!"

