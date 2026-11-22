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
from gloss import GLOSS, KINDS, READING_KEY
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
    """Every set of carved parts to try on a verb: tier x target x manners (one or two, in name order) x Styng x Lonn."""
    mans = [()] + [(m,) for m in MANNER_ORDER] + list(itertools.combinations(MANNER_ORDER, 2))
    for tier in TIER_CHOICES:
        for target in (None, "Flok", "All"):
            for ms in mans:
                for styng in (False, True):
                    for lonn in (False, True):
                        yield dict(tier=tier, target=target, manners=ms, styng=styng, lonn=lonn)

def part_list(p):
    return [x for x in (None if p["tier"] == "Base" else p["tier"], p["target"], *p["manners"],
                        "Styng" if p["styng"] else None, "Lonn" if p["lonn"] else None) if x]

def kit_index():
    """(verb, parts) -> the class and legs whose kit holds it."""
    out = {}
    for cls, legs in KITS.items():
        for leg, kit in legs.items():
            for verb, parts in kit:
                n = words.normalize(verb, **parts)
                key = (verb, n["tier"], n["target"], n["manners"], n["styng"], n["lonn"])
                out.setdefault(key, []).append(leg)
    return out

def hero_words():
    kits, out = kit_index(), []
    for verb, v in VERBS.items():
        for p in carves(verb):
            try: a = compile_verb(verb, **p)
            except (ValueError, OverCap): continue
            key = (verb, p["tier"], p["target"], tuple(p["manners"]), p["styng"], p["lonn"])
            pr = a["parts"]
            out.append(dict(
                name=a["name"], verb=verb, cls=v.get("cls"), kind=a["kind"], parts=part_list(p),
                capstone=pr.get("capstone"), byname=pr.get("byname"),
                price=a["price"], cost_type=a["cost_type"], keywords=a["keywords"], share=share_of(a),
                element=a.get("element"), status=a.get("status"), also_status=a.get("also_status"),
                wide="all" if a["all"] else a.get("shape", "one"), text=engine.plain(a),
                past_the_ladder=a["price"] > COST_LADDER[-1], kit_legs=sorted(kits.get(key, []))))
    return out

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
                                                           word=rider[1]))
    return out

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
            units.setdefault(u.name, dict(name=u.name, family=e["family"], rank=e["rank"], element=e.get("element"),
                                          parts=decompose(u.name, table)))
            for a in u.actions:
                m = moves.setdefault(a["name"], dict(name=a["name"], kind=a["kind"], families=set(), users=set(),
                                                     english=" " in a["name"] or decompose(a["name"], table) is None,
                                                     parts=decompose(a["name"], table), text=engine.plain(a),
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

def two_readings(hero, moves, units):
    """Names the seam rules let a reader take apart two ways (Rodaska: Rod + Daska, or Rod + Aska)."""
    names = sorted({h["name"] for h in hero} | {m["name"] for m in moves} | {u["name"] for u in units})
    return {n: p for n in names for p in [parses(n)] if len(p) > 1}

# ---------------------------------------------------------------- the export
def export(path=OUT):
    import lab
    hero = hero_words(); moves, units = enemy_words(); use = code_atoms()
    speakers = {}
    for h in hero:
        rider = VERBS[h["verb"]].get("rider")
        said = [h["verb"]] + h["parts"] + ([rider[1]] if rider and "Lonn" in h["parts"] else [])
        said += [nm for nm in ROOT_NAMES if h["name"].endswith(nm.lower()) or h["name"] == nm]
        said += [nm for nm in (h["capstone"], h["byname"]) if nm]
        vp = parses(h["verb"])
        if len(vp) == 1 and len(vp[0]) > 1: said += vp[0]              # a compound verb: Aukskold is Auk + Skold
        for p in said: speakers.setdefault(p, set()).add("heroes")
    for m in moves:
        for p in m["parts"] or []: speakers.setdefault(p, set()).add("foes")
    for u in units:
        for p in u["parts"] or []: speakers.setdefault(p, set()).add("foes")
    entries = {}
    for k, e in GLOSS.items():
        entries[k] = dict(e, speakers=sorted(speakers.get(k, ())), in_code=sorted(use.get(k, ())))
    doc = dict(engine=lab.ENGINE, reading_key=READING_KEY, kinds=KINDS, words=entries, verbs=verb_table(),
               hero_words=hero, enemy_moves=moves, enemy_units=units, two_readings=two_readings(hero, moves, units),
               kits={c: {str(l): [compile_verb(v, **p)["name"] for v, p in kit] for l, kit in legs.items()}
                     for c, legs in KITS.items()},
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
