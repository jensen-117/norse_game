"""Encounter v0 -- run one logged fight, then batches."""
import random, sys, statistics as st
from collections import defaultdict
from engine import *

def party_of(classes, level, rng, training):
    return [birth(c, level, rng, training) for c in classes]

def enemies_at(level, rng=None):
    if rng is None:
        return [spawn("Frost Wolf", level), spawn("Bog Archer", level), spawn("Ember Beetle", level)]
    return [spawn(k, level) for k in rng.sample(list(ENEMIES), 3)]

def show_unit(u):
    a = {k: round(v) for k, v in u.attrs.items()}
    aff = ", ".join(f"{k}:{v}" for k, v in sorted(u.aff.items()))
    kit = ", ".join(x["name"] + (f" ({x['cost']} {x['cost_type']})" if x["cost"] else "") for x in u.actions)
    extra = f"  sign {u.sign}, +{u.personality[0]}/-{u.personality[1]}" if u.cls else ""
    return (f"  {u.name}{extra}\n    HP {u.maxhp:.0f}  MP {u.maxmp:.0f}  ATK {u.ATK:.0f}  MAT {u.MAT:.0f}"
            f"  DEF {u.DEF:.0f}  MDF {u.MDF:.0f}  SPD {u.attrs['SPD']:.0f}\n    affinity: {aff}\n    kit: {kit}")

def logged(level=25, seed=3, classes=("Brennumar", "Hersir", "Dagskald")):
    rng = random.Random(seed)
    party = party_of(classes, level, rng, "1pt")
    foes = enemies_at(level)
    print(f"=== Logged fight, level {level} ===")
    for u in party + foes: print(show_unit(u))
    b = Battle(party, foes, rng, log=True)
    b.fight()
    print("\n".join(b.lines))

def batch(level, training, n=3000, seed=1):
    rng = random.Random(seed)
    wins = rounds = bonus = 0
    lengths = []
    by_class = defaultdict(lambda: defaultdict(float))
    present = defaultdict(int); present_wins = defaultdict(int)
    agg = defaultdict(float)
    fitw = defaultdict(lambda: [0, 0])
    allc = list(CLASSES)
    for i in range(n):
        party, seen = [], set()
        while len(party) < 3:                      # hire the first three distinct classes off the board
            u = recruit(level, rng, training)
            if u.cls not in seen: party.append(u); seen.add(u.cls)
        b = Battle(party, enemies_at(level, rng), rng)
        w = b.fight()
        wins += w == "party"; rounds += b.round; bonus += b.bonus_rounds; lengths.append(b.round)
        for u in party:
            present[u.cls] += 1; present_wins[u.cls] += (w == "party")
            fitw[u.natural_fit][0] += 1; fitw[u.natural_fit][1] += u.alive
            for k, v in u.stats.items(): by_class[u.cls][k] += v
            by_class[u.cls]["rounds"] += b.round
            by_class[u.cls]["survived"] += u.alive
            by_class[u.cls]["mp_left"] += u.mp / u.maxmp
            for k in ("graze", "hits", "crit"): agg[k] += u.stats[k]
    print(f"\n=== Level {level}, training {training}, {n} fights vs 3 random of 6 creatures ===")
    print(f"  party win rate {wins/n:.0%}   avg rounds {rounds/n:.1f}   bonus rounds per fight {bonus/n:.2f}")
    print(f"  survival: natural fits {fitw[True][1]/max(1,fitw[True][0]):.0%}"
          f" ({fitw[True][0]/(fitw[True][0]+fitw[False][0]):.0%} of hires), odd births {fitw[False][1]/max(1,fitw[False][0]):.0%}")
    lengths.sort()
    print(f"  fight length: median {lengths[n//2]} rounds, 90th percentile {lengths[int(n*0.9)]}")
    tot = agg['graze'] + agg['hits'] + agg['crit']
    print(f"  party rolls: graze {agg['graze']/tot:.0%}  hit {agg['hits']/tot:.0%}  crit {agg['crit']/tot:.0%}")
    print(f"  {'class':<10} {'win%':>5} {'dmg/rnd':>8} {'heal/rnd':>8} {'weak/f':>7} {'stat/f':>7} {'surv%':>6} {'MP left':>8}")
    for c in sorted(present, key=lambda c: -present_wins[c] / present[c]):
        d = by_class[c]; p = present[c]
        print(f"  {c:<10} {present_wins[c]/p:5.0%} {d['dealt']/d['rounds']:8.1f} {d['healed']/d['rounds']:8.1f}"
              f" {d['weak']/p:7.2f} {d['statuses']/p:7.2f} {d['survived']/p:6.0%} {d['mp_left']/p:8.0%}")

if __name__ == "__main__":
    import data
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    if len(sys.argv) > 2: data.HP_MULT = float(sys.argv[2])
    import engine; engine.HP_MULT = data.HP_MULT
    trainings = sys.argv[3].split(",") if len(sys.argv) > 3 else ["1pt"]
    if "nolog" not in sys.argv: logged()
    for L in (10, 30, 60):
        for t in trainings:
            batch(L, t, n=n)
