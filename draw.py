#!/usr/bin/env python3
"""Draw the front page of Tuesday 24 November 2026 as a 1024x1024 PNG.

Deterministic: fixed colours, fixed text, no randomness, no timestamps,
no network. The output is baked into the repository as entry.png and
main.py copies it to /output/entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)   # warm off-white newsprint
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (23, 42, 72)
GREY = (90, 90, 90)
RULE = (17, 17, 17)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
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


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw a wrapped paragraph; returns y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, thick=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=thick)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 36  # margin
R = W - M

# ---------------------------------------------------------------- masthead
d.text((W // 2, 30), "THE WORLD TODAY", font=font(SERIF, 84),
       fill=INK, anchor="ma")
rule(d, M, 128, R, 4)
rule(d, M, 136, R, 1)
d.text((W // 2, 148), "TUESDAY, 24 NOVEMBER 2026  •  THE DAY'S NEWS IN ONE IMAGE",
       font=font(SANS_B, 21), fill=INK, anchor="ma")
rule(d, M, 186, R, 4)

# ---------------------------------------------------------------- lead story
LY = 206
d.text((M, LY), "LEAD  •  UNITED STATES", font=font(SANS_B, 20), fill=RED)
for i, line in enumerate(["HUAWEI GUILTY OF", "TRADE SECRETS",
                         "AND BANK FRAUD"]):
    d.text((M, LY + 28 + i * 52), line, font=font(SERIF, 48), fill=INK)
y = LY + 28 + 3 * 52
y = para(d, M, y + 6,
         "A US jury convicts the Chinese tech giant of trade secrets and "
         "bank fraud. Racketeering: not guilty.",
         font(SANS, 22), 610, 29)
assert y <= 456, y

# lead illustration: courthouse panel with a GUILTY stamp
IX, IY, IW, IH = 700, LY + 4, 288, 216
d.rectangle([IX, IY, IX + IW, IY + IH], fill=NAVY)
d.polygon([(IX + 20, IY + 52), (IX + IW - 20, IY + 52), (IX + IW // 2, IY + 18)],
          fill=(250, 246, 238))
for i in range(4):
    cx = IX + 44 + i * 68
    d.rectangle([cx, IY + 62, cx + 26, IY + 150], fill=(250, 246, 238))
d.rectangle([IX + 20, IY + 150, IX + IW - 20, IY + 164], fill=(250, 246, 238))
d.rectangle([IX + 20, IY + 176, IX + IW - 20, IY + 196], fill=(250, 246, 238))
stamp = Image.new("RGBA", (260, 70), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([4, 4, 256, 66], outline=(220, 40, 40), width=5)
sd.text((130, 35), "GUILTY", font=font(SANS_B, 44), fill=(220, 40, 40),
        anchor="mm")
stamp = stamp.rotate(-8, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (IX + 14, IY + 96), stamp)
d = ImageDraw.Draw(img)

rule(d, M, 466, R, 2)

# ---------------------------------------------------------------- row 2: two stories
RY = 478
CW = (R - M - 24) // 2


def story2(x, kicker, head, body):
    y = RY
    d.text((x, y), kicker, font=font(SANS_B, 19), fill=RED)
    y = para(d, x, y + 26, head, font(SERIF, 34), CW, 38)
    y = para(d, x, y + 6, body, font(SANS, 22), CW, 27)
    return y


y2 = story2(M, "WAR IN EUROPE",
            "Ukraine strikes Russian ships in the Gulf of Finland and off Libya",
            "Kyiv says its drones hit the cargo ship Sparta II and a second "
            "Russian vessel — widening the war at sea.")
y2b = story2(M + CW + 24, "SPACE  •  NATO",
             "NATO vows to defend space after Russian nuclear satellite reports",
             "Alliance chief Mark Rutte warns the bloc will defend against "
             "any threat in orbit, after reports of a nuclear-armed satellite.")
assert max(y2, y2b) <= 706, (y2, y2b)

rule(d, M, 712, R, 2)

# ---------------------------------------------------------------- row 3: three stories
TY = 732
TW = (R - M - 48) // 3


def story3(x, kicker, head, body):
    y = TY
    d.text((x, y), kicker, font=font(SANS_B, 18), fill=RED)
    y = para(d, x, y + 24, head, font(SERIF, 26), TW, 32)
    y = para(d, x, y + 6, body, font(SANS, 19), TW, 24)
    return y


y3 = story3(M, "HEALTH  •  USA",
            "Measles-free status lost",
            "The US loses its elimination status after 25 years.")
y3b = story3(M + TW + 24, "BUSINESS",
             "Sanofi buys Insmed, $41bn",
             "Biggest biotech deal in nearly three years.")
y3c = story3(M + 2 * (TW + 24), "TURKIYE",
             "Helicopter crash kills five",
             "Air Force helicopter down after take-off from Eskisehir.")
assert max(y3, y3b, y3c) <= 878, (y3, y3b, y3c)

rule(d, M, 890, R, 2)

# ---------------------------------------------------------------- bottom strip
BY = 906
d.rectangle([M, BY, R, BY + 62], fill=INK)
d.text((M + 14, BY + 7), "MARKETS  •  S&P 500 +4.7%  •  Nasdaq +6.5%  —  best day in over a year",
       font=font(SANS_B, 20), fill=(250, 246, 238))
d.text((M + 14, BY + 34), "SPORT  •  Senegal regain the Africa Cup of Nations title after a court appeal",
       font=font(SANS, 20), fill=(250, 246, 238))

# ---------------------------------------------------------------- footer
d.text((W // 2, 982), "Sources: Reuters  •  BBC  •  AP  •  UN News  •  Just Security  —  24 November 2026",
       font=font(SANS, 16), fill=GREY, anchor="ma")

img.save("entry.png", format="PNG")
print("saved entry.png", img.size)
