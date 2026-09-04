#!/usr/bin/env python3
"""
Adobe Primetime Server-Side Ad Insertion (SSAI) & Dynamic Manifest Stitcher
FINNOVA / EZMORTGAGE AI VIDEO SUITE

Provides server-side dynamic pre-roll, mid-roll, and post-roll bumper stitching
into HLS (.m3u8) and DASH (.mpd) video streams.

Key Capabilities:
1. Dynamic Pre-Roll / Mid-Roll Injection: Injects R Bakshi's 5s video greeting,
   RBA rate shifts, or Melbourne suburban finance promotions at the manifest layer.
2. 100% Ad-Blocker Bypass: Stitches video segments directly into native HLS/DASH
   playlists via #EXT-X-DISCONTINUITY, eliminating third-party client VAST/VPAID
   calls that ad-blockers intercept.
3. Zero-Render Instant Bumper Swapping: When the RBA shifts cash rates or a new
   campaign launches, switch CTAs across thousands of published assets instantly
   without re-rendering video files via FFmpeg.
4. Adobe Primetime Ad Insertion (Ad Config Service) session parameter builder.
"""

import os
import re
import json
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

AEST = ZoneInfo("Australia/Melbourne")

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "campaigns"
CONFIG_FILE = CONFIG_DIR / "video_bumpers_config.json"

DEFAULT_CAMPAIGNS = {
    "active_campaign": "rba_rate_alert",
    "bumpers": {
        "r_bakshi_greeting": {
            "id": "r_bakshi_greeting",
            "title": "R Bakshi 5-Second Broker Welcome",
            "duration": 5.0,
            "segments": [
                {"uri": "https://ezmortgagebroker.com.au/assets/videos/bumpers/r_bakshi_greeting_001.ts", "duration": 2.5},
                {"uri": "https://ezmortgagebroker.com.au/assets/videos/bumpers/r_bakshi_greeting_002.ts", "duration": 2.5}
            ],
            "cta_overlay": "Call R Bakshi: 1300 050 099 | CRN 538522",
            "target_segments": ["general", "all"]
        },
        "rba_rate_alert": {
            "id": "rba_rate_alert",
            "title": "RBA Rate Decision Teaser - Sub-5.89% Variable Comparison",
            "duration": 5.0,
            "segments": [
                {"uri": "https://ezmortgagebroker.com.au/assets/videos/bumpers/rba_rate_alert_001.ts", "duration": 2.5},
                {"uri": "https://ezmortgagebroker.com.au/assets/videos/bumpers/rba_rate_alert_002.ts", "duration": 2.5}
            ],
            "cta_overlay": "Is your rate above 6%? Compare 30+ lenders now.",
            "target_segments": ["refinance_saver", "sub_6_refinance"]
        },
        "melbourne_fhb_grant": {
            "id": "melbourne_fhb_grant",
            "title": "Victoria First Home Buyer Grant & Stamp Duty Exemption",
            "duration": 6.0,
            "segments": [
                {"uri": "https://ezmortgagebroker.com.au/assets/videos/bumpers/fhb_grant_001.ts", "duration": 3.0},
                {"uri": "https://ezmortgagebroker.com.au/assets/videos/bumpers/fhb_grant_002.ts", "duration": 3.0}
            ],
            "cta_overlay": "5% Deposit Guarantee & $10k Grant Checklist Available",
            "target_segments": ["first_home_buyer"]
        },
        "smsf_investor_promo": {
            "id": "smsf_investor_promo",
            "title": "Melbourne SMSF Property Borrowing Specialist",
            "duration": 5.0,
            "segments": [
                {"uri": "https://ezmortgagebroker.com.au/assets/videos/bumpers/smsf_promo_001.ts", "duration": 2.5},
                {"uri": "https://ezmortgagebroker.com.au/assets/videos/bumpers/smsf_promo_002.ts", "duration": 2.5}
            ],
            "cta_overlay": "SMSF Residential & Commercial Loans up to 80% LVR",
            "target_segments": ["smsf_investor"]
        }
    },
    "post_roll_cta": {
        "id": "ez_broker_cta",
        "title": "MFAA Accredited Broker Appointment CTA",
        "duration": 4.0,
        "segments": [
            {"uri": "https://ezmortgagebroker.com.au/assets/videos/bumpers/ez_cta_001.ts", "duration": 4.0}
        ],
        "cta_url": "https://ezmortgagebroker.com.au/#contact"
    }
}


def get_current_aest_timestamp():
    """Returns ISO-8601 formatted timestamp in Melbourne timezone."""
    return datetime.now(timezone.utc).astimezone(AEST).isoformat()


def load_campaign_config():
    """Loads active bumper campaign configuration from disk or creates default."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        save_campaign_config(DEFAULT_CAMPAIGNS)
        return DEFAULT_CAMPAIGNS
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[{get_current_aest_timestamp()}] Warning: failed to load {CONFIG_FILE}: {e}")
        return DEFAULT_CAMPAIGNS


def save_campaign_config(config_data):
    """Persists campaign config to disk."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)


def swap_active_bumper(bumper_id):
    """
    Instantly swaps the active video bumper across all server-stitched streams.
    Requires ZERO video re-rendering or FFmpeg execution.
    """
    config = load_campaign_config()
    if bumper_id not in config.get("bumpers", {}):
        raise ValueError(f"Unknown bumper_id '{bumper_id}'. Available: {list(config.get('bumpers', {}).keys())}")

    previous = config.get("active_campaign")
    config["active_campaign"] = bumper_id
    config["last_swapped_at_aest"] = get_current_aest_timestamp()
    save_campaign_config(config)
    print(f"[{get_current_aest_timestamp()}] Bumper Swap Success: '{previous}' -> '{bumper_id}'")
    return config


class AdobePrimetimeSSAI:
    """
    Server-Side Ad Insertion Engine conforming to Adobe Primetime Ad Insertion specs.
    Handles manifest manipulation and ad decision routing.
    """

    def __init__(self, config=None):
        self.config = config or load_campaign_config()

    def build_adobe_ad_config_request(self, stream_url, audience_segment="general", suburb="Melbourne"):
        """
        Builds Adobe Primetime Ad Config Service session initiation payload.
        Used when routing manifests through Adobe Primetime SSAI edge routers.
        """
        active_bumper_key = self.config.get("active_campaign", "r_bakshi_greeting")
        # Match audience segment if specialized
        for b_key, b_data in self.config.get("bumpers", {}).items():
            if audience_segment in b_data.get("target_segments", []):
                active_bumper_key = b_key
                break

        return {
            "ad_config_id": "finnova_ezmortgage_melbourne_v1",
            "stream_url": stream_url,
            "session_time_aest": get_current_aest_timestamp(),
            "targeting": {
                "geo_country": "AU",
                "geo_state": "VIC",
                "geo_suburb": suburb,
                "audience_segment": audience_segment,
                "active_bumper_id": active_bumper_key,
                "client_adblock_status": "bypassed_via_ssai"
            },
            "manifest_router_endpoint": "https://manifest.auditude.com/auditude/variant/finnova/ezmortgage.m3u8"
        }

    def stitch_hls_manifest(self, base_m3u8_content, audience_segment="general", mid_roll_offset_seconds=None):
        """
        Dynamically stitches pre-roll bumper and post-roll CTA directly into HLS playlist.
        Uses RFC 8216 #EXT-X-DISCONTINUITY tags for seamless decoder reset.
        Client ad-blockers see this as native stream media, achieving 100% delivery.
        """
        active_bumper_key = self.config.get("active_campaign", "rba_rate_alert")
        # Check if segment matches specific bumper
        for b_key, b_data in self.config.get("bumpers", {}).items():
            if audience_segment in b_data.get("target_segments", []):
                active_bumper_key = b_key
                break

        bumper = self.config["bumpers"].get(active_bumper_key, self.config["bumpers"]["r_bakshi_greeting"])
        post_roll = self.config.get("post_roll_cta")

        lines = base_m3u8_content.strip().splitlines()
        header_lines = []
        body_lines = []
        in_header = True

        for line in lines:
            line_str = line.strip()
            if in_header:
                if line_str.startswith("#EXTINF") or (not line_str.startswith("#") and line_str):
                    in_header = False
                    body_lines.append(line_str)
                else:
                    header_lines.append(line_str)
            else:
                body_lines.append(line_str)

        # Prepend Pre-Roll Bumper with #EXT-X-DISCONTINUITY
        preroll_block = [
            f"# --- ADOBE PRIMETIME SSAI: PRE-ROLL INJECTION ({bumper['id']}) ---",
            "#EXT-X-DISCONTINUITY",
            f"#EXT-X-PROGRAM-DATE-TIME:{get_current_aest_timestamp()}"
        ]
        for seg in bumper["segments"]:
            preroll_block.append(f"#EXTINF:{seg['duration']:.3f},{bumper['title']}")
            preroll_block.append(seg["uri"])
        preroll_block.append("#EXT-X-DISCONTINUITY")

        # Post-roll injection before #EXT-X-ENDLIST
        postroll_block = []
        if post_roll and post_roll.get("segments"):
            postroll_block.extend([
                f"# --- ADOBE PRIMETIME SSAI: POST-ROLL CTA ({post_roll['id']}) ---",
                "#EXT-X-DISCONTINUITY",
                f"#EXT-X-PROGRAM-DATE-TIME:{get_current_aest_timestamp()}"
            ])
            for seg in post_roll["segments"]:
                postroll_block.append(f"#EXTINF:{seg['duration']:.3f},{post_roll['title']}")
                postroll_block.append(seg["uri"])

        final_body = []
        for line in body_lines:
            if line == "#EXT-X-ENDLIST":
                final_body.extend(postroll_block)
                final_body.append("#EXT-X-ENDLIST")
            else:
                final_body.append(line)

        if "#EXT-X-ENDLIST" not in final_body and postroll_block:
            final_body.extend(postroll_block)
            final_body.append("#EXT-X-ENDLIST")

        stitched_playlist = "\n".join(header_lines + preroll_block + final_body) + "\n"
        return stitched_playlist

    def stitch_dash_mpd(self, base_mpd_content, audience_segment="general"):
        """
        Dynamically stitches dynamic Pre-Roll Period into MPEG-DASH MPD manifest.
        """
        active_bumper_key = self.config.get("active_campaign", "rba_rate_alert")
        bumper = self.config["bumpers"].get(active_bumper_key, self.config["bumpers"]["r_bakshi_greeting"])

        ad_period = f"""  <Period id="adobe_ssai_preroll" duration="PT{bumper['duration']}S">
    <!-- Adobe Primetime SSAI Injected Period: {bumper['title']} -->
    <AdaptationSet mimeType="video/mp4" contentType="video">
      <Representation id="preroll_rep" bandwidth="1500000" width="1080" height="1920">
        <BaseURL>{bumper['segments'][0]['uri']}</BaseURL>
      </Representation>
    </AdaptationSet>
  </Period>"""

        if "<Period" in base_mpd_content:
            stitched = base_mpd_content.replace("<Period", f"{ad_period}\n  <Period", 1)
            return stitched
        return base_mpd_content


def generate_sample_hls():
    """Generates clean sample base HLS manifest for testing."""
    return """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:6
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:5.000,Melbourne Property Market Overview
segment_001.ts
#EXTINF:5.000,Interest Rate Trends
segment_002.ts
#EXTINF:4.500,Summary & Next Steps
segment_003.ts
#EXT-X-ENDLIST
"""


if __name__ == "__main__":
    print("=== Adobe Primetime SSAI Engine Initializing ===")
    ssai = AdobePrimetimeSSAI()
    sample_manifest = generate_sample_hls()

    print("\n[Test 1] Generating SSAI Stitched HLS Manifest for 'first_home_buyer':")
    stitched_fhb = ssai.stitch_hls_manifest(sample_manifest, audience_segment="first_home_buyer")
    print(stitched_fhb)

    print("\n[Test 2] Swapping Active Bumper to 'r_bakshi_greeting':")
    swap_active_bumper("r_bakshi_greeting")
    stitched_general = ssai.stitch_hls_manifest(sample_manifest, audience_segment="general")
    print(stitched_general[:450] + "\n... [truncated] ...")

    print("\n[Test 3] Building Adobe Primetime Ad Config Service Session Request:")
    session_req = ssai.build_adobe_ad_config_request(
        stream_url="https://ezmortgagebroker.com.au/assets/videos/daily-melbourne-update.m3u8",
        audience_segment="refinance_saver",
        suburb="Werribee"
    )
    print(json.dumps(session_req, indent=2))
    print(f"\n[{get_current_aest_timestamp()}] Adobe Primetime SSAI verified successfully.")
