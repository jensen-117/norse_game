"""Joseph's 32rogues-based Beinar (art_res64/beinar_1.aseprite, Nov 9): rank tints, pass 3 (Joseph's rule).
Ranks: white, aged, red, earth. Only bone changes; every other colour stays the sprite's own.
  Bare skeletons and the archer (1-6, 13, 14): bone = white and greys (ffffff, 9babb2, 7f708a), minus steel:
    blades (a box per frame) and the shield's metal (its greys; the white inside the shield is the hand, so it is bone).
  Robed ones (7-12): bone = the face and hands (c7dcd0), which already are "aged"; their white is their weakest rank.
Frame numbers are Joseph's (1-based)."""
import numpy as np
from PIL import Image, ImageDraw
F = "beinar_32r/frames/frame%d.png"
def rgb(h): return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)])
def hx(p): return "%02x%02x%02x" % tuple(p[:3])
RANKS = ["white", "aged", "red", "earth"]
BONE = ["7f708a", "9babb2", "ffffff"]                       # shade, mid, light
TINTS = {"white": ["7f708a", "9babb2", "ffffff"],
         "aged":  ["7f708a", "ab947a", "c7dcd0"],
         "red":   ["ae2334", "e83b3b", "f68181"],
         "earth": ["6e2727", "9e4539", "cd683d"]}
ROBED = {7, 8, 9, 10, 11, 12}
BLADE = {1: (8, 13), 5: (8, 13), 4: (5, 12), 13: (6, 12), 14: (5, 17)}    # bone-grey pixels with x<=X and y<=Y are steel
SHIELD = {4, 5}
def bone_mask(fr):
    a = np.array(Image.open(F % (fr - 1)).convert("RGBA")); m = np.zeros((32, 32), bool)
    for y, x in zip(*np.nonzero(a[:, :, 3])):
        h = hx(a[y, x])
        if fr in ROBED: m[y, x] = h == "c7dcd0"; continue
        if h not in BONE: continue
        if fr in BLADE and x <= BLADE[fr][0] and y <= BLADE[fr][1]: continue
        if fr in SHIELD and y >= 16 and h != "ffffff":
            xs = [c for c in range(21, 32) if a[y, c, 3] and hx(a[y, c]) in ("2e222f", "323353", "625565")]
            if xs and x >= min(xs): continue                         # the shield's rim
        m[y, x] = True
    return a, m
def tint(fr, rank):
    a, m = bone_mask(fr); a = a.copy()
    for y, x in zip(*np.nonzero(m)):
        h = hx(a[y, x])
        a[y, x, :3] = rgb(TINTS[rank][2] if fr in ROBED else TINTS[rank][BONE.index(h)])
    return a
def check(fr):    # what counts as bone, in magenta
    a, m = bone_mask(fr); a = a.copy(); a[m, :3] = (255, 0, 255); return a
if __name__ == "__main__":
    S = 3; W = 32 * S + 4; frames = list(range(1, 15)); rows = RANKS + ["bone?"]
    im = Image.new("RGBA", (50 + W * len(frames), 16 + W * len(rows)), (62, 53, 70, 255)); d = ImageDraw.Draw(im)
    for j, fr in enumerate(frames): d.text((50 + j * W + 40, 3), str(fr), fill="white")
    for r, rank in enumerate(rows):
        d.text((4, 16 + r * W + 42), rank, fill="white")
        for j, fr in enumerate(frames):
            t = check(fr) if rank == "bone?" else tint(fr, rank)
            im.alpha_composite(Image.fromarray(t).resize((32 * S, 32 * S), Image.NEAREST), (50 + j * W, 16 + r * W))
    im.save("beinar_32r/tint_ranks.png"); print(im.size)
