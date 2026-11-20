"""Side-by-side stat blocks for the Djur and the Oskorei at a given level, measured against an average hero."""
import random, sys
from engine import *

L = int(sys.argv[1]) if len(sys.argv) > 1 else 30
hero_attrs = {k: attr_at(15.5, L) for k in ATTRS}
hero = Unit("Average hero", "party", L, hero_attrs, {"STR": 1.0}, {"INT": 1.0}, {}, [])
b = Battle([hero], [], random.Random(0))
hero_hit = act("damage", "Base hit", element="Slash", tier="Base", power=20)

def block(u):
    single = [a for a in u.actions if a["kind"] == "damage" and not a["all"]]
    alls = [a for a in u.actions if a["kind"] == "damage" and a["all"]]
    best_s = max((b.expected_damage(u, hero, a) for a in single), default=0)
    best_a = max((b.expected_damage(u, hero, a) * 3 for a in alls), default=0)
    threat = best_s * u.actions_per_round
    to_kill = u.maxhp / max(1, b.expected_damage(hero, u, hero_hit))
    weak = ", ".join(k for k, v in u.aff.items() if v == "weak")
    resist = ", ".join(k for k, v in u.aff.items() if v == "resist")
    moves = ", ".join(a["name"] + ("" if not a["cost"] else f" ({a['cost']} MP)") for a in u.actions)
    return (u.name, u.actions_per_round, u.maxhp, u.maxmp, u.ATK, u.MAT, u.DEF, u.MDF, u.attrs["SPD"],
            best_s, best_a, threat, to_kill, weak, resist, moves, u.horn)

rows = []
for r in rank_rows("Djur"):
    rows.append(("Djur", block(spawn_family("Djur", r["name"], L, job=r["job"]))))
for tier in (1, 2, 3, 4):
    seen = set()
    for u in oskorei_encounter(L, random.Random(1), tier):
        key = u.name.split(" ")[0] if u.name.startswith("Jakthund") else u.name
        if key in seen: continue
        seen.add(key); rows.append((f"Hunt T{tier}", block(u)))

print(f"Level {L}. Average hero: HP {hero.maxhp:.0f}, ATK/MAT/DEF/MDF {hero_attrs['STR']:.0f}, SPD {hero_attrs['SPD']:.0f}.")
print("'Single' and 'All' are expected damage per action against that hero (All = total across 3 heroes).")
print("'Threat' = best single-target damage x actions per round. 'Hits' = average hero's base hits to bring it down.\n")
print("| Group | Unit | Acts | HP | ATK | MAT | DEF/MDF | SPD | Single | All | Threat/rnd | Hits | Weak to | Resists | Moves |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for g, r in rows:
    name, acts, hp, mp, atk, mat, df, mdf, spd, s, a, t, k, weak, res, moves, horn = r
    print(f"| {g} | {name}{' (horn)' if horn else ''} | {acts} | {hp:.0f} | {atk:.0f} | {mat:.0f} | {df:.0f}/{mdf:.0f} | {spd:.0f} "
          f"| {s:.0f} | {a:.0f} | {t:.0f} | {k:.1f} | {weak} | {res} | {moves} |")

print("\nFormation totals (vs. a party of 3 average heroes: HP {:.0f}, about {:.0f} damage per round from base hits)".format(
    hero.maxhp * 3, b.expected_damage(hero, hero, hero_hit) * 3))
for tier in (1, 2, 3, 4):
    us = oskorei_encounter(L, random.Random(1), tier)
    hp = sum(u.maxhp for u in us)
    threat = sum(max((b.expected_damage(u, hero, a) for a in u.actions if a["kind"] == "damage" and not a["all"]), default=0)
                 * u.actions_per_round for u in us)
    print(f"  Tier {tier}: {len(us)} units, total HP {hp:.0f}, total threat {threat:.0f} per round "
          f"(party HP lasts about {hero.maxhp*3/threat:.1f} rounds; party needs about {hp/(b.expected_damage(hero, hero, hero_hit)*3):.1f} rounds)")
