"""Step 7c: a scripted play-through by real clicks and keys, with screenshots and checks."""
from playwright.sync_api import sync_playwright
from PIL import Image
import json
S = "/tmp/claude-0/-home-claude/83f4fe98-00ce-598d-b46d-8b8b896bc028/scratchpad/s7c"
notes = []
def note(*a): notes.append(" ".join(str(x) for x in a)); print(*a)
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
    errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    p.goto("http://127.0.0.1:8765/index.html")
    p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=120000)
    p.select_option("#speed", "220")
    p.fill("#seed", "11"); p.dispatch_event("#seed", "change")
    p.select_option("#hab", "Barrow"); p.fill("#budget", "7"); p.dispatch_event("#budget", "change")
    p.click("#mkparty"); p.click("#rollpack"); p.click("#start")
    p.wait_for_function("Screen.state && !Screen.debug.busy && Screen.debug.current", timeout=60000)
    p.evaluate("window.scrollTo(0,0)"); p.wait_for_timeout(100)
    bb = p.query_selector("#screen").bounding_box(); sx = bb["width"] / 320
    k = [0]
    def shot(label):
        p.screenshot(path=f"{S}/_f.png")
        Image.open(f"{S}/_f.png").crop((bb["x"], bb["y"], bb["x"] + bb["width"], bb["y"] + bb["height"])).save(f"{S}/{k[0]:02d}_{label}.png"); k[0] += 1
    move = lambda x, y: (p.mouse.move(bb["x"] + x * sx, bb["y"] + y * sx), p.wait_for_timeout(120))
    click = lambda x, y: (p.mouse.click(bb["x"] + x * sx, bb["y"] + y * sx), p.wait_for_timeout(160))
    dbg = lambda: p.evaluate("Screen.debug")
    def hit(label):                                  # click a box item by its label position from the hit list order
        h = dbg()["hits"]; return h
    def foes(): return [u for u in dbg()["units"] if u["side"] == "enemy" and u["alive"]]
    def heroes(): return [u for u in dbg()["units"] if u["side"] == "party"]
    def idle(): p.wait_for_function("!Screen.debug.busy", timeout=120000); p.wait_for_timeout(150)
    shot("start")
    # hover a foe: the plate
    f = foes()[0]; move(f["cx"], f["cy"]); shot("hover_plate")
    # hero 1: first move -> its card -> click a foe it can reach
    cur = dbg()["current"]; o = p.evaluate(f"Lab.call('options','{cur}')")
    click(30, 141); shot("move_card")
    tg = o["halv"]["targets"]; t = next(u for u in foes() if u["id"] in tg)
    click(t["cx"], t["cy"]); note("hero1", cur, "ordered:", dbg()["current"] != cur)
    # hero 2: Guard (utility col 0 row 1)
    cur2 = dbg()["current"]; click(222, 153); note("hero2 guard:", dbg()["current"] != cur2)
    # hero 3: Move -> a cell
    cur3 = dbg()["current"]; click(222, 165); shot("move_cells")
    o3 = p.evaluate(f"Lab.call('options','{cur3}')"); want = o3["move"]["cells"][0]["cell"]
    xy = next(c["xy"] for c in dbg()["cells"] if c["cell"] == want)
    click(xy[0], xy[1] - 6); note("hero3 move to", want, "ordered:", p.evaluate(f"Lab.call('preview').find(r=>r.id==='{cur3}').ordered"))
    # Inspect a foe, then close
    click(270, 153); f = foes()[-1]; click(f["cx"], f["cy"]); shot("inspect"); click(160, 90)
    move(5, 175); shot("orders_set")
    # Fight: watch playback
    p.keyboard.press("Enter")
    for i in range(6): p.wait_for_timeout(140); shot(f"play1_{i}")
    idle(); shot("round2")
    # round 2: Fight with nothing ordered -> confirm -> OK
    p.keyboard.press("Enter"); p.wait_for_timeout(150); shot("confirm"); note("confirm mode:", dbg()["mode"])
    click(218, 165); p.wait_for_timeout(200); shot("autopilot_blink")
    idle()
    # round 3: Pouch -> first item -> a target (self/ally) if it needs one
    if p.evaluate("Screen.state.phase") != "over":
        cur = dbg()["current"]; click(222, 141); shot("pouch")
        o = p.evaluate(f"Lab.call('options','{cur}')"); it = o["items"][0] if o["items"] else None
        note("pouch item:", it and (it["name"], it["aim"], it["targets"][:3]))
        if it:
            click(30, 141); shot("item_card")
            if it["aim"] in ("self", "all"): click(30, 141)
            else:
                t = next((u for u in dbg()["units"] if u["id"] in it["targets"]), None)
                if t: click(t["cx"], t["cy"])
            note("item ordered:", dbg()["current"] != cur)
        p.keyboard.press("Enter"); p.wait_for_timeout(100)
        if dbg()["mode"] == "confirm": p.keyboard.press("Enter")
        idle(); shot("round3_done")
    # the rest on autopilot, fast
    p.select_option("#speed", "70"); rounds = 0
    while p.evaluate("Screen.state.phase") != "over" and rounds < 40:
        p.keyboard.press("Enter"); p.wait_for_timeout(80)
        if dbg()["mode"] == "confirm": p.keyboard.press("Enter")
        idle(); rounds += 1
    shot("end"); note("winner", p.evaluate("Screen.state.winner"), "rounds", p.evaluate("Screen.state.round"))
    note("last lines", dbg()["lines"])
    rec = p.evaluate("Lab.call('record')"); open(f"{S}/record.jsonl", "w").write(json.dumps(rec) + "\n")
    note("page errors", errs[:5])
    b.close()
open(f"{S}/notes.txt", "w").write("\n".join(notes))
