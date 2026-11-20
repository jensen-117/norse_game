"""Fingerprint: many fights across habitats and levels, every event. Compare before/after a refactor."""
import random, json, sys, hashlib
import engine
from engine import *
from run_spirits import hire
from composer import catalog, habitat, compose, place, spawn, roll_biome, gate
CAT = catalog()
def fights(n=60):
    out = []
    for L in (10, 30):
        for hab in ("Barrow", "Wildwood", "Rapids", None):
            rng = random.Random(1000 + L + (hash(hab) % 97 if hab else 0) if False else 1000 + L + len(hab or ""))
            for i in range(n):
                pool = habitat(CAT, hab) if hab else gate(CAT, **roll_biome(rng)[1])
                party = hire(L, rng)
                for h in party: h.pouch = [["life", 1], ["firecracker", 1]]
                b = Battle(party, spawn(place(compose(rng, pool)), L), rng, events=True)
                w = b.fight()
                out.append(dict(w=w, r=b.round, ev=b.events))
    return out
if __name__ == "__main__":
    res = fights(int(sys.argv[2]) if len(sys.argv) > 2 else 60)
    s = json.dumps(res, sort_keys=True, default=str)
    open(sys.argv[1], "w").write(s)
    from collections import Counter
    print(hashlib.sha1(s.encode()).hexdigest(), Counter(r["w"] for r in res), len(res))
