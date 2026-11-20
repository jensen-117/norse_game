"""The Drattr court (Nov 9): jobs, Types, the new move options, and the net. python3 -m unittest test_drattr -v"""
import random, unittest
import engine
from engine import *
from test_board import hero

def dr(job, cell=("front", 0), level=30):
    r = rank_row("Drattr", job)
    u = spawn_family("Drattr", r["name"], level, job=job); u.cell = cell; return u

def move(u, name): return next(a for a in u.actions if (a.get("english") or a["name"]) == name)

class Jobs(unittest.TestCase):
    def test_ten_jobs_four_shown_names(self):
        rows = rank_rows("Drattr")
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({r["job"] for r in rows}), 10)
        self.assertEqual({r["name"] for r in rows}, {"Halvdrattr", "Drattr", "Stordrattr", "Forsdrattr"})

    def test_a_job_spawns_its_own_kit_under_the_rank_name(self):
        u = dr("Spear")
        self.assertEqual(u.name, "Drattr"); self.assertEqual(u.job, "Spear")
        self.assertEqual([a["name"] for a in u.actions], ["Spett", "Skewer", "Halvskar"])

    def test_the_shield_brother_guards(self):
        self.assertTrue(dr("Shield").guard); self.assertFalse(dr("Swords").guard)

    def test_type_points_the_lean(self):
        m, c = dr("Shield"), dr("Mystic")
        self.assertGreater(m.b("ATK"), m.b("MAT")); self.assertGreater(c.b("MAT"), c.b("ATK"))
        self.assertEqual(round(m.b("ATK") + m.b("MAT"), 6), round(c.b("ATK") + c.b("MAT"), 6))   # value-neutral

    def test_hero_types_come_from_the_class(self):
        rng = random.Random(1)
        self.assertEqual(type_of(hero("Hersir", rng)), "Martial")
        self.assertEqual(type_of(hero("Brennumar", rng)), "Magical")

    def test_other_families_keep_their_names_as_jobs(self):
        u = spawn_family("Bein", "Beinbryn", 30)
        self.assertEqual(u.job, "Beinbryn"); self.assertTrue(u.guard)

class Moves(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(4)
        self.h = hero("Hersir", self.rng); self.h.cell = ("front", 0)

    def test_twin_slash_averages_one_slash(self):
        sw, sh = dr("Swords"), dr("Shield")
        b = Battle([self.h], [sw, sh], self.rng)
        twin, slash = move(sw, "Twin Slash"), move(sh, "Slash")
        self.assertEqual(twin["hits"], 2)
        self.assertAlmostEqual(b.expected_damage(sw, self.h, twin), b.expected_damage(sh, self.h, slash))

    def test_twin_slash_reports_both_numbers(self):
        sw = dr("Swords"); b = Battle([self.h], [sw], self.rng, events=True)
        b.resolve(sw, move(sw, "Twin Slash"), self.h, False)
        hit = next(e for e in b.events if e["kind"] == "hit")
        self.assertEqual(len(hit["parts"]), 2); self.assertEqual(sum(hit["parts"]), hit["dmg"])

    def test_swift_strikes_is_a_flurry(self):
        self.assertIn("flurry", move(dr("Swords"), "Swift Strikes"))

    def test_skewer_halves_the_one_behind(self):
        sp = dr("Spear"); a = move(sp, "Skewer")
        h2 = hero("Huskarl", self.rng); h2.cell = ("rear", 0)
        b = Battle([self.h, h2], [sp], self.rng)
        self.assertEqual(b.shape_targets(sp, a, self.h), [self.h, h2])
        self.assertEqual((b.shape_mult(a, 0), b.shape_mult(a, 1)), (1.0, 0.5))

    def test_splash_hits_a_row_for_a_share_of_mp(self):
        h = dr("Halvdrattr"); a = move(h, "Splash")
        self.assertEqual(a["shape"], "row")
        self.assertTrue(3 <= h.maxmp / a["cost"] <= 4.5)

    def test_feeding_frenzy_raises_atk_and_lowers_def(self):
        p, ally = dr("Princeling", ("rear", 0)), dr("Shield")
        b = Battle([self.h], [p, ally], self.rng)
        b.resolve(p, move(p, "Feeding Frenzy"), None, False)
        for x in (p, ally): self.assertEqual((x.stages["ATK"], x.stages["DEF"]), (1, -1))

class Net(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(6)
        self.h = hero("Hersir", self.rng); self.h.cell = ("front", 0)
        self.n = dr("Net")
        self.b = Battle([self.h], [self.n], self.rng, events=True)
        self.net = move(self.n, "Net Throw")

    def test_net_throw_acts_sooner_and_once(self):
        self.assertEqual(self.b.group_of(self.n, self.net), 1)
        self.assertTrue(self.net["once"])

    def test_bound_eats_the_next_action_then_clears(self):
        self.b.resolve(self.n, self.net, self.h, False)
        self.assertIn("Bound", self.h.status)
        hp = self.n.hp
        self.b.resolve(self.h, next(a for a in self.h.actions if a["kind"] == "damage"), self.n, False)
        self.assertEqual(self.n.hp, hp)
        self.assertNotIn("Bound", self.h.status)
        self.assertEqual(self.b.events[-1]["why"], "Bound")

    def test_bound_loses_a_wind_up(self):
        self.h.status["Bound"] = dict(rounds=99)
        a = dict(next(a for a in self.h.actions if a["kind"] == "damage"), _release=True)
        self.b.resolve(self.h, a, self.n, False)
        self.assertEqual(self.b.events[-1]["kind"], "bide_lost")

    def test_cover_catches_the_net(self):
        g = hero("Huskarl", self.rng); g.cell = ("front", 1)
        b = Battle([self.h, g], [self.n], self.rng, events=True)
        self.h.covered_by = g
        b.resolve(self.n, self.net, self.h, False)
        self.assertIn("Bound", g.status); self.assertNotIn("Bound", self.h.status)

    def test_after_the_throw_she_takes_up_the_spear(self):
        self.b.plan_phase([self.n], False)
        self.b.remaining = [(0, self.n, (self.net, self.h))]
        self.b.resolve_phase()
        self.assertEqual(self.n.job, "Spear")
        self.assertEqual([a["name"] for a in self.n.actions], ["Spett", "Skewer", "Halvskar"])
        self.assertTrue(any(e["kind"] == "transform" for e in self.b.events))
        self.assertNotIn("Net Throw", [a["name"] for a in self.n.actions])

    def test_one_thrower_never_plans_two_nets(self):
        for seed in range(30):
            rng = random.Random(seed); h = hero("Hersir", rng); h.cell = ("front", 0)
            n = dr("Net"); b = Battle([h], [n], rng)
            b.plan_phase([n], False)
            nets = [d for k, u, d in b.remaining if d and d[0]["name"] == "Net Throw"]
            self.assertLessEqual(len(nets), 1)

    def test_two_throwers_mark_their_targets(self):
        seen_both = 0
        for seed in range(60):
            rng = random.Random(seed)
            party = [hero(c, rng) for c in ("Hersir", "Brennumar", "Huskarl")]
            for i, x in enumerate(party): x.cell = ("front", i)
            n1, n2 = dr("Net", ("front", 0)), dr("Net", ("front", 1))
            b = Battle(party, [n1, n2], rng)
            b.plan_phase([n1, n2], False)
            tgts = [d[1] for k, u, d in b.remaining if d and d[0]["name"] == "Net Throw"]
            self.assertEqual(len(tgts), len(set(tgts)), "no double-tap")
            seen_both += len(tgts) == 2
        self.assertGreater(seen_both, 0, "the case was exercised")

    def test_the_netted_hero_isnt_asked_for_orders(self):
        self.b.control = "party"; self.h.status["Bound"] = dict(rounds=99)
        self.assertFalse(self.b.controls(self.h))

if __name__ == "__main__":
    unittest.main()
