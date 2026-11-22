"""One compiler for every move (refactor_plan Wave 2).

Every move in the game, a hero's spell, an enemy's strike, a word built by the grammar, a revive or an item, is a
spec of parts compiled here: a kind, a root, and the morphemes (target, tier, direction, manner, rider). The name, the
cost, the power and the move's rules all come from the parts, so a new move is data, not a new builder.

This module depends on data.py only, so engine.py and grammar.py both build on it.
"""
from data import *

VOWELS = set("aeiouy")

# ---------------------------------------------------------------- naming (spellbook Part 2; pillars Part 5: the seam rule)
def join_morphemes(parts):
    """Apply the seam rules: identical letters merge (Brak + Krosh = Brakrosh); vowel + vowel, the second wins."""
    word = parts[0].lower()
    for p in parts[1:]:
        p = p.lower()
        if word[-1] == p[0]:
            word = word + p[1:]
        elif word[-1] in VOWELS and p[0] in VOWELS:
            word = word[:-1] + p
        else:
            word = word + p
    return word.capitalize()

def word_name(root, tier="Base", target=None, direction=None, manner=None, rider=None):
    """A move's spoken name, from its parts in their fixed order: target, tier, direction, manner, rider, root."""
    return join_morphemes([p for p in (target, None if tier == "Base" else tier, direction, manner, rider, root) if p])

def spell_name(root, tier, all_=False, direction=None):
    return word_name(root, tier, "All" if all_ else None, direction)

# ---------------------------------------------------------------- the move record
def act(kind, name, **kw):
    d = dict(kind=kind, name=name, element=None, tier="Base", all=False, cost=0,
             cost_type="MP", power=0, status=None, stat=None, direction=None,
             target="enemy", pct_current=0.0)
    d.update(kw)
    return d

# ---------------------------------------------------------------- roots
STATUS_ROOT = {"Poisoned": "Eitr", "Cursed": "Nid", "Feared": "Ogn", "Blinded": "Blinda",
               "Disarmed": "Mogl", "Death": "Helvad", "Silenced": "Bann"}
STAT_ROOT = {"ATK": "Kraft", "DEF": "Skold", "MAT": "Seid", "MDF": "Stav",
             "ACC": "Hitt", "EVA": "Vig", "SPD": "Rask"}
WEAPON = {   # martial root: (damage type, reach override)
    "Skar": ("Slash", None), "Krosh": ("Crush", None), "Spett": ("Pierce", None), "Skott": ("Pierce", "any"),
}

# ---------------------------------------------------------------- morphemes (all tune knobs live here)
TARGETS = {
    None:   dict(),
    "Flok": dict(shape="row", cost=1.5),                         # per-target x0.75 comes from SHAPE_MULT
    "All":  dict(all=True, cost=ALL_COST_MULT),                  # per-target x0.75 comes from ALL_POWER_MULT
    "Mark": dict(spot=True),     # targets space: a painted spot (DoT for N rounds), or with Bid a one-shot on the spot.
}
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

# ---------------------------------------------------------------- price
def base_cost(kind, root, tier):
    """The cost before target and manner: what a plain move of this kind and tier costs."""
    if kind in ("heal", "revive"): return HALVLAK_COST if tier == "Halv" else TIER_COST[tier]   # healing is never free
    if kind == "damage" and root not in WEAPON and root not in MARTIAL:
        return 0 if tier == "Halv" else TIER_COST[tier] * ELEMENT[root]["cost"]
    return TIER_COST[tier]

# ---------------------------------------------------------------- the compiler
def compile_move(kind, root=None, tier="Base", target=None, manner=None, rider=None, *, status=None, stat=None,
                 up=None, name=None, power=None, parts=False, cost_type=None, **extra):
    """Compile one move from its parts.
       kind     damage, heal, cleanse, status, stat, revive
       root     the word's root: a martial root (Skar), a damage type (Slash), an element (Eld); for status and stat
                moves the root comes from the status or stat (STATUS_ROOT, STAT_ROOT)
       tier, target, manner, rider: the morphemes (TARGETS, MANNERS, RIDERS)
       status   the status a status move or a strike carries (a rider sets it too)
       stat, up a stat move's stat and direction (Auk / Ned)
       name     a name given instead of the spoken one (an enemy's "Grave Axe", a class's "Blotskar")
       power    a power given instead of the tier's
       parts    record the parts on the move (words built by the grammar)
       cost_type  "MP" or "HP", when the root alone doesn't say (a spell cast with a martial damage type)
       extra    anything else the move carries (pct_current, the revive ladder's reach)"""
    t, m = TARGETS[target], MANNERS[manner]
    direction = None if up is None else ("Auk" if up else "Ned")
    if kind == "status": word_root = STATUS_ROOT[status]
    elif kind == "stat": word_root = STAT_ROOT[stat]
    else: word_root = root
    cost = base_cost(kind, root, tier)
    if tier == "Halv" and manner: cost = HALV_MANNER_COST
    cost = round(cost * t.get("cost", 1.0) * m.get("cost", 1.0))
    martial = root in WEAPON or root in MARTIAL
    kw = dict(tier=tier, all=t.get("all", False), cost=cost)
    if kind == "damage":
        dtype, reach = WEAPON[root] if root in WEAPON else (root, None)
        p = TIER_POWER[tier] if power is None else power
        p = p * m.get("power", 1.0) * (RIDER_POWER if rider else 1.0)
        kw.update(element=dtype, power=p, cost_type=cost_type or ("HP" if martial else "MP"))
        if status or rider: kw["status"] = status or RIDERS[rider]
        elif parts: kw["status"] = None
        if reach: kw["reach"] = reach
    elif kind == "heal":
        kw.update(element="Lak", power=TIER_POWER[tier] if power is None else power, target="ally")
    elif kind == "cleanse":
        kw.update(target="ally")
    elif kind == "status":
        kw.update(status=status)
    elif kind == "stat":
        kw.update(stat=stat, direction=1 if up else -1, target="ally" if up else "enemy")
    elif kind == "revive":
        kw.update(element="Lak", target="fallen", **VAKNA[tier])      # a revive is complete on its own (A01)
        del kw["all"]
    if "shape" in t: kw["shape"] = t["shape"]
    if t.get("spot"): kw["spot"] = True
    for k in ("group", "bide", "crit_bonus", "crit_mult"):
        if k in m: kw[k] = m[k]
    if "flurry" in m: kw["flurry"] = dict(m["flurry"])
    if parts: kw["parts"] = dict(root=root, tier=tier, target=target, manner=manner, rider=rider)
    kw.update(extra)
    return finalize(act(kind, name or word_name(word_root, tier, target, direction, manner, rider), **kw))

# ---------------------------------------------------------------- the class verbs (pillars Part 5c; classes.md)
MARTIAL_CLASSES = {"Ullar", "Vasara", "Nalarbani", "Hersir", "Huskarl", "Berserker"}
LADDER = ["Halv", "Base", "Mer", "Jatte", "Ur"]

class OverCap(ValueError):
    """More upgrade parts than a move can carry, and no capstone of that shape."""

def merge_manners(manners, own_power=None):
    """Several manners on one move (already validated: no repeats, one speed manner at most). Bid winds up and
    releases in the speed manner's group (Bid + Tung: a meteor that lands Heavy), in any order. Powers and costs
    multiply. own_power: the verb's own multiplier for a manner, in place of MANNERS' (Hevn's Bid: x2)."""
    out, power, cost = {}, 1.0, 1.0
    for mn in manners:
        m = MANNERS[mn]; power *= (own_power or {}).get(mn, m.get("power", 1.0)); cost *= m.get("cost", 1.0)
        for k in ("crit_bonus", "crit_mult"):
            if k in m: out[k] = m[k]
        if "flurry" in m: out["flurry"] = dict(m["flurry"])
        if m.get("bide"): out["bide"] = True
        if "group" in m: out["group"] = m["group"]
    if out.get("bide") and "group" in out: out["release_group"] = out.pop("group")
    return out, power, cost

def normalize(verb, tier=None, target=None, manners=(), styng=False, lonn=False, source="carve"):
    """Check a verb's parts once (review C08-C11, A02) and return them in one canonical form, which the cap, the name,
    the effects and the price all read. Raises ValueError, with the reason, for anything unknown, repeated,
    contradictory, redundant, not allowed on this verb, or beyond what the move's source can reach."""
    if verb not in VERBS: raise ValueError(f"no verb {verb!r}")
    v = VERBS[verb]; kind = v["kind"]
    if source not in SOURCE_TIER: raise ValueError(f"unknown source {source!r} (carve, find, gear)")
    tier = tier or "Base"
    if tier not in LADDER: raise ValueError(f"unknown tier {tier!r}")
    if target is not None and target not in TARGET_PARTS: raise ValueError(f"unknown target part {target!r}")
    if target is not None and target not in v.get("targets", ()):
        raise ValueError(f"{verb} can't take {target}" + (" (it already reaches everyone)" if v.get("target") in ("all", "allies") else ""))
    manners = tuple(manners)
    for mn in manners:
        if mn not in MANNERS or mn is None: raise ValueError(f"unknown manner {mn!r}")
    if len(set(manners)) != len(manners): raise ValueError(f"{verb}: a manner can't be carved twice ({manners})")
    if len(SPEED_MANNERS & set(manners)) > 1: raise ValueError(f"{verb}: Swift and Heavy contradict each other")
    for mn in manners:
        needs = MANNER_NEEDS[mn]
        if needs is not None and kind not in needs: raise ValueError(f"{verb}: {mn} does nothing to a {kind} move")
        if mn == "Snar" and (v.get("group", 0) >= 1 or SPEED_GROUP_BY_KIND.get(kind, 0) >= 1):
            raise ValueError(f"{verb} already acts sooner than Swift")
        if mn in v.get("manners", ()): raise ValueError(f"{verb} is already {mn}")
    if styng and not v.get("styng"): raise ValueError(f"{verb} takes no Styng")
    if lonn and not v.get("rider"): raise ValueError(f"{verb} has no designated rider")
    rider = None
    if lonn:                                           # True: the verb's own rider; a word: another of its designated riders
        rider = v["rider"] if lonn is True else next((r for r in v.get("riders", ()) if r[1] == lonn), None)
        if rider is None: raise ValueError(f"{verb} has no rider {lonn!r}")
    own = v.get("tier", "Base")
    if tier == "Halv":
        if own != "Base": raise ValueError(f"{verb} has no Halv fork (it is {own} already)")
        if not v.get("halv"): raise ValueError(f"{verb} has no Halv fork (only attacks do: a free {kind} would break things)")
        eff = "Halv"
    elif tier == "Base": eff = own
    else:
        eff = LADDER[LADDER.index(own) + LADDER.index(tier) - LADDER.index("Base")] \
            if LADDER.index(own) + LADDER.index(tier) - LADDER.index("Base") < len(LADDER) else None
        if LADDER.index(tier) > LADDER.index(SOURCE_TIER[source]):        # the part itself: carving adds Mer at most
            raise ValueError(f"{verb}: a {tier} part can't be {source}d (up to {SOURCE_TIER[source]})")
        if eff is None or (eff == "Ur" and source != "gear"):              # only gear reaches Ur, even by promotion
            raise ValueError(f"{verb} + {tier} would be {eff or 'past Ur'}: Ur comes only from gear")
    return dict(verb=verb, tier=tier, eff=eff, own=own, target=target, manners=manners, styng=bool(styng),
                lonn=bool(lonn), rider=rider, source=source)

def verb_parts(n):
    """The upgrade parts carved onto a verb, as names: what the cap counts, capstones and bynames match, and the
    price counts. Canonical, so all four agree (review C10)."""
    p = [x for x in (None if n["tier"] == "Base" else n["tier"], n["target"]) if x] + list(n["manners"])
    # the verb's own rider counts as Lonn; another designated rider by its word (Bann), so a capstone made with
    # Lonn (Tusensplitter: Blot) isn't matched by the other
    lonn = [] if not n["lonn"] else ["Lonn"] if n["rider"] == VERBS[n["verb"]]["rider"] else [n["rider"][1]]
    return p + (["Styng"] if n["styng"] else []) + lonn

def compile_verb(verb, tier=None, target=None, manners=(), styng=False, lonn=False, source="carve"):
    """A class verb grown by parts (pillars Part 5c): its spoken name, its rules, and its cost as a share of the hero's
    own bar (priced when the hero is built: engine.price_bars). The parts are checked first (normalize); more than
    UPGRADE_CAP of them is OverCap unless they make a named capstone. The result meets the move contract
    (check_move); `unresolved` lists what still keeps it out of a playable kit (effects that arrive in Wave 4)."""
    n = normalize(verb, tier, target, manners, styng, lonn, source)
    v = VERBS[verb]; kind = v["kind"]
    carved = verb_parts(n)
    name = None
    if len(carved) > UPGRADE_CAP:
        name = next((nm for nm, (vb, ps) in CAPSTONES.items() if vb == verb and ps == frozenset(carved)), None)
        if name is None: raise OverCap(f"{verb} + {carved}: over the cap of {UPGRADE_CAP}, and no capstone")
    elif carved:                     # a byname for a long spoken name within the cap (Geirskott)
        name = next((nm for nm, (vb, ps) in BYNAMES.items() if vb == verb and ps == frozenset(carved)), None)
    eff, own = n["eff"], n["own"]
    mkw, mpower, _ = merge_manners(tuple(v.get("manners", ())) + n["manners"], {**CLASS_MANNER_POWER, **v.get("manner_power", {})})
    rider, part = (n["rider"] if n["lonn"] else (None, None))
    # a root name (Daska, Genomskott) takes the parts it stands for; the rest attach to it (Merdaska)
    root, used = verb, frozenset()
    if name is None:
        for nm, (vb, ps) in ROOT_NAMES.items():
            if vb == verb and ps <= frozenset(carved): root, used = nm, ps; break
    spoken = name or join_morphemes([x for x in (n["target"], None if n["tier"] == "Base" else n["tier"],
                                                 "Styng" if n["styng"] and "Styng" not in used else None, *n["manners"],
                                                 None if "Lonn" in used else part, root) if x])
    # who it reaches: eligibility (self, ally, enemy, fallen) and scope (one, row, all) kept apart (review C09)
    vt = v.get("target", "enemy")
    a = act(kind, spoken, tier=eff, all=(n["target"] == "All" or vt in ("all", "allies")),
            target={"self": "self", "cell": "self", "ally": "ally", "allies": "ally", "fallen": "fallen", "all": "enemy"}.get(vt, "enemy"),
            element=v.get("element"), status=v.get("status"), stat=v.get("stat"),
            direction=None if v.get("up") is None else (1 if v["up"] else -1))
    if n["target"] == "Flok": a["shape"] = "row"
    if n["target"] == "All" or vt == "all": a["all_power"] = ALL_SHARE  # wide, and thinner (Nov 20; the untie spells too, Nov 21)
    if vt == "cell": a["by_cell"] = True                                 # aimed at a cell, like Move (Skrida)
    # power, as a share of a clean Krosh (Nov 21): the tier's share of base x the class's (melee 1.0, ranged 0.75, magic
    # 0.9) or the verb's own (Blixt 1.0). The element's power and hits are the old game's table, divided back out so a
    # class verb lands its share exactly; the hero's anchor (engine.anchor_mult) turns power 20 into KROSH_CLEAN.
    tier_share = CLASS_TIER.get(eff, TIER_POWER[eff] / TIER_POWER["Base"])
    share = v.get("share", CLASS_SHARE.get(v.get("cls"), 1.0))
    if kind == "damage":
        el = ELEMENT[v["element"]]
        a["power"] = TIER_POWER["Base"] * tier_share * share * mpower / (el["power"] * el["hits"]) \
            * (RIDER_SHARE if n["lonn"] else 1.0)
    elif kind in SCALES:                                                 # heals: the healer's anchor; a rider costs the same 0.6
        a["power"] = TIER_POWER["Base"] * tier_share * mpower * (RIDER_SHARE if n["lonn"] else 1.0)
    if n["styng"]: a["styng"] = TIER_POWER["Base"] * tier_share * share * STYNG_POWER * mpower   # a hit added to a move with no damage of its own
    if kind == "revive": a.update(VAKNA[eff])
    if rider is not None:                                                # what Lonn adds
        if isinstance(rider, tuple): a["also"] = [rider]                 # a second stat stage (Lonnaukraft: DEF up)
        elif kind == "damage":
            a["status"] = rider                                          # Blotskott: may Bleed
            if rider in COUNTER_OF: a["rider_sure"] = True               # Brakrosh: a counter rider lands on every hit
        else: a["also_status"] = rider                                   # Lonnsveda: Scorched and Feeble
    if n["styng"]:                                                       # the added hit's damage type: the verb's, else its weapon's
        a["styng_el"] = v.get("element") or WEAPON[v["root"]][0]
    a["designated"] = True                                               # riders are the verb's own: no element rider (Blixt's Stun is Lonn's)
    for k in ("root", "knots", "follow", "pays_on", "pays_below", "pays", "answer", "amount", "push"):
        if k in v: a[k] = v[k]
    if "group" in v: a["group"] = v["group"]
    if eff in v.get("tier_group", {}): a["group"] = v["tier_group"][eff]   # a tier that takes longer (Merknyta: Late)
    a.update(mkw)
    group = a.get("release_group", a.get("group", SPEED_GROUP_BY_KIND.get(kind, 0)))
    a["keywords"] = [k for k in (GROUP_KEYWORD.get(group), "Patient" if a.get("bide") else None) if k]
    # the price (Nov 21, classes.md Part 7c): the verb's rung (Halv its own) x 2 a step. Steps: a rung above the verb's
    # own, Flok 2, All 3, a manner, Styng, the rider, the verb's built-in reach (weight); a knot spent pays one. Written
    # at SHEET_LEVEL; engine.price_bars scales it with the hero's pool at other levels.
    a["cost_type"] = "HP" if v.get("cls") in MARTIAL_CLASSES else "MP"
    steps = (TIER_WEIGHT[eff] - TIER_WEIGHT[own] if n["tier"] != "Halv" else 0) \
        + TARGET_STEPS.get(n["target"], 0) + len(n["manners"]) + int(n["styng"]) + int(n["lonn"]) \
        + v.get("weight", 0) - v.get("knots", 0)
    if v.get("free"): price = 0
    else: price = (HALV_COST[a["cost_type"]] if eff == "Halv" else v["cost"]) * 2 ** steps
    a["price"], a["cost"] = price, 0                                     # the ladder number at SHEET_LEVEL (engine.price_bars)
    a["parts"] = dict(verb=verb, tier=n["tier"], target=n["target"], manners=n["manners"], styng=n["styng"], lonn=n["lonn"],
                      rider_word=part,
                      source=n["source"], capstone=name if len(carved) > UPGRADE_CAP else None,
                      byname=name if len(carved) <= UPGRADE_CAP else None)
    a["unresolved"] = unresolved(a)
    problems = check_move(a)
    if problems: raise ValueError(f"{spoken}: {'; '.join(problems)}")
    return a

# ---------------------------------------------------------------- the move contract (review A01)
# Every move that can enter a fight, from any path (the builders, the grammar, class verbs, items, enemy rows), is one
# dict with the act() fields plus what its kind needs. check_move() states the contract; unresolved() says what the
# engine can't yet carry out, so a compiled but unfinished move can't be put in a playable kit (Battle refuses it).
EXECUTABLE_KINDS = {"damage", "heal", "cleanse", "status", "stat", "revive", "cover", "defend", "move", "flee", "mp",
                    "taunt", "meditate",                     # Wave 3: Egga and Meditate
                    "glide", "windfall",                     # Wave 4a: Skrida and Djupanda
                    "song",                                  # Wave 4b: Kvad
                    "knot", "displace"}                      # Wave 4c: Knyta, Kasta and Svepa
KIND_NEEDS = {"revive": ("reaches", "hp", "wound"), "stat": ("stat", "direction"), "status": ("status",),
              "glide": ("stat", "direction"), "windfall": ("amount",)}
WAVE4_FIELDS = ()   # every Wave 4 effect resolves (4a: also_status, pays_on, pays_below, styng; 4b: cleanse_one gone; 4c: knots, follow, push)
RUNTIME_STATUSES = set(STATUSES) | set(COUNTER_OF) | {"Death"}
CORE_FIELDS = ("kind", "name", "element", "tier", "all", "cost", "cost_type", "power", "status", "stat", "direction",
               "target", "pct_current")

def check_move(a):
    """The contract's structure: what any move must carry to be read by the engine. Returns the problems (empty: OK)."""
    out = [f"missing {f}" for f in CORE_FIELDS if f not in a]
    if out: return out
    out += [f"a {a['kind']} move needs {f}" for f in KIND_NEEDS.get(a["kind"], ()) if a.get(f) is None]
    if a["cost_type"] not in ("MP", "HP"): out.append(f"cost type {a['cost_type']!r}")
    if a["target"] not in ("enemy", "ally", "self", "fallen"): out.append(f"target {a['target']!r}")
    if a["kind"] in ("damage", "heal") and not a.get("spot") and not (a["power"] or a.get("fixed") or a.get("amount")):
        out.append("no power")
    return out

def unresolved(a):
    """What keeps a well-formed move out of a fight for now: a kind or an effect the engine doesn't carry out yet."""
    out = []
    if a["kind"] not in EXECUTABLE_KINDS: out.append(f"{a['kind']} moves arrive in Wave 4")
    for f in WAVE4_FIELDS:
        if a.get(f): out.append(f"{f} arrives in Wave 4")
    for st in (a.get("status"),):
        if st and st not in RUNTIME_STATUSES: out.append(f"{st} has no status row yet")
    return out

def finalize(a):
    """The last step of every path that builds an executable move: the contract holds, or this says why not."""
    problems = check_move(a) + unresolved(a)
    if problems: raise ValueError(f"{a.get('name')}: {'; '.join(problems)}")
    return a

def compile_kit(cls, leg):
    """A class's kit snapshot for one leg (data.KITS), compiled."""
    return [compile_verb(verb, **parts) for verb, parts in KITS[cls][leg]]
