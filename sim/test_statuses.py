"""Statuses as data (refactor_plan Wave 1a): the table covers everything the engine applies."""
import random, unittest
from engine import *

class TestStatusTable(unittest.TestCase):
    def test_every_applied_status_has_a_row(self):
        named = set(STATUS_ROOT) - {"Death"} | {r for r in (e["rider"] for e in ELEMENT.values()) if r}
        named |= {"Chilled", "Frozen", "Bound", "Bleeding", "Stunned"}
        self.assertEqual(named - set(STATUSES) - set(COUNTER_OF), set())   # a row, or a named counter

    def test_skips_are_in_the_table(self):
        for s in SKIP_ORDER: self.assertIn("skip", STATUSES[s])

    def test_stage_reads_sources(self):
        u = birth("Vasara", 10, random.Random(1))
        u.status["Chilled"] = dict(rounds=2)
        self.assertEqual(u.stage("SPD"), -1)
        u.status["Cursed"] = dict(rounds=3, stats=["DEF", "DEF"])
        self.assertEqual(u.stage("DEF"), -2)

    def test_flags(self):
        u = birth("Brennumar", 10, random.Random(1))
        self.assertFalse(u.silenced); u.status["Silenced"] = dict(rounds=3); self.assertTrue(u.silenced)
        u.status["Bound"] = dict(rounds=UNTIL_USED)
        self.assertTrue(u.has_flag("no_orders") and u.has_flag("breaks_bide"))


def fight(seed=1):
    rng = random.Random(seed)
    party = [birth(c, 10, random.Random(i)) for i, c in enumerate(("Vasara", "Ullar", "Brennumar"))]
    foes = family_encounter(10, rng, "Bein")
    b = Battle(party, foes, rng, events=True); b.begin(); return b

class TestCounters(unittest.TestCase):
    """Wave 1b: one counter per stat, -3..+3, named, cancelling, stepping toward zero when not pushed."""
    def test_cap_and_cancel(self):
        b = fight(); t = b.enemies[0]
        b.push(t, "ACC", -2); b.push(t, "ACC", -2)
        self.assertEqual(t.stage("ACC"), -3); self.assertEqual(t.counter_name("ACC"), "Blinded 3")
        b.push(t, "ACC", +4); self.assertEqual(t.counter_name("ACC"), "Keen 1")
        self.assertIsNone(t.counter_name("MAT"))

    def test_decay_unless_pushed(self):
        b = fight(); t = b.enemies[0]
        b.push(t, "DEF", -3); b.end_round()          # pushed this round: holds
        self.assertEqual(t.stage("DEF"), -3)
        b.end_round(); self.assertEqual(t.stage("DEF"), -2)
        b.push(t, "SPD", 2); b.end_round(); b.end_round(); b.end_round()
        self.assertEqual(t.stage("SPD"), 0)

    def test_sources_add_and_cap(self):
        b = fight(); t = b.enemies[0]
        b.push(t, "SPD", -3); t.status["Chilled"] = dict(rounds=3)
        self.assertEqual(t.stage("SPD"), -3)          # the total caps too

    def test_named_status_is_a_counter(self):
        b = fight(); t = b.enemies[0]; u = b.party[0]
        self.assertTrue(b.apply_status(u, t, "Blinded", 1.0, stacks=2))
        self.assertEqual((t.stage("ACC"), t.stage("EVA")), (-2, 0))   # Blinded no longer lowers Evasion
        self.assertNotIn("Blinded", t.status)
        b.apply_status(u, t, "AccDown", 1.0); self.assertEqual(t.counter_name("ACC"), "Blinded 3")
        self.assertTrue(b.capped(t, "Blinded"))

    def test_cleanse_lifts_lowered_only(self):
        b = fight(); u = b.party[0]
        b.push(u, "ATK", -2); b.push(u, "DEF", 2)
        b.resolve(b.party[2], cleanse_spell(), u, False)
        self.assertEqual((u.stage("ATK"), u.stage("DEF")), (0, 2))

class TestFrozenFade(unittest.TestCase):
    """Frozen: the next action is lost for sure, then 50%, then 20%; a failed roll thaws it. No refreeze."""
    def freeze(self, seed=1):
        b = fight(seed); t = spawn_family("Bein", "Beinbryn", 10)      # not a boss: bosses are immune
        b.apply_status(b.party[0], t, "Frozen", 1.0); return b, t

    def test_first_action_always_lost_and_no_orders(self):
        b, t = self.freeze()
        self.assertTrue(t.has_flag("no_orders"))
        self.assertTrue(b.skips(t)); self.assertEqual(t.status["Frozen"]["step"], 1)
        self.assertFalse(t.has_flag("no_orders"))     # thawing: a 50% roll, so a hero would get orders

    def test_no_refreeze(self):
        b, t = self.freeze(); b.skips(t)
        self.assertFalse(b.apply_status(b.party[0], t, "Frozen", 1.0))
        self.assertEqual(t.status["Frozen"]["step"], 1)

    def test_never_more_than_three(self):
        for seed in range(200):
            b, t = self.freeze(seed); lost = 0
            while b.skips(t): lost += 1
            self.assertIn(lost, (1, 2, 3)); self.assertNotIn("Frozen", t.status)

    def test_odds(self):
        n, held = 4000, [0, 0, 0, 0]
        for seed in range(n):
            b, t = self.freeze(seed); b.rng = random.Random(seed); lost = 0
            while b.skips(t): lost += 1
            held[lost] += 1
        self.assertAlmostEqual(held[1] / n, 0.5, delta=0.03)      # thawed at the 50% roll
        self.assertAlmostEqual(held[3] / n, 0.1, delta=0.02)      # held through the 20%

class TestBossImmunity(unittest.TestCase):
    def test_drott_shrugs_off_turn_enders(self):
        b = fight(); boss = spawn_family("Bein", "Fornbein", 10)
        self.assertEqual(boss.rank, "Drott")
        for s in ("Frozen", "Stunned", "Bound"):
            self.assertFalse(b.apply_status(b.party[0], boss, s, 1.0)); self.assertNotIn(s, boss.status)
        self.assertTrue(b.apply_status(b.party[0], boss, "Chilled", 1.0))

if __name__ == "__main__": unittest.main()
