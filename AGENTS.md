# Repository Agent Rules & Continuous Integration Conventions

## 1. Continuous Integration & Pre-Flight Gatekeeper
* Before any code is pushed to production or merged into `main`, `pytest tests/test_autopost_guard.py` must pass cleanly (100%).
* If any script fails compilation or emits a syntax error, the automated runner must halt immediately and notify/dispatch automated healing.

## 2. Python & Publishing Scripting Conventions
* **Australian Timezone Enforcement:** All datetime logging, article generation timestamps, and dynamic calculations MUST explicitly use the Australian timezone (`Australia/Melbourne` or a strict `UTC+10` / `UTC+11` timedelta offset).
* Never rely on naive `datetime.now()` without an explicit timezone parameter, as GitHub Actions runners operate on native UTC.
* **Escaped CSS in F-Strings:** When generating HTML/CSS inside Python f-strings, all native CSS braces (e.g., `@keyframes`, inline JavaScript objects like `window.scrollTo({{...}})`) MUST use escaped double braces `{{` and `}}`.

## 3. Article Content & Layout Standards
* Every published article must contain at least 200–300+ words of value-dense financial/technical analysis.
* Column 2 Layout: Card 1 must be the MFAA-accredited Principal Broker (R Bakshi) profile card; Card 2 must be the multi-point highlights accordion.
* Local Melbourne suburban corridors (Western, Northern, Eastern, Bayside) must be naturally integrated for local SEO authority.

## 4. Agent Baniya: Fiscal Optimization & Daily Cost Audit
* Agent Baniya ([Baniya.md](file:///Volumes/Samsung%20SSD%202TB/03.%20Documents/GitHub/Blogs-Content/Baniya.md)) actively monitors and audits all AI credits (ElevenLabs, Cloudflare Workers AI) and cloud compute.
* Cost target is strictly $0.00/month for cloud operations, with paid ElevenLabs Pro credits safeguarded and rationed via two-tier routing.
* Daily audits must be executable via `python3 scripts/track_ai_credits.py` with results logged in Australian Timezone (`Australia/Melbourne`).
