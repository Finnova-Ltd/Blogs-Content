#!/usr/bin/env python3
"""
Zero-Failure Alerting Webhook for GitHub Actions
Sends instant alert notifications to Slack/Discord/Telegram/Custom Webhook upon any automation failure.
"""

import os
import sys
import json
import urllib.request

WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL") or os.getenv("SLACK_WEBHOOK_URL") or os.getenv("DISCORD_WEBHOOK_URL")

def send_failure_alert(repo=None, workflow=None, run_id=None, error_msg=None):
    repo = repo or os.getenv("GITHUB_REPOSITORY", "Finnova-Ltd/Blogs-Content")
    workflow = workflow or os.getenv("GITHUB_WORKFLOW", "Daily Mortgage News & RSS Publisher")
    run_id = run_id or os.getenv("GITHUB_RUN_ID", "local")
    run_url = f"https://github.com/{repo}/actions/runs/{run_id}"

    payload = {
        "text": f"🚨 *GitHub Action Failed*: `{repo}`\n"
                f"• *Workflow*: {workflow}\n"
                f"• *Run ID*: {run_id}\n"
                f"• *View Logs*: {run_url}\n"
                f"• *Status*: Failed during scheduled publishing execution.",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🚨 *GitHub Action Failed on `{repo}`*\n*Workflow:* {workflow}\n*Run:* <{run_url}|View Action Logs>"
                }
            }
        ]
    }

    if not WEBHOOK_URL:
        print(f"⚠️ [Alerting] No ALERT_WEBHOOK_URL configured. Local alert payload:\n{json.dumps(payload, indent=2)}")
        return

    req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload).encode("utf-8"), headers={
        "Content-Type": "application/json"
    })

    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            print(f"✅ [Alerting] Sent failure alert to webhook (HTTP {res.status}).")
    except Exception as e:
        print(f"❌ [Alerting] Failed to send alert: {e}")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else None
    send_failure_alert(error_msg=msg)
