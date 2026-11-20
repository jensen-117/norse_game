"""Every move the builders make, as data: save before a refactor of how moves are built, compare after (Wave 2a).
    python3 checks/move_golden.py save checks/moves_golden.json   |   python3 checks/move_golden.py check checks/moves_golden.json"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
import grammar

def everything():
    out = {}
    T = TIERS
    for r in ELEMENT:
        for t in T:
            for al in (False, True): out[f"damage_spell {r} {t} {al}"] = damage_spell(r, t, al)
    for t in T:
        for al in (False, True):
            out[f"heal_spell {t} {al}"] = heal_spell(t, al); out[f"cleanse_spell {t} {al}"] = cleanse_spell(t, al)
            for s in STATUS_ROOT: out[f"status_spell {s} {t} {al}"] = status_spell(s, t, al)
            for st in STAT_ROOT:
                for up in (True, False): out[f"stat_spell {st} {up} {t} {al}"] = stat_spell(st, up, t, al)
        if t != "Halv" or True: out[f"vakna {t}"] = vakna(t)
    for d in MARTIAL:
        out[f"strike {d}"] = strike(d); out[f"strike {d} Bite 16"] = strike(d, "Bite", 16)
        for t in T:
            for al in (False, True):
                out[f"skill {d} {t} {al}"] = skill(d, "X", t, al)
                out[f"skill {d} {t} {al} Bleeding"] = skill(d, "X", t, al, status="Bleeding", power=14)
        out[f"skill {d} pct"] = skill(d, "Berserksgang", "Base", power=32, pct_current=0.25)
    for k in ITEMS: out[f"item {k}"] = item_move(k)
    for a in grammar.words(roots=list(grammar.WEAPON) + ["Eld", "Blixt"]): out["word " + a["name"] + " " + str(a["parts"])] = a
    for r in ("Skar", "Eld", "Vatn"): out[f"word mark {r}"] = grammar.compile_word(r, target="Mark")
    for c in CLASSES:
        for L in (1, 10, 20, 50): out[f"loadout {c} {L}"] = loadout(c, L)
    for fam in FAMILIES:
        for r in rank_rows(fam):
            for i, m in enumerate(r["moves"]):
                mm = tuple("Natt" if x == "@" else x for x in m)
                out[f"family {fam} {r['job']} {i}"] = family_move(mm)
    for el in SPIRIT_KITS:
        for rank, _ in SPIRIT_RANKS: out[f"spirit {rank} {el}"] = spirit_kit(rank, el)
    for el in SPIRIT_KITS:
        for rank, _ in MOGEL_RANKS: out[f"mogel {rank} {el}"] = mogel_kit(rank, el)
    for tier, specs in OSKOREI_TIERS.items():
        for s in specs:
            if s != "hound":
                for i, m in enumerate(s[5]): out[f"oskorei {s[0]} {i}"] = family_move(m)
    return json.loads(json.dumps(out, sort_keys=True, default=lambda o: list(o) if isinstance(o, tuple) else str(o)))

if __name__ == "__main__":
    mode, path = sys.argv[1], sys.argv[2]; now = everything()
    if mode == "save": json.dump(now, open(path, "w"), sort_keys=True); print(f"saved {len(now)} moves and kits"); sys.exit(0)
    was = json.load(open(path)); bad = [k for k in was if was[k] != now.get(k)] + [k for k in now if k not in was]
    if not bad: print(f"identical: {len(now)} moves and kits"); sys.exit(0)
    for k in bad[:5]:
        a, b = was.get(k), now.get(k)
        if isinstance(a, dict) and isinstance(b, dict):
            diff = {x: (a.get(x), b.get(x)) for x in set(a) | set(b) if a.get(x) != b.get(x)}
            print(f"DIFFERS {k}: {diff}")
        else: print(f"DIFFERS {k}: {str(a)[:200]} -> {str(b)[:200]}")
    print(f"{len(bad)} differ"); sys.exit(1)
