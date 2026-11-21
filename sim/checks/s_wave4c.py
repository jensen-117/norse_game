"""Wave 4c in the browser: the Skurmar at kit leg 2: Knyta ordered through the real menu (key 3 twice: a self move is
used by picking it again), then Kuling spending the knot (key 4 twice: an All move), and the record kept for replay."""
import json, sys, os
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__)); from s_smoke import serve
HERE = os.path.dirname(os.path.abspath(__file__))

def click_foe(p, who="u.side === 'enemy' && u.alive"):
    foe = p.evaluate(f"Screen.debug.units.find(u => {who})")
    cv = p.query_selector("#screen"); cv.scroll_into_view_if_needed(); box = cv.bounding_box(); k = box["width"] / 320
    p.mouse.click(box["x"] + foe["cx"] * k, box["y"] + foe["cy"] * k); p.wait_for_timeout(50)

def run():
    srv, port = serve(os.path.join(HERE, "..", "..", "fight_lab")); bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
        errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
        p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        p.goto(f"http://127.0.0.1:{port}/index.html")
        p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=180000)
        p.select_option("#speed", "0")
        for i, c in enumerate(("Skurmar", "Vasara", "Brennumar")): p.select_option(f"#cls{i}", c)
        p.select_option("#kit", "2"); p.click("#mkparty"); p.wait_for_timeout(100)
        cards = p.text_content("#partycards")
        for want in ("Knyta", "Kuling"):
            if want not in cards: bad.append(("party cards", want, cards[:200]))
        p.select_option("#hab", "Wildwood"); p.click("#rollpack"); p.wait_for_timeout(100)
        p.click("#start"); p.wait_for_function("Screen.state && Screen.state.phase === 'declare' && !Screen.debug.busy", timeout=60000)
        p.focus("body")
        for rnd, k in ((2, "3"), (3, "4")):                                          # Knyta, then Kuling
            for _ in range(2): p.keyboard.press(k); p.wait_for_timeout(30)
            p.keyboard.press("Enter"); p.wait_for_timeout(50); p.keyboard.press("Enter")   # the others: Halv strikes
            p.wait_for_function(f"(Screen.state.round >= {rnd} || Screen.state.phase !== 'declare') && !Screen.debug.busy", timeout=60000)
            if p.evaluate("Screen.state.phase") != "declare": break
        log = "\n".join(p.evaluate("Lab.call('record').log"))
        for want in ("ties the wind: 1 knot", "uses Kuling"):
            if want not in log: bad.append(("missing in the log", want))
        rec = p.evaluate("Lab.call('record')")
        open(os.path.join(HERE, "page_wave4c.jsonl"), "w").write(json.dumps(rec) + "\n")
        b.close()
    srv.shutdown()
    if errs: bad.append(("page errors", errs[:3]))
    print("FAIL" if bad else "PASS", bad); return not bad
if __name__ == "__main__": sys.exit(0 if run() else 1)
