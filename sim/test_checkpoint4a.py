"""The Wave 4a bug-fix checkpoint (AGENT_CODE_REVIEW.md): independent behavioural tests by finding ID.
Each class reproduces its finding from the review; it failed on 0590982 before the fix."""
import random, unittest
from engine import *
from grammar import compile_word
from words import compile_verb

QUIET = [act("defend", "Defend", target="self")]

def hero(cls, *kit):
    return build_hero(cls, kit=[(BASIC_VERB[cls], dict(tier="Halv"))] + [(k, {}) if isinstance(k, str) else k for k in kit])   # packs its Halv (Wave C)

def dummy(hp=10 ** 6, actions=QUIET, job="Spear", level=SHEET_LEVEL, **kw):
    e = spawn_family("Drattr", "Drattr", level, job=job); e.maxhp = e.hp = hp
    e.actions = [dict(a) for a in actions]; e.aff = {}
    for k, v in kw.items(): setattr(e, k, v)
    return e

def key(u, name): return f"m{next(i for i, a in enumerate(u.actions) if a['name'] == name)}"
def evs(b, kind, **m): return [e for e in b.events if e["kind"] == kind and all(e.get(k) == v for k, v in m.items())]
def guard_rest(b, plan=None):
    for uid in b.awaiting(): b.submit(uid, *(plan or {}).get(uid, ("guard", None)))

# ================================================================ C16: a non-damage wind-up in the net's valuation
class C16_NonDamageWindUps(unittest.TestCase):
    def test_the_review_fixture_finishes_its_turn(self):
        """The review's seed-20 fixture: real leg-3 kits, an unmodified Net Drattr, a Bonus Round."""
        v, u, br = build_hero("Vasara", 3), build_hero("Ullar", 3), build_hero("Brennumar", 3); br.mp = 0
        e = spawn_family("Drattr", "Drattr", 50, job="Net")
        b = Battle([v, u, br], [e], random.Random(20), events=True); b.begin("party")
        b.submit(v.uid, "guard"); b.submit(u.uid, "guard"); b.submit(br.uid, key(br, "Djupanda"))
        b.commit()                                                     # raised KeyError: None
        self.assertTrue(evs(b, "windup", unit=br.name))

    def test_the_net_values_stopping_djupanda(self):
        br = hero("Brennumar", ("Anda", dict(manners=("Bid",)))); br.mp = 0; e = dummy(job="Net")
        b = Battle([br], [e], random.Random(1)); dj = br.actions[1]
        ref = 20 * level_factor(e.level) * getattr(e, "dmg_mult", 1.0)
        calm = b.bind_value(e, br, ref)
        br.bide = (dj, None)
        self.assertGreater(b.bind_value(e, br, ref), calm)               # a deep breath is worth stopping

    def test_a_damage_wind_up_still_counts(self):
        v = hero("Vasara", "Krosh"); e = dummy(job="Net"); b = Battle([v], [e], random.Random(1))
        ref = 20 * level_factor(e.level); calm = b.bind_value(e, v, ref)
        bid = compile_verb("Krosh", manners=("Bid",)); v.bide = (bid, e)
        self.assertAlmostEqual(b.bind_value(e, v, ref) - calm, NET_BIDE * b.expected_damage(v, e, bid))

# ================================================================ C13: planning keeps a pending wind-up visible
class C13_PendingThreatSurvivesPlanning(unittest.TestCase):
    def fixture(self, level=15):
        v, d = build_hero("Vasara"), build_hero("Dagskald")
        e = spawn_family("Drattr", "Drattr", level, job="Spear")
        b = Battle([v, d], [e], random.Random(1), events=True)
        a = compile_word("Skott", manner="Bid"); e.actions = [a]; e.bide = (a, d); e.actions_per_round = 1
        return b, v, d, e

    def test_threat_is_the_same_before_and_after_planning(self):
        b, v, d, e = self.fixture()
        before = b.bide_threat(d); self.assertGreater(before, 0)
        b.plan_phase([v, d, e], False)
        self.assertAlmostEqual(b.bide_threat(d), before)                # was 0: the queued release was invisible

    def test_counted_once_and_gone_on_interruption(self):
        b, v, d, e = self.fixture(); before = b.bide_threat(d)
        b.plan_phase([v, d, e], False)
        self.assertAlmostEqual(b.bide_threat(d), before)                # not doubled
        b.interrupt(e, "fell"); self.assertEqual(b.bide_threat(d), 0)

    def test_the_planning_heroes_see_it(self):
        """Declaring after the release is queued, the healthy Vasara covers the Dagskald it is aimed at. (A level-50
        shot: ~286 expected, three times her Krosh; at level 15 her Krosh rightly outscores covering a 50.)"""
        b, v, d, e = self.fixture(level=50)
        v.actions.append(compile_verb("Lya")); price_bars(v)
        b.plan_phase([v, e], False)                                     # d not declaring: v decides with the release queued
        plan = {u.name: x[0]["name"] for k, u, x in b.remaining if x is not None}
        self.assertEqual(plan[v.name], "Lya")

# ================================================================ C05: an action-time fall still ends the charge
class C05_ActionTimeFallsEndTheCharge(unittest.TestCase):
    def fixture(self, enemy):
        v, d = build_hero("Vasara"), build_hero("Dagskald")
        b = Battle([v, d], [enemy], random.Random(1), events=True)
        a = compile_word("Skott", manner="Bid"); enemy.actions = [a]; enemy.bide = (a, d)
        enemy.hp = 1; enemy.status["Bleeding"] = {"rounds": 3}
        b.begin("party"); guard_rest(b)
        return b, v, d, enemy

    def check(self, enemy):
        b, v, d, e = self.fixture(enemy)
        before = d.hp; b.commit()
        self.assertEqual(before, d.hp)                                  # the old release didn't fire
        self.assertEqual(len(evs(b, "bide_lost")), 1)
        self.assertIsNone(e.charge); self.assertIsNone(e.bide)          # nothing stale left behind

    def test_a_crawling_draugr(self): self.check(spawn_family("Draugr", "Draugr", 50))
    def test_a_reforming_mogel(self): self.check(spawn_mogel("Stor", "Jord", 50))

    def test_an_uninterrupted_release_still_fires(self):
        v, d = build_hero("Vasara"), build_hero("Dagskald"); e = spawn_family("Draugr", "Draugr", 50)
        b = Battle([v, d], [e], random.Random(1), events=True)
        a = compile_word("Skott", manner="Bid"); e.actions = [a]; e.bide = (a, d)
        b.begin("party"); guard_rest(b); b.commit()
        self.assertTrue(evs(b, "hit", src=e.name)); self.assertIsNone(e.charge)

# ================================================================ C12: a taunted foe's finishing blow goes to the taunter
class C12_TauntCatchesFinishingBlows(unittest.TestCase):
    def fixture(self, reach="any"):
        v, d = build_hero("Vasara"), build_hero("Dagskald")
        e = spawn_family("Drattr", "Drattr", 15, job="Spear")
        e.actions = [dict(strike("Pierce", power=1), cost=0, reach=reach)]
        b = Battle([v, d], [e], random.Random(1), events=True)
        d.hp = 0; b.downed(d); d.breaths = 2
        b.begin("party"); return b, v, d, e

    def test_the_reachable_taunter_takes_it(self):
        b, v, d, e = self.fixture()
        hp = v.hp; b.submit(v.uid, key(v, "Egga"), e.uid); b.commit()
        self.assertEqual(d.state, "dying"); self.assertEqual(d.breaths, 1)   # only the end-of-round breath
        self.assertLess(v.hp, hp); self.assertTrue(evs(b, "drawn"))

    def test_an_unreachable_taunter_cant_redirect(self):
        """A short blade can't reach her behind a standing Ullar: the taunt doesn't pull it, and the fallen in the
        Front is still in reach of the finishing blow."""
        v, d, u = build_hero("Vasara"), build_hero("Dagskald"), build_hero("Ullar")
        e = spawn_family("Drattr", "Drattr", 15, job="Spear"); e.actions = [dict(strike("Pierce", power=1), cost=0, reach="melee")]
        b = Battle([v, d, u], [e], random.Random(1), events=True)
        v.cell, d.cell, u.cell = ("rear", 0), ("front", 0), ("front", 1)
        d.hp = 0; b.downed(d); d.breaths = 3; b.begin("party")
        b.submit(v.uid, key(v, "Egga"), e.uid); guard_rest(b); b.commit()
        self.assertFalse(evs(b, "drawn"))
        self.assertTrue(any(x["kind"] == "breath" and x.get("src") == e.name for x in b.events))

    def test_an_untaunted_foe_still_finishes(self):
        b, v, d, e = self.fixture()
        e2 = spawn_family("Drattr", "Drattr", 15, job="Spear"); e2.actions = [dict(strike("Pierce", power=1), cost=0, reach="any")]
        b2 = Battle([build_hero("Vasara"), build_hero("Dagskald")], [e, e2], random.Random(1), events=True)
        v2, d2 = b2.party; d2.hp = 0; b2.downed(d2); d2.breaths = 3; b2.begin("party")
        b2.submit(v2.uid, key(v2, "Egga"), e.uid); b2.commit()                       # e taunted, e2 not
        self.assertTrue(any(x["kind"] == "breath" and x.get("src") == e2.name for x in b2.events))

# ================================================================ C17: the AI scores the whole move
class C17_WholeMoveValue(unittest.TestCase):
    def pick(self, u, e, n=30):
        b = Battle([u], [e], random.Random(1)); return [b.declare(u) for _ in range(n)], b

    def test_it_refreshes_a_fading_burn(self):
        br = hero("Brennumar", "Sveda"); br.actions = br.actions[1:]        # Sveda alone: the refresh must be scored
        e = dummy(); b = Battle([br], [e], random.Random(1))
        b.apply_status(br, e, "Scorched", 1.0, tier="Base"); e.status["Scorched"]["step"] = 2
        self.assertTrue(all(t is e for a, t in [b.declare(br) for _ in range(30)] if a["name"] == "Sveda"))
        self.assertGreater(b.status_value(br, br.actions[0], e, 100), 0)

    def test_a_fresh_burn_of_the_same_blow_is_redundant(self):
        br = hero("Brennumar", "Sveda"); e = dummy(); b = Battle([br], [e], random.Random(1))
        b.apply_status(br, e, "Scorched", 1.0, tier="Base", move=br.actions[1])
        self.assertEqual(b.status_value(br, br.actions[1], e, 100), 0)

    def test_it_extends_a_shorter_pin_not_a_longer_one(self):
        u = hero("Ullar", ("Naglskott", dict(tier="Mer"))); e = dummy(); b = Battle([u], [e], random.Random(1))
        ng = u.actions[1]
        self.assertGreater(b.status_value(u, ng, e, 100), 0)                # a clean target
        e.status["Pinned"] = dict(rounds=1); self.assertEqual(b.status_value(u, ng, e, 100), 0)   # Nov 24: a window: no adding

    def test_lonnpeka_on_the_fully_marked_still_sunders(self):
        u, v = hero("Ullar", ("Peka", dict(lonn=True))), hero("Vasara", "Krosh"); e = dummy()
        b = Battle([u, v], [e], random.Random(1)); lp = u.actions[1]
        e.stages["EVA"] = -3
        self.assertGreater(b.status_value(u, lp, e, 100), 0)
        u.actions = [lp]                                                   # nothing else to do: it's picked, at e
        self.assertTrue(any(a["name"] == "Genomskoda" and t is e for a, t in [b.declare(u) for _ in range(30)]))
        e.stages["DEF"] = -3                                               # Marked 3 and Sundered 3: truly redundant
        self.assertEqual(b.status_value(u, lp, e, 100), 0)

    def test_styng_counts_despite_a_capped_main(self):
        u = hero("Brennumar", ("Reyk", dict(styng=True))); e = dummy(); b = Battle([u], [e], random.Random(1))
        e.stages["ACC"] = -3
        self.assertGreater(b.status_value(u, u.actions[1], e, 100), 0)

# ================================================================ C18: one occupancy rule
class C18_TheFallenHoldTheirCell(unittest.TestCase):
    def fixture(self):
        u, v, d = hero("Ullar", "Skrida"), hero("Vasara", "Krosh"), hero("Dagskald", "Sol")
        b = Battle([u, v, d], [dummy()], random.Random(1), events=True); b.begin("party")
        u.cell, v.cell, d.cell = ("front", 0), ("front", 1), ("rear", 0)
        d.hp = 0; b.downed(d)
        return b, u, v, d

    def test_skrida_isnt_offered_the_fallens_cell(self):
        b, u, v, d = self.fixture()
        sk = next(m for m in b.options(u.uid)["moves"] if m["name"] == "Skrida")
        self.assertNotIn(["rear", 0], [c["cell"] for c in sk["cells"]])
        with self.assertRaises(ValueError): b.submit(u.uid, key(u, "Skrida"), ["rear", 0])

    def test_a_fall_after_the_order_holds_the_glide(self):
        u, v, d = hero("Ullar", "Skrida"), hero("Vasara", "Krosh"), hero("Dagskald", "Sol")
        b = Battle([u, v, d], [dummy()], random.Random(1), events=True); b.begin("party")
        u.cell, v.cell, d.cell = ("front", 0), ("front", 1), ("rear", 1)
        b.submit(u.uid, key(u, "Skrida"), ["rear", 0]); b.submit(v.uid, "guard"); b.submit(d.uid, "guard")
        d.cell = ("rear", 0); d.hp = 0; b.downed(d)                       # she falls there before it lands
        b.commit()
        self.assertEqual(u.cell, ("front", 0)); self.assertEqual(d.cell, ("rear", 0))
        self.assertEqual(len({x.cell for x in (u, v, d)}), 3)
        b.stand_up(d, 0.2, False); self.assertEqual(len({x.cell for x in (u, v, d)}), 3)   # revival finds her own cell

    def test_ordinary_move_and_the_ai_respect_it_too(self):
        b, u, v, d = self.fixture()
        self.assertFalse(b.step_to(v, ("rear", 0))[0])
        v.cell = ("rear", 1); u.cell = ("rear", 2)                         # the Front empty but for the fallen? no:
        d.cell = ("front", 0)                                              # the fallen lies in the Front
        steps = [o for o in b.board_options(v, 10) if o[1]["name"] == "Step up"]
        self.assertTrue(all(tuple(o[1]["cell"]) != ("front", 0) for o in steps))

# ================================================================ C19: Cover takes a damaging move whole
class C19_CoverCatchesStyng(unittest.TestCase):
    def fixture(self, hero_, coverer_weak=None):
        e1, e2 = dummy(), dummy(aff={coverer_weak: "weak"} if coverer_weak else {})
        b = Battle([hero_], [e1, e2], random.Random(1), events=True); b.begin("party")
        e1.cell, e2.cell = ("front", 0), ("front", 1)
        e1.covered_by = e2
        return b, e1, e2

    def test_styngnaglskott_hits_and_pins_the_protector(self):
        u = hero("Ullar", ("Naglskott", dict(styng=True)))
        b, e1, e2 = self.fixture(u, coverer_weak="Pierce")                 # weak: the Pin lands for sure
        b.submit(u.uid, key(u, "Genomskott"), e1.uid); b.commit()
        self.assertTrue(evs(b, "covered", unit=e2.name))
        self.assertEqual([x["unit"] for x in evs(b, "hit", src=u.name)], [e2.name])
        self.assertIn("Pinned", e2.status); self.assertNotIn("Pinned", e1.status)

    def test_styngegga_strikes_and_dares_the_protector(self):
        v = hero("Vasara", ("Egga", dict(styng=True)))
        b, e1, e2 = self.fixture(v)
        b.submit(v.uid, key(v, "Daska"), e1.uid)
        b.commit()
        hits = [x["unit"] for x in evs(b, "hit", src=v.name)]
        self.assertEqual(hits, [e2.name]); self.assertTrue(evs(b, "covered", unit=e2.name))
        self.assertTrue(any(x["kind"] == "taunt" and x["targets"] == [e2.name] for x in b.events))

    def test_moves_without_damage_arent_caught(self):
        u = hero("Ullar", "Naglskott"); b, e1, e2 = self.fixture(u)
        b.submit(u.uid, key(u, "Naglskott"), e1.uid); b.commit()
        self.assertFalse(evs(b, "covered"))

    def test_a_rear_protector_is_reached_where_the_ally_stood(self):
        """A short Styng strike from the Vasara reaches the Front foe; the coverer from the Rear takes it there."""
        v = hero("Vasara", ("Egga", dict(styng=True))); b, e1, e2 = self.fixture(v)
        e2.cell = ("rear", 1)
        b.submit(v.uid, key(v, "Daska"), e1.uid); b.commit()
        self.assertEqual([x["unit"] for x in evs(b, "hit", src=v.name)], [e2.name])
        self.assertFalse(evs(b, "out_of_reach"))

# ================================================================ C15: the rules profile is explicit
class C15_TheRulesAreNamed(unittest.TestCase):
    def test_the_review_case(self):
        """All sheets: the new settings. One old recruit in its place: refused unless the profile is named."""
        e = spawn_family("Draugr", "Forndraugr", 50); b = Battle([build_hero(c) for c in ("Vasara", "Ullar", "Brennumar")], [e], random.Random(1))
        self.assertEqual((b.profile, e.dmg_mult, e.actions_per_round), ("new", ENEMY_DAMAGE, ENEMY_ACTIONS))
        mixed = [build_hero("Vasara"), build_hero("Ullar"), birth("Hafrunar", 50, random.Random(1))]
        with self.assertRaises(ValueError): Battle(mixed, [spawn_family("Draugr", "Forndraugr", 50)], random.Random(1))
        with self.assertRaises(ValueError): Battle(mixed, [spawn_family("Draugr", "Forndraugr", 50)], random.Random(1), profile="new")
        b2 = Battle(mixed, [spawn_family("Draugr", "Forndraugr", 50)], random.Random(1), profile="legacy")
        self.assertEqual(b2.profile, "legacy")
        old = Battle([birth("Hafrunar", 50, random.Random(1))], [spawn_family("Draugr", "Draugr", 50)], random.Random(1))
        self.assertEqual(old.profile, "legacy")                            # the regression fixtures need no change

    def test_the_lab_plays_the_new_game_and_says_so(self):
        import json, lab
        self.assertEqual({c["key"] for c in json.loads(lab.menus())["classes"]}, set(KITS))
        with self.assertRaises(ValueError): lab.make_party(json.dumps([dict(cls="Hafrunar", level=50)]))
        lab.set_seed(3)
        for _ in range(10):                                                # random rolls stay in the new game
            spec = json.loads(lab.make_party(json.dumps([dict(cls="random", level=50) for _ in range(3)])))["spec"]
            self.assertTrue(all(s["cls"] in KITS for s in spec)); self.assertEqual(len({s["cls"] for s in spec}), 3)
        lab.roll_pack("Barrow", 6, "any", 50); lab.start("auto")
        self.assertEqual(lab.S["record"]["profile"], "new")

# ================================================================ the agreed rules (Nov 20): Halv, Pin and Cover
class Nov20Rules(unittest.TestCase):
    def test_halv_only_on_attacks(self):
        for v in ("Lak", "Vakna", "Skolja", "Sveda", "Reyk", "Naglskott", "Egga", "Knyta", "Kvad", "Aukskold", "Skrida", "Anda"):
            with self.assertRaises(ValueError, msg=v): compile_verb(v, tier="Halv")
        for v in ("Eld", "Skott", "Krosh", "Sol", "Blast", "Blixt", "Fangskott", "Avliva", "Hevn"):
            h = compile_verb(v, tier="Halv"); self.assertEqual(h["price"], HALV_COST[h["cost_type"]], v)   # Nov 21: Halv's own rung

    def test_a_pinned_vasara_still_covers(self):
        """Cover moves no one (Nov 20): a Pin doesn't stop Lya."""
        v, d = hero("Vasara", "Lya"), hero("Dagskald", "Sol"); e = dummy(actions=[dict(strike("Pierce", power=5), cost=0, reach="any")])
        b = Battle([v, d], [e], random.Random(1), events=True); b.begin("party")
        b.apply_status(e, v, "Pinned", 1.0); cell = v.cell
        b.submit(v.uid, key(v, "Lya"), d.uid); b.submit(d.uid, "guard"); b.commit()
        self.assertTrue(evs(b, "cover", unit=v.name)); self.assertEqual(v.cell, cell)

    def test_hevn_resets_at_a_lost_turn_too(self):
        """Her count resets at each action opportunity, a frozen one included (Nov 20, Joseph)."""
        v = hero("Vasara", "Hevn"); e = dummy(); b = Battle([v], [e], random.Random(1), events=True); b.begin("party")
        v.hits_taken = 3; b.submit(v.uid, key(v, "Hevn"), e.uid)
        v.status["Frozen"] = dict(rounds=UNTIL_USED, step=0); b.commit()
        self.assertTrue(evs(b, "skip", unit=v.name)); self.assertEqual(v.hits_taken, 0)

if __name__ == "__main__": unittest.main()
