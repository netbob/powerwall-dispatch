# Logger spec — telemetry capture for Phase 2

Two consumers, one poll. The dispatch service polls the Netzero API every 5
minutes; that single GET fans out to both log sinks. No second poller, no
second auth session.

```
Netzero API ──5-min GET──▶ dispatch service (Pi)
                              ├──▶ local CSV      (durable, 5-min, full field set)
                              └──▶ GAS web app ──▶ Google Sheet (human view, hourly rollup)
```

## Sinks

| Sink | Cadence | Grain | Purpose |
|---|---|---|---|
| Local CSV (`logger/data/`) | every poll (5 min) | 5-min rows, full schema | durable machine record, event forensics, dispatch history |
| Google Sheet (existing logger sheet) | hourly | 1 hourly row per 12 polls | human scoreboard, rate/billing analysis, rolling-24h financial |

The Sheet keeps its current shape and column order (continuity with v5.51);
the hourly row is the sum/mean of its 12 polls plus the new forensics fields.

## Sign conventions (fixed — do not improvise)

- `grid_*`: **import positive, export negative.** (`grid_net_kw = import − export`.)
- `battery_kw`: **positive = charging, negative = dischargating.**
- Money: cost positive, export credit negative (matches v5.51 H/I columns).

## The energy-math rule (v5.51 lesson, now schema)

Every power column has an explicit per-interval energy sibling:
`energy_kwh = power_kw × (interval_minutes / 60)`. The interval is a column,
not an assumption. Instantaneous kW is never booked as energy.

## CSV schema (v1)

File: `logger/data/telemetry-YYYY-MM-DD.csv`, one file per local day
(America/Los_Angeles). Header row required. Append-only; rotate daily.

| # | Field | Type | Unit | Source | Notes |
|---|---|---|---|---|---|
| 1 | `timestamp` | ISO 8601 | — | poller | local time, e.g. `2026-09-25T14:15:04-07:00` |
| 2 | `interval_minutes` | int | min | config | 5; explicit so math never assumes |
| 3 | `solar_kw` | float | kW | Netzero telemetry | |
| 4 | `home_kw` | float | kW | Netzero telemetry | |
| 5 | `battery_pct` | float | % | Netzero telemetry | SoC at poll time |
| 6 | `battery_kw` | float | kW | Netzero telemetry | signed (see conventions) |
| 7 | `grid_net_kw` | float | kW | Netzero telemetry | signed (see conventions) |
| 8 | `grid_import_kw` | float | kW | Netzero telemetry | ≥ 0 |
| 9 | `grid_export_kw` | float | kW | Netzero telemetry | ≥ 0 |
| 10 | `inverter_mode` | string | — | Netzero config | e.g. `Autonomous` |
| 11 | `active_automation` | string | — | dispatch state | e.g. `4 Overnight Run`; `program` when Phase 2 owns it |
| 12 | `reserve_pct_effective` | float | % | Netzero config | the floor actually in force |
| 13 | `grid_charging_enabled` | bool | — | Netzero config | |
| 14 | `tou_window` | string | — | config/rates | `peak` (4–9 PM) or `offpeak` |
| 15 | `cost_rate_usd_kwh` | float | $/kWh | config/rates | below-baseline E-TOU-C: 0.40 peak / 0.32 offpeak (summer) |
| 16 | `solar_kwh` | float | kWh | computed | per-interval energy |
| 17 | `home_kwh` | float | kWh | computed | per-interval energy |
| 18 | `grid_import_kwh` | float | kWh | computed | per-interval energy |
| 19 | `grid_export_kwh` | float | kWh | computed | per-interval energy |
| 20 | `battery_charge_kwh` | float | kWh | computed | per-interval, ≥ 0 |
| 21 | `battery_discharge_kwh` | float | kWh | computed | per-interval, ≥ 0 |
| 22 | `interval_financial_usd` | float | $ | computed | `(import_kwh − export_kwh) × rate`; NEM 2.0 matched retail |
| 23 | `battery_throughput_kwh_cum` | float | kWh | computed | running total of charge+discharge; wear ledger |
| 24 | `flags` | string | — | dispatch/poller | `;`-separated: `storm_watch`, `outage`, `automation_fired`, `poll_gap`, … |
| 25 | `notes` | string | — | human/dispatch | free text, rare |

### Poll gaps

If a poll fails, do not fabricate a row. On recovery, write one row with
`flags` containing `poll_gap` and `notes` = `missed N polls`. Forensics must
be able to distinguish "nothing happened" from "we weren't watching."

## Sheet mirror (hourly rollup)

The Pi POSTs one JSON payload per hour to the GAS web app (`doPost`):

```json
{ "auth": "SHARED_SECRET", "rows": [ { "timestamp": "...", ... } ] }
```

Hourly row = sums for kWh/money columns, last-value for pct/mode/automation/
reserve/flags (concatenated if multiple), mean for kW columns. Column order
matches the v5.51 sheet with the new fields appended:

`Timestamp, Solar (kWh), Home (kWh), Grid Import (kWh), Grid Export (kWh),
Battery End (%), Battery kW avg, Inverter Mode, Active Automation,
Reserve (%), Grid Charging, TOU Window, Cost Rate, Hourly Financial,
Rolling 24H Financial, Throughput cum (kWh), Flags`

`Rolling 24H Financial` = sum of the last 24 hourly rows (same definition as
v5.51, now fed by clean hourly inputs).

## Retention

- CSV: keep 2 years local on the Pi; archive monthly to the droplet.
- Sheet: the long-term human archive (unchanged habit).

## Out of scope for the logger

Forecast fields, dispatch decision internals, candidate-vs-chosen actions —
those live in the dispatch service's own decision log (`src/dispatch/`),
not the telemetry record. The Sheet is for the human, not the machine.

## Continuity with v5.51

- v5.51's hourly Sheet rows remain valid history; new hourly rows extend the
  same columns (old stale `$0.49042` literals in pre-2026-09-24 rows are a
  known artifact, not restated).
- The 5-min CSV starts clean at Phase 2 trial cutover; it does not backfill.
