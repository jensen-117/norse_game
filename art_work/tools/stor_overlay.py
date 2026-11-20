"""Draft: carry the boss slime's skull and crossbones into all 11 Mogel frames.
The bones are cut from Joseph's boss frame, anchored to each frame's body (centre of its bounding box),
clipped to the body INTERIOR, and drawn under the slime's sheen and specular, so they read as inside.
Bones use the ramp's sheen slot, the skull's eyes the deep slot: seen through the slime, they take its colour."""
import sys, os
from PIL import Image, ImageDraw
S, OUT = sys.argv[1], sys.argv[2]
src = open(f"{S}/tools/slime_res64.py").read()
sys.argv = [sys.argv[0], S, "/dev/null"]
KEEP = OUT
exec(src[:src.index('for d in ("frames", "strips", "gifs")')])     # slot grids G, RAMPS, render, LABELS
OUT = KEEP

boss = Image.open(f"{S}/ws11/out/frame0.png").convert("RGBA")
BONE, EYE = (167, 170, 132), (75, 73, 40)
layer = {(x, y): ('B' if boss.getpixel((x, y))[:3] == BONE else 'E')
         for y in range(32) for x in range(32)
         if boss.getpixel((x, y))[3] and boss.getpixel((x, y))[:3] in (BONE, EYE)}
def bbox(g):
    pts = [(x, y) for y, r in enumerate(g) for x, c in enumerate(r) if c != '.']
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)
bb = [(x, y) for y in range(32) for x in range(32) if boss.getpixel((x, y))[3]]
bcx = (min(p[0] for p in bb) + max(p[0] for p in bb)) / 2; bcy = (min(p[1] for p in bb) + max(p[1] for p in bb)) / 2

def overlay(g):
    x0, y0, x1, y1 = bbox(g); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = round(cx - bcx), round(cy - bcy)
    out = [r[:] for r in g]
    for (x, y), k in layer.items():
        X, Y = x + dx, y + dy
        if not (0 <= X < 32 and 0 <= Y < 32): continue
        if out[Y][X] not in '012': continue             # inside only: never over outline, sheen, or glint
        # stay one pixel in from the outline so the bones never touch the skin
        if any(0 <= X+a < 32 and 0 <= Y+b < 32 and g[Y+b][X+a] in '.O' for a, b in ((1,0),(-1,0),(0,1),(0,-1))): continue
        out[Y][X] = k
    return out

def render2(g, ramp):
    pal = {'O': rgb(OUTLINE), 'B': rgb(ramp[3]), 'E': rgb(ramp[0]), **{str(k): rgb(h) for k, h in enumerate(ramp)}}
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    for y in range(32):
        for x in range(32):
            if g[y][x] != '.': im.putpixel((x, y), pal[g[y][x]] + (255,))
    return im

GS = [overlay(g) for g in G[32]]
os.makedirs(f"{OUT}/stormogel/frames", exist_ok=True)
for el, ramp in RAMPS.items():
    for i, g in enumerate(GS): render2(g, ramp).save(f"{OUT}/stormogel/frames/Stormogel_{el}_{LABELS[i]}.png")
sc = 5
sh = Image.new("RGBA", (11 * (32 * sc + 6) + 6, 2 * (32 * sc + 6) + 6), (40, 40, 48, 255))
for i in range(11):
    sh.alpha_composite(render(G[32][i], RAMPS["Jord"]).resize((32 * sc, 32 * sc), Image.NEAREST), (6 + i * (32 * sc + 6), 6))
    sh.alpha_composite(render2(GS[i], RAMPS["Jord"]).resize((32 * sc, 32 * sc), Image.NEAREST), (6 + i * (32 * sc + 6), 32 * sc + 12))
sh.save(f"{OUT}/stormogel/stormogel_draft_frames.png")
fam = Image.new("RGBA", (6 * (32 * 4 + 8) + 8, 2 * (32 * 4 + 8) + 8), (40, 40, 48, 255))
for k, el in enumerate(RAMPS):
    fam.alpha_composite(render2(GS[0], RAMPS[el]).resize((128, 128), Image.NEAREST), (8 + (k % 6) * 136, 8 + (k // 6) * 136))
fam.save(f"{OUT}/stormogel/stormogel_elements.png")
# Joseph's original frame next to the draft idle, for the read check
cmp_ = Image.new("RGBA", (3 * 256 + 32, 272), (40, 40, 48, 255))
cmp_.alpha_composite(boss.resize((256, 256), Image.NEAREST), (8, 8))
cmp_.alpha_composite(render2(GS[0], RAMPS["Jord"]).resize((256, 256), Image.NEAREST), (272, 8))
cmp_.alpha_composite(render2(GS[0], RAMPS["Vatn"]).resize((256, 256), Image.NEAREST), (536, 8))
cmp_.save(f"{OUT}/stormogel/boss_vs_draft.png")
print("ok")
