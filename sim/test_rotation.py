"""Cover, Swap, and the rotation AI (combat_spec Parts 7-8): python3 -m unittest test_rotation -v"""
import random, unittest
import engine
from engine import *
from grammar import compile_word
from test_board import hero
from test_grammar import step

def mogel(cell, level=30):
    m = spawn_mogel("Mogel", "Eld", level); m.cell = cell; return m

class Cover(unittest.TestCase):
    def setUp(self): engine.USE_BOARD = engine.USE_ROTATION = True; self.rng = random.Random(6)

    def test_cover_takes_single_target_hits(self):
        h = hero("Hersir", self.rng); a, c = mogel(("front", 0)), mogel(("front", 1))
        b = Battle([h], [a, c], self.rng); h.cell = ("front", 0)
        b.resolve(c, act("cover", "Cover", target="ally"), a, False)
        self.assertIs(a.covered_by, c)
        b.eligible, b.barred = set(), set()
        hp_a, hp_c = a.hp, c.hp
        b.resolve(h, next(x for x in h.actions if x["kind"] == "damage"), a, False)
        self.assertEqual(a.hp, hp_a); self.assertLess(c.hp, hp_c)

    def test_cover_does_not_stop_shapes_or_all(self):
        u = hero("Ullar", self.rng); a, c = mogel(("front", 0)), mogel(("front", 1))
        b = Battle([u], [a, c], self.rng)
        b.resolve(c, act("cover", "Cover", target="ally"), a, False)
        b.eligible, b.barred = set(), set()
        hp_a = a.hp
        b.resolve(u, next(x for x in u.actions if x["name"] == "Flokskott"), a, False)
        self.assertLess(a.hp, hp_a, "a row hits everyone, covered or not")

    def test_cover_runs_into_the_allys_spot(self):
        """A coverer standing in the Rear still takes a melee hit aimed at a Front ally: reach is the ally's."""
        h = hero("Hersir", self.rng); a, c = mogel(("front", 0)), mogel(("rear", 0))
        b = Battle([h], [a, c], self.rng); h.cell = ("front", 0)
        b.resolve(c, act("cover", "Cover", target="ally"), a, False)
        b.eligible, b.barred = set(), set()
        b.resolve(h, next(x for x in h.actions if x["kind"] == "damage"), a, False)
        self.assertEqual(h.stats["illegal"], 0); self.assertLess(c.hp, c.maxhp)

class Swap(unittest.TestCase):
    def setUp(self): engine.USE_BOARD = engine.USE_ROTATION = True; self.rng = random.Random(7)

    def test_swap_trades_cells(self):
        a, c = mogel(("front", 0)), mogel(("rear", 1))
        b = Battle([hero("Hersir", self.rng)], [a, c], self.rng)
        b.resolve(c, act("move", "Swap", target="self", cell=a.cell), c, False)
        self.assertEqual((a.cell, c.cell), (("rear", 1), ("front", 0)))

    def test_move_never_empties_the_front(self):
        a, c = mogel(("front", 0)), mogel(("rear", 1))
        b = Battle([hero("Hersir", self.rng)], [a, c], self.rng)
        b.resolve(a, act("move", "Fall back", target="self", cell=("rear", 2)), a, False)
        self.assertEqual(a.cell, ("front", 0))

    def test_hurt_front_rotates_out(self):
        a, c = mogel(("front", 0)), mogel(("rear", 1))
        b = Battle([hero("Hersir", self.rng)], [a, c], self.rng)
        a.hp = a.maxhp * 0.15
        opts = b.board_options(c, 20 * level_factor(30))
        self.assertTrue(any(x[1]["name"] == "Swap" for x in opts))

    def test_one_rescue_per_hurt_ally(self):
        a, c, d = mogel(("front", 0)), mogel(("rear", 1)), mogel(("front", 1))
        b = Battle([hero("Hersir", self.rng)], [a, c, d], self.rng)
        a.hp = a.maxhp * 0.15; b.claimed = {a}
        for u in (c, d):
            self.assertFalse([x for x in b.board_options(u, 20 * level_factor(30)) if x[1].get("rescue") is a])

class AnswerTheBide(unittest.TestCase):
    def setUp(self): engine.USE_BOARD = engine.USE_ROTATION = True; self.rng = random.Random(8)

    def test_a_visible_bide_gets_an_answer(self):
        h = hero("Hersir", self.rng); a, c = mogel(("front", 0)), mogel(("front", 1))
        b = Battle([h], [a, c], self.rng); h.cell = ("front", 0)
        h.bide = (compile_word("Skar", "Jatte", manner="Bid"), a)
        self.assertGreater(b.bide_threat(a), 0)
        kinds = {x[1]["kind"] for x in b.board_options(a, 20 * level_factor(30))}
        self.assertIn("defend", kinds, "the target braces")
        self.assertTrue(any(x[1]["kind"] == "cover" and x[2] is a for x in b.board_options(c, 20 * level_factor(30))),
                        "a healthy ally offers to take it")

    def test_mark_bides_are_not_tracked(self):
        h = hero("Hersir", self.rng); a = mogel(("front", 0))
        b = Battle([h], [a], self.rng)
        h.bide = (compile_word("Skar", target="Mark", manner="Bid"), a)
        self.assertEqual(b.bide_threat(a), 0)

if __name__ == "__main__":
    unittest.main()
