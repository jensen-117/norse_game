"""Draft an 8-frame run: step A = Joseph's run1-4 with the far hand shaded, step B = the same poses with
near/far hands swapped (bright = near arm), the passing hand hidden, and the contact foot moved forward."""
import sys
from PIL import Image, ImageDraw

S, OUT = sys.argv[1], sys.argv[2]
SRC = {(15,15,30):'#',(138,152,149):'x',(199,220,208):'o',(201,162,144):'3',(227,183,160):'2',
       (253,208,182):'1',(255,255,255):'W'}
def grid(i):
    im = Image.open(f"{S}/ws3/out/frame{i}.png").convert("RGBA")
    return [list(''.join(SRC[im.getpixel((x, y))[:3]] if im.getpixel((x, y))[3] else '.'
                         for x in range(16))) for y in range(32)]
SHADE = {'1': '2', '2': '3'}
def shade(g, cells):
    for x, y in cells: g[y][x] = SHADE.get(g[y][x], g[y][x])
def box(x0, x1, y0, y1): return [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]

# hand boxes per drawn frame: (front hand, back hand)
HANDS = {5: (box(12, 13, 15, 16), box(1, 2, 18, 19)),     # run1
         6: (box(13, 14, 18, 19), box(4, 5, 19, 20)),     # run2
         7: (box(7, 8, 19, 20), None),                    # run3: one hand, passing
         8: (box(12, 14, 18, 19), None)}                  # run4: forward hand only

A, B = {}, {}
for i, (front, back) in HANDS.items():
    a, b = grid(i), grid(i)
    # step A: forward arm is the near arm (bright); trailing far hand shaded
    if back: shade(a, back)
    # step B: the far arm leads (shaded) and the near arm trails (bright)
    if i != 7: shade(b, front)
    B[i] = b; A[i] = a
# run3 B: the passing hand belongs to the far arm, so it is behind the body: hide hand and cuff
for x, y in box(6, 9, 18, 21):
    if B[7][y][x] in '12' or (B[7][y][x] == 'x' and x != 7): B[7][y][x] = 'o'
# run1 B: the near foot is the leading one, so the shoe mark moves forward 3px
for y in (30, 31):
    for x in (6, 7, 8):
        if B[5][y][x] == 'x': B[5][y][x] = 'o'
for x, y in [(10, 30), (11, 30), (9, 31), (10, 31), (11, 31)]: B[5][y][x] = 'x'

PAL = {'o': (0x4d,0x9b,0xe6), 'x': (0x4d,0x65,0xb4), '1': (0xfd,0xcb,0xb0), '2': (0xfc,0xa7,0x90),
       '3': (0xab,0x94,0x7a), '#': (0x2e,0x22,0x2f), 'W': (255,255,255)}
def img(g):
    im = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c != '.': im.putpixel((x, y), PAL[c] + (255,))
    return im
ORIG = {i: img(grid(i)) for i in HANDS}
IA = {i: img(g) for i, g in A.items()}; IB = {i: img(g) for i, g in B.items()}

W8 = {5: 120, 8: 120, 7: 60, 6: 60}
loop4 = [(ORIG[i], W8[i]) for i in (5, 8, 7, 6)]
loop8 = [(IA[i], W8[i]) for i in (5, 8, 7, 6)] + [(IB[i], W8[i]) for i in (5, 8, 7, 6)]

# comparison GIF over scrolling ground, same ground speed
TICK, SC, PAD = 20, 6, 14
cw, ch = 16 * SC + 70, 32 * SC + 44
total = 720
out = []
def at(seq, t):
    t %= sum(d for _, d in seq)
    for f, d in seq:
        if t < d: return f
        t -= d
for t in range(0, total, TICK):
    im = Image.new("RGB", (2 * cw + 2 * PAD, ch + 2 * PAD), (40, 40, 48)); d = ImageDraw.Draw(im)
    for k, (name, seq) in enumerate([("4-loop 1-4-3-2", loop4), ("8-loop A then B (draft)", loop8)]):
        cx, cy = PAD + k * cw, PAD
        gy = cy + 32 * SC + 2; off = (t / 360 * 14 * SC) % (8 * SC)
        for gx in range(-8 * SC, cw, 8 * SC):
            x0 = cx + gx - off
            if cx <= x0 <= cx + cw - 10: d.line([(x0, gy), (x0 + 2 * SC, gy)], fill=(98, 85, 101), width=2)
        spr = at(seq, t).resize((16 * SC, 32 * SC), Image.NEAREST)
        im.paste(spr, (cx + 15, cy), spr); d.text((cx, gy + 6), name, fill=(220, 220, 220))
    out.append(im)
out[0].save(f"{OUT}/run_8frame_compare.gif", save_all=True, append_images=out[1:], duration=TICK, loop=0)

# static sheet: top = step A, bottom = step B, in play order
sc = 10
sh = Image.new("RGBA", (4 * (16 * sc + 10) + 10, 2 * (32 * sc + 10) + 10), (40, 40, 48, 255))
for r, set_ in enumerate((IA, IB)):
    for k, i in enumerate((5, 8, 7, 6)):
        sh.alpha_composite(set_[i].resize((16 * sc, 32 * sc), Image.NEAREST), (10 + k * (16 * sc + 10), 10 + r * (32 * sc + 10)))
sh.save(f"{OUT}/run_8frame_sheet.png")
print("ok")
