#!/usr/bin/env python3
"""
Clean up duplicate state declarations in Home.jsx
"""

HOME_JSX_PATH = "/Users/robinbakshi/Documents/Imprtant Repos/procrm-app/src/pages/Home.jsx"

with open(HOME_JSX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

duplicate_block = """  const [flippedCards, setFlippedCards] = useState({});
  const [openFaqIndex, setOpenFaqIndex] = useState(0);
  const [carouselIndex, setCarouselIndex] = useState(0);
  const [isCarouselHovered, setIsCarouselHovered] = useState(false);
  const [carouselIndex, setCarouselIndex] = useState(0);
  const [isCarouselHovered, setIsCarouselHovered] = useState(false);"""

clean_block = """  const [flippedCards, setFlippedCards] = useState({});
  const [openFaqIndex, setOpenFaqIndex] = useState(0);
  const [carouselIndex, setCarouselIndex] = useState(0);
  const [isCarouselHovered, setIsCarouselHovered] = useState(false);"""

if duplicate_block in content:
    content = content.replace(duplicate_block, clean_block, 1)
    with open(HOME_JSX_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Cleaned duplicate states in Home.jsx!")
else:
    print("⚠️ Duplicate block not found exactly as formatted.")
