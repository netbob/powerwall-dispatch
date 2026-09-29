# Phase 2 Whiteboard

Open design surface for the programmatic dispatch layer. Entries are numbered in the order raised; the whiteboard session works them in priority order.

## 1. Storm/PSPS emergency response (2026-09-26)

**Status:** first entry. A manual runbook exists (see winter-strategy.md, Tier 4); this entry is the automation of it.

**Problem:** Today, storm response is a human watching forecasts and tapping through the Netzero app. El Niño winter 2026-27 (NOAA advisory Sep 10, 2026: >90% chance of a very strong event, California above-normal precipitation) makes this the highest-risk gap in the system.

**What the automation should do:**
- Watch: NWS alerts (high wind / red flag) for the home zone, PG&E PSPS notifications, Tesla Storm Watch state.
- On trigger: set 100% reserve, enable grid charging, top off from off-peak grid immediately.
- Stand down: restore the scheduled automation's reserve when warnings clear.
- Log every trigger, action, and stand-down with timestamps (decision proof).

**Invariants:**
- Never automate the thermostat.
- Grid charging only for defensive resilience, never arbitrage.
- A false positive (topping off before a storm that misses) costs a few cents and some cycles — acceptable. A false negative (no charge before a real outage) is the failure to minimize.

**Open design questions:**
- Alert sources and polling: which feeds, how often, and failure behavior when a feed is down.
- Interaction with #5-winter: the storm trigger overrides the 10 kWh solar estimate.
- Definition of "clear": all warnings expired, plus a grace period?

**Repeatable drill (2026-09-27):** the Tier 4 configuration is exercised as a pair of Netzero automations, kept paused except during drills:
- 4.1 "Test run", 5:00 AM: 100% reserve, Self-Powered, solar-only exports, grid charging enabled.
- 4.2 "Test reset", 5:20 AM: 10% reserve, Self-Powered, solar-only exports, grid charging disabled — restores the standing #4 rule.
- The 20-minute window sits at the overnight SoC low for maximum charge signal, well before sunrise so there's no solar confounding. Measured 2026-09-29: ~1.5 kW charge rate, 0.50 kWh delivered, ~$0.22, ~0.04 EFC.
- Pause both after the drill — they're daily automations.
- Measurement: Tesla app live view for the immediate engagement check; the 5:15 logger row as a mid-test snapshot; the 5-minute CSV for ramp time, sustained rate, SoC delta, and clean stop at reset.
- First drill: 2026-09-28. Results: _pending._

## 2. Adaptive overnight reserve (2026-09-26)

**Status:** live as the standing rule since Sep 27 — #4's reserve is 10% every night, not just deficit nights. Validated by the Sep 26–27 run: 10% carried the house 10+ hours on a deficit day (15.3 kWh solar vs 18.8 kWh home), first grid sip at 7:15 AM. The 20% default was storm insurance charged on calm nights; entry #1's trigger is the better mechanism for that.

**Problem:** #4's 20% reserve was one number for every night. On deficit days (clouds, haze, laundry) the house was forced onto grid imports before morning solar even though usable energy sat below 20%. A static 20% paid storm insurance on calm nights.

**Rule:**
- Standing overnight reserve: 10%. Covers the measured overnight (~0.42 kW × 10 h ≈ 31% of 13.5 kWh) with margin on any night starting above ~45%; on deeper deficit nights the failure mode is a small off-peak sip, which is cheap and acceptable.
- Storm/PSPS risk → raise per entry #1 (100% reserve + grid charging), which overrides this entry.
- Never below 10%: keeps a floor for measurement error and surprise loads.

**Invariants:**
- The reserve gates grid-tied discharge depth, not outage discharge — in a real outage the battery gives everything regardless. The cost of 10% is thinner pre-outage positioning, not lost backup.
- Precedent: #3 already runs a 10% reserve through the 4–9 PM peak window daily, so the evening has operated at 10% all along.

**Open design questions:**
- Should the reserve scale with the evening SoC (e.g. start below 40% → still 10%, since the failure mode is benign)?
- Forecast source for storm-risk detection (ties to entry #1).
- Interaction with #5-winter: on low-solar winter days the midnight top-off already refills the battery, so the 10% standing rule matters most in shoulder seasons.

## drill-results-2026-09-28

** - First drill 2026-09-28: 0 Wh — root cause was the installer-level "Grid Charging Restricted" flag (GAF Energy), not operating mode. Lifted remotely ~11:06 AM 2026-09-28; the Tesla app now has a Grid Charging No/Yes toggle. Re-drill 2026-09-29: PASSED — charging engaged in the first 5-min interval, sustained ~1.5 kW, 0.50 kWh delivered 05:00–05:20, SoC 38%→40%, clean stop at 4.2's 5:20 reset. Netzero's grid-charging flag flips the Tesla toggle end-to-end (No→Yes proven by behavior — charging is impossible at No). 4.1/4.2 paused after.

## drill-results-2026-09-29

Re-drill: **PASSED.** 4.1 fired at 5:00 AM in the exact Tier 4 runbook config (100% reserve, Self-Powered, solar-only exports, grid charging Enabled); 4.2 reset at 5:20. The 5-min CSV shows charging engaged in the first interval (05:00–05:05, 1,416 W grid→Powerwall) — effectively immediate. Sustained ~1.5 kW to the battery (~2.0 kW total grid import, remainder serving the home) across 4 intervals 05:00–05:20: 0.50 kWh delivered, SoC 38%→40%, clean stop at the 5:20 reset, zero grid→Powerwall after. Drill cost ~0.68 kWh ≈ $0.22 at 31.8¢. All three questions answered yes: (1) physical grid charging engages post-restriction, (2) Self-Powered supports it, (3) Netzero's flag drives the Tesla toggle end-to-end. Runbook implication: observed charge rate is only ~1.5 kW, so 10%→100% takes ~8 hours — a real Tier 4 charge needs serious lead time.
