"""Nov 10: range on the move card. Open the first move's card for each hero of a few parties; screenshot the text box."""
from playwright.sync_api import sync_playwright
from PIL import Image
S = "/home/claude/art_work/leg2"
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
    errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    p.goto("http://127.0.0.1:8765/index.html")
    p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=180000)
    shots = []
    for seed in (11, 4, 9, 23):
        p.select_option("#speed", "0"); p.fill("#seed", str(seed)); p.dispatch_event("#seed", "change")
        p.click("#rollparty"); p.select_option("#hab", "Barrow"); p.click("#rollpack"); p.click("#start")
        p.wait_for_function("Screen.state && !Screen.debug.busy && Screen.debug.current", timeout=60000)
        p.evaluate("window.scrollTo(0,0)"); p.wait_for_timeout(100)
        bb = p.query_selector("#screen").bounding_box(); sx = bb["width"] / 320
        for col, row in ((30, 141), (30, 153), (124, 141)):
            p.mouse.click(bb["x"] + col * sx, bb["y"] + row * sx); p.wait_for_timeout(150)
            p.screenshot(path=f"{S}/_f.png")
            im = Image.open(f"{S}/_f.png").crop((bb["x"], bb["y"] + 128 * sx, bb["x"] + 200 * sx, bb["y"] + bb["height"]))
            shots.append(im)
            p.mouse.click(bb["x"] + 12 * sx, bb["y"] + 137 * sx); p.wait_for_timeout(120)   # "<" back
        p.click("#auto"); p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=120000)
    w, h = shots[0].size; sheet = Image.new("RGB", (w * 3 + 20, h * 4 + 30), (30, 30, 30))
    for i, im in enumerate(shots): sheet.paste(im, ((i % 3) * (w + 10), (i // 3) * (h + 10)))
    sheet.save(f"{S}/range_cards.png"); print("errors:", errs[:3]); b.close()
