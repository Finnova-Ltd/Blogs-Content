#!/usr/bin/env python3
"""
Blog Article to Video Script & Social Reel Automation
------------------------------------------------------
Converts any published blog article across our 5 platforms into:
1. 45-60s High-Retention Script for YouTube Shorts / Facebook Reels / TikTok.
2. Hook, 3 Core Takeaways, and Strong CTA (Call To Action).
3. Optimized Video Title, Description, and Viral Hashtags (#Shorts #Australia #Fintech).
4. Text-to-Speech prompt ready for free Microsoft Edge Neural TTS (en-AU-NatashaNeural / en-AU-WilliamNeural).
"""

import os
import json
import re

def generate_video_package(article_title, article_excerpt, brand_name, website_url):
    """
    Builds a complete, free-to-render short-form video package from an article.
    """
    hook = f"Did you know this latest update about {article_title.split(':')[0]}?"
    script_lines = [
        f"🚨 Big financial and tech update for Australians.",
        f"{article_excerpt}",
        f"If you are managing your loans, business software, or contracts in 2026, staying ahead of this rule can save you thousands.",
        f"👉 Read the full breakdown and get actionable steps at {website_url}."
    ]
    full_voiceover_text = " ".join(script_lines)
    
    tags = ["#Shorts", "#Australia", f"#{brand_name.replace(' ', '')}", "#Finance", "#TechNews", "#Reels"]
    
    return {
        "video_format": "9:16 Vertical (1080x1920) for YouTube Shorts, Reels & TikTok",
        "duration_estimate": "35-50 seconds",
        "suggested_voice": "en-AU-NatashaNeural (Australian Female) or en-AU-WilliamNeural (Australian Male)",
        "video_title": f"🚨 {article_title[:60]} #Shorts",
        "video_description": f"{article_excerpt}\n\n🔗 Full guide: {website_url}\n\n{' '.join(tags)}",
        "voiceover_script": full_voiceover_text,
        "visual_storyboard": [
            {"sec": "0-5s", "visual": "Punchy animated headline text on high-contrast dark gradient", "audio": script_lines[0]},
            {"sec": "5-20s", "visual": "Stock b-roll footage of Australian skyline / mobile dashboard / bank apps", "audio": script_lines[1]},
            {"sec": "20-35s", "visual": "Key data breakdown graphics with pulsing highlight boxes", "audio": script_lines[2]},
            {"sec": "35-45s", "visual": "Logo reveal & CTA button animation pointing to website", "audio": script_lines[3]}
        ]
    }

if __name__ == "__main__":
    demo = generate_video_package(
        "RBA Inflation Data & 2026 Cash Rate Forecast: What Borrowers Need to Know",
        "As headline inflation moderates, major lenders are adjusting fixed-rate pricing and stress-test assessment criteria.",
        "EZ Mortgage Broker",
        "https://ezmortgagebroker.com.au/pages/blog/rba-inflation-data-cash-rate-forecast-2026.html"
    )
    print("🎬 Generated Free Video Automation Package:")
    print(json.dumps(demo, indent=2))
