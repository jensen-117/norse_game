"""The new grammar (refactor_plan Wave 2b): class verbs grown by parts, the cap, capstones, costs as shares, keywords."""
import random, unittest
from engine import *

SPELLED = {   # the kits as classes.md and the Nov 20 kit list spell them
    "Vasara":    {1: "Krosh Egga", 2: "Krosh Egga Brakrosh Lya", 3: "Snarbrakrosh Rodegga Lya Hevn"},
    "Ullar":     {1: "Skott Naglskott", 2: "Blotskott Naglskott Peka", 3: "Merblotskott Genomskott Genomskoda Banskott"},
    "Brennumar": {1: "Eld Reyk", 2: "Eld Reyk Sveda Alleld", 3: "Mereld Alleld Lamsveda Djupanda"},
    "Dagskald":  {1: "Lak Sol", 2: "Lak Sol Kvad", 3: "Gyllenlykt Sol Merkvad Allaukraft"},
    "Skurmar":   {1: "Blast Knyta", 2: "Blast Knyta Kuling Blixt", 3: "Blast Merknyta Storm Stelblixt"},   # names: Nov 21
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
        self.assertEqual(compile_verb("Sveda", lonn=True)["name"], "Lamsveda")     # Feeble spoken Lam (Nov 21)...
        self.assertEqual(compile_verb("Blixt", lonn=True)["name"], "Stelblixt")    # ...and Stunned spoken Stel
        self.assertEqual(compile_verb("Skott", lonn=True)["status"], "Bleeding")
        self.assertEqual(compile_verb("Sveda", lonn=True)["also_status"], "Feeble")
        self.assertEqual(compile_verb("Aukraft", lonn=True)["also"], [("DEF", 1)])
        lak = compile_verb("Lak", lonn=True)                                      # Gyllenlykt (was Solak): Lak and Nimble 3 (Nov 21)
        self.assertEqual((lak["name"], lak["also"]), ("Gyllenlykt", [("EVA", 3)]))

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
    def test_root_names(self):     # Nov 21: a word for the verb and some parts; further parts attach to it
        self.assertEqual(compile_verb("Egga", lonn=True)["name"], "Rodegga")          # Blinded spoken Rod: seeing red
        self.assertEqual(compile_verb("Egga", styng=True)["name"], "Daska")            # the taunt that strikes
        self.assertEqual(compile_verb("Egga", styng=True, lonn=True)["name"], "Rodaska")   # the grammar folds the doubled d
        self.assertEqual(compile_verb("Peka", lonn=True)["name"], "Genomskoda")
        self.assertEqual(compile_verb("Naglskott", styng=True)["name"], "Genomskott")
        self.assertEqual(compile_verb("Egga", target="Flok", styng=True)["name"], "Flokdaska")
        self.assertEqual(compile_verb("Naglskott", manners=("Snar",), styng=True)["name"], "Snargenomskott")
        self.assertEqual(compile_verb("Naglskott", tier="Mer", styng=True)["name"], "Geirskott")   # an exact byname wins

    def test_long_names_need_a_byname(self):
        for cls in KITS:
            for leg in KITS[cls]:
                for a in compile_kit(cls, leg): self.assertLessEqual(len(a["name"]), BYNAME_LETTERS, a["name"])

    def test_tier_climbs_from_the_verb(self):
        self.assertEqual(compile_verb("Storm")["tier"], "Mer")
        self.assertEqual(compile_verb("Storm", tier="Mer")["tier"], "Jatte")
        self.assertEqual(compile_verb("Orkan", tier="Mer")["knots"], 3)           # Merorkan: still 3 knots, more MP
        self.assertGreater(compile_verb("Orkan", tier="Mer")["price"], compile_verb("Orkan")["price"])

class TestPrice(unittest.TestCase):     # the cost ladder (Nov 21, classes.md Part 7c): the rung x 2 a step
    def P(self, verb, **k): return compile_verb(verb, **k)["price"]

    def test_mp_ladder(self):
        self.assertEqual([self.P("Eld", tier="Halv"), self.P("Reyk"), self.P("Eld"), self.P("Eld", tier="Mer"),
                          self.P("Eld", target="Flok"), self.P("Eld", target="All")], [2, 3, 6, 12, 24, 48])
        self.assertEqual(self.P("Eld", tier="Jatte", source="find"), 24)
        self.assertEqual(self.P("Djupanda"), 0)
        self.assertEqual((self.P("Lak"), self.P("Lak", lonn=True), self.P("Kvad"), self.P("Kvad", tier="Mer")), (8, 16, 6, 12))
        self.assertEqual((self.P("Blixt"), self.P("Blixt", lonn=True), self.P("Knyta"), self.P("Knyta", tier="Mer")), (8, 16, 3, 6))

    def test_knots_pay_steps(self):     # All 3 steps, Mer 1, a follow-up 1; each knot spent pays one: all three 24
        self.assertEqual([self.P(v) for v in ("Kuling", "Storm", "Orkan")], [24, 24, 24])

    def test_hp_ladder(self):
        self.assertEqual([self.P("Skott", tier="Halv"), self.P("Naglskott"), self.P("Skott"), self.P("Skott", lonn=True),
                          self.P("Skott", tier="Mer", lonn=True), self.P("Skott", target="Flok", lonn=True)], [4, 8, 16, 32, 64, 128])
        self.assertEqual((self.P("Krosh", manners=("Snar",), lonn=True), self.P("Egga", lonn=True), self.P("Lya")), (64, 16, 8))
        self.assertEqual(compile_verb("Skott")["cost_type"], "HP")
        for v in VERBS:                                        # every rung is on the ladder
            if not VERBS[v].get("free"): self.assertIn(VERBS[v]["cost"], COST_LADDER, v)

    def test_priced_by_the_pool(self):     # the ladder number at the sheet's level; elsewhere, in proportion to the pool
        u = build_hero("Brennumar", 3)
        self.assertEqual([a["cost"] for a in u.actions], [2, 12, 48, 12, 0])
        low = build_hero("Brennumar", 3, level=25)
        self.assertEqual([a["cost"] for a in low.actions], [max(1, round(a["price"] * low.maxmp / 150)) if a["price"] else 0 for a in low.actions])
        self.assertLess(low.actions[2]["cost"], 48)

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
