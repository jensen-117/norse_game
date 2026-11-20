"""Joseph's Mogel slimes (32, 24, 16 and 8 px; 11 frames each, soft-brush colours) -> six ramp slots ->
Resurrect 64, native olive (Jord) plus every element ramp. The bright left-rim streak is faded into the
body around it. Exports frames, strips, animation GIFs, contact sheets and a death-chain demo."""
import sys, os
from collections import Counter
from PIL import Image, ImageDraw

S, OUT = sys.argv[1], sys.argv[2]
SRCS = {32: f"{S}/ws8/out", 24: f"{S}/ws10/out", 16: f"{S}/ws9_2/out", 8: f"{S}/ws9_3/out"}
RES = set(open(f"{S}/tools/res64.txt").read().split())
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def L(c):
    f = lambda v: ((v/255 + .055)/1.055)**2.4 if v/255 > .04045 else v/255/12.92
    Y = .2126*f(c[0]) + .7152*f(c[1]) + .0722*f(c[2]); return 116*Y**(1/3) - 16

# slots: O outline, 0 deep shadow, 1 shadow, 2 body, 3 sheen, 4 specular
def slot(c):
    if c[0] - c[1] > 15: return 'O'
    l = L(c)
    return '0' if l <= 45 else '1' if l <= 53 else '2' if l <= 61 else '3' if l <= 71 else '4'

def grid(path, n):
    im = Image.open(path).convert("RGBA")
    g = [[slot(im.getpixel((x, y))[:3]) if im.getpixel((x, y))[3] else '.' for x in range(n)] for y in range(n)]
    def nbrs(gr, x, y, r=1):
        return [gr[y+dy][x+dx] for dy in range(-r, r+1) for dx in range(-r, r+1)
                if (dx or dy) and 0 <= x+dx < n and 0 <= y+dy < n]
    out = [r[:] for r in g]
    # tidy: a lone body pixel whose 4 neighbours are all a different body slot takes their majority
    for y in range(n):
        for x in range(n):
            c = g[y][x]
            if c not in '0123': continue
            nb = [g[y+dy][x+dx] for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < n and 0 <= y+dy < n]
            body = [k for k in nb if k in '0123']
            if len(body) == 4 and c not in body: out[y][x] = Counter(body).most_common(1)[0][0]
    # rim fix: sheen/specular on the left side of the body fades into the body around it
    for y in range(n):                                   # left 40% of each row's span (catches the column too)
        xs = [x for x in range(n) if out[y][x] not in '.O']
        if not xs: continue
        for x in range(xs[0], xs[0] + max(2, int((xs[-1] - xs[0] + 1) * 0.4))):
            if out[y][x] in '34':
                body = [k for k in nbrs(out, x, y, 2) if k in '012']
                out[y][x] = Counter(body).most_common(1)[0][0] if body else '1'
    # soft terminators: checker-dither, only where there is room for it (the 32px sprite)
    if n >= 24:
        for y in range(n):
            for x in range(n):
                p = im.getpixel((x, y))
                if not p[3] or out[y][x] not in '012': continue
                l = L(p[:3]); chk = (x + y) % 2
                if 51 < l <= 55: out[y][x] = '2' if chk else '1'
                elif 43 < l <= 46: out[y][x] = '1' if chk else '0'
    return out

LABELS = ["idle1", "idle2", "surprise", "breathe1", "breathe2", "hit1", "hit2", "withdraw", "cast1", "cast2", "cast3"]
G = {n: [grid(f"{d}/frame{i}.png", n) for i in range(11)] for n, d in SRCS.items()}

OUTLINE = "2e222f"
RAMPS = {   # deep, shadow, body, sheen, specular (dark -> light), Res64 only
    "Jord":  ["4c3e24", "676633", "a2a947", "b2ba90", "c7dcd0"],      # native: sage sheen, cool specular
    "Eld":   ["ae2334", "e83b3b", "f57d4a", "fbb954", "fbff86"],
    "Reyk":  ["3e3546", "694f62", "966c6c", "ab947a", "fdcbb0"],
    "Vatn":  ["484a77", "4d65b4", "4d9be6", "8fd3ff", "ffffff"],
    "Hrim":  ["0b5e65", "0b8a8f", "0eaf9b", "8ff8e2", "ffffff"],
    "Blast": ["374e4a", "547e64", "92a984", "c7dcd0", "ffffff"],
    "Blixt": ["484a77", "4d65b4", "a884f3", "fbff86", "ffffff"],
    "Gro":   ["165a4c", "239063", "1ebc73", "91db69", "cddf6c"],
    "Sol":   ["cd683d", "f79617", "f9c22b", "fbff86", "ffffff"],
    "Lak":   ["a24b6f", "cf657f", "f68181", "fca790", "fdcbb0"],
    "Natt":  ["2e222f", "45293f", "6b3e75", "905ea9", "a884f3"],
    "Aska":  ["2e222f", "313638", "625565", "9babb2", "c7dcd0"],
}
def render(g, ramp):
    pal = {'O': rgb(OUTLINE), **{str(k): rgb(h) for k, h in enumerate(ramp)}}
    for h in ramp + [OUTLINE]: assert h in RES, h
    n = len(g); im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    for y in range(n):
        for x in range(n):
            if g[y][x] != '.': im.putpixel((x, y), pal[g[y][x]] + (255,))
    return im

ANIMS = {
    "idle":     [(0, 500), (1, 500)],
    "hit":      [(5, 120), (6, 220), (0, 300)],
    "defend":   [(0, 120), (7, 900)],
    "charge":   [(0, 200), (3, 250), (4, 600)],
    "cast":     [(8, 150), (9, 150), (10, 450), (0, 300)],
    "surprise": [(2, 400), (0, 300)],
}
for d in ("frames", "strips", "gifs"): os.makedirs(f"{OUT}/{d}", exist_ok=True)
def gif(frames, durs, path, n):
    sc = max(4, 192 // n); out = []
    for f in frames:
        b = Image.new("RGB", (n * sc, n * sc), (40, 40, 48)); big = f.resize((n * sc, n * sc), Image.NEAREST)
        b.paste(big, (0, 0), big); out.append(b)
    out[0].save(path, save_all=True, append_images=out[1:], duration=durs, loop=0, disposal=2)
for n in G:
    for el, ramp in RAMPS.items():
        imgs = [render(g, ramp) for g in G[n]]
        for i, im in enumerate(imgs): im.save(f"{OUT}/frames/Mogel{n}_{el}_{LABELS[i]}.png")
        strip = Image.new("RGBA", (n * 11, n), (0, 0, 0, 0))
        for i, im in enumerate(imgs): strip.alpha_composite(im, (n * i, 0))
        strip.save(f"{OUT}/strips/Mogel{n}_{el}.png")
        for name, seq in ANIMS.items():
            gif([imgs[i] for i, _ in seq], [d for _, d in seq], f"{OUT}/gifs/Mogel{n}_{el}_{name}.gif", n)

# contact sheets: native frames for each size; every element at all three sizes (true relative scale)
for n in G:
    sc = 160 // n
    sh = Image.new("RGBA", (11 * (n * sc + 6) + 6, n * sc + 12), (40, 40, 48, 255))
    for i in range(11):
        sh.alpha_composite(render(G[n][i], RAMPS["Jord"]).resize((n * sc, n * sc), Image.NEAREST), (6 + i * (n * sc + 6), 6))
    sh.save(f"{OUT}/mogel{n}_jord_frames.png")
sc = 3; cw = (32 + 24 + 16 + 8 + 18) * sc
fam = Image.new("RGBA", (6 * (cw + 10) + 10, 2 * (32 * sc + 24) + 10), (40, 40, 48, 255)); d = ImageDraw.Draw(fam)
for k, el in enumerate(RAMPS):
    x, y = 10 + (k % 6) * (cw + 10), 10 + (k // 6) * (32 * sc + 24)
    d.text((x, y), el, fill=(220, 220, 220)); xx = x
    for n in (32, 24, 16, 8):
        fam.alpha_composite(render(G[n][0], RAMPS[el]).resize((n * sc, n * sc), Image.NEAREST), (xx, y + 14 + (32 - n) * sc))
        xx += (n + 6) * sc
fam.save(f"{OUT}/mogel_families.png")

# death chain demo: each kill drops the slime one size until the smallest pops
def chain(el):
    sc, Wd, Hd = 5, 48, 36
    seq = []
    for n, nxt in ((32, 24), (24, 16), (16, 8)):
        im = [render(g, RAMPS[el]) for g in G[n]]
        seq += [(im[0], 400), (im[1], 400), (im[5], 100), (im[6], 200), (im[7], 300)]
        sm = [render(g, RAMPS[el]) for g in G[nxt]]
        seq += [(sm[2], 350 if nxt != 8 else 250)]
    seq += [(None, 600)]
    frames = []
    for spr, ms in seq:
        b = Image.new("RGB", (Wd * sc, Hd * sc), (40, 40, 48)); dd = ImageDraw.Draw(b)
        dd.rectangle([0, 33 * sc, Wd * sc, Hd * sc], fill=rgb("3e3546"))
        if spr is not None:
            n = spr.width; big = spr.resize((n * sc, n * sc), Image.NEAREST)
            b.paste(big, (((Wd - n) // 2) * sc, (33 - n) * sc), big)
        frames.append((b, ms))
    frames[0][0].save(f"{OUT}/mogel_{el.lower()}_death_chain.gif", save_all=True,
                      append_images=[f for f, _ in frames[1:]], duration=[m for _, m in frames], loop=0)
for el in ("Jord", "Vatn", "Eld"): chain(el)

src = Image.open(f"{SRCS[32]}/frame0.png").convert("RGBA")
cmp_ = Image.new("RGBA", (2 * 256 + 24, 256 + 16), (40, 40, 48, 255))
cmp_.alpha_composite(src.resize((256, 256), Image.NEAREST), (8, 8))
cmp_.alpha_composite(render(G[32][0], RAMPS["Jord"]).resize((256, 256), Image.NEAREST), (272, 8))
cmp_.save(f"{OUT}/mogel_source_vs_res64.png")
print("ok")
