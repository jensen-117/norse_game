"""Bid's power across a few values, against plain, with martial root skills swapped (see manner_check)."""
import sys, grammar
from manner_check import run
from run_families import FAMS
n, level = int(sys.argv[1]), int(sys.argv[2])
fams = FAMS + ["Mogel (drawn)"]
base = run(level, n, None, fams)
avg = lambda r: sum(r[f][0] for f in fams) / len(fams)
print(f"Level {level}, {n} fights per family: plain {avg(base):.1%}")
for p in (2.6, 2.8, 3.0):
    grammar.MANNERS["Bid"]["power"] = p
    print(f"  Bid x{p}: {avg(run(level, n, 'Bid', fams)):.1%}")
