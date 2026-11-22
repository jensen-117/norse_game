"""The lexicon: every word the game can say, read from the code and joined to the glossary (grammar library L1).

    python3 lexicon.py            writes ../grammar_book/lexicon.json and prints a short count
    python3 lexicon.py --check    prints the glossary's gaps (atoms with no entry, built entries not in the code)

What a word *does* comes from the code: the hero words from words.compile_verb over every legal set of carved parts,
the enemy words from the spawned catalog. What a word *means* comes from gloss.py. Neither file is engine-hashed, so
the book can change without touching a fight record; the export carries the engine stamp it was read from.
"""
import itertools, json, os, sys
from data import *
import words
from words import compile_verb, OverCap, STATUS_ROOT, STAT_ROOT, WEAPON, MANNERS, TARGETS, RIDERS, VOWELS
from gloss import GLOSS, KINDS, READING_KEY, INTENT
import engine

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "grammar_book", "lexicon.json")
TIER_CHOICES = ("Halv", "Base", "Mer")              # what carving reaches (SOURCE_TIER["carve"])
MANNER_ORDER = [m for m in MANNERS if m]            # Snar, Tung, Bid, Jarf, Drif: the order a name shows them in

# ---------------------------------------------------------------- hero words: every legal carve of every verb
def share_of(a):
    """The move's damage or heal as a share of a clean Krosh or a base Lak (classes.md Part 7b): the yardstick's unit."""
    if a["kind"] == "damage" and a.get("power"):
        el = ELEMENT[a["element"]]
        return round(a["power"] * el["power"] * el["hits"] / TIER_POWER["Base"] * a.get("all_power", 1.0), 3)
    if a["kind"] in SCALES and a.get("power"):
        return round(a["power"] / TIER_POWER["Base"] * a.get("all_power", 1.0), 3)
    if a.get("styng"): return round(a["styng"] / TIER_POWER["Base"], 3)
    return None

def carves(verb):
    """Every set of carved parts to try on a verb: tier x target x manners (one or two, in name order) x Styng x a
    rider (none, its own, or another designated one by its word)."""
    mans = [()] + [(m,) for m in MANNER_ORDER] + list(itertools.combinations(MANNER_ORDER, 2))
    lonns = [False, True] + [w for _, w in VERBS[verb].get("riders", ())]
    for tier in TIER_CHOICES:
        for target in (None, "Flok", "All"):
            for ms in mans:
                for styng in (False, True):
                    for lonn in lonns:
                        yield dict(tier=tier, target=target, manners=ms, styng=styng, lonn=lonn)

def part_list(p):
    lonn = None if not p["lonn"] else "Lonn" if p["lonn"] is True else p["lonn"]
    return [x for x in (None if p["tier"] == "Base" else p["tier"], p["target"], *p["manners"],
                        "Styng" if p["styng"] else None, lonn) if x]

def kit_index():
    """(verb, parts) -> the class and legs whose kit holds it."""
    out = {}
    for cls, legs in KITS.items():
        for leg, kit in legs.items():
            for verb, parts in kit:
                n = words.normalize(verb, **parts)
                key = (verb, n["tier"], n["target"], n["manners"], n["styng"], n["rider"][1] if n["lonn"] else None)
                out.setdefault(key, []).append(leg)
    return out

def hero_words():
    kits, out = kit_index(), []
    for verb, v in VERBS.items():
        for p in carves(verb):
            try: a = compile_verb(verb, **p)
            except (ValueError, OverCap): continue
            w = CLASSES.get(v.get("cls"), {}).get("weapon")     # a martial root's range in this class's weapon, as
            if a.get("root") and w: a["reach"] = RANGES[engine.root_range(a["root"], w)]   # build_hero sets it
            pr = a["parts"]
            key = (verb, p["tier"], p["target"], tuple(p["manners"]), p["styng"], pr.get("rider_word"))
            said = [verb] + part_list(p) + ([pr["rider_word"]] if pr.get("rider_word") else [])
            said += [nm for nm, (vb, ps) in ROOT_NAMES.items() if vb == verb and ps <= frozenset(part_list(p))]
            said += [nm for nm in (pr.get("capstone"), pr.get("byname")) if nm]
            out.append(dict(
                name=a["name"], verb=verb, cls=v.get("cls"), kind=a["kind"], parts=part_list(p),
                atoms=expand([x for x in said if x in GLOSS]),
                rider_word=pr.get("rider_word"), carve=dict(p, manners=list(p["manners"])),
                key=bench_key(verb, p["tier"], p["target"], p["manners"], p["styng"], pr.get("rider_word")),
                rule_name=words.join_morphemes([x for x in (p["target"], None if p["tier"] == "Base" else p["tier"],
                                                            "Styng" if p["styng"] else None, *p["manners"],
                                                            pr.get("rider_word"), verb) if x]),
                capstone=pr.get("capstone"), byname=pr.get("byname"),
                price=a["price"], cost_type=a["cost_type"], keywords=a["keywords"], share=share_of(a),
                element=a.get("element"), status=a.get("status"), also_status=a.get("also_status"),
                wide="all" if a["all"] else a.get("shape", "one"), text=engine.plain(a),
                past_the_ladder=a["price"] > COST_LADDER[-1], kit_legs=sorted(kits.get(key, []))))
    return out

BENCH_PARTS = ("Halv", "Mer", "Flok", "All", "Snar", "Tung", "Bid", "Jarf", "Drif", "Styng", "Lonn")

def rider_words():
    """Every rider word a verb owns, across the verbs (Brak, Blot, Bann, Rod...)."""
    out = []
    for v in VERBS.values():
        for _, w in ([v["rider"]] if v.get("rider") else []) + list(v.get("riders", ())):
            if w not in out and w != "Lonn": out.append(w)
    return out

def bench_key(verb, tier, target, manners, styng, rider_word):
    """One carve as one string: the workbench looks a legal word up by it (bench_rules.js builds the same)."""
    return "|".join([verb, tier or "Base", target or "", "+".join(manners), "S" if styng else "", rider_word or ""])

def single(verb, part):
    """The compiler's own words for refusing one part on one verb, or None if the part alone is fine."""
    kw = {"Halv": dict(tier="Halv"), "Mer": dict(tier="Mer"), "Flok": dict(target="Flok"), "All": dict(target="All"),
          "Styng": dict(styng=True), "Lonn": dict(lonn=True)}.get(part)
    if kw is None: kw = dict(manners=(part,)) if part in MANNER_ORDER else dict(lonn=part)
    try: words.normalize(verb, **kw); return None
    except ValueError as e: return str(e)

def bench():
    """What the workbench needs to judge a carve without the compiler: each verb's refusals part by part (the
    compiler's own words), the cap, the capstones, and the rider words. bench_rules.js applies them; test_gloss
    checks it against compile_verb on every carve."""
    refuse = {v: {p: r for p in BENCH_PARTS + tuple(rider_words()) for r in [single(v, p)] if r} for v in VERBS}
    own = {v: (row["rider"][1] if row.get("rider") else None) for v, row in VERBS.items()}
    return dict(parts=list(BENCH_PARTS), rider_words=rider_words(), refuse=refuse, own_rider=own, cap=UPGRADE_CAP,
                capstones={nm: dict(verb=vb, parts=sorted(ps)) for nm, (vb, ps) in CAPSTONES.items()},
                speed_manners=sorted(SPEED_MANNERS), manner_order=MANNER_ORDER,
                rider_owners={w: sorted(vs) for w, vs in rider_owners().items()},
                name_parts={nm: dict(verb=vb, parts=sorted(ps)) for nm, (vb, ps) in {**ROOT_NAMES, **BYNAMES, **CAPSTONES}.items()},
                vowels="".join(sorted(VOWELS)),
                slots=["target", "tier", "styng", "manners", "rider", "root"])

def verb_table():
    """Per verb: what it is and which parts it takes (the workbench's legal tiles)."""
    out = {}
    for verb, v in VERBS.items():
        takes = {"tiers": [], "targets": [], "manners": [], "styng": False, "lonn": False}
        for t in TIER_CHOICES:
            try: words.normalize(verb, tier=t); takes["tiers"].append(t)
            except ValueError: pass
        for tg in ("Flok", "All"):
            try: words.normalize(verb, target=tg); takes["targets"].append(tg)
            except ValueError: pass
        for m in MANNER_ORDER:
            try: words.normalize(verb, manners=(m,)); takes["manners"].append(m)
            except ValueError: pass
        for flag in ("styng", "lonn"):
            try: words.normalize(verb, **{flag: True}); takes[flag] = True
            except ValueError: pass
        rider = v.get("rider")
        out[verb] = dict(cls=v.get("cls"), kind=v["kind"], rung=v.get("cost"), weight=v.get("weight", 0),
                         knots=v.get("knots", 0), element=v.get("element"), takes=takes,
                         rider=None if not rider else dict(gives=rider[0] if isinstance(rider[0], str) else f"{rider[0][0]} {rider[0][1]:+d}",
                                                           word=rider[1]),
                         more_riders=[dict(gives=g, word=w) for g, w in v.get("riders", ())])
    return out

def part_effects():
    """What each part does to a hero's move, in words, with the numbers read from the constants (so it can't drift)."""
    m, pct = MANNERS, lambda x: f"x{x:g}"
    mp = lambda n: CLASS_MANNER_POWER.get(n, m[n].get("power", 1.0))
    return {
        "Halv": f"Half a base hit ({pct(CLASS_TIER['Halv'])}), at the Halv rung: {HALV_COST['HP']} HP or {HALV_COST['MP']} MP. Attacks only.",
        "Mer": f"{pct(round(CLASS_TIER['Mer'], 2))} power; one step dearer (x2 the cost).",
        "Jatte": "Two rungs up. Found, not carved.",
        "Ur": "The top rung. Only on gear.",
        "Flok": f"Hits a row. {TARGET_STEPS['Flok']} steps dearer (x{2 ** TARGET_STEPS['Flok']} the cost).",
        "All": f"Hits everyone, each at {pct(ALL_SHARE)}. {TARGET_STEPS['All']} steps dearer (x{2 ** TARGET_STEPS['All']} the cost).",
        "Mark": "Paints a spot: whoever stands there is hit. The foes' grammar.",
        "Snar": f"Acts a group sooner (Swift), at {pct(mp('Snar'))} power for heroes. One step dearer.",
        "Tung": f"Acts late (Heavy), at {pct(mp('Tung'))} power. One step dearer. Damage and heals.",
        "Bid": f"Winds up a round, then lands at {pct(mp('Bid'))}; lost if the user is broken. One step dearer. Damage and heals.",
        "Jarf": f"{pct(mp('Jarf'))} power, a {round(100 * (CRIT_BASE + m['Jarf']['crit_bonus']))}% crit that hits x{m['Jarf']['crit_mult']:g}. One step dearer. Damage only.",
        "Drif": f"A flurry: hits of {pct(m['Drif']['flurry']['per'])} that keep coming on a coin flip, up to {m['Drif']['flurry']['max']}. One step dearer. Damage only.",
        "Styng": f"Adds a hit of {pct(STYNG_POWER)} the class's base hit to a move that deals none. One step dearer.",
        "Lonn": f"Adds the move's own rider (a status, or a stage); a hit with a rider lands at {pct(RIDER_SHARE)}. One step dearer.",
        "Auk": "Raises the stat its word names.", "Ned": "Lowers the stat its word names.",
    }

# ---------------------------------------------------------------- the seam rules, run backwards
def atoms():
    """Every spelling the book can take a word apart into, lowercase -> its glossary key."""
    return {k.lower(): k for k in GLOSS if " " not in k and "!" not in k and "'" not in k}

def parses(word, table=None):
    """Every fewest-part way to take a compound apart into glossary atoms, undoing the seam rules (pillars Part 5):
    identical letters merged (Brak + Krosh = Brakrosh), and vowel + vowel, the first vowel dropped (Jatte + Eld =
    Jatteld). More than one means the word reads two ways (Rodaska: Rod + Daska, or Rod + Aska). Empty when it doesn't
    come apart (an English name, or a word with no entry)."""
    table = table or atoms(); w = word.lower(); n = len(w)
    best = {n: [[]]}                                   # position -> the fewest-part parses of w[position:]
    for i in range(n - 1, -1, -1):
        cands = []
        for sp, key in table.items():
            ends = []
            if w.startswith(sp, i): ends.append(i + len(sp))                                   # plain
            if i > 0 and sp[0] == w[i - 1] and len(sp) > 1 and w.startswith(sp[1:], i):        # its first letter merged
                ends.append(i + len(sp) - 1)
            if sp[-1] in VOWELS and len(sp) > 1 and w.startswith(sp[:-1], i):                  # its last vowel dropped
                j = i + len(sp) - 1
                if j < n and w[j] in VOWELS: ends.append(j)
            for j in ends:
                for rest in best.get(j, []): cands.append([key] + rest)
        if cands:
            k = min(map(len, cands))
            uniq = []
            for c in cands:
                if len(c) == k and c not in uniq: uniq.append(c)
            best[i] = uniq
        else: best[i] = []
    return best[0]

def expand(atoms_, table=None):
    """The atoms, plus the atoms inside any that are themselves compounds (Aukskold: Auk + Skold), each once."""
    table = table or atoms(); out = []
    for a in atoms_:
        out.append(a)
        inner = parses(a, {sp: k for sp, k in table.items() if k != a})
        if len(inner) == 1 and len(inner[0]) > 1: out += inner[0]
    return [x for i, x in enumerate(out) if x not in out[:i]]

def decompose(word, table=None):
    """The first fewest-part reading, or None."""
    p = parses(word, table)
    return p[0] if p else None

# ---------------------------------------------------------------- enemy words: read from the spawned catalog
def enemy_words():
    from composer import catalog, spawn
    moves, units, table = {}, {}, atoms()
    for e in catalog():
        for u in spawn([(0, 0, e)], ENEMY_LEVEL):
            parts = decompose(u.name, table)
            units.setdefault(u.name, dict(name=u.name, family=e["family"], rank=e["rank"], element=e.get("element"),
                                          parts=parts, atoms=expand(parts or [], table)))
            for a in u.actions:
                m = moves.setdefault(a["name"], dict(name=a["name"], kind=a["kind"], families=set(), users=set(),
                                                     english=" " in a["name"] or decompose(a["name"], table) is None,
                                                     parts=decompose(a["name"], table), text=engine.plain(a),
                                                     atoms=expand(decompose(a["name"], table) or [], table),
                                                     element=a.get("element"), status=a.get("status")))
                m["families"].add(e["family"]); m["users"].add(u.name)
    for m in moves.values():
        m["families"], m["users"] = sorted(m["families"]), len(m["users"])
    return sorted(moves.values(), key=lambda m: m["name"]), sorted(units.values(), key=lambda u: u["name"])

# ---------------------------------------------------------------- the atoms the code uses, and where
def code_atoms():
    """atom -> where the code uses it. The test holds the glossary to this list."""
    use = {}
    def add(w, where):
        if w: use.setdefault(w, set()).add(where)
    for e in ELEMENT: add(e, "ELEMENT")
    for t in TIERS:
        if t != "Base": add(t, "TIERS")
    for t in TARGETS:
        add(t, "TARGETS")
    for m in MANNERS: add(m, "MANNERS")
    add("Styng", "compile_verb"); add("Lonn", "compile_verb"); add("Auk", "stat grammar"); add("Ned", "stat grammar")
    for r in STAT_ROOT.values(): add(r, "STAT_ROOT")
    for r in STATUS_ROOT.values(): add(r, "STATUS_ROOT")
    for r in RIDERS:
        add(r, "RIDERS")
    for v in VERBS.values():
        if v.get("rider"): add(v["rider"][1], "verb riders")
        for _, w in v.get("riders", ()): add(w, "verb riders")
    for r in WEAPON: add(r, "WEAPON")
    for verb, v in VERBS.items():
        if v["kind"] != "damage" or verb not in ELEMENT: add(verb, "VERBS")
    for k in list(ROOT_NAMES) + list(BYNAMES) + list(CAPSTONES): add(k, "names")
    for c in CLASSES: add(c, "CLASSES")
    for s in STATUSES: add(s, "STATUSES")
    for c in COUNTER_OF:
        if c != "AccDown": add(c, "COUNTER_OF")       # AccDown: an internal alias of Blinded
    for k in KEYWORDS: add(k, "KEYWORDS")
    for it in ITEMS.values(): add(it["name"], "ITEMS")
    for f in ("Ande", "Mogel", "Draugr", "Bein", "Drattr", "Djur", "Oskorei"): add(f, "families")
    for units in OSKOREI_TIERS.values():                  # the Hunt's fixed formations (not in the catalog yet)
        for u in units:
            if isinstance(u, tuple) and " " not in u[0] and "-" not in u[0]: add(u[0], "OSKOREI_TIERS")
    return {k: sorted(v) for k, v in use.items()}

def gaps():
    """What the glossary misses (atoms with no entry) and what it claims (built entries the code has no trace of)."""
    use = code_atoms()
    missing = sorted(w for w in use if w not in GLOSS)
    built_names = {w["name"] for w in hero_words()}
    moves, units = enemy_words()
    said = built_names | {m["name"] for m in moves} | {u["name"] for u in units}
    found = set(use)
    for name in said:
        found |= set(decompose(name) or [])
    unclaimed = sorted(k for k, e in GLOSS.items() if e["state"] == "built" and k not in found
                       and e["kind"] not in ("action", "affinity", "status", "name_part", "myth"))
    return missing, unclaimed

def rider_owners():
    """A rider word -> the verbs it may sit in front of: its own verb, and that verb's root names (Rod: Egga, Daska)."""
    out = {}
    for verb, v in VERBS.items():
        for _, w in ([v["rider"]] if v.get("rider") else []) + list(v.get("riders", ())):
            out.setdefault(w, set()).update({verb}, (nm for nm, (vb, _) in ROOT_NAMES.items() if vb == verb))
    return out

def grammatical(parse):
    """Whether the grammar could build this reading, or only an eye could see it (Stormogel as Storm + Mogel):
    a move's root comes last; a family is followed only by its job (Bein + seidr); a stat word follows Auk or Ned;
    a rider word that belongs to a verb sits right before that verb. Returns the broken rule, or None."""
    owners = rider_owners()
    for i, a in enumerate(parse):
        kind, nxt = GLOSS[a]["kind"], parse[i + 1] if i + 1 < len(parse) else None
        if nxt is None: continue
        if kind in ("verb", "weapon", "name"): return f"{a} is a move's root: nothing follows it"
        if kind == "family" and GLOSS[nxt]["kind"] != "rank": return f"{a} is a family: only its job follows it"
        if kind == "rider" and a in owners and nxt not in owners[a]: return f"{a} belongs to {'/'.join(sorted(owners[a]))}"
    for i, a in enumerate(parse):
        if GLOSS[a]["kind"] == "stat" and (i == 0 or parse[i - 1] not in ("Auk", "Ned")): return f"{a} needs Auk or Ned before it"
    return None

def two_readings(hero, moves, units):
    """Names the seam rules let a reader take apart two ways (Rodaska: Rod + Daska, or Rod + Aska), each reading
    marked with whether the grammar could build it."""
    names = sorted({h["name"] for h in hero} | {m["name"] for m in moves} | {u["name"] for u in units})
    return {n: [dict(parts=x, broken=grammatical(x)) for x in p] for n in names for p in [parses(n)] if len(p) > 1}

# ---------------------------------------------------------------- the export
def export(path=OUT):
    import lab
    hero = hero_words(); moves, units = enemy_words(); use = code_atoms()
    speakers = {}
    for h in hero:
        for p in h["atoms"]: speakers.setdefault(p, set()).add("heroes")
    for m in moves + units:
        for p in m["atoms"]: speakers.setdefault(p, set()).add("foes")
    entries = {}
    for k, e in GLOSS.items():
        entries[k] = dict(e, speakers=sorted(speakers.get(k, ())), in_code=sorted(use.get(k, ())), intent=INTENT.get(k))
    doc = dict(engine=lab.ENGINE, reading_key=READING_KEY, kinds=KINDS, words=entries, verbs=verb_table(),
               hero_words=hero, enemy_moves=moves, enemy_units=units, two_readings=two_readings(hero, moves, units),
               kits={c: {str(l): [compile_verb(v, **p)["name"] for v, p in kit] for l, kit in legs.items()}
                     for c, legs in KITS.items()},
               part_effects=part_effects(),
               names={nm: vb for nm, (vb, _) in {**ROOT_NAMES, **BYNAMES, **CAPSTONES}.items()},
               classes=list(CLASSES), elements=list(ELEMENT), bench=bench(),
               rules=dict(order="Target + Tier + Styng + Manner + Rider + Root", cap=UPGRADE_CAP,
                          ladder=COST_LADDER, halv_cost=HALV_COST, target_steps=TARGET_STEPS,
                          seams=["Identical letters at a seam merge: Brak + Krosh = Brakrosh.",
                                 "Vowel + vowel: the second wins: Jatte + Eld = Jatteld.",
                                 "No special letters: ö and å are written o and a."]))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: json.dump(doc, f, ensure_ascii=False, separators=(",", ":"), default=list)
    return doc

if __name__ == "__main__":
    if "--check" in sys.argv:
        missing, unclaimed = gaps()
        print("no entry:", missing); print("built but not found:", unclaimed)
    else:
        d = export()
        print(f"{len(d['words'])} entries, {len(d['hero_words'])} hero words, {len(d['enemy_moves'])} enemy moves, "
              f"{len(d['enemy_units'])} enemy units -> {os.path.relpath(OUT)} ({os.path.getsize(OUT) // 1024} KB)")
