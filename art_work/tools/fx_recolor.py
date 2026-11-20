"""Recolor the CC effects sheet (one 6-tone warm ramp) into Resurrect 64 per element, plus a white
martial set. Source tones are ranked dark->light onto 5-step Res64 ramps."""
import sys, os
from PIL import Image

SRC, OUT, RES, TAG = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
RES64 = set(open(RES).read().split())
# source tone -> ramp step (0 dark .. 4 light)
STEPS = {
  "fx": {(184,52,91): 0, (204,66,94): 0, (234,98,98): 1, (250,109,116): 1,
         (244,141,109): 2, (255,184,121): 3, (252,239,141): 4},
  # bdragon1727 "Fire Pixel Bullet 16x16": 8 main tones plus a few stray near-duplicates
  "bullet": {(115,23,45): 0, (180,32,42): 0, (223,62,35): 1, (255,58,0): 1, (250,106,10): 2,
             (248,96,16): 2, (255,122,0): 2, (249,163,27): 3, (255,204,0): 3, (255,213,65): 3,
             (255,252,64): 4, (255,251,0): 4, (255,255,255): 4},
}
STEP = STEPS[TAG]
RAMPS = {   # 5 steps, dark -> light, Res64 only
    "Eld":   ["ae2334", "e83b3b", "f57d4a", "fbb954", "fbff86"],
    "Reyk":  ["3e3546", "694f62", "966c6c", "ab947a", "fdcbb0"],
    "Vatn":  ["484a77", "4d65b4", "4d9be6", "8fd3ff", "ffffff"],
    "Hrim":  ["0b5e65", "0b8a8f", "0eaf9b", "8ff8e2", "ffffff"],
    "Blast": ["374e4a", "547e64", "92a984", "c7dcd0", "ffffff"],
    "Blixt": ["484a77", "4d65b4", "a884f3", "fbff86", "ffffff"],
    "Jord":  ["4c3e24", "676633", "a2a947", "d5e04b", "fbff86"],
    "Gro":   ["165a4c", "239063", "1ebc73", "91db69", "cddf6c"],
    "Sol":   ["cd683d", "f79617", "f9c22b", "fbff86", "ffffff"],
    "Lak":   ["a24b6f", "cf657f", "f68181", "fca790", "fdcbb0"],
    "Natt":  ["2e222f", "45293f", "6b3e75", "905ea9", "a884f3"],
    "Aska":  ["2e222f", "313638", "625565", "9babb2", "c7dcd0"],
    "Martial": ["7f708a", "9babb2", "c7dcd0", "ffffff", "ffffff"],
}
for r in RAMPS.values():
    for h in r: assert h in RES64, h
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

src = Image.open(SRC).convert("RGBA")
os.makedirs(f"{OUT}/sheets", exist_ok=True)
outs = {}
for name, ramp in RAMPS.items():
    im = Image.new("RGBA", src.size, (0, 0, 0, 0)); sp = src.load(); dp = im.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = sp[x, y]
            if a < 128: continue
            dp[x, y] = rgb(ramp[STEP[(r, g, b)]]) + (255,)
    im.save(f"{OUT}/sheets/{TAG}_{name}.png"); outs[name] = im

# contact sheet: every recolor at 2x on a dark ground, labelled
from PIL import ImageDraw
sc, pad, lab = 2, 10, 14
cols = 3; rows = -(-len(outs) // cols)
cw, ch = src.width * sc + pad, src.height * sc + lab + pad
sheet = Image.new("RGB", (cols * cw + pad, rows * ch + pad), (40, 40, 48)); d = ImageDraw.Draw(sheet)
for k, (name, im) in enumerate(outs.items()):
    x, y = pad + (k % cols) * cw, pad + (k // cols) * ch
    d.text((x, y), name, fill=(220, 220, 220))
    big = im.resize((src.width * sc, src.height * sc), Image.NEAREST)
    sheet.paste(big, (x, y + lab), big)
sheet.save(f"{OUT}/{TAG}_all_elements.png")
print("ok", len(outs))
