"""The encounter composer: fills a slot budget from a tagged catalog of enemies.

How a pack is rolled (Joseph's d3 machine, generalised):
  1. Gates narrow the catalog: family, element, school, rank, art-only, or any tag. A biome is just a
     named gate ("Eldhall": elements Eld and Reyk).
  2. While budget remains: list the costs (1, 2, 3) that still FIT -- cost <= remaining budget, a unit
     of that cost survives the gates, the rules allow it, and what would be left can still be filled
     exactly. Roll among those costs (the d3, with any impossible faces removed). Then pick a unit of
     that cost from the gated catalog (weighted).
  3. Rules are toggles: banned costs ("no 1-costs"), per-cost caps ("only one 3-cost"), a unit cap
     (never more than the 6 board cells), family minimums/maximums, per-family weights.
  4. Placement: front-liners (Mogel) take the Front row, casters (Ande) the Rear; overflow spills to
     the other row. Cells are 3 lanes x (Front, Rear).
Rolling the COST first and the unit second keeps big units appearing even when the gated pool holds
many small ones; rolling units directly would drown the 3-costs.
"""
import random
from functools import lru_cache
from data import SPIRIT_RANKS, MOGEL_RANKS, SCHOOL_OF, FAMILIES, MARTIAL, BEINSEIDR_ELEMENTS, rank_rows, strike_range

# ---------------------------------------------------------------- catalog
ELEMENTS = ["Eld", "Reyk", "Vatn", "Hrim", "Blast", "Blixt", "Jord", "Gro", "Sol", "Lak", "Natt", "Aska"]
ART = {("Ande", "Halv"), ("Ande", "Ande"), ("Mogel", "Halv"), ("Mogel", "Litel"), ("Mogel", "Mogel")}
ROLE = {"Ande": "rear", "Mogel": "front"}

PHYSICAL = ["Draugr", "Bein", "Drattr", "Djur"]      # the folklore families: no element, a habitat instead
PHYSICAL_ART = {"Draugr", "Bein", "Drattr"}           # in Res64 (art_res64/undead; the Drattr from Joseph's drattr_1, Nov 9)

def kit_reaches_rear(moves, weapon=None):
    """A unit is 'ranged' when one of its damage moves can hit our Rear from anywhere: a spell, a bow, a throw."""
    for m in moves:
        if m[0] in ("spell", "ur"): return True
        if m[0] == "strike" and strike_range(m, weapon) == "Long": return True
    return False

def physical_role(moves, weapon=None):
    dmg = [m for m in moves if m[0] in ("strike", "spell", "ur")]
    melee = sum(m[0] == "strike" and strike_range(m, weapon) != "Long" for m in dmg)     # archers keep back
    return "front" if melee * 2 >= len(dmg) and melee else "rear"

def catalog():
    out = []
    for fam, ranks in (("Ande", SPIRIT_RANKS), ("Mogel", MOGEL_RANKS)):
        for rank, r in ranks:
            for el in ELEMENTS:
                out.append(dict(family=fam, rank=rank, element=el, school=SCHOOL_OF[el], cost=r["cost"],
                                role=ROLE[fam], art=(fam, rank) in ART, weight=1.0, ranged=True))
    for fam in PHYSICAL:
        for r in rank_rows(fam):
            moves = r["moves"]
            els = BEINSEIDR_ELEMENTS if any("@" in m for m in moves) else [None]   # element-adopting ranks
            for el in els:
                out.append(dict(family=fam, rank=r["name"], job=r["job"], type=r["type"], element=el,
                                school=SCHOOL_OF.get(el), cost=r["cost"],
                                role=r["opts"].get("role") or physical_role(moves, r["opts"].get("weapon")),
                                art=fam in PHYSICAL_ART, weight=1.0 / len(els),
                                ranged=kit_reaches_rear(moves, r["opts"].get("weapon"))))
    return out

HABITATS = {   # where the folklore families live, and which Ande and Mogel flavours visit (Joseph, Nov 7)
    "Barrow":   dict(families=["Draugr", "Bein"], element=["Natt", "Aska"]),
    "Wildwood": dict(families=["Djur"], element=["Gro", "Jord"]),
    "Rapids":   dict(families=["Drattr"], element=["Vatn", "Hrim"]),
}
GUEST_WEIGHT = 0.10     # each Ande or Mogel entry in a habitat, against 1.0 for a home family's entry (tune)

def habitat(cat, name, art_only=False):
    """A habitat gate: its home families at any rank, plus Ande and Mogel of its elements as guests."""
    h = HABITATS[name]; out = []
    for e in cat:
        if art_only and not e["art"]: continue
        if e["family"] in h["families"]:
            if e["element"] is None or e["element"] in h["element"]: out.append(e)    # a Beinseidr of the place
        elif e["family"] in ("Ande", "Mogel") and e["element"] in h["element"]:
            out.append(dict(e, weight=e["weight"] * GUEST_WEIGHT))
    return out

BIOMES = {   # a biome is a named gate; elements come in school pairs, plus a neighbour now and then
    "Eldhall":   dict(element=["Eld", "Reyk"]),
    "Vatnhall":  dict(element=["Vatn", "Hrim"]),
    "Blasthall": dict(element=["Blast", "Blixt"]),
    "Jordhall":  dict(element=["Jord", "Gro"]),
    "Solhall":   dict(element=["Sol", "Lak"]),
    "Natthall":  dict(element=["Natt", "Aska"]),
    "Mire":      dict(element=["Jord", "Gro", "Vatn"]),          # mould country: Mogel heavy
    "Ashfield":  dict(element=["Eld", "Reyk", "Aska"]),
}

def roll_biome(rng, names=None):
    """The freeform roll: pick a biome, which is just a named element gate."""
    name = rng.choice(names or list(BIOMES))
    return name, dict(BIOMES[name])

# ---------------------------------------------------------------- gates and rules
def gate(cat, **g):
    """Keep entries whose field is in the given list (or equals the value). art_only=True keeps drawn units."""
    out = []
    for e in cat:
        if g.get("art_only") and not e["art"]: continue
        ok = True
        for k, v in g.items():
            if k == "art_only": continue
            vals = v if isinstance(v, (list, tuple, set)) else [v]
            if e.get(k) not in vals: ok = False; break
        if ok: out.append(e)
    return out

DEFAULT_RULES = dict(budget=6, max_units=6, banned_costs=(), cost_caps={}, family_max={}, family_min={},
                     family_weight={}, ranged=None)   # ranged: "include" (at least one unit that reaches our Rear),
                                                      # "exclude" (none: the pure-melee pack), None (whatever rolls)

def _fillable(remaining, costs, caps, units_left):
    """Can `remaining` be met exactly with the allowed costs, the caps and the unit limit?"""
    costs = tuple(sorted(costs)); caps = tuple(sorted(caps.items()))
    return _fill(remaining, costs, caps, units_left)

@lru_cache(maxsize=None)
def _fill(remaining, costs, caps, units_left):
    if remaining == 0: return True
    if units_left <= 0: return False
    capd = dict(caps)
    for c in costs:
        if c > remaining or capd.get(c, 99) <= 0: continue
        nxt = dict(capd)
        if c in nxt: nxt[c] -= 1
        if _fill(remaining - c, costs, tuple(sorted(nxt.items())), units_left - 1): return True
    return False

class CompositionError(Exception): pass

@lru_cache(maxsize=None)
def _feas(remaining, types, caps, units_left, counts, maxes, mins):
    """Can `remaining` be met exactly from these (cost, family) types under the cost caps, the unit limit and the family
    rules (review C07)? A family is None when no rule names it, so with no family rules this is _fill."""
    cnt = dict(counts)
    if remaining == 0: return all(cnt.get(f, 0) >= m for f, m in mins)
    if units_left <= 0: return False
    capd, mx = dict(caps), dict(maxes)
    for c, f in types:
        if c > remaining or capd.get(c, 99) <= 0: continue
        if f is not None and cnt.get(f, 0) >= mx.get(f, 99): continue
        nc = dict(capd)
        if c in nc: nc[c] -= 1
        n2 = dict(cnt)
        if f is not None: n2[f] = n2.get(f, 0) + 1
        if _feas(remaining - c, types, tuple(sorted(nc.items())), units_left - 1, tuple(sorted(n2.items())), maxes, mins):
            return True
    return False

def compose(rng, pool, rules=None, log=None, tries=200):
    """Roll one pack. Returns a list of catalog entries, in roll order.
    The ranged rule: "exclude" gates out every unit that reaches our Rear; "include" re-rolls until the
    pack has one (if the pool holds no ranged unit at all, it raises)."""
    R = dict(DEFAULT_RULES); R.update(rules or {})
    if R["ranged"] == "exclude":
        pool = [e for e in pool if not e["ranged"]]
    if R["ranged"] == "include":
        if not any(e["ranged"] for e in pool):
            raise CompositionError("ranged: include, but nothing in the pool reaches the Rear")
        for _ in range(tries):
            picks = compose(rng, pool, dict(R, ranged=None), log)
            if any(e["ranged"] for e in picks): return picks
            if log is not None: log.append("re-roll: no ranged unit")
        raise CompositionError(f"no ranged pack in {tries} rolls")
    caps = dict(R["cost_caps"])
    fam_count = {}
    picks, remaining = [], R["budget"]
    def live_pool():
        p = []
        for e in pool:
            if e["cost"] in R["banned_costs"]: continue
            if fam_count.get(e["family"], 0) >= R["family_max"].get(e["family"], 99): continue
            p.append(e)
        return p
    def need_min():   # families still short of their minimum must be picked first
        return [f for f, m in R["family_min"].items() if fam_count.get(f, 0) < m]
    ruled = set(R["family_max"]) | set(R["family_min"])          # families a rule names (review C07)
    maxes, mins = tuple(sorted(R["family_max"].items())), tuple(sorted(R["family_min"].items()))
    types = tuple(sorted({(e["cost"], e["family"] if e["family"] in ruled else None)
                          for e in pool if e["cost"] not in R["banned_costs"]}, key=str))
    def fits(e, rem, units):
        """Could the pack still be finished, every rule kept, after picking e?"""
        after = dict(caps)
        if e["cost"] in after: after[e["cost"]] -= 1
        cnt = {f: fam_count.get(f, 0) + (e["family"] == f) for f in ruled}
        return _feas(rem - e["cost"], types, tuple(sorted(after.items())), units - 1, tuple(sorted(cnt.items())), maxes, mins)
    if R["family_min"] and not _feas(remaining, types, tuple(sorted(caps.items())), R["max_units"],
                                     tuple(sorted((f, 0) for f in ruled)), maxes, mins):
        raise CompositionError(f"no pack can meet {R['family_min']} from this pool under {R}")
    while remaining > 0:
        p = live_pool()
        short = need_min()
        if short:
            p = [e for e in p if e["family"] in short]
            if not p: raise CompositionError(f"family_min {short}: none left in the pool")
        units_left = R["max_units"] - len(picks)
        avail = {e["cost"] for e in p}
        faces = []
        for c in (1, 2, 3):
            if c not in avail or c > remaining or caps.get(c, 99) <= 0: continue
            if ruled:
                if any(fits(e, remaining, units_left) for e in p if e["cost"] == c): faces.append(c)
                continue
            after = dict(caps)
            if c in after: after[c] -= 1
            all_costs = {e["cost"] for e in live_pool()}
            if _fillable(remaining - c, all_costs, after, units_left - 1): faces.append(c)
        if not faces:
            raise CompositionError(f"cannot fill {remaining} more slots with {sorted(avail)} under {R}")
        c = rng.choice(faces)
        if log is not None: log.append(f"left {remaining}: faces {faces} -> rolled {c}")
        cands = [e for e in p if e["cost"] == c and (not ruled or fits(e, remaining, units_left))]
        w = [e["weight"] * R["family_weight"].get(e["family"], 1.0) for e in cands]
        e = rng.choices(cands, weights=w)[0]
        picks.append(e); remaining -= c
        fam_count[e["family"]] = fam_count.get(e["family"], 0) + 1
        if c in caps: caps[c] -= 1
    return picks

def place(picks):
    """Assign cells: 3 lanes x (Front, Rear). Front-liners fill Front first, casters fill Rear first."""
    cells = {"front": [], "rear": []}
    order = sorted(picks, key=lambda e: -e["cost"])       # big units get first choice of lane
    for e in order:
        want = e["role"]; other = "rear" if want == "front" else "front"
        (cells[want] if len(cells[want]) < 3 else cells[other]).append(e)
    if len(cells["front"]) == 0 and cells["rear"]:         # nobody may hide behind an empty Front
        cells["front"].append(cells["rear"].pop())
    return [(row, lane, e) for row in ("front", "rear") for lane, e in enumerate(cells[row])]

def describe(e):
    from engine import spirit_name, mogel_name
    if e["family"] == "Ande": return spirit_name(e["rank"], e["element"])
    if e["family"] == "Mogel": return mogel_name(e["rank"], e["element"])
    if e["element"]:
        from engine import join_morphemes
        pre = next((p for p in ("Halv", "Stor") if e["rank"].startswith(p)), "")
        return join_morphemes([x for x in (pre, e["element"], e["rank"][len(pre):].lower()) if x]).capitalize()
    return e["rank"]

def spawn(placed, level):
    """Turn placed entries into battle units, lettering duplicates (Eldmogel A, Eldmogel B)."""
    from engine import spawn_spirit, spawn_mogel, spawn_family
    units = []
    for row, lane, e in placed:
        if e["family"] == "Ande": u = spawn_spirit(e["rank"], e["element"], level)
        elif e["family"] == "Mogel": u = spawn_mogel(e["rank"], e["element"], level)
        else: u = spawn_family(e["family"], e["rank"], level, e["element"], job=e.get("job"))
        u.cell = (row, lane); units.append(u)
    seen = {}
    for u in units: seen[u.name] = seen.get(u.name, 0) + 1
    count = {}
    for u in units:
        u.suffix = ""
        if seen[u.name] > 1:
            count[u.name] = count.get(u.name, 0) + 1
            u.suffix = f" {chr(64 + count[u.name])}"; u.name += u.suffix
    return units

if __name__ == "__main__":
    rng = random.Random(7)
    cat = catalog()
    demos = [
        ("Any drawn unit, any element", dict(art_only=True), {}),
        ("Biome Eldhall, drawn units", dict(art_only=True, **BIOMES["Eldhall"]), {}),
        ("Mire, all ranks, only one 3-cost", BIOMES["Mire"], dict(cost_caps={3: 1})),
        ("Vatnhall, no 1-costs", BIOMES["Vatnhall"], dict(banned_costs=(1,))),
        ("Mixed: at least 1 Mogel and 1 Ande, drawn", dict(art_only=True), dict(family_min={"Mogel": 1, "Ande": 1})),
        ("Small fight: budget 3", dict(art_only=True), dict(budget=3)),
    ]
    print("\nHabitats, all ranks (ranged: unset / include / exclude)")
    for hname in HABITATS:
        for rv in (None, "include", "exclude"):
            placed = place(compose(rng, habitat(cat, hname), dict(ranged=rv)))
            print(f"   {hname:<9} {str(rv):<8} " + " | ".join(f"{row[0].upper()}{lane+1} {describe(e)}{'*' if e['ranged'] else ''} ({e['cost']})" for row, lane, e in placed))
    print("   (* reaches our Rear)")
    print("\nFreeform: roll a biome, then fill with drawn units")
    for _ in range(4):
        name, g = roll_biome(rng)
        placed = place(compose(rng, gate(cat, art_only=True, **g)))
        print(f"   {name:<10} " + " | ".join(f"{row[0].upper()}{lane+1} {describe(e)} ({e['cost']})" for row, lane, e in placed))
    for title, g, rules in demos:
        print(f"\n{title}")
        for _ in range(3):
            log = []
            picks = compose(rng, gate(cat, **g), rules, log)
            placed = place(picks)
            print("   " + " | ".join(f"{row[0].upper()}{lane+1} {describe(e)} ({e['cost']})" for row, lane, e in placed)
                  + "      rolls: " + "; ".join(x.split(': ')[1] for x in log))
