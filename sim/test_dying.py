"""Dying, Wounded, Dead; the Vakna ladder; items as moves; fixed unit ids: python3 -m unittest test_dying -v"""
import random, unittest
import engine
from engine import *
from test_board import hero
from test_grammar import step

def foe(hp=10_000):
    m = spawn_family("Draugr", "Draugr", 30); m.maxhp = m.hp = hp; m.cell = ("front", 0)
    m.actions = [act("defend", "Defend", target="self")]
    return m

class Dying(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(1)
        self.h, self.k = hero("Hersir", self.rng), hero("Dagskald", self.rng)
        self.e = foe()
        self.b = Battle([self.h, self.k], [self.e], self.rng, events=True)
        self.b.round = 1

    def fall(self, t):
        t.hp = 0; self.b.downed(t)

    def test_falling_leaves_five_breaths(self):
        self.fall(self.h)
        self.assertEqual((self.h.state, self.h.breaths), ("dying", HERO_BREATHS))
        self.assertFalse(self.h.alive)

    def test_a_breath_goes_each_round_but_not_the_one_you_fell_in(self):
        self.fall(self.h)
        self.b.tick_breaths(); self.assertEqual(self.h.breaths, HERO_BREATHS)
        self.b.round = 2; self.b.tick_breaths(); self.assertEqual(self.h.breaths, HERO_BREATHS - 1)

    def test_hits_take_breaths_and_the_last_one_kills(self):
        self.fall(self.h)
        strike = skill("Slash", "Old Sword", "Base"); strike["cost"] = 0
        for _ in range(HERO_BREATHS): self.b.resolve(self.e, strike, self.h, False)
        self.assertEqual(self.h.state, "dead")

    def test_the_enemy_ai_weighs_a_finishing_blow(self):
        self.fall(self.h); self.e.actions = [skill("Slash", "Old Sword", "Base")]
        opts = []
        a, t = self.b.declare(self.e)
        self.assertIn(t, (self.h, self.k))       # it may choose either: the fallen is on the menu
        self.assertEqual(self.b.reason(self.e, a, self.h)[0], "finish_fallen")

    def test_winning_stabilises_the_dying_wounded(self):
        self.fall(self.h); mx = self.h.maxhp
        self.e.hp = 0; self.b.fight()
        self.assertEqual(self.h.state, "up"); self.assertAlmostEqual(self.h.hp, 1)
        self.assertTrue(self.h.wounded); self.assertAlmostEqual(self.h.maxhp, mx * (1 - WOUNDED_CUT))

    def test_falling_while_wounded_is_death(self):
        self.h.wounded = True; self.fall(self.h)
        self.assertEqual(self.h.state, "dead")

class Vakna(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(2)
        self.h, self.k = hero("Hersir", self.rng), hero("Dagskald", self.rng)
        self.b = Battle([self.h, self.k], [foe()], self.rng, events=True); self.b.round = 1
        self.k.mp = self.k.maxmp = 999

    def test_halvakna_stabilises_the_dying(self):
        self.h.hp = 0; self.b.downed(self.h)
        self.b.resolve(self.k, vakna("Halv"), self.h, False)
        self.assertEqual(self.h.state, "up"); self.assertAlmostEqual(self.h.hp, 1); self.assertFalse(self.h.wounded)

    def test_vakna_adds_a_fifth(self):
        self.h.hp = 0; self.b.downed(self.h)
        self.b.resolve(self.k, vakna("Base"), self.h, False)
        self.assertAlmostEqual(self.h.hp, 1 + 0.2 * self.h.maxhp)

    def test_halvakna_cannot_reach_the_dead_but_mervakna_can(self):
        self.b.die(self.h, "test")
        self.b.resolve(self.k, vakna("Halv"), self.h, False); self.assertEqual(self.h.state, "dead")
        self.b.resolve(self.k, vakna("Mer"), self.h, False)
        self.assertEqual(self.h.state, "up"); self.assertTrue(self.h.wounded)

class Items(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(3)
        self.h = hero("Brennumar", self.rng); self.e = foe(500)
        self.b = Battle([self.h], [self.e], self.rng, events=True); self.b.round = 1

    def test_a_draught_heals_and_is_used_up(self):
        self.h.pouch = [["life", 1]]; self.h.hp = 1
        self.b.resolve(self.h, item_move("life"), self.h, False)
        self.assertAlmostEqual(self.h.hp, 1 + 0.5 * self.h.maxhp); self.assertEqual(self.h.pouch, [])

    def test_an_empty_pouch_does_nothing(self):
        self.h.hp = 1; self.b.resolve(self.h, item_move("life"), self.h, False); self.assertEqual(self.h.hp, 1)

    def test_a_firecracker_ignores_affinity(self):
        self.h.pouch = [["firecracker", 1]]; self.e.aff = {"Force": "absorb"}       # nothing absorbs Force
        self.b.eligible, self.b.barred = set(), set()
        self.b.resolve(self.h, item_move("firecracker"), self.e, False)
        self.assertLess(self.e.hp, 500)

    def test_a_caster_throws_an_axe_as_an_average_person(self):
        a = item_move("iron_axe")
        self.assertTrue(a["fixed"]); self.assertEqual(a["element"], "Slash")
        self.assertAlmostEqual(self.b.raw_damage(self.h, self.e, a),
                               self.b.raw_damage(hero("Hersir", self.rng), self.e, a), delta=1e-6 + 0.0)

    def test_a_smoke_pot_ends_the_fight(self):
        self.h.pouch = [["smoke_pot", 1]]
        self.b.resolve(self.h, item_move("smoke_pot"), self.h, False)
        self.assertTrue(self.b.over())

    def test_pocket_sand_lowers_acc(self):
        self.h.pouch = [["pocket_sand", 1]]
        self.b.resolve(self.h, item_move("pocket_sand"), self.e, False)
        self.assertEqual(self.e.stages["ACC"], -1)

class Ids(unittest.TestCase):
    def test_a_reforming_mogel_keeps_its_id(self):
        rng = random.Random(4)
        m = spawn_mogel("Mogel", "Eld", 30); m.cell = ("front", 0)
        b = Battle([hero("Hersir", rng)], [m], rng, events=True)
        uid = m.uid; m.hp = 0; b.downed(m)
        self.assertEqual(m.uid, uid)
        ev = b.events[-1]; self.assertEqual(ev["kind"], "reform"); self.assertEqual(ev["unit_id"], uid)

if __name__ == "__main__":
    unittest.main()
