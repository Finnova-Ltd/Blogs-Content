#!/usr/bin/env python3
"""
Test Suite for Adobe Developer Console Integration Suite
FINNOVA / EZMORTGAGE BROKERAGE

Validates:
1. Adobe OAuth Server-to-Server Authentication Client
2. Adobe Primetime SSAI Manifest Manipulation & Instant Bumper Swapping
3. Adobe Tartan Personalization & Telemetry Configs
4. Adobe Document Services Fact Sheet Generator
5. Adobe Sensei Smart Visual Cropping
"""

import os
import sys
import json
import pytest
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.adobe_auth_client import (
    get_adobe_headers,
    get_cached_token,
    ADOBE_CLIENT_ID,
    ADOBE_ORG_ID
)
from scripts.adobe_primetime_ssai import (
    AdobePrimetimeSSAI,
    swap_active_bumper,
    load_campaign_config,
    generate_sample_hls
)
from scripts.adobe_pdf_factsheet_generator import generate_factsheet_html
from scripts.smart_visual_cropper import SmartVisualCropper

AEST = ZoneInfo("Australia/Melbourne")


def test_adobe_auth_client_headers():
    """Verify Adobe OAuth client produces authoritative headers with valid client ID and Org ID."""
    headers = get_adobe_headers()
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Bearer ")
    assert headers["x-api-key"] == ADOBE_CLIENT_ID
    assert headers["x-gw-ims-org-id"] == ADOBE_ORG_ID


def test_adobe_primetime_ssai_stitching():
    """Verify SSAI engine stitches #EXT-X-DISCONTINUITY and bumper segments into HLS playlists."""
    ssai = AdobePrimetimeSSAI()
    sample = generate_sample_hls()
    stitched = ssai.stitch_hls_manifest(sample, audience_segment="first_home_buyer")

    assert "#EXT-X-DISCONTINUITY" in stitched
    assert "melbourne_fhb_grant" in stitched or "fhb_grant" in stitched
    assert "segment_001.ts" in stitched
    assert "#EXT-X-ENDLIST" in stitched


def test_adobe_primetime_bumper_swapping():
    """Verify dynamic bumper swapping occurs instantly at the configuration layer."""
    config_after = swap_active_bumper("r_bakshi_greeting")
    assert config_after["active_campaign"] == "r_bakshi_greeting"

    # Swap back to rate alert
    config_alert = swap_active_bumper("rba_rate_alert")
    assert config_alert["active_campaign"] == "rba_rate_alert"


def test_adobe_pdf_factsheet_generator():
    """Verify factsheet HTML contains MFAA accreditation, R Bakshi CRN 538522, and lending rates."""
    article = {
        "title": "Melbourne Sub-6% Variable Home Loan Analysis",
        "summary": "Comparing 30+ lenders to secure competitive variable borrowing power.",
        "category": "Refinancing"
    }
    html = generate_factsheet_html(article)
    assert "R BAKSHI" in html
    assert "538522" in html
    assert "1300 050 099" in html
    assert "MFAA ACCREDITED" in html
    assert "National Consumer Credit Protection Act 2009" in html
    assert "Owner Occupied" in html


def test_smart_visual_cropper():
    """Verify portrait images and person keywords trigger top-center focal positioning."""
    cropper = SmartVisualCropper()
    res_face = cropper.analyze_image("/images/broker-consultation-rate-review.jpg")
    assert res_face["recommended_object_position"] == "top center"
    assert res_face["is_portrait_or_subject"] is True

    res_skyline = cropper.analyze_image("/images/melbourne-skyline.webp")
    assert res_skyline["recommended_object_position"] == "center center"
