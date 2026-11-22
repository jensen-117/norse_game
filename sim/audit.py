"""The language audit (grammar library, Nov 21): what the language can build, what it can't yet say, where it repeats
itself. Read from the compiled moves themselves (what each one *does*), not from their labels.

    python3 audit.py      writes ../grammar_book/audit.json (the book's Audit chapter) and ../audit_report.md

Each effect is a status, a counter (a stage, by its worn name) or an act (damage, heal, cleanse...). For each one:
who gives it (hero words, foe moves, items), what takes it away, what pays it off. A gap is an effect with no hero
source, no foe source, nothing that removes it, or nothing that cashes it in. The primers (gloss.PRIMERS) say in plain
English what a word filling the gap would be trying to say: the brief for the search through the language quarries.
"""
import json, os
from collections import defaultdict
from data import *
from words import compile_verb
import lexicon
from gloss import GLOSS, INTENT, PRIMERS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "grammar_book", "audit.json")
REPORT = os.path.join(HERE, "..", "audit_report.md")
NAME_CAP = 15                                       # pillars Part 5c: past 15 letters a reachable name needs a byname

def counter(stat, sign):
    """A stage by the name it's worn under (Mighty, Sundered), or "MAT up" where the counter has no name yet."""
    names = STAT_NAMES.get(stat, (None, None))
    nm = names[1] if sign > 0 else names[0]
    return nm or f"{stat} {'up' if sign > 0 else 'down'}"

def worn(s):
    return "Blinded" if s == "AccDown" else s       # AccDown: the old game's spelling of Blinded

def effects(a, designated=False):
    """What one compiled move does, as effect names: the statuses and counters it leaves, and the act itself."""
    k, out = a["kind"], []
    if k == "damage":
        out.append("Damage")
        if a.get("pays_on"): out.append(f"pays off {a['pays_on']}")
        if a.get("pays_below"): out.append("pays off the wounded")
        if a.get("answer"): out.append("pays off hits taken")
        el = ELEMENT.get(a.get("element") or "", {})
        if not designated and not a.get("designated") and el.get("rider"): out.append(worn(el["rider"]))   # a foe spell's element rider
    elif k == "heal": out.append("Heal")
    elif k == "stat": out.append(counter(a["stat"], a["direction"]))
    elif k == "glide": out += ["Move", counter("EVA", 1)]
    elif k in ("song",): out.append("Song")
    elif k == "cleanse": out.append("Cleanse")
    elif k == "revive": out.append("Revive")
    elif k == "taunt": out.append("Taunt")
    elif k == "cover": out.append("Cover")
    elif k in ("windfall", "meditate", "mp"): out.append("MP back")
    elif k == "knot": out.append("Knot")
    elif k == "displace": out.append("Shove")
    elif k == "defend": out.append("Guard")
    elif k == "flee": out.append("Flee")
    if a.get("status"): out.append(worn(a["status"]))
    if a.get("also_status"): out.append(worn(a["also_status"]))
    for st, n in a.get("also", []) or []: out.append(counter(st, n))
    if a.get("styng") and k != "damage": out.append("Damage")
    return [x for i, x in enumerate(out) if x not in out[:i]]

# ---------------------------------------------------------------- who gives each effect
def sources():
    """effect -> {"heroes": [move names], "kits": [...], "foes": [...], "items": [...]}"""
    src = defaultdict(lambda: defaultdict(set))
    for h in lexicon.hero_words():
        a = compile_verb(h["verb"], **h["carve"])
        for e in effects(a, designated=True):
            src[e]["heroes"].add(h["name"])
            if h["kit_legs"]: src[e]["kits"].add(h["name"])
    from composer import catalog, spawn
    for e_ in catalog():
        for u in spawn([(0, 0, e_)], ENEMY_LEVEL):
            for a in u.actions:
                for e in effects(a): src[e]["foes"].add(a["name"])
    for e in ("Guard", "Move", "Flee"): src[e]["heroes"].add(f"{e} (everyone)"); src[e]["kits"].add(f"{e} (everyone)")
    src["MP back"]["heroes"].add("Meditate (casters)"); src["MP back"]["kits"].add("Meditate (casters)")
    for g in sorted(BEIN_GUARDIANS): src["Cover"]["foes"].add(f"{g} (family rule)")
    for s_, row in STATUSES.items():                     # a status reached by chaining another (Chilled twice: Frozen)
        if row.get("chain"):
            for side in ("heroes", "kits", "foes"):
                for n in src.get(s_, {}).get(side, ()): src[row["chain"]][side].add(f"{n} (twice)")
    for key, it in ITEMS.items():
        a = dict(it, all=it.get("all", False))
        for e in effects(dict(a, designated=True)): src[e]["items"].add(it["name"])
    return {e: {k: sorted(v) for k, v in d.items()} for e, d in src.items()}

# ---------------------------------------------------------------- what takes each away, and what cashes it in (the rules)
def removals():
    """effect -> the ways it ends, read from the status rows and the counter rules."""
    out = defaultdict(list)
    for s, row in STATUSES.items():
        if s == "Song": out[s].append("fades only by use: it heals until it runs out"); continue
        out[s].append("Skolja washes it off")
        if row.get("duration") is None and row.get("fade"): out[s].append("burns down on its own, a step a round")
        elif row.get("duration") is None: out[s].append("thaws or breaks free in time" if row.get("skip") else "lasts until removed")
        else: out[s].append("runs out in a few rounds")
        if row.get("shatter"): out[s].append("any damaging hit breaks it")
        if row.get("skip", {}).get("used_up"): out[s].append("clears the first time it costs an action")
    for stat, (down, up) in STAT_NAMES.items():
        for nm, other in ((down, up), (up, down)):
            if not nm: continue
            out[nm].append(f"fades a step each round it isn't renewed")
            out[nm].append(f"{other or 'its opposite'} pulls it back, stack for stack")
            if nm == down: out[nm].append("Skolja lifts it")
    return out

def payoffs():
    """effect -> what cashes it in, read from the rules (stage effects, status rows, pays_on verbs)."""
    out = defaultdict(list)
    for v, row in VERBS.items():
        if row.get("pays_on"): out[row["pays_on"]].append(f"{v} hits x{row['pays']:g} against it")
    for s, row in STATUSES.items():
        if row.get("shatter"): out[s].append(f"the next damaging hit shatters it, x{row['shatter']:g}")
        if row.get("flare"): out[s].append(f"{row['flare']} on a burning foe stokes the fire")
        if row.get("chain"): out[s].append(f"a second chill turns it into {row['chain']}")
        if row.get("rooted"): out[s].append("it can't step away from a taunt or a hammer; a shove crashes into it")
    out["Sundered"].append(f"every hit lands harder; Pierce finds the gaps (+{round(PIERCE_GAP * 100)}% a stack)")
    out["Marked"].append("every hit on it crits 1 in 3 and never grazes")
    out["Blinded"].append("its own hits whiff 1 in 3")
    out["Feeble"].append("its own hits land softer")
    out["Slowed"].append("it acts later in the round")
    out["Song"].append("heals each round at the start")
    for nm, txt in (("Mighty", "your hits land harder"), ("Fortified", "hits on you land softer"),
                    ("Evasive", "hits on you whiff 1 in 3"), ("Keen", "your hits crit 1 in 3, never graze"),
                    ("Quick", "you act sooner"), ("Poisoned", "ticks each round"), ("Bleeding", "ticks when it acts"),
                    ("Stunned", "may cost an action"), ("Bound", "costs an action"), ("Silenced", "blocks every MP move"),
                    ("Disarmed", "ATK and MAT down"), ("Cursed", "two stages down"), ("Feared", "acts late")):
        out[nm].append(txt)
    return out

# ---------------------------------------------------------------- the other lists
def byname_jobs(hero):
    return sorted([h["name"] for h in hero if len(h["name"]) > NAME_CAP and not h["byname"] and not h["capstone"]], key=len)

def past_ladder(hero):
    return sorted([(h["name"], h["price"], h["cost_type"]) for h in hero if h["past_the_ladder"]], key=lambda x: (x[1], x[0]))

def riderless():
    return [v for v, row in VERBS.items() if not row.get("rider") and row["kind"] not in ("windfall",)]

def same_job(src):
    """Effects that several distinct *words* give (not carves of one verb): where the language says one thing twice."""
    out = {}
    for e, d in src.items():
        verbs = sorted({lexicon_verb(n) for n in d.get("heroes", [])} - {None})
        if len(verbs) > 1 and e not in ("Damage",): out[e] = verbs
    return out

_VERB_OF = None
def lexicon_verb(name):
    global _VERB_OF
    if _VERB_OF is None: _VERB_OF = {h["name"]: h["verb"] for h in lexicon.hero_words()}
    return _VERB_OF.get(name)

def gaps(src, rem, pay):
    """Every effect the rules know, and what's missing for it."""
    known = set(STATUSES) | {nm for pair in STAT_NAMES.values() for nm in pair if nm} | {counter("MAT", 1), counter("MAT", -1),
                                                                                       counter("MDF", 1), counter("MDF", -1)}
    known |= {e for e in src if not e.startswith("pays off")}
    out = {}
    for e in sorted(known):
        d = src.get(e, {})
        missing = []
        if not d.get("heroes"): missing.append("no hero gives it")
        elif not d.get("kits"): missing.append("no hero kit carries it")
        if not d.get("foes"): missing.append("no foe gives it")
        if (e in STATUSES or e in COUNTER_OF) and not pay.get(e): missing.append("nothing reads it")
        out[e] = missing
    return out

def build():
    hero = lexicon.hero_words(); src = sources(); rem = removals(); pay = payoffs()
    gp = gaps(src, rem, pay)
    effects_table = {e: dict(sources=src.get(e, {}), removed=rem.get(e, []), paid=pay.get(e, []), missing=gp.get(e, []),
                             intent=INTENT.get(e), primer=PRIMERS.get(e)) for e in sorted(gp)}
    return dict(
        effects=effects_table,
        intents={k: v for k, v in INTENT.items()},
        byname_jobs=byname_jobs(hero),
        past_ladder=past_ladder(hero),
        riderless=[dict(verb=v, intent=INTENT.get(v), primer=PRIMERS.get(f"{v} rider")) for v in riderless()],
        same_job=same_job(src),
        quarry=[dict(effect=e, primer=PRIMERS[e]) for e in sorted(PRIMERS) if " rider" not in e],
    )

def report(doc):
    L = ["# The Language Audit", "",
         "Generated by `sim/audit.py` from the compiled moves (what each move does, not its label). The book's Audit chapter shows the same data.", ""]
    L += ["## Effects: who gives them, what ends them, what cashes them in", "",
          "| Effect | Trying to say | Heroes (kit) | Foes | Missing |", "|---|---|---|---|---|"]
    for e, r in doc["effects"].items():
        s = r["sources"]
        L.append(f"| {e} | {r['intent'] or ''} | {len(s.get('heroes', []))} ({len(s.get('kits', []))}) | {len(s.get('foes', []))} | {'; '.join(r['missing'])} |")
    L += ["", "## The quarry: primers for words the language still needs", ""]
    for q in doc["quarry"]: L.append(f"- **{q['effect']}:** {q['primer']}")
    L += ["", f"## Byname jobs: {len(doc['byname_jobs'])} reachable names past {NAME_CAP} letters", "", ", ".join(doc["byname_jobs"]), ""]
    L += [f"## Past the ladder: {len(doc['past_ladder'])} legal carves dearer than {COST_LADDER[-1]}", "",
          ", ".join(f"{n} ({p} {t})" for n, p, t in doc["past_ladder"]), ""]
    L += ["## Verbs with no rider", ""]
    for r in doc["riderless"]: L.append(f"- **{r['verb']}:** {r['intent'] or ''}" + (f" *Rider primer:* {r['primer']}" if r["primer"] else ""))
    L += ["", "## One effect, several words", ""]
    for e, vs in doc["same_job"].items(): L.append(f"- **{e}:** {', '.join(vs)}")
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    doc = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(doc, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
    open(REPORT, "w").write(report(doc))
    gaps_ = {e: r["missing"] for e, r in doc["effects"].items() if r["missing"]}
    print(f"{len(doc['effects'])} effects, {len(gaps_)} with gaps; {len(doc['byname_jobs'])} byname jobs; "
          f"{len(doc['past_ladder'])} past the ladder; {len(doc['riderless'])} riderless verbs")
