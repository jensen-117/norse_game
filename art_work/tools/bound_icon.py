"""Bound's icon (Nov 10): Joseph's wind-up swirl in the net Drattr's greens, appended to the 9x9 strip as "bound".
python3 bound_icon.py  (idempotent: rewrites the slot if it's already there)"""
import json
from PIL import Image
P, J = "/home/claude/fight_lab/assets/icons9.png", "/home/claude/fight_lab/assets/icons9.json"
NET = {(0xff, 0xff, 0xff): (0x92, 0xa9, 0x84), (0xc7, 0xdc, 0xd0): (0x23, 0x90, 0x63)}   # light -> sage, pale -> net green
im, idx = Image.open(P).convert("RGBA"), json.load(open(J))
sw = im.crop((idx["windup"] * 9, 0, idx["windup"] * 9 + 9, 9))
px = sw.load()
for y in range(9):
    for x in range(9):
        p = px[x, y]
        if p[3]: px[x, y] = NET.get(p[:3], p[:3]) + (p[3],)
slot = idx.get("bound", im.width // 9)
if slot * 9 >= im.width:
    big = Image.new("RGBA", (im.width + 9, 9)); big.paste(im, (0, 0)); im = big
im.paste(sw, (slot * 9, 0)); im.save(P)
idx["bound"] = slot; json.dump(idx, open(J, "w"))
print("bound ->", slot)
