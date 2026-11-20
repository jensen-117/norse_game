"""Joseph's Beinar starters (sword and shield, mage, two archers; Nov 7) -> Res64, in the three rank tints
and the three sizes. Only BONE colours are tinted; weapons keep their own colours. Sizes: cut 6 rows (32),
native (38), stretch the same 6 rows (44)."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
S, OUT = sys.argv[1], sys.argv[2]
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
RES = set(open(f"{S}/tools/res64.txt").read().split())
SRC = {"sword": "0112770b-skeleton_sword_1", "mage": "2ad1d17e-skeleton_mage_1",
       "archer": "1233632c-skeleton_archer_1", "longbow": "4b9b597a-skeleton_archer_2"}
BONE_SRC = ["474747", "b6a8a2", "c9c9c9", "ffffff"]              # shadow, mid, light, highlight
BONE = {"plain": ["3e3546", "9babb2", "c7dcd0", "ffffff"],
        "aged":  ["694f62", "ab947a", "b2ba90", "c7dcd0"],         # cooler: barrow tan in the shadows, ivory on top
        "aged_warm": ["694f62", "966c6c", "ab947a", "fdcbb0"],     # the first try (read as skin)
        "aged_moss": ["625565", "92a984", "b2ba90", "c7dcd0"],     # cooler still: mossy
        "drott": ["7a3045", "cf657f", "f68181", "fca790"]}
FIXED = {"13131c": "2e222f", "342726": "694f62", "3b3b46": "3e3546", "694e3d": "966c6c", "a26f4f": "ab947a"}   # bows: lighter wood, readable on stone
GEM = {"4d65b4", "4d9be6", "8ff8e2"}
CUT = [4, 6, 8, 10, 22, 23]       # rows from the bottom: four leg rows, and one rib bar (22) with the gap above it (23)
RIB_PAIR = (23, 22)               # stretched as a PAIR, so every rib bar keeps its 1px ink gap
GLINT_SRC = {"ffffff", "c9c9c9", "b6a8a2"}
def hx(a, y, x): return "%02x%02x%02x" % tuple(a[y, x, :3])
def gem_glints(a):
    """Light pixels joined to the orb (through other light pixels) belong to the orb, not to the bone."""
    H, W = a.shape[:2]; seen = set()
    gem = {(y, x) for y in range(H) for x in range(W) if a[y, x, 3] and hx(a, y, x) in GEM}
    comps = []                                   # the orb is the biggest blob of gem colour (eyes and runes are small)
    left = set(gem)
    while left:
        st = [left.pop()]; comp = set(st)
        while st:
            y, x = st.pop()
            for j in (-1, 0, 1):
                for i in (-1, 0, 1):
                    q = (y + j, x + i)
                    if q in left: left.discard(q); comp.add(q); st.append(q)
        comps.append(comp)
    if not comps: return seen
    stack = list(max(comps, key=len))
    while stack:
        y, x = stack.pop()
        for j in (-1, 0, 1):
            for i in (-1, 0, 1):
                Y, X = y + j, x + i
                if 0 <= Y < H and 0 <= X < W and (Y, X) not in seen and a[Y, X, 3] and hx(a, Y, X) in GLINT_SRC:
                    seen.add((Y, X)); stack.append((Y, X))
    return seen
def convert(im, tint, gem=None):
    a = np.asarray(im.convert("RGBA")).copy(); glint = gem_glints(a)
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if not a[y, x, 3]: continue
            h = hx(a, y, x)
            if (y, x) in glint: t = gem[3] if gem else "ffffff"
            elif h in GEM and gem: t = gem[["4d65b4", "4d9be6", "8ff8e2"].index(h)]
            else: t = BONE[tint][BONE_SRC.index(h)] if h in BONE_SRC else FIXED.get(h, h)
            assert t in RES, (h, t); a[y, x, :3] = rgb(t)
    return Image.fromarray(a)
def rows_(im, mode):
    if mode == "native": return im
    a = np.asarray(im); bb = im.getbbox(); bottom = bb[3] - 1; out = []
    row_at = {bottom - y: a[y] for y in range(a.shape[0])}
    for y in range(a.shape[0]):
        k = bottom - y
        if k in CUT and mode == "cut": continue
        out.append(a[y])
        if mode == "stretch":
            if k == RIB_PAIR[1]: out += [row_at[RIB_PAIR[0]], row_at[RIB_PAIR[1]]]     # gap + bar again
            elif k in CUT and k not in RIB_PAIR: out.append(a[y])
    out = np.array(out); pad = 64 - out.shape[0]                # keep the 64px canvas, feet on the bottom
    if pad > 0: out = np.concatenate([np.zeros((pad, out.shape[1], 4), np.uint8), out])
    return Image.fromarray(out[-64:] if pad < 0 else out)
os.makedirs(OUT, exist_ok=True)
COLS = [("plain", "cut"), ("plain", "native"), ("aged", "native"), ("aged", "stretch"), ("drott", "stretch")]
sc = 6; cw = 34
sheet = Image.new("RGBA", (len(COLS) * cw * sc + 20, len(SRC) * 52 * sc + 30), (40, 40, 48, 255)); d = ImageDraw.Draw(sheet)
for r, (job, f) in enumerate(SRC.items()):
    src = Image.open(f"{S}/ws_bein/{f}/frame0.png").convert("RGBA")
    for c, (tint, size) in enumerate(COLS):
        im = rows_(convert(src, tint), size); im.save(f"{OUT}/beinar_{job}_{tint}_{size}.png")
        crop = im.crop((0, 12, 32, 64))
        sheet.alpha_composite(crop.resize((32 * sc, 52 * sc), Image.NEAREST), (10 + c * cw * sc, r * 52 * sc))
for c, (tint, size) in enumerate(COLS):
    d.text((10 + c * cw * sc, len(SRC) * 52 * sc + 8), f"{tint}, {size}", fill=(220, 220, 220))
sheet.save(f"{OUT}/beinar_ladder.png"); print("ok")
