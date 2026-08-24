#!/usr/bin/env python3
"""
Update Finnova (finnova.org.au) with 25-Aug-2026 Community & Cyber Safety Articles
"""

import os
import json

FINNOVA_DIR = "/Users/robinbakshi/Documents/Imprtant Repos/Finnova"
BLOGS_DIR = "/Users/robinbakshi/Documents/GitHub/Blogs-Content"

FINNOVA_POSTS_PATH = os.path.join(FINNOVA_DIR, "posts.json")
BLOGS_POSTS_PATH = os.path.join(BLOGS_DIR, "posts.json")

NEW_FINNOVA_ARTICLES = [
    {
        "id": "ai-voice-scams-senior-cyber-defense-2026",
        "title": "AI-Powered Voice & SMS Scams Surge in Victoria: Finnova Launches Free Senior Cyber Defense Workshops",
        "date": "25 August 2026",
        "author": "Cyber Safety Taskforce",
        "category": "Cyber Safety & Scams",
        "image": "images/blog-cyber-safety.webp",
        "summary": "How AI voice cloning and fake government SMS scams are targeting elderly Australians, and how Finnova's free community workshops protect local families across Wyndham.",
        "body": [
            "<p>A dangerous new wave of AI-driven voice cloning and sophisticated text message impersonation scams is targeting Victorian seniors and multicultural families. Scammers use short audio clips extracted from social media to replicate a relative's voice, calling grandparents in distress and requesting urgent wire transfers for medical emergencies or legal bail.</p>",
            "<p>To combat this escalating threat, Finnova Ltd has launched a series of free, hands-on Cyber Safety & Anti-Scam Workshops across community hubs in Tarneit, Point Cook, and Werribee. Our accredited digital navigators teach practical verification protocols: creating family safe-words, recognizing spoofed Australian mobile numbers, and setting up biometric call-screening tools.</p>",
            "<p>\"Scammers rely on panic and emotional urgency to bypass critical thinking,\" explains Robin Bakshi, Founder of Finnova. \"Our workshops empower seniors with a simple, three-step defense: Pause, Verify via a known secondary channel, and Never send money without confirming in person. We provide a supportive, jargon-free learning environment where anyone can bring their smartphone and learn at their own pace.\"</p>",
            "<p>Workshops are completely free for all Victorian residents, seniors clubs, and multicultural community groups. Register for an upcoming session at your local Wyndham library or request an in-house presentation for your community group today.</p>"
        ]
    },
    {
        "id": "digital-inclusion-ndis-participants-tarneit-2026",
        "title": "Digital Literacy for NDIS Participants: Navigating the My NDIS App & Telehealth Safely",
        "date": "25 August 2026",
        "author": "Disability Inclusion Team",
        "category": "Digital Inclusion",
        "image": "images/blog-volunteer.webp",
        "summary": "How Finnova's specialized digital mentoring empowers NDIS participants to track funding budgets, book verified support workers, and access virtual appointments independently.",
        "body": [
            "<p>Digital portals and telehealth platforms have become essential tools for managing NDIS plan allocations and allied health appointments. However, complex interfaces, two-factor authentication hurdles, and screen-reader accessibility gaps continue to create unnecessary obstacles for participants living with cognitive, physical, or sensory disabilities.</p>",
            "<p>Finnova's Digital Inclusion Taskforce delivers tailored 1-on-1 coaching for NDIS participants, carers, and plan nominees. Our mentors assist participants to configure the My NDIS mobile app, set up automated budget tracking notifications, and safely navigate telehealth video consultations without relying entirely on third-party intermediaries.</p>",
            "<p>\"Digital autonomy is a fundamental pillar of personal independence,\" says the Finnova Community Access Lead. \"When a participant gains the confidence to independently review their service invoices or submit payment claims, it builds tremendous dignity and self-determination.\"</p>",
            "<p>Sessions are delivered in accessible venues with adaptive technology aids, including high-contrast displays, speech-to-text keyboards, and bilingual assistance in Hindi, Punjabi, Arabic, and Vietnamese.</p>"
        ]
    },
    {
        "id": "wyndham-youth-tech-mentorship-bridging-divide-2026",
        "title": "Wyndham Youth Tech Mentorship: High School Volunteers Bridge the Digital Divide in Western Melbourne",
        "date": "25 August 2026",
        "author": "Youth & Community Desk",
        "category": "Volunteer Spotlight",
        "image": "images/finnova-census-support.webp",
        "summary": "Meet the passionate high school and university students dedicating their weekends to teach digital skills, myGov setup, and device security to local elders.",
        "body": [
            "<p>In one of Australia's fastest-growing municipal areas, a remarkable intergenerational partnership is flourishing. The Finnova Youth Tech Ambassador Program connects tech-savvy high school and university students with elderly and newly arrived residents across Wyndham.</p>",
            "<p>Every weekend at local library study spaces and community centres, student mentors provide patient guidance on everything from downloading public transport apps and digital driver licences to spotting deceptive phishing links. For many elderly participants who do not have immediate family nearby, these weekly mentoring sessions provide essential social connection alongside practical technical skills.</p>",
            "<p>\"Teaching an elderly neighbour how to video call their grandchildren overseas or check their digital pension card gives our youth volunteers immense purpose and community leadership experience,\" notes Finnova's Volunteer Coordinator.</p>",
            "<p>Finnova provides all youth mentors with formal volunteer leadership certificates, working with children check accreditations, and reference credentials for university and employment applications.</p>"
        ]
    }
]

def update_finnova():
    # 1. Update Finnova/posts.json
    with open(FINNOVA_POSTS_PATH, "r", encoding="utf-8") as f:
        existing_finnova = json.load(f)

    new_slugs = {p["id"] for p in NEW_FINNOVA_ARTICLES}
    filtered_finnova = [p for p in existing_finnova if p.get("id") not in new_slugs]
    combined_finnova = NEW_FINNOVA_ARTICLES + filtered_finnova

    with open(FINNOVA_POSTS_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_finnova, f, indent=2)
    print(f"✅ Updated {FINNOVA_POSTS_PATH} with {len(combined_finnova)} articles!")

    # 2. Update Blogs-Content/posts.json
    blogs_formatted = []
    for p in NEW_FINNOVA_ARTICLES:
        blogs_formatted.append({
            "id": p["id"],
            "slug": p["id"],
            "title": p["title"],
            "category": p["category"],
            "badge": "COMMUNITY & DIGITAL INCLUSION",
            "date": "25-Aug-2026",
            "iso_date": "2026-08-25T08:00:00Z",
            "readTime": "5 min read",
            "author": p["author"],
            "authorRole": "Finnova Community Inclusion Desk",
            "authorImg": "/images/ez-mortgage-broker.webp",
            "excerpt": p["summary"],
            "snippet": p["summary"],
            "image": "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=1200&q=80",
            "url": f"/pages/blog/{p['id']}.html"
        })

    with open(BLOGS_POSTS_PATH, "r", encoding="utf-8") as f:
        existing_blogs = json.load(f)

    filtered_blogs = [p for p in existing_blogs if p.get("id") not in new_slugs]
    combined_blogs = blogs_formatted + filtered_blogs

    with open(BLOGS_POSTS_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_blogs, f, indent=2)
    print(f"✅ Updated {BLOGS_POSTS_PATH} with {len(combined_blogs)} articles!")

if __name__ == "__main__":
    update_finnova()
