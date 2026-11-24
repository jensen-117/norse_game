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

class StatsPersist(unittest.TestCase):
    """Wave B (Nov 24, D2): stats last the fight. Joseph's buffer example, now: Mighty 2 stays Mighty 2."""
    def test_the_buffer_and_the_vasara(self):
        v = hero("Vasara", "Krosh"); d = hero("Dagskald", "Aukraft"); e = dummy()
        b = fight([v, d], [e])
        go = lambda: orders(b, {d.uid: (key(d, "Aukraft"), v.uid), v.uid: ("guard", None)})
        go(); go(); self.assertEqual(v.stage("ATK"), 2)
        for _ in range(3): orders(b, {d.uid: ("guard", None), v.uid: ("guard", None)})
        self.assertEqual(v.stage("ATK"), 2)                  # nobody moved it, and it stays

    def test_opposites_cancel(self):
        v = hero("Vasara", "Krosh"); e = dummy(); b = fight([v], [e])
        v.stages["ATK"] = -2; b.push(v, "ATK", 1); b.end_round()
        self.assertEqual(v.stage("ATK"), -1)

    def test_one_offense_one_defense(self):
        v = hero("Vasara", "Krosh"); e = dummy(); b = fight([v], [e])
        b.push(v, "MAT", 1); self.assertEqual((v.stage("ATK"), v.stage("MAT")), (1, 1))     # Mighty covers spells
        b.push(v, "MDF", -2); self.assertEqual((v.stage("DEF"), v.counter_name("MDF")), (-2, "Sundered 2"))

    def test_a_new_fight_starts_clean(self):
        v = hero("Vasara", "Krosh"); b = fight([v], [dummy()]); b.push(v, "ATK", 2)
        fight([v], [dummy()]); self.assertEqual(v.stage("ATK"), 0)

    def test_the_old_game_keeps_its_staircase(self):
        v = hero("Vasara", "Krosh"); e = dummy(); b = Battle([v], [e], random.Random(1), profile="legacy")
        b.push(v, "ATK", 2); b.end_round(); b.end_round(); self.assertEqual(v.stages["ATK"], 1)

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

    def test_even_it_always_lands(self):                    # Nov 24, D1: no graze at even
        e, b = self.pin(0, 0.0); self.assertIn("Pinned", e.status)

    def test_behind_a_graze_shrugs_it_off(self):            # Nov 24, D1: behind, grazes by the net; no whiffs
        e, b = self.pin(1, 0.0); self.assertNotIn("Pinned", e.status)
        self.assertFalse(evs(b, "whiff", unit=e.name))
        e, b = self.pin(1, 0.6); self.assertIn("Pinned", e.status)                    # half graze at -1: 0.6 lands

    def test_a_rider_lands_on_every_clean_hit(self):
        u = hero("Ullar", ("Skott", dict(lonn=True))); e = dummy(); b = fight([u], [e]); b.rng = Rng(0.5)
        orders(b, {u.uid: (key(u, "Blotskott"), e.uid)})
        self.assertIn("Bleeding", e.status)

# ------------------------------------------------------------------ step 3: Late, one primitive
class LateIsOneRule(unittest.TestCase):
    def setUp(self):
        self.u = hero("Ullar", "Skott"); self.e = dummy(); self.b = ng(self.u, self.e)
        self.skott = next(a for a in self.u.actions if a["name"] == "Skott")

    def test_each_wearer_drops_a_move_to_late(self):
        for s in ("Reeling", "Chilled", "Feared"):
            self.u.status = {}
            self.b.apply_status(self.e, self.u, s, 1.0)
            self.assertEqual(self.b.group_of(self.u, self.skott), FEAR_GROUP, s)

    def test_heavy_and_last_stay_and_guard_is_spared(self):
        self.b.apply_status(self.e, self.u, "Reeling", 1.0)
        self.assertEqual(self.b.group_of(self.u, dict(self.skott, group=-2)), -2)        # Heavy stays Heavy
        self.assertEqual(self.b.group_of(self.u, dict(kind="defend")), PROTECT_GROUP)    # Guard still comes first

    def test_late_from_two_sources_is_just_late(self):
        self.b.apply_status(self.e, self.u, "Reeling", 1.0); self.b.apply_status(self.e, self.u, "Chilled", 1.0)
        self.assertEqual(self.b.group_of(self.u, self.skott), FEAR_GROUP)

    def test_pinned_and_chilled_no_longer_slow(self):
        self.b.apply_status(self.e, self.u, "Pinned", 1.0); self.b.apply_status(self.e, self.u, "Chilled", 1.0)
        self.assertEqual(self.u.stage("SPD"), 0)

    def test_reeling_is_rounds(self):
        self.b.apply_status(self.e, self.u, "Reeling", 1.0); self.b.apply_status(self.e, self.u, "Reeling", 1.0)
        self.assertEqual(self.u.status["Reeling"]["rounds"], 2)

class FrozenReplacesChilled(unittest.TestCase):
    def test_the_third_chill_freezes_and_thaws_clean(self):     # Nov 22: Chilled 1, Chilled 2, then Frozen
        u = hero("Ullar", "Skott"); e = dummy(); b = ng(u, e)
        b.apply_status(u, e, "Chilled", 1.0); b.apply_status(u, e, "Chilled", 1.0)
        self.assertEqual(e.status["Chilled"]["rounds"], 2); self.assertNotIn("Frozen", e.status)
        b.apply_status(u, e, "Chilled", 1.0)
        self.assertIn("Frozen", e.status); self.assertNotIn("Chilled", e.status)    # no freeze-lock after the thaw

    def test_a_boss_keeps_its_turns(self):
        u = hero("Ullar", "Skott"); e = dummy(); b = ng(u, e); e.rank = "Drott"   # a Boss by tier
        for _ in range(3): b.apply_status(u, e, "Chilled", 1.0)
        self.assertNotIn("Frozen", e.status); self.assertIn("Chilled", e.status)
        self.assertFalse(b.apply_status(u, e, "Stunned", 1.0)); self.assertFalse(b.apply_status(u, e, "Death", 1.0))
        self.assertTrue(b.apply_status(u, e, "Pinned", 1.0))                          # setup still works on bosses

    def test_the_old_game_still_slows(self):
        u = hero("Ullar", "Skott"); e = dummy(); b = Battle([u], [e], random.Random(1), profile="legacy")
        b.apply_status(e, u, "Pinned", 1.0); self.assertEqual(u.stage("SPD"), -1)

# ------------------------------------------------------------------ step 4: bundles
class Shorthand(unittest.TestCase):
    """Wave B (Nov 24, D4): a bundle lands its parts; each lives by its own rule."""
    def setUp(self):
        self.u = hero("Ullar", "Skott"); self.e = dummy(); self.b = ng(self.u, self.e)

    def land(self, s, n=1): return self.b.apply_status(self.u, self.e, s, 1.0, n)

    def test_feared_is_late_and_sundered(self):
        self.land("Feared", 2)
        self.assertNotIn("Feared", self.e.status); self.assertEqual(self.e.status["Reeling"]["rounds"], 2)
        self.assertEqual(self.e.stage("DEF"), -2)
        self.assertEqual(self.b.group_of(self.e, dict(kind="damage")), FEAR_GROUP)
        for _ in range(4): self.b.end_round()
        self.assertNotIn("Reeling", self.e.status); self.assertEqual(self.e.stage("DEF"), -2)   # the Late fades; the DEF stays

    def test_cursed_and_venom(self):
        self.land("Cursed"); self.assertEqual(self.e.stage("DEF"), -1); self.assertIn("Poisoned", self.e.status)
        self.land("Venom"); self.assertTrue(self.b.wears(self.e, "Bleeding"))
        self.assertEqual(self.e.status["Poisoned"]["rounds"], 2)       # one Poison, two landings: two rounds

class Holds(unittest.TestCase):
    """Wave B (Nov 24, D3): one rule. A hold blocks pushes that hurt, lets help land, and undoes its own change."""
    def setUp(self):
        self.u = hero("Ullar", "Skott"); self.e = dummy(); self.b = ng(self.u, self.e)

    def land(self, s, n=1): return self.b.apply_status(self.u, self.e, s, 1.0, n)

    def test_disarm_restores_honestly(self):                  # Joseph's worked cases
        for before, mid, after in ((-2, 0, -2), (3, 0, 3), (1, 6, 3)):
            e = dummy(); b = ng(self.u, e); e.stages["ATK"] = before
            b.apply_status(self.u, e, "Disarmed", 1.0); self.assertEqual(e.stage("ATK"), -3)
            self.assertFalse(b.push(e, "ATK", -1))               # no Feeble under it
            if mid: b.push(e, "ATK", 3); b.push(e, "ATK", 3)     # fights up to Mighty 3
            for _ in range(4): b.end_round()
            self.assertNotIn("ATK", e.held); self.assertEqual(e.stage("ATK"), after)

    def test_it_lasts_its_rounds_not_the_landing_one(self):
        self.land("Disarmed"); self.b.end_round(); self.b.end_round(); self.b.end_round()
        self.assertIn("ATK", self.e.held); self.b.end_round(); self.assertNotIn("ATK", self.e.held)

    def test_a_held_stat_takes_no_second_hold(self):
        self.assertTrue(self.land("Disarmed")); self.assertTrue(self.b.capped(self.e, "Disarmed"))
        self.assertFalse(self.land("Disarmed")); self.assertEqual(self.e.held["ATK"]["rounds"], 3)   # no refresh

    def test_steadfast_holds_the_guard_but_not_the_tempo(self):
        self.land("Steadfast", 2); self.land("Feared")
        self.assertEqual(self.e.stage("DEF"), 0)                 # the DEF part is blocked
        self.assertEqual(self.b.group_of(self.e, dict(kind="damage")), FEAR_GROUP)   # still Late
        self.assertFalse(self.b.unshoved(self.e))                # and it can be shoved now
        self.b.push(self.e, "DEF", 1); self.assertEqual(self.e.stage("DEF"), 1)    # help still lands

    def test_gyllenlykt_holds_evasive(self):
        d = hero("Dagskald", ("Lak", dict(lonn=True))); b = fight([d], [dummy()])
        orders(b, {d.uid: (key(d, "Gyllenlykt"), d.uid)})
        self.assertEqual(d.stage("EVA"), 3); self.assertIn("EVA", d.held)
        self.assertFalse(b.apply_status(b.enemies[0], d, "Marked", 1.0)); self.assertEqual(d.stage("EVA"), 3)

    def test_skolja_lifts_a_harmful_hold(self):
        d = hero("Dagskald", "Skolja"); v = hero("Vasara", "Krosh"); b = fight([d, v], [dummy()])
        v.stages["ATK"] = 1; b.apply_status(b.enemies[0], v, "Disarmed", 1.0)
        orders(b, {d.uid: (key(d, "Skolja"), v.uid), v.uid: ("guard", None)})
        self.assertNotIn("ATK", v.held); self.assertEqual(v.stage("ATK"), 1)

    def test_the_old_game_keeps_its_bundles(self):
        b = Battle([self.u], [self.e], random.Random(1), profile="legacy")
        b.apply_status(self.u, self.e, "Cursed", 1.0); self.assertIn("stats", self.e.status["Cursed"])    # the rolled pick

# ------------------------------------------------------------------ step 5: parents hit, children twist
class ParentsHitChildrenTwist(unittest.TestCase):
    def foes(self, *names):
        from composer import catalog, spawn
        return [u for e in catalog() for u in spawn([(0, 0, e)], ENEMY_LEVEL) if u.name in names]

    def test_a_child_attack_becomes_its_styng_form(self):
        f = self.foes("Hrimande")[0]; plain = {a["name"]: a for a in f.actions}
        b = ng(hero("Vasara", "Krosh"), f)
        a = next(x for x in f.actions if x["name"] == "Stynghrim")
        self.assertEqual((a["status"], a["rider_sure"]), ("Chilled", True))
        self.assertAlmostEqual(a["power"], plain["Hrim"]["power"] * STYNG_POWER)
        self.assertIn("Vatn", [x["name"] for x in f.actions])              # the parent still just hits
        b.new_game_enemy(f); self.assertEqual(sum(x["name"] == "Stynghrim" for x in f.actions), 1)   # idempotent

    def test_no_automatic_riders_and_the_twist_is_certain(self):
        f = self.foes("Hrimande")[0]; v = hero("Vasara", "Krosh"); b = ng(v, f); b.rng = Rng(0.5)
        hrim = next(x for x in f.actions if x["name"] == "Stynghrim")
        b.land(f, hrim, v, 1.0, v, False); self.assertIn("Chilled", v.status)              # a clean hit: certain
        vatn = next(x for x in f.actions if x["name"] == "Vatn"); v2 = hero("Ullar", "Skott"); b2 = ng(v2, f); b2.rng = Rng(0.5)
        blixt = dict(vatn, element="Blixt", name="Blixt")
        b2.land(f, blixt, v2, 1.0, v2, False); self.assertNotIn("Stunned", v2.status)     # Blixt's stun is Stelblixt's

    def test_the_old_game_keeps_its_spells(self):
        f = self.foes("Hrimande")[0]; Battle([hero("Vasara", "Krosh")], [f], random.Random(1), profile="legacy")
        self.assertIn("Hrim", [x["name"] for x in f.actions])

class AWaveChillsAPunchFreezes(unittest.TestCase):
    def test_an_all_chill_only_stacks(self):
        u = hero("Ullar", "Skott"); e = dummy(); b = ng(u, e); wave = dict(kind="damage", all=True)
        for _ in range(4): b.apply_status(u, e, "Chilled", 1.0, 1, "Base", wave)
        self.assertNotIn("Frozen", e.status); self.assertEqual(e.status["Chilled"]["rounds"], STACK_CAP)
        b.apply_status(u, e, "Chilled", 1.0, 1, "Base", dict(kind="damage", all=False))
        self.assertIn("Frozen", e.status)

# ------------------------------------------------------------------ step 6: Skolja washes ailments; Lonnskolja lifts stats too
class Skolja(unittest.TestCase):
    def wash(self, lonn):
        d = hero("Dagskald", ("Skolja", dict(lonn=lonn))); v = hero("Vasara", "Krosh"); e = dummy(); b = fight([d, v], [e])
        for s in ("Poisoned", "Bleeding", "Pinned", "Cursed", "Feared"): b.apply_status(e, v, s, 1.0)
        v.status["Song"] = dict(rounds=UNTIL_USED, stacks=2, heal=10); v.stages["ATK"] = -2; v.stages["DEF"] = 1
        orders(b, {d.uid: (key(d, compile_verb("Skolja", lonn=lonn)["name"]), v.uid), v.uid: ("guard", None)})
        return v

    def test_skolja_washes_ailments_not_stats(self):
        v = self.wash(False)
        self.assertEqual(set(v.status), {"Song"})                    # the helpful stays
        self.assertEqual(v.stage("ATK"), -2)                         # Feeble 2 still there: Skolja washes ailments, not stats

    def test_lonnskolja_also_lifts_lowered_stats(self):
        v = self.wash(True)
        self.assertEqual(set(v.status), {"Song"})
        self.assertEqual(v.stages["ATK"], 0); self.assertGreaterEqual(v.stages["DEF"], 0)   # a raised stat is left alone

if __name__ == "__main__":
    unittest.main()
