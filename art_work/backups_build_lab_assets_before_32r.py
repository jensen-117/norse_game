"""Fight Lab assets: one sprite atlas (+ faces and feet), backgrounds per area, Joseph's font, the board geometry.
python3 build_lab_assets.py  ->  /home/claude/fight_lab/assets/"""
import json, os, sys
sys.path.insert(0, "/home/claude/art_work/tools"); sys.path.insert(0, "/home/claude/sim")
from PIL import Image
import screen_bg as sb
OUT = "/home/claude/fight_lab/assets"; ART = "/home/claude/art_res64"
ELEMENTS = ["Eld", "Reyk", "Vatn", "Hrim", "Blast", "Blixt", "Jord", "Gro", "Sol", "Lak", "Natt", "Aska"]
sets = {}          # key -> dict(anims={name: [Image]}, face=mode)
def load(p): return Image.open(p).convert("RGBA")

# ---- heroes: the side wizard, one colour per class (martial classes borrow a caster's colours for now)
HF = f"{ART}/heroes/wizard_side_v2/frames"
CASTERS = ["Brennumar", "Dagskald", "Hafrunar", "Lundar", "Seidar", "Skurmar"]
for c in CASTERS:
    a = lambda *n: [load(f"{HF}/{c}_right_{x}.png") for x in n]
    sets[f"hero:{c}"] = dict(anims=dict(idle=a("idle1", "idle2", "idle3", "idle2"), hit=a("hit"), defend=a("defend"),
                                        defend_hit=a("defend_hit"), downed=a("downed"), cast=a("spell1"),
                                        attack=a("charge1", "charge2", "charge3"), item=a("bomb1", "bomb2")), face="top")
# ---- the Mogel: 16/24/32 px bodies, every element
SF = f"{ART}/slimes/frames"
for el in ELEMENTS:
    for size in (16, 24, 32):
        a = lambda *n: [load(f"{SF}/Mogel{size}_{el}_{x}.png") for x in n]
        sets[f"mogel{size}:{el}"] = dict(anims=dict(idle=a("idle1", "idle2"), hit=a("hit1", "hit2"), cast=a("cast1", "cast2", "cast3"),
                                                    attack=a("breathe1", "breathe2", "cast3"), defend=a("withdraw"), reform=a("surprise")),
                                         face="mid")
# ---- the Ande
import glob as _glob
def frames_of(pattern):        # whatever frames exist, in order (the Aska spirits have fewer)
    return [load(p) for p in sorted(_glob.glob(pattern), key=lambda p: int(p.rsplit("_", 1)[1].split(".")[0]))]
for el in ELEMENTS:
    # the names elide like the words do: Halv+vatn -> Halvatnande, aska+ande -> Askande
    halv = {"Vatn": "Halvatnande", "Aska": "Halvaskande"}.get(el, f"Halv{el.lower()}ande")
    whole = {"Aska": "Askande"}.get(el, f"{el}ande")
    fr = frames_of(f"{ART}/spirits/halvande/{halv}_*.png")
    if fr: sets[f"halvande:{el}"] = dict(anims=dict(idle=fr, hit=[fr[min(2, len(fr) - 1)]], cast=[fr[-1]], attack=[fr[-1]]), face="mid")
    fr = frames_of(f"{ART}/spirits/ande/{whole}_*.png")
    if fr: sets[f"ande:{el}"] = dict(anims=dict(idle=fr[:max(1, len(fr) - 2)], hit=[fr[-2]], cast=[fr[-1]], attack=[fr[-1]]), face="top")
# ---- the Draugr: Gandalf Hardcore's zombie rows (idle, slash, recoil, the fall, the crawl)
DF = f"{ART}/undead/draugr/frames"
def rc(d, cells): return [load(f"{DF}/{d}/r{r}c{c}.png") for r, c in cells]
SEQ = [(r, c) for r in range(8) for c in range(10) if not (r == 7 and c == 9)]
def seq(a, b): return SEQ[SEQ.index(a):SEQ.index(b) + 1]
for key, d in (("Halvdraugr", "draugr_pale_cut"), ("Draugr", "draugr_blar_native"), ("Stordraugr", "draugr_blar_stretch"),
               ("Forndraugr", "draugr_drott_stretch"), ("Gandraugr", "draugr_pale_native")):
    sets[f"draugr:{key}"] = dict(anims=dict(idle=rc(d, seq((0, 0), (0, 6))), attack=rc(d, seq((1, 6), (1, 9))), hit=rc(d, seq((4, 0), (4, 2))),
                                            fall=rc(d, seq((4, 3), (5, 4))), crawl=rc(d, seq((6, 0), (6, 9))), cast=rc(d, [(1, 6)])), face="top")
# ---- the Beinar: one idle frame each (they shake when hit, drop when they fall)
BF = f"{ART}/undead/beinar"
BEIN = {"Halvbeinbryn": "beinar_sword_plain_cut", "Beinbryn": "beinar_sword_aged_native", "Storbeinbryn": "beinar_sword_aged_stretch",
        "Halvbeinorv": "beinar_archer_plain_cut", "Beinorv": "beinar_archer_aged_native", "Storbeinorv": "beinar_longbow_aged_stretch",
        "Halvbeinseidr": "beinar_mage_plain_cut", "Storbeinseidr": "beinar_mage_aged_stretch", "Fornbein": "beinar_sword_drott_stretch"}
for k, f in BEIN.items(): sets[f"bein:{k}"] = dict(anims=dict(idle=[load(f"{BF}/{f}.png")]), face="skull")
for el in ["Natt", "Aska", "Eld", "Hrim", "Blixt"]:
    p = f"{BF}/beinseidr_{el}_joseph.png"
    if os.path.exists(p): sets[f"bein:Beinseidr:{el}"] = dict(anims=dict(idle=[load(p)]), face="skull")

# ---- crop every set to the union of its frames (so the feet stay put), find the face, pack
def skull_face(im):
    px = im.load(); W, H = im.size
    light = {(x, y) for x in range(W) for y in range(H) if px[x, y][3] and sum(px[x, y][:3]) > 560 and max(px[x, y][:3]) - min(px[x, y][:3]) < 40}
    seen, comps = set(), []
    for s in light:
        if s in seen: continue
        q, c = [s], []; seen.add(s)
        while q:
            x, y = q.pop(); c.append((x, y))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n in light and n not in seen: seen.add(n); q.append(n)
        xs = [x for x, _ in c]; ys = [y for _, y in c]
        if 6 <= max(xs) - min(xs) + 1 <= 10 and len(c) > 12: comps.append((min(ys), min(xs), max(xs)))
    if not comps: return None
    # the skull sits over the spine: of the high blobs, take the one nearest the body's centre line (an orb held
    # out to the side is as big as a skull, and higher)
    body = [x for x in range(W) for y in range(H // 2, H) if px[x, y][3]]
    mid = sorted(body)[len(body) // 2] if body else W // 2
    top = min(c[0] for c in comps)
    cand = [c for c in comps if c[0] <= top + 8]
    y, x0, x1 = min(cand, key=lambda c: abs((c[1] + c[2]) / 2 - mid))
    # an orb above the skull (Beinseidr) is round and small: prefer the second if the first is narrow and high
    return ((x0 + x1) // 2 - 4, y - 1)
def face_of(im, mode):
    bb = im.getbbox(); x0, y0, x1, y1 = bb
    if mode == "skull":
        f = skull_face(im)
        if f: return f
    if mode == "mid": return ((x0 + x1) // 2 - 4, (y0 + y1) // 2 - 4)
    cols = [x for x in range(x0, x1) for y in range(y0, min(y1, y0 + 8)) if im.getpixel((x, y))[3]]
    cx = (min(cols) + max(cols) + 1) // 2 if cols else (x0 + x1) // 2
    return (cx - 4, y0)
frames, meta = [], {}
for key, s in sets.items():
    allf = [f for fr in s["anims"].values() for f in fr]
    ub = None
    for f in allf:
        b = f.getbbox()
        if b: ub = b if ub is None else (min(ub[0], b[0]), min(ub[1], b[1]), max(ub[2], b[2]), max(ub[3], b[3]))
    m = dict(anims={}, w=ub[2] - ub[0], h=ub[3] - ub[1])
    fx, fy = face_of(s["anims"]["idle"][0], s["face"])
    m["face"] = [fx - ub[0], fy - ub[1]]
    m["foot"] = [m["w"] // 2, m["h"]]                    # bottom centre of the union box
    for an, fr in s["anims"].items():
        m["anims"][an] = []
        for f in fr: frames.append((key, an, f.crop(ub))); m["anims"][an].append(len(frames) - 1)
    meta[key] = m
# shelf packing, tallest first
order = sorted(range(len(frames)), key=lambda i: -frames[i][2].height)
AW, x, y, rowh, rects = 1024, 0, 0, 0, {}
for i in order:
    im = frames[i][2]
    if x + im.width > AW: x, y, rowh = 0, y + rowh + 1, 0
    rects[i] = (x, y, im.width, im.height); x += im.width + 1; rowh = max(rowh, im.height)
atlas = Image.new("RGBA", (AW, y + rowh + 1), (0, 0, 0, 0))
for i, r in rects.items(): atlas.paste(frames[i][2], r[:2])
for key, m in meta.items():
    for an in m["anims"]: m["anims"][an] = [list(rects[i]) for i in m["anims"][an]]
atlas.save(f"{OUT}/atlas.png", optimize=True)
# ---- backgrounds: the room per area, the text box frame with a clear window (the watercolor goes under it)
geo = None; areas = {}
for area in ("Neutral", "Vatn", "Eld"):
    # the roomier board (Nov 8): cells 44 px (one slab), one slab between the armies, the floor lifted 14 px into the wall
    LAYOUT = dict(lanes=[(50, 24), (74, 26), (100, 31)], pitch=44, front=131, gx=[38, 82, 170, 214])
    im, geo = sb.scene(area, dressed=True, dy=14, layout=LAYOUT)
    # the text box is Joseph's cord frame, drawn by the page: here, ink under it and a clear window inside
    FR = (9, 131, 310, 177)                      # the cord's outer rect (x1 - x0 = 1, y1 - y0 = 2, mod 4)
    from PIL import ImageDraw
    ImageDraw.Draw(im).rectangle((0, 131, 319, 179), fill=sb.INK + (255,))
    for yy in range(FR[1], FR[3] + 1):           # clear under the whole cord: the page fills inside it, notches and all
        for xx in range(FR[0], FR[2] + 1): im.putpixel((xx, yy), (0, 0, 0, 0))
    im.save(f"{OUT}/bg_{area}.png", optimize=True)
    band, tint, rune = sb.AREAS[area]
    areas[area] = dict(frame=list(FR), box=[FR[0] + 3, FR[1] + 3, FR[2] - 3, FR[3] - 3], tint=["#" + t for t in tint], band=["#" + b for b in band])
# ---- the tracker frame (Joseph's), window cleared to the frame brown
tr = Image.open("/tmp/claude-0/-home-claude/83f4fe98-00ce-598d-b46d-8b8b896bc028/scratchpad/tracker/frame0.png").convert("RGBA")
for yy in range(3, 13):
    for xx in range(3, 126): tr.putpixel((xx, yy), (0xcd, 0x68, 0x3d, 255))
tr.save(f"{OUT}/tracker.png")
# ---- Joseph's font: ink pixels per glyph, relative to the glyph's left edge and the cap band
f = sb.font; glyphs = {}
for ch, ink in f.glyphs.items():
    if not ink: glyphs[ch] = dict(w=3, px=[]); continue
    x0 = min(x for x, _ in ink)
    glyphs[ch] = dict(w=f.width(ch), px=[[x - x0, y - f.top] for x, y in ink])
json.dump(dict(sprites=meta, geo=geo, areas=areas, font=dict(height=f.height, glyphs=glyphs)), open(f"{OUT}/assets.json", "w"), separators=(",", ":"))
print(len(sets), "sets", len(frames), "frames, atlas", atlas.size, os.path.getsize(f"{OUT}/atlas.png") // 1024, "KB;",
      os.path.getsize(f"{OUT}/assets.json") // 1024, "KB json")
