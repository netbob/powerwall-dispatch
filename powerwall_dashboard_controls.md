# Powerwall 3 Dashboard — `powerwall_dashboard_controls.py`

A small local web dashboard for a Tesla Powerwall 3, served from your own machine. Shows live readings and offers a guarded set of controls through the Netzero API. Python standard library only — no pip packages needed.

## What it does

- **Live readings:** solar, battery, home, and grid power, state-of-charge gauge, backup reserve, operating mode, grid-charging status, and energy exports.
- **Safe controls** (each change asks for confirmation before it is sent):
  - Backup reserve (0–100%)
  - Operating mode (Time-Based Control / Self-Powered / Backup Only)
  - Energy exports (Solar Only / Solar + Battery / Never)
  - Grid charging (Enabled / Disabled)
- **Deliberately excluded:** go off-grid and reconnect-to-grid controls.
- **Dark mode** toggle in the header — remembers your choice and follows your OS setting on first load.

## Requirements

- Python 3.10 or newer. No third-party packages.

## Setup — the two environment variables

The script reads its credentials from environment variables, so secrets never live in the code or the repo:

| Variable              | What it is             |
|-----------------------|------------------------|
| `NETZERO_API_TOKEN`   | Your Netzero API token |
| `NETZERO_SITE_ID`     | Your Netzero site ID   |

Optional: `DASHBOARD_PORT` (default `8080`).

**Windows** — persistent, and keeps the secret out of PowerShell command history. Use the GUI, not the command line:

> Settings → System → About → Advanced system settings → Environment Variables → **New** under "User variables"

Add both variables, then open a fresh terminal.

**Linux / macOS** (bash/zsh) — add to your shell startup file so they persist across sessions:

```sh
# ~/.bashrc or ~/.zshrc
export NETZERO_API_TOKEN="paste-token-here"
export NETZERO_SITE_ID="paste-site-id-here"
```

Then reload with `source ~/.bashrc` (or `source ~/.zshrc`).

Do not put these values in any file committed to git. This repo's `.gitignore` already excludes `.env` files and anything with `token` or `secret` in the name.

## Run it

Windows:

```powershell
python powerwall_dashboard_controls.py
```

Linux / macOS:

```sh
python3 powerwall_dashboard_controls.py
```

Then open <http://localhost:8080> in your browser.

## Polling

The server polls Netzero every 60 seconds (`POLL_SECONDS` near the top of the script). The page re-renders from the server's cached reading every 10 seconds.

## Security notes

- The server listens only on `127.0.0.1` (localhost) — it is not reachable from other machines on your network.
- The API token is used server-side only, in the `Authorization` header. It is never sent to the browser.
- The control endpoints have no login, which is why localhost-only binding matters: anyone able to reach the port could change Powerwall settings.
