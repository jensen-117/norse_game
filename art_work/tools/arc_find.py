"""Find a baked slash arc in a source frame: the biggest blob of pure white (20px or more), grown into the arc's
own shading colours. The first 2 steps may touch the outline (the arc's inner rim lies against the body); further
steps may not (so the growth stops at the arm)."""
import numpy as np
GROW = {"97ad7d", "8f652b", "a08436", "545f32", "61381e", "798460", "404a24", "989a8f"}
def hx(p): return '%02x%02x%02x' % tuple(int(v) for v in p[:3])
def arc_pixels(cell, free_steps=2, steps=4):
    H, W = cell.shape[:2]
    white = {(y, x) for y in range(H) for x in range(W) if cell[y, x, 3] and hx(cell[y, x]) == "ffffff"}
    comps = []; left = set(white)
    while left:
        st = [left.pop()]; comp = set(st)
        while st:
            y, x = st.pop()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    q = (y + dy, x + dx)
                    if q in left: left.discard(q); comp.add(q); st.append(q)
        comps.append(comp)
    if not comps or max(map(len, comps)) < 20: return set()
    arc = set(max(comps, key=len)); frontier = list(arc)
    ink = lambda y, x: 0 <= y < H and 0 <= x < W and cell[y, x, 3] and hx(cell[y, x]) == "13131c"
    for step in range(steps):
        nxt = []
        for y, x in frontier:
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                Y, X = y + dy, x + dx
                if (Y, X) in arc or not (0 <= Y < H and 0 <= X < W) or not cell[Y, X, 3]: continue
                if hx(cell[Y, X]) not in GROW: continue
                if step >= free_steps and any(ink(Y + a, X + b) for a, b in ((1,0),(-1,0),(0,1),(0,-1))): continue
                arc.add((Y, X)); nxt.append((Y, X))
        frontier = nxt
    return arc
