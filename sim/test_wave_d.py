"""Wave D (Nov 24, Joseph): the fuse. Poison 12/6/2.4% and Bleed 14/7/2.8% of max HP by height, never more than a clean
Krosh; one clock (a stack drops at round end unless fed; Bleed bites only when its bearer acts). Withered, Aska's twist:
healing halved, blocked, reversed; withered bones stay down. The Curse stays on dedicated Curse moves."""
import random, unittest
from engine import *
from test_wave4a import hero, dummy, fight, orders, key

def ng(*units, hp=None):
    party = [u for u in units if u.side == "party"]; foes = [u for u in units if u.side == "enemy"]
    b = Battle(party, foes, random.Random(1), profile="new", events=True)
    for e, h in zip(foes, hp or ()):                     # the new game sets foes' HP by tier: set it after
        if h: e.maxhp = e.hp = h
    return b

class TheFuse(unittest.TestCase):
    def test_poison_burns_down_12_6_2(self):
        e = dummy(); u = hero("Ullar", "Skott"); b = ng(u, e, hp=[500])
        b.apply_status(u, e, "Poisoned", 1.0, 3); b.end_round()             # landed: holds at 3
        bites = []
        for _ in range(4):
            hp = e.hp; b.tick_statuses(e, "round_start"); bites.append(round(hp - e.hp)); b.end_round()
        self.assertEqual(bites, [60, 30, 12, 0])                            # 12%, 6%, 2.4% of 500, then out

    def test_never_more_than_a_krosh(self):
        e = dummy(); u = hero("Ullar", "Skott"); b = ng(u, e, hp=[1700])
        self.assertEqual(b.fuse_tick(e, "Poisoned", 3), KROSH_CLEAN)
        self.assertEqual(round(b.fuse_tick(e, "Poisoned", 1)), round(0.12 * 0.2 * 1700))

    def test_feeding_holds_it_at_three(self):
        e = dummy(); u = hero("Ullar", "Skott"); b = ng(u, e, hp=[500])
        for _ in range(5): b.apply_status(u, e, "Poisoned", 1.0, 1); b.end_round()
        self.assertEqual(e.status["Poisoned"]["rounds"], 3)

    def test_bleed_bites_on_acting_and_burns_down_either_way(self):
        e = dummy(); u = hero("Ullar", "Skott"); b = ng(u, e, hp=[500])
        b.apply_status(u, e, "Bleeding", 1.0, 3); b.end_round()
        hp = e.hp; b.tick_statuses(e, "action"); self.assertEqual(round(hp - e.hp), 70)   # 14% of 500
        b.end_round(); self.assertEqual(e.status["Bleeding"]["rounds"], 2)
        b.end_round(); self.assertEqual(e.status["Bleeding"]["rounds"], 1)               # no act, no bite, still drops

    def test_the_ai_reads_the_fuse(self):
        u = hero("Ullar", "Skott"); big, small = dummy(), dummy(); b = ng(u, big, small, hp=[1700, 130])
        a = dict(kind="status", status="Poisoned", tier="Mer", target="enemy", element="Gro", all=False)
        self.assertGreater(b.status_gain(u, a, big, 2, 100.0)[0], b.status_gain(u, a, small, 2, 100.0)[0])

class Withered(unittest.TestCase):
    def test_halved_blocked_reversed(self):
        d = hero("Dagskald", "Lak"); v = hero("Vasara", "Krosh"); b = ng(d, v, dummy())
        v.hp = 500
        for n, f in ((1, 0.5), (2, 0.0), (3, -1.0)):
            v.status["Withered"] = dict(rounds=n); self.assertEqual(b.heal_factor(v), f)
        hp = v.hp; b.mend(v, 75); self.assertEqual(v.hp, hp - 75)           # Withered 3: the healing burns

    def test_song_hurts_a_withered_three(self):
        v = hero("Vasara", "Krosh"); b = ng(v, dummy()); v.hp = 500
        v.status["Song"] = dict(rounds=UNTIL_USED, stacks=2, heal=30); v.status["Withered"] = dict(rounds=3)
        b.sing(); self.assertEqual(v.hp, 440)

    def test_withered_bones_stay_down(self):
        from composer import catalog, spawn
        bein = next(u for e in catalog() if e["family"] == "Bein" for u in spawn([(0, 0, e)], ENEMY_LEVEL))
        v = hero("Vasara", "Krosh"); b = ng(v, bein)
        bein.status["Withered"] = dict(rounds=2); bein.hp = 0; b.downed(bein, "Slash")
        self.assertIn(bein, b.piles); left = b.piles[bein]
        b.tick_piles(); self.assertEqual(b.piles[bein], left)

    def test_aska_withers_and_curses_stay_dedicated(self):
        self.assertEqual(CHILD_TWIST["Aska"], "Withered")
        self.assertEqual(SHORTHAND["Cursed"], (("Sundered", 1), ("Poisoned", 1)))

class TheLogShowsTheHeal(unittest.TestCase):
    def test_numbers(self):
        d = hero("Dagskald", "Lak"); v = hero("Vasara", "Krosh"); b = fight([d, v], [dummy()]); v.hp = 400
        orders(b, {d.uid: (key(d, "Lak"), v.uid), v.uid: ("guard", None)})
        line = next(e["text"] for e in b.events if e["kind"] == "heal")
        self.assertRegex(line, r"Vasara \(\+\d+\)")

if __name__ == "__main__":
    unittest.main()
