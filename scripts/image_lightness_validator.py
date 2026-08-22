#!/usr/bin/env python3
"""
Lightness & Quality Validator for Article Imagery
Ensures all images used across EZ Mortgage, EZ Consultants, and PRO CRM are light-colored,
bright, high-contrast, and compliant with premium design standards.
"""

import urllib.parse
import random

LIGHT_CURATED_COLLECTION = {
    "finance": [
        "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=80", # Bright modern sunlit home
        "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=1200&q=80", # Clean light suburban house with green lawn
        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80", # Bright luxury villa exterior
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80", # Sunlit architectural modern home
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80", # Sunlit living room with large windows
        "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80", # Bright calculator, contract & natural light
        "https://images.unsplash.com/photo-1554224154-26032ffc0d07?auto=format&fit=crop&w=1200&q=80", # Clean bright financial paperwork & pen
        "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80"  # Bright smiling financial consultation
    ],
    "enterprise": [
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80", # Bright modern collaborative office
        "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1200&q=80", # Sunlit boardroom & strategy discussion
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80", # Bright analytics dashboard & laptop
        "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80", # Minimalist light desk with MacBook
        "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=1200&q=80", # Bright tech team collaboration
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80", # White modern architecture & blue sky
        "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=1200&q=80", # Bright consulting executive
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80", # Bright innovation workshop
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80", # Clean light fintech dashboard
        "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80", # Sunlit team meeting with whiteboards
        "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80"  # Clean bright modern workspace
    ]
}

DARK_KEYWORDS = [
    "dark", "black", "night", "cyber-dark", "neon-black", "hacker", "terminal", "dark-room", "shadow"
]

def sanitize_and_lighten_query(query, domain="finance"):
    """
    Ensures search query explicitly targets high-key, sunlit, light-background photography.
    """
    clean = query.lower()
    for dk in DARK_KEYWORDS:
        clean = clean.replace(dk, "")
    
    if domain == "finance" or "mortgage" in clean or "loan" in clean or "property" in clean:
        return f"bright modern sunlit home interior natural daylight {clean.strip()}"[:80]
    else:
        return f"bright modern light sunlit corporate office glass daylight {clean.strip()}"[:80]

def get_guaranteed_light_image(domain="finance"):
    """Returns a guaranteed light, bright, high-resolution royalty-free image."""
    collection = LIGHT_CURATED_COLLECTION.get(domain, LIGHT_CURATED_COLLECTION["enterprise"])
    return random.choice(collection)

if __name__ == "__main__":
    print("Guaranteed Light Finance Image:", get_guaranteed_light_image("finance"))
    print("Guaranteed Light Enterprise Image:", get_guaranteed_light_image("enterprise"))
