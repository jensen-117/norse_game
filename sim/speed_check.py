"""A/B: the old turn order vs speed groups, across every family and the composer packs."""
import random, sys
import engine
from engine import *
from run_spirits import hire
from run_families import encounter, FAMS
from composer import catalog, gate, compose, place, spawn, roll_biome

CAT = catalog()
def composed(level, rng, fam):
    pool = gate(CAT, family=fam, art_only=True, **roll_biome(rng)[1])
    return spawn(place(compose(rng, pool)), level)

def run(level, n, flag):
    engine.USE_SPEED_GROUPS = flag
    out = {}
    for fam in FAMS + ["Mogel (drawn)", "Ande (drawn)"]:
        rng = random.Random(11)
        w = r = d = bl = late = 0; lens = []
        for _ in range(n):
            party = hire(level, rng)
            foes = composed(level, rng, fam.split()[0]) if "drawn" in fam else encounter(level, rng, fam)
            b = Battle(party, foes, rng); w += b.fight() == "party"; lens.append(b.round)
            d += sum(u.stats["defends"] for u in b.units); bl += sum(u.stats["blocked"] for u in b.units)
            late += sum(u.stats["late"] for u in b.units)
        lens.sort()
        out[fam] = (w / n, lens[n // 2], d / n, bl / n, late / n)
    return out

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    for L in (10, 30):
        a, b = run(L, n, False), run(L, n, True)
        print(f"\n=== Level {L}, {n} fights each: old order -> speed groups ===")
        print(f"  {'family':<14} {'party wins':>16} {'median rounds':>14} {'defends/fight':>15} {'blocked/fight':>15} {'late defends':>13}")
        for f in a:
            print(f"  {f:<14} {a[f][0]:>7.0%} -> {b[f][0]:<5.0%} {a[f][1]:>6} -> {b[f][1]:<4} {a[f][2]:>6.1f} -> {b[f][2]:<5.1f} "
                  f"{a[f][3]:>6.0f} -> {b[f][3]:<6.0f} {a[f][4]:>5.2f} -> {b[f][4]:.2f}")
