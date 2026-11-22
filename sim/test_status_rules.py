"""The status rules, settled Nov 22 with Joseph (beinar_pilot.md Part 1, sections 7 and 7b), pinned step by step.

Step 1, stats: a level from -3 to +3 on the curve x0.5, x0.6, x0.75, x1, x1.33, x1.67, x2; Base moves a stat 1
level, Mer 2, Jatte 3; at the end of a round, a stat nobody moved steps one toward 0 (the staircase); an opposite
pulling it back counts as moving it; a printed size wins over the tier."""
import random, unittest
from engine import *
from words import compile_verb
from test_wave4a import hero, dummy, fight, orders, key, evs

class TheCurve(unittest.TestCase):
    def test_true_mirrors_that_never_reach_zero(self):
        self.assertEqual([round(stage_mult(n), 2) for n in range(-3, 4)], [0.5, 0.6, 0.75, 1.0, 1.33, 1.67, 2.0])
        self.assertAlmostEqual(stage_mult(1) * stage_mult(-1), 1.0)       # one up and one down land back on x1

class TheTierSetsTheStep(unittest.TestCase):
    def test_base_one_mer_two_jatte_three(self):
        self.assertEqual((STACKS_BY_TIER["Base"], STACKS_BY_TIER["Mer"], STACKS_BY_TIER["Jatte"]), (1, 2, 3))

class TheStaircase(unittest.TestCase):
    """Joseph's worked example: a buffer keeps the Vasara at Mighty 2, turns away, and it steps down."""
    def test_the_buffer_and_the_vasara(self):
        v = hero("Vasara", "Krosh"); d = hero("Dagskald", "Aukraft"); e = dummy()
        b = fight([v, d], [e])
        go = lambda: orders(b, {d.uid: (key(d, "Aukraft"), v.uid), v.uid: ("guard", None)})
        go(); self.assertEqual(v.stage("ATK"), 1)            # R1: Mighty 1, held through the round's end (it was moved)
        go(); self.assertEqual(v.stage("ATK"), 2)            # R2: Mighty 2, no step down
        orders(b, {d.uid: ("guard", None), v.uid: ("guard", None)})
        self.assertEqual(v.stage("ATK"), 1)                  # R3: nobody moved it: Mighty 1
        orders(b, {d.uid: ("guard", None), v.uid: ("guard", None)})
        self.assertEqual(v.stage("ATK"), 0)                  # R4: gone

    def test_an_opposite_pull_counts_as_moving_it(self):
        v = hero("Vasara", "Krosh"); e = dummy(); b = fight([v], [e])
        v.stages["ATK"] = -2                                  # Feeble 2
        b.push(v, "ATK", 1); b.end_round()
        self.assertEqual(v.stage("ATK"), -1)                  # pulled to Feeble 1, and no second drop that round

class APrintedSizeWins(unittest.TestCase):
    def test_gyllenlykt_gives_evasive_3(self):
        d = hero("Dagskald", ("Lak", dict(lonn=True))); b = fight([d], [dummy()])
        self.assertTrue(b.new_game)
        orders(b, {d.uid: (key(d, "Gyllenlykt"), d.uid)})
        self.assertEqual(d.stage("EVA"), 3)

    def test_a_riders_size_isnt_multiplied_by_mer(self):
        name = compile_verb("Aukraft", tier="Mer", lonn=True)["name"]
        d = hero("Dagskald", ("Aukraft", dict(tier="Mer", lonn=True))); b = fight([d], [dummy()])
        orders(b, {d.uid: (key(d, name), d.uid)})
        self.assertEqual((d.stage("ATK"), d.stage("DEF")), (2, 1))   # its own stat by Mer (2); the rider's printed 1

# ------------------------------------------------------------------ step 2: ailments, flat, the number is rounds
class Rng(random.Random):
    """Every roll comes up the same: 0.0 is the first outcome (a whiff when there's one), 0.5 a plain hit."""
    def __init__(self, x): super().__init__(1); self.x = x
    def random(self): return self.x

def ng(*units):
    party = [u for u in units if u.side == "party"]; foes = [u for u in units if u.side == "enemy"]
    b = Battle(party, foes, random.Random(1), profile="new"); return b

class AilmentsAreRounds(unittest.TestCase):
    def setUp(self):
        self.u = hero("Ullar", "Skott"); self.e = dummy(); self.b = ng(self.u, self.e)

    def land(self, status, n=1): return self.b.apply_status(self.u, self.e, status, 1.0, n)

    def test_poison_1_lasts_the_round_after_it_lands(self):        # Joseph's: it won't drop until R2's end
        self.land("Poisoned"); self.assertEqual(self.e.status["Poisoned"]["rounds"], 1)
        self.b.end_round(); self.assertEqual(self.e.status["Poisoned"]["rounds"], 1)   # never the round it lands
        self.b.end_round(); self.assertNotIn("Poisoned", self.e.status)

    def test_adding_adds_and_holds_the_round(self):
        self.land("Poisoned"); self.b.end_round()
        self.land("Poisoned"); self.assertEqual(self.e.status["Poisoned"]["rounds"], 2)
        self.b.end_round(); self.assertEqual(self.e.status["Poisoned"]["rounds"], 2)    # added to this round: no drop
        self.b.end_round(); self.assertEqual(self.e.status["Poisoned"]["rounds"], 1)
        self.b.end_round(); self.assertNotIn("Poisoned", self.e.status)

    def test_the_cap_is_three(self):
        for _ in range(5): self.land("Bleeding")
        self.assertEqual(self.e.status["Bleeding"]["rounds"], STACK_CAP)
        self.assertTrue(self.b.capped(self.e, "Bleeding"))

    def test_refuse_is_gone(self):
        self.assertTrue(self.land("Silenced")); self.assertTrue(self.land("Silenced"))
        self.assertEqual(self.e.status["Silenced"]["rounds"], 2)

    def test_the_old_game_keeps_its_rules(self):
        b = Battle([self.u], [self.e], random.Random(1), profile="legacy")
        b.apply_status(self.u, self.e, "Poisoned", 1.0); self.assertEqual(self.e.status["Poisoned"]["rounds"], STATUSES["Poisoned"]["duration"])
        self.assertFalse(b.apply_status(self.u, self.e, "Poisoned", 1.0))             # refused, as before

class TheRollIsTheOnlyGamble(unittest.TestCase):
    def pin(self, eva, x):
        u = hero("Ullar", "Naglskott"); e = dummy(); b = fight([u], [e]); e.stages["EVA"] = eva; b.rng = Rng(x)
        orders(b, {u.uid: (key(u, "Naglskott"), e.uid)}); return e, b

    def test_a_clean_hit_lands_it_for_certain(self):
        e, b = self.pin(0, 0.5); self.assertIn("Pinned", e.status)

    def test_behind_it_can_whiff(self):
        e, b = self.pin(1, 0.0); self.assertNotIn("Pinned", e.status)
        self.assertTrue(evs(b, "whiff", unit=e.name))

    def test_a_graze_shrugs_it_off(self):
        e, b = self.pin(0, 0.0); self.assertNotIn("Pinned", e.status)                  # even: 0.0 is a graze

    def test_a_rider_lands_on_every_clean_hit(self):
        u = hero("Ullar", ("Skott", dict(lonn=True))); e = dummy(); b = fight([u], [e]); b.rng = Rng(0.5)
        orders(b, {u.uid: (key(u, "Blotskott"), e.uid)})
        self.assertIn("Bleeding", e.status)

if __name__ == "__main__":
    unittest.main()
