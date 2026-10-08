# Standing orders — powerwall-dispatch

## At session start
Before doing anything else, read:
- context/muse-bridge.md — current state, open threads, settled decisions
- context/MUSE.md — the owner's standing reference

Summarize the open threads back before starting work. If the bridge
names a task for this session, that is your assignment. When you finish,
append a dated entry to the bridge: what changed, the commit hash,
what is still open.

## Working rules
- You are the local executor; chat-Muse plans and prepares. The bridge
  file is the only channel between you — write to it.
- NEVER run git push. You run as a sandbox identity that cannot reach the
  owner's GitHub credentials; pushes fail and burn the session.
  Commit and stop. Michael reviews and pushes.
- If something looks wrong, record it in the bridge and stop.
  Do not improvise around a gap.

## Invariants
- Refer to Netzero automations by the owner's numbers (#1-#6, 4.1, 4.2).
- Netzero 'Success' means the API calls returned clean, not that the
  Powerwall acted. Verify outcomes in measurements, not statuses.
- Overnight backup reserve never goes below 10%.
- The thermostat is manual-only. Nothing you build touches it.

## Hard limit
This repo is PUBLIC. Never write secrets, tokens, API keys, account
numbers, or personal identifiers into any file — the bridge included.
