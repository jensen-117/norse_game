"""Engine events and the Barrow's folklore rules: python3 -m unittest test_barrow -v"""
import json, random, unittest
import engine
from engine import *
from test_board import hero
from test_grammar import step

def strike(el, power=500.0):
    a = skill(el, f"Test {el}", "Base"); a["power"] = power; a["cost"] = 0; return a

class Events(unittest.TestCase):
    def test_a_fight_streams_as_data(self):
        from run_spirits import hire
        from speed_check import composed
        rng = random.Random(5)
        b = Battle(hire(30, rng), composed(30, rng, "Mogel"), rng, events=True); b.fight()
        kinds = [e["kind"] for e in b.events]
        self.assertEqual(kinds[0], "start"); self.assertEqual(kinds[-1], "end")
        self.assertIn("intent", kinds); self.assertIn("hit", kinds)
        json.dumps(b.events)                                       # the front-end reads it as JSON
        for e in b.events:
            if e["kind"] == "intent": self.assertTrue(e["reason"]); self.assertIn("why", e)
        names = {u["unit"] for u in b.events[0]["units"]}
        for e in b.events:                                         # a re-form renames a unit: the event says so
            if e["kind"] == "reform": self.assertIn(e["was"], names); names.add(e["unit"])
            elif "unit" in e: self.assertIn(e["unit"], names)

    def test_no_events_unless_asked(self):
        rng = random.Random(1)
        b = Battle([hero("Hersir", rng)], [spawn_family("Draugr", "Halvdraugr", 30)], rng); b.fight()
        self.assertIsNone(b.events)

    def test_enemy_intents_use_the_plain_name(self):
        rng = random.Random(2)
        m = spawn_mogel("Mogel", "Eld", 30); m.cell = ("front", 0)
        b = Battle([hero("Hersir", rng)], [m], rng, events=True)
        a = next(x for x in m.actions if x.get("spot")); b.intent(m, a, b.party[0])
        self.assertEqual(b.events[-1]["shown"], '"Fire Slime!"')

class Draugr(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(3); self.h = hero("Hersir", self.rng)
        self.d = spawn_family("Draugr", "Draugr", 30); self.d.cell = ("front", 0)
        self.b = Battle([self.h], [self.d], self.rng, events=True); self.h.cell = ("front", 0)

    def hit(self, el):
        self.b.eligible, self.b.barred = set(), set(); self.d.hp = 1
        self.b.resolve(self.h, strike(el), self.d, False)

    def test_crush_leaves_a_crawler(self):
        self.hit("Crush")
        self.assertTrue(self.d.alive and self.d.crawling)
        self.assertAlmostEqual(self.d.hp, self.d.maxhp * DRAUGR_CRAWL_HP)
        self.assertEqual([a["name"] for a in self.d.actions], ["Claw"])

    def test_slash_beheads(self):
        self.hit("Slash"); self.assertFalse(self.d.alive)

    def test_it_crawls_once(self):
        self.hit("Crush"); self.hit("Crush"); self.assertFalse(self.d.alive)

class Bein(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(4); self.h = hero("Berserker", self.rng); self.h.cell = ("front", 0)
        self.k = spawn_family("Bein", "Beinbryn", 30); self.k.cell = ("front", 0)
        self.o = spawn_family("Bein", "Beinorv", 30); self.o.cell = ("rear", 0)
        self.b = Battle([self.h], [self.k, self.o], self.rng, events=True)

    def fell(self, el):
        self.b.eligible, self.b.barred = set(), set(); self.k.hp = 1
        self.b.resolve(self.h, strike(el), self.k, False)

    def test_a_slash_leaves_a_pile_that_stands_again(self):
        self.fell("Slash")
        self.assertFalse(self.k.alive); self.assertIn(self.k, self.b.piles)
        for _ in range(BEIN_PILE_ROUNDS): self.b.tick_piles()
        self.assertTrue(self.k.alive); self.assertAlmostEqual(self.k.hp, self.k.maxhp * BEIN_REASSEMBLE_HP)

    def test_crush_finishes_it(self):
        self.fell("Crush"); self.assertNotIn(self.k, self.b.piles); self.assertFalse(self.k.alive)

    def test_a_crush_on_the_pile_scatters_it(self):
        self.fell("Slash")
        self.b.resolve(self.h, strike("Crush"), self.k, False)
        self.assertNotIn(self.k, self.b.piles)
        for _ in range(3): self.b.tick_piles()
        self.assertFalse(self.k.alive)

    def test_a_rear_pile_is_out_of_melee_reach_until_exposed(self):
        self.b.eligible, self.b.barred = set(), set(); self.o.hp = 1
        self.b.resolve(self.h, dict(strike("Slash"), reach="any"), self.o, False)
        self.assertIn(self.o, self.b.piles)
        self.assertIsNone(self.b.pile_reach(self.h, strike("Crush"), self.o))
        self.k.hp = 0                                              # the Front falls: the Rear is exposed
        self.assertIsNotNone(self.b.pile_reach(self.h, strike("Crush"), self.o))

    def test_only_once(self):
        self.fell("Slash")
        for _ in range(BEIN_PILE_ROUNDS): self.b.tick_piles()
        self.fell("Slash"); self.assertNotIn(self.k, self.b.piles); self.assertFalse(self.k.alive)

class Beinar(unittest.TestCase):
    def test_beinseidr_takes_an_element(self):
        u = spawn_family("Bein", "Halvbeinseidr", 30, "Eld")
        self.assertEqual(u.name, "Halveldbeinseidr"); self.assertEqual(u.actions[0]["element"], "Eld")

    def test_archers_keep_back_and_guardians_cover(self):
        rng = random.Random(6)
        k = spawn_family("Bein", "Beinbryn", 30); o = spawn_family("Bein", "Beinorv", 30)
        d = spawn_family("Draugr", "Draugr", 30)
        b = Battle([hero("Hersir", rng)], [k, o, d], rng)
        self.assertEqual(o.cell[0], "rear"); self.assertFalse(b.wants_front(o))
        d.cell, k.cell = ("front", 0), ("front", 1); d.hp = d.maxhp * 0.45     # hurt, but not badly
        covers = [x for x in b.board_options(k, 40) if x[1]["kind"] == "cover" and x[2] is d]
        self.assertTrue(covers, "a shield-bearer covers an ally under half HP")

if __name__ == "__main__":
    unittest.main()
