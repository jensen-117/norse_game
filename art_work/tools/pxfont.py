"""Bitmap font from Joseph's sheet: 16 columns of 8x16 cells on a 9x17 pitch (1px grey grid).
Rows 0-5 are ASCII 0x20-0x7F; later rows assumed to continue from 0xA0."""
from PIL import Image
class PxFont:
    def __init__(self, path):
        im = Image.open(path).convert("RGB"); px = im.load()
        W, H = im.size; self.glyphs = {}
        n = 0
        for row in range((H - 1) // 17):
            for col in range(16):
                cp = 0x20 + n if n < 96 else 0xA0 + (n - 96)
                x0, y0 = 1 + col * 9, 1 + row * 17
                ink = [(x, y) for y in range(16) for x in range(8) if px[x0 + x, y0 + y] == (0, 0, 0)]
                self.glyphs[chr(cp)] = ink; n += 1
        rows = [y for c in map(chr, range(0x21, 0x7F)) for _, y in self.glyphs[c]]
        self.top, self.bot = min(rows), max(rows)          # trim the empty band above caps
    def width(self, ch):
        ink = self.glyphs.get(ch, [])
        return (max(x for x, _ in ink) - min(x for x, _ in ink) + 1) if ink else 3
    def text(self, im, xy, s, color, prop=True, shadow=None):
        x, y = xy
        for ch in s:
            ink = self.glyphs.get(ch, self.glyphs["?"])
            x0 = min((gx for gx, _ in ink), default=0) if prop else 0
            for gx, gy in ink:
                X, Y = x + gx - x0, y + gy - self.top
                if shadow: im.putpixel((X + 1, Y + 1), shadow + (255,))
            for gx, gy in ink:
                im.putpixel((x + gx - x0, y + gy - self.top), color + (255,))
            x += (self.width(ch) + 1) if prop else 8
        return x
    @property
    def height(self): return self.bot - self.top + 1
