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
    for f in ("data.py", "words.py", "grammar.py", "engine.py"):
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
        pouch_slots=POUCH_SLOTS))

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

# ------------------------------------------------------------ a fight
def start(control="party"):
    if not S["party_spec"] or not S["pack_spec"]: return _j(dict(error="Make a party and roll a pack first."))
    bseed = S["rng"].getrandbits(32)          # a whole number: a float seed goes through hash(), which differs on 32-bit Pyodide
    p = S["pack_spec"]
    b = Battle(_party(), spawn(p["placed"], p["level"]), random.Random(bseed), events=True, profile="new")
    S["battle"] = b
    import sys
    S["record"] = dict(engine=ENGINE, platform=sys.platform, profile=b.profile, calib=p.get("calib"), lab_seed=S["seed"], bseed=bseed, control=control, party=S["party_spec"],
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
             status=sorted(u.status), family=getattr(u, "family", None), cls=u.cls, element=getattr(u, "element", None),
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
