"""The Draugr ladder (the Beinar treatment): skin tint and rag tint walk the ranks, rows cut or stretched for size.
    pale  (nar-folr, corpse-pale)  : the fresh dead -- Halvdraugr
    blar  (hel-blar, death-blue)   : the old dead   -- Draugr, Stordraugr
    drott (hel-blar in grave-gold) : the barrow king -- Forndraugr
Sizes: cut 6 rows (Halv), native, stretch the same 6 rows (Stor and up). Frames shorter than 30px (the crawl,
the fall) are never resized. The baked slash arc keeps the effect white whatever the tint.
    python3 draugr_res64.py <scratchpad> <outdir>"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
S, OUT = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], OUT]; sys.path.insert(0, f"{S}/tools")
import undead_res64 as U

SKIN = {"pale": ["484a77", "7f708a", "9babb2", "c7dcd0", "ffffff"],
        "blar": ["323353", "484a77", "4d65b4", "7f708a", "9babb2"],
        "drott": ["323353", "484a77", "4d65b4", "7f708a", "9babb2"]}
RAGS = {"pale": ["45293f", "694f62", "966c6c", "ab947a", "ab947a", "fdcbb0"],
        "blar": ["3e3546", "45293f", "694f62", "966c6c", "966c6c", "ab947a"],
        "drott": ["2e222f", "45293f", "6e2727", "7a3045", "9e4539", "b33831"]}   # blood: the Drott mark across families (gold read as orange)
FX = ["9babb2", "c7dcd0", "ffffff"]               # the slash arc, whatever the tint
ROWS = [3, 6, 8, 10, 15, 22]                      # from the bottom: shin, three thigh rows, hands, shirt

def zmap(cols, tint):
    m = {}; skin, cloth, fx = [], [], []
    for c in cols:
        h, s, l = U.hsl(c)
        if l < 8: m[c] = U.INK
        elif U.hexs(c) == "330f1f": m[c] = "45293f"
        elif s > 0.6 and (h < 10 or h > 345): m[c] = U.GORE
        elif 60 <= h <= 100: skin.append(c)
        elif U.hexs(c) in ("ff9e24", "fff28f"): m[c] = U.GORE           # baked hit sparks go too: our effects draw hits
        elif l > 95: m[c] = "ffffff"
        else: cloth.append(c)
    m.update(U.ramp_snap(skin, SKIN[tint])); m.update(U.ramp_snap(cloth, RAGS[tint]))
    m.update(U.ramp_snap(fx, ["f9c22b", "fbff86"]))
    return m, U.ramp_snap(skin, ["9babb2", "9babb2", "c7dcd0", "c7dcd0", "ffffff"])

from arc_find import arc_pixels
def arc_fix(src_cell, out_cell, fxmap=None):
    """The baked slash arc goes effect-white whatever the tint: pure white core, then the pale steps."""
    a, o = np.asarray(src_cell), np.asarray(out_cell).copy()
    for y, x in arc_pixels(a):
        h = "%02x%02x%02x" % tuple(int(v) for v in a[y, x, :3])
        o[y, x, :3] = U.rgb("ffffff" if h == "ffffff" else "c7dcd0" if h in ("97ad7d", "989a8f") else "9babb2")
    return Image.fromarray(o)

def resize_rows(im, mode):
    bb = im.getbbox()
    if mode == "native" or not bb or bb[3] - bb[1] < 30: return im
    a = np.asarray(im); bottom = bb[3] - 1; out = []
    for y in range(a.shape[0]):
        k = bottom - y
        if k in ROWS and mode == "cut": continue
        out.append(a[y])
        if k in ROWS and mode == "stretch": out.append(a[y])
    out = np.array(out); pad = 64 - out.shape[0]
    if pad > 0: out = np.concatenate([np.zeros((pad, out.shape[1], 4), np.uint8), out])
    return Image.fromarray(out[-pad:] if pad < 0 else out)

if __name__ == "__main__":
    src = Image.open(U.SHEETS["zombie"]).convert("RGBA")
    cols = {tuple(int(v) for v in p[:3]) for p in np.asarray(src).reshape(-1, 4) if p[3]}
    LADDER = [("pale", "cut", "Halvdraugr"), ("pale", "native", "Draugr (pale)"), ("blar", "native", "Draugr"),
              ("blar", "stretch", "Stordraugr"), ("drott", "stretch", "Forndraugr")]
    KEY = [(0, 0), (1, 9), (3, 2), (4, 1), (6, 2)]          # idle, wind-up, slash, hit, crawl
    sc = 5; cw = 36
    sheet = Image.new("RGBA", (len(KEY) * cw * sc + 10, len(LADDER) * 50 * sc + 10), (62, 53, 70, 255))
    d = ImageDraw.Draw(sheet)
    for r, (tint, size, label) in enumerate(LADDER):
        m, fxm = zmap(cols, tint)
        conv = U.apply(src, m)
        dd = f"{OUT}/frames/draugr_{tint}_{size}"; os.makedirs(dd, exist_ok=True)
        cells = {}
        for (rr, cc), cell in U.frames(conv):
            raw = src.crop((cc * 64, rr * 64, cc * 64 + 64, rr * 64 + 64))
            cell = resize_rows(arc_fix(raw, cell, fxm), size); cell.save(f"{dd}/r{rr}c{cc}.png"); cells[(rr, cc)] = cell
        for k, rc in enumerate(KEY):
            im = cells[rc]; crop = im.crop((10, 14, 10 + cw, 64))
            sheet.alpha_composite(crop.resize((cw * sc, 50 * sc), Image.NEAREST), (5 + k * cw * sc, 5 + r * 50 * sc))
        d.text((8, 8 + r * 50 * sc), label, fill=(235, 235, 235))
    sheet.save(f"{OUT}/draugr_ladder.png"); print("ok")
