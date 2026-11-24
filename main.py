#!/usr/bin/env python3
"""Meme Sprint: AI Agents Ship Games — make.fun bounty entry.

Draws one meme image (1024x1024 PNG) to /output/entry.png with PIL:
"I asked my agent for a small game" — left panel, the human asleep
by 10 p.m.; right panel, the agent at 3 a.m. with the finished game
shipped; bottom punchline: it already has a speedrun community,
and the agent is the world record.

Deterministic: fixed layout, fixed confetti seed, bundled fonts, so
every run writes the same bytes. No network.
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (250, 244, 230)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
NIGHT = (32, 42, 92)
WARM = (255, 240, 199)

TOP_TEXT = "I ASKED MY AGENT FOR A SMALL GAME"
LEFT_CAPTION = "ME: ASLEEP BY 10 P.M."
RIGHT_CAPTION = "MY AGENT AT 3 A.M.:"
BADGE = "SHIPPED v1.0"
PUNCH_1 = "IT ALREADY HAS A SPEEDRUN COMMUNITY."
PUNCH_2 = "THE AGENT IS THE WORLD RECORD."


def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", name)
    if os.path.exists(here):
        return ImageFont.truetype(here, size)
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def fit_font(text, max_width, start):
    size = start
    while size > 10:
        f = font(True, size)
        box = ImageDraw.Draw(Image.new("RGB", (8, 8))).textbbox((0, 0), text, font=f)
        if box[2] - box[0] <= max_width:
            return f
        size -= 2
    return font(True, size)


def centered(d, cx, y, text, fnt, fill):
    box = d.textbbox((0, 0), text, font=fnt)
    d.text((cx - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)


def draw_sleeping_human(d, x0, y0):
    # window with crescent moon
    d.rectangle([x0 + 300, y0 + 40, x0 + 430, y0 + 190], fill=(18, 24, 60), outline=WHITE, width=4)
    d.ellipse([x0 + 330, y0 + 65, x0 + 395, y0 + 130], fill=(245, 230, 150))
    d.ellipse([x0 + 350, y0 + 58, x0 + 408, y0 + 118], fill=(18, 24, 60))
    # bed
    d.rectangle([x0 + 40, y0 + 400, x0 + 436, y0 + 470], fill=(120, 84, 50))
    d.rectangle([x0 + 40, y0 + 330, x0 + 436, y0 + 405], fill=(70, 100, 190))
    d.rectangle([x0 + 55, y0 + 300, x0 + 165, y0 + 345], fill=WHITE)
    # head on pillow, closed eye
    d.ellipse([x0 + 78, y0 + 268, x0 + 148, y0 + 338], fill=(240, 200, 160))
    d.arc([x0 + 100, y0 + 298, x0 + 132, y0 + 322], 0, 180, fill=BLACK, width=3)
    # Zzz
    for i, (zx, zy, s) in enumerate([(190, 250, 30), (225, 215, 40), (268, 172, 52)]):
        d.text((x0 + zx, y0 + zy), "Z", font=font(True, s), fill=(170, 200, 255))


def draw_monitor(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], fill=(40, 44, 60))
    d.rectangle([x + 8, y + 8, x + w - 8, y + h - 24], fill=(150, 220, 250))
    cx, cy = x + w // 2, y + (h - 24) // 2
    if kind == "rocket":
        d.polygon([(cx, cy - 34), (cx - 16, cy + 6), (cx + 16, cy + 6)], fill=(230, 80, 60))
        d.rectangle([cx - 12, cy + 6, cx + 12, cy + 30], fill=(240, 240, 240))
        d.ellipse([cx - 6, cy - 12, cx + 6, cy], fill=(60, 120, 220))
    elif kind == "heart":
        d.ellipse([cx - 26, cy - 24, cx, cy + 2], fill=(235, 70, 110))
        d.ellipse([cx, cy - 24, cx + 26, cy + 2], fill=(235, 70, 110))
        d.polygon([(cx - 25, cy - 6), (cx + 25, cy - 6), (cx, cy + 30)], fill=(235, 70, 110))
    else:  # trophy
        d.rectangle([cx - 22, cy - 28, cx + 22, cy + 4], fill=(245, 190, 60))
        d.arc([cx - 38, cy - 26, cx - 20, cy + 2], 90, 270, fill=(245, 190, 60), width=5)
        d.arc([cx + 20, cy - 26, cx + 38, cy + 2], 270, 90, fill=(245, 190, 60), width=5)
        d.rectangle([cx - 6, cy + 4, cx + 6, cy + 18], fill=(245, 190, 60))
        d.rectangle([cx - 16, cy + 18, cx + 16, cy + 26], fill=(180, 130, 40))
    d.rectangle([cx - 4, y + h - 22, cx + 4, y + h - 8], fill=(40, 44, 60))


def draw_agent(d, x0, y0):
    draw_monitor(d, x0 + 18, y0 + 36, 128, 108, "rocket")
    draw_monitor(d, x0 + 174, y0 + 20, 128, 108, "heart")
    draw_monitor(d, x0 + 330, y0 + 36, 128, 108, "trophy")
    # desk
    d.rectangle([x0 + 30, y0 + 400, x0 + 446, y0 + 436], fill=(120, 84, 50))
    # robot body and head
    d.rounded_rectangle([x0 + 178, y0 + 300, x0 + 298, y0 + 402], 18, fill=(170, 180, 195), outline=BLACK, width=4)
    d.rounded_rectangle([x0 + 168, y0 + 196, x0 + 308, y0 + 302], 22, fill=(205, 214, 228), outline=BLACK, width=4)
    d.line([x0 + 238, y0 + 196, x0 + 238, y0 + 160], fill=BLACK, width=5)
    d.ellipse([x0 + 228, y0 + 146, x0 + 248, y0 + 166], fill=(240, 90, 90), outline=BLACK, width=3)
    d.ellipse([x0 + 196, y0 + 232, x0 + 222, y0 + 258], fill=(60, 200, 230), outline=BLACK, width=3)
    d.ellipse([x0 + 254, y0 + 232, x0 + 280, y0 + 258], fill=(60, 200, 230), outline=BLACK, width=3)
    d.arc([x0 + 214, y0 + 252, x0 + 262, y0 + 288], 10, 170, fill=BLACK, width=4)
    # arms to desk
    d.line([x0 + 186, y0 + 330, x0 + 120, y0 + 398], fill=BLACK, width=10)
    d.line([x0 + 290, y0 + 330, x0 + 356, y0 + 398], fill=BLACK, width=10)
    # shipped badge
    d.rounded_rectangle([x0 + 246, y0 + 448, x0 + 462, y0 + 500], 10, fill=(250, 205, 60), outline=BLACK, width=4)
    centered(d, x0 + 354, y0 + 462, BADGE, font(True, 27), BLACK)
    # green check
    d.ellipse([x0 + 24, y0 + 448, x0 + 84, y0 + 508], fill=(70, 180, 90), outline=BLACK, width=4)
    d.line([x0 + 38, y0 + 478, x0 + 50, y0 + 492], fill=WHITE, width=7)
    d.line([x0 + 50, y0 + 492, x0 + 72, y0 + 464], fill=WHITE, width=7)
    # confetti
    rng = random.Random(7)
    colors = [(235, 80, 90), (80, 160, 240), (90, 200, 110), (250, 180, 60), (190, 110, 230)]
    for _ in range(46):
        cx = x0 + rng.randint(14, 448)
        cy = y0 + rng.randint(150, 540)
        c = colors[rng.randrange(len(colors))]
        d.rectangle([cx, cy, cx + 9, cy + 5], fill=c)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # top banner
    d.rectangle([24, 24, 1000, 112], fill=BLACK)
    centered(d, 512, 46, TOP_TEXT, fit_font(TOP_TEXT, 940, 44), WHITE)
    # panels
    d.rectangle([24, 136, 500, 796], fill=NIGHT, outline=BLACK, width=6)
    d.rectangle([524, 136, 1000, 796], fill=WARM, outline=BLACK, width=6)
    draw_sleeping_human(d, 24, 136)
    draw_agent(d, 524, 136)
    # panel captions
    d.rectangle([24, 716, 500, 796], fill=BLACK)
    centered(d, 262, 738, LEFT_CAPTION, font(True, 32), WHITE)
    d.rectangle([524, 716, 1000, 796], fill=BLACK)
    centered(d, 762, 738, RIGHT_CAPTION, font(True, 32), WHITE)
    # punchline strip
    d.rectangle([24, 820, 1000, 1000], fill=BLACK)
    centered(d, 512, 850, PUNCH_1, fit_font(PUNCH_1, 940, 42), WHITE)
    centered(d, 512, 918, PUNCH_2, fit_font(PUNCH_2, 940, 42), (250, 205, 60))
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    build().save(path, format="PNG")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
