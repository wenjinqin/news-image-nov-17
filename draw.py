#!/usr/bin/env python3
"""Draw the entry image for make.fun's news-image-20261117 contest:
one page that sums up the world news of Tuesday 17 November 2026.

Every panel is drawn with flat shapes (no photos, no external assets) and
labelled with a short headline, so the page reads at a glance. Running this
file writes entry.png beside it (1024 x 1024).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (24, 24, 24)
RED = (179, 49, 42)
GREY = (92, 92, 92)
BLUE = (46, 109, 164)
SKY = (214, 230, 242)
ORANGE = (232, 126, 34)
YELLOW = (244, 190, 60)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=1.12, align="left"):
    for line in wrap(draw, text, fnt, max_w):
        w = draw.textlength(line, font=fnt)
        tx = x if align == "left" else x + (max_w - w) / 2
        draw.text((tx, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def panel(draw, box, lw=3):
    draw.rectangle(box, outline=INK, width=lw)


def story_text(draw, x, y, w, kicker, headline, caption, hsize=30, csize=20):
    draw.text((x, y), kicker, font=font(FB, 19), fill=RED)
    y = text_block(draw, x, y + 26, headline, font(FB, hsize), INK, w)
    text_block(draw, x, y + 4, caption, font(FR, csize), GREY, w)


# ---------------------------------------------------------------- scenes
def scene_bridge(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=BLUE)
    for i in range(5):  # waves
        wx = x + 18 + i * 62
        draw.arc([wx, y + h - 26, wx + 34, y + h - 8], 0, 180, fill=(255, 255, 255), width=3)
    deck = y + h - 78
    draw.line([x + 8, deck, x + w * 0.42, deck], fill=INK, width=7)
    draw.line([x + w * 0.60, deck, x + w - 8, deck], fill=INK, width=7)
    for t in range(4):  # truss posts
        tx = x + 16 + t * 52
        draw.line([tx, deck, tx + 26, deck - 34], fill=INK, width=4)
        draw.line([tx, deck - 34, tx + 52, deck], fill=INK, width=4)
        tx2 = x + w * 0.62 + t * 40
        draw.line([tx2, deck, tx2 + 20, deck - 30], fill=INK, width=4)
    cx, cy = x + w * 0.51, deck - 6  # blast in the gap
    pts = []
    import math
    for i in range(16):
        r = 34 if i % 2 == 0 else 15
        a = math.pi * i / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=ORANGE)
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=YELLOW)
    for dx, dy, r in ((-46, -38, 13), (40, -44, 16), (2, -58, 11)):  # smoke
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(150, 150, 150))
    for dx, dy in ((70, -70), (128, -56)):  # drones overhead: body + four rotors
        gx, gy = x + dx, y + dy + h - 78
        draw.rectangle([gx - 9, gy - 4, gx + 9, gy + 4], fill=INK)
        for sx, sy in ((-14, -8), (14, -8), (-14, 7), (14, 7)):
            draw.ellipse([gx + sx - 6, gy + sy - 2, gx + sx + 6, gy + sy + 2], outline=INK, width=2)
            draw.line([gx, gy, gx + sx, gy + sy], fill=INK, width=2)


def scene_radar(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, by = x + w * 0.38, y + h - 10
    draw.polygon([(cx - 8, by), (cx + 8, by), (cx, by - 44)], fill=INK)
    draw.arc([cx - 34, by - 92, cx + 34, by - 24], 300, 120, fill=INK, width=6)
    draw.line([cx, by - 44, cx + 18, by - 66], fill=INK, width=5)
    for r in (18, 30, 42):
        draw.arc([cx + 14 - r, by - 70 - r, cx + 14 + r, by - 70 + r], 300, 60, fill=RED, width=3)
    dx, dy = x + w * 0.74, y + 26  # quadcopter
    draw.rectangle([dx - 13, dy - 6, dx + 13, dy + 6], fill=INK)
    for sx, sy in ((-20, -12), (20, -12), (-20, 10), (20, 10)):
        draw.ellipse([dx + sx - 8, dy + sy - 3, dx + sx + 8, dy + sy + 3], outline=INK, width=3)
        draw.line([dx, dy, dx + sx, dy + sy], fill=INK, width=3)


def scene_flags(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    base = y + h - 8
    cols = [(200, 30, 30), None, (230, 230, 230)]
    for i, fx in enumerate((0.22, 0.50, 0.78)):
        px = x + w * fx
        draw.line([px, y + 14, px, base], fill=INK, width=4)
        fw, fh = 52, 34
        if i == 0:  # China: red, one big + dots of stars
            draw.rectangle([px, y + 14, px + fw, y + 14 + fh], fill=(206, 40, 40))
            draw.ellipse([px + 6, y + 20, px + 14, y + 28], fill=YELLOW)
            for sy in (22, 30, 38):
                draw.ellipse([px + 20, y + sy, px + 24, y + sy + 4], fill=YELLOW)
        elif i == 1:  # USA: stripes + blue canton
            draw.rectangle([px, y + 14, px + fw, y + 14 + fh], fill=(240, 240, 240))
            for s in range(4):
                draw.rectangle([px, y + 14 + s * 9, px + fw, y + 18 + s * 9], fill=(178, 34, 52))
            draw.rectangle([px, y + 14, px + 24, y + 32], fill=(60, 59, 110))
        else:  # Russia: white / blue / red
            draw.rectangle([px, y + 14, px + fw, y + 14 + fh], fill=(240, 240, 240))
            draw.rectangle([px, y + 25, px + fw, y + 36], fill=(30, 80, 170))
            draw.rectangle([px, y + 36, px + fw, y + 48], fill=(206, 40, 40))


def scene_jet(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.ellipse([x + w - 74, y + 10, x + w - 18, y + 66], fill=(216, 60, 50))  # rising sun
    jx, jy = x + 30, y + h * 0.52
    body = [(jx, jy), (jx + 96, jy - 12), (jx + 128, jy - 2), (jx + 96, jy + 6),
            (jx + 30, jy + 8), (jx + 6, jy + 14)]
    draw.polygon(body, fill=(70, 76, 84))
    draw.polygon([(jx + 52, jy - 4), (jx + 74, jy - 24), (jx + 88, jy - 4)], fill=(70, 76, 84))
    draw.polygon([(jx + 8, jy + 4), (jx - 8, jy - 14), (jx + 16, jy - 2)], fill=(70, 76, 84))
    draw.line([jx - 14, jy + 12, jx - 34, jy + 14], fill=(255, 255, 255), width=4)
    draw.line([jx - 8, jy + 18, jx - 26, jy + 20], fill=(255, 255, 255), width=4)


def scene_cyber(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    draw.rectangle([x + 14, y + 12, x + w - 14, y + h - 12], outline=INK, width=4, fill=(250, 250, 250))
    draw.rectangle([x + 14, y + 12, x + w - 14, y + 32], fill=INK)
    for i, c in enumerate(((230, 90, 80), (240, 190, 80), (110, 200, 110))):
        draw.ellipse([x + 24 + i * 16, y + 17, x + 34 + i * 16, y + 27], fill=c)
    bx, by = x + w * 0.52, y + h * 0.58  # the bug
    draw.ellipse([bx - 17, by - 21, bx + 17, by + 21], fill=RED)
    draw.line([bx, by - 21, bx, by + 21], fill=INK, width=3)
    draw.ellipse([bx - 8, by - 32, bx + 8, by - 18], fill=INK)
    for s in (-1, 1):
        draw.line([bx + s * 14, by - 12, bx + s * 30, by - 22], fill=INK, width=4)
        draw.line([bx + s * 16, by + 2, bx + s * 32, by + 2], fill=INK, width=4)
        draw.line([bx + s * 14, by + 14, bx + s * 28, by + 24], fill=INK, width=4)
        draw.line([bx - s * 5, by - 30, bx - s * 14, by - 40], fill=INK, width=3)


def scene_rocket(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(38, 44, 66))
    for sx, sy in ((30, 18), (90, 40), (150, 14), (210, 34), (262, 20), (52, 58), (238, 60)):
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    cx = x + w * 0.30
    top, bot = y + 12, y + h - 26
    draw.polygon([(cx - 17, bot), (cx - 17, top + 26), (cx, top), (cx + 17, top + 26), (cx + 17, bot)], fill=(238, 238, 238))
    draw.polygon([(cx - 17, top + 26), (cx, top), (cx + 17, top + 26)], fill=RED)
    draw.ellipse([cx - 7, top + 36, cx + 7, top + 50], fill=BLUE)
    draw.polygon([(cx - 17, bot - 16), (cx - 30, bot + 4), (cx - 17, bot + 4)], fill=RED)
    draw.polygon([(cx + 17, bot - 16), (cx + 30, bot + 4), (cx + 17, bot + 4)], fill=RED)
    draw.polygon([(cx - 9, bot + 4), (cx, bot + 22), (cx + 9, bot + 4)], fill=ORANGE)
    for dx, dy, s in ((52, 96, 8), (74, 66, 6), (44, 130, 6)):  # falling debris
        draw.rectangle([cx + dx, y + dy, cx + dx + s, y + dy + s], fill=YELLOW)
    draw.rectangle([cx + 88, y + 28, cx + 106, y + 40], fill=(170, 180, 200))  # tumbling satellite
    draw.rectangle([cx + 76, y + 31, cx + 88, y + 37], fill=BLUE)
    draw.rectangle([cx + 106, y + 31, cx + 118, y + 37], fill=BLUE)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # page margin

    d.text((W / 2, 20), "T H E   W O R L D   I N   O N E   I M A G E",
           font=font(FB, 26), fill=INK, anchor="ma")
    date_f = font(FB, 66)
    while d.textlength("TUESDAY 17 NOVEMBER 2026", font=date_f) > W - 2 * M:
        date_f = font(FB, date_f.size - 2)
    d.text((W / 2, 54), "TUESDAY 17 NOVEMBER 2026", font=date_f, fill=INK, anchor="ma")
    d.line([M, 140, W - M, 140], fill=INK, width=5)
    d.line([M, 148, W - M, 148], fill=INK, width=2)

    # lead story ------------------------------------------------------
    panel(d, [M, 164, W - M, 452])
    scene_bridge(d, M + 10, 174, 452, 268)
    lx = M + 486
    d.text((lx, 182), "UKRAINE WAR", font=font(FB, 22), fill=RED)
    y = text_block(d, lx, 214, "UKRAINE BLOWS UP THE CRIMEA BRIDGE", font(FB, 40), INK, W - M - lx - 8)
    text_block(d, lx, y + 8,
               "Zelenskyy hails an \u201cunprecedented\u201d strike on the Kerch link to Crimea. "
               "Moscow answers by hitting two bridges in Kyiv.",
               font(FR, 22), GREY, W - M - lx - 8)

    # row of three ----------------------------------------------------
    y0, y1 = 466, 726
    cw = (W - 2 * M - 24) // 3
    cells = [
        (scene_radar, "MIDDLE EAST", "IRAN DRONES HIT US RADAR IN BAHRAIN",
         "Third strike in days; Bahrain says they were intercepted."),
        (scene_flags, "DIPLOMACY", "XI, TRUMP, PUTIN MEET IN SHENZHEN",
         "Beijing confirms the first US-China-Russia summit, for 19 Nov."),
        (scene_jet, "ASIA", "JAPAN JETS SCRAMBLE AT RUSSIAN PLANES",
         "Tokyo protests a violation of its airspace by Russian aircraft."),
    ]
    for i, (scene, kick, head, cap) in enumerate(cells):
        x0 = M + i * (cw + 12)
        panel(d, [x0, y0, x0 + cw, y1])
        scene(d, x0 + 8, y0 + 8, cw - 16, 84)
        story_text(d, x0 + 12, y0 + 102, cw - 24, kick, head, cap, hsize=25, csize=18)

    # row of two ------------------------------------------------------
    y0, y1 = 740, 948
    cw2 = (W - 2 * M - 12) // 2
    cells2 = [
        (scene_cyber, "CYBERATTACK", "HACK SPREADS TO 178 WEBSITES",
         "Malicious code slipped in via Optimizely targeted visitors to CNN, BBC, "
         "Zoom and HSBC, stealing crypto and card data."),
        (scene_rocket, "SPACE", "VULCAN ROCKET FAILS, 40 SATELLITES LOST",
         "The ULA rocket breaks up minutes after liftoff from Florida, "
         "losing all 40 Amazon Leo satellites."),
    ]
    for i, (scene, kick, head, cap) in enumerate(cells2):
        x0 = M + i * (cw2 + 12)
        panel(d, [x0, y0, x0 + cw2, y1])
        scene(d, x0 + 8, y0 + 8, 168, y1 - y0 - 16)
        story_text(d, x0 + 188, y0 + 12, cw2 - 200, kick, head, cap, hsize=26, csize=18)

    # ticker ----------------------------------------------------------
    d.line([M, 960, W - M, 960], fill=INK, width=3)
    text_block(d, M, 968,
               "ALSO TODAY \u00b7 EU sanctions 101 Russia-linked entities \u00b7 UK sanctions West Bank "
               "settlement firms \u00b7 Drone strike kills 15 in Sudan \u00b7 ILO re-elects its chief",
               font(FB, 18), INK, W - 2 * M, align="center")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
