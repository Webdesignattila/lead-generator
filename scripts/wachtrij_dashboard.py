"""
wachtrij_dashboard.py: het Wachtrij-blok voor http://localhost:8080.

Los starten (als er nog niets op 8080 draait):
    python scripts/wachtrij_dashboard.py        →  open http://localhost:8080

In een bestaand FastAPI-dashboard op 8080 (twee regels):
    from scripts.wachtrij_dashboard import router as wachtrij_router, WACHTRIJ_BLOK_HTML
    app.include_router(wachtrij_router)
    # en zet WACHTRIJ_BLOK_HTML in de HTML van je dashboardpagina

Endpoints: GET /wachtrij/status · POST /wachtrij/start · POST /wachtrij/stop · POST /wachtrij/reset
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from urllib.parse import urlparse

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = os.path.dirname(HIER)
sys.path.insert(0, HIER)
import nacht_worker as nw  # noqa: E402

router = APIRouter(prefix="/wachtrij", tags=["wachtrij"])


def _alleen_lokaal(request: Request) -> None:
    """Blokkeert POST-verzoeken die van een andere website komen (CSRF)."""
    herkomst = request.headers.get("origin") or request.headers.get("referer")
    if herkomst and urlparse(herkomst).hostname not in ("localhost", "127.0.0.1", "::1"):
        raise HTTPException(403, "Alleen vanaf localhost")


@router.get("/status")
def status():
    st = nw.lees_json(nw.STATUS, {}) or {}
    pid = nw.draait_al()
    st["draait"] = bool(pid)
    wachtrij = nw.lees_json(nw.WACHTRIJ, {"taken": []}) or {"taken": []}
    return JSONResponse({"status": st, "taken": wachtrij.get("taken", [])})


@router.post("/start")
def start(request: Request, reset: bool = False):
    _alleen_lokaal(request)
    if nw.draait_al():
        return {"ok": False, "melding": "De wachtrij draait al."}
    wachtrij = nw.lees_json(nw.WACHTRIJ, {"taken": []}) or {"taken": []}
    open_taken = [t for t in wachtrij.get("taken", []) if t.get("status", "wachtend") in ("wachtend", "bezig")]
    if not open_taken and not reset:
        return {"ok": False, "melding": "Geen wachtende taken. Klik eerst op 'Opnieuw klaarzetten'."}
    cmd = [sys.executable, os.path.join(HIER, "nacht_worker.py")] + (["--reset"] if reset else [])
    opties = dict(cwd=BASIS, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                  stderr=subprocess.DEVNULL)
    if os.name == "nt":  # los van het dashboard, zonder zwart venster
        opties["creationflags"] = (subprocess.CREATE_NEW_PROCESS_GROUP
                                   | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW)
    else:
        opties["start_new_session"] = True
    proc = subprocess.Popen(cmd, **opties)
    return {"ok": True, "melding": f"Wachtrij gestart (PID {proc.pid})."}


@router.post("/stop")
def stop(request: Request):
    _alleen_lokaal(request)
    open(nw.STOPBESTAND, "w").write(nw.nu())
    return {"ok": True, "melding": "Stopverzoek verstuurd; de worker stopt netjes."}


@router.post("/reset")
def reset(request: Request):
    _alleen_lokaal(request)
    if nw.draait_al():
        return {"ok": False, "melding": "Kan niet resetten terwijl de wachtrij draait."}
    wachtrij = nw.lees_json(nw.WACHTRIJ, {"taken": []}) or {"taken": []}
    for t in wachtrij.get("taken", []):
        t.update(status="wachtend", resultaat=None, gestart=None, klaar=None)
    nw.schrijf_json(nw.WACHTRIJ, wachtrij)
    return {"ok": True, "melding": "Alle taken staan weer klaar."}


WACHTRIJ_BLOK_HTML = r"""
<section id="wq" aria-labelledby="wq-titel">
<style>
  #wq{--wq-bg:#0f172a;--wq-kaart:#111c33;--wq-rand:#1e2a44;--wq-tekst:#e2e8f0;--wq-zacht:#94a3b8;
      --wq-accent:#6366f1;--wq-ok:#22c55e;--wq-fout:#ef4444;--wq-bezig:#f59e0b;
      font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--wq-tekst);
      background:var(--wq-bg);border:1px solid var(--wq-rand);border-radius:16px;padding:20px;
      max-width:880px;margin:24px auto;box-sizing:border-box}
  #wq *{box-sizing:border-box}
  #wq h2{margin:0;font-size:18px;font-weight:650}
  #wq .wq-kop{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin-bottom:14px}
  #wq .wq-staat{display:inline-flex;align-items:center;gap:8px;color:var(--wq-zacht);font-size:13px}
  #wq .wq-dot{width:9px;height:9px;border-radius:50%;background:var(--wq-zacht)}
  #wq .wq-dot.aan{background:var(--wq-ok);box-shadow:0 0 0 4px rgb(34 197 94 / .18)}
  #wq .wq-knoppen{display:flex;flex-wrap:wrap;gap:8px}
  #wq button{font:inherit;font-weight:600;border:1px solid var(--wq-rand);background:var(--wq-kaart);
      color:var(--wq-tekst);padding:9px 14px;border-radius:10px;cursor:pointer;
      transition:transform .15s ease,background .15s ease,border-color .15s ease}
  #wq button:hover{transform:translateY(-1px);border-color:#334155}
  #wq button:active{transform:translateY(1px)}
  #wq button.wq-primair{background:var(--wq-accent);border-color:var(--wq-accent);color:#fff}
  #wq button:disabled{opacity:.45;cursor:not-allowed;transform:none}
  #wq .wq-balk{height:8px;border-radius:99px;background:var(--wq-rand);overflow:hidden;margin:6px 0 2px}
  #wq .wq-balk>i{display:block;height:100%;width:0;background:var(--wq-accent);transition:width .4s ease}
  #wq .wq-sub{color:var(--wq-zacht);font-size:12px;min-height:18px}
  #wq ol{list-style:none;margin:14px 0;padding:0;display:grid;gap:6px}
  #wq li{display:grid;grid-template-columns:22px 1fr auto;gap:10px;align-items:start;
      background:var(--wq-kaart);border:1px solid var(--wq-rand);border-radius:10px;padding:10px 12px}
  #wq li .wq-res{grid-column:2/4;color:var(--wq-zacht);font-size:12px;word-break:break-word}
  #wq .wq-label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;padding:2px 8px;border-radius:99px;background:var(--wq-rand);color:var(--wq-zacht)}
  #wq .klaar .wq-label{background:rgb(34 197 94 / .15);color:var(--wq-ok)}
  #wq .fout .wq-label{background:rgb(239 68 68 / .15);color:var(--wq-fout)}
  #wq .bezig .wq-label{background:rgb(245 158 11 / .15);color:var(--wq-bezig)}
  #wq pre{margin:0;max-height:220px;overflow:auto;background:#020617;border:1px solid var(--wq-rand);
      border-radius:10px;padding:10px 12px;font:12px/1.5 ui-monospace,Consolas,monospace;color:#cbd5e1;white-space:pre-wrap}
  #wq .wq-melding{font-size:13px;color:var(--wq-zacht);margin-top:10px;min-height:20px}
  @media (prefers-reduced-motion:reduce){#wq *{transition:none!important}}
</style>
  <div class="wq-kop">
    <div>
      <h2 id="wq-titel">Nacht-wachtrij</h2>
      <span class="wq-staat"><span class="wq-dot" id="wq-dot"></span><span id="wq-staat">laden…</span></span>
    </div>
    <div class="wq-knoppen">
      <button class="wq-primair" id="wq-start" type="button">▶ Start wachtrij</button>
      <button id="wq-stop" type="button">■ Stop</button>
      <button id="wq-reset" type="button">↺ Opnieuw klaarzetten</button>
    </div>
  </div>
  <div class="wq-balk" aria-hidden="true"><i id="wq-balk"></i></div>
  <div class="wq-sub" id="wq-sub"></div>
  <ol id="wq-taken"></ol>
  <pre id="wq-log" aria-label="Logboek">Nog geen logboek.</pre>
  <div class="wq-melding" id="wq-melding" role="status"></div>
<script>
(() => {
  const $ = id => document.getElementById(id);
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const icoon = {wachtend:"○", bezig:"◐", klaar:"✔", fout:"✖", overgeslagen:"–"};
  let snelTot = 0;
  async function post(pad){
    snelTot = Date.now() + 15000;
    try{ const r = await fetch("/wachtrij/"+pad,{method:"POST"}); const j = await r.json();
         $("wq-melding").textContent = j.melding || j.detail || ""; }
    catch(e){ $("wq-melding").textContent = "Dashboard niet bereikbaar: "+e; }
    ververs();
  }
  $("wq-start").onclick = () => post("start");
  $("wq-stop").onclick  = () => post("stop");
  $("wq-reset").onclick = () => post("reset");
  async function ververs(){
    let d; try{ d = await (await fetch("/wachtrij/status",{cache:"no-store"})).json(); }catch(e){ return; }
    const st = d.status || {}, taken = d.taken || [];
    const klaar = taken.filter(t => ["klaar","fout","overgeslagen"].includes(t.status)).length;
    $("wq-dot").classList.toggle("aan", !!st.draait);
    $("wq-staat").textContent = st.draait
      ? `bezig: taak ${st.huidige_taak?.nummer ?? "?"} van ${st.huidige_taak?.van ?? "?"}`
      : (st.klaar ? `klaar sinds ${st.klaar}` : "staat stil");
    $("wq-start").disabled = !!st.draait; $("wq-reset").disabled = !!st.draait; $("wq-stop").disabled = !st.draait;
    const tv = st.taak_voortgang;
    const binnen = tv && tv.totaal ? tv.gedaan / tv.totaal : 0;
    const huidig = st.draait && taken.some(t => t.status === "bezig") ? 1 : 0;
    const pct = taken.length ? Math.round(((klaar + (huidig ? binnen : 0)) / taken.length) * 100) : 0;
    $("wq-balk").style.width = pct + "%";
    $("wq-sub").textContent = `${klaar}/${taken.length} taken afgerond · ${pct}%` +
      (st.draait && st.huidige_taak ? ` · nu: ${st.huidige_taak.naam}` + (tv ? ` (${tv.gedaan}/${tv.totaal} ${tv.tekst||""})` : "") : "");
    $("wq-taken").innerHTML = taken.map(t => `
      <li class="${esc(t.status||"wachtend")}">
        <span aria-hidden="true">${icoon[t.status||"wachtend"]||"○"}</span>
        <span>${esc(t.naam || t.type)}</span>
        <span class="wq-label">${esc(t.status||"wachtend")}</span>
        ${t.resultaat ? `<span class="wq-res">${esc(t.resultaat)}</span>` : ""}
      </li>`).join("");
    if (st.log && st.log.length){ const p = $("wq-log"); const onder = p.scrollTop + p.clientHeight >= p.scrollHeight - 8;
      p.textContent = st.log.join("\n"); if (onder) p.scrollTop = p.scrollHeight; }
    clearTimeout(ververs.t); ververs.t = setTimeout(ververs, (st.draait || Date.now() < snelTot) ? 1500 : 6000);
  }
  ververs();
})();
</script>
</section>
"""

app = FastAPI(title="Mainframe – Webdesign Attila")
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return f"""<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mainframe Dashboard</title>
<style>body{{margin:0;background:#020617;color:#e2e8f0;font:15px/1.5 system-ui,"Segoe UI",sans-serif;padding:16px}}
h1{{max-width:880px;margin:16px auto 0;font-size:22px}}</style></head>
<body><h1>Mainframe · Webdesign Attila</h1>{WACHTRIJ_BLOK_HTML}</body></html>"""


if __name__ == "__main__":
    import uvicorn
    poort = int(os.getenv("DASHBOARD_POORT", "8080"))
    print(f"Dashboard: http://localhost:{poort}")
    uvicorn.run(app, host="127.0.0.1", port=poort)
