"""Wave 4a: the starting three's kits, tested in complete turns (refactor_plan Wave 4; classes.md Parts 2-4).

Statuses (Pinned, Scorched, the riders' second statuses), payoffs (Pierce through a lowered guard, Fangskott, Avliva,
Hevn), the status-move rules (Styng, the weakness), and movement and tempo (Skrida, Djupanda, where the Ullar stands).
"""
import random, unittest
from engine import *
from words import compile_verb

QUIET = [act("defend", "Defend", target="self")]

def hero(cls, *kit):
    """A sheet hero with exactly this kit: each item a verb name or (verb, parts)."""
    # Wave C (Nov 24): no Halv is filled in any more; the test heroes pack their class's Halv first, as a player may,
    # so a kit move sits at actions[1] as it always has
    return build_hero(cls, kit=[(BASIC_VERB[cls], dict(tier="Halv"))] + [(k, {}) if isinstance(k, str) else k for k in kit])

def dummy(hp=10 ** 6, actions=QUIET, **kw):
    e = spawn_family("Drattr", "Drattr", SHEET_LEVEL, job="Spear"); e.maxhp = e.hp = hp
    e.actions = [dict(a) for a in actions]; e.aff = {}            # neutral, unless the test says (aff=...)
    for k, v in kw.items(): setattr(e, k, v)
    return e

def fight(party, enemies, seed=1):
    b = Battle(party, enemies, random.Random(seed), events=True); b.begin("party"); return b

def orders(b, plan):
    """plan: {uid: (key, target)}; everyone else guards. Runs the round (and any Bonus Round, everyone guarding)."""
    for uid in b.awaiting(): b.submit(uid, *plan.get(uid, ("guard", None)))
    b.commit()
    while b.phase == "bonus":
        for uid in b.awaiting(): b.submit(uid, "guard")
        b.commit()

def key(u, name): return f"m{next(i for i, a in enumerate(u.actions) if a['name'] == name)}"
def evs(b, kind, **match): return [e for e in b.events if e["kind"] == kind and all(e.get(k) == v for k, v in match.items())]

def land_until(make, check, tries=40):
    """Status moves roll: run fresh fights on new seeds until the status lands (the roll isn't what's under test)."""
    for seed in range(tries):
        out = make(seed)
        if check(*out): return out
    raise AssertionError("the status never landed")

# ================================================================ Pinned
class Pinning(unittest.TestCase):
    def pinned(self, parts=None):
        def make(seed):
            u = hero("Ullar", ("Naglskott", parts or {})); e = dummy(); b = fight([u], [e], seed)
            orders(b, {u.uid: (key(u, u.actions[1]["name"]), e.uid)}); return b, u, e
        return land_until(make, lambda b, u, e: "Pinned" in e.status)

    def test_rooted_only_and_two_rounds(self):                 # Nov 22 (status rules step 3): Pinned no longer slows
        b, u, e = self.pinned()
        self.assertIsNone(e.counter_name("SPD"))
        self.assertEqual(e.status["Pinned"]["rounds"], 1)                # cast in round 1: round 2 is its last
        orders(b, {}); self.assertNotIn("Pinned", e.status)

    def test_mer_pins_longer(self):
        b, u, e = self.pinned(dict(tier="Mer"))
        self.assertEqual(e.status["Pinned"]["rounds"], 2)                # three rounds: 1, 2, 3

    def test_a_pin_is_a_window(self):                        # Nov 24 (Joseph): its printed rounds, no adding while on
        b, u, e = self.pinned(dict(tier="Mer"))
        self.assertFalse(b.apply_status(u, e, "Pinned", 1.0, 1, "Base"))
        self.assertEqual(e.status["Pinned"]["rounds"], 2)

    def test_the_pinned_hero_cant_move_or_be_swapped(self):
        v, d = hero("Vasara", "Krosh"), hero("Dagskald", "Sol"); b = fight([v, d], [dummy()])
        b.apply_status(b.enemies[0], v, "Pinned", 1.0)
        self.assertEqual(b.options(v.uid)["move"]["cells"], [])
        self.assertFalse(any(c["swap"] == v.uid for c in b.options(d.uid)["move"]["cells"]))
        with self.assertRaises(ValueError): b.submit(v.uid, "move", list(d.cell))

    def test_an_ordered_swap_with_the_pinned_is_held(self):
        """Pinned after the order was given (the order stood when it was legal): the swap is held when it lands."""
        v, d = hero("Vasara", "Krosh"), hero("Dagskald", "Sol"); b = fight([v, d], [dummy()])
        b.submit(d.uid, "move", list(v.cell)); b.submit(v.uid, "guard")
        b.apply_status(b.enemies[0], v, "Pinned", 1.0)
        cells = (v.cell, d.cell); b.commit()
        self.assertEqual((v.cell, d.cell), cells); self.assertTrue(evs(b, "rooted"))

    def test_a_pinned_enemy_doesnt_advance(self):
        u = hero("Ullar", "Skott"); spear = dummy(actions=[skill("Pierce", "Spear", "Base")])
        b = Battle([u], [spear], random.Random(1), events=True)
        spear.cell = ("rear", 0); b.apply_status(u, spear, "Pinned", 1.0, 2)
        self.assertNotIn(spear, b.advancers([spear]))
        b.fight(max_rounds=2); self.assertEqual(spear.cell, ("rear", 0))

    def test_the_bow_pins_the_rear(self):
        """Naglskott and Peka fly from the bow: Long range, so the Rear is in reach from the Rear (it was melee)."""
        u = hero("Ullar", "Naglskott", "Peka"); f, r = dummy(), dummy(); b = fight([u], [f, r])
        r.cell = ("rear", 1)
        for m in ("Naglskott", "Peka"):
            self.assertIn(r.uid, next(x for x in b.options(u.uid)["moves"] if x["name"] == m)["targets"])

# ================================================================ Scorched
class Mid(random.Random):
    """Every roll comes up the middle: a plain hit, no variance."""
    def random(self): return 0.5

class Scorching(unittest.TestCase):
    """Scorched ticks off the caster's power (Nov 20, Joseph): one Eld hit at the applying tier's power x SCORCH_POWER,
    from his MAT against the target's MDF and affinity, worked out when it lands; then 100/50/20% of it."""
    def burning(self, parts=None, weak=True):
        """A Sveda on a dummy weak to fire: it lands for sure (the weakness rule)."""
        u = hero("Brennumar", ("Sveda", parts or {})); e = dummy(aff={"Eld": "weak"} if weak else {})
        b = fight([u], [e]); b.rng = Mid()        # Nov 22: a weakness no longer skips the roll; a plain hit lands it
        orders(b, {u.uid: (key(u, u.actions[1]["name"]), e.uid)})
        return b, u, e

    def ticks(self, b, e): return [x["dmg"] for x in evs(b, "tick", unit=e.name, status="Scorched")]
    def blow(self, b, u, e, tier="Base"):
        hit = dict(element="Eld", power=TIER_POWER[tier] * SCORCH_POWER, all=False)
        return b.raw_damage(u, e, hit) * {"weak": 1.5}.get(e.affinity("Eld"), 1.0)
    def tick(self, blow, step): return max(1, int(blow * FADE[step]))      # as the engine rounds

    def test_the_fade_100_50_20_then_out(self):
        b, u, e = self.burning()                         # cast in round 1; each round's start ticks it (round 2 first)
        blow = self.blow(b, u, e)
        for _ in range(3): orders(b, {})
        self.assertEqual(self.ticks(b, e), [self.tick(blow, i) for i in range(3)])
        self.assertNotIn("Scorched", e.status)

    def test_a_blow_not_a_share_of_hp(self):
        """A boss's size doesn't feed the burn: ten times the HP, the same tick."""
        u = hero("Brennumar", "Sveda"); e1, e2 = dummy(hp=1000, aff={"Eld": "weak"}), dummy(hp=10 ** 7, aff={"Eld": "weak"})
        b = Battle([u], [e1, e2], random.Random(1))
        self.assertAlmostEqual(b.dot_blow(u, e1, "Scorched", "Base"), b.dot_blow(u, e2, "Scorched", "Base"))

    def test_the_tier_sets_the_blow(self):
        b, u, e = self.burning(dict(tier="Mer"))
        self.assertEqual(self.ticks(b, e), [self.tick(self.blow(b, u, e, "Mer"), 0)])

    def test_sveda_starts_it_over(self):
        b, u, e = self.burning()                                         # 100% at round 2's start
        orders(b, {})                                                    # 50% at round 3's start
        orders(b, {u.uid: (key(u, "Sveda"), e.uid)})                     # Sveda again: 100% at round 4's start
        blow = self.blow(b, u, e)
        self.assertEqual(self.ticks(b, e), [self.tick(blow, 0), self.tick(blow, 1), self.tick(blow, 0)])

    def test_a_new_sveda_brings_its_own_blow(self):
        """The applying tier's blow (Nov 20): a Base Sveda over a Mer burn burns at Base, not the hotter one."""
        u = hero("Brennumar", ("Sveda", dict(tier="Mer")), "Sveda"); e = dummy(aff={"Eld": "weak"}); b = fight([u], [e])
        orders(b, {u.uid: (key(u, "Mersveda"), e.uid)})
        orders(b, {u.uid: (key(u, "Sveda"), e.uid)})
        self.assertAlmostEqual(e.status["Scorched"]["dmg"], self.blow(b, u, e, "Base"))

    def test_wind_flares_it(self):
        s, br = hero("Skurmar", "Blast"), hero("Brennumar", "Sveda"); e = dummy(aff={"Eld": "weak"})
        b = fight([br, s], [e]); orders(b, {br.uid: (key(br, "Sveda"), e.uid)})
        orders(b, {})                                                    # 100%, then 50%: the fade's last step is next
        self.assertEqual(e.status["Scorched"]["step"], 2)
        blow = e.status["Scorched"]["dmg"]
        s.stages["ACC"], e.stages["EVA"] = 3, -3                         # a Blast that can't graze
        orders(b, {s.uid: (key(s, "Halvblast"), e.uid)})
        self.assertTrue(evs(b, "flare", unit=e.name))
        self.assertEqual(self.ticks(b, e)[-1], self.tick(blow, 0))       # fanned back to 100%, the same blow

    def test_lonnsveda_leaves_feeble_too(self):
        b, u, e = self.burning(dict(lonn=True))
        self.assertIn("Scorched", e.status); self.assertEqual(e.counter_name("ATK"), "Feeble 1")   # the weakness deepens the main status only

# ================================================================ riders on hits and taunts
class Riders(unittest.TestCase):
    def test_brakrosh_sunders_on_every_hit(self):
        v = hero("Vasara", ("Krosh", dict(lonn=True))); e = dummy(); b = fight([v], [e])
        orders(b, {v.uid: (key(v, "Brakrosh"), e.uid)})
        hit = evs(b, "hit", src=v.name)[0]
        self.assertEqual(e.stage("DEF"), 0 if hit["results"] == ["graze"] else -1)
        self.assertNotIn("May", plain(v.actions[1]))

    def test_lonnpeka_marks_and_sunders(self):
        def make(seed):
            u = hero("Ullar", ("Peka", dict(lonn=True))); e = dummy(); b = fight([u], [e], seed)
            orders(b, {u.uid: (key(u, "Genomskoda"), e.uid)}); return b, u, e
        b, u, e = land_until(make, lambda b, u, e: e.stage("EVA") < 0)
        self.assertEqual((e.counter_name("EVA"), e.counter_name("DEF")), ("Marked 1", "Sundered 1"))

    def test_lonnegga_blinds_the_taunted(self):
        v = hero("Vasara", ("Egga", dict(lonn=True))); e1, e2 = dummy(), dummy(); b = fight([v], [e1, e2])
        orders(b, {v.uid: (key(v, "Rodegga"), e1.uid)})
        self.assertEqual((e1.counter_name("ACC"), e2.counter_name("ACC")), ("Blinded 1", None))

# ================================================================ payoffs
class Payoffs(unittest.TestCase):
    def ratio(self, att, move, setup, new_game=True):
        """raw damage with the condition over without, the same attacker and target otherwise."""
        e = dummy(); b = Battle([att] if new_game else [birth("Ullar", SHEET_LEVEL, random.Random(1))], [e], random.Random(1))
        base = b.raw_damage(att, e, move); setup(b, e); return b.raw_damage(att, e, move) / base

    def test_pierce_finds_the_gaps(self):
        u = hero("Ullar", "Skott"); skott = u.actions[1]
        def sunder(b, e): e.stages["DEF"] = -2
        r = self.ratio(u, skott, sunder)
        self.assertAlmostEqual(r, (1 / stage_mult(-2)) * (1 + 2 * PIERCE_GAP))
        self.assertAlmostEqual(self.ratio(u, skott, sunder, new_game=False), 1 / stage_mult(-2))   # old fights: no gap
        krosh = hero("Vasara", "Krosh").actions[1]
        self.assertAlmostEqual(self.ratio(hero("Vasara", "Krosh"), krosh, sunder), 1 / stage_mult(-2))  # Crush: none

    def test_banskott_on_the_pinned(self):
        u = hero("Ullar", "Fangskott")
        def pin(b, e): b.apply_status(u, e, "Pinned", 1.0)
        self.assertAlmostEqual(self.ratio(u, u.actions[1], pin), 1.5)

    def test_banskott_lands_it_in_a_turn(self):
        """Same seed, same roll: the Pinned target takes exactly x1.5 (its Slowed cancelled, so the roll can't shift)."""
        dmg = []
        for pinned in (False, True):
            u = hero("Ullar", "Fangskott"); e = dummy(); b = fight([u], [e], seed=3)
            if pinned: e.status["Pinned"] = dict(rounds=2); e.stages["SPD"] = 1     # set, not rolled: the rng stays in step
            orders(b, {u.uid: (key(u, "Fangskott"), e.uid)}); dmg.append(evs(b, "hit", src=u.name)[0]["dmg"])
        self.assertAlmostEqual(dmg[1] / dmg[0], 1.5, delta=0.01)

    def test_avliva_under_half(self):
        u = hero("Ullar", "Avliva")
        def wound(b, e): e.hp = 0.49 * e.maxhp
        self.assertAlmostEqual(self.ratio(u, u.actions[1], wound), 2.0)

    def test_hevn_counts_hits_and_resets(self):
        v = hero("Vasara", "Hevn"); spears = [dummy(actions=[skill("Pierce", "Spear", "Base")]) for _ in range(3)]
        for s in spears: s.actions[0]["cost"] = 0
        b = fight([v], spears)
        orders(b, {})                                                    # she guards (First); three spears strike her
        n = len([x for x in evs(b, "hit", unit=v.name) if x["dmg"] > 0])
        self.assertEqual(v.hits_taken, n)
        self.assertAlmostEqual(b.payoff(v, spears[0], v.actions[1]), 1 + min(HEVN_CAP, HEVN_PER_HIT * n))
        v.hits_taken = 9; self.assertAlmostEqual(b.payoff(v, spears[0], v.actions[1]), 1 + HEVN_CAP)   # capped
        for s in spears: s.actions = [dict(a) for a in QUIET]
        orders(b, {v.uid: (key(v, "Hevn"), spears[0].uid)})
        self.assertEqual(v.hits_taken, 0)                                # her action came

    def test_bidhevn_releases_double(self):
        """Nov 20 (D09): double an equally primed Hevn; other Bid moves keep the grammar's x2.6."""
        a = compile_verb("Hevn", manners=("Bid",)); h = compile_verb("Hevn")
        self.assertEqual((a["name"], a["power"], a["bide"]), ("Bidhevn", 2 * h["power"], True))
        self.assertAlmostEqual(compile_verb("Krosh", manners=("Bid",))["power"], TIER_POWER["Base"] * MANNERS["Bid"]["power"])
        v = hero("Vasara", "Hevn", ("Hevn", dict(manners=("Bid",)))); e = dummy(); b = Battle([v], [e], random.Random(1))
        for n in (0, 1, 4, 9):
            v.hits_taken = n
            self.assertAlmostEqual(b.raw_damage(v, e, v.actions[2]) / b.raw_damage(v, e, v.actions[1]), 2.0)

# ================================================================ the status-move rules
class StatusMoves(unittest.TestCase):
    def test_styng_adds_a_hit_at_seventy_percent(self):
        u = hero("Ullar", ("Naglskott", dict(styng=True))); e = dummy(); b = fight([u], [e])
        orders(b, {u.uid: (key(u, "Genomskott"), e.uid)})
        hit = evs(b, "hit", src=u.name); self.assertEqual(len(hit), 1); self.assertEqual(hit[0]["element"], "Pierce")
        self.assertAlmostEqual(u.actions[1]["styng"], TIER_POWER["Base"] * STYNG_POWER * CLASS_SHARE["Ullar"])   # 70% of his base hit (Nov 21: ranged 0.75)

    def test_styngegga_strikes_the_taunted(self):
        v = hero("Vasara", ("Egga", dict(styng=True))); e = dummy(); b = fight([v], [e])
        orders(b, {v.uid: (key(v, "Daska"), e.uid)})
        self.assertEqual([x["unit"] for x in evs(b, "hit", src=v.name)], [e.name])
        self.assertEqual(e.taunted_by, None)                               # (it lasted the round)
        self.assertTrue(evs(b, "taunt"))

    def test_reyk_on_the_reyk_weak(self):
        """Always lands, a stack deeper, and the Bonus Round (classes.md Part 2), unless the target Guards
        (Battle_Refactor_Current D5, Nov 24: the dummy's quiet action is Defend)."""
        from words import compile_verb
        for guards in (False, True):
            u = hero("Brennumar", "Reyk")
            e = dummy(aff={"Reyk": "weak"}, **({} if guards else dict(actions=[compile_verb("Krosh", tier="Halv")])))
            b = fight([u], [e])
            for uid in b.awaiting(): b.submit(uid, key(u, "Reyk"), e.uid)
            b.commit()
            self.assertEqual(e.counter_name("ACC"), "Blinded 2")
            self.assertEqual(b.phase == "bonus", not guards, guards)

    def test_old_fights_keep_the_roll(self):
        u = birth("Brennumar", 30, random.Random(1)); u.actions = [status_spell("Blinded", "Base")]
        e = dummy(aff={"Reyk": "weak"}); b = Battle([u], [e], random.Random(1))
        self.assertFalse(b.status_weak(u, u.actions[0], e))

# ================================================================ movement and tempo
class Gliding(unittest.TestCase):
    """Skrida aims at a cell, like Move (Nov 20, Joseph): an empty cell, he steps there; an ally's, they trade places;
    Move's rules hold; Evasive either way."""
    def test_skrida_steps_to_a_cell_and_gains_nimble(self):
        u, v = hero("Ullar", "Skrida"), hero("Vasara", "Krosh"); b = fight([u, v], [dummy()])
        u.cell, v.cell = ("front", 0), ("front", 1)
        self.assertEqual((b.group_of(u, u.actions[1]), b.aim(u.actions[1])), (1, "cell"))   # Swift, aimed at a cell
        orders(b, {u.uid: (key(u, "Skrida"), ["rear", 2])})
        self.assertEqual((u.cell, u.counter_name("EVA")), (("rear", 2), "Evasive 1"))
        orders(b, {u.uid: (key(u, "Skrida"), ["front", 0])})                 # either way
        self.assertEqual((u.cell, u.counter_name("EVA")), (("front", 0), "Evasive 2"))

    def test_the_menu_offers_moves_cells(self):
        u, v = hero("Ullar", "Skrida"), hero("Vasara", "Krosh"); b = fight([u, v], [dummy()])
        sk = next(m for m in b.options(u.uid)["moves"] if m["name"] == "Skrida")
        self.assertEqual(sk["cells"], b.options(u.uid)["move"]["cells"])

    def test_merskrida_nimble_two(self):
        u = hero("Ullar", ("Skrida", dict(tier="Mer"))); v = hero("Vasara", "Krosh"); b = fight([u, v], [dummy()])
        orders(b, {u.uid: (key(u, "Merskrida"), ["rear", 2])}); self.assertEqual(u.counter_name("EVA"), "Evasive 2")

    def test_skrida_onto_an_ally_swaps(self):
        u, v = hero("Ullar", "Skrida"), hero("Vasara", "Krosh"); b = fight([u, v], [dummy()])
        cu, cv = u.cell, v.cell
        orders(b, {u.uid: (key(u, "Skrida"), list(cv))}); self.assertEqual((u.cell, v.cell), (cv, cu))

    def test_skrida_never_empties_the_front(self):
        """Move's rule: alone in the Front he can't be ordered behind it; ordered while it was legal, he holds the
        line when it lands (the Evasive still comes)."""
        u, d = hero("Ullar", "Skrida"), hero("Dagskald", "Sol"); b = fight([u, d], [dummy()])
        u.cell, d.cell = ("front", 0), ("rear", 1)
        with self.assertRaises(ValueError): b.submit(u.uid, key(u, "Skrida"), ["rear", 0])
        d.cell = ("front", 1); b.submit(u.uid, key(u, "Skrida"), ["rear", 0]); b.submit(d.uid, "guard")
        d.cell = ("rear", 1); b.commit()                                     # she stepped back before it landed
        self.assertEqual((u.cell, u.counter_name("EVA")), (("front", 0), "Evasive 1"))

    def test_skrida_is_held_by_a_pin(self):
        u, v = hero("Ullar", "Skrida"), hero("Vasara", "Krosh"); b = fight([u, v], [dummy()])
        cell = u.cell; b.submit(u.uid, key(u, "Skrida"), ["rear", 2]); b.submit(v.uid, "guard")
        b.apply_status(b.enemies[0], u, "Pinned", 1.0)
        hp = u.hp; b.commit()
        self.assertEqual((u.cell, u.hp), (cell, hp)); self.assertTrue(evs(b, "rooted"))   # held, and not paid

class Breathing(unittest.TestCase):
    def test_djupanda_winds_up_then_lands(self):
        u = hero("Brennumar", ("Anda", dict(manners=("Bid",)))); u.mp = 0; b = fight([u], [dummy()])
        orders(b, {u.uid: (key(u, "Djupanda"), None)})
        self.assertEqual(u.mp, 0); self.assertTrue(evs(b, "windup", unit=u.name))
        orders(b, {})
        self.assertAlmostEqual(u.mp, ANDA_SHARE * MANNERS["Bid"]["power"] * u.maxmp)   # Anda wound up (D8)
        self.assertIn("Patient", u.actions[1]["keywords"]); self.assertEqual(u.actions[1]["cost"], 0)

    def test_a_stun_breaks_the_breath(self):
        u = hero("Brennumar", ("Anda", dict(manners=("Bid",)))); u.mp = 0; b = fight([u], [dummy()])
        orders(b, {u.uid: (key(u, "Djupanda"), None)})
        u.status["Stunned"] = dict(rounds=3)
        orders(b, {}); self.assertEqual(u.mp, 0); self.assertTrue(evs(b, "bide_lost", unit=u.name))

class Standing(unittest.TestCase):
    def test_the_ullar_stands_in_the_rear(self):
        party = [build_hero(c) for c in ("Vasara", "Ullar", "Brennumar")]
        b = Battle(party, [dummy()], random.Random(1))
        self.assertEqual([u.cell[0] for u in party], ["front", "rear", "rear"])
        old = [birth(c, 30, random.Random(i)) for i, c in enumerate(("Vasara", "Ullar", "Brennumar"))]
        Battle(old, [dummy()], random.Random(1)); self.assertEqual(old[1].cell[0], "front")   # old recruits unchanged

# ================================================================ the AI plays the kits
class TheAIUsesThem(unittest.TestCase):
    def test_every_new_move_gets_used(self):
        """The starting three at leg 3, and a Brennumar with Sveda and Djupanda, against real rooms: each move of
        theirs that Wave 4a made playable is chosen at least once."""
        from composer import catalog, habitat, compose, place, spawn
        cat, seen = catalog(), set()
        want = {"Fangskott", "Genomskott", "Genomskoda", "Lamsveda", "Hevn"}     # Rodegga, Djupanda: below
        for i in range(40):
            rng = random.Random(500 + i)
            party = [build_hero(c, 3) for c in ("Vasara", "Ullar", "Brennumar")]
            foes = spawn(place(compose(rng, habitat(cat, ("Barrow", "Wildwood", "Rapids")[i % 3]))), ENEMY_LEVEL)
            b = Battle(party, foes, rng, events=True); b.fight()
            seen |= {e.get("move") for e in b.events if e["kind"] in ("act", "taunt", "windup", "hit") and e.get("unit") in [p.name for p in party]}
            seen |= {e.get("move") for e in b.events if e["kind"] == "intent" and e.get("side") == "party"}
            if want <= seen: break
        self.assertEqual(want - seen, set())

    def test_lonnegga_draws_a_hurt_allys_attacker(self):
        v, d = hero("Vasara", ("Egga", dict(lonn=True))), hero("Dagskald", "Sol"); d.hp = 0.3 * d.maxhp
        spear = dummy(actions=[skill("Pierce", "Spear", "Mer")]); b = Battle([v, d], [spear], random.Random(1))
        picks = [b.declare(v)[0]["name"] for _ in range(20)]
        self.assertIn("Rodegga", picks)

    def test_a_low_brennumar_breathes_deep(self):
        """Djupanda when the MP is low (D8: no Meditate; it's the breath he carries)."""
        u = hero("Brennumar", ("Anda", dict(manners=("Bid",)))); u.mp = 0.1 * u.maxmp
        b = Battle([u], [dummy(aff={"Eld": "null"})], random.Random(1))     # nothing to burn: it's MP or nothing
        picks = [b.declare(u)[0]["name"] for _ in range(20)]
        self.assertEqual(max(set(picks), key=picks.count), "Djupanda")

    def test_the_ullar_glides_out_of_the_front(self):
        u, d = hero("Ullar", "Skott", "Skrida"), hero("Dagskald", "Sol"); b = Battle([u, d], [dummy()], random.Random(1))
        u.cell, d.cell = ("front", 0), ("front", 1)
        picks = [b.declare(u)[0] for _ in range(20)]
        glides = [a for a in picks if a["name"] == "Skrida"]
        self.assertTrue(glides); self.assertTrue(all(a["cell"][0] == "rear" for a in glides))

if __name__ == "__main__": unittest.main()
