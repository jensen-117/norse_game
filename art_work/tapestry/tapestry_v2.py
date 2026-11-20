"""Tapestry map, v2 (Nov 11): the agent's tapestry.py with Joseph's icons and the agreed changes.
- Joseph's icons (icon_test_1, drakkar_icon_1): full colour on the open map (the choices you can take now, and
  where you stand); woven into the past in three tones of the band's wool, so the record reads as stitched.
- The party is the longship, sailing in on the left of where you stand (no marker plate).
- A 1 px ink outline only where white or pale parts of an icon meet the linen.
- The linen: sparse weft dashes (one dashed row in four, 2 over 6 under, offset each time).
- Each leg's band takes its place rune's colours (Yr: the Barrow, wine; Logr: the Rapids, blue; Bjarkan: the
  Wildwood, green).
- A fallen hero is a cairn among the spoils.
Usage: python3 tapestry_v2.py OUTDIR"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent"))
import types
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent", "tapestry.py")).read()
_plate = "cv.rect(mx,my-1,13,7,C['keyline']); cv.bitmap(mx+1,my,MARKER,C['gold'],gold=True)"
assert _src.count(_plate) == 1
T = types.ModuleType("tapestry"); T.__file__ = "agent/tapestry.py"
exec(compile(_src.replace(_plate, "pass   # v2: the longship replaces the marker plate").replace("if __name__=='__main__':", "if False:"), "agent/tapestry.py", "exec"), T.__dict__)
sys.modules["tapestry"] = T
Cv, PARAMS, COLOURS, SPOILS, stitch, col_x = T.Cv, T.PARAMS, T.COLOURS, T.SPOILS, T.stitch, T.col_x

ART = "/home/claude/art_work"
INK = "2e222f"
RUNES = {   # a place rune's colours: border strand, edge, threads, and its wool (light, mid, dark) for woven glyphs
    "Yr":      dict(place="the Barrow", ground="fca790", strand="7a3045", edge="45293f", thread=("831c5d", "7a3045"), wool=("a24b6f", "7a3045", "45293f")),
    "Logr":    dict(place="the Rapids", ground="fca790", strand="4d65b4", edge="323353", thread=("323353", "484a77"), wool=("4d65b4", "484a77", "323353")),
    "Bjarkan": dict(place="the Wildwood", ground="fca790", strand="239063", edge="165a4c", thread=("239063", "165a4c"), wool=("239063", "165a4c", "313638")),
    "Kaun":    dict(place="the Surtland", ground="fca790", strand="b33831", edge="6e2727", thread=("b33831", "6e2727"), wool=("cd683d", "b33831", "6e2727")),
}
SPOILS["fallen"] = ["...#...", "..###..", "..#.#..", ".#####.", ".##.##.", "#######", "#######"]   # a cairn
COLOURS["spoil"]["fallen"] = "625565"

def icon(path):
    """Joseph's icon, with an ink outline only where its white or pale parts meet the linen (1 px of padding)."""
    im = Image.open(path).convert("RGBA"); a = np.zeros((im.height + 2, im.width + 2, 4), np.uint8); a[1:-1, 1:-1] = np.array(im)
    op = a[..., 3] > 0; lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]; light = op & (lum >= 200)
    out = a.copy(); h, w = op.shape
    for y in range(h):
        for x in range(w):
            if not op[y, x] and any(0 <= y + dy < h and 0 <= x + dx < w and light[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y, x] = (*T.rgb(INK), 255)
    out[..., 3][~op & (out[..., 3] > 0)] = 254      # outline pixels: opaque, but marked (alpha 254) so faint() can skip them
    return out
I2 = f"{ART}/icons_test2/frame%d.png"
ICONS = {"fight": icon(I2 % 18), "elite": icon(I2 % 19), "boss": icon(I2 % 21), "rest": icon(f"{ART}/icons_test2/camp_nosky.png"),
         "treasure": icon(I2 % 12), "merchant": icon(I2 % 14), "event": icon(I2 % 15)}
SHIP = icon(f"{ART}/drakkar/frame0.png")
def rows_of(t):
    a = ICONS[t]; return ["".join("#" if p[3] else "." for p in r) for r in a]
T.rows_of = rows_of

def paste_full(cv, x, y, a):
    for j in range(a.shape[0]):
        for i in range(a.shape[1]):
            if a[j, i, 3]: cv.px(x + i, y + j, "%02x%02x%02x" % tuple(a[j, i, :3]))
def paste_wool(cv, x, y, a, wool):
    """Woven: the icon in three tones of the band's wool, by lightness (light parts, mid, dark and ink)."""
    for j in range(a.shape[0]):
        for i in range(a.shape[1]):
            if a[j, i, 3]:
                l = 0.299 * a[j, i, 0] + 0.587 * a[j, i, 1] + 0.114 * a[j, i, 2]
                cv.px(x + i, y + j, wool[0] if l >= 170 else wool[1] if l >= 80 else wool[2])

def faint(cv, x, y, a, colour, progress):
    """Half-stitched ahead: the icon's edge and its dark marks (a skull's eyes) in one faint colour, dotted when
    barely begun; a glyph you can't reach from here gets only every other stitch."""
    op = a[..., 3] > 0; lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]; h, w = op.shape
    for j in range(h):
        for i in range(w):
            if not op[j, i]: continue
            edge = any(not (0 <= j + dj < h and 0 <= i + di < w and op[j + dj, i + di]) for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            dark = lum[j, i] < 80 and a[j, i, 3] == 255                 # a skull's eyes, not the added outline
            if (edge or dark) and (progress >= 0.3 or (i + j) % 2 == 0): cv.px(x + i, y + j, colour)

def linen(cv, x0, x1, y0, y1, woven, rng):
    C = COLOURS
    for y in range(y0, y1):
        for x in range(x0, x1):
            if woven: c = C["weft"] if (y % 4 == 0 and (x + (y // 4) * 2) % 8 < 2) else C["linen"]   # sparse weft dashes
            else: c = C["weft"] if x % 3 == 0 else C["linen"]                                       # bare warp strings
            cv.px(x, y, c)
T.linen = linen

def render(cols, current, runes, hover=None, seed=1, ship_frame=None):
    """The agent's render, with the glyph pass redrawn for icons. runes: one place rune per leg."""
    P = PARAMS; C = COLOURS
    C["bands"] = [RUNES[r] for r in runes]
    # draw everything but the glyphs with the agent's code, by handing it blank glyphs
    keep = T.GLYPHS; blank = {t: ["." * len(rows_of(t)[0])] * len(rows_of(t)) for t in ICONS}
    T.GLYPHS = blank; T.rows_of = lambda t: blank[t]
    T.MARKER = ["." * 11] * 5; keepk = C["keyline"]; keepg = C["gold"]
    cv, boxes = T.render(cols, current, None, seed)
    T.GLYPHS = keep; T.rows_of = rows_of
    def state(i):
        if i < current: return "past"
        if i == current: return "current"
        if i <= current + P["sight"]: return "ahead"
        if P["show_destinations"] and cols[i]["types"][0] in ("elite", "boss"): return "ahead"
        return "beyond"
    for i, c in enumerate(cols):
        st = state(i); band = C["bands"][c["band"]]
        for k, t in enumerate(c["types"]):
            a = ICONS[t]; x, y = T.glyph_xy(i, k, cols, rows_of(t))
            if st == "past":
                if k != c["chosen"]: continue
                paste_wool(cv, x, y, a, band["wool"])
                sp = c["spoils"][:5]; widths = [len(SPOILS[s][0]) for s in sp]; tw = sum(widths) + P["spoil_gap"] * (len(sp) - 1)
                sx = x + a.shape[1] // 2 - tw // 2
                for s, wd in zip(sp, widths): cv.bitmap(sx, y + a.shape[0] + 1, SPOILS[s], C["spoil"][s]); sx += wd + P["spoil_gap"]
            elif st == "current":
                if k != c["chosen"]: continue
                paste_full(cv, x, y, a)
                s = ship_frame if ship_frame is not None else SHIP
                paste_full(cv, x - s.shape[1] - 4, y + (a.shape[0] - s.shape[0]) // 2, s)   # the party sails in from the left
            elif st == "ahead":
                reach = (i == current + 1 and k in cols[current]["links"][cols[current]["chosen"]])
                if reach: paste_full(cv, x, y, a)                                             # a choice you can take now
                else: faint(cv, x, y, a, C["faint"], 0.2 if i == current + 1 else P["half_stitch"])
    if hover:
        i, k = hover; t = cols[i]["types"][k]; x, y = T.glyph_xy(i, k, cols, rows_of(t)); w, h = len(rows_of(t)[0]), len(rows_of(t))
        for j in range(-2, h + 2):
            for i2 in range(-2, w + 2):
                if (j in (-2, h + 1) or i2 in (-2, w + 1)) and (i2 + j) % 2 == 0: cv.px(x + i2, y + j, C["gold_dark"], gold=True)
    return cv

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"; os.makedirs(out, exist_ok=True)
    cols = T.demo_columns(); current = 7; runes = ["Yr", "Logr", "Bjarkan"]
    strip = render(cols, current, runes)
    strip.image().save(f"{out}/tapestry_1x.png"); strip.image(3).save(f"{out}/tapestry_3x.png")
    cam = max(0, col_x(current, cols) - 200)
    nxt = cols[current]["links"][cols[current]["chosen"]]
    hv = render(cols, current, runes, hover=(current + 1, nxt[0]))
    t = cols[current + 1]["types"][nxt[0]]
    for name, s, cx, line in (("screen_current", strip, cam, None),
                              ("screen_hover", hv, cam, f"{t} - a choice you can take. {RUNES[runes[cols[current]['band']]]['place']}.")):
        sc = T.screen(s, cx, line); sc.image().save(f"{out}/{name}_1x.png"); sc.image(4).save(f"{out}/{name}_4x.png")
    print(strip.w, strip.h, T.audit(strip, "tapestry"))
