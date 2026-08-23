#!/usr/bin/env python3
"""
Patch Home.jsx in procrm-app:
Fix ReferenceError by explicitly defining carouselIndex and isCarouselHovered state
"""

import os

HOME_JSX_PATH = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/pages/Home.jsx"

with open(HOME_JSX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Home function definition and states
target_old = """export default function Home() {
  const { hash } = useLocation();
  const [flippedCards, setFlippedCards] = useState({});
  const [openFaqIndex, setOpenFaqIndex] = useState(0);"""

target_new = """export default function Home() {
  const { hash } = useLocation();
  const [flippedCards, setFlippedCards] = useState({});
  const [openFaqIndex, setOpenFaqIndex] = useState(0);
  const [carouselIndex, setCarouselIndex] = useState(0);
  const [isCarouselHovered, setIsCarouselHovered] = useState(false);"""

if target_old in content:
    content = content.replace(target_old, target_new, 1)
    print("✅ Replaced state definitions successfully.")
else:
    print("⚠️ target_old not found. Looking for fallback pattern...")
    import re
    content = re.sub(
        r"export default function Home\(\)\s*\{",
        "export default function Home() {\n  const [carouselIndex, setCarouselIndex] = useState(0);\n  const [isCarouselHovered, setIsCarouselHovered] = useState(false);",
        content,
        count=1
    )

with open(HOME_JSX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("🎉 Home.jsx patched successfully!")
