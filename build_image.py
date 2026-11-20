#!/usr/bin/env python3
"""Draw the news-image-20261120 front page, fresh in this session.

One 1024x1024 PNG, "THE WORLD IN ONE PAGE", Friday 20 November 2026.
Pillow only, DejaVu fonts from the system, no network, no photos:
everything on the page is drawn with rectangles, circles and text.

Layout, top to bottom:
  navy masthead -> two lead stories (Akvan / Shenzhen) -> a red
  ICJ banner -> three columns of short stories -> a black footer
  with the day in figures and the sources.
All 30 headline stories were checked against live reporting in
this session (search, 20 Nov 2026, ~10:20 WIB): the cyclone, the
trilateral summit, the ICJ verdict, Kyiv, Hormuz, Anthropic,
Voyager 1 and the rest below.
"""
import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

NAVY = (15, 42, 68)
NAVY2 = (21, 58, 90)
RED = (178, 34, 34)
DARKRED = (122, 31, 31)
TEAL = (0, 128, 128)
GOLD = (198, 142, 0)
INK = (24, 24, 24)
GREY = (90, 90, 90)
LIGHT = (242, 242, 236)
PAPER = (255, 255, 253)
RULE = (200, 200, 190)


def font(name, size):
    for cand in (
        f"/usr/share/fonts/truetype/dejavu/DejaVu{name}.ttf",
        f"/usr/share/fonts/dejavu/DejaVu{name}.ttf",
    ):
        p = Path(cand)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


F_TITLE = font("Sans-Bold", 46)
F_DATE = font("Sans", 17)
F_LEAD_H = font("Sans-Bold", 24)
F_LEAD_B = font("Sans", 15)
F_BANNER_H = font("Sans-Bold", 25)
F_BANNER_B = font("Sans", 14)
F_KICK = font("Sans-Bold", 11)
F_HEAD = font("Sans-Bold", 13)
F_DECK = font("Sans", 11)
F_FOOT = font("Sans", 13)
F_FOOT_B = font("Sans-Bold", 13)
F_NUM = font("Sans-Bold", 15)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_spiral(draw, cx, cy, colour):
    """A hand-drawn cyclone: an Archimedean spiral plus rain bands."""
    pts = []
    for t in range(0, 720, 6):
        r = 4 + 0.075 * t
        a = math.radians(t)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.82))
    draw.line(pts, fill=colour, width=4)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=colour)
    for k, (dx, dy) in enumerate(((-58, -34), (52, -40), (-64, 30), (58, 34))):
        draw.line([(cx + dx, cy + dy), (cx + dx + 26, cy + dy + 8)],
                  fill=colour, width=3)
        if k % 2 == 0:
            draw.line([(cx + dx + 6, cy + dy + 14), (cx + dx + 30, cy + dy + 20)],
                      fill=colour, width=2)


def one_line(draw, text, fnt, width):
    """Truncate to a single line with an ellipsis if it would wrap."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    words = text.split()
    out = ""
    for word in words:
        trial = f"{out} {word}".strip()
        if draw.textlength(trial + "...", font=fnt) <= width:
            out = trial
        else:
            break
    return out + "..."


def lead_box(draw, x, y, w, h, kick, colour, title, body, art):
    # Text lives in the left part of the box; the art owns the right
    # 130 px, so nothing can ever overlap it.
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           outline=RULE, width=1, fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + 30], fill=colour)
    draw.text((x + 12, y + 7), kick, font=F_KICK, fill=(255, 255, 255))
    tx, tw = x + 12, w - 152
    if art == "spiral":
        draw_spiral(draw, x + w - 66, y + 105, TEAL)
    else:
        for i, (label, col) in enumerate(
                (("US", (178, 34, 34)), ("CN", (198, 142, 0)), ("RU", (15, 42, 68)))):
            cx = x + w - 138 + i * 46
            draw.ellipse([cx, y + 62, cx + 40, y + 102], fill=col,
                         outline=(255, 255, 255), width=2)
            twd = draw.textlength(label, font=F_KICK)
            draw.text((cx + 20 - twd / 2, y + 76), label,
                      font=F_KICK, fill=(255, 255, 255))
    lines = wrap(draw, title, F_LEAD_H, tw)
    yy = y + 38
    for ln in lines[:2]:
        draw.text((tx, yy), ln, font=F_LEAD_H, fill=INK)
        yy += 28
    for ln in wrap(draw, body, F_LEAD_B, tw)[:4]:
        draw.text((tx, yy), ln, font=F_LEAD_B, fill=(60, 60, 60))
        yy += 19


# --- the 27 short stories: (section, headline, one-line deck) ---
SHORTS = [
    ("KYIV", "Four ballistic missiles hit Kyiv",
     "Ukraine's capital struck as the war grinds on."),
    ("CRIMEA", "Bridge struck for third time in four days",
     "Kyiv hits the crossing again; Putin vows a harsher reply."),
    ("BERLIN", "Allies say they are ready for talks with Russia",
     "European leaders agree a united position in Berlin."),
    ("RIYADH", "Houthi missile hits the capital's tallest tower",
     "Yemen's Houthis claim strikes on four Saudi targets."),
    ("HORMUZ", "Tanker burns after hitting a mine",
     "Iran widens Gulf attacks; IEA warns of energy threat."),
    ("GAZA", "Allies urge aid access as floods hit Gaza",
     "Four allies press Israel to open Gaza up."),
    ("WASHINGTON", "Senate rejects Iran war-powers bid, 51-48",
     "Three Republicans backed it; one Democrat opposed."),
    ("MARKETS", "Anthropic up 17% on record Nasdaq debut",
     "Shares close near $97 after pricing at $83 a share."),
    ("MARKETS", "S&P 500 falls 2.0%, a fifth loss in a row",
     "Wall Street slides even as Anthropic's debut soars."),
    ("CALIFORNIA", "Nvidia faces state probe after Huang exit",
     "California queries China chip risks and disclosures."),
    ("SPACE", "Voyager 1 is a light-day away: 25.9bn km",
     "A radio signal now takes a full day to reach Earth."),
    ("GENOA", "Airport halts flights after drone sightings",
     "Unidentified drones force a suspension in northern Italy."),
    ("SARATOV", "Three killed in drone attack in Russia",
     "A strike on the Saratov region is reported overnight."),
    ("FRANCE", "One dead, 15 hurt in tower-block fire",
     "A blaze hits an 18-storey apartment building."),
    ("TBILISI", "Girl, 3, pulled alive after 8 hours in rubble",
     "Rescuers free a child after a gas explosion in Georgia."),
    ("HAITI", "Police say 34 gang suspects killed in raid",
     "Officers report an offensive in Martissant, Port-au-Prince."),
    ("SENEGAL", "Migrant boat sinks; dozens missing",
     "Another deadly crossing is reported off West Africa."),
    ("COPENHAGEN", "Denmark backs Greenland defence deal, 109-0",
     "The pact expands the US military presence there."),
    ("SHENZHEN", "APEC adopts outlook on trade, data and AI",
     "Leaders agree a shared economic and digital agenda."),
    ("CLIMATE", "Fossil-fuel mention dropped from COP31 draft",
     "The latest agreement text omits the reference entirely."),
    ("ENERGY", "Data-centre power may double by 2030: IEA",
     "Grids face strain as AI demand keeps climbing."),
    ("FAITH", "Muslims set to be the largest faith by 2035",
     "Pew projects the shift; Christianity also keeps growing."),
    ("BRAZIL", "Lula to decree a five-day working week",
     "Brazil moves to shorten the working week by decree."),
    ("ECONOMY", "IMF: AI demand to push interest rates up",
     "The Fund chief warns of pressure on borrowing costs."),
    ("PARAGUAY", "Ueno bank collapse may cost $1bn",
     "The central bank chief puts a figure on the failure."),
    ("SPORT", "LA Sparks near record $750m WNBA sale",
     "A deal would set a new high for women's basketball."),
    ("SPORT", "New Zealand pile up 317-6 against India",
     "The tourists dominate day one with the bat in hand."),
]

KICK_COLOURS = {
    "KYIV": RED, "CRIMEA": RED, "BERLIN": NAVY2, "RIYADH": RED,
    "HORMUZ": RED, "GAZA": RED, "WASHINGTON": NAVY2, "MARKETS": TEAL,
    "CALIFORNIA": TEAL, "SPACE": TEAL, "GENOA": GOLD, "SARATOV": RED,
    "FRANCE": NAVY2, "TBILISI": GOLD, "HAITI": RED, "SENEGAL": GOLD,
    "COPENHAGEN": NAVY2, "SHENZHEN": NAVY2, "CLIMATE": TEAL,
    "ENERGY": TEAL, "FAITH": GOLD, "BRAZIL": NAVY2, "ECONOMY": TEAL,
    "PARAGUAY": TEAL, "SPORT": GOLD,
}


def draw_columns(draw):
    col_w = 314
    xs = [24, 354, 684]
    top = 370
    per = 9
    for ci in range(3):
        x = xs[ci]
        y = top
        for section, head, deck in SHORTS[ci * per:(ci + 1) * per]:
            draw.text((x, y), section, font=F_KICK,
                      fill=KICK_COLOURS.get(section, NAVY2))
            y += 13
            for ln in wrap(draw, head, F_HEAD, col_w)[:2]:
                draw.text((x, y), ln, font=F_HEAD, fill=INK)
                y += 16
            # Decks are always exactly one line, truncated, so every
            # item costs the same height and the last row cannot run
            # into the footer.
            draw.text((x, y), one_line(draw, deck, F_DECK, col_w),
                      font=F_DECK, fill=GREY)
            y += 15
            y += 6
            draw.line([(x, y), (x + col_w, y)], fill=RULE, width=1)
            y += 7
        if ci < 2:
            draw.line([(x + col_w + 8, top), (x + col_w + 8, 960)],
                      fill=RULE, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 86], fill=NAVY)
    d.rectangle([0, 86, W, 90], fill=RED)
    d.text((24, 14), "THE WORLD IN ONE PAGE", font=F_TITLE, fill=(255, 255, 255))
    d.text((24, 62), "FRIDAY 20 NOVEMBER 2026  |  ONE DAY, THIRTY STORIES, ONE IMAGE",
           font=F_DATE, fill=(200, 220, 235))
    # Leads
    lead_box(d, 24, 102, 484, 190, "WEATHER  •  INDIA",
             TEAL, "Akvan comes ashore",
             "Cyclone Akvan crosses near Gopalpur at noon, winds "
             "90-100 km/h gusting to 110. Odisha has moved 72,000 "
             "people to safety; the third cyclone in a month.",
             "spiral")
    lead_box(d, 516, 102, 484, 190, "DIPLOMACY  •  SHENZHEN",
             NAVY2, "Three leaders, one declaration",
             "Trump, Xi and Putin meet for 90 minutes and issue a "
             "four-point peace declaration: a nuclear war cannot "
             "be won and must never be fought. Ukraine and Iran "
             "go unmentioned.",
             "flags")
    # ICJ banner
    d.rounded_rectangle([24, 304, 1000, 358], radius=10, fill=DARKRED)
    d.text((44, 312), "9-6", font=font("Sans-Bold", 38), fill=(255, 220, 120))
    d.text((128, 312), "The Hague: Myanmar committed genocide",
           font=F_BANNER_H, fill=(255, 255, 255))
    d.text((128, 338), "The world court rules 9-6 on the 2017 campaign against the Rohingya — the first state "
           "ever found guilty of genocide.",
           font=F_BANNER_B, fill=(240, 220, 220))
    # Columns
    draw_columns(d)
    # Footer
    d.rectangle([0, 972, W, H], fill=(12, 12, 12))
    d.text((24, 980),
           "THE DAY IN FIGURES:  72,000 evacuated  •  90-100 km/h winds  •  Anthropic +17%  •  "
           "Voyager 25.9bn km  •  S&P -2.0%",
           font=F_FOOT_B, fill=(255, 220, 120))
    d.text((24, 1000),
           "Also: Pete Rose pardoned  •  North Korea expands Yongbyon  •  UK & Norway fund Ukrainian naval craft  •  "
           "Sources: Reuters, BBC, IMD, ICJ, NASA, AP",
           font=F_FOOT, fill=(220, 220, 220))
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
