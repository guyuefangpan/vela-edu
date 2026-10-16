from PIL import Image
import os
from collections import Counter

ICO = r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\site\assets\favicon.ico"
OUT = r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\site\assets\favicon.png"

im = Image.open(ICO)
print("mode:", im.mode, "size:", im.size, "frames:", getattr(im, "n_frames", 1))

if im.mode != "RGBA":
    im = im.convert("RGBA")
w, h = im.size
im.save(OUT, "PNG")
print("saved png:", OUT, os.path.getsize(OUT))

# 分析像素：统计主色 + 透明/不透明比例
px = im.load()
cnt = Counter()
opaque = 0
total = w * h
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a > 20:
            opaque += 1
            cnt[(r // 32 * 32, g // 32 * 32, b // 32 * 32)] += 1
print("opaque ratio: %.2f" % (opaque / total))
print("top opaque colors (r,g,b):")
for c, n in cnt.most_common(6):
    print("  ", c, n)
