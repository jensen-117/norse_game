"""Nov 10: options for the tapestry map: the fight glyph, the fallen (grave) spoil, the party's prow, the event glyph,
a merchant's scales (if the prow takes the ship), and over-under weave textures. Drawn in code on the linen.
python3 tapestry_options.py -> art_work/tapestry/options.png (4x), options_1x.png"""
from PIL import Image, ImageDraw
OUT = "/home/claude/art_work/tapestry"
P = {".": None, "L": "fdcbb0", "l": "fca790", "w": "ab947a",
     "S": "c7dcd0", "s": "9babb2", "d": "625565", "k": "2e222f", "n": "232339", "K": "3e3546",
     "R": "b33831", "r": "831c5d", "q": "7a3045", "B": "4d65b4", "b": "323353", "m": "484a77",
     "g": "f9c22b", "G": "fbb954", "o": "7a5c40", "O": "4c3e24", "p": "753c54", "v": "6b3e75", "e": "966c6c"}
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
def glyph(rows):
    w = max(len(r) for r in rows); im = Image.new("RGBA", (w, len(rows)), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if P.get(c): im.putpixel((x, y), rgb(P[c]))
    return im

FIGHT = {
 "steel sword and shield": [
    "..........S..",
    ".........SsS.",
    ".........SsS.",
    "...ddd...SsS.",
    "..dsssd..SsS.",
    ".dssSssd.SsS.",
    ".dsSdSsd.SsS.",
    ".dssSssddSsSd",
    ".dssssd.dddd.",
    "..dsssd...O..",
    "...ddd....O..",
    "..........d..",
    ".............",
 ],
 "red sword, blue shield": [
    "..........R..",
    ".........RrR.",
    ".........RrR.",
    "...bbb...RrR.",
    "..bmmmb..RrR.",
    ".bmmBmmb.RrR.",
    ".bmBsBmb.RrR.",
    ".bmmBmmbbRrRb",
    ".bmmmmb.qqqq.",
    "..bmmmb...O..",
    "...bbb....O..",
    "..........q..",
    ".............",
 ],
 "one sword (wine)": [
    "......r......",
    ".....rqr.....",
    ".....rqr.....",
    ".....rqr.....",
    ".....rqr.....",
    ".....rqr.....",
    ".....rqr.....",
    ".....rqr.....",
    "..rrrrrrrrr..",
    "......q......",
    "......q......",
    ".....rqr.....",
    "......r......",
 ],
 "axe and shield": [
    ".......ddd...",
    "......dSSsd..",
    "......dSsd...",
    "...bbb.ddO...",
    "..bmmmb..O...",
    ".bmmBmmb.O...",
    ".bmBsBmb.O...",
    ".bmmBmmb.O...",
    ".bmmmmb..O...",
    "..bmmmb..O...",
    "...bbb...O...",
    ".........O...",
    ".............",
 ],
}
FALLEN = {
 "raven": [
    ".kk....",
    "kkkk...",
    "gkkkk..",
    "..kkkkk",
    "..kkkk.",
    "...k...",
    "..kk...",
 ],
 "cairn": [
    "...d...",
    "..dsd..",
    "..ddd..",
    ".dsddd.",
    ".ddsdd.",
    "dsdddsd",
    "ddddddd",
 ],
 "runestone": [
    "..dd...",
    ".dssd..",
    ".dkkd..",
    ".dsks..",
    ".dkkd..",
    "oooooo.",
    "ooooooo",
 ],
 "broken sword": [
    "......d",
    ".....d.",
    "....d..",
    ".......",
    "..d....",
    ".ddd...",
    "d.d....",
 ],
}
PROW = {
 "dragon prow, gold on plate": [
    "kkkkkkkkkkkkk",
    "kkkkkkkgggkkk",
    "kkkkkkggggggk",
    "kkkkkkggkgggk",
    "kkkkkkggkkggk",
    "kkkkkkggkkkkk",
    "kkkkkggkkkkkk",
    "kkkkkgkkkkkkk",
    "kkkkggkkkkkkk",
    "kkkkgkkkkkkkk",
    "kgggggkkkkkkk",
    "kkggggkkkkkkk",
    "kkkkkkkkkkkkk",
 ],
 "dragon prow, wood": [
    ".............",
    ".......ooo...",
    "......oooooo.",
    "......ooKooo.",
    "......oo..oo.",
    "......oo.....",
    ".....oo......",
    ".....o.......",
    "....oo.......",
    "....o........",
    ".ooooo.......",
    "..oooO.......",
    ".............",
 ],
}
EVENT = {
 "rune Ansuz (speech)": [
    ".............",
    ".....p.......",
    ".....pp......",
    ".....p.p.....",
    ".....pp.p....",
    ".....p.p.p...",
    ".....p..p....",
    ".....p...p...",
    ".....p.......",
    ".....p.......",
    ".....p.......",
    ".....p.......",
    ".............",
 ],
 "mead horn (poetry)": [
    ".............",
    ".............",
    ".gg..........",
    ".gppp........",
    "..pppp.......",
    "...pppp......",
    "....pppp.....",
    ".....pppp....",
    "......pppq...",
    ".......ppq...",
    "........qq...",
    ".............",
    ".............",
 ],
 "lyre (the skald)": [
    ".............",
    "...o.....o...",
    "..o.ooooo.o..",
    "..o.......o..",
    "..o.k.k.k.o..",
    "..o.k.k.k.o..",
    "..o.k.k.k.o..",
    "..o.k.k.k.o..",
    "..o.k.k.k.o..",
    "...o.k.k.o...",
    "....ooooo....",
    ".............",
    ".............",
 ],
}
MERCHANT = {
 "trader's scales": [
    "......O......",
    "..OOOOOOOOO..",
    "..O...O...O..",
    ".O.O..O..O.O.",
    "O...O.O.O...O",
    "OOOOO.O.OOOOO",
    ".OOO..O..OOO.",
    "......O......",
    "......O......",
    "....OOOOO....",
    ".............",
    ".............",
    ".............",
 ],
}

def weave(kind, w, h):
    im = Image.new("RGBA", (w, h), rgb(P["L"])); px = im.load(); L2 = rgb(P["l"])
    for y in range(h):
        for x in range(w):
            if kind == "tabby (1 px over-under)" and (x + y) % 2: px[x, y] = L2
            elif kind == "tabby, every other row" and y % 2 == 0 and (x + y // 2) % 2: px[x, y] = L2
            elif kind == "weft dashes (2 over, 2 under)" and y % 2 == 0 and ((x + (y // 2) * 2) % 4) < 2: px[x, y] = L2
            elif kind == "sparse ribs (1 in 4)" and y % 3 == 0 and (x + y) % 4 == 0: px[x, y] = L2
    return im
WEAVES = ["tabby (1 px over-under)", "tabby, every other row", "weft dashes (2 over, 2 under)", "sparse ribs (1 in 4)"]

def section(title, items, cell=24):
    return title, items, cell
def build(_scale=None):
    Z = 6; rows = [("FIGHT (13x13)", FIGHT), ("FALLEN (7x7)", FALLEN), ("PARTY PROW", PROW), ("EVENT", EVENT), ("MERCHANT, if the prow takes the ship", MERCHANT)]
    cw, ch = 130, 120; W = 4 * cw + 20; H = len(rows) * ch + 300
    sheet = Image.new("RGBA", (W, H), rgb(P["L"])); d = ImageDraw.Draw(sheet)
    y = 6
    for title, items in rows:
        d.text((8, y), title, fill=rgb(P["k"]))
        for i, (name, rows_) in enumerate(items.items()):
            g = glyph(rows_); g = g.resize((g.width * Z, g.height * Z), Image.NEAREST)
            x = 10 + i * cw; sheet.alpha_composite(g, (x + (cw - 20 - g.width) // 2, y + 14 + (80 - g.height) // 2))
            d.text((x, y + 98), name, fill=rgb(P["d"]))
        y += ch
    d.text((8, y), "WEAVE at 4x, with the sword and a raven on it", fill=rgb(P["k"]))
    for i, k in enumerate(WEAVES):
        sw = weave(k, 30, 40); sw.alpha_composite(glyph(FIGHT["one sword (wine)"]), (9, 6)); sw.alpha_composite(glyph(FALLEN["raven"]), (12, 24))
        sheet.alpha_composite(sw.resize((120, 160), Image.NEAREST), (10 + i * cw, y + 14)); d.text((10 + i * cw, y + 178), k, fill=rgb(P["d"]))
    return sheet

def strip():   # the weaves at 1x and 2x, as they'd sit on the screen
    out = Image.new("RGBA", (4 * 84, 64), rgb(P["L"]))
    for i, k in enumerate(WEAVES):
        sw = weave(k, 80, 30); sw.alpha_composite(glyph(FIGHT["one sword (wine)"]), (34, 8)); out.alpha_composite(sw, (i * 84, 0))
        out.alpha_composite(sw.crop((20, 0, 60, 30)).resize((80, 60), Image.NEAREST).crop((0, 0, 80, 34)), (i * 84, 30))
    return out
if __name__ == "__main__":
    build().save(f"{OUT}/options.png"); strip().save(f"{OUT}/weave_1x.png"); print("ok")
