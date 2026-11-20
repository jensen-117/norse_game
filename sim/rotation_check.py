"""A/B on the board: rotation and Cover off vs on, every family and the composer packs, against the no-board target."""
import random, sys
import engine
from engine import *
from run_spirits import hire
from run_families import encounter, FAMS
from speed_check import composed

TARGET = {10: dict(Ande=.25, Draugr=.30, Bein=.25, Drattr=.20, Djur=.24, Oskorei=.38, **{"Mogel (drawn)": .32, "Ande (drawn)": .30}),
          30: dict(Ande=.31, Draugr=.44, Bein=.42, Drattr=.32, Djur=.37, Oskorei=.51, **{"Mogel (drawn)": .53, "Ande (drawn)": .51})}

def run(level, n, rot, fams=None):
    engine.USE_BOARD = True; engine.USE_ROTATION = rot
    out = {}
    for fam in fams or FAMS + ["Mogel (drawn)", "Ande (drawn)"]:
        rng = random.Random(11)
        w = 0; lens = []; st = dict(swaps=0, covers=0, covered=0, moves=0)
        side = dict(party=dict(swaps=0, covers=0), enemy=dict(swaps=0, covers=0))
        for _ in range(n):
            party = hire(level, rng)
            foes = composed(level, rng, fam.split()[0]) if "drawn" in fam else encounter(level, rng, fam)
            b = Battle(party, foes, rng); w += b.fight() == "party"; lens.append(b.round)
            for u in b.units:
                for k in st: st[k] += u.stats[k]
                sd = side["party" if u.side == "party" else "enemy"]
                sd["swaps"] += u.stats["swaps"]; sd["covers"] += u.stats["covers"]
        lens.sort()
        out[fam] = (w / n, lens[n // 2], {k: v / n for k, v in st.items()}, {s: {k: v / n for k, v in d.items()} for s, d in side.items()})
    return out

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    for L in (10, 30):
        a, b = run(L, n, False), run(L, n, True)
        print(f"\n=== Level {L}, {n} fights each: board without rotation -> with rotation (target: no-board rate) ===")
        print(f"  {'family':<14} {'party wins':>16} {'target':>7} {'rounds':>9}   party swaps/covers   enemy swaps/covers   covered hits")
        for f in a:
            p, e = b[f][3]["party"], b[f][3]["enemy"]
            print(f"  {f:<14} {a[f][0]:>7.0%} -> {b[f][0]:<5.0%} {TARGET[L][f]:>7.0%} {a[f][1]:>3} -> {b[f][1]:<3} "
                  f"{p['swaps']:>9.2f} / {p['covers']:<6.2f} {e['swaps']:>9.2f} / {e['covers']:<6.2f} {b[f][2]['covered']:>10.2f}")
