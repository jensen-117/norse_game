"""The word compiler and the manners (spellbook Part 2): python3 -m unittest test_grammar -v"""
import random, unittest
from collections import Counter
import engine
from engine import *
from grammar import compile_word, ev, assess, flurry_hits
from test_board import hero

def step(b):
    """One numbered round without the poison/status bookkeeping."""
    b.round += 1; b.eligible, b.barred = set(), set()
    b.run_phase([u for u in b.units if u.alive], bonus=False)

def dummy(level=30, hp=10_000):
    m = spawn_mogel("Mogel", "Eld", level); m.maxhp = m.hp = hp; m.actions = [act("defend", "Defend", target="self")]
    m.aff = {}; m.cell = ("front", 0)
    return m

class Words(unittest.TestCase):
    def test_names_and_english(self):
        self.assertEqual(compile_word("Krosh", "Mer", rider="Eitr")["name"], "Mereitrkrosh")
        self.assertEqual(compile_word("Skott", target="Flok")["english"], "Volley")
        self.assertEqual(compile_word("Krosh", "Mer", "Flok")["name"], "Flokmerkrosh")
        self.assertEqual(compile_word("Krosh", target="Flok")["name"], "Flokrosh")     # the seam rule
        self.assertEqual(compile_word("Skar", manner="Drif")["english"], "Flurry of Cuts")

    def test_numbers(self):
        j = compile_word("Krosh", manner="Jarf")
        self.assertEqual(j["cost"], 12); self.assertAlmostEqual(j["power"], 14.0)
        self.assertAlmostEqual(j["crit_bonus"], 0.20); self.assertEqual(j["crit_mult"], 3.0)
        self.assertEqual(compile_word("Skar", manner="Snar")["group"], 1)
        self.assertEqual(compile_word("Skar", "Halv", manner="Tung")["cost"], 4, "manners on Halv are never free")
        self.assertEqual(compile_word("Skar", "Halv", manner="Jarf")["cost"], 6)
        self.assertEqual(compile_word("Skar", "Halv")["cost"], 0)
        self.assertEqual(compile_word("Skar", manner="Tung")["group"], -2)
        e = compile_word("Krosh", rider="Eitr"); self.assertEqual(e["status"], "Poisoned"); self.assertAlmostEqual(e["power"], 14.0)
        self.assertEqual(compile_word("Eld", "Mer")["cost_type"], "MP")
        self.assertTrue(compile_word("Skott").get("reach") == "any")

    def test_expected_values_match_the_spellbook(self):
        plain, jarf = compile_word("Krosh"), compile_word("Krosh", manner="Jarf")
        self.assertAlmostEqual(ev(plain) / 20, 0.925, places=3)
        self.assertAlmostEqual(ev(jarf) / 20, 0.98, places=3)             # 0.7 x (0.1 + 0.55 + 0.75)
        self.assertAlmostEqual(flurry_hits(compile_word("Skar", manner="Drif")["flurry"]), 1.875)

    def test_assess_covers_every_word(self):
        rows = assess(); self.assertEqual(len(rows), 4 * 5 * 3 * 6 * 7)
        self.assertEqual(len({r["word"] for r in rows}), len(rows), "every word is distinct")

class Manners(unittest.TestCase):
    def setUp(self): engine.USE_BOARD = True; self.rng = random.Random(4)

    def test_flurry_distribution(self):
        b = Battle([hero("Hersir", self.rng)], [dummy()], self.rng)
        h, d = b.party[0], b.enemies[0]
        d.stages["EVA"] = 0; h.stages["ACC"] = 0
        f = compile_word("Skar", manner="Drif")["flurry"]
        net = b.net_stage(h, d)
        n = Counter(b.flurry_count(h, d, f) for _ in range(20000))
        p = 0.5 + 0.1 * net
        self.assertAlmostEqual(n[1] / 20000, 1 - p, delta=0.02)
        self.assertEqual(max(n), 4); self.assertEqual(min(n), 1)

    def test_jarf_crits_more_and_harder(self):
        b = Battle([hero("Berserker", self.rng)], [dummy()], self.rng); h, d = b.party[0], b.enemies[0]
        j, p = compile_word("Krosh", manner="Jarf"), compile_word("Krosh")
        crits = sum(b.roll(h, d, j) == "crit" for _ in range(20000)) / 20000
        base = sum(b.roll(h, d, p) == "crit" for _ in range(20000)) / 20000
        self.assertAlmostEqual(crits - base, 0.20, delta=0.02)
        self.assertGreater(b.expected_roll_mult(h, d, j), b.expected_roll_mult(h, d, p))

    def test_snar_goes_first_tung_goes_last(self):
        b = Battle([hero("Hersir", self.rng)], [dummy()], self.rng); h = b.party[0]
        self.assertEqual(b.group_of(h, compile_word("Skar", manner="Snar")), 1)
        self.assertEqual(b.group_of(h, compile_word("Skar", manner="Tung")), -2)

    def test_bide_winds_up_then_fires_next_round(self):
        h = hero("Ullar", self.rng); d = dummy()
        h.actions = [compile_word("Skott", manner="Bid")]
        b = Battle([h], [d], self.rng)
        step(b)
        self.assertEqual(d.hp, d.maxhp, "nothing lands on the wind-up round")
        self.assertIsNotNone(h.bide)
        step(b)
        self.assertLess(d.hp, d.maxhp, "the bided shot fires next round")
        self.assertEqual(h.stats["actions"], 2, "wind-up, then the release in place of round 2's action")

    def test_bide_is_lost_to_stun(self):
        h = hero("Ullar", self.rng); d = dummy()
        h.actions = [compile_word("Skott", manner="Bid")]
        b = Battle([h], [d], self.rng)
        step(b); h.status["Frozen"] = dict(rounds=5)
        step(b)
        self.assertEqual(h.stats["bides_lost"], 1); self.assertEqual(d.hp, d.maxhp)

    def test_flurry_carries_into_a_reformed_mogel(self):
        h = hero("Hersir", self.rng); m = spawn_mogel("Mogel", "Eld", 30); m.cell = ("front", 0)
        h.actions = [compile_word("Skar", "Jatte", manner="Drif")]
        b = Battle([h], [m], self.rng)
        m.hp = 1
        b.flurry(h, h.actions[0], m, 4, bonus=False)
        self.assertGreaterEqual(m.reforms, 1, "the first hit pops it")
        self.assertLess(m.hp, m.maxhp * MOGEL_REFORM_HP, "later hits land on the re-formed body")

    def test_enemies_shout_plain_english(self):
        b = Battle([hero("Ullar", self.rng)], [dummy()], self.rng)
        v = compile_word("Skott", target="Flok")
        self.assertEqual(b.shown(b.party[0], v), "Flokskott")
        self.assertEqual(b.shown(b.enemies[0], v), '"Volley!"')

if __name__ == "__main__":
    unittest.main()
