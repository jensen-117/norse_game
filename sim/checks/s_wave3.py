"""Wave 3 in the browser: sheet heroes from the Kit choice, and Egga and Meditate ordered through the real menu
(keys 1-6 pick a move; a self move is used by picking it twice; Enter fights, filling the rest with Halv strikes)."""
import functools, http.server, socketserver, sys, threading, os
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__)); from s_smoke import serve
def run():
    srv, port = serve(os.path.join(os.path.dirname(__file__), "..", "..", "fight_lab")); bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
        errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
        p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        p.goto(f"http://127.0.0.1:{port}/index.html")
        p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=180000)
        p.select_option("#speed", "0")
        for i, c in enumerate(("Vasara", "Dagskald", "Brennumar")): p.select_option(f"#cls{i}", c); p.fill(f"#lvl{i}", "15")
        p.select_option("#kit", "1"); p.click("#mkparty"); p.wait_for_timeout(100)
        cards = p.text_content("#partycards")
        if "kit 1" not in cards or "Egga" not in cards: bad.append(("party cards", cards[:200]))
        p.select_option("#hab", "Barrow"); p.click("#rollpack"); p.wait_for_timeout(100)
        p.click("#start"); p.wait_for_function("Screen.state && Screen.state.phase === 'declare' && !Screen.debug.busy", timeout=60000)
        p.focus("body")
        for k in ("3", "3", "4", "4"): p.keyboard.press(k); p.wait_for_timeout(30)     # Vasara: Egga; Dagskald: Meditate
        p.keyboard.press("Enter"); p.wait_for_timeout(50); p.keyboard.press("Enter")     # Brennumar: filled with a Halv strike
        p.wait_for_function("(Screen.state.round >= 2 || Screen.state.phase !== 'declare') && !Screen.debug.busy", timeout=60000)   # next round, a Bonus Round, or the end
        log = "\n".join(p.evaluate("Lab.call('record').log"))
        for want in ("uses Egga, daring the foe", "meditates, recovering"):
            if want not in log: bad.append(("missing in the log", want))
        b.close()
    srv.shutdown()
    if errs: bad.append(("page errors", errs[:3]))
    print("FAIL" if bad else "PASS", bad); return not bad
if __name__ == "__main__": sys.exit(0 if run() else 1)
