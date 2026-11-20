"""What the Company remembers: python3 -m unittest test_knowledge -v"""
import random, unittest
from engine import *
from knowledge import Memory, kind_of
from data import KNOW_HP_KILLS
from run_spirits import hire
from test_steps import pack
from test_board import hero

class Remembering(unittest.TestCase):
    def test_nothing_known_shows_nothing(self):
        rng = random.Random(1); e = spawn_mogel("Mogel", "Eld", 30); e.cell = ("front", 0)
        b = Battle([hero("Hersir", rng)], [e], rng, events=True); m = Memory(); m.observe(b.begin(control="party"))
        c = m.mask(b.inspect(e.uid))
        self.assertEqual((c["hp"], c["maxhp"], c["mp"]), (None, None, None))
        self.assertTrue(all(v == "?" for v in c["affinities"].values()))
        self.assertEqual(c["intent"]["move"], b.inspect(e.uid)["intent"]["move"])     # intent is always shown
        self.assertIn(kind_of("Mogel", "Mogel", "Eld"), m.seen)

    def test_a_hit_lifts_that_affinity(self):
        m = Memory()
        m.observe([dict(kind="start", units=[dict(id="e0", family="Mogel", rank="Mogel", element="Eld", side="enemy")]),
                   dict(kind="hit", unit_id="e0", element="Vatn", affinity="weak"),
                   dict(kind="hit", unit_id="e0", element="Crush", affinity="normal", spot=True),
                   dict(kind="hit", unit_id="e0", element="Force", affinity="normal"),
                   dict(kind="absorb", unit_id="e0", element="Eld")])
        self.assertEqual(m.aff[kind_of("Mogel", "Mogel", "Eld")], {"Vatn": "weak", "Eld": "absorb"})

    def test_hp_after_enough_kills_counted_across_elements_but_once_per_body(self):
        m = Memory()
        for i in range(KNOW_HP_KILLS):
            el = "Eld" if i % 2 else "Vatn"
            m.observe([dict(kind="start", units=[dict(id="e0", family="Draugr", rank="Draugr", element=el, side="enemy")]),
                       dict(kind="crawl", unit_id="e0"), dict(kind="down", unit_id="e0")])      # crawl then down: one kill
        card = dict(side="enemy", family="Draugr", rank="Draugr", element="Eld", hp=40, maxhp=44, mp=3, maxmp=9, affinities={"Eld": "weak"})
        c = m.mask(card)
        self.assertEqual((c["hp"], c["maxhp"], c["mp"]), (40, 44, None))

    def test_a_reform_counts_the_bigger_body_and_learns_the_smaller(self):
        m = Memory()
        m.observe([dict(kind="start", units=[dict(id="e0", family="Mogel", rank="Stormogel", element="Eld", side="enemy")]),
                   dict(kind="reform", unit_id="e0", was_id="e0", rank="Mogel"), dict(kind="down", unit_id="e0")])
        self.assertEqual(m.kills, {"Mogel|Stormogel": 1, "Mogel|Mogel": 1})

    def test_real_fights_and_saving(self):
        rng = random.Random(4); m = Memory()
        for _ in range(10):
            b = Battle(hire(30, rng), pack(rng), rng, events=True); b.fight(); m.observe(b.events)
        self.assertTrue(m.aff and m.kills)
        m2 = Memory.from_json(m.to_json())
        self.assertEqual((m2.aff, m2.kills, m2.seen), (m.aff, m.kills, m.seen))

    def test_know_everything(self):
        rng = random.Random(1); e = spawn_mogel("Mogel", "Eld", 30); e.cell = ("front", 0)
        b = Battle([hero("Hersir", rng)], [e], rng, events=True); b.begin(control="party")
        self.assertEqual(Memory().mask(b.inspect(e.uid), know_all=True)["maxhp"], round(e.maxhp))

if __name__ == "__main__":
    unittest.main()
