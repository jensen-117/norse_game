"""Generate the move catalog (for the spellbook) and stat blocks (for the bestiary) straight from the data."""
import random
from engine import *

def enemy_moves():
    rows = {}
    def add(m, who):
        if m[0] != "strike": return
        if isinstance(m[-1], dict): m = m[:-1]                 # a row's options (Twin Slash's hits, Skewer's shape)
        all_ = len(m) > 4 and m[4]; status = m[5] if len(m) > 5 else None
        key = (m[2], m[1], m[3], all_, status)
        rows.setdefault(key, set()).add(who)
    for fam, f in FAMILIES.items():
        for r in rank_rows(fam):
            for m in r["moves"]: add(m, r["name"] if r["job"] == r["name"] else f'{r["name"]} ({r["job"]})')
    for tier, units in OSKOREI_TIERS.items():
        for spec in units:
            if spec == "hound": continue
            for m in spec[5]: add(m, spec[0])
    out = ["| Move | Type | Tier | Power | Targets | Extra | Used by |", "|---|---|---|---|---|---|---|"]
    for (name, typ, tier, all_, status), who in sorted(rows.items(), key=lambda kv: (kv[0][1], TIERS.index(kv[0][2]), kv[0][0])):
        power = TIER_POWER[tier] * (0.7 if status else 1.0) * (ALL_POWER_MULT if all_ else 1.0)
        out.append(f"| {name} | {typ} | {tier} | {power:.0f}{' each' if all_ else ''} | {'All' if all_ else 'Single'} "
                   f"| {('Can inflict ' + status) if status else ''} | {', '.join(sorted(who))} |")
    return "\n".join(out)

def stat_blocks(level=30):
    hero_attrs = {k: attr_at(15.5, level) for k in ATTRS}
    hero = Unit("hero", "party", level, hero_attrs, {"STR": 1.0}, {"INT": 1.0}, {}, [])
    b = Battle([hero], [], random.Random(0))
    hit = act("damage", "Base hit", element="Slash", tier="Base", power=20)
    def row(u, label=None):
        single = [a for a in u.actions if a["kind"] == "damage" and not a["all"]]
        alls = [a for a in u.actions if a["kind"] == "damage" and a["all"]]
        s = max((b.expected_damage(u, hero, a) for a in single), default=0)
        al = max((b.expected_damage(u, hero, a) * 3 for a in alls), default=0)
        hero_hit = act("damage", "Base hit", element="Crush", tier="Base", power=20)
        hits = u.maxhp / max(1, b.expected_damage(hero, u, {**hero_hit, "element": "Crush"}) / max(0.01, {"weak": 1.5, "resist": 0.5}.get(u.affinity("Crush"), 1.0)))
        return (f"| {label or u.name} | {u.actions_per_round} | {u.maxhp:.0f} | {u.MAT if u.ATK < u.MAT else u.ATK:.0f} "
                f"| {u.DEF:.0f} / {u.MDF:.0f} | {u.attrs['SPD']:.0f} | {s:.0f} | {al:.0f} | {s * u.actions_per_round:.0f} | {hits:.1f} |")
    head = ("| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |\n"
            "|---|---|---|---|---|---|---|---|---|---|")
    out = [f"Level {level}. The average hero has {hero.maxhp:.0f} HP, 44 in every attribute, and deals about "
           f"{b.expected_damage(hero, hero, hit):.0f} per base hit. Damage columns are expected damage against that hero. "
           "\"Hits to down\" ignores affinities.\n"]
    out.append("**Ande** (Eld shown; every element has the same numbers with its own moves)\n\n" + head)
    for rank, _ in SPIRIT_RANKS: out.append(row(spawn_spirit(rank, "Eld", level)))
    for fam in ("Draugr", "Bein", "Drattr", "Djur"):
        out.append(f"\n**{fam}**\n\n" + head)
        for r in rank_rows(fam):
            out.append(row(spawn_family(fam, r["name"], level, job=r["job"]),
                           None if r["job"] == r["name"] else f'{r["name"]} ({r["job"]})'))
    out.append("\n**Oskorei**\n\n" + head)
    for tier in (1, 2, 3, 4):
        seen = set()
        for u in oskorei_encounter(level, random.Random(1), tier):
            k = "Jakthund" if u.name.startswith("Jakthund") else u.name
            if k in seen: continue
            seen.add(k); out.append(row(u, f"T{tier} {k}"))
    return "\n".join(out)

if __name__ == "__main__":
    open("catalog_moves.md", "w").write(enemy_moves())
    open("catalog_stats.md", "w").write(stat_blocks())
    print(enemy_moves()); print(); print(stat_blocks())
