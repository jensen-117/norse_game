"""School uniforms (Nov 10): Joseph's 32R magicals with their robes repainted per school, so every magical body
can wear every school's colours. The robe is found by flood-fill from its main colour through the sprite's robe
colours only (hair, staffs and books that share a colour stay put unless they touch the robe), then each robe tone
maps by lightness rank: the main tone to the school's mid, lighter to light, darker to dark, darker still to deep.
python3 uniforms.py  ->  art_work/uniforms/{check.png, sheet.png}"""
import sys
import numpy as np
from PIL import Image
F = "/home/claude/art_work/heroes32/frame%d.png"
OUT = "/home/claude/art_work/uniforms"
SCHOOLS = {   # light, mid, dark, deep (the wizard's robes, plus a deep step)
    "Eld":   ("ea4f36", "b33831", "6e2727", "45293f"),
    "Vatn":  ("4d9be6", "4d65b4", "484a77", "323353"),
    "Blast": ("c7dcd0", "9babb2", "7f708a", "625565"),
    "Jord":  ("a2a947", "676633", "4c3e24", "313638"),
    "Sol":   ("fbff86", "f9c22b", "f79617", "9e4539"),     # gold, not orange: sunlight
    "Natt":  ("905ea9", "6b3e75", "45293f", "2e222f"),
}
SCHOOL_OF = {"Brennumar": "Eld", "Hafrunar": "Vatn", "Skurmar": "Blast", "Lundar": "Jord", "Dagskald": "Sol", "Seidar": "Natt"}
# Joseph's 1-based frame: (main robe colour, the other robe colours)
ROBE = {8: ("9e4539", ["45293f"]), 9: ("fbff86", ["92a984"]), 10: ("4d9be6", ["484a77", "323353"]),
        12: ("7f708a", ["484a77"]), 13: ("484a77", []), 14: ("4d65b4", ["4d9be6", "323353"])}

KEEP = {9: [(0, 0, 8, 13)],     # the gold cross on the staff shares the priest's robe yellow
        14: [(0, 0, 9, 31)]}    # the orb's ring (left of the body) shares the robe's light blue

def largest(m):
    """The biggest 4-connected blob of a mask (the robe, not a cross on a staff in the same colour)."""
    seen = np.zeros_like(m); best = None
    for y, x in zip(*np.nonzero(m)):
        if seen[y, x]: continue
        blob, st = [], [(y, x)]; seen[y, x] = True
        while st:
            cy, cx = st.pop(); blob.append((cy, cx))
            for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and m[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; st.append((ny, nx))
        if best is None or len(blob) > len(best): best = blob
    out = np.zeros_like(m)
    for y, x in best or []: out[y, x] = True
    return out

def rgb(h): return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)])
def lum(h): r, g, b = rgb(h); return 0.299 * r + 0.587 * g + 0.114 * b

def load(fr): return np.array(Image.open(F % (fr - 1)).convert("RGBA"))

def robe_mask(a, fr):
    main, others = ROBE[fr]; cols = {main, *others}
    hexes = np.array([["%02x%02x%02x" % tuple(p[:3]) if p[3] else "" for p in row] for row in a])
    inset = np.isin(hexes, list(cols))
    for x0, y0, x1, y1 in KEEP.get(fr, ()): inset[y0:y1 + 1, x0:x1 + 1] = False   # props in robe colours
    m = inset.copy(); h, w = m.shape      # every robe-coloured pixel outside the props (a hood can be all shade)
    grew = True
    while grew:                       # flood from the main colour through the robe colours (4-neighbours)
        n = m.copy()
        n[1:] |= m[:-1]; n[:-1] |= m[1:]; n[:, 1:] |= m[:, :-1]; n[:, :-1] |= m[:, 1:]
        n &= inset; grew = (n != m).any(); m = n
    return m, hexes

def tone_map(fr, school):
    main, others = ROBE[fr]; L, M, D, X = SCHOOLS[school]
    lighter = sorted([c for c in others if lum(c) > lum(main)], key=lum, reverse=True)
    darker = sorted([c for c in others if lum(c) <= lum(main)], key=lum, reverse=True)
    out = {main: M}
    for c in lighter: out[c] = L
    for i, c in enumerate(darker): out[c] = (D, X)[min(i, 1)]
    return out

NATIVE = {9: "Sol", 12: "Blast", 14: "Vatn"}    # a body in its own school keeps Joseph's colours

def uniform(fr, school):
    if NATIVE.get(fr) == school: return Image.fromarray(load(fr))
    a = load(fr); m, hexes = robe_mask(a, fr); tm = tone_map(fr, school); out = a.copy()
    for y, x in zip(*np.nonzero(m)): out[y, x, :3] = rgb(tm[hexes[y, x]])
    return Image.fromarray(out)

def check(fr):
    a = load(fr); m, _ = robe_mask(a, fr); out = a.copy(); out[m] = (255, 0, 255, 255); return Image.fromarray(out)

if __name__ == "__main__":
    S = 6; frs = list(ROBE)
    ck = Image.new("RGBA", (len(frs) * 2 * 33 * S, 33 * S), (60, 62, 72, 255))
    for i, fr in enumerate(frs):
        ck.alpha_composite(Image.fromarray(load(fr)).resize((32 * S, 32 * S), Image.NEAREST), (i * 2 * 33 * S, 0))
        ck.alpha_composite(check(fr).resize((32 * S, 32 * S), Image.NEAREST), ((i * 2 + 1) * 33 * S, 0))
    ck.save(f"{OUT}/check.png")
    S = 4; sc = list(SCHOOLS)
    sh = Image.new("RGBA", (len(sc) * 33 * S + 40, len(frs) * 33 * S), (60, 62, 72, 255))
    for r, fr in enumerate(frs):
        for c, school in enumerate(sc):
            sh.alpha_composite(uniform(fr, school).resize((32 * S, 32 * S), Image.NEAREST), (c * 33 * S, r * 33 * S))
    sh.save(f"{OUT}/sheet.png"); print("ok")
