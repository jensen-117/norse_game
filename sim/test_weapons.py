"""Range comes from the weapon (Nov 10). python3 -m unittest test_weapons -v"""
import random, unittest
from engine import *
from test_board import hero

def rng_of(u): return RANGE_NAME[u]

class Weapons(unittest.TestCase):
    def setUp(self): self.rng = random.Random(3)

    def test_every_martial_class_carries_a_weapon_of_its_damage_type(self):
        for k, c in CLASSES.items():
            if c["kind"] == "martial": self.assertEqual(WEAPONS[c["weapon"]][0], c["dmg"], k)

    def test_hero_ranges(self):
        want = {"Ullar": "Long", "Nalarbani": "Short", "Hersir": "Short", "Huskarl": "Short", "Berserker": "Short", "Vasara": "Short"}
        for cls, r in want.items():
            u = hero(cls, self.rng)
            for a in u.actions:
                if a["kind"] == "damage": self.assertEqual(rng_of(a["reach"]), r, (cls, a["name"]))

    def test_the_root_rule(self):
        self.assertEqual(root_range("Spett", "Stikk"), "Short")
        self.assertEqual(root_range("Spett", "Spear"), "Medium")
        self.assertEqual(root_range("Spett", "Bow"), "Short")      # an Ullar jabbing with an arrow
        self.assertEqual(root_range("Kross", "Bow"), "Short")      # ...or clubbing with the bow
        self.assertEqual(root_range("Kross", "Club"), "Short")
        self.assertEqual(root_range("Skott", "Bow"), "Long")

    def test_creature_weapons(self):
        def r(fam, job, move):
            row = rank_row(fam, job); u = spawn_family(fam, row["name"], 30, job=job)
            a = next(a for a in u.actions if a["name"] == move)
            return rng_of(a.get("reach") or REACH_BY_TYPE[a["element"]])
        self.assertEqual(r("Drattr", "Young", "Bite"), "Short")          # teeth
        self.assertEqual(r("Djur", "Stordjur", "Gore"), "Short")          # horns
        self.assertEqual(r("Drattr", "Spear", "Spett"), "Medium")
        self.assertEqual(r("Drattr", "Spear", "Halvskar"), "Short")       # a swipe with the spear: not a thrust
        self.assertEqual(r("Drattr", "Queen", "Trident"), "Medium")
        self.assertEqual(r("Bein", "Beinorv", "Arrow"), "Long")
        self.assertEqual(r("Bein", "Beinorv", "Volley"), "Long")

    def test_the_net_keeps_the_spear_after_the_swap(self):
        h = hero("Hersir", self.rng); h.cell = ("front", 0)
        n = spawn_family("Drattr", "Drattr", 30, job="Net"); n.cell = ("front", 0)
        b = Battle([h], [n], self.rng); b.transform(n, "Spear")
        self.assertEqual(rng_of(next(a for a in n.actions if a["name"] == "Skewer")["reach"]), "Medium")

    def test_the_hunts_bows_and_javelins(self):
        rows = [m for t in OSKOREI_TIERS.values() for u in t if isinstance(u, tuple) for m in u[5]]
        arrows = [family_move(m) for m in rows if m[0] == "strike" and m[2] in ("Arrow", "Rain of Spears")]
        self.assertTrue(arrows)
        for a in arrows: self.assertEqual(rng_of(a["reach"]), "Long")

    def test_the_card_names_the_range(self):
        u = hero("Ullar", self.rng)
        self.assertIn("Range Long", plain(next(a for a in u.actions if a["kind"] == "damage")))
        n = hero("Nalarbani", self.rng)
        self.assertIn("Range Short", plain(next(a for a in n.actions if a["kind"] == "damage")))

if __name__ == "__main__":
    unittest.main()
