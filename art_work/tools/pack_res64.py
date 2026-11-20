"""Dungeon dressing pack -> Resurrect 64 library.
Each item is cut from its sheet, scaled (box filter), then every pixel is snapped by MATERIAL:
  stone (low saturation)  -> the neutral stone slots 3e3546 / 625565 / 7f708a / 9babb2 (+ 2e222f ink)
  wood, cloth, leather    -> 694f62 / 966c6c / ab947a (muted warm, none shared with the walls)
  the pack's dark brown outline (L < 22, any hue) -> 2e222f ink
  flame / gold (yellow)   -> f79617 / f9c22b / fbff86
Stone uses the same slots as the walls, so the area recolor (Vatn blue stone, Eld warm stone) carries
over to every prop for free. Cobwebs and cracks are single-colour decals tinted per area at place time."""
import sys, os, colorsys
import numpy as np
from PIL import Image, ImageDraw

S, OUT = sys.argv[1], sys.argv[2]
P = f"{S}/pack"
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def L(c):
    f = lambda v: ((v/255 + .055)/1.055)**2.4 if v/255 > .04045 else v/255/12.92
    Y = .2126*f(c[0]) + .7152*f(c[1]) + .0722*f(c[2]); return 116*Y**(1/3) - 16 if Y > .008856 else 903.3*Y
INK = rgb("2e222f")
STONE = [rgb(h) for h in ("3e3546", "625565", "7f708a", "9babb2")]
WOOD = [rgb(h) for h in ("6e2727", "694f62", "966c6c", "ab947a")]
FLAME = [rgb(h) for h in ("f79617", "f9c22b", "fbff86")]

def snap(c):
    r, g, b = c; h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255); l = L(c)
    if l < 22: return INK
    if s > 0.45 and 0.08 < h < 0.19 and l > 55: return FLAME[0] if l < 68 else FLAME[1] if l < 82 else FLAME[2]
    if s > 0.25 and (h < 0.12 or h > 0.93):
        return INK if l < 26 else WOOD[1] if l < 34 else WOOD[2] if l < 44 else WOOD[3]
    return STONE[0] if l < 27.5 else STONE[1] if l < 35 else STONE[2] if l < 42 else STONE[3]

def cut(sheet, box, scale):
    x, y, w, h = box
    im = Image.open(f"{P}/src/{sheet}").convert("RGBA").crop((x, y, x + w, y + h))
    if scale != 1:
        a = np.asarray(im).astype(float); al = a[..., 3:4] / 255
        prem = np.concatenate([a[..., :3] * al, al * 255], axis=2).astype(np.uint8)
        nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
        sm = np.asarray(Image.fromarray(prem, "RGBA").resize((nw, nh), Image.BOX)).astype(float)
        alpha = sm[..., 3:4] / 255
        col = np.where(alpha > 0, sm[..., :3] / np.maximum(alpha, 1e-6), 0)
        im = Image.fromarray(np.concatenate([np.clip(col, 0, 255), sm[..., 3:4]], axis=2).astype(np.uint8), "RGBA").copy()
    px = im.load()
    for yy in range(im.height):
        for xx in range(im.width):
            r, g, b, a = px[xx, yy]
            px[xx, yy] = (snap((r, g, b)) + (255,)) if a >= 128 else (0, 0, 0, 0)
    return im

def decal(sheet, box, scale, thresh):
    """Single-colour decal (webs, cracks): alpha mask only, coloured when placed."""
    x, y, w, h = box
    im = Image.open(f"{P}/src/{sheet}").convert("RGBA").crop((x, y, x + w, y + h))
    if scale != 1: im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.BOX)
    a = np.asarray(im)[..., 3]
    return Image.fromarray(np.where(a >= thresh, 255, 0).astype(np.uint8), "L")

def boxes(name):
    out = {}
    for line in open(f"{P}/{name}_boxes.txt"):
        i, x, y, w, h = map(int, line.split()); out[i] = (x, y, w, h)
    return out

BR, PR = boxes("bricks"), boxes("props")
LIB = {   # name: (sheet, box, scale)
    "breach": ("bricks.png", BR[2], 0.5), "hole": ("bricks.png", BR[0], 0.5),
    "slit_a": ("bricks.png", BR[4], 0.5), "slit_b": ("bricks.png", BR[5], 0.5),
    "cell_door": ("bricks.png", BR[3], 0.5), "patch_big": ("bricks.png", BR[12], 0.5),
    "double_door": ("bricks.png", BR[14], 0.5), "arch": ("bricks.png", BR[16], 0.5),
    "window_grate": ("props.png", PR[95], 0.5), "window_cross": ("props.png", PR[96], 0.5),
    "window_arch": ("props.png", PR[129], 0.5), "window_arch_lit": ("props.png", PR[132], 0.5),
    "banner_a": ("props.png", PR[159], 0.5), "banner_b": ("props.png", PR[160], 0.5), "banner_torn": ("props.png", PR[161], 0.5),
    "skeleton": ("props.png", PR[111], 0.5), "cage_bones": ("props.png", PR[219], 0.5),
    "barrel": ("props.png", PR[126], 0.5), "barrel_lid": ("props.png", PR[125], 0.5), "cask": ("props.png", PR[143], 0.5),
    "lantern": ("props.png", PR[141], 0.5), "candle": ("props.png", PR[142], 0.5),
    "chandelier": ("props.png", PR[140], 0.5), "cauldron": ("props.png", PR[164], 0.5),
    "alcove_statue": ("props.png", PR[249], 0.5), "alcove_relic": ("props.png", PR[250], 0.5),
    "statue_knight": ("props.png", PR[181], 0.5), "statue_mourner": ("props.png", PR[183], 0.5),
    "fireplace": ("props.png", PR[137], 0.5), "great_door": ("props.png", PR[265], 0.5),
    "coffin": ("props.png", PR[247], 0.5), "chest": ("props.png", PR[266], 0.5),
    "rubble": ("props.png", PR[230], 0.5), "spiked_ball": ("props.png", PR[222], 0.5),
}
os.makedirs(f"{OUT}/props", exist_ok=True); os.makedirs(f"{OUT}/decals", exist_ok=True)
items = {}
for name, (sheet, box, sc) in LIB.items():
    items[name] = cut(sheet, box, sc); items[name].save(f"{OUT}/props/{name}.png")

# decals: webs at 3/4 size (their 1px threads survive), cracks at full size
import subprocess
for nm in ("webs", "cracks"):
    subprocess.run(["python3", "-I", f"{S}/tools/components.py", f"{P}/src/{nm}.png", f"{P}/{nm}_boxes.png", "2"],
                   stdout=open(f"{P}/{nm}_boxes.txt", "w"), check=True)
WB, CB = boxes("webs"), boxes("cracks")
dec = {}
for i, b in WB.items():
    dec[f"web_{i}"] = decal("webs.png", b, 0.75, 60)
for i, b in CB.items():
    if b[3] < 30: dec[f"crack_{i}"] = decal("cracks.png", b, 1.0, 100)
for n, m in dec.items(): m.save(f"{OUT}/decals/{n}.png")

# library sheet
names = list(items); cols = 9; sc = 3; cell = 64
sheet = Image.new("RGBA", (cols * cell * sc, (-(-len(names) // cols)) * (cell + 12) * sc), (40, 40, 48, 255))
d = ImageDraw.Draw(sheet)
for k, n in enumerate(names):
    x, y = (k % cols) * cell * sc, (k // cols) * (cell + 12) * sc
    im = items[n]
    f = min(sc, (cell * sc - 8) // max(im.width, im.height, 1)) or 1
    sheet.alpha_composite(im.resize((im.width * f, im.height * f), Image.NEAREST), (x + 4, y + 4))
    d.text((x + 4, y + cell * sc + 4), f"{n} {im.width}x{im.height}", fill=(220, 220, 220))
sheet.save(f"{OUT}/dressing_library.png")
used = {p[:3] for im in items.values() for p in im.getdata() if p[3]}
print(len(items), "props,", len(dec), "decals; colours:", sorted('%02x%02x%02x' % c for c in used))
