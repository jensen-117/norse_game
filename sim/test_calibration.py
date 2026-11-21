"""Calibration play (Nov 20): the Lab's calibration rooms are the sweep's rooms, and calib_gap.py measures the gap
between a recorded fight and the AI on the same room."""
import json, random, unittest
import lab, sweep, calib_gap, replay
from engine import *
from composer import CALIB_SEED, CALIB_PLACES

def lab_fight(kind="fodder", budget=3, add="", n=4, classes=("Vasara", "Ullar", "Brennumar"), rounds=40):
    lab.set_seed(7)
    lab.make_party(json.dumps([dict(cls=c, level=50, kit=1, pouch=[]) for c in classes]))
    room = json.loads(lab.calib_room(kind, budget, add, n))
    st = json.loads(lab.start("party"))
    while st["phase"] != "over" and rounds:
        if st["awaiting"]: lab.autofill()
        st = json.loads(lab.commit()); rounds -= 1
    return room, json.loads(lab.record())

class CalibrationRooms(unittest.TestCase):
    def test_the_labs_room_is_the_sweeps(self):
        for kind, budget, add in (("fodder", 3, ""), ("elite", 4, "Trash"), ("boss", 4, "Regular")):
            for n in (1, 2, 3, 17):
                json.loads(lab.calib_room(kind, budget, add, n))
                mine = [(r, l, e["family"], e["rank"], e.get("job"), e["element"]) for r, l, e in lab.S["pack_spec"]["placed"]]
                theirs = sweep.room(random.Random(CALIB_SEED + n - 1), CALIB_PLACES[(n - 1) % 3], kind, ENEMY_LEVEL, budget, add or None)
                self.assertEqual([(u.cell, u.name.split(" ")[0]) for u in theirs],
                                 [((r, l), u.name.split(" ")[0]) for (r, l, *_), u in zip(mine, lab.spawn(lab.S["pack_spec"]["placed"], ENEMY_LEVEL))])
                self.assertEqual(lab.S["pack_spec"]["calib"], dict(kind=kind, budget=budget, add=add or None, room=n, where=CALIB_PLACES[(n - 1) % 3]))

    def test_a_rolled_pack_is_not_a_calibration_room(self):
        json.loads(lab.calib_room("fodder", 3, "", 1)); lab.roll_pack("Barrow", 6, "any", 50)
        self.assertNotIn("calib", lab.S["pack_spec"])

class TheGap(unittest.TestCase):
    def test_a_recorded_fight_against_the_ai(self):
        room, rec = lab_fight()
        self.assertEqual(rec["calib"]["room"], 4); self.assertEqual(rec["profile"], "new")
        b = replay.replay(rec); self.assertEqual((b.winner, b.round), (rec["winner"], rec["rounds"]))
        g = calib_gap.gap(rec, n=4)
        self.assertEqual(g["human"][:2], (rec["winner"], rec["rounds"]))
        self.assertTrue(0 <= g["ai_win"] <= 1); self.assertIn("fodder 3, room 4", g["label"])
        self.assertIn("| fodder 3, room 4", calib_gap.report([rec], n=4))                 # a played (not Auto) fight

if __name__ == "__main__": unittest.main()
