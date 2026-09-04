#!/usr/bin/env python3
"""
AI Credits & Quota Tracker for ElevenLabs and Cloudflare
Enforces Australian Timezone (Australia/Melbourne) as per AGENTS.md conventions.
"""

import os
import sys
import json
import datetime
from zoneinfo import ZoneInfo
import requests
from dotenv import load_dotenv

MELBOURNE_TZ = ZoneInfo("Australia/Melbourne")

def get_melbourne_time_str():
    return datetime.datetime.now(MELBOURNE_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")

def get_elevenlabs_credits():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        return {"error": "Missing ELEVENLABS_API_KEY in environment"}
    
    try:
        res = requests.get(
            "https://api.elevenlabs.io/v1/user/subscription",
            headers={"xi-api-key": api_key},
            timeout=10
        )
        if res.status_code != 200:
            return {"error": f"API Error {res.status_code}: {res.text}"}
        
        data = res.json()
        tier = data.get("tier", "unknown")
        char_count = data.get("character_count", 0)
        char_limit = data.get("character_limit", 0)
        remaining = max(0, char_limit - char_count)
        reset_unix = data.get("next_character_count_reset_unix", 0)
        
        reset_str = "N/A"
        if reset_unix:
            reset_dt = datetime.datetime.fromtimestamp(reset_unix, tz=datetime.timezone.utc).astimezone(MELBOURNE_TZ)
            reset_str = reset_dt.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        percent_remaining = (remaining / char_limit * 100) if char_limit > 0 else 0.0
        
        return {
            "service": "ElevenLabs",
            "tier": tier,
            "used": char_count,
            "limit": char_limit,
            "remaining": remaining,
            "percent_remaining": f"{percent_remaining:.1f}%",
            "next_reset": reset_str,
            "status": "healthy" if percent_remaining > 10 else "low"
        }
    except Exception as e:
        return {"error": str(e)}

def get_cloudflare_usage():
    api_key = os.getenv("CLOUDFLARE_API_KEY")
    email = os.getenv("CLOUDFLARE_EMAIL", "testcustomer2022@gmail.com")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "7c65e471e9b5f8203763393276833de2")
    
    if not api_key:
        return {"error": "Missing CLOUDFLARE_API_KEY in environment"}
    
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Query today usage in UTC
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    today_utc = now_utc.strftime("%Y-%m-%d")
    
    query = """
    query GetAccountAnalytics($accountTag: string!, $date: string!) {
      viewer {
        accounts(filter: {accountTag: $accountTag}) {
          workersInvocationsAdaptive(limit: 10, filter: {date: $date}) {
            sum {
              subrequests
              requests
            }
          }
        }
      }
    }
    """
    
    try:
        res = requests.post(
            "https://api.cloudflare.com/client/v4/graphql",
            headers=headers,
            json={"query": query, "variables": {"accountTag": account_id, "date": today_utc}},
            timeout=10
        )
        if res.status_code != 200:
            return {"error": f"API Error {res.status_code}: {res.text}"}
        
        data = res.json()
        accounts = data.get("data", {}).get("viewer", {}).get("accounts", [])
        requests_today = 0
        subrequests_today = 0
        if accounts and accounts[0].get("workersInvocationsAdaptive"):
            summary = accounts[0]["workersInvocationsAdaptive"][0].get("sum", {})
            requests_today = summary.get("requests", 0)
            subrequests_today = summary.get("subrequests", 0)
        
        daily_free_limit = 100_000
        remaining_requests = max(0, daily_free_limit - requests_today)
        percent_remaining = (remaining_requests / daily_free_limit * 100)
        
        return {
            "service": "Cloudflare Workers & AI",
            "tier": "Free Tier (Daily Reset)",
            "requests_today": requests_today,
            "subrequests_today": subrequests_today,
            "daily_free_limit": daily_free_limit,
            "requests_remaining_today": remaining_requests,
            "percent_remaining": f"{percent_remaining:.1f}%",
            "neuron_free_quota_daily": "10,000 Neurons / Day",
            "estimated_daily_cost": "$0.00 AUD"
        }
    except Exception as e:
        return {"error": str(e)}

def print_report():
    print("=" * 70)
    print(f"  AI SERVICES USAGE & CREDITS MONITOR ({get_melbourne_time_str()})")
    print("=" * 70)
    
    eleven = get_elevenlabs_credits()
    print("\n[1] ELEVENLABS VOICE CREDITS:")
    if "error" in eleven:
        print(f"  Error: {eleven['error']}")
    else:
        print(f"  Tier:               {eleven['tier'].upper()}")
        print(f"  Characters Used:    {eleven['used']:,} / {eleven['limit']:,}")
        print(f"  Remaining Credits:  {eleven['remaining']:,} ({eleven['percent_remaining']})")
        print(f"  Next Monthly Reset: {eleven['next_reset']}")
        print(f"  Status:             {eleven['status'].upper()}")

    cf = get_cloudflare_usage()
    print("\n[2] CLOUDFLARE WORKERS & AI QUOTA (ZERO-COST TARGET):")
    if "error" in cf:
        print(f"  Error: {cf['error']}")
    else:
        print(f"  Tier:               {cf['tier']}")
        print(f"  Requests Today:     {cf['requests_today']:,} / {cf['daily_free_limit']:,}")
        print(f"  Subrequests:        {cf['subrequests_today']:,}")
        print(f"  Remaining Requests: {cf['requests_remaining_today']:,} ({cf['percent_remaining']})")
        print(f"  Workers AI Quota:   {cf['neuron_free_quota_daily']}")
        print(f"  Current Cost:       {cf['estimated_daily_cost']}")
    print("=" * 70)

if __name__ == "__main__":
    load_dotenv()
    print_report()
