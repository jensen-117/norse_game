"""Mock fight scenes (Nov 9): Joseph's 32R Beinar (bone tints) and Drattr next to the Mogel and the heroes,
placed with the Fight Lab's own cell geometry (screen.js cellFoot) on the lab backgrounds, at 1x then x4."""
import json, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "art_work/tools"); sys.argv = ["x"]
import beinar32_tints as T
T.F = "art_work/beinar_32r/frames/frame%d.png"
A = json.load(open("fight_lab/assets/assets.json")); atlas = Image.open("fight_lab/assets/atlas.png").convert("RGBA"); G = A["geo"]
def foot(side, row, lane):
    ty, th = G["lanes"][lane]; fy = ty + th - 5
    return round(G["GX"][f"{side}{row}"] + G["K"] * (G["FRONT"] - fy)) + (G["pitch"] - 16) // 2 + 8, fy
def lab(key):
    s = A["sprites"][key]; x, y, w, h = s["anims"]["idle"][0]; return atlas.crop((x, y, x + w, y + h))
def bein(fr, rank): return Image.fromarray(T.tint(fr, rank))
def drattr(i): return Image.open(f"art_work/drattr/frame{i}.png").convert("RGBA")
def place(bg, im, side, row, lane):
    fx, fy = foot(side, row, lane); bb = im.getbbox()
    im = im.crop(bb); bg.alpha_composite(im, (fx - im.width // 2, fy - im.height + 1))
HEROES = [("hero:Skurmar", 0, 0), ("hero:Lundar", 0, 1), ("hero:Brennumar", 0, 2), ("hero:Seidar", 1, 0), ("hero:Dagskald", 1, 1), ("hero:Hafrunar", 1, 2)]
def scene(bgname, foes, out):
    bg = Image.open(f"fight_lab/assets/bg_{bgname}.png").convert("RGBA")
    for k, r, l in HEROES: place(bg, lab(k), "0", r, l)
    for im, r, l in sorted(foes, key=lambda f: f[2]): place(bg, im, "1", r, l)
    bg.resize((bg.width * 4, bg.height * 4), Image.NEAREST).save(out)
scene("Neutral", [(bein(4, "aged"), 0, 0), (lab("mogel32:Natt"), 0, 1), (bein(5, "white"), 0, 2),
                  (bein(6, "red"), 1, 0), (bein(8, "white"), 1, 1), (lab("mogel16:Aska"), 1, 2)], "art_work/beinar_32r/mock_barrow_x4.png")
scene("Vatn", [(drattr(0), 0, 0), (lab("mogel24:Vatn"), 0, 1), (drattr(2), 0, 2),
               (drattr(3), 1, 0), (lab("mogel32:Hrim"), 1, 1), (drattr(4), 1, 2)], "art_work/beinar_32r/mock_vatn_x4.png")
scene("Eld", [(bein(3, "earth"), 0, 0), (lab("mogel32:Eld"), 0, 1), (bein(13, "red"), 0, 2),
              (bein(9, "red"), 1, 0), (lab("mogel16:Eld"), 1, 1), (drattr(1), 1, 2)], "art_work/beinar_32r/mock_eld_x4.png")
print("ok")
