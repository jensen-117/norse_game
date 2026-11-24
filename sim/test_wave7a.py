"""Wave 7, phase A: the roll (Nov 21, Joseph; classes.md Part 7d; refactor_plan Wave 7).

The attacker's ACC minus the target's EVA: ahead, a hit crits 1 in 3 and never grazes; behind, it whiffs 1 in 3 and
lands nothing; even, the plain roll. Speed is out of the roll; an exact tie in turn order goes to the party. Damage hits
only: a status move keeps its own roll. Old fights keep the old roll (the fingerprints cover that)."""
import random, unittest
from engine import *
from test_wave4a import hero, dummy, fight, orders, key, evs

class ZeroRng(random.Random):
    """Every roll comes up 0.0: the first outcome on the list (a graze, when behind)."""
    def random(self): return 0.0

def battle(*units):
    party = [u for u in units if u.side == "party"]; foes = [u for u in units if u.side == "enemy"]
    return Battle(party, foes, random.Random(1), profile="new")

class TheOdds(unittest.TestCase):
    """The ladder (Nov 24, Battle_Refactor_Current D1): ahead, crits 1/3, 2/3, all; behind, grazes 1/2, 3/4, all; even,
    no graze and the base crit. No whiffs."""
    def setUp(self):
        self.u = hero("Vasara", "Krosh"); self.e = dummy(); self.b = battle(self.u, self.e)
        self.krosh = next(a for a in self.u.actions if a["name"] == "Krosh")

    def odds(self): return self.b.odds(self.u, self.e, self.krosh)

    def test_even_never_grazes(self):
        w, g, c = self.odds(); self.assertEqual((w, g), (0.0, 0.0)); self.assertGreater(c, CRIT_BASE - 1e-9)

    def test_ahead_the_crit_ladder(self):
        for n, want in ((1, 1 / 3), (2, 2 / 3), (3, 1.0)):
            self.e.stages["EVA"] = -n; self.assertEqual(self.odds(), (0.0, 0.0, want))

    def test_behind_the_graze_ladder(self):
        base = self.odds()[2]
        for n, want in ((1, 0.5), (2, 0.75), (3, 1.0)):
            self.e.stages["EVA"] = n; w, g, c = self.odds()
            self.assertEqual((w, g), (0.0, want)); self.assertAlmostEqual(c, base * (1 - want))

    def test_the_net_is_clamped_to_three(self):
        self.u.stages["ACC"] = 3; self.e.stages["EVA"] = -3; self.assertEqual(self.odds()[2], 1.0)
        self.u.stages["ACC"] = -3; self.e.stages["EVA"] = 3; self.assertEqual(self.odds()[1], 1.0)

    def test_the_ai_sees_the_ladder(self):
        plain = self.b.expected_roll_mult(self.u, self.e, self.krosh)
        self.e.stages["EVA"] = 1
        self.assertLess(self.b.expected_roll_mult(self.u, self.e, self.krosh), plain)
        self.e.stages["EVA"] = 3; self.assertAlmostEqual(self.b.expected_roll_mult(self.u, self.e, self.krosh), GRAZE_MULT)

    def test_the_tug_of_war(self):
        self.u.stages["ACC"] = 1; self.e.stages["EVA"] = 1          # Keen on Evasive: even
        self.assertEqual(self.odds()[:2], (0.0, 0.0))
        self.u.stages["ACC"] = 1; self.e.stages["EVA"] = 3          # Keen 1 on Evasive 3: two behind
        self.assertEqual(self.odds()[1], 0.75)

    def test_speed_is_out_of_the_roll(self):
        self.u.stages["SPD"] = 3; self.e.stages["SPD"] = -3
        self.assertEqual(self.odds()[:2], (0.0, 0.0))

    def test_a_status_move_rolls_as_a_hit(self):            # Nov 22: the accuracy roll is the only gamble
        self.e.stages["EVA"] = 3
        self.assertEqual(self.b.odds(self.u, self.e, None)[:2], (0.0, 0.0))
        nagl = next(a for a in hero("Ullar", "Naglskott").actions if a["name"] == "Naglskott")
        self.assertEqual(self.b.odds(self.u, self.e, nagl)[1], 1.0)

    def test_a_sure_strike_never_grazes(self):
        s = hero("Skurmar", "Blixt"); e = dummy(); b = battle(s, e); s.knots = 2
        e.stages["EVA"] = 3
        self.assertEqual(b.odds(s, e, next(a for a in s.actions if a["name"] == "Blixt"))[:2], (0.0, 0.0))

class AGrazeIsAFloor(unittest.TestCase):
    """Behind, a hit grazes: half damage, no rider, no Bonus Round (D1). Guard denies the Bonus Round too (D5)."""
    def test_half_damage_no_rider(self):
        v = hero("Vasara", ("Krosh", dict(lonn=True))); e = dummy(); b = fight([v], [e])
        e.stages["EVA"] = 3; b.rng = ZeroRng()
        orders(b, {v.uid: (key(v, "Brakrosh"), e.uid)})
        self.assertFalse(evs(b, "whiff")); self.assertTrue(evs(b, "hit", src=v.name))
        self.assertLess(e.hp, e.maxhp); self.assertEqual(e.stage("DEF"), 0)        # no Sundered

    def weak_round(self, eva, guards):
        from words import compile_verb
        v = hero("Vasara", "Krosh")
        e = dummy(aff={"Crush": "weak"}, **({} if guards else dict(actions=[compile_verb("Krosh", tier="Halv")])))
        e.stages["EVA"] = eva; b = fight([v], [e]); b.rng = random.Random(3)
        for uid in b.awaiting(): b.submit(uid, key(v, "Krosh"), e.uid)
        b.commit(); return b.phase == "bonus"

    def test_a_weak_hit_earns_the_bonus_round(self): self.assertTrue(self.weak_round(0, False))
    def test_a_grazing_weak_hit_does_not(self): self.assertFalse(self.weak_round(3, False))
    def test_guard_denies_it(self): self.assertFalse(self.weak_round(0, True))

class NoForcedAdvance(unittest.TestCase):
    """D6 (Nov 24): an empty Front costs nobody their turn; the Rear is exposed, and stepping up is a choice."""
    def test_the_rear_keeps_its_turn(self):
        u = hero("Vasara", "Krosh"); e = dummy(); f = dummy(); b = fight([u], [e, f])
        e.cell, f.cell = ("rear", 0), ("rear", 1)
        self.assertEqual(b.advancers([e, f]) if not b.new_game else set(), set())
        b2 = Battle([hero("Vasara", "Krosh")], [dummy()], random.Random(1), events=True)
        b2.enemies[0].cell = ("rear", 0); b2.begin("party")
        self.assertFalse(any(d and d[0].get("name") == "Advance" for _, _, d in b2.remaining))

class NothingAffordableGuards(unittest.TestCase):
    """D7 (Nov 24, Joseph): a foe or hero with nothing it can pay for Guards, rather than losing the turn."""
    def test_guard(self):
        u = hero("Vasara", "Krosh"); e = dummy(actions=[]); b = battle(u, e)
        a, t = b.declare(e); self.assertEqual((a["kind"], t), ("defend", e))

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
