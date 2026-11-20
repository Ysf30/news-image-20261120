#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Friday 20 November 2026 — as one 1024x1024 PNG.

A newspaper front page: masthead, two lead panels (Cyclone Akvan over a
Bay of Bengal map; the Shenzhen summit aftermath), a day-in-figures band,
33 short stories in three columns, a ticker and a sources footer.
Every story is real news reported on 20 November 2026.
Deterministic: no randomness, no timestamps, fixed fonts.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (13, 116, 128)
GREY = (90, 88, 82)
LIGHT = (232, 226, 212)
RULE = (180, 172, 156)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a list of lines fitting max_w pixels."""
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


def rule(draw, x0, y, x1, weight=1):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=weight)


def tag(draw, x, y, text, colour):
    """Small coloured kicker label; returns width used."""
    fnt = font(SANS_B, 10)
    w = draw.textlength(text, font=fnt) + 10
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=2, fill=colour)
    draw.text((x + 5, y + 2), text, font=fnt, fill=(255, 255, 255))
    return w


def story(draw, x, y, w, kicker, colour, headline, size=12):
    """One numbered-style story block. Returns height used."""
    tag(draw, x, y, kicker, colour)
    fnt = font(SANS_B, size)
    lines = wrap(draw, headline, fnt, w)[:3]
    yy = y + 19
    for ln in lines:
        draw.text((x, yy), ln, font=fnt, fill=INK)
        yy += size + 2
    return yy - y + 4


def draw_cyclone_map(draw, x, y, w, h):
    """Stylised Bay of Bengal: land, sea, cyclone spiral, landfall arrow."""
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1, fill=(214, 232, 240))
    # India east coast landmass (rough polygon, left side)
    land = [(x, y + 8), (x + 140, y + 4), (x + 190, y + 30), (x + 175, y + 70),
            (x + 195, y + 100), (x + 150, y + h - 4), (x, y + h - 4)]
    draw.polygon(land, fill=(238, 226, 196), outline=(150, 135, 105))
    draw.text((x + 8, y + 8), "INDIA", font=font(SANS_B, 11), fill=GREY)
    draw.text((x + 8, y + h - 34), "ODISHA", font=font(SANS_B, 11), fill=INK)
    draw.text((x + 8, y + h - 20), "ANDHRA PRADESH", font=font(SANS_B, 10), fill=INK)
    draw.text((x + 228, y + 8), "BAY OF BENGAL", font=font(SANS_B, 10), fill=BLUE)
    # Cyclone spiral: concentric arcs centred offshore
    cx, cy = x + w - 130, y + 62
    for r, col in [(38, RED), (29, (220, 80, 40)), (20, (240, 140, 40)), (11, RED)]:
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=330,
                 fill=col, width=4)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    # Landfall arrow from eye to coast
    draw.line([(cx - 30, cy + 12), (x + 192, y + 76)], fill=RED, width=3)
    draw.polygon([(x + 192, y + 76), (x + 180, y + 68), (x + 183, y + 82)],
                 fill=RED)
    draw.text((x + 345, y + 6), "AKVAN", font=font(SANS_B, 12), fill=RED)
    draw.text((x + 345, y + 20), "SEVERE STORM", font=font(SANS_B, 9), fill=INK)


def draw_flags(draw, x, y, w, h):
    """Three small flags: USA, China, Russia, side by side."""
    fw, gap = (w - 2 * 10) // 3, 10
    # USA: stripes + blue canton
    fx = x
    for i in range(7):
        draw.rectangle([fx, y + i * h // 7, fx + fw, y + (i + 1) * h // 7],
                       fill=RED if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([fx, y, fx + fw * 2 // 5, y + h * 4 // 7], fill=BLUE)
    # China: red field, yellow stars
    fx = x + fw + gap
    draw.rectangle([fx, y, fx + fw, y + h], fill=(222, 41, 16))
    for sx, sy in [(10, 10), (26, 16), (30, 30), (20, 38), (8, 28)]:
        draw.ellipse([fx + sx, y + sy, fx + sx + 6, y + sy + 6], fill=(255, 222, 0))
    # Russia: white / blue / red horizontal
    fx = x + 2 * (fw + gap)
    for i, col in enumerate([(255, 255, 255), BLUE, RED]):
        draw.rectangle([fx, y + i * h // 3, fx + fw, y + (i + 1) * h // 3], fill=col)
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 26  # side margin

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 82], fill=INK)
    d.text((mx, 8), "THE WORLD TODAY", font=font(SERIF, 46), fill=(247, 242, 231))
    d.text((W - mx - 318, 14), "FRIDAY 20 NOVEMBER 2026", font=font(SANS_B, 17),
           fill=(255, 214, 64))
    d.text((W - mx - 318, 40), "ONE DAY  •  ONE PICTURE  •  35 STORIES",
           font=font(SANS, 12), fill=(200, 196, 186))
    d.text((mx, 60), "The world in a single page — what happened, where, and why it matters.",
           font=font(SERIF_R, 13), fill=(200, 196, 186))

    # ---- Lead zone ------------------------------------------------------
    ly, lh = 92, 208
    # Left: cyclone panel (620 wide)
    d.rectangle([mx, ly, mx + 620, ly + lh], outline=RULE, width=1, fill=(255, 255, 255))
    tag(d, mx + 10, ly + 8, "LEAD  •  CLIMATE", RED)
    d.text((mx + 10, ly + 28), "Akvan bears down on India",
           font=font(SERIF, 27), fill=INK)
    d.text((mx + 10, ly + 62),
           "80,000 evacuated as severe storm nears Odisha coast",
           font=font(SANS_B, 13), fill=INK)
    draw_cyclone_map(d, mx + 10, ly + 88, 600, 104)
    # Right: summit panel (332 wide)
    rx = mx + 620 + 14
    rw = W - mx - rx
    d.rectangle([rx, ly, rx + rw, ly + lh], outline=RULE, width=1, fill=(255, 255, 255))
    tag(d, rx + 10, ly + 8, "AFTER SHENZHEN", BLUE)
    draw_flags(d, rx + 10, ly + 30, rw - 20, 44)
    d.text((rx + 10, ly + 84), "Trump, Xi and Putin sign",
           font=font(SERIF, 20), fill=INK)
    d.text((rx + 10, ly + 110), "\u201cPeace Declaration\u201d",
           font=font(SERIF, 20), fill=INK)
    yy = ly + 140
    for ln in wrap(d, "First-ever trilateral talks: nuclear-risk dialogue and "
                    "more oil output — but no Ukraine breakthrough.",
                   font(SANS, 12), rw - 20):
        d.text((rx + 10, yy), ln, font=font(SANS, 12), fill=INK)
        yy += 15
    d.text((rx + 10, ly + 186), "90 MINUTES  •  BERLIN RESPONDS TODAY",
           font=font(SANS_B, 10), fill=RED)

    # ---- Day in figures --------------------------------------------------
    fy = 312
    d.rectangle([mx, fy, W - mx, fy + 52], fill=LIGHT, outline=RULE)
    figures = [("80,000", "evacuated"), ("9–6", "ICJ genocide vote"),
               ("51–48", "US Senate vote"), ("2,500+", "Iran missiles"),
               ("€45bn", "EU Ukraine loan"), ("$1.5tn", "Anthropic value")]
    fw = (W - 2 * mx) // 6
    for i, (num, label) in enumerate(figures):
        cx = mx + i * fw + fw // 2
        nw = d.textlength(num, font=font(SANS_B, 19))
        d.text((cx - nw // 2, fy + 6), num, font=font(SANS_B, 19), fill=RED)
        lw = d.textlength(label, font=font(SANS, 11))
        d.text((cx - lw // 2, fy + 30), label, font=font(SANS, 11), fill=INK)
        if i:
            d.line([(mx + i * fw, fy + 8), (mx + i * fw, fy + 44)], fill=RULE)

    # ---- Three columns of stories ---------------------------------------
    cols = [
        [("WORLD", BLUE, "Europe's leaders in Berlin call for a winter energy ceasefire in Ukraine"),
         ("WORLD", BLUE, "Trump says he will meet Kim Jong-un \u201cat some point\u201d"),
         ("WORLD", BLUE, "US and Venezuela sign deal to restore military cooperation"),
         ("WORLD", BLUE, "South Korea court overturns ex-PM Han Duck-soo's martial-law conviction"),
         ("WORLD", BLUE, "Fiji declares a national disaster as El Ni\u00f1o drought empties reservoirs"),
         ("WORLD", BLUE, "Australia sanctions Israeli settlers over West Bank expansion"),
         ("WORLD", BLUE, "Japan PM Takaichi seeks continued dialogue to ease China tensions"),
         ("WORLD", BLUE, "Pakistan minister to lead delegation to Delhi for SCO dialogue forum"),
         ("WORLD", BLUE, "Modi meets Prince and Princess of Wales in New Delhi"),
         ("WORLD", BLUE, "Modi opens FICCI centenary, pitches India growth to 2047"),
         ("WORLD", BLUE, "APEC adopts Shenzhen Outlook on trade, data and AI risks")],
        [("JUSTICE", RED, "World court: Myanmar committed genocide against Rohingya, 9–6"),
         ("WAR", RED, "US Senate rejects Iran war-powers resolution, 51–48"),
         ("WAR", RED, "Iran still holds 2,500+ missiles after nine-month war, US intel says"),
         ("WAR", RED, "Tanker struck in Strait of Hormuz; crew safe, one missing"),
         ("WAR", RED, "Israeli tanks cross Gaza ceasefire line in rare operation"),
         ("WAR", RED, "Gaza peace plan scores 4 of 26, five aid groups say"),
         ("WAR", RED, "Ukraine strike disrupts rail traffic on Crimea bridge"),
         ("WAR", RED, "North Korea expanding Yongbyon uranium plant, UN watchdog says"),
         ("EUROPE", TEAL, "EU proposes \u20ac45bn Ukraine loan for 2027"),
         ("EUROPE", TEAL, "UK and Norway fund \u00a3100m+ for two Ukrainian naval craft"),
         ("CLIMATE", TEAL, "COP31 AI pledge fails to win big US tech firms")],
        [("MARKETS", TEAL, "Sensex +1.21%, Nifty +1.14% in Thursday rally"),
         ("TECH", TEAL, "Anthropic valuation reportedly hits $1.5 trillion"),
         ("TECH", TEAL, "Nvidia chief's affair shadows APEC chip talks"),
         ("WORLD", BLUE, "LPG tanker that sank off Bulgaria was hit by projectiles"),
         ("INDIA", BLUE, "Fire at ancestral home of Bangladesh leader Muhammad Yunus"),
         ("SPORT", RED, "Nicholls' 113* rescues NZ at 243/5 on day one vs India"),
         ("SPORT", RED, "India beat Malaysia in Hong Kong Open badminton"),
         ("SPORT", RED, "Women's Asian Hockey Champions Trophy begins"),
         ("CULTURE", TEAL, "IFFI 2026 adds animation section with five world films"),
         ("INDIA", BLUE, "UP Police release constable exam normalised scores"),
         ("WEATHER", TEAL, "Saudi Arabia warns of thunderstorms through Tuesday")],
    ]
    cy0, cy1 = 378, 962
    col_w = (W - 2 * mx - 2 * 16) // 3
    for ci, stories in enumerate(cols):
        x = mx + ci * (col_w + 16)
        y = cy0
        for kicker, colour, headline in stories:
            used = story(d, x, y, col_w, kicker, colour, headline)
            y += used
            rule(d, x, y - 2, x + col_w)
        if ci < 2:
            d.line([(x + col_w + 8, cy0), (x + col_w + 8, cy1)], fill=RULE)

    # ---- Ticker + footer --------------------------------------------------
    d.rectangle([0, 972, W, 998], fill=INK)
    d.text((mx, 979), "TRUMP TO HOLD WHITE HOUSE PRESS CONFERENCE ON RETURN  •  CRUDE FUTURES DOWN 3%  •  SENSEX RALLY  •  GAZA RAINS HIT 46,000 HOUSEHOLDS",
           font=font(SANS_B, 11), fill=(255, 214, 64))
    d.text((mx, 1006), "Sources: NYT · BBC · Reuters · AP · Al Jazeera · IMD · ICJ · APEC  —  all stories reported on Friday 20 November 2026.",
           font=font(SANS, 10), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
