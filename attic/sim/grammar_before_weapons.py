"""The word compiler (spellbook Part 2, Martial Grammar).

A word is [Target] + [Tier] + [Manner] + [Rider] + Root, at most one of each. Every morpheme is a row of data
that modifies the move, so any legal word compiles into a full move (power, cost, speed group, crit, hits,
riders, reach) without hand-typing. `assess()` builds every word and scores it, so the grammar can tell us
which combinations are worth printing and which are broken before a class tree picks them.

    compile_word("Kross", tier="Mer", rider="Eitr")      -> Mereitrkross, a greater poisoned crush
    compile_word("Skott", target="Flok")                 -> Flokskott, shown to the player; "Volley" when a skeleton uses it
"""
from itertools import product
from data import *
from engine import join_morphemes, act, level_factor

# ---------------------------------------------------------------- morphemes (all tune knobs live here)
WEAPON = {   # root: (damage type, reach override)
    "Skar": ("Slash", None), "Kross": ("Crush", None), "Spett": ("Pierce", None), "Skott": ("Pierce", "any"),
}
SPELL_ROOTS = [r for r in ELEMENT if r not in MARTIAL and r != "Lak"]

TARGETS = {
    None:   dict(),
    "Flok": dict(shape="row", cost=1.5),                         # per-target x0.75 comes from SHAPE_MULT
    "All":  dict(all=True, cost=ALL_COST_MULT),                  # per-target x0.75 comes from ALL_POWER_MULT
    "Mark": dict(spot=True),     # targets space: a painted spot (DoT for N rounds), or with Bid a one-shot on the spot.
}                                # Compiled and named, not yet simulated (parked until the playable board).
MANNERS = {
    None:    dict(),
    "Snar":  dict(group=1, power=0.9),
    "Tung":  dict(group=-2, power=1.2),
    "Bid":   dict(bide=True, power=2.6),     # two rounds: wind up, then locked while it fires; lost if broken
    "Jarf":  dict(power=0.7, cost=1.5, crit_bonus=0.20, crit_mult=3.0),   # 5% base + 20% = 25% crit
    "Drif":  dict(flurry=dict(per=0.5, max=4, p=0.5, step=0.10)),
}
RIDERS = {   # rider morpheme -> status; a rider strike deals RIDER_POWER and rolls the tier's status-line chance
    None: None, "Eitr": "Poisoned", "Blot": "Bleeding", "Mogl": "Disarmed",
    "Blinda": "Blinded", "Ogn": "Feared", "Nid": "Cursed",
}
RIDER_POWER = 0.7
HALV_MANNER_COST = 4      # a manner on the free Halv costs a flat 4 (x the manner's cost mult): manners are never free

# ---------------------------------------------------------------- plain English, for enemies (diegetic display)
EN_ROOT = {"Skar": "Cut", "Kross": "Smash", "Spett": "Thrust", "Skott": "Shot",
           "Eld": "Fire", "Reyk": "Smoke", "Vatn": "Water", "Hrim": "Frost", "Blast": "Wind", "Blixt": "Lightning",
           "Jord": "Stone", "Gro": "Thorn", "Sol": "Sunlight", "Natt": "Shadow", "Aska": "Ash"}
EN_PLURAL = {"Cut": "Cuts", "Smash": "Smashes", "Thrust": "Thrusts", "Shot": "Shots"}
EN_TIER = {"Halv": "Light", "Base": "", "Mer": "Great", "Jatte": "Giant", "Ur": "Primal"}
EN_MANNER = {"Snar": "Swift", "Tung": "Heavy", "Bid": "Patient", "Jarf": "Reckless"}
EN_RIDER = {"Eitr": "Venom", "Blot": "Bleeding", "Mogl": "Disarming", "Blinda": "Blinding", "Ogn": "Dread", "Nid": "Cursing"}
EN_TARGET = {"Flok": "Sweeping", "All": "Storm of", "Mark": "Marked"}
EN_OVERRIDE = {"Flokskott": "Volley", "Allskott": "Arrow Rain", "Halvskar": "Slash", "Halvkross": "Bash",
               "Halvspett": "Jab", "Halvskott": "Loose"}

def english(root, tier, target, manner, rider):
    word = name_of(root, tier, target, manner, rider)
    if word in EN_OVERRIDE: return EN_OVERRIDE[word]
    noun = EN_ROOT[root]
    if manner == "Drif":
        noun = f"Flurry of {EN_PLURAL[noun]}" if noun in EN_PLURAL else f"{noun} Flurry"
    parts = [EN_TARGET.get(target, ""), EN_TIER[tier], EN_MANNER.get(manner, ""), EN_RIDER.get(rider, ""), noun]
    if target == "All": parts = [p for p in parts if p != "Storm of"] + ["Storm"]
    return " ".join(p for p in parts if p)

def name_of(root, tier="Base", target=None, manner=None, rider=None):
    return join_morphemes([p for p in (target, None if tier == "Base" else tier, manner, rider, root) if p])

# ---------------------------------------------------------------- the compiler
def compile_word(root, tier="Base", target=None, manner=None, rider=None):
    t, m = TARGETS[target], MANNERS[manner]
    martial = root in WEAPON
    if martial:
        dtype, reach = WEAPON[root]
        base_cost, cost_type = TIER_COST[tier], "HP"
    else:
        dtype, reach = root, None
        base_cost, cost_type = (0 if tier == "Halv" else TIER_COST[tier] * ELEMENT[root]["cost"]), "MP"
    power = TIER_POWER[tier] * m.get("power", 1.0) * (RIDER_POWER if rider else 1.0)
    if tier == "Halv" and manner: base_cost = HALV_MANNER_COST
    cost = base_cost * t.get("cost", 1.0) * m.get("cost", 1.0)
    a = act("damage", name_of(root, tier, target, manner, rider), element=dtype, tier=tier,
            all=t.get("all", False), cost=round(cost), cost_type=cost_type, power=power,
            status=RIDERS[rider])
    a["english"] = english(root, tier, target, manner, rider)
    a["parts"] = dict(root=root, tier=tier, target=target, manner=manner, rider=rider)
    if reach: a["reach"] = reach
    if "shape" in t: a["shape"] = t["shape"]
    if t.get("spot"): a["spot"] = True
    for k in ("group", "bide", "crit_bonus", "crit_mult"):
        if k in m: a[k] = m[k]
    if "flurry" in m: a["flurry"] = dict(m["flurry"])
    return a

def words(roots=None, tiers=TIERS, targets=[t for t in TARGETS if t != "Mark"], manners=MANNERS, riders=RIDERS):
    for root, tier, tg, mn, rd in product(roots or list(WEAPON), tiers, targets, manners, riders):
        yield compile_word(root, tier, tg, mn, rd)

# ---------------------------------------------------------------- assessment
def flurry_hits(f, net=0):
    """Expected number of hits for a coin-flip chain (the first always lands)."""
    p = max(0.05, min(0.95, f["p"] + f["step"] * net)); n, reach = 0.0, 1.0
    for _ in range(f["max"]):
        n += reach; reach *= p
    return n

def roll_ev(a, net=0):
    graze = max(0.0, GRAZE_BASE - STEP * net)
    crit = CRIT_BASE + max(0, net - 2) * 0.05 + a.get("crit_bonus", 0.0)
    return graze * GRAZE_MULT + crit * a.get("crit_mult", CRIT_MULT) + (1 - graze - crit)

def ev(a, net=0):
    """Expected damage per target, in power points, before ATK/DEF and affinity."""
    e = a["power"] * ELEMENT[a["element"]]["power"] * ELEMENT[a["element"]]["hits"] * roll_ev(a, net)
    if a.get("flurry"): e *= a["flurry"]["per"] * flurry_hits(a["flurry"], net)
    if a["all"]: e *= ALL_POWER_MULT
    elif a.get("shape"): e *= SHAPE_MULT[a["shape"]]
    return e

def assess(roots=None, tiers=TIERS):
    """Score every word against the plain move of the same root, tier and target (no manner, no rider)."""
    rows = []
    for a in words(roots, tiers):
        p = a["parts"]
        plain = compile_word(p["root"], p["tier"], p["target"])
        e, e0 = ev(a), ev(plain)
        flags = []
        free = a["cost"] == 0 and p["tier"] != "Ur"          # Ur's cost lives on the gear
        if free and e > e0 * 1.001 and p["manner"]:
            flags.append("free upgrade over the plain Halv")
        if a["cost"] and plain["cost"] and (e / a["cost"]) > (e0 / plain["cost"]) * 1.15 and not a.get("bide"):
            flags.append("more damage per point of cost than the plain move")
        if p["manner"] == "Bid" and free:
            flags.append("free bide")
        rows.append(dict(word=a["name"], english=a["english"], cost=a["cost"], cost_type=a["cost_type"],
                         group=a.get("group", 0), ev=e, vs_plain=e / e0 if e0 else 0, status=a["status"],
                         bide=bool(a.get("bide")), flags=flags, parts=p))
    return rows

if __name__ == "__main__":
    import sys
    for w in [("Kross", "Mer", None, None, "Eitr"), ("Skott", "Base", "Flok", None, None),
              ("Kross", "Base", None, "Jarf", None), ("Skar", "Jatte", "Flok", "Drif", None),
              ("Skott", "Jatte", None, "Bid", None), ("Eld", "Base", None, "Bid", None),
              ("Kross", "Mer", "All", None, "Mogl")]:
        a = compile_word(*w)
        print(f"{a['name']:<22} {a['english']:<32} power {a['power']:5.1f}  cost {a['cost']:>3} {a['cost_type']}"
              f"  group {a.get('group', 0):+d}  ev {ev(a):5.1f}  status {a['status']}")
    rows = assess()
    print(f"\n{len(rows)} martial words compiled.")
    from collections import Counter
    flagged = [r for r in rows if r["flags"]]
    print(f"{len(flagged)} flagged:", dict(Counter(f for r in flagged for f in r["flags"])))
    print("\nSingle-target Kross by manner: expected damage (cost)")
    print(f"  {'':<7}" + "".join(f"{t:>14}" for t in TIERS))
    for mn in MANNERS:
        print(f"  {str(mn or 'plain'):<7}" + "".join(f"{ev(compile_word('Kross', t, None, mn)):>8.1f} ({compile_word('Kross', t, None, mn)['cost']:>2})" for t in TIERS))
    print("\nFlagged, plain single-target words only:")
    for r in flagged:
        if r["parts"]["target"] is None and r["parts"]["rider"] is None and r["parts"]["root"] == "Kross":
            print(f"  {r['word']:<16} x{r['vs_plain']:.2f} of plain, cost {r['cost']}: {'; '.join(r['flags'])}")
