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

class TheAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import audit; cls.audit = audit; cls.doc = audit.build()

    def test_effects_are_read_from_what_moves_do(self):
        from words import compile_verb
        self.assertIn("Sundered", self.audit.effects(compile_verb("Krosh", lonn=True), designated=True))
        self.assertIn("Mighty", self.audit.effects(compile_verb("Aukraft")))            # a stat move, by its worn name
        self.assertIn("Fortified", self.audit.effects(compile_verb("Aukraft", lonn=True)))

    def test_the_known_gaps(self):
        e = self.doc["effects"]
        self.assertIn("no hero gives it", e["Keen"]["missing"])
        self.assertEqual(e["Silenced"]["sources"].get("kits"), None)                      # Bannskott is in no kit
        self.assertTrue(e["Frozen"]["sources"]["foes"])                                     # reached by chilling twice
        self.assertIn("Guard (everyone)", e["Guard"]["sources"]["heroes"])

    def test_every_primer_names_a_gap_or_a_riderless_verb(self):
        from gloss import PRIMERS
        riderless = {r["verb"] for r in self.doc["riderless"]}
        for k in PRIMERS:
            if k.endswith(" rider"): self.assertIn(k[:-6], riderless, k)
            else: self.assertIn(k, self.doc["effects"], k)

class TheBenchAgreesWithTheCompiler(unittest.TestCase):
    """bench_rules.js (the workbench's judge) against words.compile_verb on every carve: legal or not, and the name."""
    def test_every_carve(self):
        import itertools, json, os, shutil, subprocess, tempfile
        from words import OverCap
        node = shutil.which("node")
        if not node: self.skipTest("node isn't installed")
        lex = lexicon.export(os.path.join(tempfile.mkdtemp(), "lexicon.json"))
        M = lexicon.MANNER_ORDER
        mans = [()] + [(m,) for m in M] + list(itertools.combinations(M, 2))
        combos, want = [], []
        for verb, v in VERBS.items():
            own = v["rider"][1] if v.get("rider") else None
            riders = {None, "Lonn", own, "Bann", "Brak"} | {w for _, w in v.get("riders", ())}
            for tier in ("Halv", "Base", "Mer"):
                for target in (None, "Flok", "All"):
                    for ms in mans:
                        for styng in (False, True):
                            for r in riders:
                                c = dict(verb=verb, tier=tier, target=target, manners=list(ms), styng=styng, rider=r)
                                try:
                                    name = compile_verb(verb, tier=tier, target=target, manners=ms, styng=styng,
                                                        lonn=True if r == "Lonn" else (r or False))["name"]
                                except (ValueError, OverCap): name = None
                                combos.append(c); want.append(name)
        tmp = tempfile.mkdtemp()
        json.dump(dict(lex=lex, combos=combos), open(os.path.join(tmp, "in.json"), "w"), default=list)
        js = os.path.join(os.path.dirname(os.path.abspath(lexicon.__file__)), "..", "grammar_book", "bench_rules.js")
        script = ("const R=require(process.argv[1]);const d=JSON.parse(require('fs').readFileSync(process.argv[2]));"
                  "console.log(JSON.stringify(d.combos.map(c=>{const j=R.judge(d.lex,c);return j.word?j.word.name:null})))")
        got = json.loads(subprocess.run([node, "-e", script, os.path.abspath(js), os.path.join(tmp, "in.json")],
                                        capture_output=True, text=True, check=True).stdout)
        bad = [(c, w, g) for c, w, g in zip(combos, want, got) if w != g]
        self.assertEqual(bad[:5], [], f"{len(bad)} of {len(combos)} carves disagree")
        self.assertGreater(sum(1 for w in want if w), 600)

if __name__ == "__main__":
    unittest.main()
