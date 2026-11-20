"""The board (combat_spec Parts 5-7): python3 -m unittest test_board -v"""
import random, unittest
import engine
from engine import *
from run_spirits import hire
from composer import catalog, gate, compose, place, spawn, roll_biome

def pack():
    f = [spawn_mogel("Mogel", "Eld", 30), spawn_spirit("Ande", "Vatn", 30)]
    f[0].cell, f[1].cell = ("front", 0), ("rear", 0)
    return f
def hero(cls, rng):
    while True:
        h = hire(30, rng)
        for u in h:
            if u.cls == cls: return u
def basic(u): return next(a for a in u.actions if a["kind"] == "damage" and a["element"] in MARTIAL and not a["all"])

class Board(unittest.TestCase):
    def setUp(self): engine.USE_BOARD = True; self.rng = random.Random(2)

    def battle(self, heroes, foes):
        return Battle(heroes, foes, self.rng)

    def test_melee_protection_and_exposure(self):
        h = hero("Hersir", self.rng); foes = pack(); b = self.battle([h], foes); h.cell = ("front", 0)
        mog, ande = foes
        self.assertEqual(b.reach_mult(h, basic(h), mog), 1.0)
        self.assertIsNone(b.reach_mult(h, basic(h), ande), "the Rear is protected from melee")
        mog.hp = 0
        self.assertEqual(b.reach_mult(h, basic(h), ande), 1.0, "an empty Front exposes the Rear")

    def test_melee_from_rear_is_half(self):
        h = hero("Berserker", self.rng); foes = pack(); b = self.battle([h], foes); h.cell = ("rear", 0)
        self.assertEqual(b.reach_mult(h, basic(h), foes[0]), REAR_MELEE_MULT)

    def test_medium_range(self):
        # Nov 10: range is the weapon's. A spear (Medium) reaches the Rear from the Front, and the Front from the Rear.
        h = hero("Nalarbani", self.rng); foes = pack(); b = self.battle([h], foes)
        spear = dict(basic(h), reach=RANGES["Medium"])
        h.cell = ("front", 0); self.assertEqual(b.reach_mult(h, spear, foes[1]), 1.0)
        h.cell = ("rear", 0)
        self.assertIsNone(b.reach_mult(h, spear, foes[1]))
        self.assertEqual(b.reach_mult(h, spear, foes[0]), 1.0)

    def test_a_stiletto_is_short(self):
        h = hero("Nalarbani", self.rng); foes = pack(); b = self.battle([h], foes); h.cell = ("front", 0)
        self.assertIsNone(b.reach_mult(h, basic(h), foes[1]), "a knife doesn't reach past the Front")

    def test_bows_and_spells_reach_anywhere(self):
        u = hero("Ullar", self.rng); c = hero("Brennumar", self.rng); foes = pack(); b = self.battle([u, c], foes)
        u.cell, c.cell = ("rear", 0), ("rear", 1)
        volley = next(a for a in u.actions if a["name"] == "Flokskott")
        spell = next(a for a in c.actions if a["kind"] == "damage")
        self.assertEqual(b.reach_mult(u, volley, foes[1]), 1.0)
        self.assertEqual(b.reach_mult(c, spell, foes[1]), 1.0)

    def test_formation(self):
        rng = random.Random(5)
        for _ in range(300):
            party = hire(30, rng); b = Battle(party, pack(), rng)
            cells = [u.cell for u in party]
            self.assertEqual(len(set(cells)), 3)
            self.assertTrue(any(c[0] == "front" for c in cells))
            for u in party:
                if CLASSES[u.cls]["kind"] == "martial" and sum(c[0] == "front" for c in cells) < 3:
                    self.assertEqual(u.cell[0], "front")

    def test_advance_when_front_empties(self):
        h = hero("Hersir", self.rng); c = hero("Brennumar", self.rng)
        foes = pack(); b = self.battle([h, c], foes); h.cell, c.cell = ("rear", 0), ("rear", 1)
        self.assertEqual(b.advancers([h, c]), {h}, "the melee hero steps up; the caster stays")

    def test_mogel_keeps_its_cell(self):
        foes = pack(); h = hero("Hersir", self.rng); b = self.battle([h], foes)
        m = foes[0]; m.hp = 0; b.downed(m)
        self.assertTrue(m.alive); self.assertEqual(m.cell, ("front", 0)); self.assertEqual(m.mogel_rank, "Litel")

    def test_no_illegal_hits_across_many_fights(self):
        rng = random.Random(9); cat = catalog(); bad = fiz = 0
        for _ in range(300):
            foes = spawn(place(compose(rng, gate(cat, art_only=True, **roll_biome(rng)[1]))), 30)
            b = Battle(hire(30, rng), foes, rng); b.fight()
            bad += sum(u.stats["illegal"] for u in b.units)
        self.assertEqual(bad, 0)

if __name__ == "__main__":
    unittest.main()

class Shapes(unittest.TestCase):
    def test_flokskott_hits_the_whole_row_from_anywhere(self):
        engine.USE_BOARD = True; rng = random.Random(4)
        u = hero("Ullar", rng); u.cell = ("rear", 0)
        foes = [spawn_mogel("Halv", e, 30) for e in ("Eld", "Vatn", "Jord", "Gro")]
        for i, f in enumerate(foes): f.cell = ("front", i) if i < 3 else ("rear", 0)
        b = Battle([u], foes, rng)
        flok = next(a for a in u.actions if a["name"] == "Flokskott")
        self.assertEqual(set(b.shape_targets(u, flok, foes[3])), {foes[3]}, "a row of one in the Rear, reached from the Rear")
        self.assertEqual(set(b.shape_targets(u, flok, foes[0])), set(foes[:3]))

class AdvanceInFights(unittest.TestCase):
    def test_rear_melee_steps_up_when_front_falls(self):
        engine.USE_BOARD = True; rng = random.Random(3); mv = 0
        for _ in range(100):
            foes = [spawn_mogel("Halv", e, 10) for e in ["Eld", "Vatn", "Jord", "Gro", "Sol", "Hrim"]]
            b = Battle(hire(10, rng), foes, rng); b.fight(); mv += sum(u.stats["moves"] for u in b.units)
        self.assertGreater(mv, 0)
