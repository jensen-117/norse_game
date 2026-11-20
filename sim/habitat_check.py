"""Habitat packs (Barrow, Wildwood, Rapids) under the ranged rule: does a reach unit in the pack give back
what the board took, so the enemy damage knob can come down? Same seeds in every cell."""
import random, sys
import engine
from engine import *
from run_spirits import hire
from composer import catalog, habitat, compose, place, spawn, HABITATS

CAT = catalog()
def run(level, n, hab, ranged, board, knob):
    engine.USE_BOARD = board; engine.SPIRIT_DMG_SCALE = knob
    rng = random.Random(31); w = 0
    for _ in range(n):
        party = hire(level, rng)
        foes = spawn(place(compose(rng, habitat(CAT, hab), dict(ranged=ranged))), level)
        w += Battle(party, foes, rng).fight() == "party"
    return w / n

if __name__ == "__main__":
    n = int(sys.argv[1]); level = int(sys.argv[2])
    conds = [(False, 0.5), (True, 0.5), (True, 0.55), (True, 0.6)]
    print(f"=== Level {level}, {n} fights per cell: party wins ===")
    print(f"  {'habitat':<9} {'ranged':<8}" + "".join(f"{('board' if b else 'no board') + ' ' + str(k):>15}" for b, k in conds))
    for hab in HABITATS:
        for rv in (None, "include", "exclude"):
            r = [run(level, n, hab, rv, b, k) for b, k in conds]
            print(f"  {hab:<9} {str(rv):<8}" + "".join(f"{x:>15.0%}" for x in r), flush=True)
