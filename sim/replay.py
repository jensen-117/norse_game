"""Replay a fight the Fight Lab recorded: python3 replay.py record.json [--state ROUND]
Rebuilds the party, the pack and the dice from the record and feeds the same orders in."""
import json, random, sys
from engine import *
from composer import spawn
import lab

def rebuild(rec):
    lab.S["seed"] = rec["lab_seed"]; lab.S["party_spec"] = rec["party"]
    seed = rec["bseed"]
    if isinstance(seed, float):     # early records: a float seed was hashed by 32-bit Pyodide (31-bit float hash)
        from hash32 import hash_double
        seed = hash_double(seed, 31)
    party = lab._party()
    profile = rec.get("profile") or ("new" if all(getattr(u, "kit_leg", None) is not None for u in party) else "legacy")   # older records: the rule they ran under
    b = Battle(party, spawn([tuple(x) for x in rec["pack"]], rec["level"]), random.Random(seed), events=True, profile=profile)
    return b

def replay(rec, upto=None, on_round=None):
    if rec.get("engine") != lab.ENGINE: print(f"note: recorded on engine {rec.get('engine')}, this is {lab.ENGINE}")
    b = rebuild(rec)
    b.begin(control=None if rec["control"] == "auto" else "party")
    for orders in rec["orders"]:
        if b.phase == "over" or (upto and b.round >= upto): break
        if on_round: on_round(b)
        for uid, (key, t) in orders.items(): b.submit(uid, key, t)
        b.commit()
    return b

if __name__ == "__main__":
    rec = json.load(open(sys.argv[1]))
    b = replay(rec)
    print("winner", b.winner, "rounds", b.round, "| recorded:", rec["winner"], rec["rounds"])
    texts = [e["text"] for e in b.events if e.get("text") and e["kind"] != "round"]
    rec_texts = [l for l in rec["log"] if not l.startswith("-- Round") and not l.startswith("   [")]
    print("log matches:", texts[-len(rec_texts):] == rec_texts if rec_texts else "no log")
