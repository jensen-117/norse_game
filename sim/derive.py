"""Encounter v0 -- attribute and derived-stat model (draft numbers)."""
import random

ATTRS = ["STR", "CON", "SPD", "DEX", "WIL", "INT", "WIS"]

# --- Genes -> attributes -------------------------------------------------
# Genes roll 0-31 per attribute. They set both the starting value and the
# growth rate, so good genes matter more the higher a character levels.
def attr_at(gene, level, growth_mult=1.0):
    start = 10 + gene / 2                      # level 1: 10 .. 25.5
    per_level = (0.6 + gene / 50) * growth_mult  # 0.6 .. 1.22 per level
    return start + (level - 1) * per_level

# --- Derived ("living") stats ---------------------------------------------
def hp(con, level):   return 20 + 2 * con + 2 * level
def mp(wis, level):   return 10 + wis + level

def level_factor(level):  # scales damage so fights stay ~4 hits at every level
    return 0.6 + level / 20

TIER_POWER = {"Halv": 10, "Base": 20, "Mer": 35, "Jatte": 55, "Ur": 80}

def damage(power, atk, dfn, level, affinity=1.0, stage_mult=1.0):
    return power * (atk / dfn) * level_factor(level) * affinity * stage_mult

def stage_mult(n):
    return (3 + n) / 3 if n >= 0 else 3 / (3 - n)

# --- A character ------------------------------------------------------------
PERSONALITY_BOOST, PERSONALITY_CUT = 1.1, 0.9   # applied to growth

def make_character(genes, level, boost=None, cut=None, sign=None):
    a = {}
    for k in ATTRS:
        g = PERSONALITY_BOOST if k == boost else PERSONALITY_CUT if k == cut else 1.0
        a[k] = attr_at(genes[k], level, g)
    if sign:  # +/- 10% of highest base attribute, flat, floor of 1
        up, down = sign
        shift = 0.10 * max(a.values())
        a[up] += shift
        a[down] = max(1, a[down] - shift)
    d = dict(HP=hp(a["CON"], level), MP=mp(a["WIS"], level),
             ATK=a["STR"], DEF=a["CON"], MAT=a["INT"], MDF=a["WIS"],
             ACC=a["DEX"], EVA=a["SPD"], SPD=a["SPD"])
    return a, d

if __name__ == "__main__":
    print("REFERENCE PEOPLE (all genes equal; no personality, no sign)\n")
    print(f"{'Level':>5} | {'gene 0':>18} | {'gene 15.5 (avg)':>18} | {'gene 31':>18}")
    print(f"{'':>5} | {'attr  HP   MP':>18} | {'attr  HP   MP':>18} | {'attr  HP   MP':>18}")
    for L in (1, 10, 25, 50, 75, 100):
        row = []
        for g in (0, 15.5, 31):
            a, d = make_character({k: g for k in ATTRS}, L)
            row.append(f"{a['CON']:5.0f} {d['HP']:4.0f} {d['MP']:4.0f}")
        print(f"{L:>5} | {row[0]:>18} | {row[1]:>18} | {row[2]:>18}")

    print("\nHITS TO DOWN AN EQUAL (average attacker vs average defender)\n")
    print(f"{'Level':>5} | " + " | ".join(f"{t:>6}" for t in TIER_POWER))
    for L in (1, 10, 25, 50, 75, 100):
        a, d = make_character({k: 15.5 for k in ATTRS}, L)
        cells = []
        for t, p in TIER_POWER.items():
            dmg = damage(p, d["MAT"], d["MDF"], L)
            cells.append(f"{d['HP'] / dmg:6.1f}")
        print(f"{L:>5} | " + " | ".join(cells))

    print("\nSTAGES vs GEAR (DEF multiplier -> damage taken)")
    for n in (-2, -1, 1, 2, 3, 5):
        m = stage_mult(n)
        print(f"  stage {n:+d}: DEF x{m:.2f} -> damage taken x{1/m:.2f}")

    print("\nA ROLLED NPC (seed 7), level 10, Brave (+STR/-SPD), sign Bauta-style (+CON/-SPD)")
    rng = random.Random(7)
    genes = {k: rng.randint(0, 31) for k in ATTRS}
    a, d = make_character(genes, 10, boost="STR", cut="SPD", sign=("CON", "SPD"))
    print("  genes:", genes)
    print("  attrs:", {k: round(v) for k, v in a.items()})
    print("  derived:", {k: round(v) for k, v in d.items()})
