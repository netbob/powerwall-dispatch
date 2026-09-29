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
- The 20-minute window sits at the overnight SoC low for maximum charge signal (~1.5 kWh, ~$0.50, ~0.1 EFC), well before sunrise so there's no solar confounding.
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

** First drill: 2026-09-28. Result: no charging. Both automations fired and reported Success (4.1 at 5:00:22, 4.2 at 5:20:27), but the 5-minute CSV shows zero grid→Powerwall flow in every interval 00:00–06:25 — engagement never happened, delivered energy 0 Wh. Suspected cause: Self-Powered mode does not honor grid charging; #5-winter's Savings mode is the known-good path. Note: the battery hit the 10% reserve at ~4:37 AM, so grid was already covering the home before the window. Action: re-drill with 4.1 in Savings mode; then fix the Tier 4 runbook charge step to match.