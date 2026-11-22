#!/usr/bin/env python3
"""Render 'THE 22 — World Wire' for 22 November 2026 world news to entry.png.

A news-wire dashboard in ink on cold paper: masthead with the date, a lead
panel (Russian missiles and drones spilling into Polish airspace during
strikes on Ukraine, drawn as a border-crossing track map), four story tiles
down the right (FBI NCIC database hack, COP31 overtime deadlock, market
selloff, Xi-Trump-Putin summit fallout), three feature tiles below, and a
wire ticker. 1024x1024, PIL only, deterministic (fixed data, no clock or
randomness).
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (238, 240, 236)
INK = (18, 24, 34)
RED = (168, 30, 34)
BLUE = (20, 60, 110)
GREEN = (18, 110, 70)
AMBER = (176, 112, 16)
GREY = (104, 106, 104)
TILE_BG = (250, 250, 247)
BAND = (28, 44, 66)
BODY = (60, 62, 60)

FD = "/usr/share/fonts/truetype/dejavu/"

def F(name, size):
    return ImageFont.truetype(FD + name, size)

sans_b = lambda s: F("DejaVuSans-Bold.ttf", s)
sans = lambda s: F("DejaVuSans.ttf", s)
serif_b = lambda s: F("DejaVuSerif-Bold.ttf", s)
mono = lambda s: F("DejaVuSansMono.ttf", s)
mono_b = lambda s: F("DejaVuSansMono-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    return lines

def tile(x0, y0, x1, y1, kicker, kcol, head, body, head_px=23, body_px=15, body_lines=None):
    d.rectangle([x0, y0, x1, y1], fill=TILE_BG, outline=INK, width=2)
    d.rectangle([x0, y0, x0 + 8, y1], fill=kcol)
    d.text((x0 + 22, y0 + 14), kicker, font=sans_b(15), fill=kcol)
    iw = (x1 - x0) - 44
    yy = y0 + 40
    hlines = wrap(head, sans_b(head_px), iw)[:2]
    for ln in hlines:
        d.text((x0 + 22, yy), ln, font=sans_b(head_px), fill=INK)
        yy += head_px + 7
    yy += 4
    maxb = body_lines if body_lines is not None else max(1, int((y1 - yy - 14) // 20))
    for ln in wrap(body, sans(body_px), iw)[:maxb]:
        d.text((x0 + 22, yy), ln, font=sans(body_px), fill=BODY)
        yy += 20

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 10], fill=BLUE)
d.text((36, 34), "THE 22", font=serif_b(62), fill=INK)
d.text((36, 112), "WORLD WIRE · SUNDAY 22 NOVEMBER 2026", font=sans_b(21), fill=BLUE)
d.text((W - 36, 44), "one day\none image", font=sans(19), fill=GREY, anchor="ra")

# ---------------------------------------------------------------- lead panel
x0, y0, x1, y1 = 36, 168, 610, 700
tile(x0, y0, x1, y1, "LEAD · EUROPE", RED, "Russian missiles land in Poland", "", body_lines=0)
bx0, by0, bx1, by1 = x0 + 24, y0 + 92, x1 - 24, y1 - 100
d.rectangle([bx0, by0, bx1, by1], fill=(30, 38, 52), outline=INK, width=2)
# stylised map: Ukraine lower right, Belarus upper middle, Poland left, Baltic top
d.text((bx0 + 10, by0 + 8), "MISSILES OVER NATO AIRSPACE", font=mono_b(18), fill=(255, 140, 100))
# coastline / border lines
d.line([bx0 + 20, by0 + 70, bx0 + 200, by0 + 110], fill=(70, 78, 92), width=2)
d.line([bx0 + 200, by0 + 110, bx0 + 320, by0 + 90], fill=(70, 78, 92), width=2)
d.line([bx0 + 320, by0 + 90, bx1 - 30, by0 + 130], fill=(70, 78, 92), width=2)
d.text((bx0 + 26, by0 + 44), "BALTIC SEA", font=mono(13), fill=(150, 158, 170))
# Poland
d.polygon([(bx0 + 30, by0 + 150), (bx0 + 130, by0 + 130), (bx0 + 190, by0 + 190),
           (bx0 + 150, by0 + 260), (bx0 + 50, by0 + 240)], outline=(110, 160, 200))
d.text((bx0 + 60, by0 + 185), "POLAND", font=mono_b(16), fill=(120, 180, 220))
# Belarus
d.polygon([(bx0 + 210, by0 + 130), (bx0 + 330, by0 + 120), (bx0 + 360, by0 + 210),
           (bx0 + 240, by0 + 210)], outline=(90, 98, 112))
d.text((bx0 + 248, by0 + 158), "BELARUS", font=mono(13), fill=(150, 158, 170))
# Ukraine
d.polygon([(bx0 + 200, by0 + 230), (bx1 - 40, by0 + 230), (bx1 - 50, by1 - 60),
           (bx0 + 230, by1 - 50)], outline=(90, 98, 112))
d.text((bx1 - 130, by1 - 80), "UKRAINE", font=mono_b(15), fill=(228, 150, 110))
# border line Poland/Belarus-Ukraine (the NATO edge)
d.line([bx0 + 190, by0 + 195, bx0 + 235, by0 + 300], fill=(228, 90, 70), width=3)
d.text((bx0 + 96, by0 + 300), "NATO BORDER", font=mono_b(13), fill=(228, 90, 70))
# incoming tracks from Ukraine across the border into Poland
targets = [(bx0 + 70, by0 + 200), (bx0 + 110, by0 + 235), (bx0 + 90, by0 + 160)]
for (tx, ty) in targets:
    sx, sy = bx1 - 90, by1 - 90
    for i in range(10):
        t = i / 9.0
        xx = sx + (tx - sx) * t
        yy2 = sy + (ty - sy) * t + 60 * math.sin(t * 2.2)
        if i:
            d.line([px, py, xx, yy2], fill=(228, 90, 70), width=2)
        px, py = xx, yy2
    d.ellipse([tx - 5, ty - 5, tx + 5, ty + 5], fill=(255, 120, 80))
# air-defence intercept bursts over Poland
for (cx, cy) in ((bx0 + 150, by0 + 120), (bx0 + 240, by0 + 150), (bx0 + 200, by0 + 100)):
    d.line([cx - 9, cy, cx + 9, cy], fill=(120, 190, 140), width=2)
    d.line([cx, cy - 9, cx, cy + 9], fill=(120, 190, 140), width=2)
d.text((bx1 - 10, by1 - 66), "Strays from strikes on Ukraine · Tusk: 'violation'", font=sans(15), fill=(228, 226, 220), anchor="ra")
yy = y1 - 86
for ln in wrap("Stray missiles and drones from Russia's overnight assault on Ukraine crossed into Polish airspace during Nato drills; Warsaw called it a provocation. A Russian cargo ship was hit in the Baltic.", sans(15), (x1 - x0) - 44)[:3]:
    d.text((x0 + 22, yy), ln, font=sans(15), fill=BODY)
    yy += 20

# ---------------------------------------------------------------- right column
RX0, RX1 = 640, 988
tile(RX0, 168, RX1, 338, "US · CYBER", BLUE, "FBI crime database hacked",
     "Warrants and background checks breached; second FBI hack in months.", head_px=21)
tile(RX0, 354, RX1, 524, "CLIMATE · COP31", AMBER, "Talks run into overtime",
     "Delegates deadlocked on a fossil-fuel roadmap; G77 accuses rich states of dividing the bloc.", head_px=21)
tile(RX0, 540, RX1, 710, "JUSTICE", GREEN, "Myanmar rejects genocide ruling",
     "ICJ: the junta targeted 815,000 Rohingyas; Malaysia to resettle 10,000.", head_px=21)

# ---------------------------------------------------------------- lower row
tile(36, 716, 336, 896, "MARKETS · AI", BLUE, "AI stocks slide again",
     "Nvidia falls 23% in its worst week in 18 years; the Nasdaq drops 10% in five sessions.", head_px=20, body_px=14)
tile(352, 716, 624, 896, "DISASTERS", RED, "Nigeria boat toll hits 24",
     "A boat of mourners capsizes in Bayelsa state; a supercell storm wrecks a Brazil town.", head_px=20, body_px=14)
tile(640, 716, 988, 896, "SCIENCE", GREEN, "Voyager: 1 light-day out",
     "Forty-nine years after launch, Nasa's Voyager 1 becomes the first human-made object a light-day from Earth.", head_px=20, body_px=14)

# ---------------------------------------------------------------- wire ticker
d.rectangle([0, 908, W, 998], fill=BAND)
ty = 922
d.ellipse([28, ty + 20, 42, ty + 34], fill=(228, 90, 70))
xx = 58
for tag, txt in [
    ("BEIJING", "Trump-Putin-Xi summit: nuclear talks agreed"),
    ("GENEVA", "No mandate yet on ban of autonomous weapons"),
]:
    d.text((xx, ty + 8), tag, font=mono_b(15), fill=(255, 190, 120))
    xx += d.textlength(tag, font=mono_b(15)) + 12
    d.text((xx, ty + 8), txt, font=sans(15), fill=(226, 228, 226))
    xx += d.textlength(txt, font=sans(15)) + 30
d.text((28, ty + 44), "EVENTS OF SUNDAY 22 NOVEMBER 2026 · THE 22 WORLD WIRE", font=mono(13), fill=(150, 160, 175))
d.text((W - 28, ty + 44), "SUN 22 NOV 2026", font=mono_b(15), fill=(226, 228, 226), anchor="ra")
d.rectangle([0, 1002, W, 1010], fill=BLUE)

img.save("entry.png")
print("saved", img.size)
