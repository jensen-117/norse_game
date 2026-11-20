"""The playback effects atlas for the Fight Lab: fight_lab/assets/fx.png + fx.json.

  hit_slash, hit_crush2, hit_pierce2   Joseph's martial hits (art_res64/effects/martial), timed by hits_martial.CADENCE
  burst:<El>                           magic landing: the element sheet's row 5, cols 14-17 (orb -> ring -> fading ring)
  spark:<El>                           heals, buffs, hexes: row 3, cols 14-17 (a cross sparkle that thins out)
The element sheets (bdragon1727's free effect set, recoloured per element) share one layout, so one set of cells
serves all of them. fx.json: name -> {x, y, w, h, n (frames, laid left to right), ms (per frame), impact (frame)}.
"""
import json, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "..", "..", "art_res64", "effects")
OUT = os.path.join(HERE, "..", "..", "fight_lab", "assets")
CADENCE = {   # copied from hits_martial.py (frames already cut to the used ones)
    "hit_slash":   dict(ms=[40, 40, 40, 50, 70, 60, 50, 50, 60], impact=4),
    "hit_crush2":  dict(ms=[40, 40, 40, 40, 40, 20, 70, 70], impact=5),
    "hit_pierce2": dict(ms=[40, 40, 40, 40, 70, 90, 60, 60], impact=4),
}
ELEMENTS = ["Eld", "Reyk", "Vatn", "Hrim", "Blast", "Blixt", "Jord", "Gro", "Sol", "Lak", "Natt", "Aska", "Martial"]
strips = []
for name, c in CADENCE.items():
    im = Image.open(f"{ART}/martial/{name}.png").convert("RGBA"); n = len(c["ms"])
    strips.append((name, im, im.width // n, im.height, n, c["ms"], c["impact"]))
def cells(sheet, row, cols):
    return [sheet.crop((c * 16, row * 16, c * 16 + 16, row * 16 + 16)) for c in cols]
for el in ELEMENTS:
    sh = Image.open(f"{ART}/sheets/fx_{el}.png").convert("RGBA")
    for kind, row, ms, imp in (("burst", 5, [60, 70, 80, 90], 0), ("spark", 3, [70, 70, 80, 90], 0)):
        fr = cells(sh, row, range(14, 18)); im = Image.new("RGBA", (16 * len(fr), 16))
        for i, f in enumerate(fr): im.alpha_composite(f, (16 * i, 0))
        strips.append((f"{kind}:{el}", im, 16, 16, len(fr), ms, imp))
W = max(s[1].width for s in strips); H = sum(s[1].height for s in strips)
atlas = Image.new("RGBA", (W, H)); meta = {}; y = 0
for name, im, w, h, n, ms, imp in strips:
    atlas.alpha_composite(im, (0, y)); meta[name] = dict(x=0, y=y, w=w, h=h, n=n, ms=ms, impact=imp); y += im.height
atlas.save(f"{OUT}/fx.png"); json.dump(meta, open(f"{OUT}/fx.json", "w"))
print(len(meta), "strips", atlas.size)
