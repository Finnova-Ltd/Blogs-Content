#!/usr/bin/env python3
"""
YouTube SEO & Schema Generator for Cloudflare Workers AI & Make.com Pipeline
----------------------------------------------------------------------------
Implements:
1. YouTube Long-Form Metadata (16:9 8-10m) with CTR Titles & Formatted Chapter Timestamps.
2. YouTube Shorts Metadata (9:16 30-60s) with viral hooks and direct domain CTAs.
3. On-Site Google VideoObject JSON-LD Schema with Clip Segments (hasPart) for rich search snippets.
"""

import os
import json
from datetime import datetime

BRAND_INFO = {
    "ezmortgage": {
        "brand_id": "EZ_MORTGAGE_BROKER",
        "name": "EZ Mortgage Broker",
        "phone": "1300 050 099",
        "domain": "ezmortgagebroker.com.au",
        "logo_url": "https://ezmortgagebroker.com.au/images/ez-mortgage-broker.webp",
        "channel_id": os.getenv("YOUTUBE_CHANNEL_EZ_MORTGAGE", "UChNn75o0Zp4FW60uOYCE1wA"),
        "category_id": "27", # Education / Finance
        "default_lang": "en-AU",
        "primary_tags": [
            "rba cash rate",
            "home loan refinance australia",
            "first home buyer grant 2026",
            "fixed vs variable mortgage australia",
            "borrowing power calculator",
            "ez mortgage broker"
        ]
    },
    "ezconsultants": {
        "brand_id": "EZ_CONSULTANTS",
        "name": "EZ Consultants",
        "phone": "1300 050 099",
        "domain": "ezconsultants.com.au",
        "logo_url": "https://ezconsultants.com.au/assets/logo.png",
        "channel_id": os.getenv("YOUTUBE_CHANNEL_EZ_CONSULTANTS", "UC4o6IW-uQfv-uvLOG7yxCEA"),
        "category_id": "27",
        "default_lang": "en-AU",
        "primary_tags": [
            "australian tax deductions 2026",
            "small business grants australia",
            "rd tax incentive",
            "asic company compliance",
            "ez consultants"
        ]
    },
    "procrm": {
        "brand_id": "PRO_CRM",
        "name": "PRO CRM",
        "phone": "1300 050 099",
        "domain": "procrm.com.au",
        "logo_url": "https://procrm.com.au/assets/procrm-logo.png",
        "channel_id": os.getenv("YOUTUBE_CHANNEL_PRO_CRM", "UCip7du8aZJVYRUcuYF9CoVg"),
        "category_id": "28", # Science & Technology
        "default_lang": "en-AU",
        "primary_tags": [
            "enterprise crm automation",
            "lead management software",
            "sales pipeline optimization",
            "iso 27001 crm security",
            "procrm australia"
        ]
    },
    "finnova": {
        "brand_id": "FINNOVA_HUB",
        "name": "Finnova Hub",
        "phone": "1300 050 099",
        "domain": "finnova.org.au",
        "logo_url": "https://finnova.org.au/images/finnova-logo-stars.webp",
        "channel_id": os.getenv("YOUTUBE_CHANNEL_FINNOVA", "UCkkNiLMkzV78vGLfEjIzcRg"),
        "category_id": "28",
        "default_lang": "en-AU",
        "primary_tags": [
            "australian fintech news",
            "sme digital transformation",
            "open source business tools",
            "cloudflare serverless",
            "finnova australia"
        ]
    }
}

def format_iso_duration(seconds):
    """Converts seconds to ISO 8601 duration string e.g. PT8M45S."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"PT{mins}M{secs}S"

def generate_longform_youtube_metadata(
    brand_key,
    master_title,
    episodes,
    timestamps,
    total_seconds=510.0,
    youtube_video_id="YOUR_YOUTUBE_ID"
):
    """
    Generates YouTube Long-Form (16:9) SEO Payload and On-Site VideoObject JSON-LD Schema.
    """
    b = BRAND_INFO.get(brand_key, BRAND_INFO["ezmortgage"])
    
    # 1. High-CTR Title (50-65 chars)
    clean_title = master_title.strip()
    if len(clean_title) > 65:
        clean_title = clean_title[:62].rsplit(" ", 1)[0] + "..."
        
    # 2. Strategic Description with primary links in first 150 chars
    article_links = []
    for ep in episodes:
        article_links.append(f"• {ep['title']}: https://{b['domain']}/{ep.get('slug', '')}")
    links_block = "\n".join(article_links)
    
    timestamps_block = "\n".join(timestamps)
    
    description = (
        f"Comprehensive Australian market briefing and strategy guide by {b['name']}.\n"
        f"👉 Read full guides & calculate savings: https://{b['domain']}\n\n"
        f"🔗 EXPLORE ARTICLES IN THIS EPISODE:\n{links_block}\n\n"
        f"📌 CHAPTER TIMESTAMPS:\n{timestamps_block}\n\n"
        f"------------------------------------------\n"
        f"ABOUT {b['name'].upper()}:\n"
        f"We empower Australian consumers and businesses. Speak with our accredited team on {b['phone']} or visit https://{b['domain']}.\n\n"
        f"#{b['name'].replace(' ', '')} #Australia #Finance #Business #2026Guide"
    )
    
    # 3. Complete YouTube Metadata Object
    youtube_payload = {
        "brand_id": b["brand_id"],
        "target_platform": "YouTube Long-Form (16:9)",
        "video_title": clean_title,
        "video_description": description,
        "tags": b["primary_tags"],
        "category_id": b["category_id"],
        "default_language": b["default_lang"],
        "channel_id": b["channel_id"]
    }
    
    # 4. JSON-LD VideoObject Schema for On-Site Google Rich Results
    has_parts = []
    for i, ep in enumerate(episodes):
        start_sec = 30 + (i * 120)
        end_sec = start_sec + 120
        has_parts.append({
            "@type": "Clip",
            "name": ep["title"],
            "startOffset": start_sec,
            "endOffset": end_sec,
            "url": f"https://www.youtube.com/watch?v={youtube_video_id}&t={start_sec}s"
        })
        
    json_ld_schema = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": clean_title,
        "description": f"Comprehensive guide by {b['name']} exploring Australian rates, strategies, and industry insights.",
        "thumbnailUrl": [
            f"https://img.youtube.com/vi/{youtube_video_id}/maxresdefault.jpg"
        ],
        "uploadDate": datetime.now().isoformat(),
        "duration": format_iso_duration(total_seconds),
        "embedUrl": f"https://www.youtube.com/embed/{youtube_video_id}",
        "publisher": {
            "@type": "Organization",
            "name": b["name"],
            "logo": {
                "@type": "ImageObject",
                "url": b["logo_url"]
            }
        },
        "hasPart": has_parts
    }
    
    return {
        "youtube_payload": youtube_payload,
        "json_ld_schema": json_ld_schema
    }

def generate_shorts_youtube_metadata(
    brand_key,
    hook_title,
    excerpt,
    calculator_path="/calculator"
):
    """
    Generates YouTube Shorts (9:16) High-Retention Metadata.
    """
    b = BRAND_INFO.get(brand_key, BRAND_INFO["ezmortgage"])
    
    # Format Title with #Shorts
    clean_hook = hook_title.replace("#Shorts", "").strip()
    if len(clean_hook) > 55:
        clean_hook = clean_hook[:52].rsplit(" ", 1)[0]
    title_short = f"{clean_hook} 📈 #Shorts"
    
    description = (
        f"{excerpt}\n\n"
        f"📞 Call Us Today: {b['phone']}\n"
        f"👉 Free Online Calculator: https://{b['domain']}{calculator_path}\n\n"
        f"#{b['name'].replace(' ', '')} #Australia #Finance #Shorts"
    )
    
    return {
        "brand_id": b["brand_id"],
        "target_platform": "YouTube Shorts (9:16)",
        "video_title": title_short,
        "video_description": description,
        "tags": b["primary_tags"] + ["shorts", "australia"],
        "category_id": b["category_id"],
        "channel_id": b["channel_id"]
    }

if __name__ == "__main__":
    sample_episodes = [
        {"title": "RBA Cash Rate Outlook 2026", "slug": "rba-cash-rate-outlook-2026"},
        {"title": "Fixed vs Variable Refinancing Guide", "slug": "fixed-vs-variable-refinancing-guide"},
        {"title": "First Home Buyer Grants NSW & VIC", "slug": "first-home-buyer-grants-2026"},
        {"title": "Broker vs Bank Borrowing Power", "slug": "broker-vs-bank-borrowing-power"}
    ]
    sample_timestamps = [
        "0:00 - Introduction & Market Overview",
        "0:30 - Chapter 1: RBA Cash Rate Outlook 2026",
        "2:30 - Chapter 2: Fixed vs Variable Refinancing Guide",
        "4:30 - Chapter 3: First Home Buyer Grants NSW & VIC",
        "6:30 - Chapter 4: Broker vs Bank Borrowing Power",
        "8:30 - Summary & Free Assessment"
    ]
    
    result = generate_longform_youtube_metadata(
        brand_key="ezmortgage",
        master_title="RBA Rate Decision Breakdown: Refinancing & First Home Grants [2026]",
        episodes=sample_episodes,
        timestamps=sample_timestamps,
        total_seconds=525.0
    )
    
    out_dir = "/Users/robinbakshi/Documents/GitHub/Blogs-Content/assets/seo_payloads"
    os.makedirs(out_dir, exist_ok=True)
    
    with open(os.path.join(out_dir, "sample_longform_payload.json"), "w") as f:
        json.dump(result["youtube_payload"], f, indent=2)
        
    with open(os.path.join(out_dir, "sample_video_schema.json"), "w") as f:
        json.dump(result["json_ld_schema"], f, indent=2)
        
    print("✅ Successfully generated sample YouTube SEO Payload and JSON-LD Schema in:", out_dir)
