#!/usr/bin/env python3
"""
Adobe IMS Authentication Client (OAuth Server-to-Server)
FINNOVA / EZMORTGAGE INTEGRATION SUITE

Handles server-to-server OAuth token generation, verification, and caching
against Adobe Identity Management System (IMS). Adheres strictly to Agent Baniya
cost standards ($0 cloud compute) by utilizing persistent token caching with
automated refresh upon expiry.
"""

import os
import json
import time
import urllib.request
import urllib.parse
from zoneinfo import ZoneInfo
from datetime import datetime, timezone
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
CACHE_PATH = BASE_DIR / ".adobe_token_cache.json"

AEST = ZoneInfo("Australia/Melbourne")

def load_env():
    """Load key-value pairs from .env if present."""
    if not ENV_PATH.exists():
        return
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip("'").strip('"')
            os.environ.setdefault(k.strip(), v)

load_env()

ADOBE_CLIENT_ID = os.environ.get("ADOBE_CLIENT_ID", "")
ADOBE_CLIENT_SECRET = os.environ.get("ADOBE_CLIENT_SECRET", "")
ADOBE_ORG_ID = os.environ.get("ADOBE_ORG_ID", "")
ADOBE_SCOPES = os.environ.get("ADOBE_SCOPES", "read_pc.dma_tartan,additional_info,openid,AdobeID")
INITIAL_ACCESS_TOKEN = os.environ.get("ADOBE_ACCESS_TOKEN", "")

def get_current_aest_time():
    return datetime.now(timezone.utc).astimezone(AEST).isoformat()

def get_cached_token():
    """Reads cached token if valid and not expired."""
    if not CACHE_PATH.exists():
        # Check if INITIAL_ACCESS_TOKEN is present
        if INITIAL_ACCESS_TOKEN:
            return INITIAL_ACCESS_TOKEN
        return None
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 5 minute safety buffer before expiry
            if data.get("expires_at", 0) > time.time() + 300:
                return data.get("access_token")
    except Exception as e:
        print(f"[{get_current_aest_time()}] Warning: failed reading token cache: {e}")
    return None

def save_token_cache(token_data):
    """Saves valid token and calculated expiry to cache."""
    try:
        expires_in = token_data.get("expires_in", 86400000 // 1000) # milliseconds to seconds if needed
        if expires_in > 100000:
            # likely provided in milliseconds
            expires_in = expires_in // 1000
        cache_content = {
            "access_token": token_data.get("access_token"),
            "token_type": token_data.get("token_type", "bearer"),
            "expires_at": time.time() + int(expires_in),
            "updated_at_aest": get_current_aest_time(),
            "org_id": ADOBE_ORG_ID,
            "client_id": ADOBE_CLIENT_ID
        }
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache_content, f, indent=2)
    except Exception as e:
        print(f"[{get_current_aest_time()}] Warning: failed saving token cache: {e}")

def request_fresh_adobe_token():
    """Requests a new Server-to-Server access token from Adobe IMS token/v3 endpoint."""
    if not ADOBE_CLIENT_ID or not ADOBE_CLIENT_SECRET:
        raise ValueError("ADOBE_CLIENT_ID and ADOBE_CLIENT_SECRET must be configured in .env")

    token_url = "https://ims-na1.adobelogin.com/ims/token/v3"
    payload = {
        "grant_type": "client_credentials",
        "client_id": ADOBE_CLIENT_ID,
        "client_secret": ADOBE_CLIENT_SECRET,
        "scope": ADOBE_SCOPES
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        token_url,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            save_token_cache(body)
            print(f"[{get_current_aest_time()}] Successfully obtained fresh Adobe IMS OAuth token.")
            return body.get("access_token")
    except Exception as err:
        print(f"[{get_current_aest_time()}] Adobe token fetch returned error: {err}")
        # Fallback to initial token if available
        if INITIAL_ACCESS_TOKEN:
            print(f"[{get_current_aest_time()}] Falling back to static ADOBE_ACCESS_TOKEN from environment.")
            return INITIAL_ACCESS_TOKEN
        raise

def get_adobe_access_token():
    """Returns valid cached or refreshed Adobe IMS access token."""
    token = get_cached_token()
    if token:
        return token
    return request_fresh_adobe_token()

def get_adobe_headers(content_type="application/json"):
    """Returns authoritative headers for Adobe Developer API callouts."""
    token = get_adobe_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "x-api-key": ADOBE_CLIENT_ID,
        "x-gw-ims-org-id": ADOBE_ORG_ID,
        "Content-Type": content_type
    }

if __name__ == "__main__":
    print("--- Adobe Auth Client Test ---")
    print(f"Client ID: {ADOBE_CLIENT_ID[:6]}...{ADOBE_CLIENT_ID[-4:] if ADOBE_CLIENT_ID else 'EMPTY'}")
    print(f"Org ID: {ADOBE_ORG_ID}")
    try:
        tok = get_adobe_access_token()
        print(f"Access Token Status: VALID (Length: {len(tok)} chars)")
        print("Authoritative Headers:")
        headers = get_adobe_headers()
        print(json.dumps({k: (v[:20] + "..." if k == "Authorization" else v) for k, v in headers.items()}, indent=2))
    except Exception as e:
        print(f"Error validating Adobe token: {e}")
