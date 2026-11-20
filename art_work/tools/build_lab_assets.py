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

# ---- heroes: Joseph's 32R picks (heroes_1.aseprite, Nov 10), several looks per class, picked per hero by id.
# 32R faces left; heroes stand on the left, so they're mirrored. Static (life from code motions); the downed pose
# is the body laid on its back, head away from the foe. 18 and 20 (spearmen) wait for a spear class.
HR = lambda i: load(f"/home/claude/art_work/heroes32/frame{i - 1}.png").transpose(Image.FLIP_LEFT_RIGHT)
HERO32 = {"Ullar": [3, 5], "Nalarbani": [2, 4], "Hersir": [6, 7], "Huskarl": [1, 15], "Berserker": [16], "Vasara": [11],
          "Brennumar": [8], "Hafrunar": [14], "Skurmar": [10], "Lundar": [13], "Dagskald": [9], "Seidar": [12]}
def laid(im):
    b = im.getbbox(); return im.crop(b).rotate(90, expand=True)
# Magicals (Nov 10): school uniforms. Every magical body wears every school's robe (art_work/tools/uniforms.py), so
# a magical class draws from all six bodies in its own colours; a body in its own school keeps Joseph's colours.
import uniforms as UN
MAGICAL_BODIES = [8, 9, 10, 12, 13, 14]
for c, frs in HERO32.items():
    school = UN.SCHOOL_OF.get(c)
    looks = [UN.uniform(fr, school).transpose(Image.FLIP_LEFT_RIGHT) for fr in MAGICAL_BODIES] if school else [HR(fr) for fr in frs]
    for n, im in enumerate(looks, 1):
        sets[f"hero:{c}#{n}"] = dict(anims=dict(idle=[im], downed=[laid(im)]), face="top")
# ---- the Mogel: 16/24/32 px bodies, every element
SF = f"{ART}/slimes/frames"
from mogel_dull import dull
MOGEL_DULL = 2          # Nov 9: the glint and its halo come off (back-filled from the body); Joseph will round them out later
for el in ELEMENTS:
    for size in (16, 24, 32):
        a = lambda *n: [load(f"{SF}/Mogel{size}_{el}_{x}.png") for x in n]
        sets[f"mogel{size}:{el}"] = dict(anims=dict(idle=a("idle1", "idle2"), hit=a("hit1", "hit2"), cast=a("cast1", "cast2", "cast3"),
                                                    attack=a("breathe1", "breathe2", "cast3"), defend=a("withdraw"), reform=a("surprise")),
                                         face="mid")
        for an in sets[f"mogel{size}:{el}"]["anims"].values(): an[:] = [dull(f, MOGEL_DULL) for f in an]
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
# ---- the Beinar (Nov 9): Joseph's 32rogues-based sheet (art_res64/beinar_1.aseprite), rank by bone tint
# white -> aged -> red -> earth = Halv -> base -> Stor -> Forn. Only bone changes (beinar32_tints.py). The robed mage
# starts aged, so its white-face version is its Halv. Sprite numbers are Joseph's frames (1-based); 7 is the mage's cast pose.
import beinar32_tints as BT
BT.F = "/home/claude/art_work/beinar_32r/frames/frame%d.png"
def bt(fr, rank): return Image.fromarray(BT.tint(fr, rank))
BEIN32 = {"Halvbeinbryn": (5, "white"), "Beinbryn": (4, "aged"), "Storbeinbryn": (4, "red"), "Fornbein": (4, "earth"),
          "Halvbeinorv": (6, "white"), "Beinorv": (6, "aged"), "Storbeinorv": (6, "red"),
          "Halvbeinseidr": (8, "white"), "Beinseidr": (8, "aged"), "Storbeinseidr": (8, "red")}
for k, (fr, rank) in BEIN32.items():
    anims = dict(idle=[bt(fr, rank)])
    if fr == 8:      # the bone-mage (Joseph): a cast is arm up, spell out (7); a strong one shakes the stick (9, 10) first
        anims["cast"] = [bt(7, rank)]
        anims["big"] = [bt(i, rank) for i in (7, 9, 10, 9, 10, 9, 10, 7)]
    sets[f"bein:{k}"] = dict(anims=anims, face="skull", face_src=bt(fr, "white"), poses=fr == 8)
# ---- the Drattr court (Nov 9-10): Joseph's drattr_1.aseprite (20 frames), one set per job. Extra anims drive the
# per-move frames on the page: attack (a strike), cast (a spell), big (a strong move), or a move's own name.
DR = lambda i: load(f"/home/claude/art_work/drattr4/frame{i - 1}.png")       # Joseph's 1-based numbers
DRATTR = {   # job: (anims as frame lists, face: ("abs", x, y) on the idle frame, or bbox-relative (x, y))
    "Halvdrattr": (dict(idle=[7]), (0, 0)),
    "Young": (dict(idle=[6]), (4, 0)),
    "Shield": (dict(idle=[1]), ("abs", 10, 2)),
    "Swords": (dict(idle=[2]), ("abs", 10, 2)),
    "Spear": (dict(idle=[3]), (7, 1)),
    "Net": (dict(idle=[4]), (7, 3)),
    "Angler": (dict(idle=[5]), ("abs", 6, 4)),
    "Princeling": (dict(idle=[8], attack=[9], cast=[9], big=[9, 10], **{"Feeding Frenzy": [9, 8, 9, 10]}), (5, 2)),
    "Mystic": (dict(idle=[13], cast=[11], big=[11, 12], Undertow=[11, 12]), ("abs", 5, 3)),
    "Queen": (dict(idle=[16], attack=[17], cast=[18], big=[18, 19], Riptide=[18, 19]), (9, 4)),
}
for job, (anims, face) in DRATTR.items():
    sets[f"drattr:{job}"] = dict(anims={k: [DR(i) for i in v] for k, v in anims.items()}, face=face, poses=True)
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
    if isinstance(mode, tuple) and mode[0] == "abs": return mode[1], mode[2]
    if isinstance(mode, tuple): return (x0 + mode[0], y0 + mode[1])
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
    fx, fy = face_of(s.get("face_src", s["anims"]["idle"][0]), s["face"])
    m["face"] = [fx - ub[0], fy - ub[1]]
    m["foot"] = [m["w"] // 2, m["h"]]                    # bottom centre of the union box
    if s.get("poses"): m["poses"] = True                   # the page plays this set's move frames (attack/cast/big/by name)
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
