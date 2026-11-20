"""Mogel without their glint (Nov 9, Joseph's idea): the brightest k colours of each sprite are removed and
back-filled from the neighbouring body colour, outside in. Ink (2e222f) is never a source or a target."""
import json
import numpy as np
from PIL import Image
INK = (0x2e, 0x22, 0x2f)
def lum(c): return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def dull(im, k=1):
    a = np.array(im.convert("RGBA")); op = a[:, :, 3] > 0
    cols = sorted({tuple(p[:3]) for p in a[op]} - {INK}, key=lum, reverse=True)
    if len(cols) < 4: return Image.fromarray(a)          # too few tones to spare any
    gone = set(cols[:k]); hole = op & np.array([[tuple(a[y, x, :3]) in gone for x in range(a.shape[1])] for y in range(a.shape[0])])
    while hole.any():
        fill = []
        for y, x in zip(*np.nonzero(hole)):
            seen = {}
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if (dy or dx) and 0 <= yy < a.shape[0] and 0 <= xx < a.shape[1] and op[yy, xx] and not hole[yy, xx]:
                        c = tuple(a[yy, xx, :3])
                        if c != INK: seen[c] = seen.get(c, 0) + 1
            if seen: fill.append((y, x, max(seen.items(), key=lambda t: (t[1], lum(t[0])))[0]))
        if not fill: break
        for y, x, c in fill: a[y, x, :3] = c; hole[y, x] = False
    return Image.fromarray(a)
if __name__ == "__main__":
    A = json.load(open("fight_lab/assets/assets.json")); at = Image.open("fight_lab/assets/atlas.png").convert("RGBA")
    bg = Image.open("fight_lab/assets/bg_Neutral.png").convert("RGBA").crop((0, 100, 1, 101)).getpixel((0, 0))
    ELS = ["Eld", "Reyk", "Vatn", "Hrim", "Blast", "Blixt", "Jord", "Gro", "Sol", "Lak", "Natt", "Aska"]
    out = Image.new("RGBA", (len(ELS) * 36 * 2 + 8, 3 * 36), (0x3e, 0x35, 0x46, 255))
    for r, k in enumerate([0, 1, 2]):
        for j, el in enumerate(ELS):
            for s, size in enumerate((32, 16)):
                x, y, w, h = A["sprites"][f"mogel{size}:{el}"]["anims"]["idle"][0]
                im = at.crop((x, y, x + w, y + h)); im = dull(im, k) if k else im
                out.alpha_composite(im, (4 + j * 72 + s * 36, 2 + r * 36 + (32 - h)))
    out.resize((out.width * 3, out.height * 3), Image.NEAREST).save("art_work/beinar_32r/mogel_dull_strip.png"); print(out.size)
