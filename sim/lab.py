"""The Fight Lab's bridge (fight_lab_spec.md): the page calls these through Pyodide and gets JSON back.
The page never runs rules; everything here is a thin wrapper over Battle's step API and knowledge.Memory."""
import json, random
import engine
from engine import *
from composer import catalog, habitat, compose, place, spawn, describe, gate, BIOMES, CompositionError, shaped_room, CALIB_SEED, CALIB_PLACES
from knowledge import Memory

CAT = catalog()
S = dict(battle=None, memory=Memory(), know_all=False, seed=1, rng=random.Random(1), party_spec=[], pack_spec=None, record=None)

def _engine_hash():
    import hashlib, os
    h, here = hashlib.sha1(), os.path.dirname(os.path.abspath(__file__))   # next to this file, wherever it's run from
    for f in ("data.py", "words.py", "grammar.py", "brains.py", "engine.py"):
        h.update(open(os.path.join(here, f), "rb").read())                 # a missing source is an error, not an empty stamp
    return h.hexdigest()[:10]
ENGINE = _engine_hash()

def _j(x): return json.dumps(x, default=lambda o: list(o) if isinstance(o, tuple) else str(o))

# ------------------------------------------------------------ the panel's lists
def menus():
    return _j(dict(
        classes=[dict(key=k, kind=v["kind"], school=v.get("school"), dmg=v.get("dmg")) for k, v in CLASSES.items() if k in KITS],   # C15: the new game's
        items=[dict(key=k, name=v["name"], kind=v["kind"], stack=v["stack"]) for k, v in ITEMS.items()],
        habitats=["Barrow", "Wildwood", "Rapids"] + [f"Biome: {b}" for b in BIOMES],
        pouch_slots=POUCH_SLOTS, pilot_rooms=list(PILOT_ROOMS)))

def set_seed(seed):
    S["seed"] = int(seed); S["rng"] = random.Random(S["seed"]); return _j(dict(seed=S["seed"]))

# ------------------------------------------------------------ the party
def hero_card(u):
    halv = next((a for a in u.actions if a.get("basic")), None)
    return dict(name=u.name, cls=u.cls, level=u.level, hp=round(u.maxhp), mp=round(u.maxmp), kit=getattr(u, "kit_leg", None),
                waiting=[n for n, _ in getattr(u, "excluded", [])],
                attrs={k: round(v) for k, v in u.attrs.items()}, sign=u.sign,
                moves=[dict(name=a["name"], kind=a["kind"], element=a.get("element"), cost=a["cost"], cost_type=a["cost_type"],
                            halv=a is halv) for a in u.actions])

def make_party(spec_json):
    """spec: [{cls, level, pouch: [[item, n], ...]}, ...]; cls may be "random". Each hero is born from its own seed,
    so the same spec and seed always give the same people."""
    spec = json.loads(spec_json)
    # a "random" slot rolls a class the way recruits do, fresh on every click and never repeating a class
    # already in the party; then the hero is born from the seed, the same way the fight will build them
    S["rolls"] = S.get("rolls", 0) + 1
    rr = random.Random(f"{S['seed']}:{S['rolls']}")
    taken = {s["cls"] for s in spec if s.get("cls") not in (None, "", "random")}
    for s in spec:
        if s.get("cls") not in (None, "", "random") and s["cls"] not in KITS:
            raise ValueError(f"{s['cls']} isn't a class of the new game (the Lab plays the new game only: review C15)")
    for s in spec:
        if s.get("cls") in (None, "", "random"):        # rolled from the new game's classes, never repeating one
            free = [c for c in KITS if c not in taken]
            c = rr.choice(free or list(KITS)); s["cls"] = c; taken.add(c)
    S["party_spec"] = spec
    party = _party()
    return _j(dict(party=[hero_card(u) for u in party], spec=spec))

def _party():
    """The heroes of the spec. Old records (before the Lab played the new game only) may name an old class: those are
    born the old way, so the record still replays under its own profile."""
    spec = S["party_spec"]; party = []
    for i, s in enumerate(spec):
        r = random.Random(S["seed"] * 101 + i)
        if s["cls"] in KITS:                     # the new game's classes: a fixed sheet and a kit snapshot (Wave 3)
            u = build_hero(s["cls"], int(s.get("kit") or 1), int(s["level"]))
        else: u = birth(s["cls"], int(s["level"]), r)
        u.pouch = [[k, int(n)] for k, n in s.get("pouch", []) if int(n) > 0][:POUCH_SLOTS]
        party.append(u)
    return party

# ------------------------------------------------------------ the pack
def roll_pack(hab, budget, ranged, level, art_only=True):
    rng = S["rng"]
    if hab.startswith("Biome: "): pool = gate(CAT, art_only=bool(art_only), **BIOMES[hab[7:]])
    else: pool = habitat(CAT, hab, art_only=bool(art_only))
    rules = dict(budget=int(budget), ranged=None if ranged in ("", "any", None) else ranged)
    try:
        picks = place(compose(rng, pool, rules))
    except CompositionError as e:
        return _j(dict(error=str(e)))
    S["pack_spec"] = dict(placed=[(r, l, e) for r, l, e in picks], level=int(level))
    return _j(dict(pack=[dict(cell=[r, l], name=describe(e), family=e["family"], rank=e["rank"], job=e.get("job"), element=e["element"],
                              cost=e["cost"], art=e["art"]) for r, l, e in picks]))

def calib_room(kind, budget, add, n):
    """A calibration room (Nov 20): the sweep's room shape and seed, so Claude can play the AI on exactly this room
    (sim/calib_gap.py) and measure the gap. Room n is rolled from Random(CALIB_SEED + n - 1), in the sweep's places in
    turn, at the enemies' level; add: "" (as rolled), "Trash" or "Regular" (two more)."""
    n = max(1, int(n)); rng = random.Random(CALIB_SEED + n - 1); where = CALIB_PLACES[(n - 1) % len(CALIB_PLACES)]
    try:
        picks = shaped_room(rng, CAT, where, kind, int(budget), add or None, mirrored=True)
    except CompositionError as e:
        return _j(dict(error=str(e)))
    S["pack_spec"] = dict(placed=[(r, l, e) for r, l, e in picks], level=ENEMY_LEVEL,
                          calib=dict(kind=kind, budget=int(budget), add=add or None, room=n, where=where))
    return _j(dict(where=where, pack=[dict(cell=[r, l], name=describe(e), family=e["family"], rank=e["rank"], job=e.get("job"),
                                           element=e["element"], cost=e["cost"], art=e["art"]) for r, l, e in picks]))

def pilot_room(name):
    """A Bein room from PILOT_ROOMS (Nov 25), cell by cell; a Beinseidr's element is rolled from the Lab's seed."""
    rng = S["rng"]
    if name not in PILOT_ROOMS: return _j(dict(error=f"No Bein room called {name}."))
    def entry(rank):
        es = [e for e in CAT if e["family"] == "Bein" and e["rank"] == rank]
        return rng.choice(es) if es else None
    picks = [(row, lane, entry(rank)) for row, lane, rank in PILOT_ROOMS[name]]
    if any(e is None for _, _, e in picks): return _j(dict(error="A rank in that room isn't in the catalog."))
    S["pack_spec"] = dict(placed=picks, level=ENEMY_LEVEL, pilot=name)
    return _j(dict(where=name, pack=[dict(cell=[r, l], name=describe(e), family=e["family"], rank=e["rank"], job=e.get("job"),
                                          element=e["element"], cost=e["cost"], art=e["art"]) for r, l, e in picks]))

# ------------------------------------------------------------ a run (Nov 24, Joseph): a gauntlet you play, room by room
# Trash, Regular, Elite, a camp, then the Boss, in one place, carrying HP, MP, the pouch, Wounded and the dead between
# rooms (dive_spec). The adds dial puts two more Trash or Regulars in every fight room but the Regular one, which has its
# own two. Room i of run n is rolled from Random(RUN_SEED + 10n + i). Each room's record carries the party as it walked in.
RUN_STAGES = [("Trash", "fodder", 3, None), ("Regular", "fodder", 3, "Regular"), ("Elite", "elite", 4, None),
              ("Camp", None, 0, None), ("Boss", "boss", 4, None)]
RUN_SEED = 7000

def _carry(u):
    return dict(hp=u.hp, mp=getattr(u, "mp", 0), maxhp=u.maxhp, maxmp=getattr(u, "maxmp", 0), wounded=bool(getattr(u, "wounded", False)),
                unwounded=list(getattr(u, "unwounded", ())) or None, state=u.state, pouch=[list(p) for p in u.pouch])

def apply_carry(u, c):
    """A hero as they walked into a run's room (replay.py rebuilds a run's later rooms with this)."""
    u.hp, u.mp, u.maxhp, u.maxmp, u.wounded, u.state = c["hp"], c["mp"], c["maxhp"], c["maxmp"], c["wounded"], c["state"]
    if c.get("unwounded"): u.unwounded = tuple(c["unwounded"])
    u.pouch = [list(p) for p in c["pouch"]]

def _run_state(extra=None):
    r = S.get("run")
    if not r: return dict(run=None)
    out = dict(run=dict(n=r["n"], add=r["add"], where=r["where"], stages=[s[0] for s in RUN_STAGES], stage=r["stage"],
                        over=r.get("over"), log=r["log"],
                        heroes=[dict(name=u.name, cls=u.cls, hp=round(max(0, u.hp)), maxhp=round(u.maxhp), mp=round(getattr(u, "mp", 0)),
                                     maxmp=round(getattr(u, "maxmp", 0)), wounded=bool(getattr(u, "wounded", False)), state=u.state,
                                     pouch=[list(p) for p in u.pouch]) for u in r["party"]]))
    out.update(extra or {}); return out

def run_start(n, add, where):
    if not S["party_spec"]: return _j(dict(error="Make a party first."))
    S["run"] = dict(n=max(1, int(n)), add=add or None, where=where, stage=0, party=_party(), log=[], fought=False)
    return run_room()

def run_stop(): S["run"] = None; return _j(dict(run=None))

def run_room():
    """The run's current room: a pack ready to fight, or the camp."""
    r = S.get("run")
    if not r or r.get("over"): return _j(_run_state())
    name, kind, budget, own_add = RUN_STAGES[r["stage"]]
    r["fought"] = False
    if kind is None: return _j(_run_state(dict(camp=True)))
    rng = random.Random(RUN_SEED + 10 * r["n"] + r["stage"])
    try:
        picks = shaped_room(rng, CAT, r["where"], kind, budget, own_add or r["add"], mirrored=True)
    except CompositionError as e:
        return _j(dict(error=str(e)))
    S["pack_spec"] = dict(placed=[(x, l, e) for x, l, e in picks], level=ENEMY_LEVEL,
                          run=dict(n=r["n"], add=r["add"], where=r["where"], stage=name))
    return _j(_run_state(dict(room=name, pack=[dict(cell=[x, l], name=describe(e), family=e["family"], rank=e["rank"], job=e.get("job"),
                                                   element=e["element"], cost=e["cost"], art=e["art"]) for x, l, e in picks])))

def run_camp(rest_json):
    """D9: each hero Rests or not (carving waits for the dive); then on to the boss."""
    r = S.get("run")
    if not r or RUN_STAGES[r["stage"]][1] is not None: return _j(dict(error="Not at the camp."))
    for u, yes in zip(r["party"], json.loads(rest_json)):
        if yes and u.state != "dead":
            before = (round(u.hp), round(getattr(u, "mp", 0))); rest(u)
            r["log"].append(f"Camp: {u.name} rests ({before[0]} to {round(u.hp)} HP" + (f", {before[1]} to {round(u.mp)} MP" if getattr(u, "maxmp", 0) else "") + ").")
    r["stage"] += 1
    return run_room()

def run_after():
    """After a run's fight: on to the next room, or the run ends."""
    r, b = S.get("run"), S["battle"]
    if not r or not r.get("fought") or b is None or b.winner is None: return _j(_run_state())
    name = RUN_STAGES[r["stage"]][0]
    r["fought"] = False
    if b.winner == "party":
        r["log"].append(f"{name}: won in {b.round} round{'' if b.round == 1 else 's'}.")
        r["stage"] += 1
        if r["stage"] >= len(RUN_STAGES): r["over"] = "won"
    else:
        r["log"].append(f"{name}: {'fled' if b.winner == 'fled' else 'lost'} in {b.round} round{'' if b.round == 1 else 's'}."); r["over"] = "lost"
    return _j(_run_state())

# ------------------------------------------------------------ a fight
def start(control="party"):
    if not S["party_spec"] or not S["pack_spec"]: return _j(dict(error="Make a party and roll a pack first."))
    bseed = S["rng"].getrandbits(32)          # a whole number: a float seed goes through hash(), which differs on 32-bit Pyodide
    p = S["pack_spec"]
    r = S.get("run") if p.get("run") else None
    if r is not None and not r.get("over"):      # a run's room: the party as it walked in, the dead left behind
        for u in r["party"]: settle(u)
        party = [u for u in r["party"] if u.state != "dead"]; r["fought"] = True
    else: party = _party()
    carry = [_carry(u) for u in r["party"]] if r is not None else None
    b = Battle(party, spawn(p["placed"], p["level"]), random.Random(bseed), events=True, profile="new")
    S["battle"] = b
    import sys
    S["record"] = dict(engine=ENGINE, platform=sys.platform, profile=b.profile, calib=p.get("calib"), run=p.get("run"), carry=carry,
                       lab_seed=S["seed"], bseed=bseed, control=control, party=S["party_spec"],
                       pack=[[r, l, e] for r, l, e in p["placed"]], level=p["level"], orders=[], pending={},
                       winner=None, rounds=0, log=[])
    ev = b.begin(control=None if control == "auto" else "party")
    _log(ev)
    learned = S["memory"].observe(ev)
    return _j(_state(ev, learned))

def _state(ev, learned=()):
    b = S["battle"]
    return dict(events=ev, phase=b.phase, awaiting=b.awaiting(), winner=b.winner, round=b.round, learned=list(learned),
                board=[_board_unit(u) for u in b.units])

def _board_unit(u):
    """What the board shows of every unit (enemy HP as a fraction only: the bar has no numbers)."""
    b = S["battle"]
    d = dict(id=u.uid, name=u.name, side=u.side, cell=list(u.cell) if getattr(u, "cell", None) else None,
             frac=max(0.0, u.hp / u.maxhp) if u.maxhp else 0, state=u.state, alive=u.alive, piled=u in b.piles,
             status=sorted(u.status) + sorted(h["name"] for h in getattr(u, "held", {}).values()),   # holds show as badges (D3)
             held=[dict(name=h["name"], rounds=h["rounds"], harmful=h["harmful"], window=not h.get("lock", True)) for h in getattr(u, "held", {}).values()], family=getattr(u, "family", None), cls=u.cls, element=getattr(u, "element", None),
             rank=getattr(u, "mogel_rank", None) or getattr(u, "rank_name", None) or getattr(u, "rank", None),
             job=getattr(u, "job", None), winding=b.shown(u, u.bide[0]) if u.bide else None, intent=b.intents.get(u.uid),
             knots=getattr(u, "knots", 0), song=(u.status.get("Song") or {}).get("stacks", 0),   # the Song's verses (Nov 21)
             counters=[u.counter_name(s) for s in ("ATK", "DEF", "EVA", "ACC", "SPD") if u.counter_name(s)])   # Mighty 1, Evasive 3
    if u.side == "party":
        d.update(hp=round(max(0, u.hp)), maxhp=round(u.maxhp), mp=round(u.mp), maxmp=round(u.maxmp),
                 breaths=u.breaths, wounded=u.wounded)
    return d

def options(uid): return _j(S["battle"].options(uid))

def submit(uid, key, target_json="null"):
    try:
        t = json.loads(target_json)
        S["battle"].submit(uid, key, t)
        S["record"]["pending"][uid] = [key, t]
        return _j(dict(ok=True))
    except (ValueError, KeyError, IndexError) as e:
        return _j(dict(ok=False, error=str(e)))

def autofill():
    """Fight with missing orders: every hero without one Halv-strikes, or, with no Halv (a full kit, Nov 21), uses
    their simplest attack: the cheapest damaging move they can afford that isn't a last swing; with none, Guards.
    Targets are random but spread: each pick skips
    foes already picked this round, and the chain starts over once every foe is taken. Living foes before bone piles.
    No hidden information is used. Picks go through submit, so the record replays them exactly."""
    b = S["battle"]; pend = S["record"]["pending"]
    slot = {u.uid: i for i, u in enumerate(b.units)}
    missing = sorted((uid for uid in b.awaiting() if uid not in pend), key=lambda uid: slot.get(uid, 99))
    rng = random.Random(S["record"]["bseed"] * 1009 + b.round * 7 + (b.phase == "bonus"))
    def alive(t):
        try: return b.unit(t).alive
        except (KeyError, ValueError, AttributeError): return False
    taken, out = [], []
    for uid in missing:
        o = b.options(uid)
        h = o["halv"] or min((m for m in o["moves"] if m["kind"] == "damage" and m["afford"] and not m.get("drops")
                              and (m["aim"] in ("self", "all") or m["targets"])), key=lambda m: m["cost"], default=None)
        if h and h["afford"] and (h["aim"] in ("self", "all") or h["targets"]):
            t = None
            if h["aim"] not in ("self", "all"):
                live = [x for x in h["targets"] if alive(x)] or list(h["targets"])
                pool = [x for x in live if x not in taken]
                if not pool: taken.clear(); pool = live
                t = rng.choice(pool); taken.append(t)
            r = json.loads(submit(uid, h["key"], json.dumps(t)))
            if r.get("ok"): out.append(dict(id=uid, key=h["key"], target=t, shown=h["shown"])); continue
        submit(uid, "guard", "null"); out.append(dict(id=uid, key="guard", target=None, shown="Guard", fallback=True))
    return _j(out)

def preview(): return _j(S["battle"].preview_order())

def retract(uid):
    S["battle"].retract(uid); S["record"]["pending"].pop(uid, None); return _j(dict(ok=True))

def commit():
    b = S["battle"]
    rec = S["record"]
    try:
        ev = b.commit()
    except ValueError as e:
        return _j(dict(error=str(e)))
    rec["orders"].append(rec["pending"]); rec["pending"] = {}
    rec["winner"], rec["rounds"] = b.winner, b.round
    _log(ev)
    learned = S["memory"].observe(ev)
    return _j(_state(ev, learned))

def inspect(uid):
    return _j(S["memory"].mask(S["battle"].inspect(uid), S["know_all"]))

# ------------------------------------------------------------ what the Company remembers
def set_know_all(on): S["know_all"] = bool(on); return _j(dict(know_all=S["know_all"]))
def memory_save(): return S["memory"].to_json()
def memory_load(s): S["memory"] = Memory.from_json(s); return _j(dict(entries=len(S["memory"].seen)))
def memory_reset(): S["memory"] = Memory(); return _j(dict(ok=True))
def bestiary(): return _j(S["memory"].entries())

# ------------------------------------------------------------ the fight recorder (Claude replays these: replay.py)
def _log(ev):
    for e in ev:
        if e["kind"] == "round": S["record"]["log"].append(f"-- Round {e['n']}")
        elif e["kind"] == "intent":
            S["record"]["log"].append(f"   [{e['side'][0]}] {e['unit']} intends {e['shown']}" + (f" -> {e['target']}" if e.get("target") else "")
                                      + (f" ({e['why']})" if e.get("why") else ""))
        elif e.get("text"): S["record"]["log"].append(e["text"])

def record():
    """The fight so far, small enough for one database document: replay it from the seed and the orders."""
    r = dict(S["record"] or {})
    if not r: return _j(None)
    r.pop("pending", None)
    log = r["log"]; size = 0; keep = []
    for line in reversed(log):                   # keep the end of a very long fight
        size += len(line) + 4
        if size > 150_000: keep.append("... (earlier lines cut)"); break
        keep.append(line)
    r["log"] = list(reversed(keep))
    return _j(r)
