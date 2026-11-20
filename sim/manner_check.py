"""A/B: martial heroes' root skills (Base and Mer) compiled with each manner in turn.
Same seeds per family, so every column fights the same parties against the same packs."""
import random, sys
import engine
from engine import *
from grammar import compile_word, WEAPON
from run_spirits import hire
from run_families import encounter, FAMS
from speed_check import composed

def remanner(party, manner):
    for u in party:
        if CLASSES[u.cls]["kind"] != "martial": continue
        for i, a in enumerate(u.actions):
            p = a.get("parts")
            root = next((r for r in WEAPON if a["name"].lower().endswith(r.lower())), None)
            if a["kind"] != "damage" or a["tier"] not in ("Base", "Mer") or not root or a["status"] or a.get("shape"): continue
            new = compile_word(root, a["tier"], manner=manner)
            if "reach" in a: new["reach"] = a["reach"]
            u.actions[i] = new

def run(level, n, manner, fams):
    out = {}
    for fam in fams:
        rng = random.Random(23)
        w = 0; lens = []; used = 0; acts = 0
        for _ in range(n):
            party = hire(level, rng); remanner(party, manner)
            foes = composed(level, rng, fam.split()[0]) if "drawn" in fam else encounter(level, rng, fam)
            b = Battle(party, foes, rng); w += b.fight() == "party"; lens.append(b.round)
        lens.sort()
        out[fam] = (w / n, lens[n // 2])
    return out

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    level = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    fams = FAMS + ["Mogel (drawn)"]
    cols = [None, "Snar", "Tung", "Bid", "Jarf", "Drif"]
    res = {m: run(level, n, m, fams) for m in cols}
    print(f"=== Level {level}, {n} fights per cell: party wins (median rounds), martial root skills swapped ===")
    print(f"  {'family':<14}" + "".join(f"{str(m or 'plain'):>12}" for m in cols))
    for f in fams:
        print(f"  {f:<14}" + "".join(f"{res[m][f][0]:>7.0%} ({res[m][f][1]:>2})" for m in cols))
    avg = {m: sum(res[m][f][0] for f in fams) / len(fams) for m in cols}
    print(f"  {'average':<14}" + "".join(f"{avg[m]:>12.0%}" for m in cols))
