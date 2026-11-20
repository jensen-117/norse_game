"""Generic weapon overlays for the Beinar (a test): sword (Beinbryn), bow (Beinorv), staff (Beinseidr).
The job is the weapon's silhouette; the rank is the bone tint. Anchors are hand-picked per frame (64px cell
coordinates; the skeleton faces left, towards the heroes). Weapons are drawn with a 1px ink outline only
where they cross empty space, so they sit on top of the bones without a halo."""
import sys, os
from PIL import Image, ImageDraw

SRC, OUT = sys.argv[1], sys.argv[2]
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)
INK = rgb("2e222f")
STEEL = [rgb("9babb2"), rgb("c7dcd0")]          # edge, flat
WOOD = [rgb("694f62"), rgb("966c6c")]
GLOW = rgb("a884f3")                             # the staff's Natt stone

def line(x0, y0, x1, y1):
    pts = []; dx, dy = abs(x1 - x0), -abs(y1 - y0); sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1); e = dx + dy
    while True:
        pts.append((x0, y0))
        if (x0, y0) == (x1, y1): return pts
        e2 = 2 * e
        if e2 >= dy: e += dy; x0 += sx
        if e2 <= dx: e += dx; y0 += sy

def stamp(im, pts, colour, outline=True):
    px = im.load(); W, H = im.size
    if outline:
        for x, y in pts:
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                X, Y = x + dx, y + dy
                if 0 <= X < W and 0 <= Y < H and px[X, Y][3] == 0 and (X, Y) not in pts: px[X, Y] = INK
    for i, (x, y) in enumerate(pts):
        if 0 <= x < W and 0 <= y < H: px[x, y] = colour(i) if callable(colour) else colour

def sword(im, hand, tip):
    hx, hy = hand
    blade = line(hx, hy, *tip)[1:]
    stamp(im, blade, lambda i: STEEL[i % 2])
    gx, gy = hand; ux = 1 if tip[0] >= hx else -1; uy = 1 if tip[1] >= hy else -1
    guard = [(gx - uy, gy + ux), (gx, gy), (gx + uy, gy - ux)] if abs(tip[0] - hx) > abs(tip[1] - hy) else [(gx - 1, gy), (gx, gy), (gx + 1, gy)]
    stamp(im, guard, WOOD[0])

def bow(im, hand, span=10, bulge=3, facing=-1):
    hx, hy = hand; arc = []
    for k in range(-span, span + 1):
        x = hx + facing * round(bulge * (1 - (k / span) ** 2)); arc.append((x, hy + k))
    stamp(im, arc, lambda i: WOOD[1] if abs(i - span) < span - 2 else WOOD[0])
    string = [(hx, hy + k) for k in range(-span + 1, span)]
    stamp(im, string, rgb("c7dcd0"), outline=False)

def staff(im, hand, top, bottom):
    hx, hy = hand
    stamp(im, line(hx, top, hx, bottom), lambda i: WOOD[i % 2])
    stamp(im, [(hx, top - 1), (hx - 1, top - 2), (hx, top - 2), (hx + 1, top - 2), (hx, top - 3)], GLOW)

# anchors per frame (64px cell): front hand, plus where the weapon points
FRAMES = {
    "r0c0": dict(hand=(26, 51), sword_tip=(21, 62), bow_hand=(25, 47), staff=(24, 33, 63)),     # idle
    "r0c9": dict(hand=(16, 38), sword_tip=(4, 36), bow_hand=(15, 38), staff=(15, 24, 52)),      # point / aim / cast
    "r4c3": dict(hand=(18, 45), sword_tip=(6, 40), bow_hand=(18, 45), staff=(18, 32, 60)),      # swipe
}
TINTS = ["skeleton_plain", "skeleton_aged", "skeleton_drott"]
os.makedirs(OUT, exist_ok=True)
sc = 5; rows = []
for tint in TINTS:
    row = []
    for job in ("bare", "sword", "bow", "staff"):
        for fr, a in FRAMES.items():
            im = Image.open(f"{SRC}/{tint}/{fr}.png").convert("RGBA")
            if job == "sword": sword(im, a["hand"], a["sword_tip"])
            if job == "bow": bow(im, a["bow_hand"])
            if job == "staff": staff(im, (a["staff"][0], 0), a["staff"][1], a["staff"][2])
            im.save(f"{OUT}/{tint}_{job}_{fr}.png"); row.append(im)
    rows.append(row)
cw = 50
sheet = Image.new("RGBA", (len(rows[0]) * cw * sc, len(rows) * 46 * sc + 20), (40, 40, 48, 255))
d = ImageDraw.Draw(sheet)
for r, row in enumerate(rows):
    for c, im in enumerate(row):
        crop = im.crop((0, 18, cw, 64))
        sheet.alpha_composite(crop.resize((cw * sc, 46 * sc), Image.NEAREST), (c * cw * sc, r * 46 * sc))
for k, job in enumerate(("bare", "sword (Beinbryn)", "bow (Beinorv)", "staff (Beinseidr)")):
    d.text((k * 3 * cw * sc + 6, len(rows) * 46 * sc + 4), job, fill=(220, 220, 220))
sheet.save(f"{OUT}/beinar_weapons_test.png")
print("ok")
