import json, sys, os, base64, urllib.request, urllib.parse

with open('/Users/robinbakshi/Documents/GitHub/ezmortgagebroker/canva-session.json', 'r') as f:
    session = json.load(f)

if len(sys.argv) < 2:
    print("Usage: python3 scripts/exchange_canva_code.py <AUTHORIZATION_CODE_OR_CALLBACK_URL>")
    sys.exit(1)

raw_input = sys.argv[1]
if "code=" in raw_input:
    parsed = urllib.parse.urlparse(raw_input)
    query_dict = urllib.parse.parse_qs(parsed.query)
    code = query_dict.get('code', [''])[0]
else:
    code = raw_input.strip()

client_id = session['client_id']
client_secret = session['client_secret']
code_verifier = session['code_verifier']

# HTTP Basic Auth credentials
auth_str = f"{client_id}:{client_secret}"
b64_auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')

token_url = "https://api.canva.com/rest/v1/oauth/token"
payload = {
    "grant_type": "authorization_code",
    "code_verifier": code_verifier,
    "code": code
}

data = urllib.parse.urlencode(payload).encode('utf-8')
req = urllib.request.Request(token_url, data=data, method='POST')
req.add_header('Authorization', f'Basic {b64_auth}')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        print("Successfully generated Canva access tokens:")
        print(json.dumps(res_data, indent=2))
        with open('/Users/robinbakshi/Documents/GitHub/ezmortgagebroker/canva-tokens.json', 'w') as tf:
            json.dump(res_data, tf, indent=2)
        print("Saved tokens to canva-tokens.json and verified OAuth setup!")
except urllib.error.HTTPError as e:
    err_body = e.read().decode('utf-8')
    print(f"HTTP Error {e.code}: {err_body}")
except Exception as e:
    print(f"Error: {e}")