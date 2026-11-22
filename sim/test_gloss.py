"""The grammar library, L1 (Nov 21): the glossary covers the code, and the lexicon reads the code honestly."""
import unittest
import lab, lexicon
from gloss import GLOSS, KINDS
from data import KITS, VERBS
from words import compile_verb

class TheGlossaryCoversTheCode(unittest.TestCase):
    def test_no_gaps(self):
        missing, unclaimed = lexicon.gaps()
        self.assertEqual(missing, [], "atoms in the code with no glossary entry")
        self.assertEqual(unclaimed, [], "entries marked built that the code never says")

    def test_every_entry_is_well_formed(self):
        for k, e in GLOSS.items():
            self.assertIn(e["kind"], KINDS, k)
            self.assertIn(e["state"], ("built", "planned", "pocket"), k)
            self.assertTrue(e["means"], k)

    def test_old_language_words_have_a_reading(self):
        english = {"status", "counter", "keyword", "affinity", "action", "item"}
        for k, e in GLOSS.items():
            if e["kind"] in english or k in ("Slash", "Pierce", "Crush", "Force", "Huntmaster"): continue
            self.assertTrue(e["say"], f"{k} has no game reading")

    def test_the_glossary_is_not_in_the_engine_stamp(self):
        import inspect
        self.assertNotIn("gloss", inspect.getsource(lab._engine_hash))
        self.assertNotIn("lexicon", inspect.getsource(lab._engine_hash))

class TheSeamsRunBackwards(unittest.TestCase):
    def test_merges_undo(self):
        for word, parts in (("Brakrosh", ["Brak", "Krosh"]), ("Jatteld", ["Jatte", "Eld"]), ("Allak", ["All", "Lak"]),
                            ("Hrimogel", ["Hrim", "Mogel"]), ("Storeykande", ["Stor", "Reyk", "Ande"]),
                            ("Allmeraukvig", ["All", "Mer", "Auk", "Vig"]), ("Halvbeinbryn", ["Halv", "Bein", "bryn"])):
            self.assertIn(parts, lexicon.parses(word), word)

    def test_english_names_dont_come_apart(self):
        self.assertIsNone(lexicon.decompose("Engulf"))

    def test_two_readings_are_found(self):
        self.assertEqual(len(lexicon.parses("Rodaska")), 2)       # Rod + Daska, or Rod + Aska

class TheLexiconReadsTheCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.hero = lexicon.hero_words()

    def test_every_kit_move_is_a_hero_word(self):
        names = {h["name"] for h in self.hero}
        for c, legs in KITS.items():
            for leg, kit in legs.items():
                for v, p in kit: self.assertIn(compile_verb(v, **p)["name"], names, (c, leg, v))

    def test_kit_legs_are_marked(self):
        krosh = next(h for h in self.hero if h["name"] == "Krosh")
        self.assertEqual(krosh["kit_legs"], [1, 2])
        self.assertEqual(next(h for h in self.hero if h["name"] == "Snarbrakrosh")["kit_legs"], [3])

    def test_prices_and_shares_match_the_compiler(self):
        h = next(h for h in self.hero if h["name"] == "Mereld")
        self.assertEqual((h["price"], h["cost_type"], h["share"]), (12, "MP", 1.5))
        self.assertEqual(next(h for h in self.hero if h["name"] == "Brakrosh")["share"], 0.6)

    def test_every_verb_has_its_tiles(self):
        t = lexicon.verb_table()
        self.assertEqual(set(t), set(VERBS))
        self.assertIn("Halv", t["Krosh"]["takes"]["tiers"]); self.assertNotIn("Halv", t["Lak"]["takes"]["tiers"])
        self.assertTrue(t["Naglskott"]["takes"]["styng"]); self.assertFalse(t["Eld"]["takes"]["styng"])

if __name__ == "__main__":
    unittest.main()
