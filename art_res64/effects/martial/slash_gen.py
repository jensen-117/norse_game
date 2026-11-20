"""A coded slash: an invisible blade tip travels an arc, and only its smear is drawn.
The smear is the band between the arc (radius r) and a thinner inner edge, visible from the tip back along a
trailing window: thick at the tip, tapering to nothing at the tail. When the tip stops, the tail catches up.
Every pixel is decided from polar coordinates, so the shape is exact at any size and in any direction.
    slash_frames(r=12, start=-110, end=60, frames=7, trail=90, width=4, ...) -> list of RGBA images"""
import math
from PIL import Image

WHITE = [(255, 255, 255), (199, 220, 208), (155, 171, 178)]   # ffffff, c7dcd0, 9babb2: edge, body, tail

def ease_out(t): return 1 - (1 - t) ** 2      # fast through the middle, a short brake at the end

def slash_frames(r=14, start=-120, end=70, frames=5, settle=3, trail=150, width=6.0, size=(40, 40),
                 centre=None, flip=False, colours=WHITE):
    """Angles in degrees, 0 = right, positive = clockwise (screen y points down)."""
    W, H = size; cx, cy = centre or (W / 2, H / 2)
    out = []
    total = frames + settle
    for f in range(total):
        if f < frames:
            head = start + (end - start) * ease_out((f + 1) / frames)
            tail = max(start, head - trail)
        else:                                         # the tip has stopped: the tail runs in
            head = end; k = (f - frames + 1) / (settle + 1)
            tail = max(start, end - trail) + (end - max(start, end - trail)) * k
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = im.load()
        span = max(1e-6, head - tail)
        for y in range(H):
            for x in range(W):
                dx, dy = (x + 0.5 - cx), (y + 0.5 - cy)
                if flip: dx = -dx
                d = math.hypot(dx, dy); a = math.degrees(math.atan2(dy, dx))
                for wrap in (a - 360, a, a + 360):     # keep the angle comparable to the window
                    if tail <= wrap <= head: break
                else: continue
                u = (wrap - tail) / span                 # 0 at the tail, 1 at the tip
                w = width * (u ** 1.6)                   # thick at the tip, nothing at the tail
                if w < 0.6: continue
                inner = r - w
                if not (inner <= d <= r + 0.5): continue
                c = colours[0] if d >= r - 1 else (colours[1] if u > 0.35 else colours[2])
                px[x, y] = c + (255,)
        out.append(im)
    return out

if __name__ == "__main__":
    import sys
    fr = slash_frames()
    sheet = Image.new("RGBA", (40 * len(fr), 40), (62, 53, 70, 255))
    for i, im in enumerate(fr): sheet.alpha_composite(im, (40 * i, 0))
    sheet.resize((sheet.width * 6, sheet.height * 6), Image.NEAREST).save(sys.argv[1])
