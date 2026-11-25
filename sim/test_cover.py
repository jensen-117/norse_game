"""D10 (Nov 23-24): the shared Cover rule in the new game. A Cover takes its interceptions (Lya 1, Merlya 2, a foe's
Great Cover 3), then the stance ends; a whole move is one interception; Lonnlya (Bulwark) raises the coverer's shield
first. The old game's Cover lasts the round, untouched."""
import random, unittest
from engine import *
from test_wave4a import hero, dummy, orders, key

def ng(party, foes):
    b = Battle(party, foes, random.Random(1), profile="new", events=True); b.begin("party"); return b

STRIKE = dict(kind="damage", all=False, element="Slash", name="Hew")

class Cover(unittest.TestCase):
    def setUp(self):
        self.v = hero("Vasara", "Lya"); self.d = hero("Dagskald", "Lak"); self.e = dummy()

    def test_lya_takes_one_hit_then_ends(self):
        b = ng([self.v, self.d], [self.e])
        orders(b, {self.v.uid: (key(self.v, "Lya"), self.d.uid)})
        # the round is over; set the stance again by hand to watch two hits in one round
        self.d.covered_by, self.d.cover_left = self.v, 1
        self.assertEqual(b.intercept(self.e, STRIKE, [self.d])[0], [self.v])
        self.assertIsNone(self.d.covered_by)
        self.assertEqual(b.intercept(self.e, STRIKE, [self.d])[0], [self.d])   # the second goes through

    def test_the_cover_line_says_the_next_hit(self):
        b = ng([self.v, self.d], [self.e])
        orders(b, {self.v.uid: (key(self.v, "Lya"), self.d.uid)})
        line = next(e["text"] for e in b.events if e["kind"] == "cover")
        self.assertIn("covers Dagskald (the next hit)", line)

    def test_merlya_takes_two(self):
        v = hero("Vasara", ("Lya", dict(tier="Mer"))); b = ng([v, self.d], [self.e])
        a = next(m for m in v.actions if m["kind"] == "cover"); self.assertEqual(b.covers(a), 2)
        self.d.covered_by, self.d.cover_left = v, 2
        b.intercept(self.e, STRIKE, [self.d]); self.assertIs(self.d.covered_by, v)
        b.intercept(self.e, STRIKE, [self.d]); self.assertIsNone(self.d.covered_by)

    def test_great_cover_takes_three(self):
        self.assertEqual(COVERS_BY_TIER["Jatte"], 3)

    def test_lonnlya_raises_the_shield_first(self):
        v = hero("Vasara", ("Lya", dict(lonn=True))); b = ng([v, self.d], [self.e])
        a = next(m for m in v.actions if m["kind"] == "cover"); self.assertEqual(a["name"], "Lonnlya")
        orders(b, {v.uid: (key(v, "Lonnlya"), self.d.uid)})
        self.assertEqual(v.stage("DEF"), 1)
        self.assertIn("raising your shield", b.plain(a))

    def test_rows_arent_caught(self):
        b = ng([self.v, self.d], [self.e]); self.d.covered_by, self.d.cover_left = self.v, 1
        row = dict(STRIKE, shape="row")
        self.assertEqual(b.intercept(self.e, row, [self.d])[0], [self.d]); self.assertEqual(self.d.cover_left, 1)

    def test_the_round_ends_the_stance(self):
        b = ng([self.v, self.d], [self.e])
        orders(b, {self.v.uid: (key(self.v, "Lya"), self.d.uid)})
        self.assertIsNone(self.d.covered_by); self.assertEqual(self.d.cover_left, 0)

    def test_the_old_game_covers_all_round(self):
        b = Battle([self.v, self.d], [self.e], random.Random(1), profile="legacy", events=True); b.begin("party")
        self.d.covered_by = self.v
        for _ in range(3): self.assertEqual(b.intercept(self.e, STRIKE, [self.d])[0], [self.v])
        self.assertIs(self.d.covered_by, self.v)

if __name__ == "__main__":
    unittest.main()
