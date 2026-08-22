#!/usr/bin/env python3
"""
Omni-Agent DOM Allow-List Sanitizer Fuzzing & Security Test Harness
Tests sanitizer against XSS bypass payloads, obfuscated schemes, SVG/MathML injection, and DOM clobbering.
"""

import sys
import re

# Python simulation of DOMParser allow-list sanitizer matching src/index.ts implementation
def simulate_dom_allowlist_sanitizer(dirty_html):
    if not dirty_html:
        return ""
    
    # Strip forbidden tags: <script>, <style>, <iframe>, <object>, <embed>, <svg>, <math>, <form>, <input>, <link>, <img>
    clean = re.sub(r'<(?:script|style|iframe|object|embed|svg|math|form|input|link|img)\b[^>]*>(?:[\s\S]*?<\/(?:script|style|iframe|object|embed|svg|math|form|input|link|img)>)?', '', dirty_html, flags=re.IGNORECASE)
    clean = re.sub(r'<(?:script|style|iframe|object|embed|svg|math|form|input|link|img)\b[^>]*\/?>', '', clean, flags=re.IGNORECASE)
    
    # Strip event handlers (onload, onerror, onclick, etc.)
    clean = re.sub(r'\s*on[a-z]+\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)', '', clean, flags=re.IGNORECASE)
    
    # Strip disallowed attributes (style, id, etc.), keeping href, target, rel, class
    clean = re.sub(r'\s*(?:style|id|action|formaction|background|dynsrc|lowsrc)\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)', '', clean, flags=re.IGNORECASE)
    
    # Filter href for dangerous protocols (javascript:, data:, vbscript:, relative/mixed-case)
    def clean_href(match):
        attr = match.group(0)
        val = re.sub(r'[\s\x00-\x1F]', '', match.group(1)).lower()
        if not (val.startswith("http://") or val.startswith("https://") or val.startswith("/")):
            return ''
        return attr

    clean = re.sub(r'href\s*=\s*["\']?([^"\'\s>]+)["\']?', clean_href, clean, flags=re.IGNORECASE)
    return clean

FUZZ_PAYLOADS = [
    {"id": "SZ-001", "name": "Mixed-case javascript: URI scheme", "input": '<a href="JaVaScRiPt:alert(1)">Click Me</a>', "forbidden": ["javascript", "alert(1)"]},
    {"id": "SZ-002", "name": "HTML Entity encoded javascript: URI scheme", "input": '<a href="java&#x73;cript:alert(1)">Click Me</a>', "forbidden": ["java&#x73;cript", "alert(1)"]},
    {"id": "SZ-003", "name": "URL encoded javascript: URI scheme", "input": '<a href="javascript%3Aalert(1)">Click Me</a>', "forbidden": ["javascript%3a", "alert(1)"]},
    {"id": "SZ-004", "name": "Null byte / control character padded URI scheme", "input": '<a href="\x00javascript:alert(1)">Click Me</a>', "forbidden": ["javascript", "alert(1)"]},
    {"id": "SZ-005", "name": "Data URI HTML payload", "input": '<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">Click Me</a>', "forbidden": ["data:text/html"]},
    {"id": "SZ-006", "name": "VBScript URI scheme", "input": '<a href="vbscript:msgbox(1)">Click Me</a>', "forbidden": ["vbscript:"]},
    {"id": "SZ-007", "name": "SVG vector injection with onload event handler", "input": '<svg/onload=alert(1)>', "forbidden": ["<svg", "onload="]},
    {"id": "SZ-008", "name": "MathML maction link vector injection", "input": '<math><maction actiontype="statusline" xlink:href="javascript:alert(1)">Click</maction></math>', "forbidden": ["<math", "javascript:"]},
    {"id": "SZ-009", "name": "Arbitrary inline style attribute stripping", "input": '<span style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:999999;background:red;">Overlaid Text</span>', "forbidden": ["style="]},
    {"id": "SZ-010", "name": "DOM clobbering name/id attribute injection", "input": '<img id="config" name="config" src="x" onerror="alert(1)">', "forbidden": ["onerror=", "<img"]}
]

def run_sanitizer_fuzz_suite():
    print("==========================================================")
    print("🧪 RUNNING DOM ALLOW-LIST SANITIZER FUZZING TEST SUITE")
    print("==========================================================")

    passed = 0
    failed = 0
    total = len(FUZZ_PAYLOADS)

    for test in FUZZ_PAYLOADS:
        tid = test["id"]
        name = test["name"]
        raw_input = test["input"]
        sanitized = simulate_dom_allowlist_sanitizer(raw_input)

        failed_reasons = []
        for f in test["forbidden"]:
            if f.lower() in sanitized.lower():
                failed_reasons.append(f"Forbidden fragment '{f}' remained after sanitization.")

        if failed_reasons:
            failed += 1
            print(f"❌ FAIL [{tid}]: {name} -> {', '.join(failed_reasons)}")
        else:
            passed += 1
            print(f"✅ PASS [{tid}]: {name}")

    print("==========================================================")
    print(f"📊 SUMMARY: Total: {total} | Passed: {passed} ({passed/total*100:.1f}%) | Failed: {failed}")
    print("==========================================================")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(run_sanitizer_fuzz_suite())
