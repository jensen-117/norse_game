"""Lab run check (Nov 24): boot the page, start a run, play every room on Auto (resting everyone at the camp), and
check the run's track, the camp and the end. Saves a screenshot of the camp for a look.
    python3 sim/checks/s_run.py [path/to/fight_lab] [screenshot.png]"""
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
            p.select_option("#speed", "0"); p.select_option("#kit", "3"); p.select_option("#runadd", ""); p.fill("#runno", "2")
            p.click("#runstart"); p.wait_for_timeout(100)
            seen = []
            for _ in range(8):
                track = p.text_content("#runtrack")
                if "The run is won" in track or "The run ends" in track: break
                if p.query_selector("text=Break camp"):
                    seen.append("camp")
                    if shot: p.screenshot(path=shot, full_page=False)
                    p.click("text=Break camp"); p.wait_for_timeout(100); continue
                if p.is_enabled("#runnext"): p.click("#runnext"); p.wait_for_timeout(100); continue
                p.click("#auto"); p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=180000)
                p.wait_for_timeout(300); seen.append(p.evaluate("Screen.state.winner"))
            track = p.text_content("#runtrack"); b.close()
            if errs: return f"FAIL: page errors {errs[:3]}"
            ok = ("The run is won" in track or "The run ends" in track) and ("camp" in seen or "The run ends" in track)
            return ("PASS" if ok else "FAIL") + f": {seen} | {track[-160:]}"
    finally: srv.shutdown()

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "..", "fight_lab"))
    out = run_check(folder, sys.argv[2] if len(sys.argv) > 2 else None); print(out); sys.exit(0 if out.startswith("PASS") else 1)
