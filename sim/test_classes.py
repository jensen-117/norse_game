"""Wave 3: class sheets, build_hero, Meditate and Egga, tested in complete turns."""
import random, unittest
from engine import *

def fight(party, enemies, seed=1):
    b = Battle(party, enemies, random.Random(seed), events=True); b.begin("party"); return b

def orders(b, plan):
    """plan: {uid: (key, target)}; everyone else guards."""
    for uid in b.awaiting(): b.submit(uid, *plan.get(uid, ("guard", None)))
    b.commit()

def dummy(job="Spear", hp=10 ** 6, **kw):
    e = spawn_family("Drattr", "Drattr", SHEET_LEVEL, job=job); e.maxhp = e.hp = hp
    for k, v in kw.items(): setattr(e, k, v)
    return e

class Sheets(unittest.TestCase):
    def test_fixed_and_deterministic(self):
        a, b = build_hero("Vasara", 1), build_hero("Vasara", 1)
        self.assertEqual(a.attrs, b.attrs); self.assertEqual(a.level, SHEET_LEVEL)

    def test_affinities(self):
        self.assertEqual(build_hero("Brennumar").aff, build_aff(**SCHOOL_AFFINITY["Eld"]))
        u = build_hero("Ullar"); self.assertEqual((u.affinity("Slash"), u.affinity("Eld"), u.affinity("Hrim")), ("weak", "weak", "resist"))
        v = build_hero("Vasara"); self.assertEqual((v.affinity("Pierce"), v.affinity("Blixt"), v.affinity("Eld")), ("weak", "weak", "resist"))

    def test_kits_priced_and_unfinished_moves_listed(self):
        for cls in KITS:
            for leg in KITS[cls]:
                u = build_hero(cls, leg)
                self.assertEqual(u.actions[0]["tier"], "Halv"); self.assertEqual(u.actions[0]["cost"], 0)   # the free basic
                for a in u.actions[1:]:
                    if a["share"]: self.assertGreater(a["cost"], 0, a["name"])
                    self.assertEqual(a["unresolved"], [], a["name"])
                full = build_hero(cls, leg, playable=False)
                self.assertEqual({n for n, _ in u.excluded}, {a["name"] for a in full.actions if a["unresolved"]})

    def test_an_unplayable_kit_is_refused_by_battle(self):
        u = build_hero("Ullar", 1, playable=False)              # Naglskott: Pinned has no row yet
        with self.assertRaises(ValueError): Battle([u], [dummy()], random.Random(1))

    def test_bows_reach_anywhere_hammers_dont(self):
        self.assertEqual(build_hero("Ullar").actions[1]["reach"], "any")
        self.assertEqual(build_hero("Vasara").actions[1]["reach"], "melee")

    def test_no_free_cover_for_others(self):
        u = build_hero("Ullar"); b = fight([u, build_hero("Vasara")], [dummy()])
        self.assertFalse(any(m["kind"] == "cover" for m in b.slots(u)[1]))

class Meditating(unittest.TestCase):
    def test_restores_its_share(self):
        u = build_hero("Brennumar"); u.mp = 0
        b = fight([u], [dummy(actions=[act("defend", "Defend", target="self")])])
        orders(b, {u.uid: ("meditate", None)})
        self.assertEqual(u.mp, MEDITATE_SHARE * u.maxmp)

    def test_an_ordered_meditate_is_obeyed(self):
        """At full MP the AI would never meditate: the order must stand, not be re-decided (found in the browser)."""
        u = build_hero("Dagskald"); b = fight([u], [dummy(actions=[act("defend", "Defend", target="self")])])
        orders(b, {u.uid: ("meditate", None)})
        self.assertTrue(any(e["kind"] == "mp" and e.get("move") == "Meditate" for e in b.events))
        self.assertFalse(any(e["kind"] in ("act", "heal") and e.get("unit") == u.name for e in b.events))

    def test_magicals_only(self):
        v = build_hero("Vasara"); b = fight([v], [dummy()])
        self.assertNotIn("meditate", b.options(v.uid))
        with self.assertRaises(ValueError): b.submit(v.uid, "meditate")

    def test_the_ai_meditates_when_low(self):
        u = build_hero("Dagskald"); u.mp = 0
        b = Battle([u], [dummy(actions=[act("defend", "Defend", target="self")])], random.Random(2), events=True)
        b.fight(max_rounds=3)
        self.assertTrue(any(e["kind"] == "mp" and e.get("move") == "Meditate" for e in b.events))

class Taunting(unittest.TestCase):
    def setup(self, rear_target=False):
        v, d = build_hero("Vasara"), build_hero("Dagskald")
        b = fight([v, d], [dummy(job="Spear")])
        e = b.enemies[0]; e.actions = [skill("Pierce", "Spear", "Base")]; e.actions[0]["cost"] = 0; e.actions[0]["reach"] = "reach"
        return b, v, d, e

    def test_egga_draws_a_single_target_attack(self):
        b, v, d, e = self.setup()
        b.intents = {}
        b.remaining = [(k, u, ((e.actions[0], d) if u is e else x)) for k, u, x in b.remaining]   # the foe aims at the healer
        orders(b, {v.uid: ("m2", None)})                       # Egga
        hits = [x for x in b.events if x["kind"] == "hit" and x.get("src") == e.name]
        self.assertTrue(hits); self.assertTrue(all(h["unit"] == v.name for h in hits))
        self.assertTrue(any(x["kind"] == "drawn" for x in b.events))
        self.assertEqual(d.hp, d.maxhp)

    def test_it_acts_first_and_costs_hp(self):
        b, v, d, e = self.setup()
        egga = v.actions[2]; self.assertEqual(egga["name"], "Egga")
        self.assertEqual(b.group_of(v, egga), 3); self.assertEqual(egga["cost_type"], "HP"); self.assertGreater(egga["cost"], 0)

    def test_all_moves_are_not_drawn(self):
        b, v, d, e = self.setup()
        sweep = skill("Pierce", "Sweep", "Base", all_=True); sweep["cost"] = 0; sweep["reach"] = "any"
        e.actions = [sweep]
        b.remaining = [(k, u, ((sweep, None) if u is e else x)) for k, u, x in b.remaining]
        orders(b, {v.uid: ("m2", None)})
        self.assertLess(d.hp, d.maxhp)                         # the All-move still reaches the healer

    def test_it_lasts_one_round(self):
        b, v, d, e = self.setup()
        orders(b, {v.uid: ("m2", None)})
        self.assertFalse(v.taunting)

if __name__ == "__main__": unittest.main()
