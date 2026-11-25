"""Step 3 of the Beinar pilot (Nov 25): team plans for every new-game pack, and the Bein jobs' rules."""
import random, unittest
from engine import *
import brains
from test_wave4a import hero, dummy

def room(ranks, party=("Dagskald", "Skurmar", "Vasara"), seed=1, element="Eld"):
    ps = [build_hero(c, 2, SHEET_LEVEL) for c in party]
    fs = [spawn_family("Bein", r, ENEMY_LEVEL, element=element) for r in ranks]
    b = Battle(ps, fs, random.Random(seed), profile="new", events=True); b.begin(None)
    return b, {p.cls: p for p in ps}, fs

def plan_lines(b): return [e["text"].strip() for e in b.events if e["kind"] == "plan"]

class Plans(unittest.TestCase):
    def test_round_one_picks_and_says_a_plan(self):
        b, h, fs = room(["Beinbryn", "Beinseidr", "Beinorv"])
        b.plan_phase([u for u in b.units if u.alive], False)
        self.assertIn(b.pack_plan["plan"], ("Hunt", "Break", "Inflict"))
        self.assertEqual(len(plan_lines(b)), 1)

    def test_the_fornbein_heads_and_speaks(self):
        b, h, fs = room(["Beinbryn", "Fornbein"])
        b.plan_phase([u for u in b.units if u.alive], False)
        self.assertIs(b.pack_plan["head"], fs[1]); self.assertTrue(b.pack_plan["true_head"])
        self.assertIn("Fornbein points at", plan_lines(b)[0])

    def test_the_priority_target(self):
        b, h, fs = room(["Beinbryn", "Beinseidr", "Beinorv"])
        self.assertIs(brains.priority_target(b), h["Dagskald"])             # the healer
        h["Skurmar"].hp = 0.5 * h["Skurmar"].maxhp
        self.assertIs(brains.priority_target(b), h["Skurmar"])              # the hurt first
        h["Skurmar"].hp = h["Skurmar"].maxhp; h["Dagskald"].state = "dying"
        self.assertIs(brains.priority_target(b), h["Vasara"])               # the coverer (she carries Lya)

    def test_a_peer_head_falling_doesnt_break_the_order(self):
        b, h, fs = room(["Beinbryn", "Beinseidr", "Beinorv"])
        b.plan_phase([u for u in b.units if u.alive], False)
        head = b.pack_plan["head"]; head.hp = 0; head.state = "dead"
        b.round = 2; brains.plan_round(b)
        self.assertNotEqual(b.pack_plan["plan"], "Desperate"); self.assertIsNot(b.pack_plan["head"], head)

    def test_the_true_head_falling_breaks_it(self):
        b, h, fs = room(["Beinbryn", "Fornbein"])
        b.plan_phase([u for u in b.units if u.alive], False)
        fs[1].hp = 0; fs[1].state = "dead"; b.round = 2; brains.plan_round(b)
        self.assertEqual(b.pack_plan["plan"], "Desperate")
        self.assertEqual(plan_lines(b)[-2:], ["With Fornbein down, the order breaks!", "The bones break ranks!"])

    def test_a_hunt_they_protect_is_dropped_after_three_rounds(self):
        b, h, fs = room(["Beinbryn", "Beinseidr", "Beinorv"])
        b.plan_phase([u for u in b.units if u.alive], False)
        pk = b.pack_plan; pk.update(plan="Hunt", focus=h["Dagskald"], since=1, switched=1)
        b.round = 3; brains.plan_round(b); self.assertEqual(pk["plan"], "Hunt")
        b.round = 4; brains.plan_round(b); self.assertNotEqual(pk["plan"], "Hunt")

    def test_a_break_whose_focus_falls_turns_to_hunt(self):
        b, h, fs = room(["Beinbryn", "Beinseidr", "Beinorv"])
        b.plan_phase([u for u in b.units if u.alive], False)
        pk = b.pack_plan; pk.update(plan="Break", focus=h["Vasara"], since=1, switched=1)
        h["Vasara"].state = "dying"; b.round = 2; brains.plan_round(b)
        self.assertEqual(pk["plan"], "Hunt")

    def test_the_old_game_has_no_plans(self):
        v = hero("Vasara", "Krosh"); b = Battle([v], [dummy()], random.Random(1), profile="legacy", events=True)
        b.fight(); self.assertFalse(any(e["kind"] == "plan" for e in b.events)); self.assertIsNone(b.pack_plan)

class Rules(unittest.TestCase):
    def focus(self, b, x, plan="Hunt"):
        b.pack_plan = dict(head=None, family="Bein", plan=plan, focus=x, since=1, switched=1, cost=9, before=None, true_head=False)
        b.brain_claims = set(); b.brain_stats.clear()      # begin() already planned round 1: start these turns clean

    def test_archers_pin_then_cash_in_and_spread_by_claims(self):
        b, h, (o1, o2) = room(["Beinorv", "Beinorv"]); self.focus(b, h["Dagskald"])
        a, t = b.declare(o1); self.assertEqual((a["name"], t), ("Pinning Shot", h["Dagskald"]))
        a, t = b.declare(o2); self.assertNotEqual(a["name"], "Pinning Shot")     # claimed
        h["Dagskald"].status["Pinned"] = dict(rounds=2); b.brain_claims = set()
        a, t = b.declare(o1); self.assertEqual((a["name"], t), ("Killing Shot", h["Dagskald"]))

    def test_the_seidr_silences_a_caster_never_a_martial(self):
        b, h, (s,) = room(["Beinseidr"], party=("Vasara", "Ullar", "Brennumar")); self.focus(b, h["Vasara"])
        a, t = b.declare(s); self.assertEqual((a["name"], t), ("Silence", h["Brennumar"]))

    def test_no_curse_on_the_sundered(self):
        b, h, (s,) = room(["Halvbeinseidr"]); self.focus(b, h["Vasara"])
        h["Vasara"].stages["DEF"] = -1
        a, t = b.declare(s); self.assertNotEqual(a["name"], "Curse")

    def test_the_beinbryn_covers_a_struck_seidr_while_the_plan_holds(self):
        b, h, (bryn, s) = room(["Beinbryn", "Beinseidr"]); self.focus(b, h["Vasara"])
        s.struck = b.round - 1
        a, t = b.declare(bryn); self.assertEqual((a["kind"], t), ("cover", s))
        self.focus(b, h["Vasara"], plan="Break"); b.brain_claims = set()
        a, t = b.declare(bryn); self.assertNotEqual(a["kind"], "cover")           # Break presses

    def test_the_fornbein_rallies_then_waits(self):
        b, h, (f, o) = room(["Fornbein", "Beinorv"]); self.focus(b, h["Vasara"])
        a, t = b.declare(f); self.assertEqual(a["name"], "Rally")
        for x in (f, o): b.hold(f, x, "Rally", "ATK", None, 3, False, lock=False, push=2, rest=2)
        a, t = b.declare(f); self.assertNotEqual(a["name"], "Rally")

    def test_a_brain_gives_its_reason_and_counts(self):
        b, h, (o,) = room(["Beinorv"]); self.focus(b, h["Skurmar"])
        a, t = b.declare(o); b.intent(o, a, t)
        self.assertEqual(b.intents[o.uid]["why"], "pinning Skurmar")
        self.assertEqual(b.brain_stats[("Beinorv", "status:Pinned on focus")], 1)

    def test_others_fall_back_to_the_scorer_weighing_the_focus(self):
        b, h, (o,) = room(["Beinorv"]); self.focus(b, h["Skurmar"])
        o.actions = [a for a in o.actions if a["name"] == "Arrow"]
        a, t = b.declare(o)
        self.assertEqual(a["name"], "Arrow")

if __name__ == "__main__":
    unittest.main()
