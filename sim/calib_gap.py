"""The human/AI gap (Nov 20): Joseph's recorded Lab fights, replayed natively, against the AI playing the same rooms.

    python3 calib_gap.py records [n_dice]       # a JSON list, JSON lines, or a folder of one record per .json file
                                                 # (the Lab's database as ArtifactData saves it: <out_dir>/fights/)

For each finished record: Joseph's result (replayed from his orders, so it's the engine's own account), the AI on the
same room with the same dice, and the AI over n_dice more dice seeds (default 30) on the same room. Calibration rooms
(the Lab's "Load calibration room") are the sweep's rooms by shape and number, so their AI rows line up with
sweep_report.md; other records are compared the same way, room by room. Prints markdown.
"""
import json, random, statistics, sys
from engine import *
from composer import spawn
import lab, replay

def load(path):
    import os
    if os.path.isdir(path):
        return sorted((json.load(open(os.path.join(path, f))) for f in os.listdir(path) if f.endswith(".json")),
                      key=lambda r: r.get("at") or "")
    text = open(path).read().strip()
    if text.startswith("["): return json.loads(text)
    return [json.loads(l) for l in text.splitlines() if l.strip()]

def cost(party):
    return 1 - sum(max(0, h.hp) for h in party) / sum(h.maxhp for h in party)

def ai_fight(rec, seed):
    lab.S["seed"] = rec["lab_seed"]; lab.S["party_spec"] = rec["party"]
    party = lab._party()
    b = Battle(party, spawn([tuple(x) for x in rec["pack"]], rec["level"]), random.Random(seed), profile=rec.get("profile") or "new")
    w = b.fight()
    return w, b.round, cost(party), sum(h.stats["downs"] for h in party)

def label(rec):
    c = rec.get("calib")
    if c: return f"{c['kind']} {c['budget']}{' +2 ' + c['add'] if c.get('add') else ''}, room {c['room']} ({c['where']})"
    return f"rolled pack, {len(rec['pack'])} foes"

def gap(rec, n=30):
    """One record: (label, party, human, ai_same, ai_many) or None if the fight didn't finish."""
    b = replay.replay(rec)
    if b.phase != "over": return None
    human = (b.winner, b.round, cost(b.party), sum(h.stats["downs"] for h in b.party))
    same = ai_fight(rec, rec["bseed"])
    many = [ai_fight(rec, rec["bseed"] * 1009 + k + 1) for k in range(n)]
    wins = [m for m in many if m[0] == "party"]
    return dict(label=label(rec), party="/".join(f"{p['cls']} {p.get('kit', 1)}" for p in rec["party"]), note=rec.get("note"),
                human=human, same=same, ai_win=len(wins) / n, ai_cost=statistics.mean(m[2] for m in wins) if wins else None,
                ai_falls=statistics.mean(m[3] for m in many))

def report(recs, n=30):
    old = [r for r in recs if r.get("engine") != lab.ENGINE]      # another engine's fight can't be replayed by this one
    recs = [r for r in recs if r.get("engine") == lab.ENGINE and r.get("control") != "auto"]   # Auto fights are the AI's own
    rows = [g for g in (gap(r, n) for r in recs) if g]
    pct = lambda x: "-" if x is None else f"{x:.0%}"
    out = [f"{len(rows)} finished fights (of {len(recs)} records on this engine, {lab.ENGINE}; {len(old)} from older engines "
           f"left out; Auto fights aren't counted); the AI over {n} dice each.", "",
           "| Room | Party (kit) | You | You: HP spent, falls | AI, same dice | AI wins | AI HP spent (wins) | AI falls | Note |",
           "|---|---|---|---|---|---|---|---|---|"]
    for g in rows:
        h, s = g["human"], g["same"]
        out.append(f"| {g['label']} | {g['party']} | {'won' if h[0] == 'party' else h[0]} in {h[1]} | {pct(h[2])}, {h[3]} | "
                   f"{'won' if s[0] == 'party' else s[0]} in {s[1]}, {pct(s[2])} | {g['ai_win']:.0%} | {pct(g['ai_cost'])} | "
                   f"{g['ai_falls']:.2f} | {g['note'] or ''} |")
    if rows:
        hw = sum(g["human"][0] == "party" for g in rows) / len(rows)
        hc = [g["human"][2] for g in rows if g["human"][0] == "party"]
        ac = [g["ai_cost"] for g in rows if g["ai_cost"] is not None]
        out += ["", f"**Overall:** you won {hw:.0%}, the AI {statistics.mean(g['ai_win'] for g in rows):.0%} on the same rooms; "
                    f"HP spent on wins: you {pct(statistics.mean(hc) if hc else None)}, the AI {pct(statistics.mean(ac) if ac else None)}."]
    return "\n".join(out)

if __name__ == "__main__":
    print(report(load(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 30))
