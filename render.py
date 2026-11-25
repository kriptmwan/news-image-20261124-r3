#!/usr/bin/env python3
"""Render the r3 front page for news-image-20261124 (Tue 24 Nov 2026).

Dense newspaper front page: masthead + lead + 3 drawn panels + 18 dated
one-line stories in two columns under region headers. Drawn with PIL only.
Run: python3 render.py  ->  entry.png (1024x1024, deterministic).
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
LIVE = W - 2 * MARGIN  # 968

PAPER = (250, 247, 240)
INK = (20, 20, 20)
BLUE = (27, 79, 138)
RED = (179, 38, 30)
GOLD = (201, 162, 39)
GREY = (90, 90, 90)
PANEL_BG = (255, 255, 255)
RULE = (180, 175, 165)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_size(draw, text, path, start, max_w):
    """Largest size <= start at which text fits max_w; returns (font, width)."""
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f, draw.textlength(text, font=f)
        size -= 1
    f = font(path, 10)
    return f, draw.textlength(text, font=f)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines (each fits max_w)."""
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


def draw_star(d, cx, cy, r_out, r_in, n=8, fill=RED):
    import math
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def draw_courthouse(d, x, y, w, h, ink=INK):
    # Pediment triangle + 3 columns + base: reads as a court building.
    d.polygon([(x, y + h * 0.30), (x + w / 2, y), (x + w, y + h * 0.30)], fill=ink)
    d.rectangle([x + w * 0.06, y + h * 0.34, x + w * 0.94, y + h * 0.40], fill=ink)
    for i in range(3):
        cx = x + w * (0.18 + i * 0.32)
        d.rectangle([cx, y + h * 0.44, cx + w * 0.10, y + h * 0.82], fill=ink)
    d.rectangle([x, y + h * 0.86, x + w, y + h * 0.98], fill=ink)


def draw_tower(d, x, y, w, h, ink=INK):
    # Stepped tower with blast star at the top corner.
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=ink)
    d.rectangle([x + w * 0.12, y + h * 0.30, x + w * 0.88, y + h * 0.55], fill=ink)
    d.rectangle([x + w * 0.28, y + h * 0.08, x + w * 0.72, y + h * 0.30], fill=ink)
    d.rectangle([x + w * 0.45, y, x + w * 0.55, y + h * 0.08], fill=ink)
    # windows
    for row in range(3):
        for col in range(4):
            wx = x + w * (0.08 + col * 0.22)
            wy = y + h * (0.62 + row * 0.12)
            d.rectangle([wx, wy, wx + w * 0.10, wy + h * 0.06], fill=PAPER)
    draw_star(d, x + w * 0.92, y + h * 0.10, w * 0.22, w * 0.10)


def draw_trophy(d, x, y, w, h, gold=GOLD):
    # Cup: bowl + stem + base.
    d.pieslice([x, y, x + w, y + h * 0.55], 0, 180, fill=gold)
    d.rectangle([x, y, x + w, y + h * 0.12], fill=gold)
    # handles
    d.arc([x - w * 0.18, y + h * 0.02, x + w * 0.18, y + h * 0.30],
          90, 270, fill=gold, width=max(4, w // 12))
    d.arc([x + w * 0.82, y + h * 0.02, x + w * 1.18, y + h * 0.30],
          270, 90, fill=gold, width=max(4, w // 12))
    d.rectangle([x + w * 0.42, y + h * 0.55, x + w * 0.58, y + h * 0.78], fill=gold)
    d.rectangle([x + w * 0.25, y + h * 0.78, x + w * 0.75, y + h * 0.92], fill=gold)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = MARGIN

    # ---- Masthead ----
    name = "THE WORLD IN ONE DAY"
    f_name = font(SERIF_B, 40)
    nw = d.textlength(name, font=f_name)
    d.text(((W - nw) / 2, y), name, font=f_name, fill=INK)
    y += 48
    date = "TUESDAY, 24 NOVEMBER 2026"
    f_date, dw = fit_size(d, date, SERIF_B, 64, LIVE)
    d.text(((W - dw) / 2, y), date, font=f_date, fill=INK)
    y += f_date.size + 12
    d.rectangle([MARGIN, y, W - MARGIN, y + 4], fill=INK)
    y += 14

    # ---- Lead: Huawei verdict ----
    lead_x = MARGIN
    lead_w = LIVE
    kicker = "UNITED STATES  —  COURTS"
    f_kick = font(SANS_B, 22)
    d.text((lead_x, y), kicker, font=f_kick, fill=RED)
    y += 30
    head1, head2 = "HUAWEI GUILTY", "ON 10 COUNTS"
    f_head, _ = fit_size(d, head1, SANS_B, 72, lead_w - 190)
    d.text((lead_x, y), head1, font=f_head, fill=INK)
    d.text((lead_x, y + f_head.size + 2), head2, font=f_head, fill=INK)
    draw_courthouse(d, W - MARGIN - 170, y - 2, 160, 140)
    y += 2 * (f_head.size + 2) + 8
    deck = ("Brooklyn jury convicts the telecom giant of fraud and trade-secret "
            "theft; the racketeering charge fails.")
    f_deck = font(SANS, 27)
    lines = wrap(d, deck, f_deck, lead_w)
    assert len(lines) <= 2, f"deck wraps to {len(lines)} lines: {lines}"
    for ln in lines:
        d.text((lead_x, y), ln, font=f_deck, fill=INK)
        y += 33
    y += 6
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=RULE)
    y += 10

    # ---- Three drawn panels ----
    pw = (LIVE - 2 * 16) // 3  # 312
    ph = 182
    panels = [
        ("RIYADH", "TOWER HIT", "AGAIN", "11 hurt in 2nd strike", "on PIF tower", "tower"),
        ("SEOUL", "5,000", "+6.3%", "KOSPI reclaims 5,000", "", "kospi"),
        ("LAUSANNE", "SENEGAL", "CHAMPIONS", "CAS restores AFCON title", "again", "trophy"),
    ]
    py = y
    for i, (kick, h1, h2, sub1, sub2, kind) in enumerate(panels):
        px = MARGIN + i * (pw + 16)
        d.rectangle([px, py, px + pw, py + ph], fill=PANEL_BG, outline=RULE, width=1)
        d.rectangle([px, py, px + pw, py + 30], fill=BLUE)
        f_pk = font(SANS_B, 20)
        d.text((px + 12, py + 4), kick, font=f_pk, fill=(255, 255, 255))
        tx = px + 12
        ty = py + 38
        if kind == "kospi":
            f_big = font(SANS_B, 52)
            d.text((tx, ty), h1, font=f_big, fill=INK)
            f_pct = font(SANS_B, 30)
            d.text((tx, ty + 58), h2, font=f_pct, fill=BLUE)
            f_sub = font(SANS, 21)
            d.text((tx, ty + 100), sub1, font=f_sub, fill=INK)
        else:
            tw = pw - 108  # text zone; right ~96px reserved for the icon
            f_ph = font(SANS_B, 30)
            hlines = wrap(d, h1 + " " + h2, f_ph, tw)
            assert len(hlines) <= 2, f"panel headline wraps to {len(hlines)}: {hlines}"
            hy = ty
            for hl in hlines:
                d.text((tx, hy), hl, font=f_ph, fill=INK)
                hy += 34
            f_sub = font(SANS, 21)
            sub = (sub1 + " " + sub2).strip()
            slines = wrap(d, sub, f_sub, tw)
            sy = ty + 74
            for sl in slines:
                d.text((tx, sy), sl, font=f_sub, fill=INK)
                sy += 26
            if kind == "tower":
                draw_tower(d, px + pw - 88, py + 44, 72, 92)
            elif kind == "trophy":
                draw_trophy(d, px + pw - 84, py + 48, 68, 88)
    y = py + ph + 12

    # ---- Story list: two columns, region headers ----
    groups_a = [
        ("EUROPE", [
            "Zaporizhzhia strike kills 2, 40 hurt",
            "Moscow warns Estonia of 'open war'",
            "France tries officer over Nahel killing",
        ]),
        ("MIDDLE EAST", [
            "Gaza strikes kill 7 despite ceasefire",
            "Iran claims Hormuz tankers hit by mines",
            "Qatar urges Iran-US restraint",
        ]),
        ("AMERICAS", [
            "Microsoft 'Code Red' after 24-hour outage",
            "Cucuta drone attack injures 3",
            "Trump tariff findings due",
        ]),
    ]
    groups_b = [
        ("ASIA", [
            "Korea scrambles jets at Russian planes",
            "Nikkei jumps 3.9% to 58,644",
            "PNG begins Bougainville vote",
            "First train Ayodhya-Janankpur runs",
            "Hanoi blast kills 6, injures 10",
            "Hasina plans Dec 16 return",
            "Pakistan astronaut to fly Shenzhou-24",
            "Malaysia to return 6,803 Myanmar nationals",
            "Tamil Nadu signs $5.3bn in deals",
        ]),
    ]
    col_w = (LIVE - 16) // 2  # 476
    f_hdr = font(SANS_B, 23)
    f_line = font(SANS, 20)
    line_h = 27
    hdr_h = 32

    def column_height(groups):
        h = 0
        for _, lines_ in groups:
            h += hdr_h + len(lines_) * line_h
        return h

    ha, hb = column_height(groups_a), column_height(groups_b)
    list_h = max(ha, hb)
    assert y + list_h + 44 <= H, f"overflow: y={y} list_h={list_h} total={y + list_h + 44}"

    def draw_column(groups, cx):
        cy = y
        for hdr, lines_ in groups:
            d.rectangle([cx, cy, cx + col_w, cy + hdr_h - 4], fill=BLUE)
            d.text((cx + 10, cy + 3), hdr, font=f_hdr, fill=(255, 255, 255))
            cy += hdr_h
            for ln in lines_:
                wln = d.textlength(ln, font=f_line)
                assert wln <= col_w - 8, f"line too wide ({wln:.0f}): {ln}"
                d.text((cx + 2, cy), "\u2022  " + ln, font=f_line, fill=INK)
                cy += line_h
            cy += 2

    draw_column(groups_a, MARGIN)
    draw_column(groups_b, MARGIN + col_w + 16)
    y += list_h + 10

    # ---- Footer ----
    d.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=RULE)
    y += 8
    f_foot = font(SANS, 18)
    foot = "All stories: Tuesday, 24 November 2026  •  Claims labelled as claims  •  Reuters, AP, CNN, BBC"
    fw = d.textlength(foot, font=f_foot)
    assert fw <= LIVE, f"footer too wide: {fw:.0f}"
    d.text(((W - fw) / 2, y), foot, font=f_foot, fill=GREY)
    y += 24
    assert y <= H - MARGIN + 4, f"bottom overflow: y={y}"

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    data = open(out, "rb").read()
    print(f"entry.png: {img.size[0]}x{img.size[1]}, {len(data)} B, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    print(f"final y={y} (limit {H - MARGIN})")


if __name__ == "__main__":
    main()
