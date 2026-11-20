"""The new grammar (refactor_plan Wave 2b): class verbs grown by parts, the cap, capstones, costs as shares, keywords."""
import random, unittest
from engine import *

SPELLED = {   # the kits as classes.md and the Nov 20 kit list spell them
    "Vasara":    {1: "Krosh Egga", 2: "Krosh Egga Brakrosh Lya", 3: "Snarbrakrosh Lonnegga Lya Hevn"},
    "Ullar":     {1: "Skott Naglskott", 2: "Blotskott Naglskott Peka", 3: "Merblotskott Styngnaglskott Lonnpeka Banskott"},
    "Brennumar": {1: "Eld Reyk", 2: "Eld Reyk Sveda Alleld", 3: "Mereld Alleld Lonnsveda Djupanda"},
    "Dagskald":  {1: "Lak Sol", 2: "Lak Sol Kvad", 3: "Lonnlak Sol Merkvad Allaukraft"},
    "Skurmar":   {1: "Blast Knyta", 2: "Blast Knyta Kuling Blixt", 3: "Blast Merknyta Storm Lonnblixt"},
}

class TestKits(unittest.TestCase):
    def test_every_kit_compiles_to_its_spelling(self):
        for cls, legs in SPELLED.items():
            for leg, names in legs.items():
                self.assertEqual(" ".join(a["name"] for a in compile_kit(cls, leg)), names, f"{cls} leg {leg}")

    def test_kit_classes(self):
        for cls in KITS:
            for leg in KITS[cls]:
                for verb, _ in KITS[cls][leg]: self.assertIn(VERBS[verb]["cls"], (cls, None))

class TestParts(unittest.TestCase):
    def test_lonn_names(self):
        self.assertEqual(compile_verb("Krosh", lonn=True)["name"], "Brakrosh")     # Sundered spoken Brak on Krosh...
        self.assertEqual(compile_verb("Peka", lonn=True)["name"], "Lonnpeka")      # ...and Lonn on Peka
        self.assertEqual(compile_verb("Skott", lonn=True)["status"], "Bleeding")
        self.assertEqual(compile_verb("Sveda", lonn=True)["also_status"], "Feeble")
        self.assertEqual(compile_verb("Aukraft", lonn=True)["also"], [("DEF", 1)])
        self.assertTrue(compile_verb("Lak", lonn=True)["cleanse_one"])

    def test_illegal_parts(self):
        with self.assertRaises(ValueError): compile_verb("Eld", styng=True)       # no Styngeld: Eld is the damage
        with self.assertRaises(ValueError): compile_verb("Blast", lonn=True)      # no designated rider

    def test_cap_and_capstones(self):
        self.assertEqual(compile_verb("Skott", tier="Mer", lonn=True)["name"], "Merblotskott")
        self.assertEqual(compile_verb("Skott", target="Flok", lonn=True)["name"], "Flokblotskott")
        self.assertEqual(compile_verb("Skott", tier="Mer", manners=("Drif",), lonn=True)["name"], "Tusensplitter")
        self.assertEqual(compile_verb("Skott", tier="Mer", target="All", lonn=True)["name"], "Pilskur")
        self.assertEqual(compile_verb("Sveda", tier="Mer", target="All", styng=True, lonn=True)["name"], "Skogsbrand")
        with self.assertRaises(OverCap): compile_verb("Skott", tier="Mer", target="Flok", lonn=True)

    def test_bynames(self):
        self.assertEqual(compile_verb("Naglskott", tier="Mer", styng=True)["name"], "Geirskott")
        self.assertEqual(compile_verb("Sol", lonn=True)["name"], "Blindasol")
        self.assertEqual(compile_verb("Egga", lonn=True)["name"], "Lonnegga")
        for cls in KITS:
            for leg in KITS[cls]:
                for a in compile_kit(cls, leg): self.assertLessEqual(len(a["name"]), BYNAME_LETTERS, a["name"])

    def test_tier_climbs_from_the_verb(self):
        self.assertEqual(compile_verb("Storm")["tier"], "Mer")
        self.assertEqual(compile_verb("Storm", tier="Mer")["tier"], "Jatte")
        self.assertEqual(compile_verb("Orkan", tier="Mer")["knots"], 3)           # Merorkan: still 3 knots, more MP
        self.assertGreater(compile_verb("Orkan", tier="Mer")["share"], compile_verb("Orkan")["share"])

class TestPrice(unittest.TestCase):
    def test_mp_ladder(self):
        self.assertAlmostEqual(compile_verb("Eld")["share"], 1 / 16)
        self.assertAlmostEqual(compile_verb("Eld", tier="Mer")["share"], 1 / 10)
        self.assertAlmostEqual(1 / compile_verb("Eld", tier="Jatte")["share"], 6.25, places=2)
        self.assertAlmostEqual(1 / compile_verb("Orkan")["share"], 3.9, places=1)
        self.assertEqual(compile_verb("Eld", tier="Halv")["share"], 0.0)              # Halv is free
        self.assertEqual(compile_verb("Djupanda")["share"], 0.0)

    def test_hp_ladder(self):
        self.assertAlmostEqual(compile_verb("Skott")["share"], 1 / 36)
        self.assertAlmostEqual(compile_verb("Skott", lonn=True)["share"], 1 / 24)
        self.assertAlmostEqual(compile_verb("Skott", tier="Mer", lonn=True)["share"], 1 / 16)
        self.assertEqual(compile_verb("Skott")["cost_type"], "HP")

    def test_priced_by_the_bar(self):
        u = birth("Brennumar", 10, random.Random(1)); u.maxmp = 80
        u.actions = compile_kit("Brennumar", 3); price_bars(u)
        self.assertEqual([a["cost"] for a in u.actions], [8, 8, 8, 0])           # 80/10 three times; Djupanda free

class TestKeywords(unittest.TestCase):
    def test_groups(self):
        self.assertEqual(compile_verb("Egga")["keywords"], ["First"])
        self.assertEqual(compile_verb("Krosh", manners=("Snar",))["keywords"], ["Swift"])
        self.assertEqual(compile_verb("Skrida")["keywords"], ["Swift"])
        for k in GROUP_KEYWORD.values(): self.assertIn(k, KEYWORDS)

    def test_a_meteor_lands_heavy(self):
        m = compile_verb("Eld", manners=("Bid", "Tung"))
        self.assertEqual(m["name"], "Bidtungeld")
        self.assertEqual((m.get("group"), m["release_group"]), (None, -2))
        self.assertEqual(m["keywords"], ["Heavy", "Patient"])
        rng = random.Random(1)
        party = [birth(c, 10, random.Random(i)) for i, c in enumerate(("Vasara", "Ullar", "Brennumar"))]
        b = Battle(party, family_encounter(10, rng, "Bein"), rng); b.begin()
        u = party[2]; u.bide = (dict(m, cost=0), b.enemies[0])
        b.plan_phase([x for x in b.units if x.alive], bonus=False)
        rel = next(d for k, x, d in b.remaining if x is u and d and d[0].get("_release"))
        self.assertEqual(b.group_of(u, rel[0]), -2)

if __name__ == "__main__": unittest.main()
