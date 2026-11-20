"""Views for the Beinar pass: the stretched ribs up close, the mage's orb in every element (Joseph's pattern
and a redrawn sphere), and the aged-bone options. Element ramps are the Mogel's (one table for the game)."""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw
S, OUT = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], S, OUT]
src = open(f"{S}/tools/beinar_res64.py").read()
exec(src[:src.index("os.makedirs(OUT")])                     # convert, rows_, BONE, SRC, GEM ...
sl = open(f"{S}/tools/slime_res64.py").read()
i = sl.index("RAMPS = {"); exec(sl[i:sl.index("}", i) + 1])  # RAMPS: deep, shadow, body, sheen, specular
BG = (40, 40, 48, 255)
def big(im, sc): return im.resize((im.width * sc, im.height * sc), Image.NEAREST)

# 1. ribs: native vs stretched, every job, aged tint, 8x
sc = 8; ims = []
for job, f in SRC.items():
    s0 = Image.open(f"{S}/ws_bein/{f}/frame0.png").convert("RGBA")
    ims += [convert(s0, "aged").crop((0, 12, 32, 64)), rows_(convert(s0, "aged"), "stretch").crop((0, 12, 32, 64))]
sheet = Image.new("RGBA", (len(ims) * 33 * sc, 52 * sc), BG)
for k, im in enumerate(ims): sheet.alpha_composite(big(im, sc), (k * 33 * sc, 0))
sheet.save(f"{OUT}/ribs_check.png")

# 2. the orb in every element: Joseph's pattern, and a redrawn sphere
mage = Image.open(f"{S}/ws_bein/{SRC['mage']}/frame0.png").convert("RGBA")
a0 = np.asarray(mage)
glint = gem_glints(a0)
orb = {(y, x) for y in range(64) for x in range(32) if a0[y, x, 3] and (hx(a0, y, x) in GEM or (y, x) in glint) and y < 40}
ys, xs = zip(*orb); cy, cx = (min(ys) + max(ys)) / 2, (min(xs) + max(xs)) / 2; r = max(max(ys) - min(ys), max(xs) - min(xs)) / 2 + 0.5
Lx, Ly, Lz = -0.55, -0.6, 0.58                                   # light from the upper left, towards us
def sphere(im, ramp):
    a = np.asarray(im).copy()
    shade = {}
    for (y, x) in orb:
        nx, ny = (x - cx) / r, (y - cy) / r; nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
        d = nx * Lx + ny * Ly + nz * Lz; shade[(y, x)] = d
    hi = sorted(orb, key=lambda p: -shade[p])[:2]
    for p in orb:
        y, x = p; d = shade[p]; nx, ny = (x - cx) / r, (y - cy) / r
        k = 0 if d < -0.05 else 1 if d < 0.35 else 2 if d < 0.7 else 3
        if nx + ny > 0.95 and k <= 1: k = 2                     # bounce light on the lower right rim: it glows
        c = ramp[4] if p in hi else ramp[k]
        a[y, x, :3] = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
    return Image.fromarray(a)
EL = [e for e in RAMPS if e not in ("Sol",)]
def Lh(h):
    c = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    f = lambda v: ((v/255 + .055)/1.055)**2.4 if v/255 > .04045 else v/255/12.92
    Y = .2126*f(c[0]) + .7152*f(c[1]) + .0722*f(c[2]); return 116*Y**(1/3) - 16
LIFT = {"Natt": ["6b3e75", "905ea9", "a884f3", "eaaded"], "Aska": ["625565", "9babb2", "c7dcd0", "ffffff"],
        "Reyk": ["966c6c", "ab947a", "fdcbb0", "ffffff"]}       # dark ramps step up, or the eyes vanish in the sockets
def gem_of(el): return LIFT.get(el) or RAMPS[el][1:5]
sc = 6; cw = 26
sheet = Image.new("RGBA", (len(EL) * cw * sc, 2 * 34 * sc + 30), BG); d = ImageDraw.Draw(sheet)
for k, el in enumerate(EL):
    ramp = RAMPS[el]
    j = convert(mage, "plain", gem=gem_of(el))
    n = convert(mage, "aged", gem=gem_of(el))
    j.save(f"{OUT}/beinseidr_{el}_joseph.png"); n.save(f"{OUT}/beinseidr_{el}_sphere.png")
    sheet.alpha_composite(big(j.crop((0, 18, 26, 52)), sc), (k * cw * sc, 0))
    sheet.alpha_composite(big(n.crop((0, 18, 26, 52)), sc), (k * cw * sc, 34 * sc + 10))
    d.text((k * cw * sc + 6, 2 * 34 * sc + 14), el, fill=(220, 220, 220))
sheet.save(f"{OUT}/beinseidr_elements.png")

# 3. aged bone options against plain and Drott, on the floor colour
opts = ["plain", "aged_warm", "aged", "aged_moss", "drott"]
sc = 6; sw = Image.open(f"{S}/ws_bein/{SRC['sword']}/frame0.png").convert("RGBA")
sheet = Image.new("RGBA", (len(opts) * 33 * sc, 52 * sc + 24), (62, 53, 70, 255)); d = ImageDraw.Draw(sheet)
for k, t in enumerate(opts):
    sheet.alpha_composite(big(convert(sw, t).crop((0, 12, 32, 64)), sc), (k * 33 * sc, 0))
    d.text((k * 33 * sc + 6, 52 * sc + 6), t, fill=(230, 230, 230))
sheet.save(f"{OUT}/aged_options.png"); print("ok")
