"""Roll recruits -- genes, Personality, Star Sign, then a weighted-random class."""
import random, statistics as st
from collections import Counter
from data import ATTRS, CLASSES, HP_MULT, CLASS_TILT, PERSONALITY_MULT, FIT_EXPONENT
from engine import roll_normal, roll_class, is_natural_fit, natural_attrs, class_fit

def line(a, level):
    hp = HP_MULT * (20 + 2 * a["CON"] + 2 * level); mp = 10 + a["WIS"] + level
    return "  ".join(f"{k} {a[k]:3.0f}" for k in ATTRS) + f"   HP {hp:4.0f} MP {mp:3.0f}"

def show(n, cls):
    genes = " ".join(f"{n['genes'][k]:2d}" for k in ATTRS)
    s = n["sign"]; b, c = n["personality"]
    best = sorted(class_fit(n).items(), key=lambda kv: -kv[1])[0][0]
    tag = "natural fit" if is_natural_fit(n, cls) else f"odd birth (body suits {best})"
    out = [f"  {cls} -- {tag}",
           f"    genes [{genes}]  +{b}/-{c}  {s[0]} (resists {s[1]}, weak {s[2]})"]
    for L in (1, 30, 100):
        out.append(f"    L{L:<4}{line(natural_attrs(n, L, cls), L)}")
    return "\n".join(out)

if __name__ == "__main__":
    print(f"Settings: Personality +/-{PERSONALITY_MULT:.0%}, class tilt {CLASS_TILT:.0%}, fit exponent {FIT_EXPONENT:g}")
    print("Genes listed in order STR CON SPD DEX WIL INT WIS. Attributes shown before training.\n")
    rng = random.Random(11)
    for _ in range(8):
        n = roll_normal(rng); print(show(n, roll_class(n, rng))); print()
    pop = [roll_normal(rng) for _ in range(10000)]
    classes = [roll_class(n, rng) for n in pop]
    nat = sum(is_natural_fit(n, c) for n, c in zip(pop, classes))
    print(f"Across 10,000 recruits: {nat/len(pop):.0%} natural fits")
    for c, k in sorted(Counter(classes).items(), key=lambda kv: -kv[1]):
        print(f"    {c:<10} {k/len(pop):5.1%}")
    for L in (30, 100):
        gaps = sorted(max(a.values()) - min(a.values()) for a in (natural_attrs(n, L, c) for n, c in zip(pop, classes)))
        print(f"  Median best-minus-worst gap at L{L}, with class tilt: {gaps[len(gaps)//2]:.0f}")
