#!/usr/bin/env python3
"""
One-off helper: turns a photo into
  assets/avatar_duotone.webp  (cut-out bust, orange duotone, rim glow)  -> front face of the 3D rotator
  assets/portrait.json        (60x50 ASCII map with face/hoodie tones)   -> back face of the 3D rotator
Needs: pip install pillow numpy scipy      Usage: python scripts/prepare_avatar.py path/to/photo.png
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

SRC = sys.argv[1] if len(sys.argv) > 1 else "avatar.png"
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
CX, TOP, CWID = 1012, 110, 1300          # crop (centre-x, top, width) in source pixels; 4:5 portrait
OW, OH = 600, 750

src = Image.open(SRC).convert("RGB")
crop = src.crop((CX - CWID // 2, TOP, CX + CWID // 2, TOP + int(CWID * 1.25))).resize((OW, OH), Image.LANCZOS)
a = np.asarray(crop).astype(np.int16)

# background = near-white region connected to the image border
cand = a.min(axis=2) >= 228
lab, _ = ndimage.label(cand)
border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
bg = np.isin(lab, border[border > 0])
alpha = np.where(bg, 0.0, 1.0)
alpha = ndimage.grey_erosion(alpha, size=(3, 3))
alpha = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
# (the bottom fade is applied in the SVG as a mask, which avoids seam banding between strips)

rgb = np.asarray(crop).astype(np.float32) / 255
lum = .299 * rgb[..., 0] + .587 * rgb[..., 1] + .114 * rgb[..., 2]
sub = lum[alpha > .6]
lo, hi = np.percentile(sub, 3), np.percentile(sub, 99.3)
t = np.clip((lum - lo) / (hi - lo), 0, 1) ** .85
stops = [(0.0, (10, 8, 8)), (.30, (74, 28, 8)), (.58, (196, 76, 12)), (.84, (255, 112, 28)), (1.0, (246, 238, 226))]
col = np.zeros(t.shape + (3,), np.float32)
for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
    mk = (t >= t0) & (t <= t1)
    u = ((t - t0) / (t1 - t0))[mk][:, None]
    col[mk] = np.array(c0) * (1 - u) + np.array(c1) * u

glow = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))).astype(np.float32) / 255
rim = np.clip(glow - alpha * .9, 0, 1) * .8
outa = np.clip(alpha + rim * (1 - alpha), 0, 1)
orange = np.array([255, 91, 15], np.float32)
outc = np.where(outa[..., None] > 0, (col * alpha[..., None] + orange * (rim * (1 - alpha))[..., None]) / np.maximum(outa[..., None], 1e-4), 0)
Image.fromarray(np.dstack([np.clip(outc, 0, 255), outa * 255]).astype(np.uint8), "RGBA").save(
    os.path.join(OUTDIR, "avatar_duotone.webp"), "WEBP", quality=80, method=6)

# ASCII back face
CW, CH = 60, 50
small = np.asarray(crop.resize((CW, CH), Image.BOX)).astype(np.float32)
am = np.asarray(Image.fromarray((np.where(bg, 0, 255)).astype(np.uint8)).resize((CW, CH), Image.BOX)).astype(np.float32) / 255
L = (.299 * small[..., 0] + .587 * small[..., 1] + .114 * small[..., 2]) / 255
msk = am > .5
lo, hi = np.percentile(L[msk], 4), np.percentile(L[msk], 99)
tt = np.clip((L - lo) / (hi - lo), 0, 1) ** .75
ramp = " .:-=+*#%@"
fadeS = np.ones(CH); f1 = int(CH * .86); fadeS[f1:] = np.linspace(1, .35, CH - f1)
chars, tone = [], []
for r in range(CH):
    rc, rt = "", ""
    for c in range(CW):
        if not msk[r, c]:
            rc += " "; rt += "b"; continue
        k = max(int(tt[r, c] * .999 * (len(ramp) - 1) * fadeS[r]), 2)
        rc += ramp[k]
        R, G, B = small[r, c]
        rt += "o" if (G > R * 1.12 and G >= B * .8) else "b"
    chars.append(rc); tone.append(rt)
json.dump({"cols": CW, "rows": CH, "chars": chars, "tone": tone}, open(os.path.join(OUTDIR, "portrait.json"), "w"))
print("ok", os.path.getsize(os.path.join(OUTDIR, "avatar_duotone.webp")), "bytes webp;", sum(1 for r in chars for c in r if c != " "), "glyphs")
