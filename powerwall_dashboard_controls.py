#!/usr/bin/env python3
"""Powerwall 3 dashboard with safe Netzero controls.

Controls included:
  - Backup reserve
  - Operating mode
  - Energy exports
  - Grid charging

Controls excluded intentionally:
  - Go off-grid
  - Reconnect to grid

Requirements: Python 3.10+ only, no pip packages.
Run: python powerwall_dashboard_controls.py
Then open: http://localhost:8080

Credentials are read from Windows environment variables:
  NETZERO_API_TOKEN
  NETZERO_SITE_ID
"""
import json, os, threading, time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

TOKEN = os.environ.get("NETZERO_API_TOKEN", "")
SITE_ID = os.environ.get("NETZERO_SITE_ID", "")
PORT = int(os.environ.get("DASHBOARD_PORT", "8080"))
POLL_SECONDS = 60
API = "https://api.netzero.energy/api/v1"

state = {"error": "Waiting for first Netzero reading", "last_updated": None,
         "solar_power": 0, "battery_power": 0, "load_power": 0, "grid_power": 0,
         "percentage_charged": 0, "backup_reserve_percent": 0,
         "operational_mode": "unknown", "energy_exports": "unknown",
         "grid_charging": False, "grid_status": "Unknown"}
lock = threading.Lock()

def netzero(method="GET", payload=None):
    url = f"{API}/{SITE_ID}/config"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    body = None if payload is None else json.dumps(payload).encode()
    req = Request(url, data=body, headers=headers, method=method)
    with urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode())

def apply_reading(raw):
    live = raw.get("live_status", {})
    with lock:
        state.update({
            "solar_power": live.get("solar_power", 0),
            "battery_power": live.get("battery_power", 0),
            "load_power": live.get("load_power", 0),
            "grid_power": live.get("grid_power", 0),
            "percentage_charged": raw.get("percentage_charged", 0),
            "backup_reserve_percent": raw.get("backup_reserve_percent", 0),
            "operational_mode": raw.get("operational_mode", "unknown"),
            "energy_exports": raw.get("energy_exports", "unknown"),
            "grid_charging": raw.get("grid_charging", False),
            "grid_status": raw.get("grid_status", "Unknown"),
            "last_updated": datetime.now().isoformat(timespec="seconds"),
            "error": None,
        })

def poller():
    while True:
        try:
            apply_reading(netzero())
            print(f"[{datetime.now():%H:%M:%S}] refreshed")
        except Exception as exc:
            with lock: state["error"] = str(exc)
            print(f"[{datetime.now():%H:%M:%S}] read error: {exc}")
        time.sleep(POLL_SECONDS)

HTML = r'''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Powerwall 3 Monitor</title>
<style>
:root{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#24221f;background:#f5f1ed;--teal:#087f87;--orange:#bb5a37;--purple:#6257a4;--line:#e4ded7;--card:#fffdfa}*{box-sizing:border-box}body{margin:0;padding:28px 20px 60px}main{max-width:1060px;margin:auto}header{display:flex;justify-content:space-between;align-items:center;gap:18px;margin-bottom:30px;flex-wrap:wrap}h1{font-size:28px;margin:0;letter-spacing:-.04em}.sub{color:#7b7169;font-size:13px}.pill{border-radius:99px;padding:5px 11px;font-size:12px;background:#e4f2ea;color:#28804f}.pill.off{background:#fae6e2;color:#a13c2d}.intro{color:#756b63;font-size:14px;max-width:64ch;margin-bottom:26px}.flow,.reading,.battery,.controls{background:var(--card);border:1px solid var(--line);border-radius:16px}.flow{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding:34px 20px;margin-bottom:32px}.node{text-align:center}.icon{width:52px;height:52px;border-radius:14px;margin:0 auto 11px;display:grid;place-items:center;font-size:25px}.solar{background:#fff1d2;color:#c98500}.batt{background:#dff3f3;color:var(--teal)}.home{background:#fde6df;color:var(--orange)}.grid{background:#e8e6fa;color:var(--purple)}.value{font-size:23px;font-weight:650;font-variant-numeric:tabular-nums}.unit{font-size:12px;font-weight:400;color:#786f68}.label{font-size:13px;color:#887d74;margin-top:4px}.section{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:#8a7c72;margin:0 0 11px}.reading{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;overflow:hidden;margin-bottom:32px}.metric{padding:19px 20px;background:var(--card);border-right:1px solid var(--line)}.metric:last-child{border:0}.metric label{display:block;color:#8a7c72;font-size:12px;margin-bottom:7px}.metric strong{font-size:21px;font-variant-numeric:tabular-nums}.battery{display:grid;grid-template-columns:180px 1fr;gap:28px;align-items:center;padding:25px;margin-bottom:32px}.gauge{width:146px;height:146px;position:relative;margin:auto}.gauge svg{transform:rotate(-90deg)}.track{fill:none;stroke:#eee9e4;stroke-width:11}.fill{fill:none;stroke:var(--teal);stroke-width:11;stroke-linecap:round;transition:stroke-dashoffset .7s ease-out}.center{position:absolute;inset:0;display:grid;place-content:center;text-align:center}.soc{font-size:29px;font-weight:700;color:var(--teal)}.small{font-size:11px;color:#8a7c72}.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}.stat label{display:block;color:#8a7c72;font-size:12px;margin-bottom:3px}.stat strong{font-size:15px}.controls{padding:25px;margin-bottom:32px}.control-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px 24px}.control label{display:block;font-size:13px;font-weight:600;margin-bottom:7px}.control small{display:block;color:#8a7c72;font-size:11px;margin-top:5px}select,input{font:inherit;width:100%;min-height:42px;border:1px solid #d8d0c8;border-radius:9px;background:#fffdfa;padding:9px 11px;color:#2d2925}button{font:inherit;min-height:44px;border:0;border-radius:9px;background:var(--teal);color:#f8ffff;padding:10px 18px;font-weight:650;cursor:pointer;margin-top:20px}button:hover{filter:brightness(.94)}button:disabled{opacity:.55;cursor:wait}.notice{margin-top:14px;color:#746b64;font-size:13px;min-height:20px}.warning{background:#fff6e3;border:1px solid #f0d69c;border-radius:10px;padding:12px 14px;color:#72551a;font-size:12px;margin-bottom:18px}.error{background:#fae6e2;border:1px solid #e9b9b0;color:#9d3e31;padding:12px 14px;border-radius:10px;margin-bottom:20px;font-size:13px}@media(max-width:700px){body{padding:20px 14px 40px}.flow{grid-template-columns:repeat(2,1fr);gap:26px 8px}.reading{grid-template-columns:repeat(2,1fr)}.metric{border-bottom:1px solid var(--line)}.battery{grid-template-columns:1fr;text-align:center}.stats{width:100%}.control-grid{grid-template-columns:1fr}}@media(max-width:430px){.reading{grid-template-columns:1fr}.stats{grid-template-columns:1fr}}.theme-btn{min-height:0;margin:0 0 0 10px;padding:7px 13px;border-radius:99px;border:1px solid var(--line);background:transparent;color:inherit;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap}html[data-theme="dark"]{color:#e9e2d9;background:#131110;--line:#38322c;--card:#1d1a17}html[data-theme="dark"] .flow,html[data-theme="dark"] .reading,html[data-theme="dark"] .battery,html[data-theme="dark"] .controls,html[data-theme="dark"] .metric{background:var(--card)}html[data-theme="dark"] .sub,html[data-theme="dark"] .intro,html[data-theme="dark"] .label,html[data-theme="dark"] .metric label,html[data-theme="dark"] .small,html[data-theme="dark"] .stat label,html[data-theme="dark"] .control small,html[data-theme="dark"] .notice,html[data-theme="dark"] .unit,html[data-theme="dark"] .section{color:#a89c90}html[data-theme="dark"] select,html[data-theme="dark"] input{background:#26211d;border-color:#4a4239;color:#e9e2d9}html[data-theme="dark"] .track{stroke:#38322c}html[data-theme="dark"] .warning{background:#2b2313;border-color:#6b5426;color:#e8c87a}html[data-theme="dark"] .error{background:#331a16;border-color:#7a3b32;color:#f0a49a}html[data-theme="dark"] .pill{background:#1d3a2f;color:#7fd6a4}html[data-theme="dark"] .pill.off{background:#3d211d;color:#ef9a8d}
</style></head><body><main>
<header><div><h1>Powerwall 3</h1><span class="sub">Netzero-connected monitor</span></div><div><span id="status" class="pill">Connecting</span><span class="sub" id="updated" style="margin-left:8px">Waiting</span><button id="themeToggle" class="theme-btn" type="button">Dark mode</button></div></header>
<p class="intro">Live system readings plus a guarded control panel. Changes are previewed here before they are sent to Netzero.</p><div id="error"></div>
<div class="flow"><div class="node"><div class="icon solar">☼</div><div class="value" id="solar">-- <span class="unit">kW</span></div><div class="label">Solar</div></div><div class="node"><div class="icon batt">▣</div><div class="value" id="battery">-- <span class="unit">kW</span></div><div class="label">Battery</div><div class="sub" id="batteryState">--</div></div><div class="node"><div class="icon home">⌂</div><div class="value" id="home">-- <span class="unit">kW</span></div><div class="label">Home</div></div><div class="node"><div class="icon grid">♜</div><div class="value" id="grid">-- <span class="unit">kW</span></div><div class="label">Grid</div><div class="sub" id="gridState">--</div></div></div>
<div class="section">Live readings</div><div class="reading"><div class="metric"><label>Solar output</label><strong id="mSolar">-- W</strong></div><div class="metric"><label>Home load</label><strong id="mHome">-- W</strong></div><div class="metric"><label>Battery</label><strong id="mBattery">-- W</strong></div><div class="metric"><label>Grid</label><strong id="mGrid">-- W</strong></div></div>
<div class="section">Battery status</div><div class="battery"><div class="gauge"><svg width="146" height="146" viewBox="0 0 146 146"><circle class="track" cx="73" cy="73" r="59"/><circle id="gfill" class="fill" cx="73" cy="73" r="59" stroke-dasharray="370.7" stroke-dashoffset="370.7"/></svg><div class="center"><span class="soc" id="soc">--%</span><span class="small">state of charge</span></div></div><div class="stats"><div class="stat"><label>Backup reserve</label><strong id="reserve">--</strong></div><div class="stat"><label>Mode</label><strong id="mode">--</strong></div><div class="stat"><label>Grid charging</label><strong id="charging">--</strong></div><div class="stat"><label>Energy exports</label><strong id="exports">--</strong></div></div></div>
<div class="section">Safe controls</div><div class="controls"><div class="warning"><strong>Review before applying.</strong> These controls can immediately change Powerwall behavior. Off-grid and reconnect controls are intentionally not included.</div><div class="control-grid"><div class="control"><label for="reserveInput">Backup reserve (%)</label><input id="reserveInput" type="number" min="0" max="100" step="1"><small>Use 0 to 100. A higher reserve protects more backup energy.</small></div><div class="control"><label for="modeInput">Operating mode</label><select id="modeInput"><option value="autonomous">Time-Based Control</option><option value="self_consumption">Self-Powered</option><option value="backup">Backup Only</option></select></div><div class="control"><label for="exportInput">Energy exports</label><select id="exportInput"><option value="pv_only">Solar Only</option><option value="battery_ok">Solar + Battery</option><option value="never">Never</option></select></div><div class="control"><label for="gridInput">Grid charging</label><select id="gridInput"><option value="false">Disabled</option><option value="true">Enabled</option></select></div></div><button id="apply" onclick="applyChanges()">Review and apply changes</button><div id="notice" class="notice"></div></div>
</main><script>
var themeKey='pw-theme';function applyTheme(t){document.documentElement.setAttribute('data-theme',t);var b=document.getElementById('themeToggle');if(b)b.textContent=t==='dark'?'Light mode':'Dark mode';try{localStorage.setItem(themeKey,t)}catch(e){}}(function(){var t=null;try{t=localStorage.getItem(themeKey)}catch(e){}if(t!=='dark'&&t!=='light')t=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';applyTheme(t);var b=document.getElementById('themeToggle');if(b)b.addEventListener('click',function(){applyTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark')})})();
const labels={autonomous:'Time-Based Control',self_consumption:'Self-Powered',backup:'Backup Only',pv_only:'Solar Only',battery_ok:'Solar + Battery',never:'Never'};
let current={};
function kw(w){return (Number(w||0)/1000).toFixed(1)}
function set(id,text){document.getElementById(id).textContent=text}
function render(d){current=d;const on=String(d.grid_status||'').toLowerCase().includes('active');const pill=document.getElementById('status');pill.textContent=on?'On Grid':'Off Grid';pill.className='pill '+(on?'':'off');set('solar',kw(d.solar_power)+' kW');set('battery',kw(Math.abs(d.battery_power))+' kW');set('home',kw(d.load_power)+' kW');set('grid',kw(Math.abs(d.grid_power))+' kW');set('batteryState',d.battery_power<-50?'Charging':d.battery_power>50?'Discharging':'Idle');set('gridState',d.grid_power>50?'Importing':d.grid_power<-50?'Exporting':'Not importing');set('mSolar',Math.round(d.solar_power)+' W');set('mHome',Math.round(d.load_power)+' W');set('mBattery',Math.round(d.battery_power)+' W');set('mGrid',Math.round(d.grid_power)+' W');const soc=Number(d.percentage_charged||0);set('soc',soc+'%');document.getElementById('gfill').setAttribute('stroke-dashoffset',(370.7*(1-soc/100)).toFixed(1));set('reserve',d.backup_reserve_percent+'%');set('mode',labels[d.operational_mode]||d.operational_mode);set('charging',d.grid_charging?'Enabled':'Disabled');set('exports',labels[d.energy_exports]||d.energy_exports);set('updated',d.last_updated?'Updated '+new Date(d.last_updated).toLocaleTimeString():'Waiting');document.getElementById('reserveInput').value=d.backup_reserve_percent;document.getElementById('modeInput').value=d.operational_mode;document.getElementById('exportInput').value=d.energy_exports;document.getElementById('gridInput').value=String(d.grid_charging)}
async function poll(){try{const r=await fetch('/api/data');const d=await r.json();render(d);document.getElementById('error').innerHTML=d.error?'<div class="error">API error: '+escapeHtml(d.error)+'</div>':''}catch(e){document.getElementById('error').innerHTML='<div class="error">Dashboard connection lost. Retrying...</div>'}}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
async function applyChanges(){const reserve=Number(document.getElementById('reserveInput').value);if(!Number.isInteger(reserve)||reserve<0||reserve>100){set('notice','Backup reserve must be a whole number from 0 to 100.');return}const payload={backup_reserve_percent:reserve,operational_mode:document.getElementById('modeInput').value,energy_exports:document.getElementById('exportInput').value,grid_charging:document.getElementById('gridInput').value==='true'};const summary=`Reserve ${reserve}%, ${labels[payload.operational_mode]}, ${labels[payload.energy_exports]}, grid charging ${payload.grid_charging?'enabled':'disabled'}`;if(!confirm('Apply this change to your Powerwall?\n\n'+summary+'\n\nThis will be sent to Netzero immediately.'))return;const btn=document.getElementById('apply');btn.disabled=true;set('notice','Applying change...');try{const r=await fetch('/api/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const out=await r.json();if(!r.ok)throw new Error(out.error||'Netzero rejected the change');render(out);set('notice','Applied successfully at '+new Date().toLocaleTimeString()+'.')}catch(e){set('notice','Not applied: '+e.message)}finally{btn.disabled=false}}
poll();setInterval(poll,10000);
</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, obj):
        data=json.dumps(obj).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def do_GET(self):
        if self.path=='/api/data':
            with lock: self.send_json(200, state.copy())
        elif self.path in ('/','/index.html'):
            data=HTML.encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        else:self.send_error(404)
    def do_POST(self):
        if self.path!='/api/config':self.send_error(404);return
        try:
            length=int(self.headers.get('Content-Length','0')); payload=json.loads(self.rfile.read(length))
            allowed={'backup_reserve_percent','operational_mode','energy_exports','grid_charging'}
            if set(payload)-allowed: raise ValueError('Unsupported setting requested')
            reserve=payload.get('backup_reserve_percent')
            if not isinstance(reserve,int) or not 0<=reserve<=100: raise ValueError('Backup reserve must be an integer from 0 to 100')
            if payload.get('operational_mode') not in {'autonomous','self_consumption','backup'}: raise ValueError('Invalid operating mode')
            if payload.get('energy_exports') not in {'pv_only','battery_ok','never'}: raise ValueError('Invalid energy export mode')
            if not isinstance(payload.get('grid_charging'),bool): raise ValueError('Grid charging must be true or false')
            result=netzero('POST',payload);apply_reading(result);self.send_json(200,state.copy())
        except HTTPError as e:
            self.send_json(e.code,{'error':f'Netzero returned HTTP {e.code}'})
        except Exception as e:self.send_json(400,{'error':str(e)})
    def log_message(self,*args):pass

def main():
    if not TOKEN or not SITE_ID:
        raise SystemExit('Set NETZERO_API_TOKEN and NETZERO_SITE_ID in Windows User environment variables first.')
    threading.Thread(target=poller,daemon=True).start();server=HTTPServer(('127.0.0.1',PORT),Handler)
    print(f'Powerwall dashboard with safe controls: http://localhost:{PORT}')
    print(f'Netzero polling every {POLL_SECONDS}s. Press Ctrl+C to stop.')
    try:
        import webbrowser;webbrowser.open(f'http://localhost:{PORT}')
    except Exception:pass
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()

if __name__=='__main__':main()
