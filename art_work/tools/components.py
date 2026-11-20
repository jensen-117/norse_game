import sys, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
src, out, gap = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert("RGBA"); a = np.asarray(im)
mask = a[..., 3] > 40
lab, n = ndimage.label(ndimage.binary_dilation(mask, iterations=gap))
boxes = [s for s in ndimage.find_objects(lab) if s is not None]
boxes = [b for b in boxes if (b[0].stop - b[0].start) * (b[1].stop - b[1].start) > 30]
boxes.sort(key=lambda b: (b[0].start // 40, b[1].start))
sheet = im.copy().convert("RGBA"); bg = Image.new("RGBA", sheet.size, (60, 60, 70, 255)); bg.alpha_composite(sheet)
d = ImageDraw.Draw(bg)
for i, b in enumerate(boxes):
    y0, y1, x0, x1 = b[0].start, b[0].stop, b[1].start, b[1].stop
    d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(255, 60, 60, 255)); d.text((x0 + 1, y0 + 1), str(i), fill=(255, 255, 0, 255))
bg.save(out)
for i, b in enumerate(boxes): print(i, b[1].start, b[0].start, b[1].stop - b[1].start, b[0].stop - b[0].start)
