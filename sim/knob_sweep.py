"""How big a stat knob would close the board's party edge? Enemy damage (SPIRIT_DMG_SCALE, physical families)."""
import sys, engine
from board_decomp import go, fams
from rotation_check import TARGET
import board_decomp
n, L = int(sys.argv[1]), int(sys.argv[2]); board_decomp.N[0] = n; board_decomp.L = L
print(f"Level {L}, {n} fights: party wins")
print(f"  {'':<34}" + "".join(f"{f.split()[0]:>9}" for f in fams))
print(f"  {'target (no board)':<34}" + "".join(f"{TARGET[L][f]:>9.0%}" for f in fams))
for k in (0.5, 0.55, 0.6, 0.65):
    go(f"enemy damage scale {k}", SPIRIT_DMG_SCALE=k)
