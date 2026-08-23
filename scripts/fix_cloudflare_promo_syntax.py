#!/usr/bin/env python3
"""
Patch syntax errors in Cloudflare Agents index.ts:
Replace TypeScript casting inside client-side injected script strings with pure vanilla JavaScript
"""

import os

PATHS = [
    "/Users/robinbakshi/Documents/GitHub/Cloudflare Agents/src/index.ts",
    "/Users/robinbakshi/Documents/GitHub/Blogs-Content/cloudflare/chat-agent/src/index.ts"
]

target_old = "const parentComp = parentNode && parentNode.nodeType === 1 ? window.getComputedStyle(parentNode as Element) : ({} as CSSStyleDeclaration);"
target_new = "const parentComp = parentNode && parentNode.nodeType === 1 ? window.getComputedStyle(parentNode) : {};"

for p in PATHS:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        
        if target_old in content:
            content = content.replace(target_old, target_new)
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Patched syntax error in: {p}")
        else:
            print(f"⚠️ Target string not found in: {p}")

print("🎉 Cloudflare worker scripts updated successfully!")
