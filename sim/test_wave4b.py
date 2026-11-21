"""Wave 4b: the Dagskald, tested in complete turns (classes.md Part 5; Joseph, Nov 20).

Kvad (verses on the singer; each verse heals each living ally a third of his Base Lak at round start; a verse fades
each round he doesn't sing; the song ends when he falls), Solak (Lak with Lonn: and Nimble; Flok and All), heals read
WIS in the new game, and Blindasol (Sol with Lonn: a Blinded stack on every hit that doesn't graze).
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
def song_heals(b, singer): return [e for e in evs(b, "heal", unit=singer.name, move="Kvad")]

class Singing(unittest.TestCase):
    """Song is a counter on the ally (Nov 20, Joseph): Kvad adds a stack (Merkvad two, Flokvad a row, Allkvad everyone),
    up to three; at each round's start it heals for each stack; a round nobody touched it, it loses one."""
    def party(self, *kvad):
        d, v, u = hero("Dagskald", *(kvad or ("Kvad",))), hero("Vasara", "Krosh"), hero("Ullar", "Skott")
        b = fight([d, v, u], [dummy()])
        for x in (d, v, u): x.hp = 0.3 * x.maxhp
        return b, d, v, u
    def song(self, x): return x.status.get("Song", {}).get("stacks", 0)

    def test_a_stack_heals_its_ally_from_next_round(self):
        b, d, v, u = self.party()
        hp = (v.hp, u.hp); orders(b, {d.uid: (key(d, "Kvad"), v.uid)})
        self.assertEqual((self.song(v), self.song(u)), (1, 0))
        per = b.song_heal(d, d.actions[1])
        self.assertAlmostEqual(v.hp - hp[0], per, places=6); self.assertEqual(u.hp, hp[1])   # only the one sung to
        self.assertAlmostEqual(per, KVAD_SHARE * b.heal_amount(d, dict(power=TIER_POWER["Base"], all=False)))

    def test_josephs_walkthrough(self):
        """Kvad, Kvad, Kvad, then two rounds of something else: 1, 2, 3, then 2, 1; each round's start heals at the count."""
        b, d, v, u = self.party(); v.maxhp = v.hp = 10 ** 6; v.hp -= 10 ** 5   # room to heal every round
        counts = []
        for sing in (True, True, True, False, False):
            orders(b, {d.uid: (key(d, "Kvad"), v.uid)} if sing else {}); counts.append(self.song(v))
        self.assertEqual(counts, [1, 2, 3, 2, 1])
        self.assertEqual([e["stacks"] for e in evs(b, "heal", move="Kvad")], [1, 2, 3, 2, 1])   # rounds 2-6's starts: round 4
                                                         # heals at 3 and fades to 2 at its end, so round 5 heals at 2

    def test_merkvad_adds_two_and_caps_at_three(self):
        b, d, v, u = self.party(("Kvad", dict(tier="Mer")))
        orders(b, {d.uid: (key(d, "Merkvad"), v.uid)}); self.assertEqual(self.song(v), 2)
        orders(b, {d.uid: (key(d, "Merkvad"), v.uid)}); self.assertEqual(self.song(v), 3)

    def test_flokvad_a_row_allkvad_everyone_at_their_share(self):
        b, d, v, u = self.party(("Kvad", dict(target="Flok")), ("Kvad", dict(target="All")))
        d.cell, v.cell, u.cell = ("rear", 0), ("front", 0), ("front", 1)
        orders(b, {d.uid: (key(d, "Flokvad"), v.uid)})
        self.assertEqual((self.song(d), self.song(v), self.song(u)), (0, 1, 1))
        orders(b, {d.uid: (key(d, "Allkvad"), None)})
        self.assertEqual((self.song(d), self.song(v), self.song(u)), (1, 2, 2))
        single = KVAD_SHARE * b.heal_amount(d, dict(power=TIER_POWER["Base"], all=False))
        self.assertAlmostEqual(b.song_heal(d, d.actions[1]), single * SHAPE_MULT["row"])
        self.assertAlmostEqual(b.song_heal(d, d.actions[2]), single * ALL_SHARE)

    def test_a_stun_costs_the_singing(self):
        b, d, v, u = self.party()
        orders(b, {d.uid: (key(d, "Kvad"), v.uid)}); orders(b, {d.uid: (key(d, "Kvad"), v.uid)})   # 2
        d.status["Frozen"] = dict(rounds=UNTIL_USED, step=0)
        orders(b, {}); self.assertEqual(self.song(v), 1)

    def test_the_song_outlives_the_singer_and_fades(self):
        b, d, v, u = self.party()
        orders(b, {d.uid: (key(d, "Kvad"), v.uid)}); orders(b, {d.uid: (key(d, "Kvad"), v.uid)})
        d.hp = 0; b.downed(d)
        self.assertEqual(self.song(v), 2)
        orders(b, {}); self.assertEqual(self.song(v), 1); orders(b, {}); self.assertEqual(self.song(v), 0)

    def test_the_dying_arent_healed(self):
        b, d, v, u = self.party()
        orders(b, {d.uid: (key(d, "Kvad"), u.uid)})
        u.hp = 0; b.downed(u)                                             # falling clears it
        orders(b, {}); self.assertEqual(u.hp, 0); self.assertEqual(self.song(u), 0)

class Solak(unittest.TestCase):
    def test_names_and_shapes(self):
        for parts, name, shape, all_ in ((dict(lonn=True), "Solak", None, False), (dict(lonn=True, target="Flok"), "Floksolak", "row", False),
                                         (dict(lonn=True, target="All"), "Allsolak", None, True), (dict(lonn=True, tier="Mer"), "Mersolak", None, False)):
            a = compile_verb("Lak", **parts); self.assertEqual((a["name"], a.get("shape"), a["all"]), (name, shape, all_))
        self.assertIn("Nimble", plain(compile_verb("Lak", lonn=True)))

    def test_heals_and_leaves_them_nimble(self):
        d, v = hero("Dagskald", ("Lak", dict(lonn=True))), hero("Vasara", "Krosh"); b = fight([d, v], [dummy()])
        v.hp = 0.3 * v.maxhp; hp = v.hp
        orders(b, {d.uid: (key(d, "Solak"), v.uid)})
        self.assertGreater(v.hp, hp); self.assertEqual(v.counter_name("EVA"), "Nimble 1"); self.assertIsNone(d.counter_name("EVA"))

    def test_mersolak_two_stacks(self):
        d, v = hero("Dagskald", ("Lak", dict(lonn=True, tier="Mer"))), hero("Vasara", "Krosh"); b = fight([d, v], [dummy()])
        orders(b, {d.uid: (key(d, "Mersolak"), v.uid)}); self.assertEqual(v.counter_name("EVA"), "Nimble 2")

    def test_floksolak_heals_a_row_at_the_row_share(self):
        d, v, u = hero("Dagskald", ("Lak", dict(lonn=True, target="Flok"))), hero("Vasara", "Krosh"), hero("Ullar", "Skott")
        b = fight([d, v, u], [dummy()])
        d.cell, v.cell, u.cell = ("rear", 0), ("front", 0), ("front", 1)
        for x in (d, v, u): x.hp = 0.3 * x.maxhp
        hp = {x.name: x.hp for x in (d, v, u)}
        orders(b, {d.uid: (key(d, "Floksolak"), v.uid)})
        a = d.actions[1]; h = b.heal_amount(d, a)
        self.assertAlmostEqual(h, b.heal_amount(d, dict(a, shape=None)) * SHAPE_MULT["row"])
        self.assertAlmostEqual(v.hp - hp[v.name], h); self.assertAlmostEqual(u.hp - hp[u.name], h)
        self.assertEqual(d.hp, hp[d.name]); self.assertEqual((v.counter_name("EVA"), u.counter_name("EVA")), ("Nimble 1", "Nimble 1"))

class WisHeals(unittest.TestCase):
    def test_the_new_game_heals_from_wis(self):
        d = hero("Dagskald", "Lak"); b = Battle([d], [dummy()], random.Random(1)); lak = d.actions[1]
        self.assertAlmostEqual(b.heal_amount(d, lak), 1.5 * lak["power"] * level_factor(d.level) * d.attrs["WIS"] / avg_attr(d.level))
        self.assertGreater(b.heal_amount(d, lak) / (1.5 * lak["power"] * level_factor(d.level) * d.MAT / avg_attr(d.level)), 1.1)

    def test_old_fights_heal_from_mat(self):
        u = birth("Dagskald", 30, random.Random(1)); b = Battle([u], [dummy()], random.Random(1)); lak = heal_spell("Base")
        self.assertAlmostEqual(b.heal_amount(u, lak), 1.5 * lak["power"] * level_factor(u.level) * u.MAT / avg_attr(u.level))

class Blindasol(unittest.TestCase):
    def test_a_stack_on_every_hit_that_lands(self):
        d = hero("Dagskald", ("Sol", dict(lonn=True))); e = dummy(); b = fight([d], [e])
        self.assertEqual(d.actions[1]["name"], "Blindasol")
        for n in range(1, 4):
            d.stages["ACC"] = 3; e.stages["EVA"] = -3                        # a Sol that can't graze
            orders(b, {d.uid: (key(d, "Blindasol"), e.uid)})
            self.assertEqual(e.stage("ACC"), -n)
        self.assertEqual(e.counter_name("ACC"), "Blinded 3")

class TheAISings(unittest.TestCase):
    def test_allkvad_when_the_party_is_hurt(self):
        d, v, u = hero("Dagskald", "Lak", ("Kvad", dict(target="All"))), hero("Vasara", "Krosh"), hero("Ullar", "Skott")
        for x in (d, v, u): x.hp = 0.55 * x.maxhp
        b = Battle([d, v, u], [dummy()], random.Random(1))
        picks = [b.declare(d)[0]["name"] for _ in range(20)]
        self.assertEqual(max(set(picks), key=picks.count), "Allkvad")

    def test_lak_for_one_ally_near_death(self):
        d, v, u = hero("Dagskald", "Lak", ("Kvad", dict(target="All"))), hero("Vasara", "Krosh"), hero("Ullar", "Skott")
        u.hp = 0.1 * u.maxhp
        b = Battle([d, v, u], [dummy()], random.Random(1))
        picks = [b.declare(d) for _ in range(20)]
        self.assertTrue(any(a["name"] == "Lak" and t is u for a, t in picks))
        self.assertGreater(sum(a["name"] == "Lak" for a, t in picks), sum(a["name"] == "Allkvad" for a, t in picks))

    def test_kvad_on_the_one_who_needs_it(self):
        d, v, u = hero("Dagskald", "Kvad"), hero("Vasara", "Krosh"), hero("Ullar", "Skott")
        v.hp = 0.4 * v.maxhp
        b = Battle([d, v, u], [dummy()], random.Random(1))
        picks = [b.declare(d) for _ in range(20)]
        kv = [t for a, t in picks if a["name"] == "Kvad"]
        self.assertTrue(kv); self.assertEqual(max(set(kv), key=kv.count), v)

    def test_it_holds_a_song_at_three(self):
        d, v = hero("Dagskald", "Kvad"), hero("Vasara", "Krosh"); v.hp = 0.5 * v.maxhp     # the singer whole: it's hers
        b = Battle([d, v], [dummy()], random.Random(1)); per = b.song_heal(d, d.actions[1])
        v.status["Song"] = dict(rounds=UNTIL_USED, stacks=3, heal=per, src=d, touched=False)
        self.assertEqual(b.declare(d), (d.actions[1], v))

    def test_the_dagskald_kits_play_whole(self):
        from composer import catalog, habitat, compose, place, spawn
        cat, seen = catalog(), set()
        for leg in (1, 2, 3):
            self.assertEqual(build_hero("Dagskald", leg).excluded, [])
        for i in range(30):
            rng = random.Random(700 + i)
            party = [build_hero(c, 3) for c in ("Vasara", "Dagskald", "Brennumar")]
            foes = spawn(place(compose(rng, habitat(cat, ("Barrow", "Wildwood", "Rapids")[i % 3]))), ENEMY_LEVEL)
            b = Battle(party, foes, rng, events=True); b.fight()
            seen |= {e.get("move") for e in b.events if e["kind"] == "intent" and e.get("unit") == "Dagskald"}
        self.assertTrue({"Allkvad", "Solak"} <= seen, seen)

if __name__ == "__main__": unittest.main()
