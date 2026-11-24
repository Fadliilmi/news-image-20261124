#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up Tuesday 24 November 2026.

Every pixel is drawn by this script with Pillow; no photos, no borrowed art.
Stories were researched from fresh web reports of 24 Nov 2026 (Reuters, AP,
Yonhap, The Times of India, CNET). Run: python3 draw.py -> writes entry.png
beside this file (1024x1024, well under 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (20, 20, 26)
NAVY = (18, 33, 61)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (15, 118, 110)
SKY = (70, 130, 180)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
MUTED = (90, 90, 96)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w):
    """Largest bold/regular font size <= size that fits max_w."""
    while size > 10 and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=PANEL, outline=(200, 192, 175), width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=accent)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- Masthead ----
d.rectangle([0, 0, W, 148], fill=NAVY)
d.rectangle([0, 148, W, 154], fill=GOLD)
d.text((512, 18), "THE WORLD IN ONE PICTURE",
       font=font(FONT_B, 52), fill=WHITE, anchor="ma")
d.text((512, 84), "TUESDAY  •  24 NOVEMBER 2026",
       font=font(FONT_B, 34), fill=GOLD, anchor="ma")
d.text((512, 126), "A picture-editor's front page of the day's world news",
       font=font(FONT_R, 19), fill=(200, 205, 220), anchor="ma")

# ---- Lead story: South Korea airspace scare ----
lx, ly, lw, lh = 28, 170, 968, 330
panel(d, lx, ly, lw, lh, RED)
# Illustration: night sky over Ulleung Island, jet, alert beacon.
ix, iy, iw, ih = lx + 14, ly + 22, 470, 286
d.rectangle([ix, iy, ix + iw, iy + ih], fill=(24, 44, 84))
for sx, sy, r in [(60, 40, 2), (150, 25, 2), (260, 55, 3), (350, 30, 2),
                  (420, 70, 2), (100, 80, 2), (310, 90, 2)]:
    d.ellipse([ix + sx - r, iy + sy - r, ix + sx + r, iy + sy + r],
              fill=WHITE)
for r in (30, 60, 90):
    d.arc([ix + 330 - r, iy + 180 - r, ix + 330 + r, iy + 180 + r],
          start=200, end=340, fill=(120, 180, 255), width=3)
d.rectangle([ix, iy + 220, ix + iw, iy + ih], fill=(16, 60, 96))
d.polygon([(ix + 40, iy + 250), (ix + 120, iy + 190), (ix + 210, iy + 205),
           (ix + 300, iy + 235), (ix + 380, iy + 250)], fill=(28, 68, 48))
jx, jy = ix + 150, iy + 120
d.polygon([(jx, jy), (jx + 150, jy + 14), (jx + 40, jy + 22),
           (jx + 70, jy + 34), (jx + 20, jy + 30), (jx - 10, jy + 16)],
          fill=(210, 215, 225))
d.polygon([(jx + 30, jy + 8), (jx + 55, jy - 12), (jx + 70, jy + 6)],
          fill=(210, 215, 225))
bx, by = ix + 400, iy + 60
for r, col in ((46, (178, 34, 34)), (30, RED), (16, (255, 90, 90))):
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
d.text((bx, by - 13), "!", font=font(FONT_B, 30), fill=WHITE, anchor="ma")
d.text((ix + 16, iy + ih - 34), "ULLEUNG ISLAND, SOUTH KOREA",
       font=font(FONT_B, 18), fill=(190, 210, 240))

# Lead text (right of illustration). Text column: x 536..968 (432 wide).
tx = lx + 508
tw = lw - 508 - 28
f1 = fit(d, "AIRSPACE SCARE", FONT_B, 44, tw)
d.text((tx, ly + 24), "AIRSPACE SCARE", font=f1, fill=RED)
f2 = fit(d, "OVER ULLEUNG ISLAND", FONT_B, 44, tw)
d.text((tx, ly + 76), "OVER ULLEUNG ISLAND", font=f2, fill=INK)
text_block(d, tx, ly + 132,
           "A suspected North Korean jet enters South Korean "
           "airspace. Islanders take shelter — the warning "
           "lifts within minutes.",
           font(FONT_R, 24), INK, tw, leading=31)
d.text((tx, ly + 282), "REUTERS  •  AP  •  YONHAP",
       font=font(FONT_B, 19), fill=MUTED)

# ---- Row 2: Singapore + crypto ----
ry, rh = 516, 226
# Singapore (text column x sx+220, width 232)
sx, sy, sw = 28, ry, 476
panel(d, sx, sy, sw, rh, TEAL)
d.rectangle([sx + 14, sy + 120, sx + 14 + 190, sy + 120 + 86],
            fill=(210, 228, 222))
for bx0, bh in ((16, 55), (56, 85), (96, 48), (136, 100)):
    d.rectangle([sx + 14 + bx0, sy + 120 + 86 - bh,
                 sx + 14 + bx0 + 32, sy + 120 + 86], fill=TEAL)
d.line([(sx + 14, sy + 100), (sx + 70, sy + 70), (sx + 130, sy + 78),
        (sx + 196, sy + 34)], fill=(22, 140, 60), width=6)
d.polygon([(sx + 196, sy + 34), (sx + 182, sy + 34), (sx + 196, sy + 20)],
          fill=(22, 140, 60))
tx2 = sx + 220
tw2 = sw - 220 - 24
d.text((tx2, sy + 26), "SINGAPORE", font=font(FONT_B, 27), fill=INK)
d.text((tx2, sy + 58), "SPEEDS UP", font=font(FONT_B, 27), fill=INK)
text_block(d, tx2, sy + 100,
           "Economy grows 6.1% in Q3; 2026 forecast raised "
           "to about 6%.",
           font(FONT_R, 21), INK, tw2, leading=27)
d.text((tx2, sy + 192), "REUTERS", font=font(FONT_B, 19), fill=MUTED)

# Crypto / CFTC (text column x cx+136, width 316)
cx, cw = 520, 476
panel(d, cx, ry, cw, rh, GOLD)
d.ellipse([cx + 16, ry + 96, cx + 116, ry + 196], fill=(232, 184, 44),
          outline=(160, 120, 20), width=4)
d.text((cx + 66, ry + 108), "B", font=font(FONT_B, 64), fill=(120, 84, 8),
       anchor="ma")
d.line([(cx + 52, ry + 104), (cx + 52, ry + 188)], fill=(120, 84, 8), width=5)
d.line([(cx + 80, ry + 104), (cx + 80, ry + 188)], fill=(120, 84, 8), width=5)
tx3 = cx + 136
tw3 = cw - 136 - 24
d.text((tx3, ry + 26), "CRYPTO COUNTS", font=font(FONT_B, 27), fill=INK)
d.text((tx3, ry + 58), "AS RESERVES", font=font(FONT_B, 27), fill=INK)
text_block(d, tx3, ry + 100,
           "US regulator: crypto may count as platforms' "
           "reserves — not liquidity.",
           font(FONT_R, 21), INK, tw3, leading=27)
d.text((tx3, ry + 192), "REUTERS", font=font(FONT_B, 19), fill=MUTED)

# ---- Row 3: chess, India AI, supermoon ----
by, bh = 758, 214
bw = 312

# Chess: headline top, body full width, mini board bottom-left, tag bottom-right
px = 28
panel(d, px, by, bw, bh, NAVY)
d.text((px + 16, by + 18), "CHESS CROWN", font=font(FONT_B, 24), fill=INK)
d.text((px + 16, by + 46), "ON THE LINE", font=font(FONT_B, 24), fill=INK)
text_block(d, px + 16, by + 82,
           "World title match opens in Geneva: Gukesh defends "
           "against Sindarov.",
           font(FONT_R, 18), INK, bw - 32, leading=23)
cell = 12
for r in range(4):
    for c in range(4):
        col = WHITE if (r + c) % 2 == 0 else NAVY
        d.rectangle([px + 16 + c * cell, by + 158 + r * cell,
                     px + 16 + (c + 1) * cell, by + 158 + (r + 1) * cell],
                    fill=col, outline=(150, 150, 150))
d.text((px + 22, by + 160), "K", font=font(FONT_B, 11), fill=RED, anchor="ma")
d.text((px + 58, by + 196), "Q", font=font(FONT_B, 11), fill=GOLD, anchor="ma")
d.text((px + bw - 16, by + 178), "TIMES OF INDIA",
       font=font(FONT_B, 15), fill=MUTED, anchor="ra")

# India AI: headline top, body, building + circuit bottom-left, tag bottom-right
px = 356
panel(d, px, by, bw, bh, (120, 60, 160))
d.text((px + 16, by + 18), "INDIA BETS ON AI", font=font(FONT_B, 24), fill=INK)
text_block(d, px + 16, by + 52,
           "PM Modi opens an AI centre at IIT Patna.",
           font(FONT_R, 18), INK, bw - 32, leading=23)
d.rectangle([px + 16, by + 118, px + 106, by + 198], fill=(120, 60, 160))
for wy in (132, 152, 172):
    for wx in (32, 56, 80):
        d.rectangle([px + wx, by + wy, px + wx + 14, by + wy + 11],
                    fill=(255, 220, 90))
for nx, ny in ((140, 130), (160, 160), (140, 188)):
    d.ellipse([px + nx - 6, by + ny - 6, px + nx + 6, by + ny + 6],
              fill=GOLD)
d.line([(px + 140, by + 130), (px + 160, by + 160), (px + 140, by + 188)],
       fill=GOLD, width=3)
d.text((px + bw - 16, by + 178), "TIMES OF INDIA",
       font=font(FONT_B, 15), fill=MUTED, anchor="ra")

# Supermoon: dark box, headline top, moon bottom-left, text right, tag bottom
px = 684
panel(d, px, by, bw, bh, (40, 40, 90))
d.rectangle([px + 12, by + 18, px + bw - 12, by + bh - 12], fill=(12, 14, 44))
d.text((px + 26, by + 30), "SUPERMOON MEETS", font=font(FONT_B, 21),
       fill=WHITE)
d.text((px + 26, by + 56), "THE PLEIADES", font=font(FONT_B, 21), fill=GOLD)
d.text((px + bw - 26, by + 58), "CNET", font=font(FONT_B, 15),
       fill=(170, 170, 190), anchor="ra")
d.ellipse([px + 26, by + 100, px + 106, by + 180], fill=(245, 230, 170))
d.ellipse([px + 44, by + 120, px + 60, by + 136], fill=(220, 200, 140))
d.ellipse([px + 72, by + 148, px + 84, by + 160], fill=(220, 200, 140))
for sx_, sy_ in [(40, 190), (90, 186), (150, 192), (200, 188), (240, 193),
                 (275, 187), (115, 196)]:
    d.ellipse([px + sx_ - 3, by + sy_ - 3, px + sx_ + 3, by + sy_ + 3],
              fill=WHITE)
text_block(d, px + 122, by + 100,
           "Full moon glides past the Seven Sisters tonight.",
           font(FONT_R, 18), (220, 220, 235), bw - 122 - 24, leading=23)

# ---- Footer ----
d.text((512, 986), "Sources: Reuters  •  AP  •  Yonhap  •  The Times of India  •  CNET  —  all drawn by code, no photographs",
       font=font(FONT_R, 17), fill=MUTED, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
