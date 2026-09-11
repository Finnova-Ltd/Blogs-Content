import os
import ast
import re
import pytest

# Target scripts to strictly audit for syntax, f-string braces, and timezone localization
TARGET_SCRIPTS = [
    "scripts/fetch_google_alerts.py",
    "scripts/ingest_authority_sources.py",
    "scripts/generate_rss_feed.py",
    "scripts/ingest_salesforce_news.py"
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
        # If an f-string block defines CSS, look for unescaped patterns like "0% {" or "100% {"
        # Real escaped CSS in Python f-strings must use "0% {{"
        bad_css_braces = re.findall(r"(?:\d+%\s*\{[^\{])", content)
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

    canned_signature = "The Reserve Bank of Australia and major retail banks have updated residential mortgage assessment benchmarks"
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

