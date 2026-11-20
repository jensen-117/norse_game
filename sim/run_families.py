"""3 recruits vs 6-slot packs from each enemy family: Ande, Draugr, Bein, and mixed Undead."""
import random, sys
from collections import defaultdict
from engine import *
from run_spirits import hire

FAMS = ["Ande", "Draugr", "Bein", "Drattr", "Djur", "Oskorei"]

def encounter(level, rng, fam):
    if fam == "Ande": return spirit_encounter(level, rng)
    if fam == "Oskorei": return oskorei_encounter(level, rng)
    return family_encounter(level, rng, fam)

def logged(level=30, seed=9, fam="Oskorei"):
    rng = random.Random(seed)
    party, foes = hire(level, rng), encounter(level, rng, fam)
    print(f"=== Logged fight, level {level}: {', '.join(u.cls for u in party)} vs {', '.join(f.name for f in foes)} ===")
    for f in foes:
        print(f"  {f.name}: HP {f.maxhp:.0f}, {f.actions_per_round} action(s): {', '.join(m['name'] for m in f.actions)}")
    b = Battle(party, foes, rng, log=True); b.fight(); print("\n".join(b.lines))

def batch(level, n=1500, seed=1):
    rng = random.Random(seed)
    print(f"\n=== Level {level}: {n} fights per family ===")
    table = defaultdict(dict)
    for fam in FAMS:
        wins = 0; lengths = []; tiers = defaultdict(lambda: [0, 0])
        cls = defaultdict(lambda: [0, 0, 0.0, 0.0])      # present, wins, weak hits, output per round
        for _ in range(n):
            party, foes = hire(level, rng), encounter(level, rng, fam)
            b = Battle(party, foes, rng); w = b.fight() == "party"
            wins += w; lengths.append(b.round)
            if fam == "Oskorei": t = tiers[foes[0].oskorei_tier]; t[0] += 1; t[1] += w
            for u in party:
                c = cls[u.cls]; c[0] += 1; c[1] += w; c[2] += u.stats["weak"]
                c[3] += (u.stats["dealt"] + u.stats["healed"]) / b.round
        lengths.sort()
        print(f"  vs {fam:<7} party wins {wins/n:4.0%}   median fight {lengths[n//2]} rounds")
        if tiers: print("      by tier: " + "   ".join(f"T{k} {v[1]/v[0]:.0%}" for k, v in sorted(tiers.items())))
        for c, v in cls.items(): table[c][fam] = v
    print(f"\n  {'class':<10} " + " ".join(f"{f:>12}" for f in FAMS))
    print(f"  {'':<10} " + " ".join(f"{'win weak/f':>12}" for f in FAMS))
    order = sorted(table, key=lambda c: (CLASSES[c]['kind'], c))
    for c in order:
        cells = []
        for f in FAMS:
            p, w, wk, o = table[c][f]
            cells.append(f"{w/p:4.0%} {wk/p:5.1f}")
        print(f"  {c:<10} " + " ".join(f"{x:>12}" for x in cells))

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    if "nolog" not in sys.argv: logged()
    for L in (10, 30, 60): batch(L, n)
