# powerwall-dispatch

Programmatic dispatch layer for a Tesla Powerwall 3 (PG&E, E-TOU-C, NEM 2.0).
Phase 1: Netzero scheduled automations. Phase 2: forecast-driven control via API.

## Layout

- `docs/` — strategy, rate plan, automation inventory, API research, findings
  - `docs/findings/` — dated analysis write-ups (export autopsy, baselines, rate comps)
- `pseudocode/` — dispatch logic worked out on the whiteboard, before code
- `src/` — the real thing
  - `netzero_client/` — Netzero REST API client (primary actuator)
  - `tesla_client/` — Tesla Fleet API fallback
  - `dispatch/` — decision engine (15-min loop: read → decide → act on change)
  - `config/` — site config, rates, reserves
- `deploy/raspberry-pi/` — trial deployment (Pi 400: dry-run first, then live)
- `deploy/digitalocean/` — production deployment (droplet: uptime)
- `logger/` — telemetry capture spec (`LOGGER_SPEC.md`): 5-min CSV on the Pi + hourly Sheet rollup; v5.51 Apps Script sheet logger lives on until cutover
- `analysis/` — one-off analysis scripts (rate comparisons etc.)
- `context/` — MUSE.md: everything the assistant needs to know, maintained by hand

## Hardware map

| Role | Machine |
|---|---|
| Dev / whiteboard | Dell Inspiron 7640 2-in-1 |
| Trial | Raspberry Pi 400 (4 GB) — dry-run soak, then live |
| Prod | DigitalOcean droplet — systemd service, uptime |

## Status

- [x] Phase 1: Netzero automations (Self-Powered daytime as of 2026-09-24)
- [x] Phase 2 API research (`docs/phase2-api-research.md`)
- [ ] Whiteboard: dispatch strategy → `pseudocode/`
- [ ] Pi trial build
- [ ] Droplet cutover
