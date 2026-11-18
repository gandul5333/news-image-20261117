#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a newspaper front page summing up
Tuesday 17 November 2026's world news in one 1024x1024 image.

Stories (all reported on 17 Nov 2026, cross-checked across several outlets):
  1. Ukraine strike collapses a span of the Kerch Bridge to Crimea; Russia
     hits Kyiv's river bridges in reply.
  2. Tankers hit by mines near the Strait of Hormuz catch fire; a third
     US carrier arrives in the region.
  3. Trump, Xi and Putin confirmed to meet in Shenzhen on Thursday at APEC.
  4. ULA Vulcan rocket fails in flight, destroying 40 Amazon Leo satellites.
  5. A JPMorgan Chase software bug disrupts online banking and Zelle.
  Also: five European states plan a Rwanda return hub for rejected asylum
  seekers.

The script is deterministic (fixed geometry, fixed fonts, no randomness) and
writes entry.png next to itself. Run: python3 draw_image.py
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (22, 22, 22)
NAVY = (20, 33, 61)
RED = (178, 32, 44)
GOLD = (201, 162, 39)
SKY = (214, 230, 242)
SEA = (46, 90, 128)
GREY = (90, 96, 104)
LIGHT = (236, 232, 220)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans-Bold.ttf", s)
F_TEXT = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
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


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    """Draw wrapped text, return the y just below the last line."""
    leading = leading or int(fnt.size * 1.18)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def panel(draw, box, tag, tag_color=RED):
    """A white panel with a thin ink border and a small red kicker tag."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=INK, width=2)
    return (x0, y0, x1, y1)


def kicker(draw, x, y, text, size=17):
    f = F_SANS(size)
    w = draw.textlength(text, font=f) + 16
    draw.rectangle([x, y, x + w, y + size + 10], fill=RED)
    draw.text((x + 8, y + 5), text, font=f, fill=(255, 255, 255))
    return y + size + 12


# ------------------------------------------------------------------ scenes

def draw_bridge(draw, box):
    """Kerch Bridge: deck with a collapsed middle span, smoke, sea."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    # sun glow
    draw.ellipse([x1 - 150, y0 + 8, x1 - 70, y0 + 88], fill=(245, 201, 138))
    # sea
    draw.rectangle([x0, y0 + 122, x1, y1], fill=SEA)
    for i in range(5):
        yy = y0 + 138 + i * 8
        draw.line([(x0 + 12 + i * 37, yy), (x0 + 90 + i * 37, yy)],
                  fill=(120, 165, 200), width=3)
    # bridge deck: left segment, gap, right segment
    deck_y = y0 + 96
    draw.rectangle([x0, deck_y, x0 + 300, deck_y + 14], fill=(70, 74, 80))
    draw.rectangle([x0 + 430, deck_y, x1, deck_y + 14], fill=(70, 74, 80))
    # fallen span, tilted into the water
    draw.polygon([(x0 + 310, deck_y + 6), (x0 + 420, deck_y + 30),
                  (x0 + 400, deck_y + 46), (x0 + 305, deck_y + 22)],
                 fill=(52, 56, 62))
    # pylons
    for px in (x0 + 60, x0 + 210, x0 + 500, x0 + 660):
        draw.rectangle([px, y0 + 30, px + 12, deck_y], fill=(52, 56, 62))
        draw.rectangle([px - 8, y0 + 22, px + 20, y0 + 32], fill=(52, 56, 62))
    # cables
    for px, top in ((x0 + 66, y0 + 32), (x0 + 216, y0 + 32),
                    (x0 + 506, y0 + 32), (x0 + 666, y0 + 32)):
        draw.line([(px, top), (px - 60, deck_y)], fill=(120, 126, 132), width=2)
        draw.line([(px, top), (px + 60, deck_y)], fill=(120, 126, 132), width=2)
    # explosion burst at the gap
    cx, cy = x0 + 365, deck_y - 6
    for ang, r in ((0, 46), (45, 38), (90, 48), (135, 36), (180, 44),
                   (225, 37), (270, 47), (315, 39)):
        import math
        ex = cx + int(r * math.cos(math.radians(ang)))
        ey = cy + int(r * math.sin(math.radians(ang)))
        draw.line([(cx, cy), (ex, ey)], fill=(255, 140, 40), width=7)
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(255, 190, 60))
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 240, 180))
    # smoke plumes
    for sx, sy, sr in ((x0 + 330, y0 + 42, 26), (x0 + 360, y0 + 18, 32),
                       (x0 + 400, y0 + 44, 24)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 112, 116))
        draw.ellipse([sx - sr + 8, sy - sr + 6, sx + sr - 4, sy + sr - 8],
                     fill=(140, 142, 146))


def draw_tanker(draw, box):
    """Oil tanker on fire near the Strait of Hormuz."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(226, 214, 180))
    draw.rectangle([x0, y0 + 120, x1, y1], fill=(38, 74, 104))
    # tanker hull
    draw.polygon([(x0 + 30, y0 + 88), (x0 + 300, y0 + 88),
                  (x0 + 320, y0 + 130), (x0 + 10, y0 + 130)],
                 fill=(140, 30, 30))
    draw.rectangle([x0 + 30, y0 + 78, x0 + 300, y0 + 90], fill=(60, 60, 60))
    # superstructure
    draw.rectangle([x0 + 235, y0 + 34, x0 + 295, y0 + 80], fill=(240, 240, 235))
    draw.rectangle([x0 + 245, y0 + 22, x0 + 285, y0 + 36], fill=(200, 60, 40))
    # one flame rising from the deck, mid-ship
    fx = x0 + 140
    draw.polygon([(fx - 26, y0 + 82), (fx - 8, y0 + 34), (fx + 4, y0 + 52),
                  (fx + 22, y0 + 30), (fx + 28, y0 + 82)], fill=(255, 120, 30))
    draw.ellipse([fx - 14, y0 + 48, fx + 14, y0 + 82], fill=(255, 180, 50))
    draw.ellipse([fx - 7, y0 + 60, fx + 7, y0 + 82], fill=(255, 230, 120))
    # smoke
    for sx, sy, sr in ((x0 + 140, y0 + 14, 18), (x0 + 168, y0 + 6, 20)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(70, 70, 72))
    # naval mine in the water
    mx, my = x0 + 355, y0 + 138
    draw.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=(30, 30, 30))
    for ang in range(0, 360, 45):
        ex = mx + int(20 * math.cos(math.radians(ang)))
        ey = my + int(20 * math.sin(math.radians(ang)))
        draw.line([(mx, my), (ex, ey)], fill=(30, 30, 30), width=4)
    # waves
    for i in range(3):
        yy = y0 + 132 + i * 7
        draw.line([(x0 + 10 + i * 20, yy), (x0 + 70 + i * 20, yy)],
                  fill=(120, 165, 200), width=3)


def draw_summit(draw, box):
    """Three flags (US, China, Russia) over a Shenzhen skyline."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(200, 220, 235))
    # skyline
    heights = [70, 110, 85, 130, 95, 120, 78]
    bw = (x1 - x0) // len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + i * bw + 6
        draw.rectangle([bx, y1 - 34 - hh, bx + bw - 12, y1 - 34],
                       fill=(52, 68, 92))
        for wy in range(y1 - 34 - hh + 10, y1 - 44, 18):
            draw.rectangle([bx + 6, wy, bx + 12, wy + 8], fill=(255, 220, 120))
    draw.rectangle([x0, y1 - 34, x1, y1], fill=(30, 42, 64))
    # flags on poles
    flags = [
        ("US", [(200, 30, 40), (255, 255, 255), (200, 30, 40), (255, 255, 255),
                (200, 30, 40), (255, 255, 255), (200, 30, 40)]),
        ("CN", [(222, 41, 16)]),
        ("RU", [(255, 255, 255), (0, 57, 166), (213, 0, 50)]),
    ]
    fw, fh = 92, 58
    total = 3 * fw + 2 * 40
    fx = x0 + (x1 - x0 - total) // 2
    fy = y0 + 18
    for name, stripes in flags:
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
        sh = fh // len(stripes)
        for j, col in enumerate(stripes):
            draw.rectangle([fx, fy + j * sh, fx + fw, fy + (j + 1) * sh],
                           fill=col)
        if name == "US":
            draw.rectangle([fx, fy, fx + 38, fy + 28], fill=(30, 40, 90))
            for sx in range(3):
                for sy in range(2):
                    draw.ellipse([fx + 6 + sx * 12, fy + 6 + sy * 11,
                                  fx + 10 + sx * 12, fy + 10 + sy * 11],
                                 fill=(255, 255, 255))
        if name == "CN":
            draw.ellipse([fx + 12, fy + 10, fx + 26, fy + 24], fill=(255, 222, 0))
            for dx, dy in ((30, 8), (34, 18), (28, 26)):
                draw.ellipse([fx + dx, fy + dy, fx + dx + 7, fy + dy + 7],
                             fill=(255, 222, 0))
        draw.line([(fx + fw // 2, fy + fh), (fx + fw // 2, fy + fh + 26)],
                  fill=(70, 70, 70), width=4)
        fx += fw + 40


def draw_rocket(draw, box):
    """Vulcan rocket failing: tilted rocket, explosion, falling satellites."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(18, 26, 48))
    # stars
    import math
    for sx, sy in ((x0 + 30, y0 + 20), (x0 + 90, y0 + 50), (x0 + 300, y0 + 18),
                   (x0 + 350, y0 + 60), (x0 + 200, y0 + 12), (x0 + 40, y0 + 90)):
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # smoke trail
    for i, (sx, sy, sr) in enumerate(((x0 + 118, y0 + 88, 18),
                                      (x0 + 100, y0 + 100, 20),
                                      (x0 + 82, y0 + 104, 12))):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(180, 180, 185))
    # rocket body, tilted
    cx, cy = x0 + 190, y0 + 52
    draw.polygon([(cx - 14, cy + 40), (cx - 14, cy - 30), (cx, cy - 52),
                  (cx + 14, cy - 30), (cx + 14, cy + 40)], fill=(235, 235, 230))
    draw.polygon([(cx - 14, cy - 30), (cx, cy - 52), (cx + 14, cy - 30)],
                 fill=(200, 50, 40))
    draw.rectangle([cx - 14, cy + 8, cx + 14, cy + 22], fill=(40, 90, 160))
    draw.polygon([(cx - 14, cy + 40), (cx - 30, cy + 58), (cx - 14, cy + 48)],
                 fill=(200, 50, 40))
    draw.polygon([(cx + 14, cy + 40), (cx + 30, cy + 58), (cx + 14, cy + 48)],
                 fill=(200, 50, 40))
    # explosion burst at the base
    ex, ey = cx, cy + 42
    for ang in range(0, 360, 30):
        r = 22 if ang % 60 == 0 else 15
        px = ex + int(r * math.cos(math.radians(ang)))
        py = ey + int(r * math.sin(math.radians(ang)))
        draw.line([(ex, ey), (px, py)], fill=(255, 140, 40), width=5)
    draw.ellipse([ex - 13, ey - 13, ex + 13, ey + 13], fill=(255, 190, 60))
    # falling satellites
    for sx, sy in ((x0 + 310, y0 + 60), (x0 + 335, y0 + 88), (x0 + 285, y0 + 100)):
        draw.rectangle([sx - 8, sy - 4, sx + 8, sy + 4], fill=(255, 255, 255),
                       outline=(150, 150, 150))
        draw.rectangle([sx - 16, sy - 2, sx - 8, sy + 2], fill=(60, 120, 220))
        draw.rectangle([sx + 8, sy - 2, sx + 16, sy + 2], fill=(60, 120, 220))


def draw_bank(draw, box):
    """Bank facade with a phone showing a failed payment."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 226, 210))
    # bank building
    bx0, bx1 = x0 + 18, x0 + 210
    draw.rectangle([bx0, y0 + 44, bx1, y1 - 8], fill=(245, 243, 236),
                   outline=INK, width=2)
    draw.polygon([(bx0 - 8, y0 + 46), (bx0 + 96, y0 + 14), (bx1 + 8, y0 + 46)],
                 fill=(150, 40, 40))
    for i in range(4):
        cx = bx0 + 24 + i * 46
        draw.rectangle([cx, y0 + 60, cx + 16, y1 - 8], fill=(210, 205, 190))
    draw.rectangle([bx0 + 70, y1 - 52, bx0 + 122, y1 - 8], fill=(60, 60, 60))
    # phone
    px0, py0, px1, py1 = x0 + 238, y0 + 12, x0 + 330, y1 - 8
    draw.rounded_rectangle([px0, py0, px1, py1], radius=14, fill=(24, 24, 28),
                           outline=INK, width=2)
    draw.rounded_rectangle([px0 + 8, py0 + 12, px1 - 8, py1 - 12], radius=8,
                           fill=(255, 255, 255))
    # red error circle with exclamation mark
    ccx, ccy = (px0 + px1) // 2, py0 + 36
    draw.ellipse([ccx - 20, ccy - 20, ccx + 20, ccy + 20], fill=(200, 30, 40))
    draw.rectangle([ccx - 3, ccy - 11, ccx + 3, ccy + 5], fill=(255, 255, 255))
    draw.ellipse([ccx - 3, ccy + 8, ccx + 3, ccy + 14], fill=(255, 255, 255))
    f = F_SANS(18)
    draw.text(((px0 + px1) // 2 - draw.textlength("Zelle", font=f) // 2,
               py0 + 64), "Zelle", font=f, fill=INK)


# ------------------------------------------------------------------ page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    f_title = F_SERIF(58)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_title)) // 2, 14), title,
           font=f_title, fill=(255, 255, 255))
    f_date = F_SANS(30)
    date = "TUESDAY  17  NOVEMBER  2026"
    d.text(((W - d.textlength(date, font=f_date)) // 2, 76), date,
           font=f_date, fill=(240, 200, 90))

    M = 24  # outer margin

    # ---- hero: Kerch Bridge ----
    hero = (M, 134, W - M, 432)
    panel(d, hero, "UKRAINE")
    draw_bridge(d, (hero[0] + 2, hero[1] + 2, hero[2] - 2, hero[1] + 150))
    y = kicker(d, hero[0] + 14, hero[1] + 160, "WAR IN EUROPE")
    y = text_block(d, hero[0] + 14, y, "UKRAINE STRIKE COLLAPSES SPAN OF CRIMEA BRIDGE",
                   F_SANS(30), INK, hero[2] - hero[0] - 28, leading=34)
    text_block(d, hero[0] + 14, y + 2,
               "Second attack in 24 hours \u2014 as Russia hits Kyiv's bridges.",
               F_TEXT(20), (60, 60, 60), hero[2] - hero[0] - 28, leading=24)

    # ---- middle row: Hormuz / summit ----
    row2_y0, row2_y1 = 438, 700
    half = (W - 3 * M) // 2
    left = (M, row2_y0, M + half, row2_y1)
    right = (M + half + M, row2_y0, W - M, row2_y1)
    for box, scene, tag, head, sub in (
            (left, draw_tanker, "MIDDLE EAST",
             "TANKERS HIT BY MINES NEAR HORMUZ",
             "Two tankers burn; a third US carrier arrives."),
            (right, draw_summit, "DIPLOMACY",
             "TRUMP, XI AND PUTIN TO MEET IN SHENZHEN",
             "Three-way talks set for Thursday at APEC.")):
        panel(d, box, tag)
        scene(d, (box[0] + 2, box[1] + 2, box[2] - 2, box[1] + 140))
        y = kicker(d, box[0] + 12, box[1] + 150, tag, size=15)
        y = text_block(d, box[0] + 12, y, head, F_SANS(24), INK,
                       box[2] - box[0] - 24, leading=28)
        text_block(d, box[0] + 12, y + 2, sub, F_TEXT(17), (60, 60, 60),
                   box[2] - box[0] - 24, leading=21)

    # ---- bottom row: rocket / bank outage ----
    row3_y0, row3_y1 = 714, 962
    left3 = (M, row3_y0, M + half, row3_y1)
    right3 = (M + half + M, row3_y0, W - M, row3_y1)
    for box, scene, tag, head, sub in (
            (left3, draw_rocket, "SPACE",
             "VULCAN ROCKET FAILS \u2014 40 AMAZON SATELLITES LOST",
             "ULA rocket fails minutes after launch."),
            (right3, draw_bank, "BUSINESS",
             "JPMORGAN BUG HITS BANKING AND ZELLE",
             "A software bug, not a cyberattack.")):
        panel(d, box, tag)
        scene(d, (box[0] + 2, box[1] + 2, box[2] - 2, box[1] + 116))
        y = kicker(d, box[0] + 12, box[1] + 126, tag, size=15)
        y = text_block(d, box[0] + 12, y, head, F_SANS(23), INK,
                       box[2] - box[0] - 24, leading=27)
        text_block(d, box[0] + 12, y + 2, sub, F_TEXT(17), (60, 60, 60),
                   box[2] - box[0] - 24, leading=21)

    # ---- footer strip ----
    f_foot = F_TEXT(19)
    foot = ("ALSO:  Five European states plan a Rwanda return hub for rejected "
            "asylum seekers  \u00b7  17 NOVEMBER 2026")
    d.text(((W - d.textlength(foot, font=f_foot)) // 2, 976), foot,
           font=f_foot, fill=(60, 60, 60))

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
