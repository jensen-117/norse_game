"""Bein room check (Nov 25): boot the page, make the party, load Joseph's full house from the Bein room presets, fight
it on Auto, and check the pack's plan reached the log. Saves a screenshot of the fight's end.
    python3 sim/checks/s_pilot.py [path/to/fight_lab] [screenshot.png]"""
import os, sys
from s_smoke import serve
from playwright.sync_api import sync_playwright

def run_check(folder, shot=None):
    srv, port = serve(folder)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 1000})
            errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
            p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
            p.goto(f"http://127.0.0.1:{port}/index.html")
            p.wait_for_function("/^(Ready|Python didn't|The rules didn't|The art didn't)/.test(document.querySelector('#status').textContent)", timeout=180000)
            if not p.text_content("#status").startswith("Ready"): return "FAIL: " + p.text_content("#status")
            p.select_option("#speed", "0"); p.click("#mkparty"); p.wait_for_timeout(200)
            p.select_option("#pilotroom", "Full house (Joseph)"); p.click("#pilotload"); p.wait_for_timeout(200)
            cards = p.text_content("#packcards")
            p.click("#auto"); p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=240000)
            p.wait_for_timeout(300)
            if shot: p.screenshot(path=shot, full_page=False)
            text = p.text_content("body"); b.close()
            if errs: return f"FAIL: page errors {errs[:3]}"
            ok = "Fornbein" in cards and "beinseidr" in cards.lower() and ("points at" in text or "sets the pack" in text or "drives at" in text)
            return ("PASS" if ok else "FAIL") + f": {cards[:120]}"
    finally: srv.shutdown()

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "..", "fight_lab"))
    out = run_check(folder, sys.argv[2] if len(sys.argv) > 2 else None); print(out); sys.exit(0 if out.startswith("PASS") else 1)
