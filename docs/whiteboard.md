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
