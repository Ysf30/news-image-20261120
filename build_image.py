#!/usr/bin/env python3
"""Render the 20 November 2026 front page to entry.png (1024x1024).

My own layout, drawn fresh in this session: masthead, two lead panels
with a drawn Bay of Bengal cyclone chart and a three-leader panel,
an ICJ strip, a figures strip, four columns of short stories, a
ticker and a sources footer. All headlines are my own wording from
live news research done in this session.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (24, 48, 96)
TEAL = (14, 90, 86)
GREY = (90, 88, 80)
RULE = (60, 58, 50)

F = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=15):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline_block(draw, x, y, width, kick, head, deck, head_size=12):
    y = para(draw, x, y, width, head, SERIF_B(head_size), leading=head_size + 2)
    y = para(draw, x, y + 1, width, deck, SANS(10), fill=(52, 50, 44), leading=13)
    return y + 6


canvas = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(canvas)
d.rectangle([0, 0, W - 1, H - 1], outline=RULE, width=3)

# ---- masthead ----
d.rectangle([14, 12, W - 14, 108], fill=(24, 24, 24))
d.text((512, 26), "THE WORLD TODAY", font=SERIF_B(52), fill=(247, 243, 232),
       anchor="ma")
d.text((512, 82), "FRIDAY 20 NOVEMBER 2026  •  ONE DAY IN ONE IMAGE",
       font=SANS_B(15), fill=(232, 196, 90), anchor="ma")

# ---- lead row: cyclone chart (left) + trilateral (right) ----
LY, LH = 118, 252
d.rectangle([14, LY, 618, LY + LH], outline=INK, width=2)
d.text((22, LY + 8), "LEAD  •  INDIA", font=SANS_B(11), fill=RED)
d.text((22, LY + 26), "AKVAN SLAMS INTO INDIA'S EAST COAST",
       font=SERIF_B(24), fill=INK)
para(d, 22, LY + 60, 580,
     "Severe Cyclone Akvan crosses the Andhra Pradesh coast around "
     "noon, with sustained winds of 120–130 km/h gusting to 145. "
     "Three lakh people evacuated, 423 rescue teams deployed, "
     "schools shut across Odisha as the storm surge floods low land.",
     SANS(12), leading=16)
# drawn Bay of Bengal chart
cx0, cy0, cx1, cy1 = 22, LY + 138, 330, LY + 244
d.rectangle([cx0, cy0, cx1, cy1], fill=(205, 226, 238), outline=NAVY, width=2)
d.polygon([(cx0 + 18, cy1), (cx0 + 95, cy0 + 8), (cx0 + 135, cy0 + 55),
           (cx0 + 105, cy1)], fill=(238, 222, 180), outline=NAVY)
d.text((cx0 + 30, cy0 + 68), "INDIA", font=SANS_B(11), fill=NAVY)
d.text((cx0 + 195, cy0 + 8), "BAY OF BENGAL", font=SANS_B(10), fill=NAVY)
# spiral
sx, sy = cx0 + 225, cy0 + 58
for r in (34, 25, 16, 8):
    d.ellipse([sx - r, sy - r, sx + r, sy + r], outline=RED, width=3)
d.text((sx - 7, sy - 7), "A", font=SANS_B(13), fill=RED)
d.line([(sx - 30, sy + 22), (cx0 + 128, cy0 + 62)], fill=RED, width=3)
d.polygon([(cx0 + 128, cy0 + 62), (cx0 + 142, cy0 + 56),
           (cx0 + 138, cy0 + 70)], fill=RED)
d.text((352, LY + 142), "120–130 km/h", font=SERIF_B(20), fill=RED)
d.text((352, LY + 168), "sustained winds,\ngusts to 145 km/h",
       font=SANS(11), fill=INK)
d.text((352, LY + 202), "300,000 evacuated\n423 rescue teams\nLandfall ~noon",
       font=SANS_B(11), fill=INK)

# trilateral panel
d.rectangle([630, LY, W - 14, LY + LH], outline=INK, width=2)
d.rectangle([630, LY, W - 14, LY + 30], fill=NAVY)
d.text((640, LY + 7), "LEAD  •  SHENZHEN", font=SANS_B(11), fill=(255, 255, 255))
d.text((640, LY + 38), "THREE LEADERS,\nONE PEACE DECLARATION",
       font=SERIF_B(21), fill=INK)
para(d, 640, LY + 96, 360,
     "Trump, Xi and Putin hold the first-ever trilateral meeting "
     "and release a joint Peace Declaration. Putin then invites "
     "European envoys to Moscow to clarify their place in the "
     "Ukraine talks.", SANS(12), leading=16)
for i, (ini, name) in enumerate([("T", "TRUMP"), ("X", "XI"), ("P", "PUTIN")]):
    px = 660 + i * 118
    d.ellipse([px, LY + 182, px + 52, LY + 234], fill=RED, outline=INK, width=2)
    d.text((px + 26, LY + 191), ini, font=SERIF_B(24), fill=(255, 255, 255),
           anchor="ma")
    d.text((px + 26, LY + 238), name, font=SANS_B(9), fill=INK, anchor="ma")

# ---- ICJ strip ----
IY = LY + LH + 10
d.rectangle([14, IY, W - 14, IY + 58], fill=(24, 48, 96))
d.text((24, IY + 8), "THE HAGUE  •  ICJ RULES MYANMAR COMMITTED GENOCIDE",
       font=SERIF_B(19), fill=(255, 255, 255))
d.text((24, IY + 34), "Top UN court finds Myanmar guilty over the Rohingya — a landmark judgment after the 2017 crackdown.",
       font=SANS(12), fill=(220, 228, 240))

# ---- figures strip ----
FY = IY + 68
FIGS = [("$1.77tn", "Anthropic closes\nits first day"), ("$107bn",
       "Largest IPO ever\nraised by Anthropic"),
       ("2%", "US stocks fall;\nS&P down 6 days"),
       ("1,650", "Killed in Gaza\nsince the ceasefire"),
       ("317–6", "New Zealand\nvs India, 2nd day"),
       ("1 light-day", "Voyager 1's\nrecord distance")]
cw = (W - 28) // 6
for i, (big, small) in enumerate(FIGS):
    x0 = 14 + i * cw
    d.rectangle([x0, FY, x0 + cw - 6, FY + 62], outline=INK, width=1)
    d.text((x0 + 8, FY + 6), big, font=SERIF_B(17), fill=RED)
    para(d, x0 + 8, FY + 30, cw - 16, small, SANS(9), leading=11)

# ---- four columns of stories ----
CY = FY + 72
COLS = [
    ("WORLD", [
        ("TRUMP WAITS ON IRAN",
         "Trump pushes any Iran war decision to 2027: 'see what happens' after 1 January, he says."),
        ("EUROPE READY TO TALK",
         "At a Berlin summit, European leaders say they are ready to negotiate with Russia — any deal must be acceptable to Kyiv and Europe."),
        ("ABU DHABI, NO BREAKTHROUGH",
         "Russia–Ukraine–US talks end with a prisoner exchange agreed, but no ceasefire and no deal on territory."),
        ("KERCH BRIDGE HIT AGAIN",
         "Putin's Crimea bridge is struck for the third time this week, halting rail traffic to occupied Crimea."),
        ("VAN GOGH, $190.4m",
         "A Van Gogh sells for a record $190.4m after a row over its Nazi-era history."),
        ("BOAT SINKS OFF SENEGAL",
         "Dozens missing after a boat carrying 100 migrants sinks off Senegal's coast."),
        ("VENEZUELA–US DEAL",
         "Venezuela signs a military deal with the US less than a year after Maduro's ouster."),
    ]),
    ("MIDDLE EAST & ASIA", [
        ("GAZA: FIRST GROUND PUSH",
         "Israel launches its first ground offensive in Gaza since the October 2025 ceasefire; three killed, families flee Nuseirat."),
        ("PEACE PLAN SCORES 4/26",
         "Aid groups give Gaza's one-year-old peace plan a failing mark; Israeli forces now hold up to 70% of Gaza."),
        ("BOARD FAULTS BOTH SIDES",
         "Trump's Board of Peace says Israel and Hamas both failed their Gaza commitments; the truce is at risk of collapse."),
        ("RIYADH TOWER HIT",
         "Saudi sovereign wealth fund tower damaged as Houthis attack Riyadh."),
        ("MODI MEETS ROYALS",
         "PM Modi meets the Prince and Princess of Wales in New Delhi to deepen India–UK ties."),
        ("SENSEX RALLIES",
         "Indian stocks jump: Sensex gains 1.21% and Nifty 1.14% on autos and banks."),
        ("FIRE AT YUNUS HOME",
         "Fire at the ancestral home of Bangladesh's former interim leader Muhammad Yunus; arson suspected."),
    ]),
    ("MARKETS & TECH", [
        ("ANTHROPIC'S WILD DEBUT",
         "Anthropic opens at $111.50, briefly tops $2tn, then closes at $97.17 — still a $1.77tn valuation on the biggest IPO ever."),
        ("DOW DROPS 1,101",
         "Wall Street slumps 2% as the Anthropic pop fails to lift AI sentiment; Nasdaq falls 2.25%."),
        ("MUSK: 'NOT MAGA'",
         "Elon Musk tells the DealBook summit he felt 'pretty foolish' over nearly $500m spent backing Republicans."),
        ("GRINDR'S $120 AI PLAN",
         "Dating app Grindr launches a $120-a-month AI subscription that reads users' private chats."),
        ("PEW: FAITH SHIFT",
         "Pew projects Islam will eclipse Christianity as the world's largest religion within a decade."),
        ("VOYAGER 1, ONE LIGHT-DAY",
         "NASA confirms Voyager 1 is now a full light-day away — a day for a signal to reach it."),
        ("HAYABUSA2 GIVES UP LANDING",
         "Engine trouble forces Japan's Hayabusa2 probe to abandon its asteroid landing plan."),
    ]),
    ("SPORT & CULTURE", [
        ("PHILLIPS 118, NZ 317–6",
         "Glenn Phillips hits a century as New Zealand reach 317–6 against India in Wellington, after Nicholls' 113."),
        ("PHILLIPS' RARE TREBLE",
         "Phillips becomes only the second man to score centuries in all three formats against one side in a year."),
        ("HARMER'S 130-YEAR MARK",
         "Simon Harmer takes 6/51 — a 130-year-old record — as South Africa beat Bangladesh."),
        ("BAVUMA PASSES PONTING",
         "Temba Bavuma passes Ricky Ponting in a historic Test captaincy record."),
        ("GTA 6 BEATS THE ODYSSEY",
         "GTA 6 sales have already passed The Odyssey's $1.80bn global run."),
        ("MUMBAI KEEP 16",
         "Mumbai Indians finalise their 16-player retention list ahead of the IPL 2027 auction."),
        ("ICC MAPS TO 2035",
         "ICC confirms major events through 2035; India hosts the 2029 Champions Trophy."),
    ]),
]

col_w = (W - 28 - 3 * 12) // 4
for ci, (section, items) in enumerate(COLS):
    x0 = 14 + ci * (col_w + 12)
    d.rectangle([x0, CY, x0 + col_w, CY + 22], fill=INK)
    d.text((x0 + 8, CY + 4), section, font=SANS_B(11), fill=(255, 255, 255))
    y = CY + 30
    for head, deck in items:
        y = headline_block(d, x0, y, col_w, "", head, deck, head_size=12)
        d.line([(x0, y - 4), (x0 + col_w, y - 4)], fill=(200, 196, 184), width=1)

# ---- ticker + footer ----
TY = 952
d.rectangle([14, TY, W - 14, TY + 30], fill=(178, 34, 34))
d.text((22, TY + 7),
       "AKVAN LANDFALL  •  PEACE DECLARATION  •  ICJ: MYANMAR GUILTY  •  "
       "ANTHROPIC $1.77tn  •  GAZA GROUND PUSH  •  NZ 317–6  •  VOYAGER 1 LIGHT-DAY",
       font=SANS_B(11), fill=(255, 255, 255))
d.text((14, TY + 38),
       "Sources: Reuters, BBC, The Hindu, IMD, Al Jazeera, ReliefWeb, AP — all events of Friday 20 November 2026.",
       font=SANS(10), fill=GREY)
d.text((14, TY + 52),
       "The World Today — a one-image summary of the day. Built by an AI agent for make.fun news-image-20261120.",
       font=SANS(10), fill=GREY)

canvas.save("entry.png", optimize=True)
print("saved entry.png", canvas.size)
