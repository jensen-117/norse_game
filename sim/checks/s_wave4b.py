"""Wave 4b in the browser: the Dagskald at kit leg 2, Kvad ordered through the real menu (key 4, then a click on the
Vasara), two rounds sung to her, and the page's record kept for native replay (check_page.py)."""
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
        for i, c in enumerate(("Dagskald", "Vasara", "Brennumar")): p.select_option(f"#cls{i}", c)
        p.select_option("#kit", "2"); p.click("#mkparty"); p.wait_for_timeout(100)
        cards = p.text_content("#partycards")
        for want in ("Kvad",):
            if want not in cards: bad.append(("party cards", want, cards[:200]))
        p.select_option("#hab", "Wildwood"); p.click("#rollpack"); p.wait_for_timeout(100)
        p.click("#start"); p.wait_for_function("Screen.state && Screen.state.phase === 'declare' && !Screen.debug.busy", timeout=60000)
        p.focus("body")
        for rnd in (2, 3):                                                           # sing twice: two verses
            p.keyboard.press("4"); p.wait_for_timeout(30)                             # Dagskald: Kvad, on the Vasara
            click_foe(p, "u.side === 'party' && u.name === 'Vasara'")
            p.keyboard.press("Enter"); p.wait_for_timeout(50); p.keyboard.press("Enter")   # the others: Halv strikes
            p.wait_for_function(f"(Screen.state.round >= {rnd} || Screen.state.phase !== 'declare') && !Screen.debug.busy", timeout=60000)
            if p.evaluate("Screen.state.phase") != "declare": break
        log = "\n".join(p.evaluate("Lab.call('record').log"))
        for want in ("sings Kvad: Song Vasara 1", "Vasara's Song (1) heals", "sings Kvad: Song Vasara 2"):
            if want not in log: bad.append(("missing in the log", want))
        rec = p.evaluate("Lab.call('record')")
        open(os.path.join(HERE, "page_wave4b.jsonl"), "w").write(json.dumps(rec) + "\n")
        b.close()
    srv.shutdown()
    if errs: bad.append(("page errors", errs[:3]))
    print("FAIL" if bad else "PASS", bad); return not bad
if __name__ == "__main__": sys.exit(0 if run() else 1)
