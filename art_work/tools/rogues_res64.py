"""32rogues (Seth Boyles) -> Resurrect 64.

The four sheets share one 59-colour palette (palette.png, 16x4), so the whole job is one palette map:
each 32rogues colour goes to a *distinct* Res64 colour (an optimal assignment in OKLab), so no two shades of a
ramp collapse into one. Lightness is weighted up so ramps keep their order. Overrides go in FIX.

    python3 rogues_res64.py            # writes art_res64/rogues/*.png, the map, and before/after sheets
"""
import os, json
import numpy as np
from PIL import Image
from scipy.optimize import linear_sum_assignment

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "sources", "32rogues")
OUT = os.path.join(HERE, "..", "..", "art_res64", "rogues")
RES = open(os.path.join(HERE, "res64.txt")).read().split()
SHEETS = ["rogues", "monsters", "animals", "items"]
FIX = {                  # "32rogues hex": "res64 hex" -- hand overrides after review
    # steel and stone greys onto Res64's cool grey ramp (3e3546 625565 7f708a 9babb2 c7dcd0), not olive or tan
    "323c39": "3e3546", "696a6a": "625565", "6f5756": "694f62", "999f8e": "9babb2", "d3d9b2": "c7dcd0",
    # blue-greys (cloaks, the lich, snakes): stay blue
    "17394a": "323353", "3b6983": "484a77", "748f93": "7f708a", "a5b5d4": "9babb2", "cdd1ec": "c7dcd0",
    # skin: off the saturated oranges
    "e17b50": "e6904e", "fb9b72": "fca790", "a84111": "9e4539",
}
W_L = 2.0                # lightness weight: keep ramps ordered

rgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
hexs = lambda c: "%02x%02x%02x" % tuple(c[:3])

def oklab(c):
    c = np.array(c[:3], float) / 255
    c = np.where(c > .04045, ((c + .055) / 1.055) ** 2.4, c / 12.92)
    l = .4122214708 * c[0] + .5363325363 * c[1] + .0514459929 * c[2]
    m = .2119034982 * c[0] + .6806995451 * c[1] + .1073969566 * c[2]
    s = .0883024619 * c[0] + .2817188376 * c[1] + .6299787005 * c[2]
    l, m, s = np.cbrt([l, m, s])
    return np.array([.2104542553 * l + .7936177850 * m - .0040720468 * s,
                     1.9779984951 * l - 2.4285922050 * m + .4505937099 * s,
                     .0259040371 * l + .7827717662 * m - .8086757660 * s])

pal = Image.open(f"{SRC}/palette.png").convert("RGBA")
src = []
for y in range(pal.height):
    for x in range(pal.width):
        c = pal.getpixel((x, y))
        if c[3] and hexs(c) not in src: src.append(hexs(c))
A = np.array([oklab(rgb(h)) for h in src]); B = np.array([oklab(rgb(h)) for h in RES])
w = np.array([W_L, 1, 1])
cost = np.sqrt((((A[:, None, :] - B[None, :, :]) * w) ** 2).sum(-1))
# Plain nearest. 32rogues has ~10 tinted near-blacks where Res64 has one ink, so they fold into ink (that is how
# Res64 sprites are outlined anyway); greys and skins that land on the wrong Res64 ramp are set by hand in FIX.
INK, INK_L = "2e222f", .22
MAP = {s: (INK if A[i][0] < INK_L else RES[int(np.argmin(cost[i]))]) for i, s in enumerate(src)}
MAP.update(FIX)
d = {s: float(cost[i, RES.index(MAP[s])]) for i, s in enumerate(src)}

os.makedirs(OUT, exist_ok=True)
json.dump(MAP, open(f"{OUT}/map.json", "w"), indent=0)
for name in SHEETS:
    im = Image.open(f"{SRC}/{name}.png").convert("RGBA"); a = np.array(im)
    out = a.copy()
    for s, t in MAP.items():
        m = (a[..., :3] == rgb(s)).all(-1) & (a[..., 3] > 0)
        out[m, :3] = rgb(t)
    Image.fromarray(out).save(f"{OUT}/{name}.png")
    both = Image.new("RGBA", (im.width * 2 + 8, im.height), (46, 34, 47, 255))
    both.alpha_composite(im, (0, 0)); both.alpha_composite(Image.fromarray(out), (im.width + 8, 0))
    both.resize((both.width * 2, both.height * 2), Image.NEAREST).save(f"{OUT}/compare_{name}.png")

# the swap card: source swatch -> Res64 swatch, worst matches flagged
order = sorted(src, key=lambda s: -d[s])
card = Image.new("RGBA", (2 * 12 + 4, len(order) * 6), (46, 34, 47, 255))
for k, s in enumerate(order):
    card.paste(rgb(s) + (255,), (0, k * 6, 12, k * 6 + 5)); card.paste(rgb(MAP[s]) + (255,), (16, k * 6, 28, k * 6 + 5))
card.resize((card.width * 6, card.height * 6), Image.NEAREST).save(f"{OUT}/map_card.png")
print("worst:", [(s, MAP[s], round(d[s], 3)) for s in order[:8]])
print("mean", round(float(np.mean(list(d.values()))), 3))
