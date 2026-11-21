"""The new game's tuning settings (Nov 20): fight-scoped, by tier, baked into heroes, kept through a re-form."""
import random, unittest
from engine import *

def party(): return [build_hero(c, 1) for c in ("Vasara", "Ullar", "Brennumar")]

class Tuning(unittest.TestCase):
    def test_only_whole_sheet_parties(self):
        e = spawn_family("Draugr", "Stordraugr", 50); hp = e.maxhp
        b = Battle([birth("Vasara", 50, random.Random(1))], [e], random.Random(1))
        self.assertFalse(b.new_game); self.assertEqual(e.maxhp, hp); self.assertFalse(hasattr(e, "dmg_mult"))
        e2 = spawn_family("Draugr", "Stordraugr", 50)              # a mixed party must name its rules (review C15)
        with self.assertRaises(ValueError): Battle([build_hero("Vasara"), birth("Ullar", 50, random.Random(1))], [e2], random.Random(1))
        b2 = Battle([build_hero("Vasara"), birth("Ullar", 50, random.Random(1))], [e2], random.Random(1), profile="legacy")
        self.assertFalse(b2.new_game); self.assertEqual(b2.profile, "legacy")

    def test_tiers_and_hp(self):
        cases = {"Halvdraugr": "Trash", "Draugr": "Regular", "Stordraugr": "Elite", "Forndraugr": "Boss"}
        for rank, tier in cases.items():
            e = spawn_family("Draugr", rank, 50); base = e.maxhp
            self.assertEqual(enemy_tier(e), tier, rank)
            Battle(party(), [e], random.Random(1))
            self.assertAlmostEqual(e.maxhp, base * TIER_HP[tier]); self.assertEqual(e.hp, e.maxhp)
        for rank, tier in (("Halv", "Trash"), ("Litel", "Trash"), ("Ande", "Regular"), ("Stor", "Elite"), ("Drott", "Boss")):
            self.assertEqual(enemy_tier(spawn_spirit(rank, "Eld", 50)), tier, rank)

    def test_damage_both_ways(self):
        h, e = build_hero("Ullar"), spawn_family("Draugr", "Draugr", 50)
        plain = build_hero("Ullar"); plain.dmg_mult = 1.0
        b = Battle([h], [e], random.Random(1)); skott = h.actions[1]
        self.assertAlmostEqual(b.raw_damage(h, e, skott) / b.raw_damage(plain, e, skott), HERO_POWER["Ullar"])
        claw = e.actions[0]; e2 = spawn_family("Draugr", "Draugr", 50)
        self.assertAlmostEqual(b.raw_damage(e, h, claw) / b.raw_damage(e2, h, claw), ENEMY_DAMAGE)

    def test_items_are_fixed(self):
        h, e = build_hero("Ullar"), spawn_family("Draugr", "Draugr", 50)
        b = Battle([h], [e], random.Random(1)); fc = item_move("firecracker")
        plain = build_hero("Ullar"); plain.dmg_mult = 1.0
        self.assertEqual(b.raw_damage(h, e, fc), b.raw_damage(plain, e, fc))

    def test_a_reformed_mogel_keeps_the_settings(self):
        m = spawn_mogel("Stor", "Jord", 50)
        b = Battle(party(), [m], random.Random(1), events=True)
        m.hp = 0; b.downed(m, "Slash")
        fresh = spawn_mogel("Litel", "Jord", 50)
        self.assertEqual(m.mogel_rank, "Litel"); self.assertEqual(m.dmg_mult, ENEMY_DAMAGE)
        self.assertAlmostEqual(m.maxhp, fresh.maxhp * TIER_HP["Trash"])
        self.assertAlmostEqual(m.hp, m.maxhp * MOGEL_REFORM_HP)

class Bodies(unittest.TestCase):
    def test_stat_blocks(self):
        v = build_hero("Vasara"); plain = sheet_attrs("Vasara", SHEET_LEVEL)
        self.assertAlmostEqual(v.maxhp, HP_MULT * (20 + 2 * plain["CON"] + 2 * SHEET_LEVEL) * 1.25)
        self.assertAlmostEqual(v.DEF, plain["CON"] * 1.25)
        u = build_hero("Ullar"); self.assertGreater(u.speed(), v.speed())
        self.assertEqual(build_hero("Brennumar").b("ATK"), 1.0)          # a stat the class never uses stays neutral

    def test_value_is_near_neutral(self):
        W = dict(HP=1, ATK=1, MAT=1, DEF=0.5, MDF=0.5, SPD=0.5, WIL=0.25)
        for c, body in CLASS_BODIES.items():
            v = sum(W[k] * (m - 1) for k, m in body.items())
            self.assertTrue(-0.01 <= v <= 0.11, (c, v))

    def test_enemies_act_once_in_the_new_game(self):
        boss = spawn_family("Draugr", "Forndraugr", 50); reg = spawn_family("Draugr", "Draugr", 50)
        Battle(party(), [boss, reg], random.Random(1))
        self.assertEqual((boss.actions_per_round, reg.actions_per_round), (1, 1))
        self.assertEqual(enemy_tier(boss), "Boss")                      # still a boss
        old = spawn_family("Draugr", "Draugr", 50); Battle([birth("Vasara", 50, random.Random(1))], [old], random.Random(1))
        self.assertEqual(old.actions_per_round, 2)                       # legacy fights unchanged

if __name__ == "__main__": unittest.main()
