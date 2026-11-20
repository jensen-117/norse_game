"""Joseph's hit animations (slash 48x32, crush and pierce 16x16; Nov 7) -> martial white, with cadences.
His warm ramp maps by lightness onto the martial white ramp already used by fx_Martial:
    fcef8d -> ffffff, ffb879 -> c7dcd0, f48d6d -> 9babb2, ea6262 -> 7f708a
Cadence is data: per-frame ms, plus a hit-stop (the target holds its hit pose, nudged 1px) on the impact frame.
    python3 hits_martial.py <scratchpad> <art_res64>"""
import sys, os, glob
from PIL import Image, ImageDraw
S, ART = sys.argv[1], sys.argv[2]
SRC = {"slash": "2f79e9ef-slash_1", "crush": "10b17927-crush_1", "pierce": "29c7747c-pierce_1",
       "crush2": "3e668d1c-crush_2", "pierce2": "260ee6ad-pierce_2"}      # second versions: already Res64 whites
MAP = {"fcef8d": "ffffff", "ffb879": "c7dcd0", "f48d6d": "9babb2", "ea6262": "7f708a",
       "ffffff": "ffffff", "c7dcd0": "c7dcd0"}
# frames used (slash frame 0 is a reference of the crescents, not part of the swing), ms per frame, impact frame
CADENCE = {
    "slash":  dict(frames=list(range(1, 10)), ms=[40, 40, 40, 50, 70, 60, 50, 50, 60], impact=4),
    "crush":  dict(frames=list(range(8)),     ms=[40, 90, 70, 60, 60, 60, 60, 70],     impact=1),
    "pierce": dict(frames=list(range(8)),     ms=[40, 50, 90, 60, 50, 50, 50, 60],     impact=2),
    # crush 2: the ring pulls in (the wind-up), a beat on the dot, then the blow bursts out and shards fly
    "crush2": dict(frames=list(range(8)),     ms=[40, 40, 40, 40, 40, 20, 70, 70],     impact=5),   # the white burst: one flicker (20ms is the shortest a GIF plays reliably)
    # pierce 2: the thrust line runs in and narrows to the point, then the hit sprays along the line
    "pierce2": dict(frames=list(range(8)),    ms=[40, 40, 40, 40, 70, 90, 60, 60],     impact=4),
    "slash_coded": dict(frames=list(range(8)), ms=[40, 40, 40, 50, 60, 50, 50, 60],   impact=2),
}
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def load(name):
    out = []
    for p in sorted(glob.glob(f"{S}/ws_hit/{SRC[name]}/frame[0-9].png")):
        im = Image.open(p).convert("RGBA"); px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                if px[x, y][3]: px[x, y] = rgb(MAP["%02x%02x%02x" % px[x, y][:3]]) + (255,)
        out.append(im)
    return out

if __name__ == "__main__":
    OUT = f"{ART}/effects/martial"; os.makedirs(OUT, exist_ok=True)
    fx = {n: load(n) for n in SRC}
    sys.path.insert(0, f"{S}/tools"); from slash_gen import slash_frames
    fx["slash_coded"] = slash_frames(flip=True, centre=(26, 20))     # a hero cuts across the enemy's front
    for n, fr in fx.items():
        used = [fr[i] for i in CADENCE[n]["frames"]]
        strip = Image.new("RGBA", (used[0].width * len(used), used[0].height))
        for i, f in enumerate(used): strip.alpha_composite(f, (used[0].width * i, 0))
        strip.save(f"{OUT}/hit_{n}.png")
    sc, W, H = 4, 120, 64
    wiz = Image.open(f"{ART}/heroes/wizard_side_v2/frames/Brennumar_right_idle1.png").convert("RGBA")
    dr = lambda rc: Image.open(f"{ART}/undead/draugr/frames/draugr_blar_native/{rc}.png").convert("RGBA")
    idle, hit = dr("r0c0"), dr("r4c1")
    def stage(enemy, f=None, label="", nudge=0):
        im = Image.new("RGBA", (W, H), (62, 53, 70, 255)); d = ImageDraw.Draw(im); d.fontmode = "1"   # no anti-aliased text: GIF colours stay exact
        d.rectangle([0, 58, W, H], fill=(46, 34, 47, 255))
        im.alpha_composite(wiz, (14, 26)); im.alpha_composite(enemy, (W - 66 + nudge, -6))
        if f is not None: im.alpha_composite(f, (W - 34 - f.width // 2 + nudge, 34 - f.height // 2))
        d.text((3, 2), label, fill=(255, 255, 255))
        return im.resize((W * sc, H * sc), Image.NEAREST)
    for tag, timed in (("tuned", True), ("flat100", False)):
        out, durs = [], []
        for n in ("slash", "slash_coded", "crush", "crush2", "pierce", "pierce2"):
            c = CADENCE[n]; out.append(stage(idle, label=n)); durs.append(500)
            for k, i in enumerate(c["frames"]):
                struck = k >= c["impact"] and k < c["impact"] + 3
                out.append(stage(hit if struck else idle, fx[n][i], n, nudge=1 if struck else 0))
                durs.append(c["ms"][k] if timed else 100)
            out.append(stage(idle, label=n)); durs.append(300)
        # quantize every frame onto the Res64 palette itself, undithered: the GIF shows the exact colours
        res = [rgb(h) for h in open(f"{S}/tools/res64.txt").read().split()]
        pal = Image.new("P", (1, 1)); pal.putpalette([v for c in res for v in c] + [0] * (768 - 3 * len(res)))
        out = [f.convert("RGB").quantize(palette=pal, dither=Image.Dither.NONE) for f in out]
        out[0].save(f"{OUT}/hits_demo_{tag}.gif", save_all=True, append_images=out[1:], duration=durs, loop=0)
    print("ok")
