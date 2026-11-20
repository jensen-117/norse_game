"""320x180 battle-screen mock v2: Res64 walls, floor slabs as the 3x2 board cells, Joseph's bitmap font,
and a bevelled text box (filigree option 1) tinted per area with a rune plaque."""
import sys, random
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/claude/art_work/tools")
from pxfont import PxFont
sys.path.insert(0, "/home/claude/sim")
from engine import spirit_name
import composer

S, ART = "/home/claude/art_work", "/home/claude/art_res64"
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
    for y in range(max(0, cy - r_out), min(64, cy + r_out + 64)):
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
def dress(im, area, stone, dy=0):
    D = DRESS[area]
    for name, x, y in D["lights"]: light_pool(im, x + 3, y + 7 - dy, 9, 15, stone)
    if area == "Eld": light_pool(im, 160, 52 - dy, 20, 30, stone)       # the hearth lights the wall around it
    for k, (c, x, y) in enumerate([("crack_3", 30, 42), ("crack_11", 278, 44)]):
        put_decal(im, c, (x, y - dy), D["crack"])
    for name, x, y in D["wall"]:
        im.alpha_composite(prop(name, stone, D["band"] if name.startswith("banner") else None), (x, y - dy))
    for name, x, y in D["lights"]: im.alpha_composite(prop(name, stone), (x, y - dy))
    put_decal(im, "web_4", (0, 0), D["web"]); put_decal(im, "web_4", (W - Image.open(f"{DR}/decals/web_4.png").width, 0), D["web"], flip=True)
    for name, x, y in D["floor"]:
        p = prop(name, stone); im.alpha_composite(p, (x, y + 16 - p.height + 10 - dy))

def scene(area, seed=3, stone=None, highlight=None, foes=None, dressed=False, dy=0, layout=None):
    rnd = random.Random(seed)
    band, tint, rune = AREAS[area]
    stone = stone or area
    im = Image.new("RGBA", (W, H), INK + (255,)); d = ImageDraw.Draw(im)
    wt = [recolor(t, stone) for t in walls]
    for x in range(0, W, 32):
        im.alpha_composite(wt[rnd.choice([0, 1, 2, 3, 0, 1])], (x, -dy))
        im.alpha_composite(wt[rnd.choice([8, 9, 10, 11, 14, 15])], (x, 32 - dy))
    slab = recolor(slabs[0], stone, darken=2)
    # Floor: three courses of slabs (one per lane), one continuous grid sheared the same way across the
    # whole room. Slabs lose their outer ring and are laid with a 1px mortar joint; each board cell IS a slab.
    lanes = [(65 - dy, 20), (85 - dy, 21), (106 - dy, 25)]             # (course top y, course height), back to front
    pitch, K, FRONT = 34, 0.3, 131 - dy                      # grid pitch, shear (px per px of depth), floor front edge
    GX = {(0, 1): 48, (0, 0): 82, (1, 0): 184, (1, 1): 218}   # (side, row) -> cell left edge at the floor front
    if layout:                                               # a roomier board: lanes, pitch and columns given
        lanes, pitch, FRONT = layout["lanes"], layout["pitch"], layout["front"]
        GX = {(0, 1): layout["gx"][0], (0, 0): layout["gx"][1], (1, 0): layout["gx"][2], (1, 1): layout["gx"][3]}
    def edge(side, row, y): return GX[(side, row)] + K * (FRONT - y)
    mortar = rgb(STONE[stone][4])
    d.rectangle([0, 64 - dy, W, (FRONT - 1) if layout else 130 - dy], fill=mortar)
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
    d.rectangle([0, 64 - dy, W, 65 - dy], fill=INK)                 # contact shadow where wall meets floor
    if dressed: dress(im, area, stone, dy)
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

    geo = dict(lanes=lanes, pitch=pitch, K=K, FRONT=FRONT, GX={f"{s}{r}": v for (s, r), v in GX.items()})
    return im, geo

def textbox(im, area, by0, by1=H - 4, divider=None):
    band, tint, rune = AREAS[area]
    d = ImageDraw.Draw(im)
    bx0, bx1 = 3, W - 4
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
    if divider:
        d.line([divider, by0 + 6, divider, by1 - 6], fill=dk); d.line([divider + 1, by0 + 6, divider + 1, by1 - 6], fill=lt)
    return dict(box=[bx0, by0, bx1, by1], band=[dk, md, lt])
