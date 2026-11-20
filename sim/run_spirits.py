"""Encounter v0 with the Ande spirits: 3 recruits vs a 6-slot spirit pack."""
import random, sys
from collections import defaultdict
from engine import *
import engine

def hire(level, rng, training="1pt"):
    party, seen = [], set()
    while len(party) < 3:
        u = recruit(level, rng, training)
        if u.cls not in seen: party.append(u); seen.add(u.cls)
    return party

def shape(foes):
    if any(getattr(f, "rank", "") == "Drott" for f in foes): return "boss"
    if len(foes) >= 4: return "swarm"
    return "mixed"

def logged(level=30, seed=4):
    rng = random.Random(seed)
    party, foes = hire(level, rng), spirit_encounter(level, rng)
    print(f"=== Logged fight, level {level}: {', '.join(u.cls for u in party)} vs "
          f"{', '.join(f.name for f in foes)} ===")
    for f in foes:
        print(f"  {f.name}: HP {f.maxhp:.0f}, {f.actions_per_round} action(s): {', '.join(m['name'] for m in f.actions)}")
    b = Battle(party, foes, rng, log=True); b.fight()
    print("\n".join(b.lines))

def batch(level, n=2000, seed=1):
    rng = random.Random(seed)
    res = defaultdict(lambda: [0, 0, 0])            # shape -> fights, wins, rounds
    cls = defaultdict(lambda: defaultdict(lambda: [0, 0]))   # class -> shape -> present, wins
    out = defaultdict(lambda: [0.0, 0])             # class -> output per round, count
    weak = defaultdict(float); bonus = 0; lengths = []
    for _ in range(n):
        party, foes = hire(level, rng), spirit_encounter(level, rng)
        b = Battle(party, foes, rng); w = b.fight() == "party"
        s = shape(foes); r = res[s]; r[0] += 1; r[1] += w; r[2] += b.round
        bonus += b.bonus_rounds; lengths.append(b.round)
        for u in party:
            for key in (s, "all"):
                c = cls[u.cls][key]; c[0] += 1; c[1] += w
            o = out[u.cls]; o[0] += (u.stats["dealt"] + u.stats["healed"]) / b.round; o[1] += 1
            weak[u.cls] += u.stats["weak"]
    lengths.sort()
    tot = sum(v[0] for v in res.values()); wins = sum(v[1] for v in res.values())
    print(f"\n=== Level {level}: {n} fights, 3 recruits vs a 6-slot spirit pack ===")
    print(f"  party win rate {wins/tot:.0%}   median fight {lengths[n//2]} rounds (90th pct {lengths[int(n*.9)]})"
          f"   bonus rounds per fight {bonus/n:.2f}")
    for s in ("swarm", "mixed", "boss"):
        f, w_, r = res[s]
        if f: print(f"    {s:<6} {f/tot:4.0%} of fights   win {w_/f:4.0%}   avg {r/f:4.1f} rounds")
    print(f"  {'class':<10} {'all':>5} {'swarm':>6} {'mixed':>6} {'boss':>6} {'out/rnd':>8} {'weak/f':>7}")
    for c in sorted(cls, key=lambda c: -cls[c]["all"][1] / cls[c]["all"][0]):
        row = [cls[c][k][1] / cls[c][k][0] if cls[c][k][0] else 0 for k in ("all", "swarm", "mixed", "boss")]
        print(f"  {c:<10} " + " ".join(f"{x:5.0%} " for x in row) + f" {out[c][0]/out[c][1]:7.1f} {weak[c]/cls[c]['all'][0]:7.2f}")

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    if len(sys.argv) > 2: engine.SPIRIT_HP_SCALE = float(sys.argv[2])
    if len(sys.argv) > 3: engine.SPIRIT_DMG_SCALE = float(sys.argv[3])
    if "nolog" not in sys.argv: logged()
    for L in (10, 30, 60): batch(L, n)
