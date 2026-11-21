"""The yardstick (Nov 21, Joseph): the level-50 soft-launch sheet, and how far today's heroes and foes sit from it.

    python3 yardstick.py            # markdown: hero pools, every hero damage move's hits-to-kill, every foe against its tier

The measure is the Vasara's Krosh: a clean hit on a plain foe is about 104. Foe HP is set by how many hammer blows it
takes (Trash 2, and 1 with one ATK stage; Regular 4-5; Elite 9-10; Boss about 5 rounds of the whole party). The other
side: a foe's normal hit takes 10-12% of a mid hero's HP, a wind-up 30-40%.

The yardstick foe is plain on purpose: no affinities, no body quirks, DEF and MDF equal (CON = WIS = 60, where a clean
Krosh is ~104), the other attributes average. Martial and magic moves meet the same guard, so they compare on their own
merits; a family's real defenses (the Ande's high MDF, the Beinar's high DEF) are its deviation from the yardstick.
The heroes' side was applied in the hero pass (Nov 21); the foes' side is still a target (the enemy pass)."""
import math, random
from engine import *
from composer import catalog, spawn, tier_of

LEVEL = 50
POOLS = HERO_POOLS              # applied in the hero pass (Nov 21): martial MP is 0
TIERS = {"Trash": 130, "Regular": 450, "Elite": 950, "Boss": 1700}
HITS = {"Trash": "2 (1 with a stage)", "Regular": "4-5", "Elite": "9-10", "Boss": "~5 party rounds"}
FOE_HIT = (0.10, 0.12)          # a foe's normal hit, as a share of a mid hero's HP
FOE_WINDUP = (0.30, 0.40)       # a wind-up's
MID_HP = 600

def plain_foe(hp, level=LEVEL):
    """The yardstick foe: a real foe's frame with plain numbers (no affinities, no body, CON = WIS = 60)."""
    e = next(x for x in catalog() if tier_of(x) == "Regular")
    u = spawn([("front", 0, e)], level)[0]
    u.name, u.aff, u.body = "Yardstick", {}, {}
    u.attrs = {k: 62 for k in u.attrs}; u.attrs.update(CON=60, WIS=60)
    u.maxhp = u.hp = hp
    return u

def hits(hp, dmg): return math.ceil(hp / dmg) if dmg > 0 else None

def hero_rows():
    out = []
    for leg in (1, 3):
        for c in KITS:
            h = build_hero(c, leg, LEVEL)
            f = plain_foe(TIERS["Trash"])
            b = Battle([h], [f], random.Random(1), profile="new")
            for a in h.actions:
                if a["kind"] != "damage" or not a.get("element"): continue
                n = a.get("hits") or ELEMENT[a["element"]]["hits"]
                clean = b.raw_damage(h, f, a) * n
                stat = "ATK" if a["element"] in MARTIAL else "MAT"
                h.stages[stat] = 1; up = b.raw_damage(h, f, a) * n; h.stages[stat] = 0
                reach = "All" if a["all"] else (a.get("shape") or "one")
                out.append((c, leg, a["name"], reach, f"{a['cost']} {a['cost_type']}", clean, up))
    return out

def foe_rows():
    """Every catalogued foe at the enemies' level: its HP against its tier's target, and its hits on the mid hero."""
    mid = build_hero("Ullar", 1, LEVEL)
    rows, seen = [], set()
    for e in catalog():
        try: u = spawn([("front", 0, e)], ENEMY_LEVEL)[0]
        except Exception: continue
        if u.name in seen: continue
        seen.add(u.name)
        b = Battle([mid], [u], random.Random(1), profile="new")
        normal = [b.raw_damage(u, mid, a) * (a.get("hits") or ELEMENT[a["element"]]["hits"])
                  for a in u.actions if a["kind"] == "damage" and a.get("element") and not a.get("bide")]
        rows.append((tier_of(e), u.name, u.maxhp, max(normal) / mid.maxhp if normal else None))
    return sorted(rows, key=lambda r: (list(TIERS).index(r[0]), r[1]))

def report():
    pct = lambda x: "-" if x is None else f"{x:.0%}"
    L = [f"# The yardstick (level {LEVEL} soft launch)", "",
         "Heroes: as applied (Nov 21). Foes: targets. A hit count is clean hits (no graze, no crit) on the plain foe; a graze halves a hit, a crit is x1.5.", "",
         "## Hero pools", "", "| Class | HP now | HP target | MP now | MP target |", "|---|---|---|---|---|"]
    for c, (hp, mp) in POOLS.items():
        h = build_hero(c, 1, LEVEL)
        L.append(f"| {c} | {round(h.maxhp)} | {hp} | {round(h.maxmp)} | {mp} |")
    L += ["", "## Foe HP by tier", "", "| Tier | HP | Krosh hits |", "|---|---|---|"]
    L += [f"| {t} | {hp} | {HITS[t]} |" for t, hp in TIERS.items()]
    L += ["", f"Foe hits: a normal hit {FOE_HIT[0]:.0%}-{FOE_HIT[1]:.0%} of a mid hero ({MID_HP} HP: "
          f"{MID_HP * FOE_HIT[0]:.0f}-{MID_HP * FOE_HIT[1]:.0f}), a wind-up {FOE_WINDUP[0]:.0%}-{FOE_WINDUP[1]:.0%} "
          f"({MID_HP * FOE_WINDUP[0]:.0f}-{MID_HP * FOE_WINDUP[1]:.0f}).", "",
          "## Hero damage moves on the plain foe", "",
          "Per target. Hits to kill each tier, clean; then Trash with one ATK/MAT stage (the target is 1).", "",
          "| Class | Leg | Move | Reach | Cost | Clean hit | vs Krosh | Trash | Regular | Elite | Boss | Trash, +1 stage |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    rows = hero_rows()
    krosh = next(r[5] for r in rows if r[2] == "Krosh")
    for c, leg, name, reach, cost, clean, up in rows:
        L.append(f"| {c} | {leg} | {name} | {reach} | {cost} | {clean:.0f} | {clean / krosh:.2f} | "
                 + " | ".join(str(hits(hp, clean)) for hp in TIERS.values()) + f" | {hits(TIERS['Trash'], up)} |")
    L += ["", "## Today's foes against their tier", "",
          f"HP against the tier's target; the best damage move on Ullar ({MID_HP}-HP class, his own affinities aside), as "
          f"a share of his HP (target {FOE_HIT[0]:.0%}-{FOE_HIT[1]:.0%}). No catalogued foe lists a wind-up move, so "
          f"wind-ups are measured in the enemy pass.", "",
          "| Tier | Foe | HP | x target | Best hit |", "|---|---|---|---|---|"]
    for t, name, hp, n in foe_rows():
        L.append(f"| {t} | {name} | {hp:.0f} | {hp / TIERS[t]:.1f} | {pct(n)} |")
    return "\n".join(L)

if __name__ == "__main__":
    print(report())
