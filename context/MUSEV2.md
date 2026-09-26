# SYSTEM ENVIRONMENT PROFILE & NETZERO AUTOMATION MANIFESTO

*Auto-generated from memory.json on 2026-08-18 22:03*

## 1. LOCAL HARDWARE & TECHNICAL ENVIRONMENT
* **Location / Zip Code:** Clovis, CA 93619 (Extreme Central Valley summer heatwaves, frequently 100°F+)
* **Solar Generation Array:** 11 LONGi LR5-54HPB-410M panels totaling 4.51 kW peak capacity (Split: 3 East-facing, 8 West-facing).
* **Storage Solution:** 1x Tesla Powerwall 3 (13.5 kWh capacity, 11.5 kW inverter [Model: 1707000-XX-Y], 1841000-XX-Y (Gateway 3)).
* **Climate Control Hardware:** Honeywell Smart Thermostats, upstairs and downstairs zones + Electric heat pump.
* **Domestic Hot Water Hardware:** High-efficiency hybrid electric heat pump water heater.
* **Edge Infrastructure:** Windows 11 Pro, GitHub Desktop, Google Apps Script.
* **Decommissioned Hardware:** Bitaxe Gamma 602 ASIC miner, Raspberry Pi 400 Stratum pool server.

## 2. INTERCONNECTION & REGULATORY STATUS (NEM 2.0 LEGACY)
* **PTO Date:** 2026-02-24
* **Annual True-Up Target:** 02-24 (First settlement: 2027-02-24)
* **Account Number:** \*\*\*REDACTED\*\*\*
* **Interconnection Reference Number:** \*\*\*REDACTED\*\*\*
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

## 4. INVIOLABLE USER COMFORT & OPERATIONAL PREFERENCES
* **Daytime Temperature Rule:** 77°F during the day.
* **Nighttime Rule:** A/C off at night.
* **Thermostat Control Style:** manual only, not automated.
* **Thermal Schedule:** On 8:30-9:00 AM (timed so solar is active for compressor startup surge); off 9:00 PM (extended to 10:00 PM on extreme heat nights).
* **ELIMINATED STRATEGY:** Daytime pre-cooling to 70°F - causes headaches, permanently rejected, do not suggest

## 5. UTILITY RATE STRUCTURE
**Cancelled EV2-A (Residential Home Charging) under NEM 2.0** (switched 2026-08)
* **Base Services Charge:** $24.60/month (0.79343/day). Target net bill: low 40s.
* **Peak Window ($0.54/kWh):** 4:00 PM - 9:00 PM.
* **Part Peak Window ($0.43/kWh):** 3:00-4:00 PM and 9:00 PM-12:00 AM.
* **Off Peak Window ($0.23/kWh):** 12:00 AM - 3:00 PM.

## 6. NETZERO APP AUTOMATION TIMELINE
1. **Rule 1 - Morning Shift (9:00 AM):**
   * *Settings:* Mode: `Self-Powered` | Backup Reserve: `40%`
   * *Objective:* Battery smooths daytime 77°F A/C spikes exceeding solar generation, drawing zero or low-cost ($0.23) off-peak grid power
3. **Rule 3 - Peak Discharge (4:00 PM):**
   * *Settings:* Mode: `Self-Powered` | Backup Reserve: `10%`
   * *Objective:* Battery carries full household load and exports aggressively at premium $0.40 peak price
4. **Rule 4 - Overnight Run (9:00 PM):**
   * *Settings:* Mode: `Savings` | Backup Reserve: `20%`
   * *Objective:* Late-night cushion; carries load through $0.43 part-peak hour if A/C runs to 10 PM, then drops to cover dark-house baseline overnight

## 7. REVENUE LOGGING & TELEMETRY TRACKING
* **Tool:** Google Apps Script + Google Sheets
* **Active Cost Formula:**
  ```javascript
  =IF(AND(HOUR(A{row})>=16, HOUR(A{row})<21), 0.54, IF(OR(HOUR(A{row})=15, HOUR(A{row})>=21), 0.43, 0.23))
  ```
* **Sheet Formatting Rule:** Do not use manual ARRAYFORMULA in F3/G3 - collides with script's row-by-row insertions, causes #REF! crash
* **Verification Metric:** Column G (Net Grid Flow) strictly negative or zero during afternoon confirms export under NEM 2.0
