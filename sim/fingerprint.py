"""Fixed-party fingerprint (refactor_plan Wave 0).

regress.py hires random recruits; this one fights fixed parties, so a refactor of the engine's internals (Waves 1a
and 2a) can prove it changed nothing: same seeds, same parties, same packs, every event, one hash.

    python3 fingerprint.py save checks/fp_base.json     # record the baseline
    python3 fingerprint.py check checks/fp_base.json    # compare: identical, or the first fight and event that differs

Parties: the starting three, then the Dagskald and the Skurmar each swapped in for one of them. Heroes are built by
birth() from fixed seeds (the old path, untouched until Wave 3). Every place, levels 10 and 30.
"""
import json, random, sys, hashlib
from engine import *
from composer import catalog, habitat, compose, place, spawn

PARTIES = [("Vasara", "Ullar", "Brennumar"), ("Vasara", "Ullar", "Dagskald"), ("Vasara", "Skurmar", "Brennumar"),
           ("Dagskald", "Ullar", "Skurmar")]
PLACES = ["Barrow", "Wildwood", "Rapids"]
LEVELS = [10, 30]
CAT = catalog()

def party(classes, level, seed):
    out = []
    for i, c in enumerate(classes):
        u = birth(c, level, random.Random(seed * 31 + i))
        u.pouch = [["life", 1], ["firecracker", 1]]
        out.append(u)
    return out

def fights(n=12):
    out = []
    for L in LEVELS:
        for pi, classes in enumerate(PARTIES):
            for hab in PLACES:
                for i in range(n):
                    seed = L * 10000 + pi * 1000 + PLACES.index(hab) * 100 + i
                    rng = random.Random(seed)
                    foes = spawn(place(compose(rng, habitat(CAT, hab))), L)
                    b = Battle(party(classes, L, seed), foes, rng, events=True)
                    w = b.fight()
                    out.append(dict(key=f"L{L} {'/'.join(classes)} {hab} #{i}", w=w, r=b.round, ev=b.events))
    return out

def digest(res): return hashlib.sha1(json.dumps(res, sort_keys=True, default=str).encode()).hexdigest()

if __name__ == "__main__":
    mode, path = sys.argv[1], sys.argv[2]
    res = fights(int(sys.argv[3]) if len(sys.argv) > 3 else 12)
    h = digest(res)
    if mode == "save":
        json.dump(dict(hash=h, fights=res), open(path, "w"), sort_keys=True, default=str)
        print(f"saved {len(res)} fights, {sum(len(r['ev']) for r in res)} events: {h}")
    else:
        base = json.load(open(path))
        if base["hash"] == h: print(f"identical: {len(res)} fights, {h}"); sys.exit(0)
        cur = json.loads(json.dumps(res, sort_keys=True, default=str))
        for a, b in zip(base["fights"], cur):
            if a != b:
                for j, (x, y) in enumerate(zip(a["ev"], b["ev"])):
                    if x != y:
                        print(f"DIFFERS: {a['key']}, event {j}\n  was: {x}\n  now: {y}"); break
                else: print(f"DIFFERS: {a['key']} (length or result: {a['w']}/{a['r']} vs {b['w']}/{b['r']})")
                break
        sys.exit(1)
