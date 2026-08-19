#!/usr/bin/env python3
"""
Make.com (Integromat) API v2 Client
==================================
Official REST API integration for Make.com according to Developer Hub specifications.
Reference: https://developers.make.com/api-documentation

Features:
- Authentication via 'Authorization: Token <token>'
- Multi-zone endpoint resolution (eu1, eu2, us1, us2, custom)
- User / Team / Organization introspection (/users/me, /teams, /organizations)
- Scenario management (List, Details, Run / Trigger on demand, Logs)
- Webhook management & Direct Webhook dispatch
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, List, Optional

# Supported Make zones
MAKE_ZONES = {
    "eu1": "https://eu1.make.com/api/v2",
    "eu2": "https://eu2.make.com/api/v2",
    "us1": "https://us1.make.com/api/v2",
    "us2": "https://us2.make.com/api/v2",
    "celonis-eu1": "https://eu1.make.celonis.com/api/v2",
    "celonis-us1": "https://us1.make.celonis.com/api/v2",
}

class MakeApiClient:
    def __init__(
        self,
        api_token: Optional[str] = None,
        zone: str = "eu1",
        team_id: Optional[int] = None,
        organization_id: Optional[int] = None
    ):
        self.api_token = api_token or os.getenv("MAKE_API_TOKEN", "")
        self.zone = (zone or os.getenv("MAKE_ZONE", "eu1")).lower()
        self.base_url = MAKE_ZONES.get(self.zone, f"https://{self.zone}.make.com/api/v2" if not self.zone.startswith("http") else self.zone)
        
        env_team = os.getenv("MAKE_TEAM_ID")
        self.team_id = team_id or (int(env_team) if env_team and env_team.isdigit() else None)
        
        env_org = os.getenv("MAKE_ORGANIZATION_ID")
        self.organization_id = organization_id or (int(env_org) if env_org and env_org.isdigit() else None)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute authenticated HTTP request against Make API v2."""
        if not self.api_token:
            raise ValueError("Make API Token is missing. Set MAKE_API_TOKEN in environment or pass to client.")

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if params:
            query_str = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            if query_str:
                url = f"{url}?{query_str}"

        headers = {
            "Authorization": f"Token {self.api_token.strip()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "MakeApiClient-Finnova/1.0"
        }

        data_bytes = None
        if body is not None:
            data_bytes = json.dumps(body).encode("utf-8")

        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method.upper())

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                content_type = resp.headers.get("Content-Type", "")
                resp_data = resp.read().decode("utf-8")
                if "application/json" in content_type and resp_data:
                    return json.loads(resp_data)
                return {"status": resp.status, "data": resp_data}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            try:
                err_json = json.loads(err_body)
                raise RuntimeError(f"Make API Error [{e.code}]: {err_json.get('message', err_body)}")
            except Exception:
                raise RuntimeError(f"Make API Error [{e.code}]: {err_body}")
        except Exception as e:
            raise RuntimeError(f"Make API Request Failed: {str(e)}")

    # -------------------------------------------------------------------------
    # 1. User & Account Info
    # -------------------------------------------------------------------------
    def get_me(self) -> Dict[str, Any]:
        """Retrieve current authenticated user and roles."""
        return self._request("GET", "/users/me")

    def list_organizations(self) -> Dict[str, Any]:
        """List accessible organizations."""
        return self._request("GET", "/organizations")

    def list_teams(self, organization_id: Optional[int] = None) -> Dict[str, Any]:
        """List accessible teams."""
        org_id = organization_id or self.organization_id
        params = {"organizationId": org_id} if org_id else None
        return self._request("GET", "/teams", params=params)

    # -------------------------------------------------------------------------
    # 2. Scenarios Management
    # -------------------------------------------------------------------------
    def list_scenarios(
        self,
        team_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        limit: int = 50,
        name_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List scenarios for a given team."""
        t_id = team_id or self.team_id
        if not t_id and not self.organization_id:
            # Auto-detect team
            teams_res = self.list_teams()
            teams = teams_res.get("teams", [])
            if teams:
                t_id = teams[0].get("id")
                self.team_id = t_id

        params: Dict[str, Any] = {
            "pg[limit]": limit,
            "pg[sortDir]": "desc"
        }
        if t_id:
            params["teamId"] = t_id
        elif self.organization_id:
            params["organizationId"] = self.organization_id
        if is_active is not None:
            params["isActive"] = str(is_active).lower()
        if name_filter:
            params["name"] = name_filter

        res = self._request("GET", "/scenarios", params=params)
        return res.get("scenarios", [])

    def get_scenario(self, scenario_id: int) -> Dict[str, Any]:
        """Get scenario details."""
        res = self._request("GET", f"/scenarios/{scenario_id}")
        return res.get("scenario", res)

    def run_scenario(
        self,
        scenario_id: int,
        data: Optional[Dict[str, Any]] = None,
        responsive: bool = True
    ) -> Dict[str, Any]:
        """
        Execute / trigger a Make.com scenario on demand.
        Endpoint: POST /scenarios/{scenarioId}/run
        """
        body: Dict[str, Any] = {}
        if data:
            body["data"] = data
        if responsive:
            body["responsive"] = True
        return self._request("POST", f"/scenarios/{scenario_id}/run", body=body)

    def get_scenario_logs(self, scenario_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent execution logs for a scenario."""
        params = {"pg[limit]": limit, "pg[sortDir]": "desc"}
        res = self._request("GET", f"/scenarios/{scenario_id}/logs", params=params)
        return res.get("scenarioLogs", [])

    # -------------------------------------------------------------------------
    # 3. Webhooks & Direct Ingestion
    # -------------------------------------------------------------------------
    def list_hooks(self, team_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """List registered webhooks for a team."""
        t_id = team_id or self.team_id
        params = {"teamId": t_id} if t_id else None
        res = self._request("GET", "/hooks", params=params)
        return res.get("hooks", [])

    @staticmethod
    def send_webhook_payload(webhook_url: str, payload: Dict[str, Any]) -> bool:
        """
        Dispatch raw JSON payload directly to a Make.com Custom Webhook URL.
        Example: https://hook.eu1.make.com/xxxx-yyyy-zzzz
        """
        if not webhook_url:
            raise ValueError("Make Custom Webhook URL is empty.")

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data_bytes,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "MakeSyndicator-Finnova/1.0"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
                return 200 <= status < 300
        except Exception as e:
            print(f"❌ Failed to dispatch webhook to {webhook_url}: {e}")
            return False


# -----------------------------------------------------------------------------
# CLI Diagnostic & Utility Runner
# -----------------------------------------------------------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Make.com API v2 CLI Client")
    parser.add_argument("--test", action="store_true", help="Test authentication with Make API")
    parser.add_argument("--list-scenarios", action="store_true", help="List all scenarios in your team")
    parser.add_argument("--run-scenario", type=int, help="Trigger a specific scenario ID")
    parser.add_argument("--scenario-logs", type=int, help="View recent execution logs for a scenario")
    parser.add_argument("--list-hooks", action="store_true", help="List all webhooks")
    parser.add_argument("--webhook-url", type=str, help="Make.com custom webhook URL to send test payload to")
    parser.add_argument("--zone", type=str, default=os.getenv("MAKE_ZONE", "eu1"), help="Make zone (eu1, eu2, us1, us2)")

    args = parser.parse_args()

    token = os.getenv("MAKE_API_TOKEN")
    client = MakeApiClient(api_token=token, zone=args.zone)

    if args.webhook_url:
        print(f"📡 Sending test ping payload to Make.com Webhook: {args.webhook_url}")
        test_payload = {
            "event": "ping",
            "message": "Hello from Finnova Make API Client",
            "timestamp": "now"
        }
        success = MakeApiClient.send_webhook_payload(args.webhook_url, test_payload)
        print(f"{'✅ Webhook delivered successfully' if success else '❌ Webhook delivery failed'}")
        return

    if not token:
        print("⚠️ MAKE_API_TOKEN environment variable is not set.")
        print("💡 You can generate an API Token in Make.com -> Profile -> API -> Create API Token.")
        print("💡 Make API Reference: https://developers.make.com/api-documentation")
        sys.exit(1)

    if args.test:
        print(f"🔍 Testing Make API connection ({client.base_url})...")
        try:
            me = client.get_me()
            user = me.get("user", me)
            print("✅ Successfully authenticated with Make API!")
            print(f"👤 Name: {user.get('name')}")
            print(f"📧 Email: {user.get('email')}")
            print(f"🏢 Timezone: {user.get('timezone')}")
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            sys.exit(1)

    if args.list_scenarios:
        print("📋 Fetching scenarios from Make.com...")
        try:
            scenarios = client.list_scenarios()
            print(f"✅ Found {len(scenarios)} scenario(s):")
            for sc in scenarios:
                status = "🟢 Active" if sc.get("isActive") else "⚪ Inactive"
                print(f"  • [{sc.get('id')}] {sc.get('name')} — {status} (Folder: {sc.get('folderPath', 'Root')})")
        except Exception as e:
            print(f"❌ Error fetching scenarios: {e}")

    if args.run_scenario:
        print(f"🚀 Triggering scenario ID: {args.run_scenario}...")
        try:
            res = client.run_scenario(args.run_scenario)
            print("✅ Scenario triggered successfully:")
            print(json.dumps(res, indent=2))
        except Exception as e:
            print(f"❌ Failed to run scenario: {e}")

    if args.scenario_logs:
        print(f"📜 Fetching execution logs for scenario ID: {args.scenario_logs}...")
        try:
            logs = client.get_scenario_logs(args.scenario_logs)
            print(f"✅ Retrieved {len(logs)} log entries:")
            for l in logs:
                print(f"  • [{l.get('id')}] Status: {l.get('status')} | Duration: {l.get('duration')}ms | Operations: {l.get('operations')}")
        except Exception as e:
            print(f"❌ Failed to get logs: {e}")

    if args.list_hooks:
        print("🎣 Fetching Webhooks...")
        try:
            hooks = client.list_hooks()
            print(f"✅ Found {len(hooks)} webhook(s):")
            for h in hooks:
                print(f"  • [{h.get('id')}] {h.get('name')} (Type: {h.get('type')})")
        except Exception as e:
            print(f"❌ Error fetching webhooks: {e}")


if __name__ == "__main__":
    main()
