"""The mirror (Nov 23, beinar_pilot Part 2 section 8): packs reserve reach slots within their budget."""
import random, unittest
from collections import Counter
from composer import catalog, habitat, compose, mirror, reach_slots, shaped_room, tier_of, CALIB_PLACES

CAT = catalog()

class TheMirror(unittest.TestCase):
    def test_slots(self):
        self.assertEqual([reach_slots(n) for n in range(1, 7)], [1, 1, 1, 2, 2, 2])

    def test_a_swap_keeps_price_and_shape(self):
        pool = habitat(CAT, "Barrow")
        for seed in range(300):
            rng = random.Random(seed)
            before = compose(rng, pool)
            after = mirror(random.Random(seed), before, pool)
            self.assertEqual(sorted((e["cost"], tier_of(e)) for e in before), sorted((e["cost"], tier_of(e)) for e in after))

    def test_most_rooms_reach_and_some_are_brutes(self):
        met = Counter()
        for n in range(600):
            rng = random.Random(n)
            room = [e for _, _, e in shaped_room(rng, CAT, CALIB_PLACES[n % 3], ("fodder", "elite", "boss")[n % 3], 4, None, mirrored=True)]
            if all(tier_of(e) == "Trash" for e in room): continue
            met[sum(e["ranged"] for e in room) >= reach_slots(len(room))] += 1
        self.assertGreater(met[True] / sum(met.values()), 0.9)            # a brute room may still roll an archer

    def test_brute_rooms(self):
        pool = habitat(CAT, "Barrow"); brutes = 0
        for n in range(800):
            log = []
            picks = [e for e in compose(random.Random(n), pool) if tier_of(e) != "Trash"] or compose(random.Random(n), pool)
            if all(tier_of(e) == "Trash" for e in picks): continue
            mirror(random.Random(n + 10_000), picks, pool, log)
            brutes += any("brute" in x for x in log)
        self.assertTrue(60 < brutes < 150, brutes)                         # about 1 in 8

    def test_old_rooms_are_untouched(self):
        for n in range(50):
            a = shaped_room(random.Random(n), CAT, "Barrow", "elite", 4)
            b = shaped_room(random.Random(n), CAT, "Barrow", "elite", 4, mirrored=False)
            self.assertEqual([(r, l, e["rank"], e["element"]) for r, l, e in a], [(r, l, e["rank"], e["element"]) for r, l, e in b])

    def test_compose_takes_it_as_a_rule(self):
        log = []
        compose(random.Random(3), habitat(CAT, "Wildwood"), dict(ranged="mirror"), log)
        self.assertTrue(all(isinstance(x, str) for x in log))

if __name__ == "__main__":
    unittest.main()
