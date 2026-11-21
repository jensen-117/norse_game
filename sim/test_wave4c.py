"""Wave 4c: the Skurmar, tested in complete turns (classes.md Part 7).

Knots (a pool tied by Knyta, spent by Kuling, Storm and Orkan; held: Blast harder, Blixt sure, MP at three), Orkan's
lightning, Blixt's Stun only on Lonnblixt (a class verb's riders are its own), Kasta and Svepa (a shove a row back or
forward; into an occupied cell both swap and are slammed; a Pinned unit is a wall), and Medvind (Quick).
"""
import random, unittest
from engine import *
from words import compile_verb

QUIET = [act("defend", "Defend", target="self")]
def hero(cls, *kit): return build_hero(cls, kit=[(k, {}) if isinstance(k, str) else k for k in kit])
def dummy(hp=10 ** 6, actions=QUIET, **kw):
    e = spawn_family("Drattr", "Drattr", SHEET_LEVEL, job="Spear"); e.maxhp = e.hp = hp
    e.actions = [dict(a) for a in actions]; e.aff = {}
    for k, v in kw.items(): setattr(e, k, v)
    return e
def fight(party, enemies, seed=1):
    b = Battle(party, enemies, random.Random(seed), events=True); b.begin("party"); return b
def orders(b, plan=None):
    for uid in b.awaiting(): b.submit(uid, *(plan or {}).get(uid, ("guard", None)))
    b.commit()
    while b.phase == "bonus":
        for uid in b.awaiting(): b.submit(uid, "guard")
        b.commit()
def key(u, name): return f"m{next(i for i, a in enumerate(u.actions) if a['name'] == name)}"
def evs(b, kind, **m): return [e for e in b.events if e["kind"] == kind and all(e.get(k) == v for k, v in m.items())]
def move_of(b, u, name): return next(m for m in b.options(u.uid)["moves"] if m["name"] == name)

class Knots(unittest.TestCase):
    def test_tied_up_to_three_and_kept(self):
        s = hero("Skurmar", "Knyta", ("Knyta", dict(tier="Mer"))); b = fight([s], [dummy()])
        orders(b, {s.uid: (key(s, "Knyta"), None)}); self.assertEqual(s.knots, 1)
        orders(b, {s.uid: (key(s, "Merknyta"), None)}); self.assertEqual(s.knots, 3)
        orders(b, {s.uid: (key(s, "Merknyta"), None)}); self.assertEqual(s.knots, 3)        # the cap
        orders(b, {}); orders(b, {}); self.assertEqual(s.knots, 3)                           # never decaying

    def test_one_knot_the_wind_hits_harder(self):
        s = hero("Skurmar", "Blast"); e = dummy(); b = Battle([s], [e], random.Random(1)); blast = s.actions[1]
        base = b.raw_damage(s, e, blast); s.knots = 1
        self.assertAlmostEqual(b.raw_damage(s, e, blast) / base, KNOT_BLAST)
        blixt = compile_verb("Blixt"); s.knots = 0; bx = b.raw_damage(s, e, blixt); s.knots = 1
        self.assertAlmostEqual(b.raw_damage(s, e, blixt), bx)                                # Blast only

    def test_two_knots_blixt_cant_graze(self):
        s = hero("Skurmar", "Blixt"); e = dummy(); b = Battle([s], [e], random.Random(1)); bx = s.actions[1]
        s.stages["ACC"] = -3; e.stages["EVA"] = 3                                          # grazes as likely as they get
        self.assertIn("graze", {b.roll(s, e, bx) for _ in range(200)})
        s.knots = 2
        self.assertNotIn("graze", {b.roll(s, e, bx) for _ in range(500)})
        self.assertIn("graze", {b.roll(s, e, s.actions[0]) for _ in range(200)})            # Blast still grazes

    def test_three_knots_half_a_meditate_each_round(self):
        s = hero("Skurmar", "Blast"); b = fight([s], [dummy()]); s.knots = 3; s.mp = 0
        orders(b, {}); self.assertAlmostEqual(s.mp, KNOT_MP * MEDITATE_SHARE * s.maxmp)
        s.knots = 2; mp = s.mp; orders(b, {}); self.assertEqual(s.mp, mp)

class Untying(unittest.TestCase):
    def test_kuling_costs_a_knot_on_top_of_mp(self):
        s = hero("Skurmar", "Kuling"); e1, e2 = dummy(), dummy(); b = fight([s], [e1, e2])
        self.assertFalse(move_of(b, s, "Kuling")["afford"])
        with self.assertRaises(ValueError): b.submit(s.uid, key(s, "Kuling"))
        s.knots = 2; b2 = fight([s], [dummy(), dummy()]); s.knots = 2; mp = s.mp
        orders(b2, {s.uid: (key(s, "Kuling"), None)})
        self.assertEqual(s.knots, 1); self.assertLess(s.mp, mp)
        self.assertEqual(len({x["unit"] for x in evs(b2, "hit", src=s.name)}), 2)            # everyone

    def test_storm_two_orkan_three_and_its_lightning(self):
        s = hero("Skurmar", "Storm", "Orkan"); e1, e2 = dummy(), dummy(); b = fight([s], [e1, e2]); s.knots = 3
        orders(b, {s.uid: (key(s, "Orkan"), None)})
        self.assertEqual(s.knots, 0)
        els = [x["element"] for x in evs(b, "hit", src=s.name)]
        self.assertEqual((els.count("Blast"), els.count("Blixt")), (2, 2)); self.assertTrue(evs(b, "follow"))
        self.assertEqual(compile_verb("Storm")["knots"], 2)

    def test_the_ai_unties_into_a_wide_room_and_ties_when_empty(self):
        s = hero("Skurmar", "Knyta", "Kuling"); foes = [dummy() for _ in range(4)]
        b = Battle([s], foes, random.Random(1))
        picks = [b.declare(s)[0]["name"] for _ in range(20)]
        self.assertIn("Knyta", picks); self.assertNotIn("Kuling", picks)                      # no knot: no Kuling
        s.knots = 1; picks = [b.declare(s)[0]["name"] for _ in range(20)]
        self.assertEqual(max(set(picks), key=picks.count), "Kuling")

class Lightning(unittest.TestCase):
    def test_plain_blixt_never_stuns(self):
        s = hero("Skurmar", "Blixt"); e = dummy(); b = fight([s], [e])
        for _ in range(12): orders(b, {s.uid: (key(s, "Blixt"), e.uid)})
        self.assertFalse(evs(b, "status", status="Stunned"))

    def test_lonnblixt_can(self):
        for seed in range(40):
            s = hero("Skurmar", ("Blixt", dict(lonn=True))); e = dummy(); b = fight([s], [e], seed)
            orders(b, {s.uid: (key(s, "Lonnblixt"), e.uid)})
            if evs(b, "status", status="Stunned"): return
        self.fail("Lonnblixt never stunned")

class Shoving(unittest.TestCase):
    def setup(self, verb="Kasta", **parts):
        s = hero("Skurmar", (verb, parts)); a, c = dummy(), dummy(); b = fight([s], [a, c])
        a.cell, c.cell = ("front", 0), ("rear", 2)
        return b, s, a, c, s.actions[1]["name"]

    def test_kasta_into_an_empty_cell(self):
        b, s, a, c, nm = self.setup(); hp = a.hp
        orders(b, {s.uid: (key(s, nm), a.uid)})
        self.assertEqual(a.cell, ("rear", 0)); self.assertEqual(a.hp, hp)                    # no bump

    def test_into_an_occupied_cell_both_swap_and_are_slammed(self):
        b, s, a, c, nm = self.setup(); c.cell = ("rear", 0)
        orders(b, {s.uid: (key(s, nm), a.uid)})
        self.assertEqual((a.cell, c.cell), (("rear", 0), ("front", 0)))
        for x in (a, c): self.assertEqual(x.maxhp - x.hp, max(1, int(x.maxhp * BUMP_SHARE)))

    def test_a_pinned_target_doesnt_budge(self):
        b, s, a, c, nm = self.setup(); b.apply_status(s, a, "Pinned", 1.0)
        orders(b, {s.uid: (key(s, nm), a.uid)})
        self.assertEqual(a.cell, ("front", 0)); self.assertTrue(evs(b, "rooted"))

    def test_a_pinned_occupant_is_a_wall(self):
        b, s, a, c, nm = self.setup(); c.cell = ("rear", 0); b.apply_status(s, c, "Pinned", 1.0)
        orders(b, {s.uid: (key(s, nm), a.uid)})
        self.assertEqual((a.cell, c.cell), (("front", 0), ("rear", 0))); self.assertTrue(evs(b, "wall"))
        for x in (a, c): self.assertLess(x.hp, x.maxhp)

    def test_svepa_pulls_forward_not_past_the_edge(self):
        b, s, a, c, nm = self.setup("Svepa")
        self.assertNotIn(a.uid, move_of(b, s, nm)["targets"])                                # already in the Front
        orders(b, {s.uid: (key(s, nm), c.uid)}); self.assertEqual(c.cell, ("front", 2))

    def test_styngkasta_batters_then_shoves_and_cover_takes_it_whole(self):
        b, s, a, c, nm = self.setup("Kasta", styng=True); c.cell = ("front", 1); a.covered_by = c
        orders(b, {s.uid: (key(s, nm), a.uid)})
        self.assertTrue(evs(b, "covered", unit=c.name)); self.assertEqual(c.cell, ("rear", 1)); self.assertEqual(a.cell, ("front", 0))
        self.assertTrue(evs(b, "hit", src=s.name, unit=c.name))

    def test_the_ai_pulls_a_rear_caster_into_the_blades(self):
        s, v = hero("Skurmar", "Svepa"), hero("Vasara", "Krosh"); a, c = dummy(), dummy()
        b = Battle([s, v], [a, c], random.Random(1)); a.cell, c.cell = ("front", 0), ("rear", 2)
        picks = [b.declare(s) for _ in range(20)]
        self.assertTrue(any(m["name"] == "Svepa" and t is c for m, t in picks))

class Tailwind(unittest.TestCase):
    def test_medvind_one_a_row_all(self):
        s, v, u = hero("Skurmar", "Medvind", ("Medvind", dict(target="Flok")), ("Medvind", dict(target="All"))), hero("Vasara", "Krosh"), hero("Ullar", "Skott")
        b = fight([s, v, u], [dummy()]); s.cell, v.cell, u.cell = ("rear", 0), ("front", 0), ("front", 1)
        orders(b, {s.uid: (key(s, "Medvind"), v.uid)}); self.assertEqual(v.counter_name("SPD"), "Quick 1")
        orders(b, {s.uid: (key(s, "Flokmedvind"), u.uid)})
        self.assertEqual((v.counter_name("SPD"), u.counter_name("SPD"), s.counter_name("SPD")), ("Quick 2", "Quick 1", None))
        orders(b, {s.uid: (key(s, "Allmedvind"), None)}); self.assertEqual(s.counter_name("SPD"), "Quick 1")

class TheKitsPlay(unittest.TestCase):
    def test_the_skurmar_kits_play_whole(self):
        from composer import catalog, habitat, compose, place, spawn
        cat, seen = catalog(), set()
        for leg in (1, 2, 3): self.assertEqual(build_hero("Skurmar", leg).excluded, [])
        for i in range(30):
            rng = random.Random(900 + i)
            party = [build_hero(c, 3) for c in ("Vasara", "Skurmar", "Brennumar")]
            foes = spawn(place(compose(rng, habitat(cat, ("Barrow", "Wildwood", "Rapids")[i % 3]))), ENEMY_LEVEL)
            b = Battle(party, foes, rng, events=True); b.fight()
            seen |= {e.get("move") for e in b.events if e["kind"] == "intent" and e.get("unit") == "Skurmar"}
        self.assertTrue({"Merknyta", "Storm", "Lonnblixt"} <= seen, seen)

if __name__ == "__main__": unittest.main()
