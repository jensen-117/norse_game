"""Nov 9: the 32R Beinar, the Drattr and the dulled Mogel on the page: the opening board per habitat (screenshot),
then the same fight on Auto to the end (no page errors)."""
from playwright.sync_api import sync_playwright
OUT = "/home/claude/art_work/beinar_32r"
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
    errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    p.goto("http://127.0.0.1:8765/index.html")
    p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=120000)
    for i, (hab, seed) in enumerate([("Barrow", 11), ("Barrow", 23), ("Rapids", 5), ("Rapids", 17), ("Biome: Mire", 9)]):
        p.select_option("#speed", "0")
        p.fill("#seed", str(seed)); p.dispatch_event("#seed", "change"); p.click("#rollparty"); p.wait_for_timeout(50)
        p.select_option("#hab", hab); p.fill("#elevel", "30"); p.fill("#budget", "8")
        p.dispatch_event("#budget", "change"); p.dispatch_event("#elevel", "change")
        p.click("#rollpack"); p.wait_for_timeout(50)
        p.click("#start"); p.wait_for_timeout(900)
        p.locator("#fight canvas").first.screenshot(path=f"{OUT}/page_{i}.png")
        foes = [u["name"] for u in p.evaluate("Screen.debug.units") if u["side"] != "party"]
        p.click("#auto"); p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=120000)
        print(hab, seed, foes, "->", p.evaluate("Lab.call('record')")["winner"])
    print("errors:", errs[:3])
    b.close()
