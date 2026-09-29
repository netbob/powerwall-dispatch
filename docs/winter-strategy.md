# Winter Strategy 2026–27

E-TOU-C, NEM 2.0. Winter season: Oct 1 – May 31. Peak 4–9 PM daily, year-round.
Winter rates (below baseline): peak $0.37 / off-peak $0.29 — the peak rate needs verification against the tariff (the PDF suggests 32¢).

## Why this winter is different

NOAA issued an El Niño Advisory on Sep 10, 2026: greater than 90% chance of a very strong event through fall/winter 2026-27, with California in the above-normal precipitation zone. For the Central Valley that means atmospheric-river rain, high-wind events, extended cloudy stretches, and elevated outage/PSPS risk. Expect multi-day near-zero solar stretches. The battery cannot be assumed to recover from solar day-to-day.

## The four tiers

### Tier 1 — Normal winter day
#2 (100% reserve at 3 PM), #6, #4 carry the 4–9 PM peak on solar-charged battery. Same playbook as September, winter automation set.

### Tier 2 — Low-solar forecast (est. daily solar < 10 kWh)
#5-winter tops off to 100% at midnight on 29¢ off-peak grid. The battery covers the next day's peak; overnight baseline may run on off-peak grid. Economics: roughly 5¢/kWh saved versus 37¢ peak imports after round-trip losses — the money is trivial, resilience is the point.

### Tier 3 — Fog/rain stretch (multi-day)
The battery stops being a solar store and becomes a nightly-charged peak shaver: top off every night at 29¢, shave every 4–9 PM peak, let cheap off-peak grid carry the rest. Do not expect solar recovery between days.

### Tier 4 — Emergency (storm / PSPS)
Manual action, runbook below. Full battery before the event, regardless of forecast or cost.

## Emergency runbook (implement before Oct 1)

Triggers — any one of these:
- NWS high wind warning or red flag warning for the Clovis/Fresno zone
- PG&E PSPS notification (text/email)
- Tesla Storm Watch activates in the app
- Your judgment — don't wait for a forecast's permission

Procedure (Netzero app, ~2 minutes):
1. Set backup reserve to 100%.
2. Turn grid charging ON.
3. Mode: Self-Powered. Charge to full from grid immediately — do not wait for midnight.
4. Stand down when warnings clear: restore the reserve called for by the active automation (#2/#4/#6).

Notes:
- Grid charging here is defensive resilience, not arbitrage. Cost is irrelevant in Tier 4.
- The thermostat is never automated — comfort rules still apply.
- If the outage hits mid-charge, whatever is in the battery is what you have.
- Drill-verified 2026-09-29: Netzero's grid-charging flag flips the Tesla toggle end-to-end; Energy Exports stays Solar throughout. Observed charge rate ~1.5 kW → 10%→100% takes ~8 hours, so start the charge the moment a trigger fires.

## Pre-Oct 1 checklist

- [ ] Unpause #2, #5-winter, #6 (reminder set: Sep 30, ~9:10 PM)
- [ ] Keep #5-summer paused; old #3 export burst stays retired
- [ ] Verify winter peak rate: 37¢ vs 32¢ against tariff or bill
- [x] Dry-run the Tier 4 procedure once before it's needed
- [ ] Confirm PG&E outage/PSPS notifications are on (text + email)

## Open questions

- How good is Netzero's "est. daily solar" estimate? A bad estimate tops off on sunny days (wasted cycles) or misses fog days. Phase 2 forecasting replaces this trigger.
- Should #5-winter target 100% or lower (e.g. 80%) on marginal calls? 100% is simple; 80% saves cycles. Undecided.
- Winter peak rate verification (above).
