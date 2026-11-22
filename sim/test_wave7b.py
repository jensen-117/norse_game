"""Wave 7, phase B (Nov 21, Joseph): the Halv is a kit pick that takes a free slot and never bumps an established move;
Merknyta is Late (two knots take longer); Nimble is called Evasive."""
import json, random, unittest
from engine import *
import lab

class TheHalvIsAPick(unittest.TestCase):
    def test_only_in_a_free_slot(self):
        for cls in KITS:
            for leg in KITS[cls]:
                has = any(a.get("basic") for a in build_hero(cls, leg).actions)
                self.assertEqual(has, len(KITS[cls][leg]) < KIT_SLOTS, (cls, leg))
        self.assertTrue(all(any(a.get("basic") for a in build_hero(c, 1).actions) for c in KITS))        # every leg 1
        self.assertFalse(any(any(a.get("basic") for a in build_hero(c, 3).actions) for c in KITS))       # no leg 3

    def test_the_menu_has_no_halv_slot_then(self):
        v = build_hero("Vasara", 3); b = Battle([v], [spawn_dummy()], random.Random(1), profile="new"); b.begin(control="party")
        o = b.options(v.uid)
        self.assertIsNone(o["halv"]); self.assertEqual(len(o["moves"]), 4)

    def test_autofill_guards_without_a_halv(self):
        lab.set_seed(1)
        lab.make_party(json.dumps([dict(cls=c, level=50, kit=3) for c in ("Dagskald", "Skurmar", "Vasara")]))
        lab.calib_room("elite", 4, "", 1); lab.start("party")
        out = json.loads(lab.autofill())
        self.assertTrue(out); self.assertTrue(all(o["key"] == "guard" for o in out), out)

    def test_ai_fights_without_one(self):
        from composer import shaped_room, catalog, spawn, CALIB_PLACES
        for s in range(4):
            party = [build_hero(c, 3) for c in ("Vasara", "Ullar", "Brennumar")]
            foes = spawn(shaped_room(random.Random(s), catalog(), CALIB_PLACES[s % 3], "elite", 4), ENEMY_LEVEL)
            self.assertIn(Battle(party, foes, random.Random(s), profile="new").fight(), ("party", "enemy"))

class Merknyta(unittest.TestCase):
    def test_late_at_six(self):
        m, k = compile_verb("Knyta", tier="Mer"), compile_verb("Knyta")
        self.assertEqual((m["name"], m["price"], m.get("group")), ("Merknyta", 6, -1)); self.assertIn("Late", m["keywords"])
        self.assertEqual(k.get("group", 0), 0); self.assertNotIn("Late", k["keywords"])

class Evasive(unittest.TestCase):
    def test_the_name(self):
        self.assertEqual(STAT_NAMES["EVA"], ("Marked", "Evasive"))
        u = build_hero("Vasara"); u.stages["EVA"] = 3; self.assertEqual(u.counter_name("EVA"), "Evasive 3")
        self.assertEqual(COUNTER_OF["Evasive"], ("EVA", 1))

def spawn_dummy():
    from test_wave4a import dummy
    return dummy()

if __name__ == "__main__":
    unittest.main()
