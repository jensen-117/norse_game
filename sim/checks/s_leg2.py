"""Nov 10: Joseph's 32R heroes and the Drattr court on the page.
1. Opening boards (Rapids, Barrow): every unit has art. 2. A fight with a net-thrower at normal speed, sampled
every 60 ms, until she has thrown and taken up the spear: catches Bound's swirl, the move frames and the fade.
3. Fights on Auto to the end: no page errors."""
import json, sys
from playwright.sync_api import sync_playwright
OUT = "/home/claude/art_work/leg2"
import os; os.makedirs(OUT, exist_ok=True)

def setup(p, hab, seed, budget=8, level=30):
    p.select_option("#speed", "0")
    p.fill("#seed", str(seed)); p.dispatch_event("#seed", "change"); p.click("#rollparty"); p.wait_for_timeout(30)
    p.select_option("#hab", hab); p.fill("#elevel", str(level)); p.fill("#budget", str(budget))
    p.dispatch_event("#budget", "change"); p.dispatch_event("#elevel", "change")
    p.click("#rollpack"); p.wait_for_timeout(30)
    p.click("#start"); p.wait_for_timeout(500)
    return p.evaluate("Screen.debug.units")

with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
    errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    p.goto("http://127.0.0.1:8765/index.html")
    p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=180000)

    # 1. opening boards
    missing, shots = [], 0
    for hab, seed in [("Rapids", 5), ("Rapids", 17), ("Rapids", 29), ("Barrow", 11), ("Barrow", 23)]:
        us = setup(p, hab, seed)
        missing += [(hab, seed, u["name"]) for u in us if not u["key"]]
        p.locator("#fight canvas").first.screenshot(path=f"{OUT}/open_{shots}.png"); shots += 1
        p.click("#auto"); p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=120000)
    print("units without art:", missing)

    # 2. find a pack with a net-thrower, then watch it at normal speed
    found = None
    for seed in range(1, 200):
        us = setup(p, "Rapids", seed)
        if any(u["key"] == "drattr:Net" for u in us): found = seed; break
        p.click("#auto"); p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=120000)
    print("net seed:", found)
    seen = dict(bound=0, pose=set(), spear=False, frames=[])
    if found:
        p.select_option("#speed", "220"); p.click("#auto")
        for i in range(900):
            us = p.evaluate("Screen.debug.units")
            st = p.evaluate("Screen.state && Screen.state.phase")
            nb = sum(1 for u in us if u["bound"]); poses = {(u["key"], u["pose"]) for u in us if u["pose"]}
            spear_now = any(u["key"] == "drattr:Spear" for u in us) and not any(u["key"] == "drattr:Net" for u in us)
            interesting = nb > seen["bound"] or (poses - seen["pose"]) or (spear_now and not seen["spear"])
            if interesting and len(seen["frames"]) < 12:
                f = f"{OUT}/watch_{len(seen['frames'])}.png"; p.locator("#fight canvas").first.screenshot(path=f)
                seen["frames"].append((f, nb, sorted(poses - seen["pose"]), spear_now))
            seen["bound"] = max(seen["bound"], nb); seen["pose"] |= poses; seen["spear"] |= spear_now
            if st == "over": break
            p.wait_for_timeout(60)
        print("bound seen:", seen["bound"], "| poses:", sorted(seen["pose"]), "| took up spear:", seen["spear"])
        for f in seen["frames"]: print("  ", f)
        print("log:", [l for l in p.evaluate("Screen.debug.lines")])
        p.select_option("#speed", "0")
        p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=180000)

    # 3. fights to the end
    for hab, seed in [("Rapids", s) for s in range(40, 52)] + [("Barrow", s) for s in range(60, 66)]:
        setup(p, hab, seed); p.click("#auto")
        p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=120000)
    print("errors:", errs[:5])
    b.close()
