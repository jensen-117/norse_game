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
    "Skar": ("Slash", None), "Kross": ("Crush", None), "Spett": ("Pierce", None), "Skott": ("Pierce", "any"),
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
        kw.update(element="Lak", target="fallen")
        del kw["all"]
    if "shape" in t: kw["shape"] = t["shape"]
    if t.get("spot"): kw["spot"] = True
    for k in ("group", "bide", "crit_bonus", "crit_mult"):
        if k in m: kw[k] = m[k]
    if "flurry" in m: kw["flurry"] = dict(m["flurry"])
    if parts: kw["parts"] = dict(root=root, tier=tier, target=target, manner=manner, rider=rider)
    kw.update(extra)
    return act(kind, name or word_name(word_root, tier, target, direction, manner, rider), **kw)

# ---------------------------------------------------------------- the class verbs (pillars Part 5c; classes.md)
MARTIAL_CLASSES = {"Ullar", "Vasara", "Nalarbani", "Hersir", "Huskarl", "Berserker"}
LADDER = ["Halv", "Base", "Mer", "Jatte", "Ur"]

class OverCap(ValueError):
    """More upgrade parts than a move can carry, and no capstone of that shape."""

def merge_manners(manners):
    """Several manners on one move: the speed group of the non-Bid one; Bid winds up and releases in that group
    (Bid + Tung: a meteor that lands Heavy). Powers and costs multiply."""
    out, power, cost = {}, 1.0, 1.0
    for mn in manners:
        m = MANNERS[mn]; power *= m.get("power", 1.0); cost *= m.get("cost", 1.0)
        for k in ("crit_bonus", "crit_mult"):
            if k in m: out[k] = m[k]
        if "flurry" in m: out["flurry"] = dict(m["flurry"])
        if m.get("bide"): out["bide"] = True
        if "group" in m: out["group"] = m["group"]
    if out.get("bide") and "group" in out: out["release_group"] = out.pop("group")
    return out, power, cost

def verb_parts(tier, target, manners, styng, lonn):
    """The upgrade parts carved onto a verb, as names (what the cap counts and capstones match)."""
    p = [x for x in (None if tier in (None, "Base") else tier, target) if x] + list(manners)
    return p + (["Styng"] if styng else []) + (["Lonn"] if lonn else [])

def compile_verb(verb, tier=None, target=None, manners=(), styng=False, lonn=False):
    """A class verb grown by parts (pillars Part 5c): its spoken name, its rules, and its cost as a share of the hero's
    own bar (priced when the hero is built: engine.price_bars). Raises OverCap for more than UPGRADE_CAP parts, unless
    the parts make a named capstone."""
    v = VERBS[verb]
    carved = verb_parts(tier, target, manners, styng, lonn)
    if styng and not v.get("styng"): raise ValueError(f"{verb} takes no Styng")
    if lonn and not v.get("rider"): raise ValueError(f"{verb} has no designated rider")
    name = None
    if len(carved) > UPGRADE_CAP:
        name = next((n for n, (vb, ps) in CAPSTONES.items() if vb == verb and ps == frozenset(carved)), None)
        if name is None: raise OverCap(f"{verb} + {carved}: over the cap of {UPGRADE_CAP}, and no capstone")
    # the tier: a carved rung climbs from the verb's own (Storm is Mer; Merstorm is Jatte)
    own = v.get("tier", "Base")
    eff = own if tier in (None, "Base") else tier if tier == "Halv" else LADDER[min(len(LADDER) - 1, LADDER.index(own) + LADDER.index(tier) - 1)]
    allm = tuple(v.get("manners", ())) + tuple(manners)
    mkw, mpower, _ = merge_manners(allm)
    rider, part = (v["rider"] if lonn else (None, None))
    spoken = name or join_morphemes([x for x in (target, None if tier in (None, "Base") else tier, "Styng" if styng else None,
                                                 *manners, part, verb) if x])
    vt = v.get("target", "enemy")
    a = act(v["kind"], spoken, tier=eff, all=(target == "All" or vt in ("all", "allies")),
            target={"self": "self", "ally": "ally", "allies": "ally", "fallen": "fallen", "all": "enemy"}.get(vt, "enemy"),
            element=v.get("element"), status=v.get("status"), stat=v.get("stat"),
            direction=None if v.get("up") is None else (1 if v["up"] else -1))
    if target == "Flok": a["shape"] = "row"
    if v["kind"] in ("damage", "answer"): a["power"] = TIER_POWER[eff] * mpower
    if styng: a["styng"] = TIER_POWER[eff] * STYNG_POWER * mpower       # a hit added to a move with no damage of its own
    if v["kind"] == "heal": a["power"] = TIER_POWER[eff]
    if v["kind"] == "revive": a.update(VAKNA[eff])
    if rider is not None:                                                # what Lonn adds
        if isinstance(rider, tuple): a["also"] = [rider]                 # a second stat stage (Lonnaukraft: DEF up)
        elif rider == "cleanse_one": a["cleanse_one"] = True             # Lonnlak
        elif v["kind"] == "damage": a["status"] = rider                  # Blotskott: may Bleed
        else: a["also_status"] = rider                                   # Lonnsveda: Scorched and Feeble
    for k in ("root", "knots", "follow", "pays_on", "push"):
        if k in v: a[k] = v[k]
    if "group" in v: a["group"] = v["group"]
    a.update(mkw)
    group = a.get("release_group", a.get("group", SPEED_GROUP_BY_KIND.get(v["kind"], 0)))
    a["keywords"] = [k for k in (GROUP_KEYWORD.get(group), "Patient" if a.get("bide") else None) if k]
    # the price: a share of the hero's own bar
    a["cost_type"] = "HP" if v.get("cls") in MARTIAL_CLASSES else "MP"
    steps = (TIER_WEIGHT.get(eff, 0) - TIER_WEIGHT.get(own, 0) if tier not in (None, "Base", "Halv") else 0) \
        + (1 if target else 0) + len(manners) + int(styng) + int(lonn) + v.get("weight", 0)
    if v.get("free") or (eff == "Halv" and steps == 0): share = 0.0
    else: share = BASE_SHARE[a["cost_type"]] * PART_STEP[a["cost_type"]] ** (steps - (1 if eff == "Halv" else 0))
    a["share"], a["cost"] = share, 0
    a["parts"] = dict(verb=verb, tier=tier or "Base", target=target, manners=tuple(manners), styng=styng, lonn=lonn,
                      capstone=name)
    return a

def compile_kit(cls, leg):
    """A class's kit snapshot for one leg (data.KITS), compiled."""
    return [compile_verb(verb, **parts) for verb, parts in KITS[cls][leg]]
