"""The Mogel and the composer in the sim: 3 recruits vs composed packs."""
import random, sys
from collections import defaultdict
import data, engine
from engine import *
from run_spirits import hire
from composer import catalog, gate, compose, place, spawn, roll_biome

CAT = catalog()
SCENARIOS = {
    "Mogel only":        lambda rng: (gate(CAT, family="Mogel", **roll_biome(rng)[1]), {}),
    "Ande only":         lambda rng: (gate(CAT, family="Ande", **roll_biome(rng)[1]), {}),
    "Mixed biome":       lambda rng: (gate(CAT, **roll_biome(rng)[1]), dict(family_min={"Mogel": 1, "Ande": 1})),
    "Mixed, drawn only": lambda rng: (gate(CAT, art_only=True, **roll_biome(rng)[1]), dict(family_min={"Mogel": 1, "Ande": 1})),
}

def batch(level, n, seed=1, quiet=False):
    rng = random.Random(seed)
    res = {}
    cls = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for name, mk in SCENARIOS.items():
        wins, lengths, reforms = 0, [], 0
        for _ in range(n):
            pool, rules = mk(rng)
            foes = spawn(place(compose(rng, pool, rules)), level)
            party = hire(level, rng)
            b = Battle(party, foes, rng); w = b.fight() == "party"
            wins += w; lengths.append(b.round); reforms += sum(getattr(f, "reforms", 0) for f in foes)
            for u in party: c = cls[u.cls][name]; c[0] += 1; c[1] += w
        lengths.sort()
        res[name] = (wins / n, lengths[n // 2], reforms / n)
        if not quiet:
            print(f"  {name:<18} party wins {wins/n:4.0%}   median {lengths[n//2]:>2} rounds   re-forms/fight {reforms/n:.1f}")
    return res, cls

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    for L in (10, 30, 60):
        print(f"\n=== Level {L}, {n} fights per scenario (MOGEL_REFORM_HP {data.MOGEL_REFORM_HP}) ===")
        res, cls = batch(L, n)
        if L == 30:
            print(f"\n  {'class':<10} " + " ".join(f"{s:>18}" for s in SCENARIOS))
            for c in sorted(cls, key=lambda c: (CLASSES[c]['kind'], c)):
                print(f"  {c:<10} " + " ".join(f"{cls[c][s][1]/max(1,cls[c][s][0]):>18.0%}" for s in SCENARIOS))
