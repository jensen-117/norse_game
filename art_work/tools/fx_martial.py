"""The martial effect set (white), cut from the converted bdragon sheet by name, plus demo GIFs:
every effect on a Draugr, and the Gandraugr's stand-in cast (hold a frame, flash, Natt out).
The sheet's layout is the same in every element sheet, so the same table names elemental effects too.
    python3 fx_martial.py <art_res64>"""
import sys, os
from PIL import Image, ImageDraw
ART = sys.argv[1]
SHEETS = f"{ART}/effects/sheets"
GROUPS = {"A": (0, 5), "B": (7, 8), "C": (10, 12), "D": (14, 17), "E": (19, 22), "F": (24, 28), "G": (30, 35)}

# name: list of (group, row, frame index within the group), and the frame time in ms
FX = {
    "slash":  ([("C", 3, i) for i in range(3)], 70),                     # a thin crescent slice
    "crush":  ([("B", 5, 0), ("B", 5, 1), ("D", 5, 2), ("D", 5, 3)], 70),  # a burst, then the shockwave ring
    "pierce": ([("F", 6, i) for i in range(5)], 50),                      # a fast streak, point first
    "shot":   ([("F", 0, i) for i in range(5)], 50),                      # the arrow in flight (moved by the caller)
    "spark":  ([("C", 6, i) for i in range(3)], 70),                      # a shot landing
    "crit":   ([("F", 1, i) for i in range(5)], 60),                      # the sparkle laid over a crit
    "graze":  ([("F", 4, i) for i in (2, 3, 4)], 70),                     # a small fading glint
    "defend": ([("F", 8, i) for i in range(5)], 70),                      # a ward ring closing in
    "taunt":  ([("C", 6, i) for i in range(3)], 90),                      # shout lines
    "move":   ([("C", 1, i) for i in range(3)], 80),                      # a dust puff
    "flash":  ([("C", 8, i) for i in range(3)], 70),                      # a cast going off
    "down":   ([("F", 12, i) for i in range(5)], 90),                     # the last breath rising
}

def frames(name, element="Martial"):
    sheet = Image.open(f"{SHEETS}/fx_{element}.png").convert("RGBA")
    seq, ms = FX[name]
    return [sheet.crop(((GROUPS[g][0] + i) * 16, r * 16, (GROUPS[g][0] + i) * 16 + 16, r * 16 + 16)) for g, r, i in seq], ms

def white(spr):
    """A full-white silhouette, for the cast flash."""
    out = spr.copy(); px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            if px[x, y][3]: px[x, y] = (255, 255, 255, 255)
    return out

if __name__ == "__main__":
    OUT = f"{ART}/effects/martial"; os.makedirs(OUT, exist_ok=True)
    # 1. strips, one per named effect
    for n in FX:
        fr, _ = frames(n); strip = Image.new("RGBA", (16 * len(fr), 16))
        for i, f in enumerate(fr): strip.alpha_composite(f, (16 * i, 0))
        strip.save(f"{OUT}/fx_{n}.png")
    # 2. demo: every effect on a Draugr, a wizard watching
    sc, W, H = 4, 120, 64
    BG = (62, 53, 70, 255)
    wiz = Image.open(f"{ART}/heroes/wizard_side_v2/frames/Brennumar_right_idle1.png").convert("RGBA")
    def dr(rc, tint="blar"):
        return Image.open(f"{ART}/undead/draugr/frames/draugr_{tint}_native/{rc}.png").convert("RGBA")
    def stage(enemy, fx=None, fx_at=(78, 30), wiz_fx=None, label="", proj=None):
        im = Image.new("RGBA", (W, H), BG); d = ImageDraw.Draw(im)
        d.rectangle([0, 58, W, H], fill=(46, 34, 47, 255))
        im.alpha_composite(wiz, (14, 58 - 32)); im.alpha_composite(enemy, (W - 64 - 2, 58 - 64))
        if fx is not None: im.alpha_composite(fx, fx_at)
        if wiz_fx is not None: im.alpha_composite(wiz_fx, (14, 34))
        if proj is not None: im.alpha_composite(proj[0], proj[1])
        d.text((3, 2), label, fill=(240, 240, 240))
        return im.resize((W * sc, H * sc), Image.NEAREST)
    idle = dr("r0c0"); hit = dr("r4c1")                          # the hit pose (its baked spark is gone)
    out, durs = [], []
    def hold(im, ms): out.append(im); durs.append(ms)
    for n in ("slash", "crush", "pierce", "graze", "crit"):
        fr, ms = frames(n)
        hold(stage(idle, label=n), 400)
        for f in fr: hold(stage(hit, f, label=n), ms)
        hold(stage(idle, label=n), 250)
    fr, ms = frames("shot"); sp, ms2 = frames("spark")             # an arrow crossing, then the spark
    hold(stage(idle, label="shot"), 300)
    for k in range(8):
        f = fr[min(k, len(fr) - 1)]
        hold(stage(idle, proj=(f, (30 + k * 6, 30)), label="shot"), 40)
    for f in sp: hold(stage(hit, f, label="shot"), ms2)
    hold(stage(idle, label="shot"), 250)
    for n in ("defend", "taunt"):
        fr, ms = frames(n)
        hold(stage(idle, label=n), 300)
        for f in fr: hold(stage(idle, wiz_fx=f, label=n), ms)
        hold(stage(idle, label=n), 250)
    out[0].save(f"{OUT}/martial_fx_demo.gif", save_all=True, append_images=out[1:], duration=durs, loop=0)
    # 3. the Gandraugr's stand-in cast: hold the raised frame, flash, Natt goes out, lands on the wizard
    out, durs = [], []
    raise_ = dr("r1c7")
    nb, _ = frames("flash", "Natt"); orb, _ = frames("shot", "Natt"); land, _ = frames("crush", "Natt")
    hold(stage(idle, label="Gandraugr: Mernatt"), 400)
    hold(stage(raise_, label="Gandraugr: Mernatt"), 450)                              # hold
    for k in range(2):                                                               # flash
        hold(stage(white(raise_), label="Gandraugr: Mernatt"), 60); hold(stage(raise_, label="Gandraugr: Mernatt"), 60)
    for f in nb: hold(stage(raise_, f, fx_at=(66, 16), label="Gandraugr: Mernatt"), 70)  # it goes off in the hand
    for k in range(8):                                                               # out
        f = orb[min(k, len(orb) - 1)].transpose(Image.FLIP_LEFT_RIGHT)
        hold(stage(raise_, proj=(f, (64 - k * 6, 30)), label="Gandraugr: Mernatt"), 40)
    for f in land: hold(stage(idle, wiz_fx=f, label="Gandraugr: Mernatt"), 70)
    hold(stage(idle, label="Gandraugr: Mernatt"), 500)
    out[0].save(f"{OUT}/gandraugr_cast_demo.gif", save_all=True, append_images=out[1:], duration=durs, loop=0)
    print("ok")
