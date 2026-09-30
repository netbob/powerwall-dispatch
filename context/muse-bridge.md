# muse-bridge.md — handoff notes between Muse (chat) and local Muse Code sessions

This file is the shared notes between Michael's two Muse instances. There is no
direct channel between them — this file (plus Michael) is the bridge.

- **Muse (chat)** — the personal agent in the Muse app. Long memory, data analysis,
  planning, ledger work. Cannot push to git or touch Michael's machines.
- **Muse Code (local)** — terminal sessions on Michael's machines (e.g. Dell,
  `c:\src\powerwall-dispatch`). Local hands: git push, running code, local edits.
  Same model family (Muse Spark), separate memory.

Both sides: read this file at session start. Append dated entries for anything the
other side needs to know. Keep entries short. Current state first, log below.

## Rules

- Public repo: NEVER put secrets, tokens, API keys, account numbers, service
  addresses, or personal identifiers in this file.
- Corrections are durable: don't re-litigate settled decisions (see decisions log).
- Michael's machines, repos, accounts, automations, and spreadsheet: look, don't
  touch, unless he asks. Destructive steps (force-push, history rewrite) are
  checklists he executes, never actions taken alone. He is the merge authority.
- Local sessions: keep approvals and sandbox on; never bypass them to move faster.
- When describing Netzero automations, use his numbers (#1–#6, 4.1/4.2).
- Ledger before verdict: show the numbers, then the conclusion.
- Netzero "Success" means the API calls returned clean, NOT that the Powerwall
  acted. The CSV is the authority on what physically happened.

## Current state (2026-09-30)

**Repo / Phase 2:** `github.com/netbob/powerwall-dispatch` (public) is the source of
truth and the sole Muse↔VS collaboration bridge. Phase 2 dispatch scaffold exists
(`src/` 15-min loop design, `config/`, `deploy/raspberry-pi/` + `deploy/digitalocean/`,
`logger/LOGGER_SPEC.md`); no controller built yet. Pi 4 is the dry-run host;
DigitalOcean droplet is for the proven build. Custom Python controller judged
feasible (Sep 29): Netzero REST API as actuator (account grandfathered, free),
NWS via api.weather.gov (free), solar forecast via Open-Meteo (free). Home
Assistant is optional, not required.

**Netzero automations (E-TOU-C, NEM 2.0):** #1 (9 AM), #3 (4 PM slot), #4 (9 PM)
active at 10% reserve, Self-Powered, solar-only exports. #2, #5-winter, #6 paused
until the **Sep 30 ~9:10 PM winter switchover** — then three Resume taps, no config
changes (verified Sep 29): #2 = 100% reserve, #5-winter = 100% reserve/Savings/grid
charging on (<10 kWh est. solar), #6 = 40% reserve/Savings/solar-only (<10 kWh).
#5-summer stays paused; old #3 export burst stays retired; 4.1/4.2 drill
automations stay paused. #1/#3/#4 unchanged by the switchover.

**Rates:** Summer 44.10¢ peak / 31.80¢ off-peak (bill-decoded, Jul bill line
structure). Winter 37¢/29¢ PROVISIONAL until the October bill shows the same
line structure. Tesla app rate plan corrected Sep 29 (2-decimal limits: .44/.32
summer, .37/.29 winter, sell = buy); Netzero dashboard reads the Powerwall
tariff, so it follows. Logger v5.52 live with bill-decoded summer rates.

**Grid charging:** Installer restriction lifted by GAF Sep 28; drill passed Sep 29
(0.50 kWh delivered, ~$0.22, clean stop). #5-winter's premise is functional for
the first time. Tesla Storm Watch vs. restriction still unverified.

**Muse Code on Dell:** Being evaluated as the git-push path. Chat-Muse's VM cannot
push (Secure Vault PAT has no vault-backed shell git credential — tooling gap,
filed with the Muse team Sep 28). A local `muse` session uses Michael's existing
GitHub auth and can push.

## Open threads

- [ ] Sep 30 ~9:10 PM: winter switchover — unpause #2, #5-winter, #6.
- [ ] #5-winter first midnight top-off verdict — needs morning 5-min CSV (chat Muse).
- [ ] October bill — settle winter rates (37¢/29¢ provisional).
- [ ] Green Button CSV, Feb 1 2026 → latest (pending his download).
- [ ] Logger: fix "dischargating" typo; decide restate-vs-boundary for old rows.
- [ ] Repo hygiene: reclone in Working Copy on iPad; `git update-index --chmod=+x
      hooks/pre-commit`; finalize Markdown sweep report.
- [ ] Muse Code: install on Dell, first session, prove the push path.

## Decisions log (settled — do not re-litigate)

- Stay on E-TOU-C / NEM 2.0; EV2-A switch cancelled (~$155/yr worse).
- Strategy: avoiding grid imports beats monetizing exports.
- Grid-charging arbitrage ruled out (~4.5¢/kWh net after losses); grid charging is
  defensive resilience only.
- Export-everything and fixed export bursts retired (nets ~$0 under NEM 2.0).
- Adaptive reserve: #4 stands at 10% overnight (validated Sep 26–27).
- Thermostat is MANUAL ONLY — never automate it. No pre-cooling to 70°F (headaches).
- Value export bursts by energy actually moved (SoC change), never by
  instantaneous kW booked as full-hour energy.

## Session log

### 2026-09-30 — bridge file created (chat Muse)
First entry. Awaiting Michael's review/merge and the first local Muse Code session.
Proposed first dogfood task for that session: commit and push this file.
