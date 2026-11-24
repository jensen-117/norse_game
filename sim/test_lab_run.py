"""The Lab's run (Nov 24, Joseph): Trash, Regular, Elite, a camp, the Boss, in one place, carrying the party between
rooms; each room's record replays exactly (the party as it walked in rides in the record)."""
import json, unittest
import lab, replay

class ARun(unittest.TestCase):
    def play(self, n, add):
        lab.set_seed(1)
        lab.make_party(json.dumps([dict(cls="Vasara", level=50, kit=2, pouch=[["life", 1]]), dict(cls="Dagskald", level=50, kit=2),
                                   dict(cls="Skurmar", level=50, kit=2)]))
        lab.run_start(n, add, "Barrow"); recs = []
        for _ in range(8):
            st = lab._run_state()["run"]
            if st["over"]: break
            if st["stages"][st["stage"]] == "Camp": lab.run_camp(json.dumps([True, True, True])); continue
            lab.start("auto"); b = lab.S["battle"]
            while b.phase != "over": lab.commit()
            recs.append(json.loads(lab.record())); lab.run_after()
            if not lab._run_state()["run"]["over"]: lab.run_room()
        return lab._run_state()["run"], recs

    def test_rooms_carry_and_replay(self):
        run, recs = self.play(3, "Trash")
        self.assertTrue(run["over"]); self.assertTrue(recs)
        self.assertEqual(recs[0]["run"]["stage"], "Trash")
        for rec in recs:
            b = replay.replay(rec)
            self.assertEqual((b.winner, b.round), (rec["winner"], rec["rounds"]), rec["run"]["stage"])
        if len(recs) > 1:                                          # the second room starts where the first left them
            self.assertLess(sum(c["hp"] for c in recs[1]["carry"]), sum(c["maxhp"] for c in recs[1]["carry"]))

    def test_the_regular_room_keeps_its_own_adds(self):
        lab.set_seed(1); lab.make_party(json.dumps([dict(cls="Vasara", level=50, kit=1)]))
        r = json.loads(lab.run_start(1, "Trash", "Barrow")); n_trash = len(r["pack"])
        lab.S["run"]["stage"] = 1; r = json.loads(lab.run_room())
        self.assertEqual(r["room"], "Regular"); self.assertGreaterEqual(len(r["pack"]), 4)

if __name__ == "__main__":
    unittest.main()
