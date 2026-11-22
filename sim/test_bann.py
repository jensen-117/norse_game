"""The Bann family (Nov 21, Joseph): Bann is the ban. Bannskott is Skott with its second designated rider, a shot that
may Silence; the pinned-prey finisher is Fallskott (was Banskott). Lonn names a rider by its word when a verb has more
than one."""
import unittest
from engine import *
from words import compile_verb
from test_wave4a import dummy, fight, orders, key, evs

class Bannskott(unittest.TestCase):
    def test_the_shot_that_silences(self):
        a, blot = compile_verb("Skott", lonn="Bann"), compile_verb("Skott", lonn=True)
        self.assertEqual((a["name"], a["price"], a["status"]), ("Bannskott", 32, "Silenced"))
        self.assertEqual((blot["name"], blot["status"]), ("Blotskott", "Bleeding"))
        self.assertEqual(a["power"], blot["power"])                       # the rider's 0.6, either rider
        self.assertEqual(compile_verb("Skott", tier="Mer", lonn="Bann")["name"], "Merbannskott")

    def test_a_capstone_made_with_blot_isnt_matched_by_bann(self):
        self.assertEqual(compile_verb("Skott", tier="Mer", manners=("Drif",), lonn=True)["name"], "Tusensplitter")
        with self.assertRaises(ValueError): compile_verb("Skott", tier="Mer", manners=("Drif",), lonn="Bann")

    def test_only_a_designated_rider(self):
        with self.assertRaises(ValueError): compile_verb("Krosh", lonn="Bann")

    def test_it_lands_in_a_fight(self):
        landed = 0
        for s in range(40):
            u = build_hero("Ullar", 1, kit=[("Skott", dict(lonn="Bann"))]); e = dummy(); b = fight([u], [e], seed=s)
            orders(b, {u.uid: (key(u, "Bannskott"), e.uid)})
            landed += any(x["status"] == "Silenced" for x in evs(b, "status"))
        self.assertGreater(landed, 0)

class Fallskott(unittest.TestCase):
    def test_the_finisher_is_renamed(self):
        self.assertIn("Fallskott", VERBS); self.assertNotIn("Banskott", VERBS)
        self.assertIn("Fallskott", [compile_verb(v, **p)["name"] for v, p in KITS["Ullar"][3]])

if __name__ == "__main__":
    unittest.main()
