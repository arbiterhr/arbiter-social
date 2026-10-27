"""Make a 1080x1080 Arbiter HR brand card (black and gold) for a social post.

Usage: python make_card.py out.png "Eyebrow" "Headline text" "Sub line" LOGO_PNG SERIF_TTF SANS_TTF
"""
import sys
from PIL import Image, ImageDraw, ImageFont

out, eyebrow, headline, sub, logo_p, serif_p, sans_p = sys.argv[1:8]
W = H = 1080
BG = (15, 14, 12)
GOLD = (201, 162, 74)
CREAM = (240, 232, 214)
MUTED = (165, 157, 138)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def font(path, size, weight=None, wdth=None):
    f = ImageFont.truetype(path, size)
    try:
        axes = f.get_variation_axes()
        vals = []
        for a in axes:
            name = a.get("name", b"")
            name = name.decode() if isinstance(name, bytes) else name
            if name.lower().startswith("weight") and weight:
                vals.append(weight)
            elif name.lower().startswith("width") and wdth:
                vals.append(wdth)
            else:
                vals.append(a["default"])
        f.set_variation_by_axes(vals)
    except Exception:
        pass
    return f

M = 96
# soft gold glow top-right
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
for r in range(520, 0, -8):
    t = r / 520
    c = tuple(int(BG[i] + (GOLD[i] - BG[i]) * 0.10 * (1 - t)) for i in range(3))
    gd.ellipse((W - 160 - r, -160 - r, W - 160 + r, -160 + r), fill=c)
img = glow
d = ImageDraw.Draw(img)

# logo + wordmark
logo = Image.open(logo_p).convert("RGBA")
logo = logo.crop(logo.getbbox()).resize((92, 92 * logo.crop(logo.getbbox()).height // logo.crop(logo.getbbox()).width) if False else (92, 80))
img.paste(logo, (M, M - 6), logo)
wm = font(serif_p, 40, weight=600)
d.text((M + 116, M + 6), "A R B I T E R", font=wm, fill=CREAM)
tag = font(sans_p, 17, weight=500)
d.text((M + 118, M + 56), "WORKPLACE INVESTIGATIONS & HR", font=tag, fill=GOLD)

# eyebrow
eb = font(sans_p, 24, weight=600)
y = 330
d.text((M, y), eyebrow.upper(), font=eb, fill=GOLD)
y += 54

# headline, wrapped
hf = font(serif_p, 84, weight=600)
maxw = W - 2 * M
words, lines, cur = headline.split(), [], ""
for w in words:
    t = (cur + " " + w).strip()
    if d.textlength(t, font=hf) <= maxw:
        cur = t
    else:
        lines.append(cur); cur = w
lines.append(cur)
for ln in lines:
    d.text((M, y), ln, font=hf, fill=CREAM)
    y += 92

# sub line
y += 18
d.rectangle((M, y, M + 64, y + 4), fill=GOLD)
y += 30
sf = font(sans_p, 32, weight=400)
words, lines, cur = sub.split(), [], ""
for w in words:
    t = (cur + " " + w).strip()
    if d.textlength(t, font=sf) <= maxw:
        cur = t
    else:
        lines.append(cur); cur = w
lines.append(cur)
for ln in lines:
    d.text((M, y), ln, font=sf, fill=MUTED)
    y += 46

# footer
d.line((M, H - 150, W - M, H - 150), fill=(60, 52, 36), width=2)
ff = font(sans_p, 28, weight=500)
d.text((M, H - 118), "arbiterhr.co.uk", font=ff, fill=GOLD)
ft = font(sans_p, 22, weight=400)
txt = "Independent HR for health and social care"
d.text((W - M - d.textlength(txt, font=ft), H - 114), txt, font=ft, fill=MUTED)

img.save(out, "PNG", optimize=True)
print(out)
