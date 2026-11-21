"""A03: the Enter-restart regression, exercised the way a player meets it. Click Fight with the mouse (the button
takes focus), then press Enter to fight the round, with no focus change, canvas click or other help from the test.
The fight must stay the same fight (its seed and id) while its round advances. Run against a folder:
    python3 sim/checks/s_focus.py [path/to/fight_lab]
Removing the page's blur() in startFight makes this fail (the review's mutation check)."""
import sys, os
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__)); from s_smoke import serve

def run(folder):
    srv, port = serve(folder); bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
        errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
        p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        p.goto(f"http://127.0.0.1:{port}/index.html")
        p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=180000)
        p.select_option("#speed", "0")
        p.click("#start")                                                 # a real click: the button takes focus
        p.wait_for_function("Screen.state && Screen.state.phase === 'declare' && !Screen.debug.busy", timeout=60000)
        before = p.evaluate("[Lab.call('record').bseed, fightId]")
        for _ in range(2):                                                # Enter fights (the second confirms the fill)
            p.keyboard.press("Enter"); p.wait_for_timeout(80)
        try: p.wait_for_function("(Screen.state.round >= 2 || Screen.state.phase !== 'declare') && !Screen.debug.busy", timeout=20000)
        except Exception: pass                                            # judged below: a restarted fight stays in round 1
        after = p.evaluate("[Lab.call('record').bseed, fightId]")
        rnd = p.evaluate("Screen.state.round")
        if before != after: bad.append(("the fight restarted", before, after))
        if rnd < 2 and p.evaluate("Screen.state.phase") == "declare": bad.append(("the round didn't advance", rnd))
        b.close()
    srv.shutdown()
    if errs: bad.append(("page errors", errs[:3]))
    print("FAIL" if bad else "PASS", bad); return not bad

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.exit(0 if run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "..", "fight_lab")) else 1)
