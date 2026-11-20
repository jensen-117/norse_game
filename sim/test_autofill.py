"""Fight with missing orders: autofill Halv-strikes with spread targets, and the record replays exactly."""
import json, lab, replay

def run(seed, hab="Barrow", rounds=40):
    lab.set_seed(seed)
    lab.make_party(json.dumps([dict(cls="random", level=5, pouch=[]) for _ in range(3)]))
    lab.roll_pack(hab, 6, "any", 5)
    st = json.loads(lab.start("party")); fills = []
    while st["phase"] != "over" and rounds:
        if st["awaiting"]:
            reach = {uid: set((json.loads(lab.options(uid))["halv"] or {}).get("targets") or []) for uid in st["awaiting"]}
            f = json.loads(lab.autofill()); fills.append(f)
            assert {x["id"] for x in f} == set(st["awaiting"]), "every unordered hero got an order"
            before = []
            for x in f:      # a repeat only when this hero could reach nothing that hadn't been picked
                if x["target"] in before: assert reach[x["id"]] <= set(before), f"spread broken: {f}"
                if x["target"] is not None: before.append(x["target"])
        st = json.loads(lab.commit()); rounds -= 1
    return json.loads(lab.record()), fills

def test_autofill_fights_and_replays():
    for seed in range(1, 9):
        rec, fills = run(seed, ["Barrow", "Biome: Mire", "Rapids"][seed % 3])
        assert fills and all(fills)
        assert any(x["key"] != "guard" for f in fills for x in f)
        b = replay.replay(rec)
        assert (b.winner, b.round) == (rec["winner"], rec["rounds"]), f"seed {seed}: replay mismatch"

if __name__ == "__main__":
    test_autofill_fights_and_replays(); print("ok")
