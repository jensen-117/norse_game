"""Gandalf Hardcore sheets (skeleton, zombie, archer) -> Resurrect 64.
Each source colour is sorted into a MATERIAL by hue/saturation, then snapped onto that material's Res64 ramp
by lightness rank (darkest source -> darkest slot). Gore is removed (red pixels take their neighbours' colour).
Outputs per-frame PNGs (cut from the 64px grid), converted sheets, and before/after contact sheets.

    python3 undead_res64.py <outdir>
"""
import sys, os, colorsys
from collections import Counter
import numpy as np
from PIL import Image

OUT = sys.argv[1]
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sources")   # the attached sheets, kept with the tools
SHEETS = {"skeleton": f"{SRC}/00ec923d-image.png", "zombie": f"{SRC}/f5a9ad0c-image.png", "archer": f"{SRC}/2c71a4a8-image.png"}
RES = set(open(os.path.join(os.path.dirname(__file__), "res64.txt")).read().split())
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def hexs(c): return "%02x%02x%02x" % c
def L(c):
    f = lambda v: ((v/255 + .055)/1.055)**2.4 if v/255 > .04045 else v/255/12.92
    Y = .2126*f(c[0]) + .7152*f(c[1]) + .0722*f(c[2]); return 116*Y**(1/3) - 16 if Y > .008856 else 903.3*Y
def hsl(c):
    h, s, v = colorsys.rgb_to_hsv(*[x/255 for x in c]); return h * 360, s, L(c)

INK = "2e222f"
GORE = "gore"            # removed: takes its neighbours' colour
# Bone ramps (dark shadow, shadow, mid, light, highlight): the rank tint is a ramp swap
BONE = {
    "plain": ["3e3546", "625565", "9babb2", "c7dcd0", "ffffff"],      # Halv: clean, cold bone
    "aged":  ["45293f", "694f62", "966c6c", "ab947a", "fdcbb0"],      # Bein: yellowed, old (no pure white)
    "drott": ["45293f", "7a3045", "cf657f", "f68181", "fca790"],      # Drott: blood-red bone
}

def ramp_snap(colours, ramp):
    """Map colours (one material) onto a ramp by lightness rank, spread over the ramp's length."""
    cs = sorted(colours, key=L); n = len(cs); out = {}
    for i, c in enumerate(cs):
        k = round(i * (len(ramp) - 1) / max(1, n - 1)) if n <= len(ramp) else min(len(ramp) - 1, int(i * len(ramp) / n))
        out[c] = ramp[k]
    return out

def skeleton_map(cols, tint="plain"):
    m = {}
    for c in cols:
        h, s, l = hsl(c)
        if l < 10: m[c] = INK
        elif s > 0.5 and (h < 15 or h > 345): m[c] = {"540f0f": "6e2727", "a22b2b": "ae2334"}.get(hexs(c), "e83b3b")   # eyes
    bone = [c for c in cols if c not in m]
    m.update(ramp_snap(bone, BONE[tint]))
    return m

def zombie_map(cols):
    m = {}; skin, cloth, fx = [], [], []
    for c in cols:
        h, s, l = hsl(c)
        if l < 8: m[c] = INK
        elif hexs(c) == "330f1f": m[c] = "45293f"
        elif s > 0.6 and (h < 10 or h > 345): m[c] = GORE                          # blood
        elif 60 <= h <= 100: skin.append(c)                                         # green skin -> corpse-blue
        elif hexs(c) in ("ff9e24", "fff28f"): fx.append(c)                          # hit spark
        elif l > 95: m[c] = "ffffff"
        else: cloth.append(c)                                                       # grave rags
    m.update(ramp_snap(skin, ["484a77", "7f708a", "9babb2", "c7dcd0", "ffffff"]))      # corpse-pale blue
    m.update(ramp_snap(cloth, ["45293f", "694f62", "966c6c", "ab947a", "ab947a", "fdcbb0"]))    # grave rags, lifted off the stone
    m.update(ramp_snap(fx, ["f9c22b", "fbff86"]))
    return m

def archer_map(cols):
    m = {}; dark, armor, wood, skin, cloth, gold = [], [], [], [], [], []
    for c in cols:
        h, s, l = hsl(c); x = hexs(c)
        if l < 7: m[c] = INK
        elif x in ("912b2e", "8e5252", "6a413d"): m[c] = "b2ba90"                   # the red cross: gone into the tabard
        elif x == "dc6a14": m[c] = "8ff8e2"                                         # arrow trail
        elif x in ("cc8b7e", "e9b5a3"): skin.append(c)                              # face skin -> ectoplasm glow
        elif l < 24 and s < 0.7: dark.append(c)
        elif 40 <= h <= 55 and s > 0.5: gold.append(c)                              # the yellow scarf
        elif s < 0.2 and l >= 66: cloth.append(c)                                   # tabard, light mail
        elif 15 <= h <= 30 and s > 0.35: wood.append(c)                              # bow, leather
        else: armor.append(c)
    m.update(ramp_snap(dark, ["2e222f", "313638", "313638", "374e4a"]))
    m.update(ramp_snap(armor, ["374e4a", "547e64", "547e64", "92a984", "92a984"]))
    m.update(ramp_snap(wood, ["313638", "374e4a", "547e64", "547e64"]))
    m.update(ramp_snap(gold, ["547e64", "92a984", "b2ba90", "c7dcd0"]))
    m.update(ramp_snap(cloth, ["b2ba90", "c7dcd0", "c7dcd0", "ffffff"]))
    m.update(ramp_snap(skin, ["0eaf9b", "30e1b9", "8ff8e2"]))
    return m

def apply(im, m):
    a = np.asarray(im.convert("RGBA")).copy(); h, w = a.shape[:2]
    out = a.copy(); gore = []
    for y in range(h):
        for x in range(w):
            if not a[y, x, 3]: continue
            t = m[tuple(int(v) for v in a[y, x, :3])]
            if t == GORE: gore.append((x, y)); continue
            assert t in RES, t
            out[y, x, :3] = rgb(t)
    for x, y in gore:                                   # gore: majority of non-gore neighbours, else clear
        nb = [tuple(out[y+dy, x+dx]) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
              if (dx or dy) and 0 <= y+dy < h and 0 <= x+dx < w and (x+dx, y+dy) not in gore]
        opaque = [p for p in nb if p[3]]
        out[y, x] = Counter(opaque).most_common(1)[0][0] if len(opaque) >= 4 else (0, 0, 0, 0)
    return Image.fromarray(out)

def frames(sheet, cw=64, ch=64):
    out = []
    for r in range(sheet.height // ch):
        for c in range(sheet.width // cw):
            cell = sheet.crop((c*cw, r*ch, c*cw+cw, r*ch+ch))
            if cell.getbbox(): out.append(((r, c), cell))
    return out

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    conv = {}
    for name, path in SHEETS.items():
        src = Image.open(path).convert("RGBA")
        cols = {tuple(int(v) for v in p[:3]) for p in np.asarray(src).reshape(-1, 4) if p[3]}
        maps = {"skeleton": {t: skeleton_map(cols, t) for t in BONE}, "zombie": {"corpse": zombie_map(cols)},
                "archer": {"hunt": archer_map(cols)}}[name]
        for tag, m in maps.items():
            print(name, tag, " ".join(f"{hexs(c)}>{t}" for c, t in sorted(m.items(), key=lambda kv: L(kv[0]))))
            cs = apply(src, m); conv[(name, tag)] = cs
            cs.save(f"{OUT}/{name}_{tag}_sheet.png")
            d = f"{OUT}/frames/{name}_{tag}"; os.makedirs(d, exist_ok=True)
            for (r, c), cell in frames(cs): cell.save(f"{d}/r{r}c{c}.png")
        # before/after contact sheet (2x)
        tags = list(maps)
        bw = src.width * 2; sheet = Image.new("RGBA", (bw * (1 + len(tags)) + 8 * len(tags), src.height * 2), (40, 40, 48, 255))
        sheet.alpha_composite(src.resize((bw, src.height * 2), Image.NEAREST), (0, 0))
        for i, t in enumerate(tags):
            sheet.alpha_composite(conv[(name, t)].resize((bw, src.height * 2), Image.NEAREST), ((bw + 8) * (i + 1), 0))
        sheet.save(f"{OUT}/{name}_before_after.png")
    print("ok")
