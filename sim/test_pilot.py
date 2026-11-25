"""The Beinar pilot, step 2 (Nov 24): the hand-made kits in the new game (the old game keeps the generated ones);
Pinned and Silenced as windows; D14's window on the hold path (Rally); foes raise their side to their want."""
import random, unittest
from engine import *
from test_wave4a import hero, dummy, orders, key

def bein(*ranks, element="Hrim", seed=1):
    party = [hero("Vasara", "Krosh"), hero("Dagskald", "Lak")]
    foes = [spawn_family("Bein", r, ENEMY_LEVEL, element=element) for r in ranks]
    b = Battle(party, foes, random.Random(seed), profile="new", events=True); b.begin("party")
    return b, party, foes

names = lambda u: [a["name"] for a in u.actions]

class Kits(unittest.TestCase):
    def test_the_new_game_carries_the_pilot_kits(self):
        b, _, (bryn, seidr, orv, forn) = bein("Beinbryn", "Beinseidr", "Beinorv", "Fornbein")
        self.assertEqual(names(bryn), ["Cover", "Hew", "Fortify"])
        self.assertEqual(names(seidr), ["Frost Bolt", "Silence", "Curse"])     # the twist keeps the foes' name
        self.assertEqual(names(orv)[:3], ["Arrow", "Pinning Shot", "Killing Shot"])
        self.assertIn(names(orv)[3], ("Barbed Arrow", "Poison Arrow"))          # the quiver
        self.assertEqual(names(forn), ["Cleaver", "Great Carve", "Rally", "Ogn"])
        self.assertTrue(bryn.guard); self.assertFalse(forn.guard)               # the commander doesn't Cover

    def test_the_old_game_keeps_the_generated_bein(self):
        u = spawn_family("Bein", "Beinbryn", ENEMY_LEVEL)
        self.assertEqual(names(u), ["Old Sword", "Shield Bash", "Aukskold"])
        b = Battle([hero("Vasara", "Krosh")], [u], random.Random(1), profile="legacy")
        self.assertEqual(names(u), ["Old Sword", "Shield Bash", "Aukskold"])

    def test_each_move_names_its_twin(self):
        _, _, (orv,) = bein("Storbeinorv")
        twins = {a["name"]: a.get("twin") for a in orv.actions}
        self.assertEqual(twins["Pinning Shot"], "Genomskott"); self.assertEqual(twins["Killing Shot"], "Merfangskott")

    def test_the_grave_bolt_is_plain_aska(self):
        _, _, (s,) = bein("Beinseidr", element="Aska")
        bolt = s.actions[0]; self.assertEqual(bolt["name"], "Grave Bolt"); self.assertIsNone(bolt["status"])

    def test_the_cleaver_winds_up_a_row(self):
        _, _, (f,) = bein("Fornbein")
        c = f.actions[0]; self.assertTrue(c["bide"]); self.assertEqual(c["shape"], "row")

    def test_killing_shot_pays_on_the_pinned(self):
        _, _, (orv,) = bein("Beinorv")
        ks = next(a for a in orv.actions if a["name"] == "Killing Shot")
        self.assertEqual((ks["pays_on"], ks["pays"]), ("Pinned", 1.5))

class Windows(unittest.TestCase):
    def test_pinning_shot_pins_for_two_and_cant_be_added_to(self):
        b, (v, d), (orv,) = bein("Beinorv")
        ps = next(a for a in orv.actions if a["name"] == "Pinning Shot")
        self.assertEqual(ps["stacks"], 2)
        self.assertTrue(b.apply_status(orv, v, "Pinned", 1.0, 2)); self.assertEqual(v.status["Pinned"]["rounds"], 2)
        self.assertFalse(b.apply_status(orv, v, "Pinned", 1.0, 2)); self.assertTrue(b.capped(v, "Pinned"))
        b.end_round(); b.end_round(); b.end_round(); self.assertNotIn("Pinned", v.status)   # landed, then 2, 1, gone

    def test_silence_is_a_window(self):
        b, (v, d), (s,) = bein("Beinseidr")
        self.assertTrue(b.apply_status(s, d, "Silenced", 1.0)); self.assertFalse(b.apply_status(s, d, "Silenced", 1.0))

class Rally(unittest.TestCase):
    def setUp(self):
        self.b, self.party, (self.f, self.o) = bein("Fornbein", "Beinorv")
        self.rally = next(a for a in self.f.actions if a["name"] == "Rally")

    def test_mighty_two_for_three_rounds_then_taken_back(self):
        b, f, o = self.b, self.f, self.o
        for x in (f, o): b.hold(f, x, "Rally", "ATK", None, 3, False, lock=False, push=2, rest=2)
        self.assertEqual(o.stage("ATK"), 2)
        for _ in range(4): b.end_round()
        self.assertEqual(o.stage("ATK"), 0); self.assertNotIn("ATK", o.held)

    def test_a_push_against_it_eats_into_it_first(self):
        b, f, o = self.b, self.f, self.o
        b.hold(f, o, "Rally", "ATK", None, 3, False, lock=False, push=2)
        self.assertTrue(b.push(o, "ATK", -1)); self.assertEqual(o.stage("ATK"), 1)   # Nedkraft lands: it isn't a lock
        b.release(o, "ATK"); self.assertEqual(o.stage("ATK"), 0)                     # takes back 1, never past 0

    def test_on_mighty_one_it_returns_to_one(self):
        b, f, o = self.b, self.f, self.o
        o.stages["ATK"] = 1
        b.hold(f, o, "Rally", "ATK", None, 3, False, lock=False, push=2)
        self.assertEqual(o.stage("ATK"), 3); b.release(o, "ATK"); self.assertEqual(o.stage("ATK"), 1)

    def test_no_second_rally_and_the_ai_waits_two_rounds(self):
        b, f, o = self.b, self.f, self.o
        for x in (f, o): b.hold(f, x, "Rally", "ATK", None, 3, False, lock=False, push=2, rest=2)
        self.assertFalse(b.hold(f, o, "Rally", "ATK", None, 3, False, lock=False, push=2))   # no second while it's up
        f.actions = [self.rally, dict(f.actions[1])]
        self.assertNotEqual(b.declare(f)[0]["name"], "Rally")
        b.round = 5
        for x in (f, o): b.release(x, "ATK")
        self.assertEqual(b.rested[("enemy", "Rally")], 5)
        b.round = 6; self.assertTrue(all(b.declare(f)[0]["name"] != "Rally" for _ in range(20)))   # resting
        b.round = 7; self.assertTrue(any(b.declare(f)[0]["name"] == "Rally" for _ in range(20)))

class Wants(unittest.TestCase):
    def test_a_foe_fortifies_to_its_want_then_strikes(self):
        b, _, (bryn,) = bein("Beinbryn")
        bryn.actions = [a for a in bryn.actions if a["name"] in ("Fortify", "Hew")]
        self.assertTrue(any(b.declare(bryn)[0]["name"] == "Fortify" for _ in range(20)))
        bryn.stages["DEF"] = 1
        self.assertTrue(all(b.declare(bryn)[0]["name"] == "Hew" for _ in range(20)))

    def test_fortify_is_aimed_at_itself(self):
        b, _, (bryn, orv) = bein("Beinbryn", "Beinorv")
        bryn.actions = [a for a in bryn.actions if a["name"] == "Fortify"]
        a, t = b.declare(bryn); self.assertIs(t, bryn)

if __name__ == "__main__":
    unittest.main()
