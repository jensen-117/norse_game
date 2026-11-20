"""Side wizard v2: recolor Joseph's 14 frames to Resurrect 64 per school and assemble
idle/breath, hand, attack windup, run and cast animations."""
import sys, os
from PIL import Image

S = sys.argv[1]; OUT = sys.argv[2]
RES64 = set(open(f"{S}/tools/res64.txt").read().split())
SRC = {(15,15,30):'#',(138,152,149):'x',(199,220,208):'o',(201,162,144):'3',
       (227,183,160):'2',(253,208,182):'1',(255,255,255):'W',
       (148,120,112):'c',(121,99,95):'b',(95,78,79):'a',(118,129,129):'D'}   # chin shadow, open mouth, mouth depth

def grid(i):
    im = Image.open(f"{S}/ws5/out/frame{i}.png").convert("RGBA")
    return [''.join(SRC[im.getpixel((x,y))[:3]] if im.getpixel((x,y))[3] else '.'
                    for x in range(16)) for y in range(32)]

F = [grid(i) for i in range(17)]

FR = F

# Animations: (frame index, ms)
LABELS = ["idle1", "idle2", "idle3", "hit", "spell1", "run1", "run2", "run3", "run4",
          "charge1", "charge2", "charge3", "bomb1", "bomb2", "downed", "defend", "defend_hit"]
ANIMS = {
    "idle":   [(0, 600), (1, 300), (2, 600), (1, 300)],
    "hit":    [(0, 100), (3, 400), (0, 300)],
    "spell":  [(0, 150), (4, 450), (0, 300)],
    # Joseph's reordered run at an even 8fps
    "run":    [(5, 125), (6, 125), (7, 125), (8, 125)],
    "charge": [(9, 300), (10, 300), (11, 450)],
    "bomb":   [(12, 150), (13, 500)],
    "cast":   [(0, 250), (9, 300), (10, 300), (11, 450), (12, 150), (13, 500), (0, 300)],
    "downed": [(0, 150), (3, 200), (14, 1200)],
    "defend": [(0, 150), (15, 1200)],
    "defend_hit": [(15, 300), (16, 350), (15, 600)],
    "taunt":  [(0, 150), (13, 650), (15, 900)],          # yell (bomb2), then settle into Defend
}
PREVIEW = ["idle", "run", "cast", "defend_hit", "taunt", "downed"]

SKIN = {'1': 'fdcbb0', '2': 'fca790', '3': 'ab947a', '#': '2e222f', 'W': 'ffffff',
        'c': '966c6c', 'b': '966c6c', 'a': '694f62'}   # c and b never share a frame
ROBES = {"Hafrunar": ("4d9be6", "4d65b4", "484a77"), "Brennumar": ("ea4f36", "b33831", "6e2727"),
         "Skurmar": ("c7dcd0", "9babb2", "7f708a"), "Lundar": ("a2a947", "676633", "4c3e24"),
         "Dagskald": ("f9c22b", "f79617", "fb6b1d"), "Seidar": ("905ea9", "6b3e75", "45293f")}

def hexrgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def render(g, robe):
    pal = dict(SKIN, o=robe[0], x=robe[1], D=robe[2])
    im = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c != '.':
                assert pal[c] in RES64, pal[c]
                im.putpixel((x, y), hexrgb(pal[c]) + (255,))
    return im

def gif(frames, durs, path, scale=8, bg=(40, 40, 48)):
    out = []
    for f in frames:
        b = Image.new("RGB", (f.width * scale, f.height * scale), bg)
        b.paste(f.resize((f.width * scale, f.height * scale), Image.NEAREST), (0, 0),
                f.resize((f.width * scale, f.height * scale), Image.NEAREST))
        out.append(b)
    out[0].save(path, save_all=True, append_images=out[1:], duration=durs, loop=0, disposal=2)

os.makedirs(f"{OUT}/frames", exist_ok=True); os.makedirs(f"{OUT}/strips", exist_ok=True)
os.makedirs(f"{OUT}/gifs", exist_ok=True)
for cls, robe in ROBES.items():
    imgs = [render(g, robe) for g in FR]
    for side in ("right", "left"):
        ims = imgs if side == "right" else [i.transpose(Image.FLIP_LEFT_RIGHT) for i in imgs]
        for name, seq in ANIMS.items():
            fr = [ims[i] for i, _ in seq]
            # unique frames per anim, in order, as a strip for Aseprite's Import Sprite Sheet
            uniq = []
            for i, _ in seq:
                if i not in uniq: uniq.append(i)
            strip = Image.new("RGBA", (16 * len(uniq), 32), (0, 0, 0, 0))
            for k, i in enumerate(uniq):
                strip.alpha_composite(ims[i], (16 * k, 0))
                ims[i].save(f"{OUT}/frames/{cls}_{side}_{LABELS[i]}.png")
            strip.save(f"{OUT}/strips/{cls}_{side}_{name}.png")
            gif(fr, [d for _, d in seq], f"{OUT}/gifs/{cls}_{side}_{name}.gif")

# Contact sheet: one row per class, frames 0..7 at 6x, plus a combined live preview GIF.
sc, pad = 6, 10
names = list(ROBES)
sheet = Image.new("RGBA", (len(FR) * (16*sc + pad) + pad, len(names) * (32*sc + pad) + pad), (40, 40, 48, 255))
for r, cls in enumerate(names):
    for k, g in enumerate(FR):
        sheet.alpha_composite(render(g, ROBES[cls]).resize((16*sc, 32*sc), Image.NEAREST),
                              (pad + k * (16*sc + pad), pad + r * (32*sc + pad)))
sheet.save(f"{OUT}/wizard_side_v2_sheet.png")

# Preview GIF: 4 animations side by side for three classes, synced at a 50ms tick.
tick = 50
def frame_at(seq, t):
    total = sum(d for _, d in seq); t %= total
    for i, d in seq:
        if t < d: return i
        t -= d
L = 1
for seq in (ANIMS[n] for n in PREVIEW):
    L = L * sum(d for _, d in seq) // __import__("math").gcd(L, sum(d for _, d in seq))
L = min(L, 36000)
show = ["Hafrunar", "Brennumar", "Seidar"]
sc2 = 5
pw = len(PREVIEW) * (16*sc2 + pad) + pad; ph = len(show) * (32*sc2 + pad) + pad
cache = {c: [render(g, ROBES[c]) for g in FR] for c in show}
out = []
for t in range(0, L, tick):
    b = Image.new("RGBA", (pw, ph), (40, 40, 48, 255))
    for r, c in enumerate(show):
        for k, seq in enumerate(ANIMS[n] for n in PREVIEW):
            b.alpha_composite(cache[c][frame_at(seq, t)].resize((16*sc2, 32*sc2), Image.NEAREST),
                              (pad + k * (16*sc2 + pad), pad + r * (32*sc2 + pad)))
    out.append(b.convert("RGB"))
out[0].save(f"{OUT}/wizard_side_v2_preview.gif", save_all=True, append_images=out[1:],
            duration=tick, loop=0)
print("ok", len(out), "preview frames")
