import struct, os

ICO = r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\site\assets\favicon.ico"
data = open(ICO, "rb").read()
print("size:", len(data), "magic:", data[:4].hex())
count = struct.unpack("<H", data[4:6])[0]
print("images:", count)
off = 6
best = None
for i in range(count):
    w, h, c, res, planes, bpp = data[off], data[off+1], data[off+2], data[off+3], struct.unpack("<H", data[off+4:off+6])[0], struct.unpack("<H", data[off+6:off+8])[0]
    sz = struct.unpack("<I", data[off+8:off+12])[0]
    o = struct.unpack("<I", data[off+12:off+16])[0]
    w = 256 if w == 0 else w
    h = 256 if h == 0 else h
    print(f"  img{i}: {w}x{h} bpp={bpp} planes={planes} bytes={sz} offset={o}")
    if best is None or sz > best[1]:
        best = (o, sz, w, h, bpp, i)
    off += 16

o, sz, w, h, bpp, i = best
chunk = data[o:o+sz]
print("best chunk first bytes:", chunk[:8].hex())
# 若内嵌 PNG 直接写出
if chunk[:8] == b"\x89PNG\r\n\x1a\n":
    out = r"C:\Users\Administrator\WorkBuddy\2026-10-11-12-57-51\site\assets\favicon.png"
    open(out, "wb").write(chunk)
    print("WROTE PNG (embedded):", out, len(chunk))
else:
    print("not embedded PNG; raw bpp:", bpp, "first4:", chunk[:4].hex())
