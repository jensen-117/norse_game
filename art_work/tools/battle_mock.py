"""320x180 battle-screen mock v2: Res64 walls, floor slabs as the 3x2 board cells, Joseph's bitmap font,
and a bevelled text box (filigree option 1) tinted per area with a rune plaque."""
import sys, random
from PIL import Image, ImageDraw
sys.path.insert(0, sys.argv[1] + "/tools")
from pxfont import PxFont
sys.path.insert(0, "/home/claude/sim")
from engine import spirit_name
import composer

S, ART, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
ENV = f"{ART}/environment"
walls = [Image.open(f"{ENV}/walls/walls_{i}.png").convert("RGBA") for i in range(22)]
slabs = [Image.open(f"{ENV}/floors/floors_{i}.png").convert("RGBA") for i in range(3)]
font = PxFont(f"{ART}/ui/font_sheet.png")
wc = Image.open(f"{ART}/backgrounds/sol_watercolor_gold.png").convert("L")
W, H = 320, 180
INK = rgb("2e222f")

AREAS = {   # frame (dark, mid, light), box fill ramp (dark->light), rune
    "Vatn": (("323353", "4d65b4", "4d9be6"), ("2e222f", "323353", "484a77"), "laguz"),
    "Eld":  (("6e2727", "b33831", "ea4f36"), ("2e222f", "45293f", "6e2727"), "kaunan"),
    "Neutral": (("3e3546", "7f708a", "c7dcd0"), ("2e222f", "3e3546", "625565"), "raidho"),
}
# neutral tile colours -> per-area ramp (stone s0..s3, mortar m0..m1); all Res64
NEUTRAL = ["3e3546", "625565", "7f708a", "9babb2", "2e222f", "45293f"]
STONE = {
    "Neutral": NEUTRAL,
    "Vatn": ["323353", "484a77", "7f708a", "9babb2", "2e222f", "0b5e65"],   # cold blue stone, wet teal seams
    "Eld":  ["45293f", "694f62", "966c6c", "ab947a", "2e222f", "b33831"],   # warm stone, smouldering mortar
}
def recolor(tile, area, darken=0):
    """Swap the neutral ramp for an area ramp; darken shifts stone down a step (floors sit below walls)."""
    m = {}
    for i, h in enumerate(NEUTRAL):
        if i >= 4: m[rgb(h)] = rgb(STONE[area][4] if darken else STONE[area][i])   # floors: no glowing seams
        else:
            j = max(0, i - darken) if i > 0 or not darken else -1   # floor bevel shade merges into the face
            m[rgb(h)] = rgb(STONE[area][j] if j >= 0 else STONE[area][4])
    out = tile.copy(); px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            p = px[x, y]
            if p[3]: px[x, y] = m.get(p[:3], p[:3]) + (255,)
    return out
RUNES = {"laguz":  ["#....", "##...", "#.#..", "#..#.", "#....", "#....", "#...."],
         "kaunan": ["...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."],
         "raidho": ["#....", "##...", "#.#..", "##...", "#.#..", "#..#.", "#...#"]}
# 7x7 corner stud: dark ring, lit upper-left, shaded lower-right
STUD = [".#####.", "#LLLMM#", "#LL#MD#", "#L###D#", "#MM#DD#", "#MDDDD#", ".#####."]

def squash(tile, w, h, b=3):
    """Foreshorten a top-down square slab into a w x h floor cell, keeping its b-px borders (9-slice)."""
    T = tile.width
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    xs = list(range(b)) + [b + (i * (T - 2 * b)) // (w - 2 * b) for i in range(w - 2 * b)] + list(range(T - b, T))
    ys = list(range(b)) + [b + (i * (T - 2 * b)) // (h - 2 * b) for i in range(h - 2 * b)] + list(range(T - b, T))
    src = tile.load(); dst = out.load()
    for j, sy in enumerate(ys):
        for i, sx in enumerate(xs): dst[i, j] = src[sx, sy]
    return out

# ---------------------------------------------------------------- dungeon dressing (the CC pack, in Res64)
DR = f"{ART}/dressing"
def prop(name, area, band=None):
    im = recolor(Image.open(f"{DR}/props/{name}.png").convert("RGBA"), area)
    if band:                                # cloth takes the area colour (banners as area flags)
        m = {rgb("694f62"): rgb(band[0]), rgb("966c6c"): rgb(band[1]), rgb("ab947a"): rgb(band[2])}
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                p = px[x, y]
                if p[3] and p[:3] in m: px[x, y] = m[p[:3]] + (255,)
    return im
def put_decal(im, name, xy, colour, flip=False):
    m = Image.open(f"{DR}/decals/{name}.png")
    if flip: m = m.transpose(Image.FLIP_LEFT_RIGHT)
    im.paste(Image.new("RGBA", m.size, rgb(colour) + (255,)), xy, m)
def light_pool(im, cx, cy, r_in, r_out, area):
    """Palette-safe light: wall stone inside the pool steps one notch up its own ramp (checker at the rim)."""
    ramp = [rgb(h) for h in STONE[area][:4]]
    up = {ramp[i]: ramp[i + 1] for i in range(3)}
    px = im.load()
    for y in range(max(0, cy - r_out), min(64, cy + r_out)):
        for x in range(max(0, cx - r_out), min(W, cx + r_out)):
            dd = ((x - cx) ** 2 + ((y - cy) * 1.4) ** 2) ** 0.5
            if dd > r_out: continue
            if dd > r_in and (x + y) % 2: continue
            p = px[x, y][:3]
            if p in up: px[x, y] = up[p] + (255,)
DRESS = {   # per area: webs colour, crack colour, cloth band, and what hangs where
    "Neutral": dict(web="9babb2", crack="3e3546", band=("3e3546", "625565", "7f708a"),
                    wall=[("window_arch", 52, 14), ("banner_a", 152, 2), ("alcove_statue", 262, 18)],
                    lights=[("lantern", 112, 22), ("lantern", 204, 22)], floor=[("barrel", 10, 66), ("cask", 284, 46)]),
    "Vatn":    dict(web="8fd3ff", crack="0b5e65", band=("323353", "4d65b4", "4d9be6"),
                    wall=[("window_cross", 52, 18), ("banner_b", 152, 2), ("slit_a", 236, 12)],
                    lights=[("candle", 112, 22)], floor=[("rubble", 2, 62), ("barrel_lid", 292, 64)]),
    "Eld":     dict(web="625565", crack="6e2727", band=("6e2727", "b33831", "ea4f36"),
                    wall=[("fireplace", 146, 13), ("banner_torn", 60, 2), ("banner_torn", 244, 2)],
                    lights=[("lantern", 104, 22), ("lantern", 212, 22)], floor=[("cauldron", 12, 64), ("chest", 290, 64)]),
}
def dress(im, area, stone):
    D = DRESS[area]
    for name, x, y in D["lights"]: light_pool(im, x + 3, y + 7, 9, 15, stone)
    if area == "Eld": light_pool(im, 160, 52, 20, 30, stone)       # the hearth lights the wall around it
    for k, (c, x, y) in enumerate([("crack_3", 30, 42), ("crack_11", 278, 44)]):
        put_decal(im, c, (x, y), D["crack"])
    for name, x, y in D["wall"]:
        im.alpha_composite(prop(name, stone, D["band"] if name.startswith("banner") else None), (x, y))
    for name, x, y in D["lights"]: im.alpha_composite(prop(name, stone), (x, y))
    put_decal(im, "web_4", (0, 0), D["web"]); put_decal(im, "web_4", (W - Image.open(f"{DR}/decals/web_4.png").width, 0), D["web"], flip=True)
    for name, x, y in D["floor"]:
        p = prop(name, stone); im.alpha_composite(p, (x, y + 16 - p.height + 10))

def scene(area, seed=3, stone=None, highlight=None, foes=None, dressed=False):
    rnd = random.Random(seed)
    band, tint, rune = AREAS[area]
    stone = stone or area
    im = Image.new("RGBA", (W, H), INK + (255,)); d = ImageDraw.Draw(im)
    wt = [recolor(t, stone) for t in walls]
    for x in range(0, W, 32):
        im.alpha_composite(wt[rnd.choice([0, 1, 2, 3, 0, 1])], (x, 0))
        im.alpha_composite(wt[rnd.choice([8, 9, 10, 11, 14, 15])], (x, 32))
    slab = recolor(slabs[0], stone, darken=2)
    # Floor: three courses of slabs (one per lane), one continuous grid sheared the same way across the
    # whole room. Slabs lose their outer ring and are laid with a 1px mortar joint; each board cell IS a slab.
    lanes = [(65, 20), (85, 21), (106, 25)]             # (course top y, course height), back to front
    pitch, K, FRONT = 34, 0.3, 131                      # grid pitch, shear (px per px of depth), floor front edge
    GX = {(0, 1): 48, (0, 0): 82, (1, 0): 184, (1, 1): 218}   # (side, row) -> cell left edge at the floor front
    def edge(side, row, y): return GX[(side, row)] + K * (FRONT - y)
    mortar = rgb(STONE[stone][4])
    d.rectangle([0, 64, W, 130], fill=mortar)
    inner = slab.crop((1, 1, slab.width - 1, slab.height - 1))
    for lane, (ty, th) in enumerate(lanes):
        sq = squash(inner, pitch - 1, th - 1, b=2); sp = sq.load()
        for j in range(th - 1):                          # last row of each course stays mortar
            y = ty + j
            base = GX[(0, 1)] + K * (FRONT - y)
            for c in range(-3, 11):
                x0 = int(round(base + c * pitch))
                for i in range(pitch - 1):               # last column stays mortar
                    x = x0 + i
                    if 0 <= x < W:
                        p = sp[i, j]
                        if p[3]: im.putpixel((x, y), p)
    d.rectangle([0, 64, W, 65], fill=INK)                 # contact shadow where wall meets floor
    if dressed: dress(im, area, stone)
    def cell_poly(side, row, lane):
        ty, th = lanes[lane]
        xt, xb = edge(side, row, ty), edge(side, row, ty + th - 1)
        return [(xt, ty), (xt + pitch - 1, ty), (xb + pitch - 1, ty + th - 1), (xb, ty + th - 1)]
    if highlight:
        for side, row, lane in highlight:               # one fixed UI colour, whatever the area
            d.polygon(cell_poly(side, row, lane), outline=rgb("ffffff"))
    def foot(side, row, lane):
        ty, th = lanes[lane]; fy = ty + th - 5
        return int(round(edge(side, row, fy))) + (pitch - 16) // 2, fy

    sprites = []
    for lane, cls in enumerate(["Hafrunar", "Brennumar", "Seidar"]):
        x, y = foot(0, 0, lane)
        sprites.append((y, x, Image.open(f"{ART}/heroes/wizard_side_v2/frames/{cls}_right_idle1.png").convert("RGBA")))
    if foes is None:
        ande, halv = ("Vatnande", "Halvatnande") if area == "Vatn" else ("Eldande", "Halveldande")
        for lane in range(3):
            x, y = foot(1, 0, lane); sprites.append((y, x, Image.open(f"{ART}/spirits/ande/{ande}_0.png").convert("RGBA")))
            x, y = foot(1, 1, lane); sprites.append((y, x, Image.open(f"{ART}/spirits/halvande/{halv}_0.png").convert("RGBA")))
    else:                                   # a composer roll: (row, lane, catalog entry)
        for row, lane, e in foes:
            x, y = foot(1, 0 if row == "front" else 1, lane)
            if "sprite" in e:                   # a ready sprite (the undead test)
                spr = e["sprite"]; sprites.append((y, x + 8 - spr.width // 2, spr)); continue
            if e["family"] == "Ande":
                nm = spirit_name(e["rank"], e["element"])
                path = f"{ART}/spirits/{'halvande' if e['rank'] == 'Halv' else 'ande'}/{nm}_0.png"
            else:
                size = {"Halv": 16, "Litel": 24}.get(e["rank"], 32)
                path = f"{ART}/slimes/frames/Mogel{size}_{e['element']}_idle1.png"
            spr = Image.open(path).convert("RGBA")
            sprites.append((y, x + 8 - spr.width // 2, spr))
    for y, x, spr in sorted(sprites, key=lambda s: s[0]):
        d.ellipse([x + 2, y - 2, x + 13, y + 1], fill=INK)
        im.alpha_composite(spr, (x, y - spr.height))

    # --- text box (option 1): watercolor fill tinted to the area, bevelled band, corner studs, rune ---
    bx0, by0, bx1, by1 = 3, 133, W - 4, H - 4
    bw, bh = bx1 - bx0 + 1, by1 - by0 + 1
    tex = wc.crop((200, 200, 200 + bw * 4, 200 + bh * 4)).resize((bw, bh), Image.BILINEAR); tp = tex.load()
    ramp = [rgb(h) for h in tint]
    for y in range(bh):
        for x in range(bw):
            v = tp[x, y]; k = 0 if v < 150 else (1 if v < 205 else 2)
            im.putpixel((bx0 + x, by0 + y), ramp[k] + (255,))
    dk, md, lt = (rgb(h) for h in band)
    d.rectangle([bx0, by0, bx1, by1], outline=INK)
    d.rectangle([bx0 + 1, by0 + 1, bx1 - 1, by1 - 1], outline=md)
    d.rectangle([bx0 + 2, by0 + 2, bx1 - 2, by1 - 2], outline=md)
    d.line([bx0 + 1, by0 + 1, bx1 - 1, by0 + 1], fill=lt); d.line([bx0 + 1, by0 + 1, bx0 + 1, by1 - 1], fill=lt)
    d.line([bx0 + 2, by1 - 1, bx1 - 1, by1 - 1], fill=dk); d.line([bx1 - 1, by0 + 2, bx1 - 1, by1 - 1], fill=dk)
    d.rectangle([bx0 + 3, by0 + 3, bx1 - 3, by1 - 3], outline=INK)
    stud = {'#': INK, 'L': lt, 'M': md, 'D': dk}
    for cx, cy in [(bx0 - 2, by0 - 2), (bx1 - 4, by0 - 2), (bx0 - 2, by1 - 4), (bx1 - 4, by1 - 4)]:
        for j, r in enumerate(STUD):
            for i, c in enumerate(r):
                if c != '.': im.putpixel((cx + i, cy + j), stud[c] + (255,))
    px0 = (bx0 + bx1) // 2 - 5; py0 = by0 - 6
    d.rectangle([px0, py0, px0 + 10, py0 + 10], fill=md, outline=INK)
    d.line([px0 + 1, py0 + 1, px0 + 9, py0 + 1], fill=lt); d.line([px0 + 1, py0 + 9, px0 + 9, py0 + 9], fill=dk)
    for j, r in enumerate(RUNES[rune]):
        for i, c in enumerate(r):
            if c == '#': im.putpixel((px0 + 3 + i, py0 + 2 + j), INK + (255,))
    # divider between commands and party
    d.line([150, by0 + 6, 150, by1 - 6], fill=dk); d.line([151, by0 + 6, 151, by1 - 6], fill=lt)

    white, dim = rgb("ffffff"), rgb("9babb2")
    rows = [by0 + 6, by0 + 18, by0 + 30]
    for (label, col), y in zip([("Strike", 0), ("Spell", 1), ("Defend", 2)], rows):
        font.text(im, (16, y), label, lt if label == "Spell" else white, shadow=INK)
    for label, y in zip(["Item", "Move", "Flee"], rows):
        font.text(im, (80, y), label, dim if label == "Flee" else white, shadow=INK)
    font.text(im, (8, rows[1]), ">", lt, shadow=INK)
    for (n, hp), y in zip([("Hafrunar", "96/120"), ("Brennumar", "71/108"), ("Seidar", "102/102")], rows):
        font.text(im, (160, y), n, white, shadow=INK)
        wv = sum(font.width(c) + 1 for c in hp) - 1
        font.text(im, (bx1 - 9 - wv, y), hp, white, shadow=INK)
    return im

if len(sys.argv) > 4 and sys.argv[4] == "composed":
    rng = random.Random(int(sys.argv[5]) if len(sys.argv) > 5 else 11)
    cat = composer.catalog(); shots = []
    for biome, area in (("Eldhall", "Eld"), ("Vatnhall", "Vatn"), ("Mire", "Neutral")):
        picks = composer.compose(rng, composer.gate(cat, art_only=True, **composer.BIOMES[biome]),
                                 dict(family_min={"Mogel": 1, "Ande": 1}))
        placed = composer.place(picks)
        print(biome, " | ".join(f"{r[0].upper()}{l+1} {composer.describe(e)}" for r, l, e in placed))
        im = scene(area, foes=placed); shots.append(im)
        im.resize((W * 4, H * 4), Image.NEAREST).save(f"{OUT}/composed_{biome.lower()}_x4.png")
    sheet = Image.new("RGBA", (W * 2, H * 2 * 3 + 24), INK + (255,))
    for k, im in enumerate(shots):
        sheet.alpha_composite(im.resize((W * 2, H * 2), Image.NEAREST), (0, k * (H * 2 + 12)))
    sheet.save(f"{OUT}/composed_encounters.png")
    sys.exit()
if len(sys.argv) > 4 and sys.argv[4] == "dressed":
    rng = random.Random(5); cat = composer.catalog(); shots = []
    for biome, area in (("Mire", "Neutral"), ("Vatnhall", "Vatn"), ("Eldhall", "Eld")):
        placed = composer.place(composer.compose(rng, composer.gate(cat, art_only=True, **composer.BIOMES[biome]),
                                                 dict(family_min={"Mogel": 1, "Ande": 1})))
        im = scene(area, foes=placed, dressed=True); shots.append(im)
        im.resize((W * 4, H * 4), Image.NEAREST).save(f"{OUT}/dressed_{area.lower()}_x4.png")
    sheet = Image.new("RGBA", (W * 2, H * 2 * 3 + 24), INK + (255,))
    for k, im in enumerate(shots): sheet.alpha_composite(im.resize((W * 2, H * 2), Image.NEAREST), (0, k * (H * 2 + 12)))
    sheet.save(f"{OUT}/dressed_encounters.png")
    used = {p[:3] for im in shots for p in im.getdata() if p[3]}
    res = set(open(f"{S}/tools/res64.txt").read().split())
    print("off-palette:", [c for c in ('%02x%02x%02x' % u for u in used) if c not in res])
    sys.exit()
if len(sys.argv) > 4 and sys.argv[4] == "barrow":
    import numpy as np
    U = f"{ART}/undead"
    def fr(name, rc, flip=False):
        im = Image.open(f"{U}/{name}/{rc}.png").convert("RGBA"); im = im.crop(im.getbbox())
        return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
    CUT = [4, 6, 8, 10, 22, 23]
    def rows_(im, grow):
        a = np.asarray(im); h = a.shape[0]; out = []
        for y in range(h):
            k = h - 1 - y
            if k in CUT and not grow: continue
            out.append(a[y])
            if k in CUT and grow: out.append(a[y])
        return Image.fromarray(np.array(out))
    def wpn(tint, job):
        im = Image.open(f"{U}/weapons/{tint}_{job}_r0c0.png").convert("RGBA"); return im.crop(im.getbbox())
    mog = Image.open(f"{ART}/slimes/frames/Mogel32_Natt_idle1.png").convert("RGBA")
    def bn(job, tint, size):
        im = Image.open(f"{U}/beinar/beinar_{job}_{tint}_{size}.png").convert("RGBA"); return im.crop(im.getbbox())
    packs = {
        "barrow_a": [("front", 0, fr("frames/zombie_corpse", "r0c0")), ("front", 1, bn("sword", "aged", "native")),
                     ("front", 2, bn("sword", "plain", "cut")),
                     ("rear", 0, bn("archer", "aged", "native")), ("rear", 1, mog), ("rear", 2, bn("mage", "aged", "native"))],
        "barrow_b": [("front", 0, bn("sword", "drott", "stretch")), ("front", 1, fr("frames/zombie_corpse", "r0c0")),
                     ("front", 2, bn("archer", "plain", "cut")),
                     ("rear", 0, fr("frames/archer_hunt", "r0c0", flip=True)), ("rear", 1, bn("longbow", "aged", "stretch"))],
    }
    def dg(tint, size, rc="r0c0"):
        im = Image.open(f"{U}/draugr/frames/draugr_{tint}_{size}/{rc}.png").convert("RGBA"); return im.crop(im.getbbox())
    packs["barrow_c"] = [("front", 0, dg("drott", "stretch")), ("front", 1, dg("blar", "native")), ("front", 2, dg("pale", "cut")),
                         ("rear", 0, dg("blar", "stretch")), ("rear", 1, bn("archer", "aged", "native")), ("rear", 2, bn("mage", "plain", "native"))]
    shots = []
    for name, pack in packs.items():
        im = scene("Neutral", foes=[(r, l, {"sprite": spr}) for r, l, spr in pack], dressed=True); shots.append(im)
        im.resize((W * 4, H * 4), Image.NEAREST).save(f"{OUT}/{name}_x4.png")
    sheet = Image.new("RGBA", (W * 3, H * 3 * len(shots) + 12 * (len(shots) - 1)), INK + (255,))
    for k, im in enumerate(shots): sheet.alpha_composite(im.resize((W * 3, H * 3), Image.NEAREST), (0, k * (H * 3 + 12)))
    sheet.save(f"{OUT}/barrow_mock.png")
    shots[-1].resize((W * 4, H * 4), Image.NEAREST).save(f"{OUT}/barrow_draugr_x4.png")
    sys.exit()
a = scene("Neutral")
b = scene("Vatn", highlight=[(0, 1, 0), (0, 1, 1), (0, 1, 2)])      # Move: the open Rear cells
c = scene("Eld", highlight=[(1, 0, 1)])                               # targeting one enemy cell
for name, im in (("battle_mock_neutral", a), ("battle_mock_vatn", b), ("battle_mock_eld", c)):
    im.save(f"{OUT}/{name}.png"); im.resize((W * 4, H * 4), Image.NEAREST).save(f"{OUT}/{name}_x4.png")
both = Image.new("RGBA", (W * 2, H * 2 * 3 + 24), INK + (255,))
for k, im in enumerate((a, b, c)):
    both.alpha_composite(im.resize((W * 2, H * 2), Image.NEAREST), (0, k * (H * 2 + 12)))
both.save(f"{OUT}/battle_mock_compare.png")
print("ok")
