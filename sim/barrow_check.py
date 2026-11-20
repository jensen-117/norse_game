"""Barrow packs with the folklore rules (crawl, piles, guardian Cover) on and off, levels 10 and 30."""
import random, sys
import engine
from engine import *
from run_spirits import hire
from composer import catalog, habitat, compose, place, spawn
CAT = catalog()
def run(level, n, rules=True):
    saved = (engine.DRAUGR_CRAWL_HP, engine.BEIN_PILE_ROUNDS, engine.GUARDIAN_COVER)
    if not rules:
        engine.DRAUGR_FINAL = {"Slash", "Eld", "Crush", "Pierce", None} | set(ELEMENT)   # every blow is final
        engine.BEIN_GUARDIANS = set()
    rng = random.Random(31); w = 0; R = []; ev = dict(crawl=0, pile=0, scatter=0, reassemble=0, covered=0)
    for _ in range(n):
        b = Battle(hire(level, rng), spawn(place(compose(rng, habitat(CAT, "Barrow"))), level), rng, events=True)
        w += b.fight() == "party"; R.append(b.round)
        for e in b.events:
            if e["kind"] in ev: ev[e["kind"]] += 1
    engine.DRAUGR_FINAL = {"Slash", "Eld"}; engine.BEIN_GUARDIANS = {"Halvbeinbryn", "Beinbryn", "Storbeinbryn", "Fornbein"}
    if not rules: engine.piles_off = False
    R.sort()
    return w / n, R[n // 2], {k: v / n for k, v in ev.items()}
if __name__ == "__main__":
    n = int(sys.argv[1])
    for L in (10, 30):
        for on in (False, True):
            if not on:          # piles off: a Bein that falls stays down
                orig = engine.Battle.downed
                def downed(self, t, by=None, _o=orig):
                    if getattr(t, "family", None) == "Bein": t.piled = True
                    return _o(self, t, by)
                engine.Battle.downed = downed
            r = run(L, n, on)
            if not on: engine.Battle.downed = orig
            print(f"Level {L}, rules {'on ' if on else 'off'}: party wins {r[0]:.0%}, median rounds {r[1]}, per fight "
                  + ", ".join(f"{k} {v:.2f}" for k, v in r[2].items()), flush=True)
