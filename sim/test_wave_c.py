"""Wave C (Nov 24, Battle_Refactor_Current D8, D9): sustain. No universal Meditate (Anda is found, Djupanda is Anda
wound up), Lak 75 for 12 MP (Gyllenlykt 20), no Halv filled in, the knots' trickle, and the Rest."""
import random, unittest
from engine import *
from words import compile_verb
from test_wave4a import hero, dummy, fight, orders, key

class Prices(unittest.TestCase):
    def test_lak_and_the_lantern(self):
        self.assertEqual(LAK_CLEAN, 75)
        self.assertEqual((compile_verb("Lak")["price"], compile_verb("Lak", lonn=True)["price"]), (12, 20))

    def test_djupanda_is_anda_wound_up(self):
        d = compile_verb("Anda", manners=("Bid",))
        self.assertEqual(d["name"], "Djupanda"); self.assertTrue(d.get("bide"))
        self.assertAlmostEqual(d["amount"], ANDA_SHARE * MANNERS["Bid"]["power"])
        self.assertAlmostEqual(compile_verb("Anda")["amount"], ANDA_SHARE)

class TheRest(unittest.TestCase):
    def test_it_heals_two_thirds_and_the_wound(self):          # Joseph's pre-flight: the pools come back whole
        v = build_hero("Vasara"); full_hp, full_mp = v.maxhp, v.maxmp
        b = Battle([v], [dummy()], random.Random(1)); b.stand_up(v, 1, True)
        self.assertTrue(v.wounded); self.assertLess(v.maxhp, full_hp)
        v.hp = 1; rest(v)
        self.assertFalse(v.wounded); self.assertEqual((v.maxhp, v.maxmp), (full_hp, full_mp))
        self.assertAlmostEqual(v.hp, 1 + REST_SHARE * full_hp)

    def test_a_caster_gets_mp(self):
        d = build_hero("Dagskald"); d.mp = 0; rest(d); self.assertAlmostEqual(d.mp, REST_SHARE * d.maxmp)

    def test_the_dead_stay_dead(self):
        v = build_hero("Vasara"); v.state, v.hp = "dead", 0; rest(v); self.assertEqual((v.state, v.hp), ("dead", 0))

class StatMovesAnswerFirst(unittest.TestCase):
    def test_lifting_a_drop_is_worth_more_than_stacking(self):   # Joseph's pre-flight: no Aukskold to +3 on a whim
        v = hero("Vasara", "Aukskold"); b = fight([v], [dummy()])
        a = next(m for m in v.actions if m["name"] == "Aukskold")
        v.stages["DEF"] = -1; low = b.declare(v)
        v.stages["DEF"] = 2; high = b.declare(v)
        self.assertEqual(low[0]["name"], "Aukskold")             # answers its Sundered
        self.assertNotEqual(high[0]["name"], "Aukskold")         # at +2 it would rather hit

if __name__ == "__main__":
    unittest.main()
