"""The engine one decision at a time (fight_lab_spec Part 1): python3 -m unittest test_steps -v"""
import random, unittest
import engine
from engine import *
from run_spirits import hire
from composer import catalog, habitat, compose, place, spawn
from test_board import hero
CAT = catalog()

def pack(rng, level=30, hab="Barrow"):
    return spawn(place(compose(rng, habitat(CAT, hab))), level)

def random_order(b, uid, rng):
    """A random legal order from the menu, as a player clicking around would give."""
    o = b.options(uid)
    picks = []
    for m in ([o["halv"]] if o["halv"] else []) + o["moves"] + o["items"]:
        if not m["afford"]: continue
        if m["aim"] in ("self", "all"): picks.append((m["key"], None))
        elif m["targets"]: picks.append((m["key"], rng.choice(m["targets"])))
    picks.append(("guard", None))
    if o["move"]["cells"]: picks.append(("move", rng.choice(o["move"]["cells"])["cell"]))
    if rng.random() < 0.03: picks.append(("flee", None))
    return rng.choice(picks)

class Steps(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(5)
        self.party = hire(30, self.rng)
        for h in self.party: h.pouch = [["life", 2], ["firecracker", 1], ["smoke_pot", 1]]
        self.b = Battle(self.party, pack(self.rng), self.rng, events=True)

    def test_begin_shows_enemy_intents_and_waits_for_the_party(self):
        ev = self.b.begin(control="party")
        self.assertEqual(self.b.phase, "declare")
        self.assertEqual(set(self.b.awaiting()), {h.uid for h in self.party})
        intents = [e for e in ev if e["kind"] == "intent"]
        self.assertTrue(intents and all(e["side"] == "enemy" for e in intents))

    def test_commit_needs_every_order(self):
        self.b.begin(control="party")
        with self.assertRaises(ValueError): self.b.commit()

    def test_an_illegal_target_is_refused(self):
        self.b.begin(control="party")
        h = self.party[0]
        with self.assertRaises(ValueError): self.b.submit(h.uid, self.b.options(h.uid)["halv"]["key"], h.uid)

    def test_the_last_order_wins_and_shows_as_an_intent(self):
        self.b.begin(control="party")
        for h in self.party: self.b.submit(h.uid, "guard")
        h = self.party[0]; self.b.submit(h.uid, "move", self.b.options(h.uid)["move"]["cells"][0]["cell"])
        ev = self.b.commit()
        mine = [e for e in ev if e["kind"] == "intent" and e["side"] == "party"]
        self.assertEqual(next(e for e in mine if e["unit_id"] == h.uid)["move"], "Move")

    def test_guard_and_swap(self):
        self.b.begin(control="party")
        a, c = self.party[0], self.party[1]
        cell_a, cell_c = a.cell, c.cell
        self.b.submit(a.uid, "move", list(cell_c))
        for h in self.party[1:]: self.b.submit(h.uid, "guard")
        ev = self.b.commit()
        mv = [e for e in ev if e["kind"] == "move" and e["unit_id"] == a.uid]
        if a.alive and mv: self.assertEqual((a.cell, mv[0]["swapped_id"]), (cell_c, c.uid))

    def test_random_players_finish_every_fight(self):
        rng = random.Random(9)
        seen = set()
        for i in range(60):
            party = hire(rng.choice((10, 30)), rng)
            for h in party: h.pouch = [["life", 1], ["firecracker", 1], ["thunderpot", 1], ["pocket_sand", 1]]
            b = Battle(party, pack(rng, party[0].level, rng.choice(("Barrow", "Wildwood", "Rapids"))), rng, events=True)
            b.begin(control="party")
            steps = 0
            while b.phase != "over":
                if b.phase == "bonus":
                    last = [e for e in b.events if e["kind"] == "bonus"][-1]
                    self.assertTrue(set(b.awaiting()) <= {b.uid_of[n] for n in last["units"]})
                    seen.add("bonus")
                for uid in b.awaiting():
                    k, t = random_order(b, uid, rng); b.submit(uid, k, t); seen.add(k if k in ("guard", "move", "flee", "cover") else k[0])
                b.commit(); steps += 1
                self.assertLess(steps, 200)
            seen.add(b.winner)
        self.assertTrue({"bonus", "guard", "move", "m", "i", "party", "enemy"} <= seen, seen)

    def test_fight_is_the_same_loop(self):
        r1 = random.Random(3); b1 = Battle(hire(30, r1), pack(r1), r1, events=True); w1 = b1.fight()
        r2 = random.Random(3); b2 = Battle(hire(30, r2), pack(r2), r2, events=True); b2.begin()
        while b2.phase != "over": self.assertEqual(b2.awaiting(), []); b2.commit()
        self.assertEqual((w1, b1.events), (b2.winner, b2.events))

class Edges(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(11)
        self.h, self.k = hero("Hersir", self.rng), hero("Dagskald", self.rng)

    def foe(self, hp=10_000, cell=("front", 0)):
        m = spawn_family("Draugr", "Draugr", 30); m.maxhp = m.hp = hp; m.cell = cell
        m.name = f"Draugr {cell[1]}"; m.crawling = True          # one fall and it's down
        m.actions = [act("defend", "Defend", target="self")]
        return m

    def test_the_frozen_are_not_asked(self):
        b = Battle([self.h, self.k], [self.foe()], self.rng, events=True)
        self.h.status["Frozen"] = dict(rounds=3)
        b.begin(control="party")
        self.assertEqual(b.awaiting(), [self.k.uid])

    def test_a_bonus_round_waits_for_the_hero_who_earned_it(self):
        e = self.foe(); e.aff = {"Slash": "weak"}
        b = Battle([self.h, self.k], [e], self.rng, events=True); b.begin(control="party")
        halv = b.options(self.h.uid)["halv"]
        self.h.attrs["DEX"] = 999      # land the hit
        for _ in range(20):
            b.submit(self.h.uid, halv["key"], e.uid); b.submit(self.k.uid, "guard"); b.commit()
            if b.phase == "bonus": break
        self.assertEqual((b.phase, b.awaiting()), ("bonus", [self.h.uid]))
        b.submit(self.h.uid, "guard"); b.commit()
        self.assertEqual(b.phase, "declare")

    def test_a_target_that_falls_first_is_retargeted_and_reported(self):
        a, z = self.foe(hp=1, cell=("front", 0)), self.foe(cell=("front", 1))
        b = Battle([self.h, self.k], [a, z], self.rng, events=True); b.begin(control="party")
        for u in (self.h, self.k): u.attrs["DEX"] = 999
        b.submit(self.h.uid, b.options(self.h.uid)["halv"]["key"], a.uid)
        b.submit(self.k.uid, b.options(self.k.uid)["halv"]["key"], a.uid)
        ev = b.commit()
        r = [e for e in ev if e["kind"] == "retarget"]
        self.assertEqual((len(r), r[0]["was_id"], r[0]["target_id"]), (1, a.uid, z.uid))

    def test_flee_is_a_weighted_coin_and_ends_the_fight(self):
        b = Battle([self.h, self.k], [self.foe()], self.rng, events=True); b.begin(control="party")
        ch = b.flee_chance(self.h); self.assertTrue(FLEE_MIN <= ch <= FLEE_MAX)
        for _ in range(30):
            b.submit(self.h.uid, "flee"); b.submit(self.k.uid, "guard"); b.commit()
            if b.phase == "over": break
        self.assertEqual(b.winner, "fled")
        self.assertTrue(any(e["kind"] == "flee_failed" for e in b.events) or ch > 0)

    def test_no_flee_from_the_hunt(self):
        b = Battle([self.h], [self.foe()], self.rng, events=True); b.no_flee = True; b.begin(control="party")
        self.assertFalse(b.options(self.h.uid)["flee"]["allowed"])
        with self.assertRaises(ValueError): b.submit(self.h.uid, "flee")

    def test_martials_get_cover_and_it_protects(self):
        b = Battle([self.h, self.k], [self.foe()], self.rng, events=True); b.begin(control="party")
        cover = next(m for m in b.options(self.h.uid)["moves"] if m["kind"] == "cover")
        self.assertEqual(cover["targets"], [self.k.uid])
        b.submit(self.h.uid, "cover", self.k.uid); b.submit(self.k.uid, "guard"); ev = b.commit()
        self.assertTrue(any(e["kind"] == "cover" and e["target_id"] == self.k.uid for e in ev))

    def test_inspect_reads_the_sheet(self):
        e = self.foe(); b = Battle([self.h], [e], self.rng, events=True); b.begin(control="party")
        c = b.inspect(e.uid)
        self.assertEqual((c["maxhp"], c["intent"]["move"]), (10_000, "Defend"))
        self.assertIn("Slash", c["affinities"])

if __name__ == "__main__":
    unittest.main()
