import struct, sys, colorsys
from PIL import Image
S = sys.argv[1]
# read the palette from the user's Aseprite file
d = open(f"{S}/art_in/wizard.aseprite", "rb").read()
off = 128; pal = []
nframes = struct.unpack_from('<H', d, 6)[0]
fbytes = struct.unpack_from('<I', d, off)[0]
nch = struct.unpack_from('<I', d, off + 12)[0] or struct.unpack_from('<H', d, off + 6)[0]
p = off + 16
for _ in range(nch):
    csize, ctype = struct.unpack_from('<IH', d, p); body = d[p + 6:p + csize]
    if ctype == 0x2019:
        n, first, last = struct.unpack_from('<III', body, 0); q = 20
        for i in range(first, last + 1):
            ef, r, g, b, a = struct.unpack_from('<HBBBB', body, q); q += 6
            if ef & 1: q += 2 + struct.unpack_from('<H', body, q)[0]
            if a: pal.append((r, g, b))
    p += csize
def nearest(c):
    return min(pal, key=lambda q: (q[0]-c[0])**2*0.3 + (q[1]-c[1])**2*0.59 + (q[2]-c[2])**2*0.11)
ROBE = {(77,155,230),(71,140,208),(96,165,230),(96,117,186),(115,133,192)}
TARGETS = {"Vatn (original)": None, "Eld": (0.00, 1.0), "Blast": (0.55, 0.35), "Jord": (0.33, 0.9),
           "Sol": (0.105, 1.15), "Natt": (0.77, 0.9)}
frames = [Image.open(f"{S}/art_out/frame{i}.png").convert("RGBA") for i in range(4)]
rows = []
for name, t in TARGETS.items():
    row = []
    for fr in frames:
        im = fr.copy(); px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a and (r, g, b) in ROBE and t:
                    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
                    nr, ng, nb = colorsys.hsv_to_rgb(t[0], s * t[1], min(1.0, v * (1.08 if t[0] == 0.105 else 1)))
                    px[x, y] = nearest((int(nr*255), int(ng*255), int(nb*255))) + (a,)
        row.append(im)
    rows.append((name, row))
scale, pad = 6, 12
W = len(frames) * (16 * scale + pad) + pad
H = len(rows) * (32 * scale + pad) + pad
sheet = Image.new("RGBA", (W, H), (40, 40, 48, 255))
for ri, (name, row) in enumerate(rows):
    for fi, im in enumerate(row):
        sheet.alpha_composite(im.resize((16*scale, 32*scale), Image.NEAREST),
                              (pad + fi * (16*scale + pad), pad + ri * (32*scale + pad)))
sheet.save(f"{S}/art_out/wizard_schools.png")
# transpose for a compact one-row-per-frame-0 preview
prev = Image.new("RGBA", (len(rows) * (16*scale + pad) + pad, 32*scale + 2*pad), (40, 40, 48, 255))
for ri, (name, row) in enumerate(rows):
    prev.alpha_composite(row[0].resize((16*scale, 32*scale), Image.NEAREST), (pad + ri*(16*scale+pad), pad))
prev.save(f"{S}/art_out/wizard_schools_idle.png")
print(len(pal), "palette colors")
