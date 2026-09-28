# SYSTEM ENVIRONMENT PROFILE & NETZERO AUTOMATION MANIFESTO

## 1. LOCAL HARDWARE & TECHNICAL ENVIRONMENT
* **Location / Zip Code:** Clovis, CA 93619 (Extreme Central Valley summer heatwaves, frequently 100°F+)
* **Solar Generation Array:** 11 LONGi LR5-54HPB-410M panels totaling 4.51 kW peak capacity (Split: 3 East-facing, 8 West-facing).
* **Storage Solution:** 1x Tesla Powerwall 3 (13.5 kWh capacity, 11.5 kW inverter [Model: 1707000-XX-Y], 1841000-XX-Y (Gateway 3)).
* **Climate Control Hardware:** Honeywell Smart Thermostats, upstairs and downstairs zones + Electric heat pump.
* **Domestic Hot Water Hardware:** High-efficiency hybrid electric heat pump water heater.

## 2. INTERCONNECTION & REGULATORY STATUS (NEM 2.0 LEGACY)
* **PTO Date:** 2026-02-24
* **Annual True-Up Target:** 01-2027
* **Tariff Structure:** NEM 2.0 (grandfathered, verified with PG&E Solar Dept)
* **Credit Valuation Rule:** 1-to-1 retail net export credit, not subject to NEM 3.0
* **Retroactive Protection Cash Cushion:** $182.13 (March-July 2026 post-PTO overpayments)

## 3. HISTORICAL OUT-OF-POCKET CASH BASELINE (2026)
* **Jan:** $393.22 (2025-12-27 to 2026-01-27) -> *Gross winter heat pump space heating load*
* **Feb:** $241.23 (2026-01-28 to 2026-02-26) -> *Post-PTO transition phase onset*
* **Mar:** $91.01 (2026-02-27 to 2026-03-29) -> *Initial solar drop*
* **Apr:** $52.12 (2026-03-30 to 2026-04-27)
* **May:** $41.87 (2026-04-28 to 2026-05-27)
* **June:** $40.77 (2026-05-28 to 2026-06-25)
* **July:** $79.36 (2026-06-26 to 2026-07-26) -> *Extreme Valley summer heatwave peak*
* **August:**  -> *Transition phase: flat $24.60 base + residual pre-migration E-ELEC charges + $36.18 CA Climate Credit*
* **Sept-Dec (Projected):** $24.60 -> *Flat monthly minimum; all energy flows into True-Up credit bucket*

## 4. UTILITY RATE STRUCTURE (E-TOU-C, NEM 2.0)
* **Plan:** E-TOU-C. EV2-A switch canceled Sep 2026 — do not switch (~$155/yr worse; base charge dominates).
* **Base Services Charge:** $0.79343/day (~$23.80/month).
* **Summer (Jun 1–Sep 30), below baseline:** Peak $0.40 / Off-peak $0.32. Peak window 4–9 PM daily.
* **Winter (Oct 1–May 31), below baseline:** Peak $0.37 / Off-peak $0.29 (verify against tariff — PDF suggests 32¢ peak).

## 5. NETZERO AUTOMATION INVENTORY (reworked 2026-09-24)
* **#1 Morning Shift (9 AM, active):** 10% reserve, Self-Powered, solar-only exports, grid charging off.
* **#2 Mid-peak Guard (3 PM, paused → unpause Oct 1):** 100% reserve, Self-Powered, solar-only, grid charging off.
* **#3 Peak Self-Power (4 PM, active):** 10% reserve, Self-Powered, solar-only, grid charging off. (Export burst retired.)
* **#4 Overnight Run (9 PM, active):** 10% reserve, Self-Powered, solar-only, grid charging off.
* **#5 Winter Grid Top-Off (midnight, paused → unpause Oct 1):** 100% reserve, Savings, grid charging on when est. daily solar < 10 kWh.
* **#6 Winter Reset (6 AM, paused → unpause Oct 1):** 40% reserve, Savings, solar-only, grid charging off when est. daily solar < 10 kWh.
* **Strategy:** avoid grid imports; no export monetization (retired — nets ~$0 under NEM 2.0, adds cycle wear).

## 6. REVENUE LOGGING & TELEMETRY
* **Tool:** Google Apps Script + Google Sheets (logger v5.51, hourly).
* **Rates:** E-TOU-C below-baseline (summer 0.40/0.32; winter 0.37/0.29). Old rows may carry stale rate literals.
* **Energy math:** kW × interval_hours per row — never book instantaneous kW as hourly energy.
* **Sheet rule:** no manual ARRAYFORMULA in F3/G3 — collides with script row insertions, causes #REF!.
* **Phase 2:** 5-min CSV on the Pi (schema: logger/LOGGER_SPEC.md) + hourly Sheet rollup.
* **Sheet Formatting Rule:** Do not use manual ARRAYFORMULA in F3/G3 - collides with script's row-by-row insertions, causes #REF! crash
* **Verification Metric:** Column G (Net Grid Flow) strictly negative or zero during afternoon confirms export under NEM 2.0


