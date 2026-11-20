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

# ---------------------------------------------------------------- the compiler contract (C08-C11, A01, A02)
from itertools import combinations
from words import compile_verb, normalize, OverCap, check_move, unresolved, finalize, LADDER

def arena(verb, n_party=3, **parts):
    """A hero casting one compiled verb in a real turn (after the review's fixture)."""
    party = [birth(c, 10, random.Random(i)) for i, c in enumerate(("Vasara", "Dagskald", "Skurmar")[:n_party])]
    move = compile_verb(verb, **parts); party[0].actions = [move]
    party[0].maxmp = party[0].mp = 100; price_bars(party[0])
    enemy = spawn_family("Drattr", "Drattr", 10, job="Spear"); enemy.maxhp = enemy.hp = 10 ** 6; enemy.aff = {}
    enemy.actions = [act("defend", "Defend", target="self")]; enemy.actions_per_round = 1
    b = Battle(party, [enemy], random.Random(10), events=True)
    return b, party, enemy, move

def one_turn(b, target=None):
    b.begin("party")
    for uid in b.awaiting(): b.submit(uid, "m0" if uid == "p0" else "guard", target if uid == "p0" else None)
    b.commit()

TIERS_ = [None, "Halv", "Mer", "Jatte", "Ur"]

class C08_TierAccessAndPrice(unittest.TestCase):
    def test_storm_cannot_promote_into_a_cheap_ur(self):
        self.assertEqual(compile_verb("Storm", tier="Mer")["tier"], "Jatte")            # Merstorm, carvable
        with self.assertRaises(ValueError): compile_verb("Storm", tier="Jatte", source="find")   # would be Ur
        with self.assertRaises(ValueError): compile_verb("Eld", tier="Jatte")            # a Jatte part isn't carved
        with self.assertRaises(ValueError): compile_verb("Eld", tier="Ur", source="find")
        self.assertEqual(compile_verb("Storm", tier="Jatte", source="gear")["tier"], "Ur")

    def test_every_verb_respects_its_source(self):
        for verb in VERBS:
            for t in TIERS_:
                for src, top in SOURCE_TIER.items():
                    try: a = compile_verb(verb, tier=t, source=src)
                    except ValueError: continue
                    if t not in (None, "Halv"): self.assertLessEqual(LADDER.index(t), LADDER.index(top), (verb, t, src))
                    if a["tier"] == "Ur": self.assertEqual(src, "gear", (verb, t))

    def test_a_higher_tier_never_costs_less(self):
        for verb in VERBS:
            shares = []
            for t in (None, "Mer", "Jatte", "Ur"):
                try: shares.append((t, compile_verb(verb, tier=t, source="gear")["share"]))
                except ValueError: pass
            for (t1, s1), (t2, s2) in zip(shares, shares[1:]):
                if s1: self.assertGreater(s2, s1, f"{verb}: {t2} costs less than {t1}")

class C09_TargetsDoWhatTheySay(unittest.TestCase):
    def test_unsupported_scopes_are_refused(self):
        for verb in ("Aukseid", "Vakna", "Byr", "Kvad", "Knyta", "Egga", "Lya"):
            with self.assertRaises(ValueError): compile_verb(verb, target="All")

    def test_aukskold_reaches_herself_her_row_or_everyone(self):
        for parts, want in (({}, [1, 0, 0]), ({"target": "All"}, [1, 1, 1])):
            b, p, e, m = arena("Aukskold", **parts); one_turn(b)
            self.assertEqual([u.stages["DEF"] for u in p], want, parts)
        b, p, e, m = arena("Aukskold", target="Flok"); one_turn(b)
        row = p[0].cell[0]
        self.assertEqual([u.stages["DEF"] for u in p], [1 if u.cell[0] == row else 0 for u in p])

    def test_all_heal_reaches_every_ally(self):
        b, p, e, m = arena("Lak", target="All")
        for u in p: u.hp = u.maxhp * 0.3
        before = [u.hp for u in p]; one_turn(b)
        self.assertTrue(all(u.hp > h for u, h in zip(p, before)))

class C10_RecipesAreExact(unittest.TestCase):
    def test_duplicates_are_refused(self):
        with self.assertRaises(ValueError): compile_verb("Skott", tier="Mer", manners=("Drif", "Drif"), lonn=True)
        self.assertEqual(compile_verb("Skott", tier="Mer", manners=("Drif",), lonn=True)["name"], "Tusensplitter")

    def test_surplus_parts_fail(self):
        with self.assertRaises(OverCap): compile_verb("Skott", tier="Mer", target="All", manners=("Drif",), lonn=True)

class C11_ManneredHeals(unittest.TestCase):
    def heal(self, **parts):
        b, p, e, m = arena("Lak", **parts); p[1].hp = 1; before = p[1].hp; one_turn(b, target="p1")
        if m.get("bide"): one_turn_more(b)
        return p[1].hp - before, m

    def test_heavy_heals_more_and_costs_more(self):
        (plain, a), (heavy, t) = self.heal(), self.heal(manners=("Tung",))
        self.assertAlmostEqual(heavy / plain, 1.2, places=3)
        self.assertGreater(t["cost"], a["cost"]); self.assertEqual(t["group"], -2)

    def test_crits_and_flurries_dont_apply_to_heals(self):
        for mn in ("Jarf", "Drif"):
            with self.assertRaises(ValueError): compile_verb("Lak", manners=(mn,))

def one_turn_more(b, target=None):
    for uid in b.awaiting(): b.submit(uid, "guard")
    b.commit()

class A01_OneContract(unittest.TestCase):
    def test_every_path_meets_the_contract(self):
        for k in ITEMS: self.assertEqual(check_move(item_move(k)), [], k)
        net = family_move(("status", "Bound", "Base", dict(name="Net Throw", once=True, sure=True, thrown=True)))
        self.assertEqual(check_move(net) + unresolved(net), [])
        rv = compile_move("revive", "Vakna", "Base")
        self.assertEqual((rv["reaches"], rv["hp"], rv["wound"]), ("Dying", 0.20, False))
        for cls in KITS:
            for leg in KITS[cls]:
                for a in compile_kit(cls, leg): self.assertEqual(check_move(a), [], a["name"])

    def test_an_unfinished_move_cant_enter_a_fight(self):
        song = compile_verb("Kvad")
        self.assertTrue(song["unresolved"])
        u = birth("Dagskald", 10, random.Random(1)); u.actions = [song]
        with self.assertRaises(ValueError): Battle([u], [spawn_family("Bein", "Beinbryn", 10)], random.Random(1))

class A02_ModifierPolicy(unittest.TestCase):
    def test_unknown_parts(self):
        with self.assertRaises(ValueError): compile_verb("Eld", target="Bogus")
        with self.assertRaises(ValueError): compile_verb("Eld", manners=("Quick",))
        with self.assertRaises(ValueError): compile_verb("Eld", tier="Huge")

    def test_swift_and_heavy_contradict_in_any_order(self):
        for mn in (("Snar", "Tung"), ("Tung", "Snar")):
            with self.assertRaises(ValueError): compile_verb("Krosh", manners=mn)

    def test_the_meteor_is_order_free(self):
        a, b = compile_verb("Eld", manners=("Bid", "Tung")), compile_verb("Eld", manners=("Tung", "Bid"))
        self.assertEqual((a["release_group"], a["share"]), (b["release_group"], b["share"]))

    def test_redundant_parts(self):
        with self.assertRaises(ValueError): compile_verb("Egga", manners=("Snar",))       # already First
        with self.assertRaises(ValueError): compile_verb("Djupanda", manners=("Bid",))    # already Patient
        with self.assertRaises(ValueError): compile_verb("Reyk", manners=("Tung",))       # nothing to make heavier

# ---------------------------------------------------------------- C04-C07
from knowledge import Memory, kind_of
from composer import compose, CompositionError

def frozen_target(seed=4, aff=None):
    ul = birth("Ullar", 30, random.Random(1)); t = spawn_family("Drattr", "Drattr", 30, job="Spear")
    t.hp = t.maxhp = 10 ** 6
    if aff is not None: t.aff = aff
    b = Battle([ul], [t], random.Random(seed), events=True); b.apply_status(ul, t, "Frozen", 1.0)
    return b, ul, t

class C04_OneShatterRule(unittest.TestCase):
    def test_a_flurry_shatters_once(self):
        b, ul, t = frozen_target()
        b.flurry(ul, compile_word("Skott", manner="Drif"), t, 3, False)
        self.assertNotIn("Frozen", t.status)
        self.assertEqual(sum(e["kind"] == "shatter" for e in b.events), 1)

    def test_a_multi_hit_shatters_once(self):
        b, ul, t = frozen_target(); ul.cell = ("front", 0)
        b.resolve(ul, dict(compile_word("Skott"), hits=3, power=2), t, False)
        self.assertEqual(sum(e["kind"] == "shatter" for e in b.events), 1)

    def test_null_and_absorb_dont_shatter(self):
        for aff in ({"Pierce": "null"}, {"Pierce": "absorb"}):
            b, ul, t = frozen_target(aff=aff)
            b.resolve(ul, compile_word("Skott"), t, False)
            self.assertIn("Frozen", t.status, aff)
            b2, ul2, t2 = frozen_target(aff=aff)
            b2.flurry(ul2, compile_word("Skott", manner="Drif"), t2, 2, False)
            self.assertIn("Frozen", t2.status, aff)

class C05_FallingEndsAWindUp(unittest.TestCase):
    def setup(self):
        ul = birth("Ullar", 10, random.Random(1)); en = spawn_family("Drattr", "Drattr", 10, job="Spear")
        b = Battle([ul], [en], random.Random(5), events=True); ul.bide = (compile_word("Skott", manner="Bid"), en)
        return b, ul, en

    def released(self, b, u):
        b.plan_phase([u] + b.enemies, False)
        return any(d and d[0].get("_release") for k, x, d in b.remaining if x is u)

    def test_death_then_revival_cannot_release(self):
        b, ul, en = self.setup(); b.die(ul, "probe"); b.stand_up(ul, .2, True)
        self.assertFalse(self.released(b, ul))
        self.assertEqual(sum(e["kind"] == "bide_lost" for e in b.events), 1)

    def test_falling_dying_interrupts(self):
        b, ul, en = self.setup(); ul.hp = 0; b.downed(ul)
        self.assertEqual(ul.state, "dying"); self.assertIsNone(ul.bide)
        b.stand_up(ul, .2, False); self.assertFalse(self.released(b, ul))

    def test_an_unbroken_wind_up_still_releases(self):
        b, ul, en = self.setup(); self.assertTrue(self.released(b, ul))

class C06_KnowledgeFollowsTheJob(unittest.TestCase):
    def test_learn_under_the_new_job(self):
        ul = birth("Ullar", 30, random.Random(1)); net = spawn_family("Drattr", "Drattr", 30, job="Net")
        net.hp = net.maxhp = 10 ** 6
        b = Battle([ul], [net], random.Random(6), events=True); m = Memory()
        m.observe(b.begin("party"))
        b.resolve(ul, compile_word("Skott"), net, False)                 # learned as the Net
        b.transform(net, "Spear"); b.resolve(ul, compile_word("Skar"), net, False)
        m.observe(b.drain())
        card = m.mask(b.inspect(net.uid))
        self.assertNotEqual(card["affinities"]["Slash"], "?")            # learned after the transform: shown
        self.assertIn("Pierce", m.aff[kind_of("Drattr", "Net", None)])  # what was learned before stays
        self.assertNotIn("Slash", m.aff.get(kind_of("Drattr", "Net", None), {}))
        m2 = Memory.from_json(m.to_json())
        self.assertEqual(m2.aff, m.aff)
        net.hp = 0; b.downed(net); m.observe(b.drain())
        self.assertEqual(m.kills.get("Drattr|Spear"), 1)                 # credit goes to the job it fell as

def brute(pool, rules):
    """Every pack (a multiset of pool entries) that meets every rule: the reference solver for C07."""
    from itertools import combinations_with_replacement as cwr
    R = dict(budget=6, max_units=6, banned_costs=(), cost_caps={}, family_max={}, family_min={}); R.update(rules)
    out = []
    for n in range(1, R["max_units"] + 1):
        for pk in cwr(range(len(pool)), n):
            es = [pool[i] for i in pk]
            if sum(e["cost"] for e in es) != R["budget"]: continue
            if any(e["cost"] in R["banned_costs"] for e in es): continue
            if any(sum(e["cost"] == c for e in es) > m for c, m in R["cost_caps"].items()): continue
            fam = {f: sum(e["family"] == f for e in es) for f in {e["family"] for e in pool} | set(R["family_min"])}
            if any(fam.get(f, 0) > m for f, m in R["family_max"].items()): continue
            if any(fam.get(f, 0) < m for f, m in R["family_min"].items()): continue
            out.append(es)
    return out

class C07_PacksKeepTheirRules(unittest.TestCase):
    def test_the_review_cases(self):
        A, B = dict(family="A", cost=1, weight=1.0, ranged=False), dict(family="B", cost=2, weight=1.0, ranged=False)
        for seed in (1, 2, 3, 4):
            got = compose(random.Random(seed), [A, B], dict(budget=2, family_max={"A": 1}))
            self.assertEqual(got, [B])
        with self.assertRaises(CompositionError): compose(random.Random(1), [B], dict(budget=2, family_min={"A": 1}))

    def test_against_exhaustive_enumeration(self):
        rng = random.Random(77)
        for case in range(300):
            pool = [dict(family=rng.choice("ABC"), cost=rng.randint(1, 3), weight=1.0, ranged=False)
                    for _ in range(rng.randint(1, 4))]
            fams = sorted({e["family"] for e in pool} | {"C"})
            rules = dict(budget=rng.randint(2, 6), max_units=rng.randint(2, 4))
            if rng.random() < 0.5: rules["family_max"] = {rng.choice(fams): rng.randint(0, 2)}
            if rng.random() < 0.5: rules["family_min"] = {rng.choice(fams): rng.randint(1, 2)}
            if rng.random() < 0.3: rules["cost_caps"] = {rng.randint(1, 3): rng.randint(0, 1)}
            if rng.random() < 0.2: rules["banned_costs"] = (rng.randint(1, 3),)
            ok = brute(pool, rules)
            for seed in range(3):
                try: got = compose(random.Random(seed), pool, rules)
                except CompositionError:
                    self.assertFalse(ok, f"case {case}: failed though {ok[:1]} works; {pool} {rules}"); continue
                self.assertTrue(ok, f"case {case}: returned a pack where none is legal; {pool} {rules}")
                key = sorted(map(str, got))
                self.assertIn(key, [sorted(map(str, x)) for x in ok], f"case {case}: {got} breaks {rules}")
