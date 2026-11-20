"""Run-cycle timing comparison: 2 frame orders x 3 timings, each over scrolling ground ticks."""
import sys
from PIL import Image, ImageDraw

S, OUT = sys.argv[1], sys.argv[2]
ROBE = {(199,220,208): (0x4d,0x9b,0xe6), (138,152,149): (0x4d,0x65,0xb4), (253,208,182): (0xfd,0xcb,0xb0),
        (227,183,160): (0xfc,0xa7,0x90), (201,162,144): (0xab,0x94,0x7a), (15,15,30): (0x2e,0x22,0x2f),
        (255,255,255): (255,255,255)}
def load(i):
    im = Image.open(f"{S}/ws3/out/frame{i}.png").convert("RGBA"); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a: px[x, y] = ROBE[(r, g, b)] + (255,)
    return im
F = {i: load(i) for i in (5, 6, 7, 8)}

ORDERS = {"loop 1-4-3-2": [5, 8, 7, 6], "pingpong 1-4-3-2-3-4": [5, 8, 7, 6, 7, 8]}
def timing(order, kind):
    if kind == "even 8fps": return [(f, 120) for f in order]
    if kind == "even 12fps": return [(f, 80) for f in order]
    # weighted: hold the two key poses (stride 6 and crouch 9), rush the in-betweens
    return [(f, 120 if f in (5, 8) else 60) for f in order]
TIMINGS = ["weighted"]

TICK, SC, PAD, STRIDE = 20, 5, 14, 14       # ground moves STRIDE px (sprite scale) per cycle
cells = [(o, t, timing(ORDERS[o], t)) for o in ORDERS for t in TIMINGS]
total = 3240                                 # LCM of 360, 540
cw, ch = 16 * SC + 70, 32 * SC + 44
W, H = 2 * cw + PAD * 2, ch + PAD * 2
def frame_at(seq, t):
    t %= sum(d for _, d in seq)
    for f, d in seq:
        if t < d: return f
        t -= d
out = []
for t in range(0, total, TICK):
    im = Image.new("RGB", (W, H), (40, 40, 48)); d = ImageDraw.Draw(im)
    for k, (o, tm, seq) in enumerate(cells):
        cx = PAD + (k % 2) * cw; cy = PAD + (k // 2) * ch
        cyc = sum(dd for _, dd in seq)
        off = (t / 360 * STRIDE * SC) % (8 * SC)      # same ground speed for both
        gy = cy + 32 * SC + 2
        for gx in range(-8 * SC, cw, 8 * SC):          # ground ticks scroll left
            x0 = cx + gx - off
            if cx <= x0 <= cx + cw - 10: d.line([(x0, gy), (x0 + 2 * SC, gy)], fill=(98, 85, 101), width=2)
        spr = F[frame_at(seq, t)].resize((16 * SC, 32 * SC), Image.NEAREST)
        im.paste(spr, (cx + 15, cy), spr)
        d.text((cx, gy + 6), o, fill=(220, 220, 220))
    out.append(im)
out[0].save(f"{OUT}/run_pingpong_compare.gif", save_all=True, append_images=out[1:], duration=TICK, loop=0)
# a static legend so the grid is readable
lg = Image.new("RGB", (W, H), (40, 40, 48)); d = ImageDraw.Draw(lg)
for k, (o, tm, seq) in enumerate(cells):
    cx = PAD + (k % 2) * cw; cy = PAD + (k // 2) * ch
    d.text((cx, cy), f"{o}\n{tm}\n" + " ".join(f"{f+1}:{ms}" for f, ms in seq), fill=(220, 220, 220))
lg.save(f"{OUT}/run_pingpong_legend.png")
print(len(out), "frames")
