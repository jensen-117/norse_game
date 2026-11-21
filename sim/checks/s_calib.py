"""Calibration rooms in the browser: load the sweep's elite 4, room 2, with two Trash adds, Auto it to the end, and
check the record names the room (calib_gap.py reads it)."""
import json, sys, os
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__)); from s_smoke import serve
HERE = os.path.dirname(os.path.abspath(__file__))

def run():
    srv, port = serve(os.path.join(HERE, "..", "..", "fight_lab")); bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
        errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
        p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        p.goto(f"http://127.0.0.1:{port}/index.html")
        p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=180000)
        p.select_option("#speed", "0")
        p.select_option("#calshape", "elite:4"); p.select_option("#caladd", "Trash"); p.fill("#calno", "2")
        p.click("#calload"); p.wait_for_timeout(100)
        cards = p.text_content("#packcards")
        if "Calibration: elite 4 +2 Trash, room 2" not in cards: bad.append(("cards", cards[:160]))
        p.click("#auto")
        p.wait_for_function("Screen.state && Screen.state.phase === 'over' && !Screen.debug.busy", timeout=120000)
        rec = p.evaluate("Lab.call('record')")
        if rec.get("calib") != dict(kind="elite", budget=4, add="Trash", room=2, where="Wildwood"): bad.append(("record", rec.get("calib")))
        open(os.path.join(HERE, "page_calib.jsonl"), "w").write(json.dumps(rec) + "\n")
        b.close()
    srv.shutdown()
    if errs: bad.append(("page errors", errs[:3]))
    print("FAIL" if bad else "PASS", bad); return not bad
if __name__ == "__main__": sys.exit(0 if run() else 1)
