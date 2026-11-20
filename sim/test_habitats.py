"""Habitats, the ranged rule, and the Mogel's slime paint: python3 -m unittest test_habitats -v"""
import random, unittest
import engine
from engine import *
from composer import catalog, habitat, compose, place, spawn, HABITATS
from test_board import hero

CAT = catalog()

class Habitats(unittest.TestCase):
    def test_home_families_and_guests(self):
        pool = habitat(CAT, "Barrow")
        fams = {e["family"] for e in pool}
        self.assertEqual(fams, {"Draugr", "Bein", "Ande", "Mogel"})
        self.assertTrue(all(e["element"] in ("Natt", "Aska") for e in pool if e["family"] in ("Ande", "Mogel")))

    def test_ranged_include_and_exclude(self):
        rng = random.Random(1)
        for hab in HABITATS:
            pool = habitat(CAT, hab)
            for _ in range(100):
                self.assertTrue(any(e["ranged"] for e in compose(rng, pool, dict(ranged="include"))))
                self.assertFalse(any(e["ranged"] for e in compose(rng, pool, dict(ranged="exclude"))))

    def test_ranged_tag_matches_the_kits(self):
        tag = {(e["family"], e["rank"]): e["ranged"] for e in CAT if e["family"] not in ("Ande", "Mogel")}
        self.assertFalse(tag[("Draugr", "Halvdraugr")]); self.assertTrue(tag[("Draugr", "Gandraugr")])
        self.assertTrue(tag[("Bein", "Halvbeinorv")]); self.assertFalse(tag[("Bein", "Beinbryn")])
        self.assertFalse(tag[("Djur", "Forndjur")])

    def test_physical_packs_spawn_and_fight(self):
        rng = random.Random(2)
        for hab in HABITATS:
            foes = spawn(place(compose(rng, habitat(CAT, hab))), 30)
            self.assertTrue(all(hasattr(u, "cell") for u in foes))
            Battle([hero("Hersir", rng)], foes, rng).fight()

class Paint(unittest.TestCase):
    def setUp(self): engine.USE_BOARD = engine.USE_ROTATION = True; self.rng = random.Random(3)

    def mogel(self):
        m = spawn_mogel("Mogel", "Eld", 30); m.cell = ("front", 0); return m

    def test_mogel_ranks_carry_the_paint(self):
        names = [a["name"] for a in mogel_kit("Stor", "Vatn")]
        self.assertIn("Markmervatn", names)
        self.assertFalse(any(a.get("spot") for a in mogel_kit("Litel", "Vatn")))
        self.assertFalse(any(a.get("spot") for a in mogel_kit("Mogel", "Lak")))

    def test_paint_hits_now_then_ticks(self):
        h = hero("Brennumar", self.rng); m = self.mogel(); b = Battle([h], [m], self.rng)
        paint = next(a for a in m.actions if a.get("spot"))
        hp0 = h.hp; b.eligible, b.barred = set(), set()
        b.resolve(m, paint, h, False)
        self.assertLess(h.hp, hp0, "whoever stands there is hit when it lands")
        hp1 = h.hp; b.tick_spots()
        self.assertLess(h.hp, hp1, "and again at the start of the next round")
        self.assertEqual(b.spots[("party", h.cell)]["rounds"], SPOT_ROUNDS - 1)

    def test_paint_ignores_affinity_and_cover(self):
        h = hero("Brennumar", self.rng); m = self.mogel(); b = Battle([h], [m], self.rng)
        h.aff = {"Eld": "absorb"}
        paint = next(a for a in m.actions if a.get("spot"))
        hp0 = h.hp; b.eligible, b.barred = set(), set()
        b.resolve(m, paint, h, False)
        self.assertLess(h.hp, hp0)

    def test_stepping_off_ends_the_ticks(self):
        h = hero("Brennumar", self.rng); m = self.mogel(); b = Battle([h], [m], self.rng)
        paint = next(a for a in m.actions if a.get("spot"))
        b.eligible, b.barred = set(), set(); b.resolve(m, paint, h, False)
        opts = [o for o in b.board_options(h, 40) if o[1]["name"] == "Step off"]
        self.assertTrue(opts)
        b.resolve(h, opts[0][1], h, False)
        hp1 = h.hp; b.tick_spots()
        self.assertEqual(h.hp, hp1)

    def test_one_paint_per_target_per_round(self):
        h = hero("Brennumar", self.rng); m1, m2 = self.mogel(), spawn_mogel("Mogel", "Eld", 30)
        m2.cell = ("front", 1); b = Battle([h], [m1, m2], self.rng)
        b.paint_claims = {h}
        for m in (m1, m2):
            paint = next(a for a in m.actions if a.get("spot"))
            m.actions = [paint]
            a, t = b.declare(m)
            self.assertFalse(a.get("spot") and t is h)

if __name__ == "__main__":
    unittest.main()
