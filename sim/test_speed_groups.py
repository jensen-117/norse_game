"""Speed groups (combat_spec Part 3): python3 -m unittest test_speed_groups -v"""
import random, unittest
import engine
from engine import *
from run_spirits import hire

def setup(seed=1):
    rng = random.Random(seed)
    party = hire(30, rng)
    foes = [spawn_mogel("Mogel", "Eld", 30), spawn_mogel("Halv", "Vatn", 30)]
    return Battle(party, foes, rng), party, foes

def defend(u): return next(a for a in u.actions if a["kind"] == "defend") if any(a["kind"] == "defend" for a in u.actions) \
    else act("defend", "Defend", target="self")
def strike(u): return next(a for a in u.actions if a["kind"] == "damage")

class SpeedGroups(unittest.TestCase):
    def setUp(self): engine.USE_SPEED_GROUPS = True

    def test_slow_defend_beats_fast_attack(self):
        b, party, foes = setup()
        slow, fast = party[0], foes[1]
        slow.attrs["DEX"] = 1; fast.attrs["DEX"] = 200
        entries = [(0, fast, (strike(fast), slow)), (0, slow, (defend(slow), slow))]
        order = b.order(entries)
        self.assertIs(order[0][1], slow, "Defend (+3) must resolve before any group-0 attack")

    def test_fear_drops_attacks_but_not_protection(self):
        b, party, foes = setup()
        h = party[0]; h.status["Feared"] = {"rounds": 2}
        self.assertEqual(b.group_of(h, strike(h)), FEAR_GROUP)
        self.assertEqual(b.group_of(h, defend(h)), PROTECT_GROUP)
        entries = [(0, h, (strike(h), foes[0])), (0, foes[0], (strike(foes[0]), h))]
        for f in entries: pass
        foes[0].attrs["DEX"] = 1; h.attrs["DEX"] = 200
        self.assertIs(b.order(entries)[-1][1], h, "a Feared attacker goes after normal actions, however fast")

    def test_first_actions_before_second_within_a_group(self):
        b, party, foes = setup()
        big = foes[0]; big.attrs["DEX"] = 300                 # fastest unit, 2 actions
        slowest = party[2]; slowest.attrs["DEX"] = 1
        entries = [(0, big, (strike(big), slowest)), (1, big, (strike(big), slowest)), (0, slowest, (strike(slowest), big))]
        ks = [(e[0], e[1] is big) for e in b.order(entries)]
        self.assertEqual(ks, [(0, True), (0, False), (1, True)])

    def test_no_late_defends_with_groups(self):
        late = {}
        for flag in (False, True):
            engine.USE_SPEED_GROUPS = flag; rng = random.Random(4); n = 0
            for _ in range(150):
                party = hire(30, rng); foes = [spawn_mogel("Mogel", "Eld", 30), spawn_mogel("Litel", "Vatn", 30), spawn_mogel("Halv", "Jord", 30)]
                b = Battle(party, foes, rng); b.fight(); n += sum(u.stats["late"] for u in b.units)
            late[flag] = n
        self.assertEqual(late[True], 0)
        self.assertGreater(late[False], 0)

if __name__ == "__main__":
    unittest.main()
