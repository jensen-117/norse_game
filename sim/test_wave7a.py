"""Wave 7, phase A: the roll (Nov 21, Joseph; classes.md Part 7d; refactor_plan Wave 7).

The attacker's ACC minus the target's EVA: ahead, a hit crits 1 in 3 and never grazes; behind, it whiffs 1 in 3 and
lands nothing; even, the plain roll. Speed is out of the roll; an exact tie in turn order goes to the party. Damage hits
only: a status move keeps its own roll. Old fights keep the old roll (the fingerprints cover that)."""
import random, unittest
from engine import *
from test_wave4a import hero, dummy, fight, orders, key, evs

class ZeroRng(random.Random):
    """Every roll comes up 0.0: the first outcome on the list (a whiff, when there's one)."""
    def random(self): return 0.0

def battle(*units):
    party = [u for u in units if u.side == "party"]; foes = [u for u in units if u.side == "enemy"]
    return Battle(party, foes, random.Random(1), profile="new")

class TheOdds(unittest.TestCase):
    def setUp(self):
        self.u = hero("Vasara", "Krosh"); self.e = dummy(); self.b = battle(self.u, self.e)
        self.krosh = next(a for a in self.u.actions if a["name"] == "Krosh")

    def odds(self): return self.b.odds(self.u, self.e, self.krosh)

    def test_even_is_the_plain_roll(self):
        w, g, c = self.odds(); self.assertEqual((w, g), (0.0, GRAZE_BASE)); self.assertGreater(c, 0)

    def test_a_nimble_target_whiffs_one_in_three(self):
        plain = self.b.expected_roll_mult(self.u, self.e, self.krosh)
        self.e.stages["EVA"] = 1
        self.assertAlmostEqual(self.odds()[0], 1 / 3)
        self.assertAlmostEqual(self.b.expected_roll_mult(self.u, self.e, self.krosh) / plain, 2 / 3)   # the AI sees two-thirds

    def test_a_marked_target_crits_one_in_three_and_never_grazes(self):
        self.e.stages["EVA"] = -1; self.assertEqual(self.odds(), (0.0, 0.0, AHEAD_CRIT))

    def test_stacks_are_duration_not_strength(self):
        self.e.stages["EVA"] = 3; self.assertAlmostEqual(self.odds()[0], 1 / 3)
        self.e.stages["EVA"] = -3; self.assertEqual(self.odds()[2], AHEAD_CRIT)

    def test_the_tug_of_war(self):
        self.u.stages["ACC"] = 1; self.e.stages["EVA"] = 1          # Keen on Nimble: even
        self.assertEqual(self.odds()[:2], (0.0, GRAZE_BASE))
        self.u.stages["ACC"] = -1; self.e.stages["EVA"] = -1        # Blinded on Marked: even
        self.assertEqual(self.odds()[:2], (0.0, GRAZE_BASE))
        self.u.stages["ACC"] = 1; self.e.stages["EVA"] = 3          # Keen 1 on Nimble 3: behind
        self.assertAlmostEqual(self.odds()[0], 1 / 3)

    def test_speed_is_out_of_the_roll(self):
        self.u.stages["SPD"] = 3; self.e.stages["SPD"] = -3
        self.assertEqual(self.odds()[:2], (0.0, GRAZE_BASE))

    def test_a_status_moves_roll_is_its_own(self):
        self.e.stages["EVA"] = 3
        self.assertEqual(self.b.odds(self.u, self.e, None)[0], 0.0)
        nagl = next(a for a in hero("Ullar", "Naglskott").actions if a["name"] == "Naglskott")
        self.assertEqual(self.b.odds(self.u, self.e, nagl)[0], 0.0)

    def test_a_sure_strike_never_misses(self):
        s = hero("Skurmar", "Blixt"); e = dummy(); b = battle(s, e); s.knots = 2
        e.stages["EVA"] = 3
        self.assertEqual(b.odds(s, e, next(a for a in s.actions if a["name"] == "Blixt"))[:2], (0.0, 0.0))

class AWhiffLandsNothing(unittest.TestCase):
    def test_no_damage_no_rider(self):
        v = hero("Vasara", ("Krosh", dict(lonn=True))); e = dummy(); b = fight([v], [e])
        e.stages["EVA"] = 3; b.rng = ZeroRng()
        orders(b, {v.uid: (key(v, "Brakrosh"), e.uid)})
        self.assertTrue(evs(b, "whiff", unit=e.name)); self.assertFalse(evs(b, "hit", src=v.name))
        self.assertEqual(e.hp, e.maxhp); self.assertEqual(e.stage("DEF"), 0)       # no Sundered
        self.assertEqual(v.stats["whiff"], 1)

    def test_the_page_hears_it(self):
        self.assertIn("whiff", open("../fight_lab/screen.js").read())

class Drif(unittest.TestCase):
    def test_the_chain_reads_no_stages(self):
        u = hero("Ullar", ("Skott", dict(manners=("Drif",)))); e = dummy(); b = battle(u, e)
        a = next(x for x in u.actions if x.get("flurry"))
        counts = []
        for acc in (0, 3, -3):
            u.stages["ACC"] = acc; b.rng = random.Random(5)
            counts.append([b.flurry_count(u, e, a["flurry"]) for _ in range(20)])
        self.assertEqual(counts[0], counts[1]); self.assertEqual(counts[0], counts[2])

class Ties(unittest.TestCase):
    def test_an_exact_tie_goes_to_the_party(self):
        v = hero("Vasara", "Krosh"); e = dummy(); b = battle(v, e)
        e.attrs = dict(v.attrs); e.body = dict(v.body)
        entries = [(0, e, (dict(v.actions[1]), None)), (0, v, (v.actions[1], None))]          # the same move: the same group
        self.assertEqual(v.speed(), e.speed())
        self.assertIs(b.order(entries)[0][1], v)

class OldFightsKeepTheOldRoll(unittest.TestCase):
    def test_legacy_reads_speed(self):
        u = birth("Ullar", 30, random.Random(1)); e = dummy(); b = Battle([u], [e], random.Random(1), profile="legacy")
        self.assertFalse(b.new_game); self.assertNotIn("whiff", [b.roll(u, e, u.actions[0]) for _ in range(200)])

if __name__ == "__main__":
    unittest.main()
