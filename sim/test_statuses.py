"""Statuses as data (refactor_plan Wave 1a): the table covers everything the engine applies."""
import random, unittest
from engine import *

class TestStatusTable(unittest.TestCase):
    def test_every_applied_status_has_a_row(self):
        named = set(STATUS_ROOT) - {"Death"} | {r for r in (e["rider"] for e in ELEMENT.values()) if r and r != "AccDown"}
        named |= {"Chilled", "Frozen", "Bound", "Bleeding", "Stunned"}
        self.assertEqual(named - set(STATUSES), set())

    def test_skips_are_in_the_table(self):
        for s in SKIP_ORDER: self.assertIn("skip", STATUSES[s])

    def test_stage_reads_sources(self):
        u = birth("Vasara", 10, random.Random(1))
        u.status["Chilled"] = dict(rounds=2); u.status["Blinded"] = dict(rounds=2)
        self.assertEqual((u.stage("SPD"), u.stage("ACC"), u.stage("EVA")), (-1, -1, -1))
        u.status["Cursed"] = dict(rounds=3, stats=["DEF", "DEF"])
        self.assertEqual(u.stage("DEF"), -2)

    def test_flags(self):
        u = birth("Brennumar", 10, random.Random(1))
        self.assertFalse(u.silenced); u.status["Silenced"] = dict(rounds=3); self.assertTrue(u.silenced)
        u.status["Bound"] = dict(rounds=UNTIL_USED)
        self.assertTrue(u.has_flag("no_orders") and u.has_flag("breaks_bide"))

if __name__ == "__main__": unittest.main()
