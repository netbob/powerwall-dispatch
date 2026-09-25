# Phase 2 API Research: Programmatic Powerwall Control

**Date:** 2026-09-25 (overnight research for morning strategy session)
**Goal:** Replace Netzero's scheduled automations with forecast-driven programmatic dispatch
(e.g., export only on proven surplus, laundry-aware scheduling).
**Verdict up front:** Use the **Netzero REST API**. Details below.

---

## 1. Netzero REST API

**Docs (official, verified):** https://docs.netzero.energy/docs/tesla/API

### Endpoints
Base: `https://api.netzero.energy/api/v1/{site_id}/config`

- `GET /config` — current configuration **plus live status**: `backup_reserve_percent`,
  `operational_mode`, `energy_exports`, `grid_charging`, `storm_watch`, `percentage_charged`,
  `grid_status`, and `live_status` (solar/battery/load/grid power in watts, wall connectors).
- `POST /config` — set any combination in one request:
  - `backup_reserve_percent`: 0–100, or `"preserve"` (pins reserve at current SoC —
    handy while the dryer runs)
  - `operational_mode`: `autonomous` (Savings/TBC), `self_consumption` (Self-Powered),
    `backup`
  - `energy_exports`: `pv_only`, `battery_ok`, `never`
  - `grid_charging`: `true` / `false`
  - `storm_watch`: `true` / `false`
  - `off_grid_status`: `go_off_grid` / `reconnect_grid` (requires subscription + Powerwall pairing)

This covers **every knob the current six automations use** (mode, reserve, exports,
grid charging) plus live telemetry for decision-making. One endpoint does it all.

### Auth
- Bearer token + energy site ID, both found in the Netzero app under
  **Settings > Developer API**. No app registration, no OAuth dance, no key hosting.
- Token is revocable/regenerable in-app.

### Cost / access
- **Free** for existing accounts. Per the docs: *"The Developer API requires a Netzero
  subscription for accounts created from July 2026 on."* Your account predates that,
  so you should be grandfathered — verify under Settings > Developer API.
- Non-commercial use only (fine for a homeowner).

### Rate limits
- **None published.** Community integrations (e.g., the Home Assistant integration at
  https://github.com/kilroyd/powerwall_control) poll it routinely with no reported
  throttling. Treat as "be reasonable" — a 5–15 min control loop is well within norms.

### Gotchas (Tesla-side, apply to both paths)
- Backup reserve of **81–99% is rejected by Tesla and resets to 80%** (documented in
  Netzero's docs; corroborated by pypowerwall: cloud APIs cap reserve at 80%).
  Your automations only use 10/20/40/50/100%, so unaffected.

### Community proof
- HA integration: https://github.com/kilroyd/powerwall_control
- API skill writeup with curl/Python examples:
  https://github.com/monty72/hermes-skills/blob/HEAD/devops/netzero-powerwall-api/SKILL.md

---

## 2. Tesla Fleet API

**Docs (official):** https://developer.tesla.com/docs/fleet-api/endpoints/energy

### Energy endpoints (all under `https://fleet-api.prd.na.vn.cloud.tesla.com/api/1`)
Reads: `GET energy_sites/{id}/live_status`, `/site_info`, `/calendar_history`,
`/telemetry_history`, `/products`
Writes:
- `POST energy_sites/{id}/operation` — mode (`autonomous` / `self_consumption`)
- `POST energy_sites/{id}/backup` — backup reserve %
- `POST energy_sites/{id}/storm_mode` — Storm Watch on/off
- `POST energy_sites/{id}/grid_import_export` — grid charging / export control
- `POST energy_sites/{id}/time_of_use_settings` — push utility tariff structures
  (can update the Powerwall's rate plan programmatically — genuinely useful)
- `POST energy_sites/{id}/off_grid_vehicle_charging_reserve`

Capability-wise it's a superset of Netzero's API (adds tariff push + history), minus
Netzero's one-call-does-everything convenience.

### Auth (the friction)
1. Create account at developer.tesla.com, register an application → client_id/secret.
2. Generate an EC keypair; host the public key at
   `https://<your-domain>/.well-known/appspecific/com.tesla.3p.public-key.pem`
   — **requires a domain you control with valid HTTPS** (GitHub Pages works).
3. One-time partner registration: `POST /api/1/partner_accounts` with a
   client-credentials partner token binding your domain.
4. OAuth authorization-code flow as yourself with scopes
   `openid offline_access energy_device_data energy_cmds`; store the refresh token
   and rotate access tokens (8h lifetime) in your controller.

This is a real afternoon of setup versus Netzero's "copy two strings from the app."

### Cost (verified from https://developer.tesla.com/docs/fleet-api/billing-and-limits)
- Pay-per-use with a **$10/month per-account discount**.
- Commands: **$1 / 1,000** · Data requests: **$1 / 500** · (wakes/streaming N/A for energy).
- **Billing limit defaults to 0 — you must add a payment method and raise it, or the
  app is auto-disabled.**
- Modeled for your controller:
  - ~6 settings commands/day → 180/mo → **$0.18/mo** (trivial)
  - `live_status` polling every 5 min → 8,640/mo → **$17.28/mo** — blows past the
    $10 discount (~$7.28 out of pocket)
  - Polling every 15 min → **$5.76/mo** (inside the discount, effectively free)
  - Polling hourly → **$1.44/mo**
- So: affordable, but **polling cadence is a cost lever you must design around**.

### Rate limits (official)
60 realtime-data req/min, 30 device commands/min (per device, per account).
A home controller will never touch these.

### Gotchas
- **80% reserve cap** via cloud APIs (same Tesla limitation as Netzero path).
- **Storm Watch via Fleet API is disputed:** Tesla's own scope table says `energy_cmds`
  covers storm mode and community wrappers list a `storm_mode` endpoint, but a
  July-2026 integration author reports it's unavailable/not working via Fleet API.
  Unresolved — test before depending on it.
- **Owner API (the old unofficial one) is dying:** vehicle endpoints deprecated
  mid-2026; energy endpoints "appear unaffected at this time" per community reports,
  but no guarantees. Don't build on it — Fleet API is the supported path.
  (Source: https://github.com/oznetmaster/teslapowerwallcrestrondriver)
- Per-endpoint pricing categories for energy reads weren't individually verified;
  `live_status` is assumed to bill as a data request — confirm in the developer
  dashboard before settling on a poll cadence.

---

## 3. Comparison & recommendation

| | Netzero REST API | Tesla Fleet API |
|---|---|---|
| Setup effort | Copy token + site ID from app (~5 min) | Dev account + domain + key hosting + partner registration + OAuth (~1 afternoon) |
| Cost | Free (grandfathered pre-Jul-2026) | ~$0–7/mo depending on poll cadence; $10/mo discount; payment method required |
| Control knobs | Mode, reserve, exports, grid charging, Storm Watch, off-grid toggle | Same + tariff push + richer history |
| Telemetry | Live power + SoC in the same GET | live_status, site_info, calendar history |
| Rate limits | Unpublished; community use is unthrottled | Published and generous |
| Failure mode | Depends on a small third party (terms already tightened once, Jul 2026) | First-party; you're the customer |
| Auth maintenance | Static token, rotate manually | Refresh-token rotation in code |

**Recommendation: build Phase 2 on the Netzero REST API.**

Why:
1. It exposes every control your six automations use today, through one endpoint,
   with live telemetry in the same call — exactly the read/decide/act loop a
   forecast-driven dispatcher needs.
2. Setup is five minutes and it's free. The Fleet API's afternoon of
   domain/key/OAuth/billing setup buys you nothing you need at this stage.
3. Your decision logic (surplus forecasting, laundry awareness) lives in *your*
   code either way — the API is just the actuator. Porting actuators later is cheap.

**Hedge:** keep the Fleet API as the documented fallback. If Netzero ever degrades
the API or changes terms again, the port is mechanical: same knobs, different
base URL and auth. Worth one line in the design doc, not worth building twice now.

**Not recommended:** the old Tesla Owner API (being deprecated), and local-gateway
control via pypowerwall (needs gateway password + LAN presence; fragile vs. cloud).

---

## 4. Minimal viable Phase 2 setup (Netzero path)

1. **Host:** any always-on machine — your Dell via Task Scheduler, a Raspberry Pi,
   or a small cloud VM. (This Linux VM works for prototyping.)
2. **Secrets:** `NETZERO_API_TOKEN` + `SITE_ID` in environment variables or the
   Secure Vault — never in code or logs.
3. **Loop (every 15 min):**
   - `GET /config` → SoC, solar, load, grid, current mode/reserve
   - **Decide** (start as 1:1 ports of automations #1–#6, then add):
     - *Surplus export:* only set `energy_exports=battery_ok` when SoC = 100% AND
       forecast evening load < projected stored energy (the dynamic version of the
       retired burst)
     - *Laundry-aware:* on laundry days, delay heavy-load expectation; optionally
       `"preserve"` the reserve during the 1–3 PM dryer window
     - *Winter:* replicate #5/#6 logic against a solar forecast (Open-Meteo is free)
       instead of fixed dates
   - **Act:** `POST /config` only when the decision differs from current state
     (idempotent, minimal churn)
4. **Safety rails:** never set reserve < 10% outside 4–9 PM; cap POSTs at a sane
   rate; log every decision + API response (your logger sheet already does the
   telemetry half); dry-run mode that logs decisions without POSTing, for soak
   testing — steal this pattern from
   https://github.com/echang793/franklinwh-advisor (dry-run → compare → go-live).
5. **Keep Netzero's scheduled automations as the fallback** during the soak:
   run the controller in dry-run for a week, diff its decisions against what the
   schedules did, then cut over one automation at a time.

---

## 5. Verified vs. uncertain

**Verified (official docs read directly):**
- Netzero endpoints, parameters, auth method, subscription-from-Jul-2026 rule —
  https://docs.netzero.energy/docs/tesla/API
- Fleet API energy endpoint list, OAuth scopes, billing/limits/rate limits —
  https://developer.tesla.com/docs/fleet-api/ (energy, authentication/overview,
  billing-and-limits)

**Second-hand but credible (community, multiple sources):**
- Fleet API setup friction (domain + key hosting + partner registration)
- $10 discount / $1-per-1k-commands pricing in practice
- Owner API deprecation in progress; energy endpoints currently working
- 80% reserve cap on cloud APIs

**Uncertain — verify before depending on:**
- Netzero's unpublished rate limits / long-term API stability
- Whether your specific Netzero account needs a subscription for API access
  (docs say pre-Jul-2026 accounts are exempt; confirm in-app)
- Storm Watch actually working via Fleet API (conflicting reports)
- Exact Fleet API pricing category of energy `live_status` polls
