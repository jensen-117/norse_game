"""Room adds (Joseph, Nov 20): the sweep's three smallest room shapes, as rolled, then the same rooms with two more
Trash or two more Regulars added, played by the AI. Same seeds as sweep.py, so the "as rolled" rows match its report.
    python3 checks/adds_sweep.py [n]          # prints a markdown table"""
import os, random, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sweep
from engine import *
from composer import habitat, compose, place, spawn as spawn_pack

TIER = lambda e: "Boss" if e["cost"] >= 3 else "Trash" if e["rank"].startswith(("Halv", "Litel")) else "Elite" if e["rank"].startswith("Stor") else "Regular"

def room(rng, where, kind, budget, add=None):
    pool = habitat(sweep.CAT, where)
    want = {"fodder": {"Trash", "Regular"}, "elite": {"Trash", "Regular", "Elite"}, "boss": {"Trash", "Regular", "Boss"}}[kind]
    picks = None
    for _ in range(200):
        p = compose(rng, [e for e in pool if TIER(e) in want], dict(budget=budget, cost_caps={3: 1}))
        ts = [TIER(e) for e in p]
        if kind == "elite" and "Elite" not in ts: continue
        if kind == "boss" and "Boss" not in ts: continue
        picks = p; break
    if add:                                               # the adds come from the same place's pool
        extra = [e for e in pool if TIER(e) == add]
        picks = picks + [rng.choice(extra) for _ in range(2)]
    return spawn_pack(place(picks), ENEMY_LEVEL)

def run(n, party_classes, leg, kind, budget, add):
    wins, lost, falls, rs = 0, [], 0, []
    for i in range(n):
        rng = random.Random(1000 + i); where = ("Barrow", "Wildwood", "Rapids")[i % 3]
        party = [build_hero(c, leg) for c in party_classes]
        foes = room(rng, where, kind, budget, add)
        b = Battle(party, foes, rng); w = b.fight()
        if w == "party":
            wins += 1; rs.append(b.round)
            lost.append(1 - sum(max(0, h.hp) for h in party) / sum(h.maxhp for h in party))
        falls += sum(h.stats["downs"] for h in party)
    return wins / n, statistics.median(rs) if rs else None, statistics.mean(lost) if lost else None, falls / n

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    for label, cls, leg in sweep.PARTIES:
        print(f"\n**{label}:**\n\n| Room | Adds | Wins | Rounds | HP spent | Falls |\n|---|---|---|---|---|---|")
        for kind, budget in (("fodder", 3), ("elite", 4), ("boss", 4)):
            for add in (None, "Trash", "Regular"):
                w, r, hp, f = run(n, cls, leg, kind, budget, add)
                print(f"| {kind} ({budget}) | {'+2 ' + add if add else 'as rolled'} | {w:.0%} | {r if r is not None else '-'} | "
                      f"{'-' if hp is None else f'{hp:.0%}'} | {f:.2f} |", flush=True)
