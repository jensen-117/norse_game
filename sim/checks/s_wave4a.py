"""Wave 4a in the browser: the starting three at kit leg 2, Naglskott and Sveda ordered through the real menu (keys
pick a move, then a click on a foe), and the page's record (its first round) kept for native replay (check_page.py)."""
import json, sys, os
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__)); from s_smoke import serve
HERE = os.path.dirname(os.path.abspath(__file__))

def keyfor(p, name):
    """The menu number of a move by its name, for the hero whose turn it is (Nov 21: kits shift when the Halv isn't in one)."""
    return str(p.evaluate("""(n) => { const o = Lab.call('options', Screen.debug.current);
        return [o.halv, ...o.moves, o.meditate].filter(Boolean).findIndex(m => m.name === n || m.shown === n) + 1; }""", name))

def click_foe(p):
    foe = p.evaluate("Screen.debug.units.find(u => u.side === 'enemy' && u.alive)")
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
        for i, c in enumerate(("Ullar", "Brennumar", "Vasara")): p.select_option(f"#cls{i}", c)
        p.select_option("#kit", "2"); p.click("#mkparty"); p.wait_for_timeout(100)
        cards = p.text_content("#partycards")
        for want in ("Naglskott", "Sveda"):
            if want not in cards: bad.append(("party cards", want, cards[:200]))
        p.select_option("#hab", "Wildwood"); p.click("#rollpack"); p.wait_for_timeout(100)
        p.click("#start"); p.wait_for_function("Screen.state && Screen.state.phase === 'declare' && !Screen.debug.busy", timeout=60000)
        p.focus("body")
        p.keyboard.press(keyfor(p, "Naglskott")); p.wait_for_timeout(30); click_foe(p)   # Ullar: Naglskott on a foe
        p.keyboard.press(keyfor(p, "Sveda")); p.wait_for_timeout(30); click_foe(p)       # Brennumar: Sveda on a foe
        p.keyboard.press("Enter"); p.wait_for_timeout(50); p.keyboard.press("Enter")  # Vasara: a Halv strike
        p.wait_for_function("(Screen.state.round >= 2 || Screen.state.phase !== 'declare') && !Screen.debug.busy", timeout=60000)
        log = "\n".join(p.evaluate("Lab.call('record').log"))
        for want in ("casts Naglskott", "casts Sveda"):
            if want not in log: bad.append(("missing in the log", want))
        rec = p.evaluate("Lab.call('record')")
        open(os.path.join(HERE, "page_wave4a.jsonl"), "w").write(json.dumps(rec) + "\n")
        b.close()
    srv.shutdown()
    if errs: bad.append(("page errors", errs[:3]))
    print("FAIL" if bad else "PASS", bad); return not bad
if __name__ == "__main__": sys.exit(0 if run() else 1)
