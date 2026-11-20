"""A/B: the Mogel's slime paint on vs off (drawn Mogel packs, board and rotation on)."""
import sys, engine
from rotation_check import run
n = int(sys.argv[1])
for L in (10, 30):
    engine.MOGEL_PAINT_RANKS = set(); off = run(L, n, True, ["Mogel (drawn)"])["Mogel (drawn)"]
    engine.MOGEL_PAINT_RANKS = {"Mogel", "Stor", "Drott"}; on = run(L, n, True, ["Mogel (drawn)"])["Mogel (drawn)"]
    print(f"Level {L}: party wins {off[0]:.0%} without paint -> {on[0]:.0%} with paint; median rounds {off[1]} -> {on[1]}")
