"""Encounter v0 -- battle engine."""
import random
from data import *

VOWELS = set("aeiouy")

# ================================================================ naming
def join_morphemes(parts):
    """Apply the seam rules: identical letters merge; vowel+vowel, second wins."""
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

def spell_name(root, tier, all_=False, direction=None):
    parts = []
    if all_: parts.append("All")
    if tier != "Base": parts.append(tier)
    if direction: parts.append(direction)
    parts.append(root)
    return join_morphemes(parts)

# ================================================================ math
def clamp(x, lo, hi): return max(lo, min(hi, x))
def stage_mult(n): return (3 + n) / 3 if n >= 0 else 3 / (3 - n)
def level_factor(level): return 0.6 + level / 20
def attr_at(gene, level, growth_mult=1.0):
    return 10 + gene / 2 + (level - 1) * (0.6 + gene / 50) * growth_mult
def avg_attr(level): return attr_at(15.5, level)

UNIT_KEYS = ("unit", "src", "target", "instead_of", "swapped", "was")

# ================================================================ actions
def act(kind, name, **kw):
    d = dict(kind=kind, name=name, element=None, tier="Base", all=False, cost=0,
             cost_type="MP", power=0, status=None, stat=None, direction=None,
             target="enemy", pct_current=0.0)
    d.update(kw)
    return d

def vakna(tier):
    """The revive ladder (combat_spec Part 10): Halvakna and Vakna reach the Dying, Mervakna and up raise the Dead."""
    name = join_morphemes([x for x in (None if tier == "Base" else tier, "Vakna") if x]).capitalize()
    cost = HALVLAK_COST if tier == "Halv" else TIER_COST[tier]
    return act("revive", name, element="Lak", tier=tier, target="fallen", cost=cost, **VAKNA[tier])

def item_move(key):
    """An item as a move: fixed power, no cost but the item itself."""
    it = ITEMS[key]; k = it["kind"]
    if k == "revive": return dict(vakna(it["tier"]), name=it["name"], cost=0, item=key, element=None)
    a = act(k, it["name"], item=key, fixed=True, tier="Base",
            target={"heal": "ally", "mp": "ally", "stat": "enemy", "damage": "enemy", "flee": "self"}[k])
    if k in ("heal", "mp"): a["amount"] = it["amount"]
    if k == "stat": a.update(stat=it["stat"], direction=it["direction"])
    if k == "damage": a.update(element=it["element"], power=it["power"], all=it.get("all", False), reach="any")
    return a

def damage_spell(root, tier, all_=False):
    cost = 0 if tier == "Halv" else TIER_COST[tier] * ELEMENT[root]["cost"]
    if all_: cost *= ALL_COST_MULT
    return act("damage", spell_name(root, tier, all_), element=root, tier=tier, all=all_,
               cost=round(cost), power=TIER_POWER[tier])

def heal_spell(tier, all_=False):
    cost = HALVLAK_COST if tier == "Halv" else TIER_COST[tier]
    if all_: cost *= ALL_COST_MULT
    return act("heal", spell_name("Lak", tier, all_), element="Lak", tier=tier, all=all_,
               cost=round(cost), power=TIER_POWER[tier], target="ally")

STATUS_ROOT = {"Poisoned": "Eitr", "Cursed": "Nid", "Feared": "Ogn", "Blinded": "Blinda",
               "Disarmed": "Mogl", "Death": "Helvad", "Silenced": "Bann"}
def cleanse_spell(tier="Base", all_=False):
    cost = TIER_COST[tier] * (ALL_COST_MULT if all_ else 1)
    return act("cleanse", spell_name("Skolja", tier, all_), tier=tier, all=all_, cost=round(cost),
               target="ally")

def status_spell(status, tier, all_=False):
    cost = TIER_COST[tier] * (ALL_COST_MULT if all_ else 1)
    return act("status", spell_name(STATUS_ROOT[status], tier, all_), status=status,
               tier=tier, all=all_, cost=round(cost))

STAT_ROOT = {"ATK": "Kraft", "DEF": "Skold", "MAT": "Seid", "MDF": "Stav",
             "ACC": "Hitt", "EVA": "Vig", "SPD": "Rask"}
def stat_spell(stat, up, tier="Base", all_=False):
    cost = TIER_COST[tier] * (ALL_COST_MULT if all_ else 1)
    return act("stat", spell_name(STAT_ROOT[stat], tier, all_, "Auk" if up else "Ned"),
               stat=stat, direction=1 if up else -1, tier=tier, all=all_, cost=round(cost),
               target="ally" if up else "enemy")

def strike(dtype, name="Strike", power=10):
    return act("damage", name, element=dtype, tier="Halv", power=power, cost=0, cost_type="HP")

def skill(dtype, name, tier, all_=False, status=None, power=None, pct_current=0.0):
    cost = TIER_COST[tier] * (ALL_COST_MULT if all_ else 1)
    return act("damage", name, element=dtype, tier=tier, all=all_, cost=round(cost),
               cost_type="HP", power=power or TIER_POWER[tier], status=status,
               pct_current=pct_current)

def top_tier(level):
    return "Jatte" if level >= 50 else "Mer" if level >= 20 else "Base"

def loadout(cls, level):
    c = CLASSES[cls]
    top = top_tier(level)
    if c["kind"] == "magical":
        p = c["school"]; ch = CHILD_OF[p]
        if p == "Sol":
            return [damage_spell("Sol", "Halv"), heal_spell(top), heal_spell("Base", True),
                    damage_spell("Sol", top)]
        if p == "Natt":
            return [damage_spell("Natt", "Halv"), damage_spell("Natt", top),
                    damage_spell("Aska", top), status_spell("Cursed", "Mer" if level >= 20 else "Base")]
        return [damage_spell(p, "Halv"), damage_spell(p, top), damage_spell(ch, top),
                damage_spell(p, "Base", True)]
    d = c["dmg"]
    root = "Skott" if cls == "Ullar" else MARTIAL_ROOT[d]        # bows own the Skott line
    nm = lambda tier, prefix="": join_morphemes([x for x in (prefix, {"Base": ""}.get(tier, tier), root) if x]).capitalize()
    kit = [strike(d, nm("Halv")), skill(d, nm("Base"), "Base")]
    if level >= 50: kit.append(skill(d, nm("Jatte"), "Jatte"))
    elif level >= 20: kit.append(skill(d, nm("Mer"), "Mer"))
    sig = {"Hersir": skill(d, "Blotskar", "Base", status="Bleeding", power=14),
           "Nalarbani": skill(d, "Blotspett", "Base", status="Bleeding", power=14),
           "Ullar": dict(skill(d, "Flokskott", "Base"), shape="row", cost=12),
           "Huskarl": stat_spell("DEF", True),
           "Vasara": stat_spell("DEF", True),
           "Berserker": skill(d, "Berserksgang", "Base", power=32, pct_current=0.25)}[cls]
    kit.append(sig)
    for a in kit:                     # range: the root in this class's weapon (Skott on a Bow: Long; Spett on a Stikk: Short)
        if a["kind"] == "damage": a["reach"] = RANGES[root_range(root, c["weapon"])]; a["weapon"] = c["weapon"]
    if len(kit) < 4: kit.append(act("defend", "Defend", target="self"))
    return kit

# ================================================================ plain English for every move (the menu's hover card)
PLAIN_TIER = {"Halv": "Weak", "Base": "Average", "Mer": "High", "Jatte": "Great", "Ur": "Primal"}   # Joseph's scale
PLAIN_SHARE = {0.25: "a quarter of", 0.5: "half of", 1.0: "all of"}
PLAIN_STEPS = {1: "one step", 2: "two steps", 3: "three steps", 4: "four steps"}
PLAIN_MANNER = {"Snar": "Acts sooner.", "Tung": "Acts last, and hits harder.",
                "Bid": "Winds up this round and lands next round; lost if you're stunned or frozen.",
                "Jarf": "Reckless: weaker, but crits often and hard.", "Drif": "A flurry: may chain up to four hits."}

def plain(a):
    """One line a player can read: what the move does, with no lore needed (Joseph, Nov 8)."""
    k, el, tier = a["kind"], a.get("element"), a.get("tier") or "Base"
    parts = a.get("parts") or {}
    who_foe = "all foes" if a["all"] else {"row": "a row of foes", "column": "one foe and the one behind it"}.get(a.get("shape"), "one foe")
    who_ally = "all allies" if a["all"] else "one ally"
    if k == "damage":
        if a.get("fixed"):
            power = "Average" if (a.get("power") or 0) <= 24 else "High"
            s = f"{power} {el} damage to {who_foe}" + (", ignoring weaknesses and resistances." if el == "Force" else ".")
            return s + " Thrown: reaches anywhere."
        reach = a.get("reach") or (REACH_BY_TYPE.get(el) if el in MARTIAL else "any")
        if a["all"] and reach == "melee": who_foe = "every foe in their Front"
        if a.get("spot"):
            s = f"Coats one foe's spot in {el}: hits whoever stands there, then again each round for three rounds."
        else:
            s = f"{PLAIN_TIER.get(tier, 'Average')} {el} damage to {who_foe}."
        if reach == "melee": s += " Range Short: reaches the Front; half damage from the Rear."
        elif reach == "reach": s += " Range Medium: reaches the Rear while you stand in the Front."
        elif reach == "any" and el in MARTIAL: s += " Range Long: reaches anywhere."
        if a.get("hits", 1) > 1: s += f" In {a['hits']} hits."
        if a.get("falloff"): s += " Half damage to the one behind."
        if a.get("status"): s += f" May leave them {a['status']}."
        if parts.get("manner") in PLAIN_MANNER: s += " " + PLAIN_MANNER[parts["manner"]]
        elif a.get("bide"): s += " " + PLAIN_MANNER["Bid"]
        elif a.get("flurry"): s += " " + PLAIN_MANNER["Drif"]
        if a.get("pct_current"): s += f" Costs {PLAIN_SHARE.get(a['pct_current'], 'part of')} your current HP."
        return s
    if k == "heal":
        if a.get("item"): return f"Restores {PLAIN_SHARE.get(a.get('amount'), 'some of')} one ally's HP."
        return f"{PLAIN_TIER.get(tier, 'Average')} healing for {who_ally}."
    if k == "mp": return f"Restores {PLAIN_SHARE.get(a.get('amount'), 'some of')} one ally's MP."
    if k == "stat":
        steps = PLAIN_STEPS.get(max(1, TIERS.index(tier)) if tier in TIERS else 1, "one step")
        if a.get("also"):
            st, d = a["also"][0]
            return f"Raises the {a['stat']} of {who_ally} by {steps}, but lowers their {st}."
        if a["direction"] > 0: return f"Raises the {a['stat']} of {who_ally} by {steps}."
        return f"Lowers the {a['stat']} of {who_foe} by {steps}."
    if k == "status":
        if a["status"] == "Death": return f"A chance to fell {who_foe} outright."
        if a["status"] == "Bound":
            return "Nets one foe: they lose their next action. Acts sooner. Once per fight."
        return f"May leave {who_foe} {a['status']}."
    if k == "cleanse": return f"Washes ailments and lowered stats off {who_ally}."
    if k == "revive":
        reach = "a Dying or Dead ally" if a.get("reaches") == "Dead" else "a Dying ally"
        hp = "at 1 HP" if not a.get("hp") else ("at full HP" if a["hp"] >= 1 else f"with {PLAIN_SHARE.get(a['hp'], 'a fifth of')} their HP" if a["hp"] in PLAIN_SHARE else "with a fifth of their HP")
        return f"Stands {reach} back up {hp}." + (" They're left Wounded." if a.get("wound") else "")
    if k == "flee": return "Escape the fight, for certain." if a.get("item") else "Try to run."
    if k == "defend": return "Halve the damage you take this round. Acts first."
    if k == "cover": return "Take the hits meant for one ally this round. Acts first."
    if k == "move": return "Step to another spot, or swap with the ally there."
    return ""

# ================================================================ characters
class Unit:
    def __init__(self, name, side, level, attrs, atk_w, mat_w, aff, actions, cls=None, sign=None,
                 personality=None):
        self.name, self.side, self.level, self.attrs = name, side, level, attrs
        self.cls, self.sign, self.personality = cls, sign, personality
        self.atk_w, self.mat_w, self.aff, self.actions = atk_w, mat_w, aff, actions
        self.maxhp = HP_MULT * (20 + 2 * attrs["CON"] + 2 * level)
        self.maxmp = 10 + attrs["WIS"] + level
        self.hp, self.mp = self.maxhp, self.maxmp
        self.actions_per_round = 1
        self.natural_fit = None
        self.horn = False
        self.body = {}
        self.stages = {k: 0 for k in ["ATK", "DEF", "MAT", "MDF", "ACC", "EVA", "SPD"]}   # each stat's own stacks
        self.pushed = set()       # stats pushed this round: they don't step toward zero at its end
        self.status = {}          # name -> dict(rounds=..., ...)
        self.defending = False
        self.bide = None          # (action, target) wound up last round, fires this round (Bid- moves)
        self.covered_by = None    # an ally who Covers this unit this round (combat_spec Part 8)
        self.once_used = set()    # once-per-fight moves already spent (Net Throw)
        self.state = "up"          # heroes: up, dying, dead (combat_spec Part 10)
        self.breaths = 0
        self.wounded = False
        self.pouch = []            # [[item key, count], ...], at most POUCH_SLOTS
        self.stats = dict(dealt=0.0, healed=0.0, weak=0, crit=0, graze=0, hits=0, statuses=0,
                          bonus=0, actions=0, downs=0, defends=0, blocked=0.0, late=0,
                          rear_melee=0, fizzles=0, moves=0, illegal=0, bides=0, bides_lost=0, flurry_hits=0,
                          swaps=0, covers=0, covered=0.0, paints=0, spot_ticks=0)

    alive = property(lambda s: s.hp > 0)
    def weighted(self, w): return sum(self.attrs[k] * v for k, v in w.items())
    def b(self, k): return self.body.get(k, 1.0)
    ATK = property(lambda s: s.weighted(s.atk_w) * s.b("ATK"))
    MAT = property(lambda s: s.weighted(s.mat_w) * s.b("MAT"))
    DEF = property(lambda s: s.attrs["CON"] * s.b("DEF"))
    MDF = property(lambda s: s.attrs["WIS"] * s.b("MDF"))
    WIL = property(lambda s: s.attrs["WIL"] * s.b("WIL"))

    def apply_body(self, family, type_=None):
        self.body = dict(FAMILY_BODIES.get(family, {}))
        if type_ and self.body and TYPE_LEAN:                 # the Type tilts the family's attack line its way
            up, down = ("ATK", "MAT") if type_ == "Martial" else ("MAT", "ATK")
            if TYPE_LEAN == "swap":
                if self.body[up] < self.body[down]: self.body[up], self.body[down] = self.body[down], self.body[up]
            else:
                self.body[up] += TYPE_TILT; self.body[down] -= TYPE_TILT
        self.maxhp *= self.b("HP"); self.hp = self.maxhp

    def stage(self, stat):
        return clamp(self.stages[stat] + status_stat(self, stat), -STACK_CAP, STACK_CAP)

    def has_flag(self, flag):
        """Does any status this unit carries set this flag (no_orders, blocks_mp, breaks_bide...)? A flag of "sure"
        holds only while the status's next roll is certain (a fresh freeze: no orders; a thawing one: orders)."""
        for s, inst in self.status.items():
            v = STATUSES.get(s, {}).get(flag)
            if v == "sure": v = STATUSES[s]["fade"][inst.get("step", 0)] >= 1.0
            if v: return True
        return False

    def counter_name(self, stat):
        """The name a stat's counter shows (Blinded 2, Quick 1), or None at zero or for an unnamed stat."""
        n = self.stage(stat)
        name = STAT_NAMES[stat][0 if n < 0 else 1] if n else None
        return f"{name} {abs(n)}" if name else None

    silenced = property(lambda s: s.has_flag("blocks_mp"))

    def speed(self): return self.attrs["SPD"] * self.b("SPD") * stage_mult(self.stage("SPD"))
    def affinity(self, element):
        if element == "Force": return "normal"            # affinity-free (Firecracker, Thunderpot)
        return self.aff.get(element, "normal")

    def can_afford(self, a):
        if a["cost_type"] == "MP": return self.mp >= a["cost"]
        if a["pct_current"]: return self.hp > 1
        return self.hp > a["cost"]

    def pay(self, a):
        if a["cost_type"] == "MP": self.mp -= a["cost"]
        elif a["pct_current"]: self.hp -= max(1, int(self.hp * a["pct_current"]))
        else: self.hp -= a["cost"]

def status_stat(u, stat):
    """What u's statuses do to one stat, in stages (Chilled: SPD -1; a Curse's rolled stats)."""
    n = 0
    for s, inst in u.status.items():
        row = STATUSES.get(s, {})
        n += row.get("stats", {}).get(stat, 0)
        if "pick" in row: n -= inst.get("stats", []).count(stat)
    return n

def build_aff(resist=(), weak=(), null=(), absorb=()):
    aff = {}
    for kind, elems in (("resist", resist), ("weak", weak), ("null", null), ("absorb", absorb)):
        for e in elems: aff[e] = kind
    return aff

def roll_normal(rng):
    """A person before any class: genes, Personality, Star Sign."""
    return dict(genes={k: rng.randint(0, 31) for k in ATTRS},
                personality=tuple(rng.sample(ATTRS, 2)), sign=rng.choice(ZODIAC))

def feeders(cls):
    c = CLASSES[cls]
    return c["mat"] if c["kind"] == "magical" else c["atk"]

def class_growth(cls):
    """Budget-neutral tilt: weapon feeders grow faster, everything else slightly slower."""
    g = {k: 1.0 for k in ATTRS}
    if cls is None: return g
    w = feeders(cls)
    others = [k for k in ATTRS if k not in w]
    for k in others: g[k] = 1.0 - CLASS_TILT / len(others)
    for k, v in w.items(): g[k] = 1.0 + CLASS_TILT * v
    return g

def natural_attrs(n, level, cls=None, training=None):
    boost, cut = n["personality"]
    cg = class_growth(cls)
    a = {}
    for k in ATTRS:
        p = 1 + PERSONALITY_MULT if k == boost else 1 - PERSONALITY_MULT if k == cut else 1.0
        a[k] = attr_at(n["genes"][k], level, p * cg[k])
    if training and cls:
        t = CLASSES[cls]["train"]
        a[t[0]] += (level - 1)
        if training == "2pt": a[t[1]] += (level - 1)
    shift = 0.10 * max(a.values())
    up, down = n["sign"][5]
    a[up] += shift
    a[down] = max(1, a[down] - shift)
    return a

def class_fit(n):
    """How well each class's weapon feeders match this person's natural body (projected to L30)."""
    a = natural_attrs(n, 30)
    mean = sum(a.values()) / len(a)
    return {c: sum(a[k] * w for k, w in feeders(c).items()) / mean for c in CLASSES}

def roll_class(n, rng):
    fit = class_fit(n)
    classes = list(fit)
    weights = [fit[c] ** FIT_EXPONENT for c in classes]
    return rng.choices(classes, weights)[0]

def is_natural_fit(n, cls):
    """A 'sensible' recruit: the class's feeder profile is among this body's top two profiles."""
    fit = class_fit(n)
    profiles = sorted({round(v, 6) for v in fit.values()}, reverse=True)
    return round(fit[cls], 6) in profiles[:2]

def birth(cls, level, rng, training="1pt", name=None, normal=None):
    n = normal or roll_normal(rng)
    c = CLASSES[cls]
    attrs = natural_attrs(n, level, cls, training)
    _, eres, eweak, mres, mweak, _ = n["sign"]
    if c["kind"] == "magical":
        sa = SCHOOL_AFFINITY[c["school"]]
        aff = build_aff(resist=sa["resist"] + [mres], weak=sa["weak"] + [mweak])
    else:
        aff = build_aff(resist=[eres, CHILD_OF[eres]], weak=[c["weak"], eweak, CHILD_OF[eweak]])
    u = Unit(name or cls, "party", level, attrs, c["atk"], c["mat"], aff, loadout(cls, level),
             cls=cls, sign=n["sign"][0], personality=n["personality"])
    u.natural_fit = is_natural_fit(n, cls)
    return u

def recruit(level, rng, training="1pt"):
    n = roll_normal(rng)
    return birth(roll_class(n, rng), level, rng, training, normal=n)

ENEMY_TRAIN = 0.45   # extra per level into the creature's attack attribute, CON, and WIS

def spawn(kind, level, name=None):
    e = ENEMIES[kind]
    attrs = {k: attr_at(15.5, level) for k in ATTRS}
    main = max(e["atk"], key=e["atk"].get)
    attrs[main] += ENEMY_TRAIN * (level - 1)
    attrs["CON"] += ENEMY_TRAIN * (level - 1)
    attrs["WIS"] += ENEMY_TRAIN * (level - 1)   # keep DEF and MDF symmetric
    actions = []
    for a in e["actions"]:
        if a[0] == "strike": actions.append(strike(a[1], a[2], ENEMY_STRIKE_POWER))
        elif a[0] == "spell": actions.append(damage_spell(a[1], a[2], a[3]))
        elif a[0] == "skill": actions.append(skill(a[1], a[4], a[2], all_=a[3]))
    return Unit(name or kind, "enemy", level, attrs, e["atk"], e["mat"], build_aff(**e["aff"]),
                actions)

# ================================================================ battle
class Battle:
    def __init__(self, party, enemies, rng, log=False, events=False):
        self.party, self.enemies, self.rng = party, enemies, rng
        self.units = party + enemies
        self.spots = {}            # (side, cell) -> dict(src, a, rounds): painted spots (Mark- moves)
        self.lines = [] if log else None
        self.events = [] if events else None   # structured events for the front-end (see emit)
        self.piles = {}            # fallen Bein -> rounds until they stand again (Barrow rule)
        self.fled = False
        self.uid_of = {}           # battle name -> fixed id (a Mogel that re-forms keeps its id)
        names = [u.name for u in self.units]
        for u in self.units:       # two heroes of one class, say: letter them, as the composer letters enemies
            if names.count(u.name) > 1:
                n = sum(1 for x in self.units[:self.units.index(u)] if x.name.split(" ")[0] == u.name)
                u.name = f"{u.name} {chr(65 + n)}"
        for side, team in (("p", party), ("e", enemies)):
            for i, u in enumerate(team):
                u.uid = f"{side}{i}"; self.uid_of[u.name] = u.uid
        self.round = 0
        self.bonus_rounds = 0
        self.eligible, self.barred = set(), set()
        self.pending_defend = set()
        self.control, self.phase, self.waiting, self.orders, self.remaining = None, "new", [], {}, []
        self.max_rounds, self.winner, self._mark = 30, None, 0
        self.intents, self.no_flee, self.coin = {}, False, {}     # no_flee: the Hunt's top tiers can't be run from
        self.by_uid = {u.uid: u for u in self.units}
        if USE_BOARD:
            self.form_up(self.party); self.form_up(self.enemies)

    # ------------------------------------------------------------ the board
    def wants_front(self, u):
        """Front-liners: martial heroes, and enemies whose damage is mostly martial (Mogel, Draugr...)."""
        if u.side == "party": return CLASSES.get(u.cls, {}).get("kind") == "martial"
        if getattr(u, "family", None) == "Mogel": return True
        dmg = [a for a in u.actions if a["kind"] == "damage"]
        melee = sum(a["element"] in MARTIAL and a.get("reach") != "any" for a in dmg)   # archers keep back
        return melee * 2 >= len(dmg) and melee > 0

    def form_up(self, team):
        """Give every unit without a cell one: front-liners Front, others Rear, overflow to the other row,
        and never an empty Front while the Rear holds someone."""
        taken = {getattr(u, "cell", None) for u in team} - {None}
        def free(row): return [l for l in range(3) if (row, l) not in taken]
        for u in sorted([u for u in team if getattr(u, "cell", None) is None], key=lambda u: -u.actions_per_round):
            want = "front" if self.wants_front(u) else "rear"
            other = "rear" if want == "front" else "front"
            row = want if free(want) else other
            u.cell = (row, free(row)[0]); taken.add(u.cell)
        if not any(u.cell[0] == "front" for u in team) and team:
            u = max(team, key=lambda x: x.maxhp); u.cell = ("front", free("front")[0])

    def eff_front(self, team):
        """The units that count as a side's Front for targeting (exposure: an empty Front exposes the Rear)."""
        alive = [x for x in team if x.alive]
        front = [x for x in alive if x.cell[0] == "front"]
        return front or alive

    def team_of(self, u): return self.party if u.side == "party" else self.enemies

    def front_ok_without(self, u):
        """Would u's side still have someone in the Front if u left it?"""
        return u.cell[0] != "front" or any(x.alive and x is not u and x.cell[0] == "front" for x in self.team_of(u))

    def reach_mult(self, u, a, t):
        """Damage multiplier if u can reach t with a, else None."""
        if not USE_BOARD or a["target"] in ("ally", "self") or a["element"] not in MARTIAL: return 1.0
        reach = a.get("reach") or REACH_BY_TYPE[a["element"]]
        if reach == "any": return 1.0
        in_front = t in self.eff_front(self.team_of(t))
        mine_front = u.cell[0] == "front"
        if reach == "melee": return (1.0 if mine_front else REAR_MELEE_MULT) if in_front else None
        return 1.0 if (mine_front or in_front) else None          # reach (Pierce)

    def shape_targets(self, u, a, t):
        shape = a.get("shape", "single")
        if not USE_BOARD:                                # no board, no rows: a row skill hits the whole side
            return [x for x in self.team_of(t) if x.alive] if shape == "row" else [t]
        if shape == "row":
            return [x for x in self.team_of(t) if x.alive and x.cell[0] == t.cell[0] and self.reach_mult(u, a, x) is not None]
        if shape == "column":
            behind = [x for x in self.team_of(t) if x.alive and x.cell == ("rear", t.cell[1]) and x is not t]
            return [t] + [x for x in behind if t.cell[0] == "front" and self.reach_mult(u, a, x) is not None]
        return [t]

    def say(self, s):
        if self.lines is not None: self.lines.append(s)

    def emit(self, kind, text=None, **data):
        """One thing that happened, as data: the front-end draws from these, the prose log reads from `text`.
        Units are named by their unique battle name; cells are (row, lane)."""
        if self.events is not None:
            ev = dict(kind=kind, round=self.round, **data)
            for k in UNIT_KEYS:                         # every unit named also gets its fixed id
                v = data.get(k)
                if isinstance(v, str) and v in self.uid_of: ev[k + "_id"] = self.uid_of[v]
            if isinstance(data.get("targets"), list):
                ev["target_ids"] = [self.uid_of.get(t["unit"] if isinstance(t, dict) else t) for t in data["targets"]]
            if text: ev["text"] = text.strip()
            self.events.append(ev)
        if text is not None: self.say(text)

    def downed(self, t, by=None):
        """A unit just hit 0 HP. Most stay down; a Mogel re-forms one size smaller in the same cell; a Draugr that
        wasn't beheaded or burned crawls on; a Bein falls into a pile that stands again unless it is crushed.
        `by` is the element of the killing blow (None for ticks and the like)."""
        fam = getattr(t, "family", None)
        if t.side == "party" and USE_DYING:
            if t.wounded:
                self.die(t, "falls while Wounded"); return
            t.state, t.breaths, t.fell_round, t.hp = "dying", HERO_BREATHS, self.round, 0
            t.status = {}; t.stats["downs"] += 1
            self.emit("dying", f"      {t.name} falls, dying! ({t.breaths} breaths)", unit=t.name, breaths=t.breaths)
            return
        if fam == "Draugr" and by not in DRAUGR_FINAL and not getattr(t, "crawling", False):
            t.crawling = True; t.hp = t.maxhp * DRAUGR_CRAWL_HP
            claw = family_move(("strike", "Slash", "Claw", "Halv"))
            t.actions = [claw]; t.actions_per_round = 1
            self.emit("crawl", f"      {t.name} falls, and crawls on! ({t.hp:.0f}/{t.maxhp:.0f})", unit=t.name,
                      hp=round(t.hp), maxhp=round(t.maxhp))
            return
        if fam == "Bein" and by != "Crush" and not getattr(t, "piled", False):
            t.piled = True; self.piles[t] = BEIN_PILE_ROUNDS; t.stats["downs"] += 1
            self.emit("pile", f"      {t.name} falls into a pile of bones.", unit=t.name, rounds=BEIN_PILE_ROUNDS)
            return
        nxt = MOGEL_REFORM.get(getattr(t, "mogel_rank", None)) if fam == "Mogel" else None
        if not nxt:
            self.emit("down", f"      {t.name} is down!", unit=t.name); t.stats["downs"] += 1
            return
        old = t.name
        fresh = spawn_mogel(nxt, t.element, t.level)
        keep = dict(stats=t.stats, side=t.side, suffix=getattr(t, "suffix", ""), reforms=getattr(t, "reforms", 0),
                    cell=getattr(t, "cell", None))
        t.__dict__.update(fresh.__dict__)
        t.stats, t.side, t.suffix, t.reforms = keep["stats"], keep["side"], keep["suffix"], keep["reforms"] + 1
        t.cell = keep["cell"]
        t.name = fresh.name + t.suffix
        others = {x.name for x in self.units if x is not t}
        uid = self.uid_of.get(old)
        if t.name in others:                                    # re-formed into a name already on the board
            for ch in "ABCDEFGH":
                if f"{fresh.name} {ch}" not in others: t.suffix = f" {ch}"; t.name = fresh.name + t.suffix; break
        if uid: self.uid_of[t.name] = uid
        t.hp = t.maxhp * MOGEL_REFORM_HP
        self.emit("reform", f"      {old} bursts and re-forms as {t.name}! ({t.hp:.0f}/{t.maxhp:.0f})", unit=t.name, was=old, rank=t.mogel_rank, hp=round(t.hp), maxhp=round(t.maxhp))

    def allies(self, u): return [x for x in (self.party if u.side == "party" else self.enemies) if x.alive]
    def foes(self, u): return [x for x in (self.enemies if u.side == "party" else self.party) if x.alive]
    def over(self): return self.fled or not any(x.alive for x in self.party) or not any(x.alive for x in self.enemies)

    # ------------------------------------------------------------ roll
    def horn_bonus(self, u):
        return 1 if any(x.horn for x in self.allies(u)) else 0

    def speed_shift(self, att, dfn):
        r = att.speed() / max(0.01, dfn.speed())
        steps = int((r - 1) / SPEED_STEP) if r >= 1 else -int((1 / r - 1) / SPEED_STEP)
        return clamp(steps, -SPEED_CAP, SPEED_CAP)

    def net_stage(self, att, dfn):
        return clamp(att.stage("ACC") + self.horn_bonus(att) + self.speed_shift(att, dfn)
                     - dfn.stage("EVA"), -5, 5)

    def roll(self, att, dfn, a=None):
        net = self.net_stage(att, dfn)
        graze = max(0.0, GRAZE_BASE - STEP * net)
        crit = CRIT_BASE + max(0, net - 2) * 0.05 + att.attrs["DEX"] / 20 / 100 + (a or {}).get("crit_bonus", 0.0)
        r = self.rng.random()
        if r < graze: return "graze"
        if r < graze + crit: return "crit"
        return "hit"

    def expected_roll_mult(self, att, dfn, a=None):
        a = a or {}
        net = self.net_stage(att, dfn)
        graze = max(0.0, GRAZE_BASE - STEP * net)
        crit = CRIT_BASE + max(0, net - 2) * 0.05 + att.attrs["DEX"] / 20 / 100 + a.get("crit_bonus", 0.0)
        m = graze * GRAZE_MULT + crit * a.get("crit_mult", CRIT_MULT) + (1 - graze - crit)
        if a.get("flurry"):
            f = a["flurry"]; p = clamp(f["p"] + f["step"] * net, 0.05, 0.95)
            m *= f["per"] * sum(p ** i for i in range(f["max"]))
        return m

    def flurry_count(self, att, dfn, f):
        """Drif: the first hit always lands; each coin flip won adds one more, up to the max."""
        p = clamp(f["p"] + f["step"] * self.net_stage(att, dfn), 0.05, 0.95); n = 1
        while n < f["max"] and self.rng.random() < p: n += 1
        return n

    def wil_ratio(self, att, dfn): return clamp(att.WIL / dfn.WIL, 0.5, 1.5)

    # ------------------------------------------------------------ damage
    def raw_damage(self, att, dfn, a):
        el = ELEMENT[a["element"]]
        phys = a["element"] in MARTIAL
        A = (att.ATK if phys else att.MAT) * stage_mult(att.stage("ATK" if phys else "MAT"))
        if a.get("fixed"): A = avg_attr(att.level)                    # an item: an average person's blow
        if a["element"] == "Force": phys = True                       # affinity-free blast, met by DEF
        D = (dfn.DEF if phys else dfn.MDF) * stage_mult(dfn.stage("DEF" if phys else "MDF"))
        dmg = a["power"] * el["power"] * (A / D) * level_factor(att.level)
        if a["all"]: dmg *= ALL_POWER_MULT
        return dmg

    def expected_damage(self, att, dfn, a):
        aff = dfn.affinity(a["element"])
        mult = {"weak": 1.5, "resist": 0.5, "null": 0.0, "absorb": -1.0, "normal": 1.0}[aff]
        hits = a.get("hits") or ELEMENT[a["element"]]["hits"]
        return self.raw_damage(att, dfn, a) * hits * mult * self.expected_roll_mult(att, dfn, a)

    def heal_amount(self, healer, a):
        h = 1.5 * a["power"] * level_factor(healer.level) * healer.MAT / avg_attr(healer.level)
        return h * (ALL_POWER_MULT if a["all"] else 1)

    # ------------------------------------------------------------ statuses
    def push(self, t, stat, n):
        """Move a stat's counter n stacks (up and down cancel), capped; it holds this round."""
        t.stages[stat] = clamp(t.stages[stat] + n, -STACK_CAP, STACK_CAP); t.pushed.add(stat)

    def capped(self, t, status):
        """Is a counter status already as deep as it goes on t (Blinded 3)? Then landing it again does nothing."""
        if status not in COUNTER_OF: return status in t.status
        stat, sign = COUNTER_OF[status]
        return t.stage(stat) * sign >= STACK_CAP

    def apply_status(self, src, tgt, status, chance, stacks=1):
        if not tgt.alive or self.rng.random() >= chance: return False
        if STATUSES.get(status, {}).get("boss_immune") and getattr(tgt, "rank", None) == "Drott":
            self.emit("immune", f"      {tgt.name} shrugs off {status}.", unit=tgt.name, status=status); return False
        if status in COUNTER_OF:                        # a named counter: Blinded is ACC down
            stat, sign = COUNTER_OF[status]
            self.push(tgt, stat, sign * stacks)
            src.stats["statuses"] += 1
            shown = tgt.counter_name(stat) or STAT_NAMES[stat][0 if sign < 0 else 1] or status
            self.emit("status", f"      {tgt.name} is {shown}!", unit=tgt.name, status=STAT_NAMES[stat][0 if sign < 0 else 1] or status,
                      stat=stat, stacks=tgt.stage(stat), src=src.name)
            return True
        if status == "Death":
            tgt.hp = 0
            src.stats["statuses"] += 1
            self.emit("status", f"      {tgt.name} is struck down by Helvad!", unit=tgt.name, status="Death", src=src.name)
            return True
        else:
            row = STATUSES.get(status, dict(duration=STATUS_DURATION, reapply="refuse"))
            if row["reapply"] == "refuse" and status in tgt.status: return False
            inst = {}
            if "pick" in row:
                pool, n = row["pick"]; inst["stats"] = [self.rng.choice(pool) for _ in range(n)]
            d = row["duration"]
            inst["rounds"] = UNTIL_USED if d is None else self.rng.randint(*d) if isinstance(d, tuple) else d
            if "fade" in row: inst["step"] = 0
            tgt.status[status] = inst
        src.stats["statuses"] += 1
        self.emit("status", f"      {tgt.name} is {status}!", unit=tgt.name, status=status, src=src.name)
        return True

    def riders(self, att, tgt, a, result, was_weak):
        el = ELEMENT[a["element"]]
        if result == "graze" or not tgt.alive: return
        if a["status"]:      # martial skill with a status (Blot)
            self.apply_status(att, tgt, a["status"], STATUS_LINE_CHANCE[a["tier"]] * self.wil_ratio(att, tgt))
        rider = el["rider"]
        if not rider or a["tier"] == "Halv": return
        chance = RIDER_CHANCE[a["tier"]] * self.wil_ratio(att, tgt)
        chain = STATUSES.get(rider, {}).get("chain")
        if chain:                       # Chilled on the Chilled becomes Frozen; a weakness always lands the first step
            if rider in tgt.status and chain not in tgt.status:
                self.apply_status(att, tgt, chain, chance)
            elif rider not in tgt.status:
                self.apply_status(att, tgt, rider, 1.0 if was_weak else chance)
        else:
            self.apply_status(att, tgt, rider, chance)

    # ------------------------------------------------------------ resolve one action
    # ------------------------------------------------------------ the fallen hero (combat_spec Part 10)
    def die(self, t, why):
        t.state, t.breaths, t.hp = "dead", 0, 0
        self.emit("dead", f"      {t.name} dies ({why}).", unit=t.name, why=why)

    def dying(self): return [x for x in self.party if x.state == "dying"]

    def lose_breath(self, t, by=None):
        t.breaths -= 1
        self.emit("breath", f"      {t.name} loses a breath ({t.breaths} left).", unit=t.name, breaths=t.breaths,
                  src=by.name if by else None)
        if t.breaths <= 0: self.die(t, "bled out" if by is None else f"struck down by {by.name}")

    def tick_breaths(self):
        for t in self.dying():
            if t.fell_round != self.round: self.lose_breath(t)

    def stand_up(self, t, hp, wound):
        """Up again, in its own spot if free, else the nearest free one."""
        if USE_BOARD and getattr(t, "cell", None):
            taken = {x.cell for x in self.team_of(t) if x.alive}
            if t.cell in taken:
                t.cell = next(((r, l) for r in (t.cell[0], "rear" if t.cell[0] == "front" else "front")
                               for l in range(3) if (r, l) not in taken), t.cell)
        if wound and not t.wounded:
            t.wounded = True; t.maxhp *= 1 - WOUNDED_CUT; t.maxmp = getattr(t, "maxmp", 0) * (1 - WOUNDED_CUT)
            t.mp = min(getattr(t, "mp", 0), t.maxmp)
        t.state, t.breaths = "up", 0
        t.hp = max(1.0, min(t.maxhp, 1 + hp * t.maxhp))

    def fallen_reach(self, u, a, p):
        """Can u land a finishing blow on Dying hero p? Reach as for a pile: the Front, or an exposed Rear."""
        if a["kind"] != "damage" or a["all"] or a.get("shape") or p.state != "dying" or p.side == u.side: return None
        if not USE_BOARD: return 1.0
        reach = a.get("reach") or REACH_BY_TYPE.get(a["element"], "any")
        if reach == "any" or a["element"] not in MARTIAL: return 1.0
        exposed = not any(x.alive and x.cell[0] == "front" for x in self.team_of(p))
        if p.cell[0] != "front" and not exposed: return None
        return 1.0

    # ------------------------------------------------------------ items
    def item_actions(self, u):
        return [item_move(k) for k, n in u.pouch if n > 0]

    def use_item(self, u, a):
        for slot in u.pouch:
            if slot[0] == a["item"]:
                slot[1] -= 1
                if slot[1] <= 0: u.pouch.remove(slot)
                return True
        return False

    def pile_reach(self, u, a, p):
        """Can u bring a Crush down on pile p? Melee reaches a pile in the Front (half from the Rear); a spell anywhere."""
        if a["kind"] != "damage" or a["element"] != "Crush" or a["all"] or a.get("shape") or p not in self.piles: return None
        if p.side == u.side: return None
        if not USE_BOARD: return 1.0
        reach = a.get("reach") or REACH_BY_TYPE["Crush"]
        if reach == "any": return 1.0
        exposed = not any(x.alive and x.cell[0] == "front" for x in self.team_of(p))   # an empty Front exposes the Rear
        if p.cell[0] != "front" and not exposed: return None
        return 1.0 if u.cell[0] == "front" else REAR_MELEE_MULT

    def scatter(self, u, a, p):
        del self.piles[p]; u.stats["actions"] += 1
        self.emit("scatter", f"    {u.name} uses {self.shown(u, a)}: the bones of {p.name} scatter for good.",
                  unit=u.name, move=a["name"], shown=self.shown(u, a), target=p.name)

    def tick_piles(self):
        for p in list(self.piles):
            self.piles[p] -= 1
            if self.piles[p] > 0: continue
            taken = {x.cell for x in self.team_of(p) if x.alive}
            cell = p.cell if p.cell not in taken else next(((r, l) for r in (p.cell[0], "rear" if p.cell[0] == "front" else "front")
                                                           for l in range(3) if (r, l) not in taken), None)
            if cell is None: continue                     # nowhere to stand: it waits
            del self.piles[p]; p.cell = cell; p.hp = p.maxhp * BEIN_REASSEMBLE_HP; p.status = {}
            self.emit("reassemble", f"    The bones of {p.name} stand up again! ({p.hp:.0f}/{p.maxhp:.0f})",
                      unit=p.name, cell=cell, hp=round(p.hp), maxhp=round(p.maxhp))

    def targets_for(self, u, a, chosen):
        if a["target"] == "self": return [u]
        pool = self.allies(u) if a["target"] == "ally" else self.foes(u)
        pool = [x for x in pool if self.reach_mult(u, a, x) is not None]
        if not pool:
            u.stats["fizzles"] += 1
            self.emit("fizzle", f"    {u.name} has no one in reach for {self.shown(u, a)}.", unit=u.name, move=a["name"], shown=self.shown(u, a))
            return []
        if a["all"]: return pool
        if chosen in pool: return self.shape_targets(u, a, chosen)
        if a["target"] == "ally":
            out = [min(pool, key=lambda x: x.hp / x.maxhp)]
        elif chosen is not None and USE_BOARD and any(x.cell[0] == chosen.cell[0] for x in pool):
            same = [x for x in pool if x.cell[0] == chosen.cell[0]]       # retarget: same row first, then anyone legal
            out = self.shape_targets(u, a, self.rng.choice(same))
        else:
            out = self.shape_targets(u, a, self.rng.choice(pool))
        if chosen is not None and out:
            why = "is down" if not chosen.alive else "is out of reach"
            self.emit("retarget", f"    {chosen.name} {why}; {u.name} turns on {out[0].name} instead.", unit=u.name,
                      move=a["name"], was=chosen.name, target=out[0].name, why="down" if not chosen.alive else "reach")
        return out

    def tick_statuses(self, u, when):
        """Statuses that cost HP at this moment ("round_start": Poison; "action": Bleeding). False if u went down."""
        for s, row in STATUSES.items():
            tk = row.get("tick")
            if not tk or tk["when"] != when or s not in u.status or not u.alive: continue
            dmg = max(1, int(u.maxhp * tk["share"])); u.hp -= dmg
            self.emit("tick", "    " + tk["line"].format(name=u.name, dmg=dmg), unit=u.name, status=s, dmg=dmg, hp=max(0, round(u.hp)))
            if not u.alive:
                self.downed(u)
                if not u.alive: return False
        return True

    def skips(self, u):
        """Does a status take this action away (the net, ice, a stun)? Checked in SKIP_ORDER; the first that fires wins."""
        for s in SKIP_ORDER:
            row = STATUSES[s]; sk = row.get("skip")
            if s not in u.status or not sk: continue
            if "fade" in row:                         # Frozen: sure, then 50%, then 20%; a failed roll thaws it
                inst = u.status[s]; ch = row["fade"][inst["step"]]
                if ch < 1.0 and self.rng.random() >= ch:
                    del u.status[s]; self.emit("thaw", "    " + row["thaw"].format(name=u.name), unit=u.name, status=s); continue
                inst["step"] += 1
                if inst["step"] >= len(row["fade"]): del u.status[s]
                self.emit("skip", "    " + sk["line"].format(name=u.name), unit=u.name, why=s); return True
            if sk["chance"] < 1.0 and self.rng.random() >= sk["chance"]: continue
            if sk["used_up"]: del u.status[s]
            self.emit("skip", "    " + sk["line"].format(name=u.name), unit=u.name, why=s); return True
        return False

    def resolve(self, u, a, chosen, bonus):
        if not u.alive: return
        if not self.tick_statuses(u, "action"): return
        if a.get("_release") and u.has_flag("breaks_bide"):
            for s in [s for s in u.status if STATUSES.get(s, {}).get("bide_pops")]: del u.status[s]
            u.stats["bides_lost"] += 1
            self.emit("bide_lost", f"    {u.name} loses {self.shown(u, a)}!", unit=u.name, move=a["name"], shown=self.shown(u, a)); return
        if self.skips(u): return
        if u.silenced and a["cost_type"] == "MP" and a["cost"] > 0:
            free = [x for x in u.actions if x["cost"] == 0]
            if not free:
                self.emit("skip", f"    {u.name} is silenced and can't act!", unit=u.name, why="Silenced"); return
            a = free[0]; self.emit("silenced", f"    {u.name} is silenced!", unit=u.name)
        if not u.can_afford(a):
            affordable = [x for x in u.actions if u.can_afford(x)
                          and not (u.silenced and x["cost_type"] == "MP" and x["cost"] > 0)]
            if not affordable:
                self.emit("skip", f"    {u.name} has nothing left to use.", unit=u.name, why="spent"); return
            a = min(affordable, key=lambda x: x["cost"])
        if a.get("bide") and not a.get("_release"):        # Bid-: pay now, wind up, fire next round
            u.pay(a); u.stats["actions"] += 1; u.stats["bides"] += 1
            u.bide = (a, chosen)
            self.emit("windup", f"    {u.name} winds up {self.shown(u, a)}...{' [Bonus]' if bonus else ''}", unit=u.name, move=a["name"], shown=self.shown(u, a), target=chosen.name if chosen else None); return
        if a.get("spot") and USE_BOARD:                  # without the board there is no space: a plain hit
            self.paint(u, a, chosen, bonus); return
        if a.get("item"):
            if not self.use_item(u, a): return             # the pouch ran dry
            self.emit("item", f"    {u.name} uses a {a['name']}.{' [Bonus]' if bonus else ''}", unit=u.name, item=a["item"], name=a["name"],
                      target=chosen.name if chosen is not None else None)
        if a["kind"] == "flee":
            if not a.get("item"):                       # a Smoke Pot always works; running is a coin weighted by SPD
                ch = self.flee_chance(u)
                if self.rng.random() >= ch:
                    self.emit("flee_failed", f"    {u.name} tries to run, but can't get away!", unit=u.name, chance=round(ch, 2)); return
                self.fled = True; self.emit("fled", f"    {u.name} leads the party away!", unit=u.name); return
            self.fled = True; self.emit("fled", "    The party slips away in the smoke.", unit=u.name); return
        if a["kind"] == "revive":
            t = chosen if chosen is not None and chosen.side == u.side else None
            ok = t is not None and (t.state == "dying" or (t.state == "dead" and a["reaches"] == "Dead"))
            if not ok: return
            u.pay(a); u.stats["actions"] += 1
            was = t.state; self.stand_up(t, a["hp"], a["wound"] or was == "dead")
            self.emit("revive", f"    {u.name} {'uses' if a.get('item') else 'casts'} {a['name']}: {t.name} stands! ({t.hp:.0f}/{t.maxhp:.0f})",
                      unit=u.name, target=t.name, move=a["name"], was=was, hp=round(t.hp), wounded=t.wounded)
            return
        if a["kind"] == "mp":
            t = chosen if chosen is not None and chosen.alive else u
            got = min(a["amount"] * t.maxmp, t.maxmp - t.mp); t.mp += got
            self.emit("mp", f"    {t.name} recovers {got:.0f} MP.", unit=t.name, amount=round(got)); return
        if a["kind"] == "heal" and a.get("item"):
            t = chosen if chosen is not None and chosen.alive else u
            got = min(a["amount"] * t.maxhp, t.maxhp - t.hp); t.hp += got
            self.emit("heal", f"    {t.name} recovers {got:.0f} HP.", unit=u.name, move=a["name"], element=None,
                      targets=[dict(unit=t.name, amount=round(got), hp=round(t.hp))]); return
        if chosen is not None and getattr(chosen, "state", "up") == "dying":   # a finishing blow on the fallen
            if self.fallen_reach(u, a, chosen) is not None:
                u.pay(a); u.stats["actions"] += 1
                self.emit("act", f"    {u.name} uses {self.shown(u, a)} on the fallen {chosen.name}.", unit=u.name,
                          move=a["name"], shown=self.shown(u, a), move_kind="damage", element=a["element"],
                          targets=[chosen.name], bonus=bonus)
                self.lose_breath(chosen, by=u); return
            chosen = None
        if chosen in self.piles:                           # a Crush meant for a pile of bones
            if self.pile_reach(u, a, chosen) is not None:
                u.pay(a); self.scatter(u, a, chosen); return
            chosen = None
        tgts = self.targets_for(u, a, chosen)
        if not tgts: return
        u.pay(a)
        if a.get("once"): u.once_used.add(a["name"])
        u.stats["actions"] += 1
        tag = " [Bonus]" if bonus else ""
        if a["kind"] == "move":
            if "cell" in a:                                     # Move to a spot, or Swap if an ally stands there
                dest = a["cell"]
                if dest == u.cell: return
                other = next((x for x in self.team_of(u) if x.alive and x is not u and x.cell == dest), None)
                if other is None and dest[0] != u.cell[0] and not self.front_ok_without(u):
                    return                                      # never leave the Front empty
                if other: other.cell = u.cell; u.stats["swaps"] += 1
                u.cell = dest; u.stats["moves"] += 1
                self.emit("move", f"    {u.name} {'swaps with ' + other.name if other else 'moves'} "
                          f"to the {dest[0].capitalize()}.{tag}", unit=u.name, cell=dest,
                          swapped=other.name if other else None, other_cell=other.cell if other else None); return
            taken = {x.cell for x in self.team_of(u) if x.alive and x is not u}
            lanes = [l for l in range(3) if (a["to"], l) not in taken]
            lanes.sort(key=lambda l: bool(self.painted(u, (a["to"], l))))      # a clean lane first
            if not lanes: return
            u.cell = (a["to"], lanes[0]); u.stats["moves"] += 1
            self.emit("move", f"    {u.name} steps up to the {a['to'].capitalize()}.{tag}", unit=u.name, cell=u.cell, advance=True); return
        if a["kind"] == "cover":
            t = tgts[0]
            if t is u or not t.alive: return
            t.covered_by = u; u.stats["covers"] += 1
            self.emit("cover", f"    {u.name} covers {t.name}.{tag}", unit=u.name, target=t.name); return
        if a["kind"] == "defend":
            u.defending = True; self.pending_defend.discard(u); u.stats["defends"] += 1
            self.emit("defend", f"    {u.name} defends.{tag}", unit=u.name); return
        if a["kind"] == "heal":
            healed = []
            for t in tgts:
                h = min(self.heal_amount(u, a), t.maxhp - t.hp)
                t.hp += h; u.stats["healed"] += h; healed.append(dict(unit=t.name, amount=round(h), hp=round(t.hp)))
            self.emit("heal", f"    {u.name} casts {a['name']}, healing {', '.join(t.name for t in tgts)}.{tag}",
                      unit=u.name, move=a["name"], element=a["element"], targets=healed)
            return
        if a["kind"] == "stat":
            n = STACKS_BY_TIER.get(a["tier"], 1)
            changes = [(a["stat"], a["direction"])] + list(a.get("also") or [])
            for t in tgts:
                for st, d in changes: self.push(t, st, d * n)
            self.emit("stat", f"    {u.name} casts {self.shown(u, a)} on {', '.join(t.name for t in tgts)}.{tag}", unit=u.name, move=a["name"], shown=self.shown(u, a), stat=a["stat"], direction=a["direction"], also=[list(c) for c in changes[1:]] or None, targets=[t.name for t in tgts])
            return
        if a["kind"] == "cleanse":
            for t in tgts:
                t.status = {}
                for s in t.stages: t.stages[s] = max(0, t.stages[s])
            self.emit("cleanse", f"    {u.name} casts {a['name']}, washing {', '.join(t.name for t in tgts)} clean.{tag}", unit=u.name, move=a["name"], targets=[t.name for t in tgts])
            return
        if a["kind"] == "status":
            said = f"{u.name} {a['line']}" if a.get("line") else f"{u.name} casts {self.shown(u, a)}."   # a row's own line: "throws a net!"
            self.emit("act", f"    {said}{tag}", unit=u.name, move=a["name"], shown=self.shown(u, a), move_kind="status", element=a["element"], targets=[t.name for t in tgts], bonus=bonus, tier=a.get("tier"), all=a["all"])
            if a.get("thrown") and len(tgts) == 1 and not a["all"]:        # Cover catches a thrown thing (the net)
                c = tgts[0].covered_by
                if c is not None and c.alive and c is not u and c.side == tgts[0].side:
                    self.emit("covered", f"      {c.name} takes it for {tgts[0].name}!", unit=c.name, instead_of=tgts[0].name); c.stats["covered"] += 1
                    tgts = [c]
            for t in tgts:
                stacks = STACKS_BY_TIER.get(a["tier"], 1)
                if a.get("sure"):
                    self.apply_status(u, t, a["status"], 1.0, stacks); continue
                res = self.roll(u, t)
                if res == "crit" and CRIT_EARNS_BONUS and not bonus: self.eligible.add(u)
                if res == "graze":
                    self.emit("resist", f"      {t.name} shrugs it off.", unit=t.name); continue
                if a["status"] == "Death":
                    aff = {"resist": 0.5, "weak": 1.5, "null": 0.0, "absorb": 0.0}.get(t.affinity("Aska"), 1.0)
                    chance = HELVAD_CHANCE * self.wil_ratio(u, t) * aff
                else:
                    chance = STATUS_LINE_CHANCE[a["tier"]] * self.wil_ratio(u, t)
                if self.apply_status(u, t, a["status"], chance, stacks) and not t.alive:
                    self.downed(t)
            return
        # damage
        self.emit("act", f"    {u.name} uses {self.shown(u, a)}.{tag}", unit=u.name, move=a["name"], shown=self.shown(u, a), move_kind="damage", element=a["element"], targets=[t.name for t in tgts], bonus=bonus, tier=a.get("tier"), all=a["all"])
        reach_as = {}                                   # a coverer runs into the ally's spot: reach is the ally's
        if len(tgts) == 1 and not a["all"] and not a.get("shape"):
            c = tgts[0].covered_by
            if c is not None and c.alive and c is not u and c.side == tgts[0].side:
                self.emit("covered", f"      {c.name} takes it for {tgts[0].name}!", unit=c.name, instead_of=tgts[0].name); c.stats["covered"] += 1
                reach_as = {c: tgts[0]}; tgts = [c]
        if a.get("flurry"):
            n = self.flurry_count(u, tgts[0], a["flurry"])       # one chain for the whole move
            self.emit("flurry", f"      {n} hit{'s' if n > 1 else ''}!", unit=u.name, hits=n)
            shaped = len(tgts) > 1 and not a["all"]
            for t in tgts: self.flurry(u, a, t, n, bonus, shaped, reach_as.get(t, t))
            return
        for ti, t in enumerate(tgts):
            if not t.alive: continue
            aff = t.affinity(a["element"])
            total, results, parts = 0.0, [], []
            for _ in range(a.get("hits") or ELEMENT[a["element"]]["hits"]):
                res = self.roll(u, t, a)
                results.append(res)
                dmg = self.raw_damage(u, t, a)
                var = ELEMENT[a["element"]]["var"]
                dmg *= 1 + self.rng.uniform(-var, var)
                dmg *= {"graze": GRAZE_MULT, "hit": 1.0, "crit": a.get("crit_mult", CRIT_MULT)}[res]
                dmg *= {"weak": 1.5, "resist": 0.5, "null": 0.0, "absorb": 1.0, "normal": 1.0}[aff]
                rm = self.reach_mult(u, a, reach_as.get(t, t))
                if rm is None: u.stats["illegal"] += 1; rm = 0.0
                if rm < 1.0: u.stats["rear_melee"] += 1
                dmg *= rm * (self.shape_mult(a, ti) if len(tgts) > 1 and not a["all"] else 1.0)
                if t.defending: t.stats["blocked"] += dmg * 0.5; dmg *= 0.5
                elif t in self.pending_defend: t.stats["late"] += 1       # hit before its own Defend landed
                sh = next((s for s in t.status if STATUSES.get(s, {}).get("shatter")), None)
                if sh and aff != "absorb":
                    dmg *= STATUSES[sh]["shatter"]
                    del t.status[sh]
                    self.emit("shatter", f"      Shatter!", unit=t.name)
                total += dmg; parts.append(dmg)
                u.stats[res if res != "hit" else "hits"] += 1
            if aff == "absorb":
                t.hp = min(t.maxhp, t.hp + total)
                self.emit("absorb", f"      {t.name} absorbs it, healing {total:.0f}!", unit=t.name, src=u.name, element=a["element"], amount=round(total), hp=round(t.hp))
                self.barred.add(u)
                if not bonus: self.eligible.add(t)
                continue
            t.hp -= total
            u.stats["dealt"] += total
            label = "/".join(r.capitalize() for r in results)
            extra = " Weak!" if aff == "weak" else " Resist." if aff == "resist" else " Null!" if aff == "null" else ""
            self.emit("hit", f"      {label} on {t.name}: {total:.0f}.{extra} ({max(0, t.hp):.0f}/{t.maxhp:.0f})", src=u.name, unit=t.name, element=a["element"], results=results, affinity=aff, dmg=round(total), hp=max(0, round(t.hp)), maxhp=round(t.maxhp),
                      parts=split_shown(parts, total) if len(parts) > 1 else None)
            if aff == "null": self.barred.add(u)
            if (aff == "weak" or (CRIT_EARNS_BONUS and "crit" in results)) and not bonus:
                self.eligible.add(u)
                if aff == "weak": u.stats["weak"] += 1
            if not t.alive:
                self.downed(t, a["element"]); continue
            best = "crit" if "crit" in results else "hit" if "hit" in results else "graze"
            self.riders(u, t, a, best, aff == "weak")

    def hit_once(self, u, a, t, res, per=1.0, shaped=False, spot=None):
        """One landed hit's damage after every multiplier (used by Drif, which lands hits one at a time)."""
        aff = t.affinity(a["element"])
        dmg = self.raw_damage(u, t, a) * per
        var = ELEMENT[a["element"]]["var"]
        dmg *= 1 + self.rng.uniform(-var, var)
        dmg *= {"graze": GRAZE_MULT, "hit": 1.0, "crit": a.get("crit_mult", CRIT_MULT)}[res]
        dmg *= {"weak": 1.5, "resist": 0.5, "null": 0.0, "absorb": 1.0, "normal": 1.0}[aff]
        rm = self.reach_mult(u, a, spot or t)
        if rm is None: u.stats["illegal"] += 1; rm = 0.0
        dmg *= rm * (SHAPE_MULT.get(a.get("shape", "single"), 1.0) if shaped else 1.0)
        if t.defending: t.stats["blocked"] += dmg * 0.5; dmg *= 0.5
        return dmg

    def bind_value(self, u, f, ref):
        """What netting f is worth: the action it would lose (its best blow or mend), more if it's winding up."""
        best = 0.0
        for x in f.actions:
            if x["kind"] == "damage": best = max(best, self.expected_damage(f, u, x))
            elif x["kind"] == "heal": best = max(best, 0.8 * ref)
        bide = self.expected_damage(f, f.bide[1], f.bide[0]) if f.bide is not None and f.bide[1] is not None else 0.0
        return NET_VALUE * best + NET_BIDE * bide

    def transform(self, u, job):
        """A unit takes up another job mid-fight (the net Drattr, net spent, takes up the spear). HP, statuses and
        stages stay; the kit, Type and art change."""
        row = rank_row(u.family, job)
        u.actions = [family_move(m) for m in row["moves"]]; price_shares(u)
        wield(u, row["opts"].get("weapon"))
        u.job, u.type = row["job"], row["type"]
        u.guard = bool(row["opts"].get("guard"))
        self.emit("transform", f"    {u.name} takes up the {row['opts'].get('takes', row['job'].lower())}.", unit=u.name, job=u.job)

    def shape_mult(self, a, i):
        """A shaped move's share for its i-th target: its own falloff (Skewer: 1.0, then 0.5), else the shape's."""
        if a.get("falloff"): return a["falloff"][min(i, len(a["falloff"]) - 1)]
        return SHAPE_MULT.get(a.get("shape", "single"), 1.0)

    def flurry(self, u, a, t, n, bonus, shaped=False, spot=None):
        """Drif: n hits, each rolled and applied on its own. A Mogel that re-forms mid-flurry takes the rest."""
        for i in range(n):
            if not t.alive: return
            aff = t.affinity(a["element"])
            res = self.roll(u, t, a)
            dmg = self.hit_once(u, a, t, res, a["flurry"]["per"], shaped, spot or t)
            u.stats[res if res != "hit" else "hits"] += 1; u.stats["flurry_hits"] += 1
            if aff == "absorb":
                t.hp = min(t.maxhp, t.hp + dmg); self.barred.add(u)
                if not bonus: self.eligible.add(t)
                self.emit("absorb", f"      {t.name} absorbs it, healing {dmg:.0f}!", unit=t.name, src=u.name, element=a["element"], amount=round(dmg), hp=round(t.hp)); return
            t.hp -= dmg; u.stats["dealt"] += dmg
            self.emit("hit", f"      {res.capitalize()} on {t.name}: {dmg:.0f}.{' Weak!' if aff == 'weak' else ''} ({max(0, t.hp):.0f}/{t.maxhp:.0f})", src=u.name, unit=t.name, element=a["element"], results=[res], affinity=aff, dmg=round(dmg), hp=max(0, round(t.hp)), maxhp=round(t.maxhp))
            if aff == "null": self.barred.add(u); return
            if aff == "weak" and not bonus:
                if u not in self.eligible: u.stats["weak"] += 1
                self.eligible.add(u)
            if not t.alive:
                self.downed(t, a["element"]); continue
            self.riders(u, t, a, res, aff == "weak")

    # ------------------------------------------------------------ spots (Mark-: targets space, not bodies)
    def occupant(self, side, cell):
        team = self.party if side == "party" else self.enemies
        return next((x for x in team if x.alive and x.cell == cell), None)

    def spot_damage(self, src, t, a, mult):
        """Element damage on a painted spot: affinity is ignored (for now), and Cover can't take it."""
        dmg = self.raw_damage(src, t, a) * mult
        var = ELEMENT[a["element"]]["var"]
        return dmg * (1 + self.rng.uniform(-var, var))

    def paint(self, u, a, chosen, bonus):
        """Paint the chosen foe's spot: hit whoever stands there now, then the spot ticks at each round's start."""
        foes = self.foes(u)
        if not foes: return
        t = chosen if chosen in foes else self.rng.choice(foes)
        side, cell = t.side if t.side == "party" else "enemy", t.cell
        u.pay(a); u.stats["actions"] += 1; u.stats["paints"] += 1
        self.spots[(side, cell)] = dict(src=u, a=a, rounds=SPOT_ROUNDS)
        self.emit("paint", f"    {u.name} uses {self.shown(u, a)}, coating {t.name}'s spot.{' [Bonus]' if bonus else ''}", unit=u.name, move=a["name"], shown=self.shown(u, a), element=a["element"], side=side, cell=cell, target=t.name)
        res = self.roll(u, t, a)
        dmg = self.spot_damage(u, t, a, SPOT_IMPACT) * {"graze": GRAZE_MULT, "hit": 1.0, "crit": CRIT_MULT}[res]
        if t.defending: dmg *= 0.5
        t.hp -= dmg; u.stats["dealt"] += dmg
        self.emit("hit", f"      {res.capitalize()} on {t.name}: {dmg:.0f}. ({max(0, t.hp):.0f}/{t.maxhp:.0f})", src=u.name, unit=t.name, element=a["element"], results=[res], affinity="normal", spot=True, dmg=round(dmg), hp=max(0, round(t.hp)), maxhp=round(t.maxhp))
        if not t.alive: self.downed(t, a["element"])

    def tick_spots(self):
        for key in list(self.spots):
            sp = self.spots[key]; t = self.occupant(*key)
            if t is not None:
                dmg = self.spot_damage(sp["src"], t, sp["a"], SPOT_TICK)
                t.hp -= dmg; sp["src"].stats["dealt"] += dmg; t.stats["spot_ticks"] += 1
                self.emit("tick", f"    {t.name} stands in {sp['a']['element']} slime: {dmg:.0f}. ({max(0, t.hp):.0f}/{t.maxhp:.0f})", unit=t.name, status="slime", element=sp["a"]["element"], dmg=round(dmg), hp=max(0, round(t.hp)))
                if not t.alive: self.downed(t)
            sp["rounds"] -= 1
            if sp["rounds"] <= 0: del self.spots[key]

    def painted(self, u, cell=None):
        if not USE_BOARD or not hasattr(u, "cell"): return None
        sp = self.spots.get(("party" if u.side == "party" else "enemy", cell or u.cell))
        return sp if sp and sp["rounds"] > 0 else None

    def shown(self, u, a):
        """Heroes see the old-language word; an enemy shouts the plain English name (spellbook Part 10)."""
        if u.side != "party" and a.get("english"): return f'"{a["english"]}!"'
        return a["name"]

    # ------------------------------------------------------------ AI
    def declare(self, u):
        ref = 20 * level_factor(u.level)
        options = []
        for a in u.actions + self.item_actions(u):
            if not u.can_afford(a): continue
            if a.get("once") and (a["name"] in u.once_used or (u.uid, a["name"]) in getattr(self, "once_claims", ())): continue
            if u.silenced and a["cost_type"] == "MP" and a["cost"] > 0: continue
            cost_pen = 0.25 * a["cost"] if a["cost_type"] == "MP" else 0.15 * a["cost"]
            thrift = AI_ITEM_THRIFT if a.get("item") else 1.0
            if a["kind"] == "revive":
                for t in self.party if u.side == "party" else []:
                    if t.state == "dying" or (t.state == "dead" and a["reaches"] == "Dead"):
                        options.append((2.0 * ref * thrift - cost_pen, a, t))
                continue
            if a["kind"] == "flee": continue                  # the sim never runs
            if a["kind"] in ("heal", "mp") and a.get("item"):
                pool = [x for x in self.allies(u) if (x.hp < 0.4 * x.maxhp if a["kind"] == "heal" else x.mp < 0.25 * x.maxmp)]
                for x in pool:
                    got = a["amount"] * (x.maxhp if a["kind"] == "heal" else x.maxmp)
                    options.append((1.2 * got * thrift if a["kind"] == "heal" else 0.6 * ref * thrift, a, x))
                continue
            if a["kind"] == "damage" and not a["all"] and not a.get("shape") and USE_DYING:
                for p in (self.party if u.side != "party" else []):
                    if self.fallen_reach(u, a, p) is not None:
                        # worth most when it kills: a breath taken from five is a fifth of a death
                        options.append((AI_FINISH_VALUE * ref / max(1, p.breaths) - cost_pen, a, p))
            if a["kind"] == "damage" and a.get("spot") and USE_BOARD:
                for f in self.foes(u):
                    if self.painted(f) or f in getattr(self, "paint_claims", ()): continue   # coated, or about to be
                    hit = self.raw_damage(u, f, a) * self.expected_roll_mult(u, f)
                    s = hit * SPOT_IMPACT + hit * SPOT_TICK * AI_SPOT_TICKS
                    options.append((s - cost_pen, a, f))
                continue
            if a["kind"] == "damage":
                for p in self.piles:
                    if self.pile_reach(u, a, p) is not None:
                        options.append((PILE_VALUE * p.maxhp * BEIN_REASSEMBLE_HP - cost_pen, a, p))
                foes = self.foes(u)
                foes = [f for f in foes if self.reach_mult(u, a, f) is not None]
                if not foes: continue
                if a["all"]:
                    s = sum(self.expected_damage(u, f, a) * self.reach_mult(u, a, f) for f in foes)
                    options.append((s - cost_pen, a, None))
                else:
                    for f in foes:
                        if a.get("shape") in ("row", "column") and USE_BOARD:
                            hit = self.shape_targets(u, a, f)
                            s = sum(self.expected_damage(u, x, a) * self.reach_mult(u, a, x)
                                    * (self.shape_mult(a, i) if len(hit) > 1 else 1.0) for i, x in enumerate(hit))
                        else:
                            s = self.expected_damage(u, f, a) * self.reach_mult(u, a, f)
                        if f.affinity(a["element"]) == "weak": s *= 1.5     # tempo value
                        if s >= f.hp: s *= 1.3
                        if a["status"] and not self.capped(f, a["status"]): s += 0.4 * ref
                        s *= AI_MANNER_VALUE.get((a.get("parts") or {}).get("manner"), 1.0)
                        options.append((s - cost_pen, a, f))
            elif a["kind"] == "heal":
                hurt = [x for x in self.allies(u) if x.hp < 0.5 * x.maxhp]
                if a["all"]:
                    s = sum(min(self.heal_amount(u, a), x.maxhp - x.hp) for x in self.allies(u) if x.hp < 0.7 * x.maxhp)
                    options.append((1.2 * s - cost_pen, a, None))
                for x in hurt:
                    s = min(self.heal_amount(u, a), x.maxhp - x.hp)
                    options.append((1.2 * s - cost_pen, a, x))
            elif a["kind"] == "status":
                for f in self.foes(u):
                    if self.capped(f, a["status"]): continue
                    if a["status"] == "Bound":
                        if f.has_flag("no_orders") or f in getattr(self, "bind_claims", ()) or f.state != "up": continue
                        options.append((self.bind_value(u, f, ref) - cost_pen, a, f)); continue
                    s = 0.9 * ref * STATUS_LINE_CHANCE[a["tier"]]
                    options.append((s - cost_pen, a, f))
            elif a["kind"] == "stat":
                pool = self.allies(u) if a["direction"] > 0 else self.foes(u)
                for x in pool:
                    if x.stage(a["stat"]) * a["direction"] >= STACK_CAP: continue   # already as far as it goes
                    options.append((0.8 * ref - cost_pen, a, x))
            elif a["kind"] == "cleanse":
                def burden(x): return len(x.status) + sum(-v for v in x.stages.values() if v < 0)
                pool = [x for x in self.allies(u) if burden(x) > 0]
                if a["all"] and pool:
                    options.append((0.5 * ref * sum(burden(x) for x in pool) - cost_pen, a, None))
                for x in pool:
                    options.append((0.5 * ref * burden(x) - cost_pen, a, x))
            elif a["kind"] == "defend":
                s = (0.8 if u.hp < 0.25 * u.maxhp else 0.1) * ref
                options.append((s, a, u))
        if USE_BOARD and USE_ROTATION:
            options += self.board_options(u, ref)
        options = [(sc * (AI_ITEM_THRIFT if a.get("item") and a["kind"] in ("damage", "stat") else 1.0), a, t)
                   for sc, a, t in options]
        if not options:
            return u.actions[0], None
        options.sort(key=lambda o: -o[0])
        pick = options[0] if self.rng.random() < 0.8 else self.rng.choice(options[:3])
        return pick[1], pick[2]

    def reason(self, u, a, t):
        """Why the AI chose this: (code, plain English). Read after the choice, so the scoring stays one place.
        The front-end shows it on hover; the codes are stable for icons and tests."""
        n = lambda x: x.name if x is not None else "them"
        k = a["kind"]
        if a.get("_release"): return "release", "the wind-up comes down"
        if k == "revive": return "revive", f"{n(t)} is {'dying' if t is not None and t.state == 'dying' else 'dead'}"
        if k == "flee": return "flee", "the fight is lost"
        if k == "mp": return "mend", f"{n(t)} is out of MP"
        if t is not None and getattr(t, "state", "up") == "dying" and k == "damage":
            return "finish_fallen", f"{t.name} is dying"
        if k == "move":
            if a["name"] == "Advance": return "advance", "its line is empty"
            if a["name"] == "Step off": return "step_off", "it is standing in slime"
            if a["name"] == "Step up": return "fill", "there is room in the Front"
            if a["name"] == "Fall back": return "fall_back", "it keeps behind the line"
            r = a.get("rescue")
            if r is not None and self.bide_threat(r) > 0: return "dodge", f"a wind-up is aimed at {r.name}"
            return "rotate", f"{n(r)} is badly hurt"
        if k == "cover":
            r = a.get("rescue") or t
            if r is not None and self.bide_threat(r) > 0: return "shield", f"{r.name} is about to be struck"
            return "shield", f"{n(r)} is badly hurt"
        if k == "defend":
            if self.bide_threat(u) > 0: return "brace", "a wind-up is aimed at it"
            return "brace", "it is badly hurt" if u.hp < 0.25 * u.maxhp else "it waits"
        if k == "heal": return "mend", f"{n(t)} is hurt" if t is not None else "its side is hurt"
        if k == "status": return "hex", f"to leave {n(t)} {a['status']}"
        if k == "stat": return ("bolster" if a["direction"] > 0 else "weaken"), f"{a['stat']} on {n(t)}"
        if k == "cleanse": return "cleanse", f"{n(t)} is afflicted" if t is not None else "its side is afflicted"
        if k == "damage":
            if t in self.piles: return "scatter", f"{t.name}'s bones will stand again"
            if a.get("spot"): return "coat", f"{n(t)} is standing still"
            if a.get("bide"): return "bide", "it gathers for a heavy blow"
            if t is not None:
                if t.affinity(a["element"]) == "weak": return "weak", f"{t.name} is weak to {a['element']}"
                if self.expected_damage(u, t, a) >= t.hp: return "finish", f"{t.name} is nearly down"
                if a["status"] and not self.capped(t, a["status"]): return "rider", f"to leave {t.name} {a['status']}"
                if USE_BOARD and getattr(t, "cell", ("front",))[0] == "rear": return "reach", f"{t.name} stands behind the line"
            return ("sweep" if a["all"] or a.get("shape") else "strike"), "its strongest blow"
        return "act", ""

    def intent(self, u, a, t, ordered=False):
        if self.events is None: return
        code, why = ("order", "") if ordered else self.reason(u, a, t)   # a player's order carries no AI reasoning
                                                                           # (which reads true affinities)
        self.intents[u.uid] = dict(move=a["name"], shown=self.shown(u, a), plain=plain(a), move_kind=a["kind"],
                                   element=a.get("element"), item=a.get("item") or None, all=a["all"], shape=a.get("shape"),
                                   reach=a.get("reach") or (REACH_BY_TYPE.get(a.get("element")) if a.get("element") in MARTIAL else "any"),
                                   bide=bool(a.get("bide")), jarf=(a.get("parts") or {}).get("manner") == "Jarf",
                                   direction=a.get("direction"), status=a.get("status"), target=t.name if t is not None and t is not u else None,
                                   target_id=t.uid if t is not None and t is not u and hasattr(t, "uid") else None,
                                   reason=code, why=why)
        self.emit("intent", unit=u.name, side=u.side, move=a["name"], shown=self.shown(u, a), move_kind=a["kind"],
                  element=a["element"], target=t.name if t is not None and t is not u else None,
                  group=self.group_of(u, a), reason=code, why=why)

    def bide_threat(self, x):
        """Expected damage of a hero or enemy wind-up aimed at x, visible on the board since last round."""
        return sum(self.expected_damage(f, x, f.bide[0]) for f in self.foes(x)
                   if f.bide is not None and f.bide[1] is x and not f.bide[0].get("spot"))

    def board_options(self, u, ref):
        """Rotation, Cover, and answers to a visible wind-up: scored like any other option (combat_spec Parts 7-8).
        Swap: a hurt Front unit trades places with a healthy melee unit behind it (either one may make the move).
        Step up: a Rear melee unit takes an empty Front spot. Casters stay back. Cover: a healthy front-liner
        takes the hits for a badly hurt ally, or for the target of a wind-up."""
        out = []
        team = [x for x in self.team_of(u) if x.alive]
        frac = lambda x: x.hp / x.maxhp
        melee = self.wants_front(u)
        mine = self.bide_threat(u)
        def swap(x, hurt): return act("move", "Swap", target="self", cell=x.cell, rescue=hurt)
        claimed = getattr(self, "claimed", set())           # allies someone already declared to rescue this phase
        if mine > 0:                                            # brace for the wind-up aimed at me
            out.append((ROT_DEFEND_BIDE * mine, act("defend", "Defend", target="self"), u))
        for x in team:
            if x is u: continue
            # Swap: the hurt one is in the Front, the healthy melee one behind it
            front, back = (u, x) if u.cell[0] == "front" else (x, u)
            if front.cell[0] == "front" and back.cell[0] == "rear" and self.wants_front(back) \
                    and frac(front) < ROT_HURT and frac(back) > ROT_HEALTHY and front not in claimed:
                gain = (frac(back) - frac(front)) * ref * ROT_SWAP_VALUE
                if self.painted(front): gain *= 0.3              # the fresh unit would stand in the slime
                gain += ROT_DODGE_BIDE * self.bide_threat(front)
                if u is back: gain *= 1.2                        # the Rear melee unit's own swing was only half anyway
                out.append((gain, swap(x, front), u))
            # Cover: a healthy front-liner shields a badly hurt ally, or the target of a wind-up
            if melee and frac(u) > ROT_HEALTHY and x not in claimed and x.cell[0] == "front" or \
                    (melee and frac(u) > ROT_HEALTHY and x not in claimed and self.bide_threat(x) > 0):
                threat = self.bide_threat(x)
                guard = getattr(u, "guard", False)
                hurt = GUARDIAN_COVER_HURT if guard else ROT_COVER_HURT
                s = (ROT_COVER_VALUE * ref if frac(x) < hurt else 0.0) + ROT_COVER_BIDE * threat
                if guard: s *= GUARDIAN_COVER
                if s > 0: out.append((s, act("cover", "Cover", target="ally", rescue=x), x))
        taken = {x.cell for x in team}
        sp = self.painted(u)
        if sp:                                                   # step off a painted spot, within the row
            clean = [(u.cell[0], l) for l in range(3) if (u.cell[0], l) not in taken and not self.painted(u, (u.cell[0], l))]
            if clean:
                tick = self.raw_damage(sp["src"], u, sp["a"]) * SPOT_TICK
                out.append((ROT_SPOT_VALUE * tick * min(sp["rounds"], 2), act("move", "Step off", target="self", cell=clean[0]), u))
        if melee and u.cell[0] == "rear":                        # step up into an empty Front spot
            free = [("front", l) for l in range(3) if ("front", l) not in taken and not self.painted(u, ("front", l))]
            if free and frac(u) > ROT_HURT:
                out.append((ROT_STEP_VALUE * ref, act("move", "Step up", target="self", cell=free[0]), u))
        if not melee and u.cell[0] == "front" and self.front_ok_without(u):   # casters fall back
            free = [("rear", l) for l in range(3) if ("rear", l) not in taken and not self.painted(u, ("rear", l))]
            if free: out.append((ROT_FALLBACK_VALUE * ref, act("move", "Fall back", target="self", cell=free[0]), u))
        return out

    # ------------------------------------------------------------ rounds
    def group_of(self, u, a):
        """The speed group an action resolves in (combat_spec Part 3)."""
        g = a.get("group", SPEED_GROUP_BY_KIND.get(a["kind"], 0))
        if g < PROTECT_GROUP:                       # Fear drops anything below protection
            for s in u.status:
                fg = STATUSES.get(s, {}).get("group")
                if fg is not None: g = min(g, fg)
        return g

    def order(self, entries):
        """Resolution order: group (high first), then first actions before second, then SPD, then each unit's coin,
        flipped once when the phase is planned, so the turn-order bar can show the order that will happen."""
        if USE_SPEED_GROUPS:
            key = lambda e: (-self.group_of(e[1], e[2][0]), e[0], -e[1].speed(), self.coin.get(e[1].uid, 0.5))
        else:   # the old rule, kept for A/B: first actions first, Feared last, then SPD
            key = lambda e: (e[0], "Feared" in e[1].status, -e[1].speed(), self.coin.get(e[1].uid, 0.5))
        return sorted(entries, key=key)

    def advancers(self, actors):
        """A side whose Front is empty sends its healthiest melee unit forward (casters stay put: spells reach)."""
        out = set()
        for team in (self.party, self.enemies):
            alive = [x for x in team if x.alive]
            if not alive or any(x.cell[0] == "front" for x in alive): continue
            melee = [x for x in alive if x in actors and self.wants_front(x)]
            if melee: out.add(max(melee, key=lambda x: x.hp))
        return out

    # ------------------------------------------------------------ a phase: plan, then resolve
    def plan_phase(self, actors, bonus):
        """Declare a phase. Units we control leave an empty slot (filled by submit); everyone else declares now.
        Units act once per cost point; everyone's first actions resolve before anyone's second."""
        remaining = []
        advancers = self.advancers(actors) if USE_BOARD else set()
        locked = set()
        if not bonus:          # last round's wind-ups fire this round, in place of the unit's first action
            for u in self.units:
                if u.bide is None: continue
                ba, bt = u.bide; u.bide = None
                if not u.alive: u.stats["bides_lost"] += 1; continue
                rel = dict(ba, _release=True, cost=0, group=0)
                remaining.append((0, u, (rel, bt))); locked.add(u); self.intent(u, rel, bt)
        self.claimed, self.paint_claims, self.bind_claims, self.once_claims = set(), set(), set(), set()
        self.waiting = []
        for u in actors:
            if not u.alive or (bonus and u.bide is not None): continue      # a unit winding up sits out bonus rounds
            for k in range(1 if bonus else u.actions_per_round):
                if k == 0 and u in locked: continue
                if k == 0 and u in advancers:
                    adv = act("move", "Advance", target="self", to="front")
                    remaining.append((k, u, (adv, u))); self.intent(u, adv, u)
                elif k == 0 and self.controls(u):
                    remaining.append((k, u, None)); self.waiting.append(u)     # the player's order goes here
                else:
                    d = self.declare(u); remaining.append((k, u, d)); self.intent(u, *d)
                    if d[0].get("rescue") is not None: self.claimed.add(d[0]["rescue"])
                    if d[0].get("spot") and d[1] is not None: self.paint_claims.add(d[1])
                    if d[0].get("status") == "Bound" and d[1] is not None: self.bind_claims.add(d[1])   # marked: no double-tap
                    if d[0].get("once"): self.once_claims.add((u.uid, d[0]["name"]))
        self.remaining, self.phase_bonus, self.orders = remaining, bonus, {}
        self.coin = {u.uid: self.rng.random() for u in self.units}      # SPD ties: one flip per unit per phase

    def controls(self, u):
        """Does the player order this unit now? Heroes who can act; the Frozen are skipped (they couldn't)."""
        return self.control == u.side and u.alive and not u.has_flag("no_orders")

    def resolve_phase(self):
        bonus = self.phase_bonus
        remaining = []
        for k, u, d in self.remaining:
            if d is None:
                d = self.orders[u.uid]; self.intent(u, *d, ordered=True)
            remaining.append((k, u, d))
        self.waiting, self.orders = [], {}
        self.pending_defend = {u for k, u, (a, t) in remaining if a["kind"] == "defend"}
        if self.lines is not None:
            self.say("  Order: " + " | ".join(f"[{self.group_of(u, a):+d}] {u.name} {a['name']}"
                                              for k, u, (a, t) in self.order(remaining)))
        if self.events is not None:
            self.emit("order", entries=[dict(unit=u.name, move=a["name"], group=self.group_of(u, a))
                                        for k, u, (a, t) in self.order(remaining)], bonus=bonus)
        while remaining and not self.over():
            remaining = self.order(remaining)            # re-ranked every step: SPD or Fear can change
            k, u, (a, tgt) = remaining.pop(0)
            if k >= u.actions_per_round: continue      # re-formed smaller since declaring
            if a not in u.actions and a["kind"] not in ("defend", "move", "cover", "flee") and not a.get("_release") \
                    and not a.get("item"):
                a, tgt = self.declare(u)
            self.resolve(u, a, tgt, bonus)
            if a.get("then") and a["name"] in getattr(u, "once_used", ()) and u.alive and getattr(u, "job", None) != a["then"]:
                self.transform(u, a["then"])
            if a["kind"] == "defend": self.pending_defend.discard(u)   # landed, or lost to Stun/Frozen
        self.remaining = []

    def run_phase(self, actors, bonus):
        self.plan_phase(actors, bonus); self.resolve_phase()

    def roster(self):
        return [dict(unit=u.name, id=u.uid, side=u.side, family=getattr(u, "family", None), cls=getattr(u, "cls", None),
                     rank=getattr(u, "mogel_rank", None) or getattr(u, "rank_name", None) or getattr(u, "rank", None),
                     job=getattr(u, "job", None), type=type_of(u), element=getattr(u, "element", None),
                     cell=getattr(u, "cell", None), hp=round(u.hp), maxhp=round(u.maxhp),
                     mp=round(getattr(u, "mp", 0)), maxmp=round(getattr(u, "maxmp", 0)),
                     pouch=[dict(item=k, name=ITEMS[k]["name"], count=n) for k, n in u.pouch],
                     moves=[dict(name=a["name"], shown=a.get("english") if u.side != "party" and a.get("english") else a["name"],
                                 kind=a["kind"], element=a["element"], cost=a["cost"], cost_type=a["cost_type"])
                            for a in u.actions]) for u in self.units]

    # ------------------------------------------------------------ the fight, one decision at a time
    # begin() -> loop { phase, awaiting(), options(uid), submit(uid, key, target), commit() } (fight_lab_spec Part 1).
    # commit() stops at the start of every round, and at a Bonus Round our heroes earned; with nothing awaited, the
    # page just commits again. fight() is the same loop with the AI ordering everyone.
    def begin(self, control=None, max_rounds=30):
        self.control, self.max_rounds, self.phase, self.winner = control, max_rounds, "start", None
        self._mark = 0
        if self.events is not None: self.emit("start", units=self.roster())
        if USE_BOARD and self.lines is not None:
            for team in (self.party, self.enemies):
                self.say("  " + "  ".join(f"{u.name} {u.cell[0][0].upper()}{u.cell[1] + 1}" for u in sorted(team, key=lambda x: x.cell)))
        self.next_round()
        return self.drain()

    def drain(self):
        if self.events is None: return []
        out = self.events[self._mark:]; self._mark = len(self.events); return out

    def awaiting(self):
        return [u.uid for u in self.waiting] if self.phase in ("declare", "bonus") else []

    def next_round(self):
        if self.over() or self.round >= self.max_rounds:
            self.finish(); return
        self.round += 1; self.intents = {}
        self.emit("round", f"Round {self.round}", n=self.round)
        for u in self.units:
            if u.alive: self.tick_statuses(u, "round_start")
        self.tick_spots(); self.tick_piles()
        self.eligible, self.barred = set(), set()
        for u in self.units: u.defending, u.covered_by = False, None
        self.plan_phase([u for u in self.units if u.alive], bonus=False)
        self.phase = "declare"

    def commit(self):
        """Resolve what was planned, and run on to the next round's orders (or a Bonus Round our heroes earned)."""
        if self.phase == "over": return self.drain()
        missing = [u.uid for u in self.waiting if u.uid not in self.orders]
        if missing: raise ValueError(f"no order for {missing}")
        bonus = self.phase == "bonus"
        self.resolve_phase()
        if not bonus:
            entrants = [u for u in self.units if u in self.eligible and u.alive and u not in self.barred]
            if entrants and not self.over():
                self.bonus_rounds += 1
                for u in entrants: u.stats["bonus"] += 1
                self.emit("bonus", f"  Bonus Round! ({', '.join(u.name for u in entrants)})", units=[u.name for u in entrants])
                self.plan_phase(entrants, bonus=True)
                if self.waiting:
                    self.phase = "bonus"; return self.drain()
                self.resolve_phase()
        self.end_round()
        self.next_round()
        return self.drain()

    def end_round(self):
        if USE_DYING: self.tick_breaths()
        for u in self.units:      # counters nobody pushed this round step toward zero
            for st, v in u.stages.items():
                if v and st not in u.pushed: u.stages[st] = v - 1 if v > 0 else v + 1
            u.pushed = set()
        for u in self.units:      # only numbered rounds tick durations
            for s in list(u.status):
                u.status[s]["rounds"] -= 1
                if u.status[s]["rounds"] <= 0: del u.status[s]

    def finish(self):
        winner = "fled" if self.fled else \
            "party" if any(x.alive for x in self.party) and not any(x.alive for x in self.enemies) \
            else "enemy" if not any(x.alive for x in self.party) else "draw"
        if winner in ("party", "fled") and USE_DYING:     # the Dying are stabilised: up at 1 HP, Wounded
            for t in self.dying():
                self.stand_up(t, 0.0, True)
                self.emit("stabilised", f"  {t.name} is stabilised at 1 HP, Wounded.", unit=t.name, hp=round(t.hp))
        self.emit("end", f"Result: {winner} after {self.round} rounds", winner=winner, rounds=self.round)
        self.phase, self.winner, self.waiting = "over", winner, []

    # ------------------------------------------------------------ the player's side: what can this hero do?
    def unit(self, uid): return self.by_uid[uid]

    def flee_chance(self, u):
        if self.no_flee: return 0.0
        mine = [x.speed() for x in self.allies(u)]; theirs = [x.speed() for x in self.foes(u)]
        if not mine or not theirs: return FLEE_MAX
        r = (sum(mine) / len(mine)) / (sum(theirs) / len(theirs))
        return clamp(FLEE_BASE + FLEE_PER_QUARTER * (r - 1) / 0.25, FLEE_MIN, FLEE_MAX)

    def slots(self, u):
        """The hero's Halv move and their four slotted moves (fight_lab_spec Part 2). Defend is Guard, not a slot;
        a martial hero with a free slot gets Cover, which the AI uses through the board rules."""
        halv = next((a for a in u.actions if a.get("tier") == "Halv" and a["cost"] == 0 and a["kind"] == "damage"), None)
        moves = [a for a in u.actions if a is not halv and a["kind"] != "defend"]
        if CLASSES.get(u.cls, {}).get("kind") == "martial" and len(moves) < 4 and USE_BOARD:
            moves.append(act("cover", "Cover", target="ally"))
        return halv, moves[:4]

    def aim(self, a):
        if a["target"] == "self" or a["kind"] in ("defend", "flee"): return "self"
        if a["all"]: return "all"
        return a.get("shape") or "one"

    def legal(self, u, a):
        """Who u could aim a at, as things stand. Reach is checked again when the move lands."""
        if a["target"] == "self": return [u]
        if a["target"] == "fallen":
            return [x for x in self.team_of(u) if x.state == "dying" or (x.state == "dead" and a.get("reaches") == "Dead")]
        if a["target"] == "ally":
            pool = [x for x in self.allies(u) if not (a["kind"] == "cover" and x is u)]
            return pool
        pool = [x for x in self.foes(u) if self.reach_mult(u, a, x) is not None]
        if a["kind"] == "damage" and not a["all"]:
            pool += [p for p in self.piles if self.pile_reach(u, a, p) is not None]
        return pool

    def describe(self, u, a, key, slot):
        silenced = u.silenced and a["cost_type"] == "MP" and a["cost"] > 0
        afford = u.can_afford(a) and not silenced
        tg = self.legal(u, a)
        parts = a.get("parts") or {}
        return dict(key=key, slot=slot, name=a["name"], shown=self.shown(u, a), kind=a["kind"], element=a.get("element"),
                    cost=a["cost"], cost_type=a["cost_type"], afford=afford, why=None if afford else ("Silenced" if silenced else "cost"),
                    group=self.group_of(u, a), aim=self.aim(a), targets=[x.uid for x in tg],
                    card=dict(word=a["name"], plain=plain(a), english=a.get("english"), power=round(a.get("power") or 0, 1), tier=a.get("tier"),
                              reach=a.get("reach") or (REACH_BY_TYPE.get(a["element"]) if a.get("element") in MARTIAL else "any"),
                              status=a.get("status"), shape=a.get("shape"), all=a["all"], bide=bool(a.get("bide")),
                              spot=bool(a.get("spot")), manner=parts.get("manner"), target_kind=parts.get("target"),
                              rider=parts.get("rider"), flurry=bool(a.get("flurry"))))

    def options(self, uid):
        """Everything this hero can be ordered to do now, with legal targets by id (or cells, for Move)."""
        u = self.unit(uid)
        halv, moves = self.slots(u)
        out = dict(unit=uid, halv=None, moves=[], items=[], guard=None, move=None, flee=None)
        if halv is not None: out["halv"] = self.describe(u, halv, f"m{u.actions.index(halv)}", "halv")
        for a in moves:
            key = f"m{u.actions.index(a)}" if a in u.actions else a["kind"]
            out["moves"].append(self.describe(u, a, key, "move"))
        for k, n in u.pouch:
            if n <= 0: continue
            d = self.describe(u, item_move(k), f"i:{k}", "item"); d["count"] = n; out["items"].append(d)
        out["guard"] = dict(key="guard", slot="guard", name="Guard", group=self.group_of(u, act("defend", "Defend")), aim="self")
        cells = []
        if USE_BOARD:
            for r in ("front", "rear"):
                for l in range(3):
                    c = (r, l)
                    if c == u.cell: continue
                    who = next((x for x in self.team_of(u) if x is not u and getattr(x, "cell", None) == c and x.state != "dead"
                                and (x.alive or x.state == "dying")), None)
                    if who is not None and not who.alive: continue           # a fallen hero lies there
                    if who is None and r != u.cell[0] and not self.front_ok_without(u): continue   # never empty the Front
                    cells.append(dict(cell=[r, l], swap=who.uid if who else None, swap_name=who.name if who else None))
        out["move"] = dict(key="move", slot="move", name="Move", group=self.group_of(u, act("move", "Move")), aim="cell", cells=cells)
        out["flee"] = dict(key="flee", slot="flee", name="Flee", group=self.group_of(u, act("flee", "Flee")), aim="self",
                           chance=round(self.flee_chance(u), 2), allowed=not self.no_flee)
        return out

    def order_for(self, u, key, target):
        """Turn a menu key and a target (an id, a [row, lane] cell, or None) into the engine's (action, target)."""
        if key == "guard": return act("defend", "Guard", target="self"), u
        if key == "flee":
            if self.no_flee: raise ValueError("this fight can't be run from")
            return act("flee", "Flee", target="self"), u
        if key == "move":
            cell = tuple(target)
            if not any(tuple(c["cell"]) == cell for c in self.options(u.uid)["move"]["cells"]): raise ValueError(f"can't move to {cell}")
            return act("move", "Move", target="self", cell=cell), u
        if key.startswith("i:"):
            k = key[2:]
            if not any(s[0] == k and s[1] > 0 for s in u.pouch): raise ValueError(f"no {k} in the pouch")
            a = item_move(k)
        elif key == "cover":
            a = next(m for m in self.slots(u)[1] if m["kind"] == "cover")
        else:
            a = u.actions[int(key[1:])]
            halv, moves = self.slots(u)
            if a is not halv and a not in moves: raise ValueError(f"{a['name']} isn't slotted")
        if not u.can_afford(a): raise ValueError(f"can't afford {a['name']}")
        if self.aim(a) == "self": return a, u
        if self.aim(a) == "all": return a, None
        t = self.unit(target) if target is not None else None
        if t is None or t not in self.legal(u, a): raise ValueError(f"{a['name']} can't reach {target}")
        if a["kind"] == "cover": a = dict(a, rescue=t)
        return a, t

    def submit(self, uid, key, target=None):
        u = self.unit(uid)
        if u not in self.waiting: raise ValueError(f"{uid} isn't waiting for an order")
        self.orders[uid] = self.order_for(u, key, target)

    def retract(self, uid): self.orders.pop(uid, None)

    def preview_order(self):
        """The turn-order bar: the planned phase in resolution order, our orders so far included. It never rolls the
        fight's dice. Exact unless SPD or Fear changes mid-round (the order is re-ranked as the round goes)."""
        rows = []
        for k, u, d in self.remaining:
            if d is None: d = self.orders.get(u.uid)
            a = d[0] if d else None
            g = self.group_of(u, a) if a else 0
            rows.append(dict(id=u.uid, name=u.name, side=u.side, move=self.shown(u, a) if a else None, group=g, k=k,
                             speed=round(u.speed(), 2), ordered=a is not None))
        for r in rows: r["coin"] = self.coin.get(r["id"], 0.5)
        rows.sort(key=lambda r: (-r["group"], r["k"], -r["speed"], r["coin"]))
        for i, r in enumerate(rows):       # tied on speed: the coin already decided, but say so on hover
            r["tie"] = any(o is not r and (o["group"], o["k"], o["speed"]) == (r["group"], r["k"], r["speed"]) for o in rows)
            del r["coin"]
        return rows

    def inspect(self, uid):
        """A unit's whole sheet, as the engine knows it. The page masks it by what the Company remembers (knowledge.py)."""
        u = self.unit(uid)
        dtypes = [e for e in ELEMENT if e != "Force"]
        return dict(id=uid, name=u.name, side=u.side, family=getattr(u, "family", None), cls=u.cls,
                    rank=getattr(u, "mogel_rank", None) or getattr(u, "rank_name", None) or getattr(u, "rank", None),
                    job=getattr(u, "job", None), type=type_of(u), element=getattr(u, "element", None), level=u.level,
                    hp=round(max(0, u.hp)), maxhp=round(u.maxhp), mp=round(getattr(u, "mp", 0)), maxmp=round(getattr(u, "maxmp", 0)),
                    state=u.state, breaths=u.breaths, wounded=u.wounded, cell=list(u.cell) if getattr(u, "cell", None) else None,
                    piled=u in self.piles, crawling=getattr(u, "crawling", False),
                    status={k: v["rounds"] for k, v in u.status.items()}, stages={k: v for k, v in u.stages.items() if v},
                    affinities={e: u.affinity(e) for e in dtypes}, moves=[self.shown(u, a) for a in u.actions],
                    move_lines=[dict(name=self.shown(u, a), plain=plain(a)) for a in u.actions],
                    intent=self.intents.get(uid), winding=self.shown(u, u.bide[0]) if u.bide else None,
                    defending=u.defending, covered_by=u.covered_by.uid if u.covered_by else None,
                    pouch=[dict(item=k, name=ITEMS[k]["name"], count=n) for k, n in u.pouch])

    def fight(self, max_rounds=30):
        self.begin(None, max_rounds)
        while self.phase != "over": self.commit()
        return self.winner


# ================================================================ the Ande spirits
def spirit_name(rank, element):
    p = dict(SPIRIT_RANKS)[rank]["prefix"]
    base = join_morphemes([p, element]) if p else element
    return base + ("nde" if base.endswith("a") else "ande")

def spirit_move(spec, element, tier):
    kind = spec[0]
    if kind == "dmg": return damage_spell(spec[1], tier)
    if kind == "heal": return heal_spell(spec[1] if len(spec) > 1 else tier)
    if kind == "status": return status_spell(spec[1], spec[2] if len(spec) > 2 else tier)
    if kind == "stat":
        t = spec[3] if len(spec) > 3 else ("Base" if tier in ("Halv", "Base") else "Mer")
        return stat_spell(spec[1], spec[2] > 0, t)

def spirit_kit(rank, element):
    r = dict(SPIRIT_RANKS)[rank]
    main = (lambda t, a=False: heal_spell(t, a)) if element == "Lak" else \
           (lambda t, a=False: damage_spell(element, t, a))
    kit = [main(r["main"])]
    if r["all"]: kit.append(main(r["all"], True))
    status_tier = "Base" if r["main"] in ("Halv", "Base") else r["main"]
    for u in r["utils"]:
        tier = r["main"] if u == "U1" else status_tier
        kit.append(spirit_move(SPIRIT_KITS[element][u], element, tier))
    return kit

def spawn_spirit(rank, element, level, name=None):
    r = dict(SPIRIT_RANKS)[rank]
    attrs = {k: attr_at(15.5, level) for k in ATTRS}
    for k in ("INT", "CON", "WIS"): attrs[k] += SPIRIT_TRAIN * (level - 1)
    attrs["INT"] *= ANDE_MAT_SCALE * (HALV_BODY if rank == "Halv" else 1.0)
    sa = SCHOOL_AFFINITY[SCHOOL_OF[element]]
    u = Unit(name or spirit_name(rank, element), "enemy", level, attrs, {"STR": 1.0}, {"INT": 1.0},
             build_aff(resist=sa["resist"], weak=sa["weak"]), spirit_kit(rank, element))
    u.maxhp *= r["hp"] * SPIRIT_HP_SCALE; u.hp = u.maxhp
    u.maxmp *= r["cost"] * ANDE_MP_MULT; u.mp = u.maxmp
    u.actions_per_round = r["cost"]
    u.rank, u.element = rank, element
    u.apply_body("Ande")
    return u

def spirit_encounter(level, rng, budget=6):
    """A themed pack: one or two elements, filled to the slot budget."""
    pack = rng.sample(list(SPIRIT_KITS), rng.choice((1, 2)))
    out, left = [], budget
    while left > 0:
        rank, r = rng.choice([x for x in SPIRIT_RANKS if x[1]["cost"] <= left])
        out.append(spawn_spirit(rank, rng.choice(pack), level))
        left -= r["cost"]
    seen = {}
    for u in out:
        seen[u.name] = seen.get(u.name, 0) + 1
    count = {}
    for u in out:
        if seen[u.name] > 1:
            count[u.name] = count.get(u.name, 0) + 1
            u.name = f"{u.name} {chr(64 + count[u.name])}"
    return out

# ================================================================ martial families
def split_shown(parts, total):
    """Per-hit numbers that add up to the total shown (Twin Slash reads 17+16 when it hits for 33)."""
    shown = [round(p) for p in parts[:-1]]
    return shown + [round(total) - sum(shown)]

def arm(a, weapon):
    """A strike carried by a weapon: its range (and the weapon, for the card)."""
    a["weapon"] = weapon; a["reach"] = RANGES[WEAPONS[weapon][1]]

def wield(u, weapon):
    """A rank's weapon arms its strikes of the weapon's damage type that don't name their own (a Drattr's trident,
    a Beinorv's bow). Strikes of other types stay Short: the queen's Trident is Medium, her bite would not be."""
    if not weapon: return
    for a in u.actions:
        if a["kind"] == "damage" and a.get("element") == WEAPONS[weapon][0] and not a.get("weapon"): arm(a, weapon)

def price_shares(u):
    """Moves priced as a share of max MP (Splash) get their cost once the body is known."""
    for a in u.actions:
        if a.get("mp_share"): a["cost"] = max(1, round(u.maxmp * a["mp_share"]))

def type_of(u):
    """Martial or Magical: a creature's rank says so; a hero's class kind does."""
    if getattr(u, "type", None): return u.type
    k = CLASSES.get(getattr(u, "cls", None) or "", {}).get("kind")
    return {"magical": "Magical", "martial": "Martial"}.get(k)

def family_move(m):
    """An enemy move from its data row. A row may end in an options dict (Nov 9):
       name   -- what the enemy shouts, for a spell or other non-strike ("Splash"); a strike's name is in the row
       shape  -- "row" or "column";  falloff -- per-target share down a shape ([1.0, 0.5]: Skewer)
       hits   -- split the move's power into this many hits (Twin Slash: N+M)
       manner -- "Drif": the flurry (Swift Strikes)
       cost, group -- override the MP cost or the speed group
       also   -- a second stat change on the same targets, (stat, direction) (Feeding Frenzy)
       once   -- usable once per fight;  then -- the job this unit becomes after using it (the net, then the spear)
       sure   -- a status move that never misses;  thrown -- a status move Cover catches (Net Throw)
       mp_share -- the MP cost is this share of the caster's max MP, set at spawn (Splash: 3-4 casts at any level)
       line   -- what the log says when it goes off, after the unit's name ("throws a net!")
       weapon -- the strike's own weapon, which sets its range (WEAPONS); else the rank's weapon, else Short"""
    opts = m[-1] if isinstance(m[-1], dict) else {}
    if opts: m = m[:-1]
    a = _family_move(m, opts)
    if opts.get("name") and m[0] != "strike": a["english"] = opts["name"]
    for k in ("shape", "falloff", "group", "once", "then", "sure", "thrown", "mp_share", "line"):
        if k in opts: a[k] = opts[k]
    if opts.get("hits", 1) > 1: a["hits"] = opts["hits"]; a["power"] /= opts["hits"]
    if opts.get("manner") == "Drif":
        from grammar import MANNERS
        a["flurry"] = dict(MANNERS["Drif"]["flurry"])
    if "cost" in opts: a["cost"] = opts["cost"]
    if "also" in opts: a["also"] = [tuple(opts["also"])]
    return a

def _family_move(m, opts):
    k = m[0]
    if k == "strike":
        all_ = len(m) > 4 and m[4]
        status = m[5] if len(m) > 5 else None
        a = skill(m[1], m[2], m[3], all_=all_, status=status,
                  power=TIER_POWER[m[3]] * (0.7 if status else 1.0))
        a["cost"] = 0                      # enemies never pay HP
        if opts.get("weapon"): arm(a, opts["weapon"])   # its own weapon (a Hunt archer's bow, a thrown javelin)
        return a
    if k == "spell": return damage_spell(m[1], m[2], len(m) > 3 and m[3])
    if k == "heal": return heal_spell(m[1], len(m) > 2 and m[2])
    if k == "cleanse": return cleanse_spell(m[1], len(m) > 2 and m[2])
    if k == "ur":
        a = damage_spell(m[1], "Ur"); a["cost"] = ENEMY_UR_COST; return a
    if k == "status":
        if m[1] not in STATUS_ROOT:                    # a status with no spell line (Bound): the row names the move
            return act("status", opts.get("name", m[1]), status=m[1], tier=m[2], cost=0)
        return status_spell(m[1], m[2], len(m) > 3 and m[3])
    if k == "stat": return stat_spell(m[1], m[2] > 0, m[3], all_=len(m) > 4 and m[4])

def spawn_family(family, rank_name, level, element=None, job=None):
    fam = FAMILIES[family]
    row = rank_row(family, job or rank_name)
    name, cost, hp, moves = row["name"], row["cost"], row["hp"], row["moves"]
    rank_name = name
    if any("@" in m for m in moves):                      # an element-adopting rank (the Beinseidr)
        element = element or BEINSEIDR_ELEMENTS[0]
        moves = [tuple(element if x == "@" else x for x in m) for m in moves]
        pre = next((p for p in ("Halv", "Stor") if name.startswith(p)), "")
        name = join_morphemes([x for x in (pre, element, name[len(pre):].lower()) if x]).capitalize()
    attrs = {k: attr_at(15.5, level) for k in ATTRS}
    for k in ("STR", "INT", "CON", "WIS"): attrs[k] += SPIRIT_TRAIN * (level - 1)
    body = HALV_BODY if name.startswith("Halv") else 1.0
    attrs["STR"] *= SPIRIT_DMG_SCALE * body; attrs["INT"] *= SPIRIT_DMG_SCALE * body
    u = Unit(name, "enemy", level, attrs, {"STR": 1.0}, {"INT": 1.0}, build_aff(**fam["aff"]),
             [family_move(m) for m in moves])
    u.maxhp *= hp * SPIRIT_HP_SCALE; u.hp = u.maxhp
    u.maxmp *= cost; u.mp = u.maxmp
    price_shares(u)
    u.actions_per_round = cost
    u.rank = "Drott" if cost == 3 else rank_name
    u.rank_name = rank_name
    u.job, u.type = row["job"], row["type"]
    u.guard = rank_name in BEIN_GUARDIANS or bool(row["opts"].get("guard"))
    wield(u, row["opts"].get("weapon"))
    if element: u.element = element
    u.family = family
    u.apply_body(family, u.type)
    return u

def family_encounter(level, rng, family, budget=6):
    fams = ["Draugr", "Bein"] if family == "Undead" else [family]
    out, left = [], budget
    while left > 0:
        f = rng.choice(fams)
        r = rng.choice([r for r in rank_rows(f) if r["cost"] <= left])
        out.append(spawn_family(f, r["name"], level, job=r["job"])); left -= r["cost"]
    count, seen = {}, {}
    for u in out: seen[u.name] = seen.get(u.name, 0) + 1
    for u in out:
        if seen[u.name] > 1:
            count[u.name] = count.get(u.name, 0) + 1
            u.name = f"{u.name} {chr(64 + count[u.name])}"
    return out


# ================================================================ the Oskorei formations
def spawn_custom(name, cost, hp, aff, moves, level, horn=False):
    attrs = {k: attr_at(15.5, level) for k in ATTRS}
    for k in ("STR", "INT", "CON", "WIS"): attrs[k] += SPIRIT_TRAIN * (level - 1)
    body = HALV_BODY if name.startswith("Halv") else 1.0
    attrs["STR"] *= SPIRIT_DMG_SCALE * body; attrs["INT"] *= SPIRIT_DMG_SCALE * body
    u = Unit(name, "enemy", level, attrs, {"STR": 1.0}, {"INT": 1.0}, aff, [family_move(m) for m in moves])
    u.maxhp *= hp * SPIRIT_HP_SCALE; u.hp = u.maxhp
    u.maxmp *= cost; u.mp = u.maxmp
    u.actions_per_round = cost
    u.horn = horn
    u.rank = "Drott" if cost == 3 else name
    u.apply_body("Oskorei")
    return u

def oskorei_encounter(level, rng, tier=None):
    tier = tier or rng.randint(1, 4)
    sa = SCHOOL_AFFINITY["Blast"]
    out, hounds = [], 0
    for spec in OSKOREI_TIERS[tier]:
        if spec == "hound":
            hounds += 1
            u = spawn_family("Djur", "Halvdjur", level); u.name = f"Jakthund {chr(64 + hounds)}"
        else:
            name, cost, hp, mweak, horn, moves = spec
            aff = build_aff(resist=sa["resist"], weak=sa["weak"] + [mweak])
            u = spawn_custom(name, cost, hp, aff, moves, level, horn)
        out.append(u)
    for u in out: u.oskorei_tier = tier
    return out


# ================================================================ the Mogel (slimes)
def mogel_name(rank, element):
    p = dict(MOGEL_RANKS)[rank]["prefix"]
    el = "" if element == "Jord" else element          # the plain olive Mogel is the Jord one
    return join_morphemes([x for x in (p, el, "mogel") if x]).capitalize()

def mogel_kit(rank, element):
    r = dict(MOGEL_RANKS)[rank]
    kit = [family_move(("strike", "Crush", "Engulf", r["crush"]))]
    if r["splatter"]: kit.append(family_move(("strike", "Crush", "Splatter", r["splatter"], True)))
    kit.append(heal_spell(r["spell"]) if element == "Lak" else damage_spell(element, r["spell"]))
    if rank in MOGEL_PAINT_RANKS and element != "Lak":       # slime paint: Mark + the Mogel's element
        from grammar import compile_word, EN_ROOT
        p = compile_word(element, r["spell"], target="Mark")
        p.update(reach="any", english=f"{EN_ROOT[element]} Slime")
        kit.append(p)
    if r["withdraw"]: kit.append(act("defend", "Withdraw", target="self"))
    if r["reabsorb"]:
        h = heal_spell("Mer"); h["name"] = "Reabsorb"; h["target"] = "self"; kit.append(h)
    return kit

def spawn_mogel(rank, element, level, name=None):
    r = dict(MOGEL_RANKS)[rank]
    attrs = {k: attr_at(15.5, level) for k in ATTRS}
    for k in ("STR", "INT", "CON", "WIS"): attrs[k] += SPIRIT_TRAIN * (level - 1)
    body = HALV_BODY if rank == "Halv" else 1.0
    attrs["STR"] *= SPIRIT_DMG_SCALE * body; attrs["INT"] *= SPIRIT_DMG_SCALE * body
    sa = SCHOOL_AFFINITY[SCHOOL_OF[element]]
    aff = build_aff(resist=MOGEL_AFF["resist"], weak=MOGEL_AFF["weak"] + list(sa["weak"]), absorb=[element])
    u = Unit(name or mogel_name(rank, element), "enemy", level, attrs, {"STR": 1.0}, {"INT": 1.0},
             aff, mogel_kit(rank, element))
    u.maxhp *= r["hp"] * SPIRIT_HP_SCALE; u.hp = u.maxhp
    u.maxmp *= r["cost"]; u.mp = u.maxmp
    u.actions_per_round = r["cost"]
    u.rank = "Drott" if rank == "Drott" else rank
    u.mogel_rank, u.element, u.family = rank, element, "Mogel"
    u.apply_body("Mogel")
    return u
