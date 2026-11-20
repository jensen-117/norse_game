"""A/B: no board vs the board (reach, protection, exposure, Advance), every family and the composer packs."""
import random, sys
from collections import defaultdict
import engine
from engine import *
from run_spirits import hire
from run_families import encounter, FAMS
from speed_check import composed

def run(level, n, flag):
    engine.USE_BOARD = flag
    out, cls = {}, defaultdict(lambda: [0, 0])
    kinds = defaultdict(lambda: [0, 0])          # hero kind -> [present, downed]
    for fam in FAMS + ["Mogel (drawn)", "Ande (drawn)"]:
        rng = random.Random(11)
        w = 0; lens = []; rm = fz = mv = 0
        for _ in range(n):
            party = hire(level, rng)
            foes = composed(level, rng, fam.split()[0]) if "drawn" in fam else encounter(level, rng, fam)
            b = Battle(party, foes, rng); win = b.fight() == "party"; w += win; lens.append(b.round)
            rm += sum(u.stats["rear_melee"] for u in party); fz += sum(u.stats["fizzles"] for u in b.units)
            mv += sum(u.stats["moves"] for u in b.units)
            for u in party:
                c = cls[u.cls]; c[0] += 1; c[1] += win
                k = kinds[CLASSES[u.cls]["kind"]]; k[0] += 1; k[1] += u.stats["downs"] > 0
        lens.sort()
        out[fam] = (w / n, lens[n // 2], rm / n, fz / n, mv / n)
    return out, cls, kinds

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    for L in (10, 30):
        (a, ca, ka), (b, cb, kb) = run(L, n, False), run(L, n, True)
        print(f"\n=== Level {L}, {n} fights each: no board -> board ===")
        print(f"  {'family':<14} {'party wins':>16} {'median rounds':>14} {'rear-melee hits':>16} {'fizzles':>8} {'advances':>9}")
        for f in a:
            print(f"  {f:<14} {a[f][0]:>7.0%} -> {b[f][0]:<5.0%} {a[f][1]:>6} -> {b[f][1]:<4} {b[f][2]:>16.1f} {b[f][3]:>8.2f} {b[f][4]:>9.2f}")
        print(f"\n  {'class':<10} {'win, no board':>14} {'board':>7}")
        for c in sorted(ca, key=lambda c: (CLASSES[c]['kind'], c)):
            print(f"  {c:<10} {ca[c][1]/ca[c][0]:>14.0%} {cb[c][1]/cb[c][0]:>7.0%}")
        print("  heroes Downed at least once: " + ", ".join(
            f"{k} {ka[k][1]/ka[k][0]:.0%} -> {kb[k][1]/kb[k][0]:.0%}" for k in ka))
