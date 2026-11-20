"""The bug-fix checkpoint (AGENT_CODE_REVIEW.md): one independent behavioural test per finding, by ID."""
import random, unittest
from engine import *
from grammar import compile_word

def last_breath_fixture(seed=3):
    """A Dying Ullar on his last breath; Vasara about to win with one blow (the review's C01 fixture)."""
    u1, u2 = birth("Ullar", 30, random.Random(1)), birth("Vasara", 30, random.Random(2))
    d = spawn_family("Drattr", "Drattr", 30, job="Spear"); d.hp = 1; d.actions = [act("defend", "Defend", target="self")]
    u2.actions = [strike("Crush", "Big", 10000)]
    b = Battle([u1, u2], [d], random.Random(seed), events=True); b.downed(u1); u1.hp = 0
    b.begin("party"); u1.breaths = 1
    return b, u1, u2, d

def order_all(b, key_for):
    for uid in b.awaiting(): b.submit(uid, *key_for(uid))

class C01_VictorySettlesFirst(unittest.TestCase):
    def test_last_breath_victory_stabilises(self):
        b, u1, u2, d = last_breath_fixture()
        order_all(b, lambda uid: ("m0", "e0") if uid == u2.uid else ("guard", None))
        b.commit()
        self.assertEqual(b.winner, "party")
        self.assertEqual(u1.state, "up"); self.assertTrue(u1.wounded)
        self.assertEqual(sum(e["kind"] == "stabilised" for e in b.events), 1)
        self.assertEqual(sum(e["kind"] == "end" for e in b.events), 1)
        b.commit()                                    # committing a finished fight changes nothing
        self.assertEqual(sum(e["kind"] == "end" for e in b.events), 1)

    def test_ongoing_fight_still_loses_breaths(self):
        b, u1, u2, d = last_breath_fixture(); d.hp = d.maxhp = 10 ** 9
        u2.actions = [strike("Crush", "Tap", 1)]
        u1.breaths = 2
        order_all(b, lambda uid: ("m0", "e0") if uid == u2.uid else ("guard", None))
        b.commit()
        self.assertEqual((u1.state, u1.breaths), ("dying", 1))

    def test_flee_victory_obeys_the_same_rule(self):
        b, u1, u2, d = last_breath_fixture()
        b.fled = True
        order_all(b, lambda uid: ("guard", None))
        b.commit()
        self.assertEqual((b.winner, u1.state), ("fled", "up"))

    def test_the_dead_stay_dead(self):
        b, u1, u2, d = last_breath_fixture(); b.die(u1, "probe")
        order_all(b, lambda uid: ("m0", "e0") if uid == u2.uid else ("guard", None))
        b.commit()
        self.assertEqual((b.winner, u1.state), ("party", "dead"))

if __name__ == "__main__": unittest.main()
