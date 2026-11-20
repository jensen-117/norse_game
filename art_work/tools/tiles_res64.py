"""Snap Joseph's wall and floor tiles to Resurrect 64 (by value onto the cool grey ramp, mortar onto
plum darks) and export them as single PNGs plus Aseprite-importable strips."""
import sys, os, math
from PIL import Image

S, OUT = sys.argv[1], sys.argv[2]
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def L(c):
    f = lambda v: ((v/255 + .055)/1.055)**2.4 if v/255 > .04045 else v/255/12.92
    Y = .2126*f(c[0]) + .7152*f(c[1]) + .0722*f(c[2])
    return 116*(Y**(1/3) if Y > .008856 else 7.787*Y + 16/116) - 16
G = {k: rgb(h) for k, h in dict(d0="2e222f", d1="3e3546", g1="625565", g2="7f708a", g3="9babb2", m="45293f").items()}

def wall(c):
    r, g, b = c; l = L(c)
    if r - b > 30: return G["d0"] if l < 24 else G["m"]
    return G["d1"] if l < 38.6 else G["g1"] if l < 46 else G["g2"] if l < 52 else G["g3"]
def floor(c):
    r, g, b = c; l = L(c)
    if r - b > 30: return G["d0"] if l < 24 else G["m"]
    return G["d0"] if l < 20 else G["d1"] if l < 36 else G["g1"] if l < 52 else G["g2"] if l < 57 else G["g3"]

def snap_set(src_dir, n, fn, name):
    os.makedirs(f"{OUT}/{name}", exist_ok=True)
    tiles = []
    for i in range(n):
        im = Image.open(f"{src_dir}/frame{i}.png").convert("RGBA"); px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a: px[x, y] = fn((r, g, b)) + (255,)
        im.save(f"{OUT}/{name}/{name}_{i}.png"); tiles.append(im)
    w, h = tiles[0].size
    strip = Image.new("RGBA", (w * n, h), (0, 0, 0, 0))
    for i, t in enumerate(tiles): strip.alpha_composite(t, (w * i, 0))
    strip.save(f"{OUT}/{name}_strip.png")
    cols = {p[:3] for t in tiles for p in t.getdata() if p[3]}
    print(name, n, "tiles,", len(cols), "colours:", sorted('%02x%02x%02x' % c for c in cols))
    return tiles

snap_set(f"{S}/ws6/out", 22, wall, "walls")
snap_set(f"{S}/ws7/out", 3, floor, "floors")
