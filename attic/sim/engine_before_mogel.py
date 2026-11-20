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

# ================================================================ actions
def act(kind, name, **kw):
    d = dict(kind=kind, name=name, element=None, tier="Base", all=False, cost=0,
             cost_type="MP", power=0, status=None, stat=None, direction=None,
             target="enemy", pct_current=0.0)
    d.update(kw)
    return d

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
    if c["kind"] == "caster":
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
    kit = [strike(d), skill(d, "Power Strike", "Base")]
    if level >= 50: kit.append(skill(d, "Crushing Blow", "Jatte"))
    elif level >= 20: kit.append(skill(d, "Great Strike", "Mer"))
    sig = {"Hersir": skill(d, "Blot", "Base", status="Bleeding", power=14),
           "Nalarbani": skill(d, "Blot", "Base", status="Bleeding", power=14),
           "Ullar": skill(d, "Volley", "Base", all_=True),
           "Huskarl": stat_spell("DEF", True),
           "Vasara": stat_spell("DEF", True),
           "Berserker": skill(d, "Reckless Strike", "Base", power=32, pct_current=0.25)}[cls]
    kit.append(sig)
    if len(kit) < 4: kit.append(act("defend", "Defend", target="self"))
    return kit

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
        self.stages = {k: 0 for k in ["ATK", "DEF", "MAT", "MDF", "ACC", "EVA", "SPD"]}
        self.status = {}          # name -> dict(rounds=..., ...)
        self.defending = False
        self.stats = dict(dealt=0.0, healed=0.0, weak=0, crit=0, graze=0, hits=0, statuses=0,
                          bonus=0, actions=0, downs=0)

    alive = property(lambda s: s.hp > 0)
    def weighted(self, w): return sum(self.attrs[k] * v for k, v in w.items())
    def b(self, k): return self.body.get(k, 1.0)
    ATK = property(lambda s: s.weighted(s.atk_w) * s.b("ATK"))
    MAT = property(lambda s: s.weighted(s.mat_w) * s.b("MAT"))
    DEF = property(lambda s: s.attrs["CON"] * s.b("DEF"))
    MDF = property(lambda s: s.attrs["WIS"] * s.b("MDF"))
    WIL = property(lambda s: s.attrs["WIL"] * s.b("WIL"))

    def apply_body(self, family):
        self.body = dict(FAMILY_BODIES.get(family, {}))
        self.maxhp *= self.b("HP"); self.hp = self.maxhp

    def stage(self, stat):
        n = self.stages[stat]
        if "Chilled" in self.status and stat == "SPD": n -= 1
        if "Blinded" in self.status and stat in ("ACC", "EVA"): n -= 1
        if "Cursed" in self.status: n -= self.status["Cursed"]["stats"].count(stat)
        if "Disarmed" in self.status and stat in ("ATK", "MAT"): n -= 1
        return clamp(n, -5, 5)

    def speed(self): return self.attrs["SPD"] * self.b("SPD") * stage_mult(self.stage("SPD"))
    def affinity(self, element): return self.aff.get(element, "normal")

    def can_afford(self, a):
        if a["cost_type"] == "MP": return self.mp >= a["cost"]
        if a["pct_current"]: return self.hp > 1
        return self.hp > a["cost"]

    def pay(self, a):
        if a["cost_type"] == "MP": self.mp -= a["cost"]
        elif a["pct_current"]: self.hp -= max(1, int(self.hp * a["pct_current"]))
        else: self.hp -= a["cost"]

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
    return c["mat"] if c["kind"] == "caster" else c["atk"]

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
    if c["kind"] == "caster":
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
    def __init__(self, party, enemies, rng, log=False):
        self.party, self.enemies, self.rng = party, enemies, rng
        self.units = party + enemies
        self.lines = [] if log else None
        self.round = 0
        self.bonus_rounds = 0
        self.eligible, self.barred = set(), set()

    def say(self, s):
        if self.lines is not None: self.lines.append(s)

    def allies(self, u): return [x for x in (self.party if u.side == "party" else self.enemies) if x.alive]
    def foes(self, u): return [x for x in (self.enemies if u.side == "party" else self.party) if x.alive]
    def over(self): return not any(x.alive for x in self.party) or not any(x.alive for x in self.enemies)

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

    def roll(self, att, dfn):
        net = self.net_stage(att, dfn)
        graze = max(0.0, GRAZE_BASE - STEP * net)
        crit = CRIT_BASE + max(0, net - 2) * 0.05 + att.attrs["DEX"] / 20 / 100
        r = self.rng.random()
        if r < graze: return "graze"
        if r < graze + crit: return "crit"
        return "hit"

    def expected_roll_mult(self, att, dfn):
        net = self.net_stage(att, dfn)
        graze = max(0.0, GRAZE_BASE - STEP * net)
        crit = CRIT_BASE + max(0, net - 2) * 0.05 + att.attrs["DEX"] / 20 / 100
        return graze * GRAZE_MULT + crit * CRIT_MULT + (1 - graze - crit)

    def wil_ratio(self, att, dfn): return clamp(att.WIL / dfn.WIL, 0.5, 1.5)

    # ------------------------------------------------------------ damage
    def raw_damage(self, att, dfn, a):
        el = ELEMENT[a["element"]]
        phys = a["element"] in MARTIAL
        A = (att.ATK if phys else att.MAT) * stage_mult(att.stage("ATK" if phys else "MAT"))
        D = (dfn.DEF if phys else dfn.MDF) * stage_mult(dfn.stage("DEF" if phys else "MDF"))
        dmg = a["power"] * el["power"] * (A / D) * level_factor(att.level)
        if a["all"]: dmg *= ALL_POWER_MULT
        return dmg

    def expected_damage(self, att, dfn, a):
        aff = dfn.affinity(a["element"])
        mult = {"weak": 1.5, "resist": 0.5, "null": 0.0, "absorb": -1.0, "normal": 1.0}[aff]
        hits = ELEMENT[a["element"]]["hits"]
        return self.raw_damage(att, dfn, a) * hits * mult * self.expected_roll_mult(att, dfn)

    def heal_amount(self, healer, a):
        h = 1.5 * a["power"] * level_factor(healer.level) * healer.MAT / avg_attr(healer.level)
        return h * (ALL_POWER_MULT if a["all"] else 1)

    # ------------------------------------------------------------ statuses
    def apply_status(self, src, tgt, status, chance):
        if not tgt.alive or self.rng.random() >= chance: return False
        if status == "Cursed":
            if "Cursed" in tgt.status: return False
            stats = [self.rng.choice(["ATK", "MAT", "DEF", "MDF"]) for _ in range(2)]
            tgt.status["Cursed"] = dict(rounds=STATUS_DURATION, stats=stats)
        elif status == "Chilled":
            tgt.status["Chilled"] = dict(rounds=self.rng.randint(*CHILL_DURATION))
        elif status == "Frozen":
            tgt.status["Frozen"] = dict(rounds=self.rng.randint(*FREEZE_DURATION))
        elif status == "Death":
            tgt.hp = 0
            src.stats["statuses"] += 1
            self.say(f"      {tgt.name} is struck down by Helvad!")
            return True
        elif status == "AccDown":
            tgt.stages["ACC"] = clamp(tgt.stages["ACC"] - 1, -5, 5)
        else:
            if status in tgt.status: return False
            tgt.status[status] = dict(rounds=STATUS_DURATION)
        src.stats["statuses"] += 1
        self.say(f"      {tgt.name} is {status}!")
        return True

    def riders(self, att, tgt, a, result, was_weak):
        el = ELEMENT[a["element"]]
        if result == "graze" or not tgt.alive: return
        if a["status"]:      # martial skill with a status (Blot)
            self.apply_status(att, tgt, a["status"], STATUS_LINE_CHANCE[a["tier"]] * self.wil_ratio(att, tgt))
        rider = el["rider"]
        if not rider or a["tier"] == "Halv": return
        chance = RIDER_CHANCE[a["tier"]] * self.wil_ratio(att, tgt)
        if rider == "Chilled":
            if "Chilled" in tgt.status and "Frozen" not in tgt.status:
                self.apply_status(att, tgt, "Frozen", chance)
            elif "Chilled" not in tgt.status:
                self.apply_status(att, tgt, "Chilled", 1.0 if was_weak else chance)
        else:
            self.apply_status(att, tgt, rider, chance)

    # ------------------------------------------------------------ resolve one action
    def targets_for(self, u, a, chosen):
        if a["target"] == "self": return [u]
        pool = self.allies(u) if a["target"] == "ally" else self.foes(u)
        if not pool: return []
        if a["all"]: return pool
        if chosen in pool: return [chosen]
        if a["target"] == "ally":
            return [min(pool, key=lambda x: x.hp / x.maxhp)]
        return [self.rng.choice(pool)]

    def resolve(self, u, a, chosen, bonus):
        if not u.alive: return
        if "Bleeding" in u.status:
            dmg = max(1, int(u.maxhp * BLEED_TICK))
            u.hp -= dmg
            self.say(f"    {u.name} bleeds for {dmg}.")
            if not u.alive:
                self.say(f"    {u.name} is down!"); return
        if "Frozen" in u.status:
            self.say(f"    {u.name} is frozen solid."); return
        if "Stunned" in u.status and self.rng.random() < STUN_LOSE_CHANCE:
            del u.status["Stunned"]
            self.say(f"    {u.name} is stunned and loses the action!"); return
        if "Silenced" in u.status and a["cost_type"] == "MP" and a["cost"] > 0:
            free = [x for x in u.actions if x["cost"] == 0]
            if not free:
                self.say(f"    {u.name} is silenced and can't act!"); return
            a = free[0]; self.say(f"    {u.name} is silenced!")
        if not u.can_afford(a):
            affordable = [x for x in u.actions if u.can_afford(x)
                          and not ("Silenced" in u.status and x["cost_type"] == "MP" and x["cost"] > 0)]
            if not affordable:
                self.say(f"    {u.name} has nothing left to use."); return
            a = min(affordable, key=lambda x: x["cost"])
        tgts = self.targets_for(u, a, chosen)
        if not tgts: return
        u.pay(a)
        u.stats["actions"] += 1
        tag = " [Bonus]" if bonus else ""
        if a["kind"] == "defend":
            u.defending = True
            self.say(f"    {u.name} defends.{tag}"); return
        if a["kind"] == "heal":
            for t in tgts:
                h = min(self.heal_amount(u, a), t.maxhp - t.hp)
                t.hp += h; u.stats["healed"] += h
            self.say(f"    {u.name} casts {a['name']}, healing {', '.join(t.name for t in tgts)}.{tag}")
            return
        if a["kind"] == "stat":
            n = TIERS.index(a["tier"])
            for t in tgts:
                t.stages[a["stat"]] = clamp(t.stages[a["stat"]] + a["direction"] * n, -5, 5)
            self.say(f"    {u.name} casts {a['name']} on {', '.join(t.name for t in tgts)}.{tag}")
            return
        if a["kind"] == "cleanse":
            for t in tgts:
                t.status = {}
                for s in t.stages: t.stages[s] = max(0, t.stages[s])
            self.say(f"    {u.name} casts {a['name']}, washing {', '.join(t.name for t in tgts)} clean.{tag}")
            return
        if a["kind"] == "status":
            self.say(f"    {u.name} casts {a['name']}.{tag}")
            for t in tgts:
                res = self.roll(u, t)
                if res == "crit" and CRIT_EARNS_BONUS and not bonus: self.eligible.add(u)
                if res == "graze":
                    self.say(f"      {t.name} shrugs it off."); continue
                if a["status"] == "Death":
                    aff = {"resist": 0.5, "weak": 1.5, "null": 0.0, "absorb": 0.0}.get(t.affinity("Aska"), 1.0)
                    chance = HELVAD_CHANCE * self.wil_ratio(u, t) * aff
                else:
                    chance = STATUS_LINE_CHANCE[a["tier"]] * self.wil_ratio(u, t)
                if self.apply_status(u, t, a["status"], chance) and not t.alive:
                    self.say(f"      {t.name} is down!"); t.stats["downs"] += 1
            return
        # damage
        self.say(f"    {u.name} uses {a['name']}.{tag}")
        for t in tgts:
            if not t.alive: continue
            aff = t.affinity(a["element"])
            total, results = 0.0, []
            for _ in range(ELEMENT[a["element"]]["hits"]):
                res = self.roll(u, t)
                results.append(res)
                dmg = self.raw_damage(u, t, a)
                var = ELEMENT[a["element"]]["var"]
                dmg *= 1 + self.rng.uniform(-var, var)
                dmg *= {"graze": GRAZE_MULT, "hit": 1.0, "crit": CRIT_MULT}[res]
                dmg *= {"weak": 1.5, "resist": 0.5, "null": 0.0, "absorb": 1.0, "normal": 1.0}[aff]
                if t.defending: dmg *= 0.5
                if "Frozen" in t.status and aff != "absorb":
                    dmg *= SHATTER_MULT
                    del t.status["Frozen"]
                    self.say(f"      Shatter!")
                total += dmg
                u.stats[res if res != "hit" else "hits"] += 1
            if aff == "absorb":
                t.hp = min(t.maxhp, t.hp + total)
                self.say(f"      {t.name} absorbs it, healing {total:.0f}!")
                self.barred.add(u)
                if not bonus: self.eligible.add(t)
                continue
            t.hp -= total
            u.stats["dealt"] += total
            label = "/".join(r.capitalize() for r in results)
            extra = " Weak!" if aff == "weak" else " Resist." if aff == "resist" else " Null!" if aff == "null" else ""
            self.say(f"      {label} on {t.name}: {total:.0f}.{extra} ({max(0, t.hp):.0f}/{t.maxhp:.0f})")
            if aff == "null": self.barred.add(u)
            if (aff == "weak" or (CRIT_EARNS_BONUS and "crit" in results)) and not bonus:
                self.eligible.add(u)
                if aff == "weak": u.stats["weak"] += 1
            if not t.alive:
                self.say(f"      {t.name} is down!"); t.stats["downs"] += 1; continue
            best = "crit" if "crit" in results else "hit" if "hit" in results else "graze"
            self.riders(u, t, a, best, aff == "weak")

    # ------------------------------------------------------------ AI
    def declare(self, u):
        ref = 20 * level_factor(u.level)
        options = []
        for a in u.actions:
            if not u.can_afford(a): continue
            if "Silenced" in u.status and a["cost_type"] == "MP" and a["cost"] > 0: continue
            cost_pen = 0.25 * a["cost"] if a["cost_type"] == "MP" else 0.15 * a["cost"]
            if a["kind"] == "damage":
                foes = self.foes(u)
                if a["all"]:
                    s = sum(self.expected_damage(u, f, a) for f in foes)
                    options.append((s - cost_pen, a, None))
                else:
                    for f in foes:
                        s = self.expected_damage(u, f, a)
                        if f.affinity(a["element"]) == "weak": s *= 1.5     # tempo value
                        if s >= f.hp: s *= 1.3
                        if a["status"] and a["status"] not in f.status: s += 0.4 * ref
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
                    if a["status"] in f.status: continue
                    s = 0.9 * ref * STATUS_LINE_CHANCE[a["tier"]]
                    options.append((s - cost_pen, a, f))
            elif a["kind"] == "stat":
                pool = self.allies(u) if a["direction"] > 0 else self.foes(u)
                for x in pool:
                    if abs(x.stages[a["stat"]]) >= 2: continue
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
        if not options:
            return u.actions[0], None
        options.sort(key=lambda o: -o[0])
        pick = options[0] if self.rng.random() < 0.8 else self.rng.choice(options[:3])
        return pick[1], pick[2]

    # ------------------------------------------------------------ rounds
    def run_phase(self, actors, bonus):
        """Units act once per cost point; everyone's first actions resolve before anyone's second."""
        remaining = []
        for u in actors:
            if not u.alive: continue
            for k in range(1 if bonus else u.actions_per_round):
                remaining.append((k, u, self.declare(u)))
        while remaining and not self.over():
            remaining.sort(key=lambda e: (-e[0], "Feared" not in e[1].status, e[1].speed(), self.rng.random()),
                           reverse=True)
            k, u, (a, tgt) = remaining.pop(0)
            self.resolve(u, a, tgt, bonus)

    def fight(self, max_rounds=30):
        while not self.over() and self.round < max_rounds:
            self.round += 1
            self.say(f"Round {self.round}")
            for u in self.units:
                if u.alive and "Poisoned" in u.status:
                    dmg = max(1, int(u.maxhp * POISON_TICK)); u.hp -= dmg
                    self.say(f"    {u.name} takes {dmg} poison damage.")
                    if not u.alive: self.say(f"    {u.name} is down!")
            self.eligible, self.barred = set(), set()
            for u in self.units: u.defending = False
            self.run_phase([u for u in self.units if u.alive], bonus=False)
            entrants = [u for u in self.eligible if u.alive and u not in self.barred]
            if entrants and not self.over():
                self.bonus_rounds += 1
                for u in entrants: u.stats["bonus"] += 1
                self.say(f"  Bonus Round! ({', '.join(u.name for u in entrants)})")
                self.run_phase(entrants, bonus=True)
            for u in self.units:      # only numbered rounds tick durations
                for s in list(u.status):
                    u.status[s]["rounds"] -= 1
                    if u.status[s]["rounds"] <= 0: del u.status[s]
        winner = "party" if any(x.alive for x in self.party) and not any(x.alive for x in self.enemies) \
            else "enemy" if not any(x.alive for x in self.party) else "draw"
        self.say(f"Result: {winner} after {self.round} rounds")
        return winner


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
def family_move(m):
    k = m[0]
    if k == "strike":
        all_ = len(m) > 4 and m[4]
        status = m[5] if len(m) > 5 else None
        a = skill(m[1], m[2], m[3], all_=all_, status=status,
                  power=TIER_POWER[m[3]] * (0.7 if status else 1.0))
        a["cost"] = 0                      # enemies never pay HP
        return a
    if k == "spell": return damage_spell(m[1], m[2], len(m) > 3 and m[3])
    if k == "cleanse": return cleanse_spell(m[1], len(m) > 2 and m[2])
    if k == "ur":
        a = damage_spell(m[1], "Ur"); a["cost"] = ENEMY_UR_COST; return a
    if k == "status": return status_spell(m[1], m[2])
    if k == "stat": return stat_spell(m[1], m[2] > 0, m[3], all_=len(m) > 4 and m[4])

def spawn_family(family, rank_name, level):
    fam = FAMILIES[family]
    name, cost, hp, moves = next(r for r in fam["ranks"] if r[0] == rank_name)
    attrs = {k: attr_at(15.5, level) for k in ATTRS}
    for k in ("STR", "INT", "CON", "WIS"): attrs[k] += SPIRIT_TRAIN * (level - 1)
    body = HALV_BODY if name.startswith("Halv") else 1.0
    attrs["STR"] *= SPIRIT_DMG_SCALE * body; attrs["INT"] *= SPIRIT_DMG_SCALE * body
    u = Unit(name, "enemy", level, attrs, {"STR": 1.0}, {"INT": 1.0}, build_aff(**fam["aff"]),
             [family_move(m) for m in moves])
    u.maxhp *= hp * SPIRIT_HP_SCALE; u.hp = u.maxhp
    u.maxmp *= cost; u.mp = u.maxmp
    u.actions_per_round = cost
    u.rank = "Drott" if cost == 3 else rank_name
    u.family = family
    u.apply_body(family)
    return u

def family_encounter(level, rng, family, budget=6):
    fams = ["Draugr", "Bein"] if family == "Undead" else [family]
    out, left = [], budget
    while left > 0:
        f = rng.choice(fams)
        name, cost, _, _ = rng.choice([r for r in FAMILIES[f]["ranks"] if r[1] <= left])
        out.append(spawn_family(f, name, level)); left -= cost
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
