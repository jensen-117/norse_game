"""Step 7a: the page's Auto fights (Pyodide, wasm32) recorded, for native replay."""
from playwright.sync_api import sync_playwright
import json, sys, time
OUT = "/home/claude/sim/checks/page_auto.jsonl"
HABS = ["Barrow", "Wildwood", "Rapids", "Biome: Mire", "Biome: Ashfield", "Biome: Eldhall", "Biome: Vatnhall", "Biome: Natthall"]
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
    errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    p.goto("http://127.0.0.1:8765/index.html")
    p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=120000)
    p.select_option("#speed", "0")
    n = 0; t0 = time.time(); out = open(OUT, "w")
    for seed in range(1, 7):
        for hab in HABS:
            p.fill("#seed", str(seed * 37 + len(hab))); p.dispatch_event("#seed", "change")
            p.click("#rollparty"); p.wait_for_timeout(50)
            p.select_option("#hab", hab)
            p.fill("#elevel", str(26 + seed * 2)); p.fill("#budget", str(5 + seed % 5)); p.dispatch_event("#budget", "change"); p.dispatch_event("#elevel", "change")
            p.click("#rollpack"); p.wait_for_timeout(50)
            if p.is_disabled("#auto"): print("skip", seed, hab); continue
            p.click("#auto")
            p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=120000)
            rec = p.evaluate("Lab.call('record')"); rec["hab"] = hab
            out.write(json.dumps(rec) + "\n"); n += 1
    print(n, "fights", round(time.time() - t0), "s; errors:", errs[:3])
    b.close()
