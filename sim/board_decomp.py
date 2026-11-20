"""Where does the board's party edge come from? Toggle one board rule at a time (rotation on), level 30."""
import sys, engine
from rotation_check import run, TARGET
if __name__ != "__main__": n, L = 0, 30
else: n = int(sys.argv[1]); L = int(sys.argv[2]) if len(sys.argv) > 2 else 30
fams = ["Draugr", "Bein", "Drattr", "Djur", "Oskorei", "Mogel (drawn)"]
N = [n]
def go(label, **kw):
    old = {k: getattr(engine, k) for k in kw}
    for k, v in kw.items(): setattr(engine, k, v)
    r = run(L, N[0], True, fams)
    for k, v in old.items(): setattr(engine, k, v)
    print(f"  {label:<34}" + "".join(f"{r[f][0]:>9.0%}" for f in fams), flush=True)
if __name__ == "__main__":
    print(f"Level {L}, {n} fights: party wins")
    print(f"  {'':<34}" + "".join(f"{f.split()[0]:>9}" for f in fams))
    print(f"  {'target (no board)':<34}" + "".join(f"{TARGET[L][f]:>9.0%}" for f in fams))
    go("board, rotation on")
    go("Rear melee at full damage", REAR_MELEE_MULT=1.0)
    go("melee reaches the Rear (no protection)", REACH_BY_TYPE={"Slash": "any", "Crush": "any", "Pierce": "any"})
