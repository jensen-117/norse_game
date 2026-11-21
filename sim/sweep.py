"""The level sweep (refactor_plan Waves 3 and 5; pillars Part 5b).

Layer 1, hit counts: the five sheet heroes (kit leg 1) against every enemy rank of every family, in a new-game Battle
(so HERO_POWER, ENEMY_DAMAGE and TIER_HP apply exactly as in play). Expected hits from the damage model (the
graze/hit/crit roll included), neutral affinities, each class's base attack:
  - party hits to kill one: its max HP over one hero's expected hit;
  - its hits to kill a hero: the hero's max HP over the enemy's best expected single-target hit.
The solver finds the settings that best fit the targets: HERO_POWER from Trash and Regular, TIER_HP for Elite and
Boss, ENEMY_DAMAGE from all four (least squares on the logs, since hits scale as 1/multiplier).

Layer 2, real fights: the starting party against rooms rolled by the composer in each place (a fodder fight, an
elite fight, a boss fight), played by the AI: win rate, rounds, HP and MP spent. The AI plays worse than a person,
so these are a floor.

    python3 sweep.py [n_fights]          # writes ../sweep_report.md
    python3 sweep.py --check             # is the saved report from these sources? (fast: the source hash)
    python3 sweep.py --check --rerun     # ...and does it reproduce? (reruns at the report's n, writes nothing)

Provenance (review C14): the report's header carries a hash of every source it depends on and its whole
configuration, so a rules change can't leave it silently stale.
"""
import hashlib, math, random, re, statistics, sys, os
import data
from engine import *
from composer import catalog, habitat, compose, place, spawn as spawn_pack, CompositionError

TARGET_KILL = {"Trash": 3, "Regular": 6, "Elite": 12, "Boss": 18}        # party hits to kill one (at least, above Trash)
TARGET_DIE = {"Trash": 6.5, "Regular": 5, "Elite": 4, "Boss": 3}         # its hits to kill a hero
TARGET_COST = {"fodder": "10-25%", "elite": "40-50%", "boss": "most of it"}   # party HP a room should cost, played well
TIERS_ = ["Trash", "Regular", "Elite", "Boss"]
CLASSES5 = list(KITS)

def roster(L):
    """Every enemy rank at level L, freshly spawned: (family, unit)."""
    out = []
    for fam in ("Draugr", "Bein", "Drattr", "Djur"):
        for r in rank_rows(fam): out.append((fam, spawn_family(fam, r["name"], L, job=r["job"])))
    for rank, r in SPIRIT_RANKS:
        for el in ("Eld", "Vatn", "Blast", "Jord"): out.append(("Ande", spawn_spirit(rank, el, L)))
    for rank, r in MOGEL_RANKS: out.append(("Mogel", spawn_mogel(rank, "Jord", L)))
    return out

def hits(H=None, E=None):
    """Layer 1 at the current settings: {tier: [party hits]}, {tier: {class: [its hits]}}."""
    H, E = H or SHEET_LEVEL, E or ENEMY_LEVEL
    kill = {t: [] for t in TIERS_}; die = {t: {c: [] for c in CLASSES5} for t in TIERS_}
    for fam, e in roster(E):
        heroes = [build_hero(c, 1, H) for c in CLASSES5]
        for h in heroes: h.aff = {}
        e.aff = {}
        t = enemy_tier(e)
        b = Battle(heroes, [e], random.Random(1))          # a new-game fight: the settings apply to e once
        for h in heroes:
            atk = next(a for a in h.actions if a["name"] == BASIC_VERB[h.cls])
            kill[t].append(e.maxhp / b.expected_damage(h, e, atk))
            best = max((b.expected_damage(e, h, a) for a in e.actions if a["kind"] == "damage" and not a["all"]), default=0)
            if best: die[t][h.cls].append(h.maxhp / best)
    return kill, die

def med(xs): return statistics.median(xs)
def die_all(die, t): return [x for c in CLASSES5 for x in die[t][c]]

def solve(kill, die):
    """The settings that best fit the targets, from a measurement at the current settings."""
    p0, d0, hp0 = HERO_POWER["Vasara"], ENEMY_DAMAGE, dict(TIER_HP)
    base = {t: med(kill[t]) * p0 / hp0[t] for t in TIERS_}           # hits per unit of tier HP, at power 1
    p = math.exp(statistics.mean(math.log(base[t] / TARGET_KILL[t]) for t in ("Trash", "Regular")))
    tier = {t: (1.0 if t in ("Trash", "Regular") else TARGET_KILL[t] * p / base[t]) for t in TIERS_}
    d = math.exp(statistics.mean(math.log(med(die_all(die, t)) * d0 / TARGET_DIE[t]) for t in TIERS_))
    return p, d, tier, base

def predict(base, die, d0, p, d, tier):
    return ({t: base[t] * tier[t] / p for t in TIERS_}, {t: med(die_all(die, t)) * d0 / d for t in TIERS_})

# ---------------------------------------------------------------- Layer 2: rooms, played
CAT = catalog()
def room(rng, where, kind, L, budget=6):
    pool = habitat(CAT, where)
    tierof = lambda e: "Boss" if e["cost"] >= 3 else "Trash" if e["rank"].startswith(("Halv", "Litel")) else "Elite" if e["rank"].startswith("Stor") else "Regular"
    want = {"fodder": {"Trash", "Regular"}, "elite": {"Trash", "Regular", "Elite"}, "boss": {"Trash", "Regular", "Boss"}}[kind]   # odd sizes fill with Trash
    pool = [e for e in pool if tierof(e) in want]
    for _ in range(200):
        picks = compose(rng, pool, dict(budget=budget, cost_caps={3: 1}))
        ts = [tierof(e) for e in picks]
        if kind == "elite" and "Elite" not in ts: continue
        if kind == "boss" and "Boss" not in ts: continue
        return spawn_pack(place(picks), L)
    raise CompositionError(f"no {kind} room in {where}")

SHAPES = [("fodder", 3), ("fodder", 4), ("fodder", 5), ("fodder", 6), ("elite", 4), ("elite", 5), ("elite", 6),
          ("boss", 4), ("boss", 5), ("boss", 6)]

def layer2(n, party_classes=("Vasara", "Ullar", "Brennumar"), leg=1, shapes=SHAPES):
    """Rooms of each shape (kind, slot budget), played by the AI: wins, rounds, HP and MP spent (of wins), falls."""
    out = {}
    for kind, budget in shapes:
        wins = rounds = 0; lost, spent, falls = [], [], 0; rs = []
        for i in range(n):
            rng = random.Random(1000 + i); where = ("Barrow", "Wildwood", "Rapids")[i % 3]
            party = [build_hero(c, leg) for c in party_classes]
            foes = room(rng, where, kind, ENEMY_LEVEL, budget)
            b = Battle(party, foes, rng); w = b.fight()
            hp0 = sum(h.maxhp for h in party)
            if w == "party":
                wins += 1; rs.append(b.round)
                lost.append(1 - sum(max(0, h.hp) for h in party) / hp0)
                mags = [h for h in party if CLASSES[h.cls]["kind"] == "magical"]
                if mags: spent.append(1 - sum(h.mp for h in mags) / sum(h.maxmp for h in mags))
            falls += sum(h.stats["downs"] for h in party)
        out[(kind, budget)] = dict(win=wins / n, rounds=med(rs) if rs else None, hp=statistics.mean(lost) if lost else None,
                         mp=statistics.mean(spent) if spent else None, falls=falls / n)
    return out

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES = ("data.py", "words.py", "engine.py", "grammar.py", "composer.py", "sweep.py")
REPORT = os.path.join(HERE, "..", "sweep_report.md")
PARTIES = (("The starting three, kit leg 1", ("Vasara", "Ullar", "Brennumar"), 1),
           ("The starting three, kit leg 3", ("Vasara", "Ullar", "Brennumar"), 3),
           ("Vasara, Dagskald, Brennumar, kit leg 1", ("Vasara", "Dagskald", "Brennumar"), 1))

def source_hash():
    """SHA-256 over the sources the sweep's numbers depend on (line endings normalised), first 12 hex digits."""
    h = hashlib.sha256()
    for f in SOURCES: h.update(f.encode()); h.update(open(os.path.join(HERE, f), "rb").read().replace(b"\r\n", b"\n"))
    return h.hexdigest()[:12]

def provenance(n):
    return (f"Source hash `{source_hash()}` ({', '.join(SOURCES)}); rules profile new; {n} fights per room shape, seeds "
            f"1000+i, places rotating Barrow, Wildwood, Rapids; shapes {', '.join(f'{k} {b}' for k, b in SHAPES)}; parties "
            f"{'; '.join(f'{c} leg {g}' for _, c, g in PARTIES)}. Check with `python3 sweep.py --check [--rerun]`.")

def report(n):
    kill, die = hits()
    p, d, tier, base = solve(kill, die)
    pk, pd = predict(base, die, ENEMY_DAMAGE, p, d, tier)
    L = [f"# Level sweep (generated by sim/sweep.py, {SHEET_LEVEL} v {ENEMY_LEVEL})", "", provenance(n), "",
         f"Current settings: HERO_POWER x{HERO_POWER['Vasara']}, ENEMY_DAMAGE x{ENEMY_DAMAGE}, TIER_HP {TIER_HP}.", "",
         "## Layer 1: hit counts (medians; neutral affinities; kit leg 1)", "",
         "| | " + " | ".join(TIERS_) + " |", "|---" * 5 + "|",
         "| Party hits to kill: now | " + " | ".join(f"{med(kill[t]):.1f}" for t in TIERS_) + " |",
         "| Party hits to kill: target | " + " | ".join(f"{TARGET_KILL[t]}{'' if t == 'Trash' else '+'}" for t in TIERS_) + " |",
         "| Its hits to kill a hero: now | " + " | ".join(f"{med(die_all(die, t)):.1f}" for t in TIERS_) + " |",
         "| Its hits to kill a hero: target | " + " | ".join(f"{TARGET_DIE[t]:g}" for t in TIERS_) + " |", "",
         "**By class, its hits to kill a hero:**", "", "| Tier | " + " | ".join(CLASSES5) + " |", "|---" * 6 + "|"]
    for t in TIERS_: L.append(f"| {t} | " + " | ".join(f"{med(die[t][c]):.1f}" for c in CLASSES5) + " |")
    L += ["", "### The solver's fit", "",
          f"HERO_POWER **x{p:.2f}**, ENEMY_DAMAGE **x{d:.2f}**, TIER_HP **Elite x{tier['Elite']:.2f}, Boss x{tier['Boss']:.2f}**. "
          "Predicted at those settings:", "",
          "| | " + " | ".join(TIERS_) + " |", "|---" * 5 + "|",
          "| Party hits to kill | " + " | ".join(f"{pk[t]:.1f}" for t in TIERS_) + " |",
          "| Its hits to kill a hero | " + " | ".join(f"{pd[t]:.1f}" for t in TIERS_) + " |", "",
          "**Joseph's power ladder** (at the solved enemy damage and tier HP): party hits to kill Trash / Regular / Elite / Boss", "",
          "| Power | Trash | Regular | Elite | Boss |", "|---|---|---|---|---|"]
    for q in (1.15, 1.25, 1.35, 1.4, 1.5):
        L.append(f"| x{q} | " + " | ".join(f"{base[t] * tier[t] / q:.1f}" for t in TIERS_) + " |")
    L += ["", "## Layer 2: room shapes, played by the AI (a floor: it plays worse than a person)", "",
          f"{n} fights per shape (kind, slots), rotating the Barrow, the Wildwood and the Rapids; every enemy acts once a "
          f"round (ENEMY_ACTIONS {ENEMY_ACTIONS}); every fight from full HP and MP; rounds and HP and MP spent are for "
          "wins. Room costs the pace table wants, played well: fodder 10-25% of the party's HP, elite 40-50%, boss most of it.", ""]
    for label, cls, leg in PARTIES:
        r = layer2(n, cls, leg)
        ex = sorted({nm for c in cls for nm, _ in build_hero(c, leg).excluded})
        if ex: L += [f"*Kit moves not yet playable, left out: {', '.join(ex)}.*", ""]
        L += [f"**{label}:**", "", "| Room (slots) | Wins | Rounds | HP spent | MP spent | Falls per fight |", "|---|---|---|---|---|---|"]
        for (k, bud), v in r.items():
            f = lambda x, pct=True: "-" if x is None else (f"{x:.0%}" if pct else f"{x:g}")
            L.append(f"| {k} ({bud}) | {v['win']:.0%} | {f(v['rounds'], False)} | {f(v['hp'])} | {f(v['mp'])} | {v['falls']:.2f} |")
        L.append("")
    return "\n".join(L) + "\n", (p, d, tier)

def check(rerun=False):
    """Is the saved report from these sources, and (rerun) does it reproduce? Returns the problems; writes nothing."""
    saved = open(REPORT).read().replace("\r\n", "\n")
    m = re.search(r"Source hash `([0-9a-f]+)`.*?; (\d+) fights per room shape", saved)
    if not m: return ["the saved report has no provenance line"]
    out = [] if m.group(1) == source_hash() else [f"stale: the report is from sources {m.group(1)}, these are {source_hash()}"]
    if rerun and not out:
        fresh, _ = report(int(m.group(2)))
        if fresh != saved: out.append("the report doesn't reproduce at its own configuration")
    return out

if __name__ == "__main__":
    if "--check" in sys.argv:
        bad = check("--rerun" in sys.argv); print("\n".join(bad) or "the saved report matches these sources"
                                                    + (" and reproduces" if "--rerun" in sys.argv else ""))
        sys.exit(1 if bad else 0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    out, fit = report(n)
    open(REPORT, "w").write(out)
    print(out)
