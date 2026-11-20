"""C02 (AGENT_CODE_REVIEW): start fight B while fight A's Auto playback has a continuation pending; A must not touch B.
Run with the Lab served on 127.0.0.1:8765. Prints PASS or FAIL with what it saw."""
from playwright.sync_api import sync_playwright
import sys
def run(trials=4):
    bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
        errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
        p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        p.goto("http://127.0.0.1:8765/index.html")
        p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=120000)
        p.select_option("#speed", "70")
        for t in range(trials):
            p.fill("#seed", str(11 + t)); p.dispatch_event("#seed", "change")
            p.click("#rollparty"); p.wait_for_timeout(50); p.click("#rollpack"); p.wait_for_timeout(50)
            p.click("#auto")                                    # fight A, Auto
            # wait for A to finish playing a round: the start button comes back while A's next commit is pending
            p.wait_for_function("!document.querySelector('#start').disabled && Screen.state && Screen.state.phase !== 'over'", timeout=60000)
            p.click("#start")                                    # fight B, the player's: it must wait for orders
            p.wait_for_timeout(2500)                             # long enough for any of A's leftovers to fire
            s = p.evaluate("({phase: Screen.state.phase, round: Screen.state.round, orders: Lab.call('record').orders.length})")
            if not (s["phase"] == "declare" and s["round"] == 1 and s["orders"] == 0): bad.append((t, s))
        # and a whole Auto fight at a non-zero speed still plays to the end in one session
        p.fill("#seed", "99"); p.dispatch_event("#seed", "change"); p.click("#rollparty"); p.wait_for_timeout(50)
        p.click("#rollpack"); p.wait_for_timeout(50); p.click("#auto")
        try: p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=240000)
        except Exception: bad.append(("auto at speed 70 never finished", p.evaluate("Screen.state && Screen.state.round")))
        b.close()
    if errs: bad.append(("page errors", errs[:3]))
    print("FAIL" if bad else "PASS", bad)
    return not bad
if __name__ == "__main__": sys.exit(0 if run() else 1)
