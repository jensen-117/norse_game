"""The foes' brains (step 3 of the Beinar pilot, Nov 25; beinar_pilot.md Part 2, sections 1-3 and 7).

Two layers, both data (data.py: PLAN_*, HEADS, BRAINS):
- **A plan** for every new-game pack: its head (the boss, else its most expensive unit) picks one in round 1, weighted
  by family; it names a focus and a stance, re-plans by its rules, and every switch is said out loud.
- **Unit rules** for the jobs that have them (the Bein): first fit wins. When none fits, the unit falls back to the
  shared scorer, which weighs the plan's focus (FOCUS_BONUS). Every pick and every fallback is counted (Battle.brain_stats).

The engine calls three things: plan_round (each round's start), pick (a foe's declaration) and focus_of (the scorer).
"""
from data import (PLAN_WEIGHTS, PLAN_HOLDS, FOCUS_BONUS, PLAN_ROUNDS, STABILIZE_ROUNDS, HUNT_HURT, STABILIZE_HURT,
                  UNIT_DESPERATE, HEADS, PLAN_LINES, DESPERATE_LINES, HEAD_FELL_LINE, BRAINS, BRAIN_DESPERATE,
                  DEFAULT_WANT, STAT_NAMES, COMBINED_STAT, enemy_tier)

HEALS = ("heal", "song", "revive")

# ---------------------------------------------------------------- reading the board
def up(x): return x.alive and getattr(x, "state", "up") == "up"     # the Dying are skipped: finishing blows have their own rule
def frac(x): return max(0.0, x.hp) / x.maxhp if x.maxhp else 0.0
def front(x): return getattr(x, "cell", ("front",))[0] == "front"
def job_of(u):
    """A Bein rank's job: Halvbeinorv and Storbeinorv are Beinorv."""
    n = getattr(u, "rank_name", None) or ""
    for p in ("Halv", "Stor"):
        if n.startswith(p): n = n[len(p):].capitalize()
    return n if n in BRAINS else None

def heroes(b): return [x for x in b.party if up(x)]
def pack_units(b): return list(b.enemies)

def reachable(b, side_units, x):
    """Can anyone in the pack strike x where it stands?"""
    return any(x in b.legal(u, a) for u in side_units if u.alive for a in u.actions if a["kind"] == "damage")

def lowest(b, xs, key):
    """The lowest by key, a coin flip on ties."""
    if not xs: return None
    best = min(key(x) for x in xs)
    ties = [x for x in xs if abs(key(x) - best) < 1e-9]
    return ties[0] if len(ties) == 1 else b.rng.choice(ties)

def healer(x): return any(a["kind"] in HEALS for a in x.actions)
def coverer(b, x): return getattr(x, "covered_round", None) == b.round - 1 or any(a["kind"] in ("cover", "taunt") for a in x.actions)
def mp_spend(x): return sum(a["cost"] for a in x.actions if a["cost_type"] == "MP")

def priority_target(b):
    """Joseph's rule, the Bein's out-think: 1. anyone reachable at or under 60%, lowest first; 2. a healer; 3. the
    coverer (who Covered last round, or carries Cover or Taunt); 4. the lowest HP."""
    pool = [x for x in heroes(b) if reachable(b, pack_units(b), x)] or heroes(b)
    hurt = [x for x in pool if frac(x) <= HUNT_HURT]
    if hurt: return lowest(b, hurt, frac)
    for test in (healer, lambda x: coverer(b, x)):
        xs = [x for x in pool if test(x)]
        if xs: return lowest(b, xs, lambda x: x.hp)
    return lowest(b, pool, lambda x: x.hp)

def debuffs(x):
    """How many things are wrong with x: harmful statuses, and stats pushed down."""
    from data import HELPFUL_STATUSES
    return sum(1 for s in x.status if s not in HELPFUL_STATUSES) + sum(1 for st, v in x.stages.items() if v < 0)

# ---------------------------------------------------------------- the plan
TIER_RANK = {"Trash": 0, "Regular": 1, "Elite": 2, "Boss": 3}

def head_of(b):
    alive = [u for u in pack_units(b) if u.alive]
    if not alive: return None
    boss = [u for u in alive if enemy_tier(u) == "Boss"]
    return (boss or sorted(alive, key=lambda u: -getattr(u, "cost", 1)))[0]

def outranks(b, head):
    """A true head: a boss, or of a higher tier than every other unit in the pack. Only its fall breaks the order;
    in a pack of peers the next steps up (Nov 25: the first measure had every Regular room Desperate from round 2)."""
    others = [u for u in pack_units(b) if u is not head]
    return enemy_tier(head) == "Boss" or all(TIER_RANK[enemy_tier(head)] > TIER_RANK[enemy_tier(u)] for u in others)

def legal_plans(b):
    us = [u for u in pack_units(b) if u.alive]
    moves = [(u, a) for u in us for a in u.actions]
    out = ["Break"]                                                       # the fallback: always legal
    rear = [x for x in heroes(b) if not front(x)]
    if not rear or any(reachable(b, us, x) for x in rear): out.append("Hunt")
    if sum(1 for u, a in moves if a["kind"] == "status" or (a["kind"] == "stat" and a["direction"] < 0)) >= 2: out.append("Inflict")
    heals = any(a["kind"] in ("heal", "revive", "cleanse") for u, a in moves)
    if heals or sum(1 for u, a in moves if a["kind"] == "cover" or (a["kind"] == "stat" and a["direction"] > 0)) >= 2:
        out.append("Stabilize")
    return out

def roll(b, family, among):
    w = PLAN_WEIGHTS.get(family) or PLAN_WEIGHTS[None]
    opts = [(p, w.get(p, 0)) for p in among if w.get(p, 0) > 0] or [("Break", 1)]
    r = b.rng.random() * sum(x for _, x in opts)
    for p, x in opts:
        r -= x
        if r <= 0: return p
    return opts[-1][0]

def focus_for(b, plan, pk):
    hs = heroes(b)
    if not hs: return None
    if plan in ("Hunt", "Inflict"): return priority_target(b)
    if plan == "Break":
        fr = [x for x in hs if front(x)] or hs
        return lowest(b, fr, lambda x: x.hp)                              # the line's weakest link
    if plan == "Desperate": return lowest(b, hs, frac)                    # the most hurt
    f = pk.get("focus")
    return f if f is not None and up(f) else priority_target(b)          # Stabilize keeps its focus

def say(b, pk, line, **kw):
    head = pk.get("head")
    text = line.format(head=head.name if head else "The pack", **kw)
    b.emit("plan", "  " + text, plan=pk["plan"], focus=pk["focus"].name if pk.get("focus") else None,
           focus_id=pk["focus"].uid if pk.get("focus") else None, head=head.name if head else None)

def announce(b, pk):
    f = pk.get("focus"); head = pk.get("head")
    tmpl = HEADS.get(getattr(head, "rank_name", None), {}).get("says") if head is not None and head.alive else None
    if tmpl and f is not None and pk["plan"] not in ("Desperate", "Stabilize"):
        say(b, pk, tmpl + f" ({pk['plan']})", focus=f.name)
    else:
        say(b, pk, PLAN_LINES[pk["plan"]], focus=f.name if f else "you")

def switch(b, pk, plan, chosen=True, said=True):
    if plan == "Stabilize": pk["before"] = pk["plan"]
    pk.update(plan=plan, since=b.round, focus=focus_for(b, plan, pk))
    if chosen: pk["switched"] = b.round
    b.brain_stats[("plan", plan)] += 1
    if said: announce(b, pk)

def plan_round(b):
    """Each round's start (not Bonus Rounds): pick, keep, or change the pack's plan, and keep its focus standing."""
    if not hasattr(b, "pack_plan") or b.pack_plan is None:
        head = head_of(b)
        if head is None: return
        pk = b.pack_plan = dict(head=head, family=getattr(head, "family", None), plan=None, focus=None, since=1, switched=1,
                                cost=sum(getattr(u, "cost", 1) for u in pack_units(b)), before=None, true_head=outranks(b, head))
        switch(b, pk, roll(b, pk["family"], legal_plans(b)), chosen=False)
        return
    pk = b.pack_plan
    if pk["plan"] == "Desperate":
        if pk["focus"] is None or not up(pk["focus"]): pk["focus"] = focus_for(b, "Desperate", pk)
        return
    head = pk["head"]
    lost = sum(getattr(u, "cost", 1) for u in pack_units(b) if not u.alive)
    if head is not None and not head.alive and not pk["true_head"]:      # a peer fell: the next steps up, quietly
        pk["head"] = head = head_of(b)
        if head is None: return
    if head is not None and not head.alive:                              # kill the head and the order breaks
        say(b, pk, HEAD_FELL_LINE)
        switch(b, pk, "Desperate", chosen=False, said=False)
        fam = DESPERATE_LINES.get(pk["family"])
        if fam: say(b, pk, fam)
        pk["head"] = None
        return
    if lost * 2 >= pk["cost"]:
        switch(b, pk, "Desperate", chosen=False); return
    wait = HEADS.get(getattr(head, "rank_name", None), {}).get("replan", 2)
    free = b.round - pk["switched"] >= wait
    f, plan, held = pk["focus"], pk["plan"], b.round - pk["since"]
    gone = f is None or not up(f)
    if plan == "Stabilize":
        if held >= STABILIZE_ROUNDS: switch(b, pk, pk.get("before") or "Break", chosen=False)
        return
    us = [u for u in pack_units(b) if u.alive]
    keys = [head] + [u for u in us if any(a["cost_type"] == "MP" or a["kind"] == "status" for a in u.actions)]
    if free and "Stabilize" in legal_plans(b) and any(frac(u) < STABILIZE_HURT for u in keys if u.alive) \
            and sum(map(frac, heroes(b))) / max(1, len(heroes(b))) > sum(map(frac, us)) / max(1, len(us)):
        switch(b, pk, "Stabilize"); return
    if plan == "Break" and gone:
        switch(b, pk, "Hunt", chosen=False); return
    if plan == "Hunt":
        if gone:
            pk["focus"] = focus_for(b, "Hunt", pk)
            if pk["focus"] is not None: say(b, pk, PLAN_LINES["refocus"], focus=pk["focus"].name)
            return
        if free and held >= PLAN_ROUNDS and frac(f) > HUNT_HURT:            # they're protecting it: think again
            switch(b, pk, roll(b, pk["family"], [p for p in legal_plans(b) if p not in ("Hunt", "Stabilize")])); return
    if plan == "Inflict":
        if gone: pk["focus"] = focus_for(b, "Inflict", pk)
        elif free and (debuffs(f) >= 2 or held >= PLAN_ROUNDS):
            switch(b, pk, roll(b, pk["family"], [p for p in ("Hunt", "Break") if p in legal_plans(b)])); return

def focus_of(b, u):
    """The plan's focus for u's side (only the foes plan)."""
    pk = getattr(b, "pack_plan", None)
    if pk is None or u.side != "enemy": return None
    f = pk.get("focus")
    return f if f is not None and up(f) else None

def holds(b):
    pk = getattr(b, "pack_plan", None)
    return pk is not None and pk["plan"] in PLAN_HOLDS

# ---------------------------------------------------------------- the units' rules
def target(b, u, how, focus):
    hs = heroes(b)
    if how == "self": return u
    if how == "focus": return focus
    if how == "most_hurt": return focus if focus is not None and b.pack_plan and b.pack_plan["plan"] == "Desperate" else lowest(b, hs, frac)
    if how == "killable":
        k = [x for x in hs if any(x in b.legal(u, a) and b.expected_damage(u, x, a) >= x.hp
                                  for a in u.actions if a["kind"] == "damage" and not a.get("bide"))]
        return lowest(b, k, lambda x: x.hp)
    if how == "caster":
        cs = [x for x in hs if mp_spend(x) > 0]
        return max(cs, key=mp_spend) if cs else None
    if how == "toughest":
        fr = [x for x in hs if front(x)] or hs
        return max(fr, key=lambda x: x.hp) if fr else None
    if how == "cursed_hurt":
        cursed = [x for x in hs if x.stage("DEF") < 0 and "Poisoned" in x.status]
        return lowest(b, cursed, frac) if cursed else focus
    if how == "ward":                                    # a Beinseidr or the head, likely to be struck and not covered
        head = (b.pack_plan or {}).get("head")
        ws = [x for x in b.allies(u) if x is not u and up(x) and x.covered_by is None
              and (job_of(x) == "Beinseidr" or x is head)
              and (getattr(x, "struck", None) == b.round - 1 or frac(x) < 0.5)]
        return lowest(b, ws, frac)
    raise ValueError(f"unknown brain target {how}")

def move_for(b, u, spec, t):
    """The move a rule names, if u carries one that can be aimed at t."""
    def aimable(a):
        if not u.can_afford(a) or (u.silenced and a["cost_type"] == "MP" and a["cost"] > 0): return False
        return a["all"] or a["target"] == "self" or t in b.legal(u, a)
    acts = u.actions
    if spec == "best_strike":
        ds = [a for a in acts if a["kind"] == "damage" and not a.get("bide") and aimable(a)]
        return max(ds, key=lambda a: b.expected_damage(u, t, a)) if ds else None
    if spec == "quiver": cands = [a for a in acts if a["kind"] == "damage" and a.get("status") in ("Bleeding", "Poisoned")]
    elif spec == "bide": cands = [a for a in acts if a["kind"] == "damage" and a.get("bide")]
    elif spec == "cover": cands = [a for a in acts if a["kind"] == "cover"]
    elif spec.startswith("status:"): cands = [a for a in acts if a["kind"] == "status" and a.get("status") == spec[7:]]
    elif spec.startswith("pays:"): cands = [a for a in acts if a.get("pays_on") == spec[5:]]
    else: cands = [a for a in acts if a["name"] == spec]
    cands = [a for a in cands if aimable(a)]
    return cands[0] if cands else None

def fits(b, u, cond, t, rule, a):
    if cond == "holds": return holds(b)
    if cond == "front": return front(u)
    if cond == "not_last": return u.picks.get(a["name"]) != b.round - 1
    if cond.startswith("below_want:"):
        st = cond.split(":")[1]
        return t.stage(st) < (getattr(u, "wants", None) or {}).get(STAT_NAMES[st][1], DEFAULT_WANT)
    if cond.startswith("lacks:"):
        s = cond[6:]
        return s not in t.status and not b.capped(t, s)
    if cond.startswith("has:"): return cond[4:] in t.status
    if cond == "unsundered": return t.stage("DEF") >= 0       # D11: never on a hero already Sundered (Joseph, Nov 24)
    if cond == "unfed":
        s = a.get("status")
        return s is not None and not b.capped(t, s)
    if cond == "rally_ready":
        stat = COMBINED_STAT.get(a["stat"], a["stat"])
        if any(x.held.get(stat, {}).get("name") == a["name"] for x in b.allies(u)): return False
        closed = b.rested.get((u.side, a["name"]))
        if closed is not None and b.round - closed < a.get("ai_rest", 0): return False
        lifters = [x for x in b.allies(u) if any(m["kind"] == "damage" for m in x.actions)]
        return sum(1 for x in lifters if x.stage(stat) < 1) >= max(1, len(lifters) // 2 + 1)
    if cond == "row_crowded":
        row = getattr(t, "cell", ("front",))[0]
        return sum(1 for x in heroes(b) if getattr(x, "cell", ("front",))[0] == row) >= 2
    raise ValueError(f"unknown brain condition {cond}")

def pick(b, u):
    """A foe's choice by its brain, or None (it falls back to the scorer). Records the claim and the reason."""
    job = job_of(u) if getattr(u, "family", None) == "Bein" else None
    if job is None: return None
    focus = focus_of(b, u)
    pk = getattr(b, "pack_plan", None)
    if pk is not None and pk["plan"] == "Desperate" and pk["family"] == "Bein": rules, tag = BRAIN_DESPERATE, "desperate"
    elif front(u) and frac(u) <= UNIT_DESPERATE: rules, tag = [dict(BRAIN_DESPERATE[0], on="focus")], "desperate"
    else: rules, tag = BRAINS[job], None
    for i, r in enumerate(rules):
        t = target(b, u, r["on"], focus) if r["on"] != "focus" or focus is not None else None
        if r["on"] == "focus" and t is None and tag: t = target(b, u, "most_hurt", None)
        if t is None: continue
        a = move_for(b, u, r["move"], t)
        if a is None: continue
        if not all(fits(b, u, c, t, r, a) for c in r.get("when", ())): continue
        key = None
        if r.get("claim"):
            key = (r["claim"], a.get("status") if r["claim"] == "feed" else None, t.uid)
            if key in b.brain_claims: continue
            b.brain_claims.add(key)
        u.picks[a["name"]] = b.round
        b.brain_stats[(job, tag or f'{r["move"]} on {r["on"]}')] += 1
        u.brain_why = ("brain" if tag is None else tag, r["say"].format(t=t.name if t is not u else "itself", status=a.get("status") or ""))
        return a, (u if a["all"] and a["target"] != "self" and r["on"] == "self" else t)
    b.brain_stats[(job, "fallback")] += 1
    return None
