"""Render the front page for Tuesday 24 November 2026.

Reads stories.json (verified story set) and draws one 1024x1024 PNG.
Pure Pillow, no network, no clock, no randomness: the same input always
writes the same bytes. Run: python3 render.py  ->  entry.png
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (248, 244, 233)
INK = (22, 19, 14)
RED = (179, 38, 30)
NAVY = (20, 50, 79)
NAVY_D = (13, 36, 58)
GOLD = (185, 138, 29)
SLATE = (90, 86, 76)
LINE = (201, 191, 166)
SEA = (188, 211, 228)
LAND = (231, 220, 192)
LAND_LINE = (138, 127, 99)
PANEL = (255, 252, 244)
DUSK_TOP = (24, 42, 74)
DUSK_MID = (96, 74, 88)
DUSK_LOW = (214, 122, 54)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None, spacing=0):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---- simplified continent outlines (lon, lat), equirectangular ----
NORTH_AMERICA = [(-168, 66), (-158, 58), (-140, 60), (-130, 54), (-125, 49), (-124, 42),
                 (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-92, 15),
                 (-86, 12), (-83, 9), (-79, 9), (-81, 13), (-84, 16), (-87, 21), (-90, 21),
                 (-91, 19), (-96, 19), (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 26),
                 (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47),
                 (-55, 47), (-60, 52), (-65, 58), (-68, 58), (-78, 62), (-85, 66), (-92, 66),
                 (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70), (-25, 76),
             (-35, 77), (-50, 76), (-58, 72)]
SOUTH_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
                 (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
                 (-66, -55), (-68, -50), (-65, -45), (-62, -40), (-58, -35), (-52, -32),
                 (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3),
                 (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-77, 8)]
AFRICA = [(-17, 15), (-16, 20), (-13, 27), (-10, 31), (-5, 35), (0, 36), (10, 37),
          (11, 34), (15, 32), (20, 32), (25, 31), (30, 31), (32, 31), (34, 28), (35, 24),
          (37, 20), (39, 18), (41, 15), (43, 12), (46, 11), (51, 12), (51, 10), (48, 5),
          (42, 0), (40, -5), (40, -10), (39, -15), (36, -18), (33, -25), (28, -33),
          (20, -35), (17, -32), (15, -27), (13, -18), (12, -12), (13, -6), (12, -2),
          (9, 0), (9, 4), (6, 4), (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12)]
EURASIA = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49), (0, 51),
           (3, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64), (13, 66),
           (18, 69), (25, 71), (30, 70), (35, 68), (40, 68), (45, 68), (50, 69), (55, 68),
           (60, 69), (68, 73), (75, 73), (80, 73), (90, 75), (100, 77), (110, 74),
           (120, 73), (130, 72), (140, 72), (150, 70), (160, 69), (170, 66), (178, 65),
           (178, 62), (170, 60), (162, 60), (158, 52), (156, 51), (150, 59), (142, 55),
           (141, 50), (140, 45), (135, 43), (130, 42), (127, 40), (126, 38), (122, 38),
           (120, 34), (122, 30), (120, 28), (118, 25), (112, 22), (109, 20), (108, 18),
           (105, 10), (103, 7), (100, 8), (98, 12), (94, 16), (92, 21), (89, 22), (86, 20),
           (83, 18), (80, 15), (77, 8), (75, 12), (72, 20), (68, 23), (66, 25), (62, 25),
           (58, 25), (56, 27), (52, 28), (50, 29), (48, 30), (44, 29), (42, 27), (39, 22),
           (38, 20), (35, 28), (34, 31), (33, 36), (30, 36), (27, 37), (26, 38), (23, 36),
           (22, 37), (19, 40), (18, 40), (16, 38), (15, 40), (12, 42), (10, 44), (8, 44),
           (6, 43), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37)]
AUSTRALIA = [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
             (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
             (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
             (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
             (118, -20)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 35), (140, 38), (141, 41),
         (142, 44), (144, 44), (141, 40), (139, 38), (137, 36), (134, 34), (131, 32)]
UK = [(-5, 50), (-3, 53), (-5, 55), (-3, 56), (-2, 57), (-1, 58), (-3, 57), (-5, 56), (-5, 53)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EURASIA, AUSTRALIA, JAPAN, UK]
# small island blobs (lon, lat, rx, ry) in degrees
ISLANDS = [(100, 2, 4, 2), (107, -6, 4, 1.5), (114, -8, 3, 1.5), (120, -2, 3, 2),
           (128, -3, 3, 2), (136, -4, 4, 2), (141, -4, 4, 2), (167, -42, 2.5, 2),
           (174, -39, 2, 2.5)]


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    return (mx + (lon + 180.0) / 360.0 * mw, my + (90.0 - lat) / 180.0 * mh)


def draw_gaza_panel(draw, x, y, w, h):
    """Dusk skyline over Gaza: layered sky, low sun, dome and minaret silhouettes.
    All vertical sizes scale with the panel height h."""
    s = h / 150.0
    for i in range(h):
        t = i / max(1, h - 1)
        if t < 0.45:
            c = tuple(int(DUSK_TOP[k] + (DUSK_MID[k] - DUSK_TOP[k]) * (t / 0.45)) for k in range(3))
        else:
            u = (t - 0.45) / 0.55
            c = tuple(int(DUSK_MID[k] + (DUSK_LOW[k] - DUSK_MID[k]) * u) for k in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=c)
    # sun
    sx, sy, sr = x + int(w * 0.72), y + int(h * 0.52), max(14, int(26 * s))
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(240, 196, 110))
    draw.ellipse([sx - sr - 7, sy - sr - 7, sx + sr + 7, sy + sr + 7], outline=(240, 196, 110))
    base = y + h
    sil = (16, 22, 40)
    # far skyline
    for bx, bw, bh in [(0, 70, 34), (62, 44, 52), (104, 60, 30), (160, 52, 44), (210, 66, 30),
                       (272, 48, 56), (318, 62, 34), (378, 56, 46), (432, 64, 30), (492, 58, 38)]:
        bh2 = max(8, int(bh * s))
        draw.rectangle([x + bx, base - bh2, x + bx + bw, base], fill=sil)
    # dome
    dx = x + 300
    draw.pieslice([dx - 34, base - int(108 * s), dx + 34, base - int(40 * s)], 180, 360, fill=sil)
    draw.rectangle([dx - 34, base - int(74 * s), dx + 34, base], fill=sil)
    draw.rectangle([dx - 3, base - int(122 * s), dx + 3, base - int(74 * s)], fill=sil)
    # minaret
    mx = x + 120
    draw.rectangle([mx - 7, base - int(128 * s), mx + 7, base], fill=sil)
    draw.polygon([(mx - 11, base - int(128 * s)), (mx + 11, base - int(128 * s)),
                  (mx, base - int(152 * s))], fill=sil)
    # smoke columns
    for cx, ch in [(x + 210, 66), (x + 430, 58), (x + 60, 48)]:
        for k, r in enumerate((16, 11, 7)):
            yy = base - int(ch * s) - k * 14
            draw.ellipse([cx - r, yy - r, cx + r, yy + r], fill=(120, 112, 104))
    # lit windows
    for wx, wy in [(x + 20, 22), (x + 80, 38), (x + 180, 26),
                   (x + 290, 40), (x + 400, 28), (x + 520, 24)]:
        wy2 = base - int(wy * s)
        draw.rectangle([wx, wy2, wx + 5, wy2 + 7], fill=(240, 196, 110))


def draw_pictogram(draw, x, y, s, kind):
    """Small square pictogram: 'flats' (Zaporizhzhia) or 'factory' (Banten)."""
    draw.rectangle([x, y, x + s, y + s], fill=NAVY)
    if kind == "flats":
        draw.rectangle([x + 14, y + 22, x + 58, y + s - 8], fill=(228, 222, 205))
        for r in range(3):
            for c in range(3):
                wx, wy = x + 20 + c * 14, y + 28 + r * 16
                col = (60, 60, 60) if (r, c) != (1, 1) else RED
                draw.rectangle([wx, wy, wx + 8, wy + 9], fill=col)
        draw.polygon([(x + 40, y + 8), (x + 52, y + 22), (x + 44, y + 22)], fill=(214, 122, 54))
        draw.ellipse([x + 46, y + 4, x + 58, y + 16], fill=(150, 144, 134))
    else:  # factory
        draw.rectangle([x + 12, y + 40, x + 58, y + s - 8], fill=(228, 222, 205))
        draw.rectangle([x + 46, y + 16, x + 54, y + 44], fill=(228, 222, 205))
        draw.rectangle([x + 18, y + 48, x + 26, y + 56], fill=NAVY)
        draw.rectangle([x + 34, y + 48, x + 42, y + 56], fill=NAVY)
        draw.polygon([(x + 30, y + 14), (x + 38, y + 30), (x + 26, y + 30)], fill=(240, 150, 40))
        draw.polygon([(x + 36, y + 22), (x + 42, y + 34), (x + 30, y + 34)], fill=(214, 90, 30))
        draw.ellipse([x + 48, y + 6, x + 58, y + 16], fill=(150, 144, 134))


def draw_map(draw, x, y, w, h, pins):
    draw.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=1)
    for gx in range(1, 6):
        gx0 = x + w * gx / 6
        draw.line([(gx0, y), (gx0, y + h)], fill=(255, 255, 255), width=1)
    for gy in range(1, 4):
        gy0 = y + h * gy / 4
        draw.line([(x, gy0), (x + w, gy0)], fill=(255, 255, 255), width=1)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x, y, w, h) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_LINE)
    for lon, lat, rx, ry in ISLANDS:
        cx, cy = lonlat_to_xy(lon, lat, x, y, w, h)
        ex = rx / 360.0 * w
        ey = ry / 180.0 * h
        draw.ellipse([cx - ex, cy - ey, cx + ex, cy + ey], fill=LAND, outline=LAND_LINE)
    for p in pins:
        px, py = lonlat_to_xy(p["lon"], p["lat"], x, y, w, h)
        # dot always on the true spot; the number badge may sit offset,
        # joined to its dot by a leader line, so close pins stay readable
        # without lying about where they are.
        f = font(F_SANS_B, 11)
        if "bx" in p and "by" in p:
            bx, by = px + p["bx"], py + p["by"]
            draw.line([(px, py), (bx, by)], fill=RED, width=1)
            draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(255, 255, 255))
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED)
            draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(255, 255, 255))
            draw.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED)
            tw = draw.textlength(str(p["n"]), font=f)
            draw.text((bx - tw / 2, by - 7), str(p["n"]), font=f, fill=(255, 255, 255))
        else:
            draw.ellipse([px - 11, py - 11, px + 11, py + 11], fill=(255, 255, 255))
            draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED)
            tw = draw.textlength(str(p["n"]), font=f)
            draw.text((px - tw / 2, py - 7), str(p["n"]), font=f, fill=(255, 255, 255))


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as f:
        d = json.load(f)

    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)
    MX = 16
    RX = W - MX  # 1008

    # ---------- masthead ----------
    f_top = font(F_SANS_B, 11)
    top = "A FRONT PAGE OF THE DAY'S NEWS  —  EVERY STORY VERIFIED AGAINST ITS SOURCE"
    tw = dr.textlength(top, font=f_top)
    dr.text(((W - tw) / 2, 10), top, font=f_top, fill=SLATE)
    rule(dr, MX, 30, RX, LINE, 1)
    f_title = font(F_SERIF_B, 52)
    tw = dr.textlength(d["masthead"], font=f_title)
    dr.text(((W - tw) / 2, 36), d["masthead"], font=f_title, fill=INK)
    f_date = font(F_SANS_B, 21)
    date_line = "TUESDAY  24  NOVEMBER  2026"
    tw = dr.textlength(date_line, font=f_date)
    dr.text(((W - tw) / 2, 96 - 2, ), date_line, font=f_date, fill=RED)
    f_sub = font(F_SANS, 12)
    sub = "ALL TIMES UTC  ·  13 STORIES  ·  5 REGIONS  ·  12 PLACES ON THE MAP"
    tw = dr.textlength(sub, font=f_sub)
    dr.text(((W - tw) / 2, 122), sub, font=f_sub, fill=SLATE)

    # ---------- stats bar ----------
    sy, sh = 146, 60
    dr.rectangle([MX, sy, RX, sy + sh], fill=NAVY)
    stats = d["stats"]
    cw = (RX - MX) / 4
    f_val = font(F_SANS_B, 30)
    f_lab = font(F_SANS, 10)
    for i, s in enumerate(stats):
        cx = MX + i * cw
        if i:
            dr.line([(cx, sy + 8), (cx, sy + sh - 8)], fill=(120, 150, 180), width=1)
        vw = dr.textlength(s["value"], font=f_val)
        dr.text((cx + (cw - vw) / 2, sy + 4), s["value"], font=f_val, fill=(255, 255, 255))
        text_block(dr, cx + 12, sy + 36, s["label"], f_lab, (205, 220, 235), cw - 24, leading=11)

    # ---------- heroes ----------
    hy, hh = 214, 244
    hero = d["heroes"][0]
    hx, hw = MX, 584
    dr.rectangle([hx, hy, hx + hw, hy + hh], fill=PANEL, outline=INK, width=1)
    draw_gaza_panel(dr, hx + 1, hy + 1, hw - 2, 96)
    yy = hy + 106
    f_kick = font(F_SANS_B, 12)
    dr.text((hx + 12, yy), hero["kicker"] + "  ·  GAZA CITY", font=f_kick, fill=RED)
    yy += 18
    f_h1 = font(F_SANS_B, 27)
    yy = text_block(dr, hx + 12, yy, hero["headline"], f_h1, INK, hw - 24, leading=30)
    yy += 4
    f_deck = font(F_SANS, 13)
    yy = text_block(dr, hx + 12, yy, hero["deck"], f_deck, (40, 36, 30), hw - 24, leading=16)
    f_src = font(F_SANS, 11)
    dr.text((hx + 12, hy + hh - 18), "REPORTED  ·  Source: " + hero["source"], font=f_src, fill=SLATE)

    # right heroes, stacked
    rx0, rw = 612, RX - 612
    rh = (hh - 12) // 2
    kinds = ["flats", "factory"]
    for i, h2 in enumerate(d["heroes"][1:]):
        y0 = hy + i * (rh + 12)
        dr.rectangle([rx0, y0, rx0 + rw, y0 + rh], fill=PANEL, outline=INK, width=1)
        draw_pictogram(dr, rx0 + 10, y0 + 10, 56, kinds[i])
        tx = rx0 + 78
        dr.text((tx, y0 + 8), h2["kicker"], font=f_kick, fill=RED)
        f_h2 = font(F_SANS_B, 16)
        y1 = text_block(dr, tx, y0 + 24, h2["headline"], f_h2, INK, rw - 90, leading=19)
        y1 = text_block(dr, tx, y1 + 2, h2["deck"], f_deck, (40, 36, 30), rw - 90, leading=16)
        dr.text((tx, y0 + rh - 16), h2["place"] + "  ·  " + h2["source"], font=f_src, fill=SLATE)

    # ---------- map panel ----------
    my, mh = 466, 184
    dr.rectangle([MX, my, RX, my + mh], fill=PANEL, outline=INK, width=1)
    f_sec = font(F_SANS_B, 13)
    dr.text((MX + 12, my + 8), "WHERE IT HAPPENED — 12 PLACES, 5 REGIONS", font=f_sec, fill=INK)
    map_x, map_y, map_w, map_h = MX + 10, my + 30, 620, mh - 40
    draw_map(dr, map_x, map_y, map_w, map_h, d["pins"])
    # legend, two columns
    lx = map_x + map_w + 14
    f_leg = font(F_SANS, 11)
    f_legb = font(F_SANS_B, 11)
    ly = map_y + 2
    col_w = (RX - 12 - lx) // 2
    for i, p in enumerate(d["pins"]):
        col = i // 6
        row = i % 6
        px = lx + col * col_w
        py = ly + row * 11
        dr.text((px, py), str(p["n"]), font=f_legb, fill=RED)
        dr.text((px + 18, py), p["place"], font=f_leg, fill=INK)
    ly = ly + 6 * 11 + 4
    rule(dr, lx, ly, RX - 12, LINE, 1)
    ly += 5
    # region bar
    total = sum(r["count"] for r in d["regions"])
    bx, bw = lx, RX - 12 - lx
    x0 = bx
    cols = [RED, NAVY, GOLD, (90, 130, 90), SLATE]
    for i, r in enumerate(d["regions"]):
        seg = bw * r["count"] / total
        dr.rectangle([x0, ly, x0 + seg - 1, ly + 9], fill=cols[i])
        x0 += seg
    ly += 12
    for i, r in enumerate(d["regions"]):
        dr.rectangle([lx, ly, lx + 8, ly + 8], fill=cols[i])
        dr.text((lx + 12, ly - 1), "%s %d" % (r["name"], r["count"]), font=f_leg, fill=INK)
        ly += 10

    # ---------- timeline ----------
    ty, th = 658, 66
    dr.rectangle([MX, ty, RX, ty + th], fill=PANEL, outline=INK, width=1)
    dr.text((MX + 12, ty + 6), "THE DAY IN ORDER — AS THE NEWS BROKE (UTC)", font=f_sec, fill=INK)
    tl = d["timeline"]
    tw5 = (RX - MX - 24) / 5
    f_when = font(F_SANS_B, 11)
    f_tl = font(F_SANS, 11)
    lx0 = MX + 12
    dr.line([(lx0 + 4, ty + 32), (RX - 12, ty + 32)], fill=LINE, width=2)
    for i, item in enumerate(tl):
        cx = lx0 + i * tw5
        dr.ellipse([cx, ty + 27, cx + 9, ty + 36], fill=RED)
        dr.text((cx + 14, ty + 24), item["when"], font=f_when, fill=RED)
        text_block(dr, cx, ty + 38, item["text"], f_tl, INK, tw5 - 12, leading=11)

    # ---------- mains ----------
    gy, gh = 732, 118
    dr.text((MX, gy), "MORE OF THE DAY", font=f_sec, fill=INK)
    mains = d["mains"]
    cw3 = (RX - MX - 24) / 3
    f_mh = font(F_SANS_B, 14)
    f_md = font(F_SANS, 11)
    for i, m in enumerate(mains):
        col, row = i % 3, i // 3
        x0 = MX + col * (cw3 + 12)
        y0 = gy + 20 + row * 62
        if col:
            dr.line([(x0 - 6, y0), (x0 - 6, y0 + 54)], fill=LINE, width=1)
        dr.text((x0, y0), m["kicker"] + "  ·  " + m["place"] + "  ·  " + m["source"], font=f_kick, fill=RED)
        y1 = text_block(dr, x0, y0 + 15, m["headline"], f_mh, INK, cw3, leading=16)
        text_block(dr, x0, y1 + 1, m["deck"], f_md, (40, 36, 30), cw3, leading=13)

    # ---------- briefs strip ----------
    by = 876
    rule(dr, MX, by, RX, INK, 2)
    dr.text((MX, by + 6), "IN BRIEF", font=f_sec, fill=INK)
    f_bh = font(F_SANS_B, 12)
    f_bd = font(F_SANS, 11)
    bw4 = (RX - MX - 36) / 4
    for i, b in enumerate(d["briefs"]):
        x0 = MX + i * (bw4 + 12)
        if i:
            dr.line([(x0 - 6, by + 6), (x0 - 6, by + 52)], fill=LINE, width=1)
        y1 = text_block(dr, x0, by + 22, b["headline"], f_bh, INK, bw4, leading=14)
        text_block(dr, x0, y1, b["deck"], f_bd, (40, 36, 30), bw4, leading=13)

    # ---------- date check + footer ----------
    dy = 940
    dr.rectangle([MX, dy, RX, dy + 80], fill=(235, 228, 210), outline=INK, width=1)
    dr.text((MX + 12, dy + 6), "DATE CHECK — LEFT OUT ON PURPOSE: NOT 24 NOVEMBER", font=f_sec, fill=RED)
    f_dc = font(F_SANS, 11)
    yy = dy + 24
    for line in d["date_check"]:
        dr.text((MX + 12, yy), "✕  " + line, font=f_dc, fill=INK)
        yy += 11
    f_foot = font(F_SANS, 9)
    text_block(dr, MX + 12, yy + 2, d["footer_sources"], f_foot, SLATE, RX - MX - 24, leading=11)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
