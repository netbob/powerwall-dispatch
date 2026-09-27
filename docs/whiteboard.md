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

## 2. Adaptive overnight reserve (2026-09-26)

**Status:** raised during the Sep 26 evening watch — 43% SoC at 7:43 PM projected to land ~21% by morning, kissing #4's static 20% reserve after a deficit day (15.3 kWh solar vs 18.8 kWh home).

**Problem:** #4's 20% reserve is one number for every night. On deficit days (clouds, haze, laundry) the house is forced onto grid imports before morning solar even though usable energy sits below 20%. On strong days the reserve is never threatened. A static reserve either wastes streaks or wastes resilience — it can't do both jobs.

**Proposal:** set the overnight reserve conditionally:
- Deficit day + clear tomorrow's forecast + no storm risk → 10% reserve. Usable energy grows ~1.35 kWh ≈ 5 extra baseline hours.
- Any storm/PSPS risk → 20% or higher regardless of the day's balance (entry #1 overrides this entry).
- Normal day → 20% stays.

**Invariants:**
- The reserve gates grid-tied discharge depth, not outage discharge — in a real outage the battery gives everything regardless. The cost of 10% is thinner pre-outage positioning, not lost backup.
- Never below 10%: keeps a floor for measurement error and surprise loads.
- The manual version exists today: adjust #4's reserve in the Netzero app on deficit evenings. The automation is Phase 2.

**Open design questions:**
- Deficit definition: today's solar kWh vs home kWh? Net grid for the day? A threshold?
- Forecast source for "clear tomorrow" (ties to the Phase 2 forecasting work).
- Interaction with #5-winter: on low-solar winter days the midnight top-off already refills the battery, so adaptive reserve matters most in shoulder seasons.
