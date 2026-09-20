#!/usr/bin/env python3
"""Build seal and signature PNG assets for GCN certificate."""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ASSETS = Path("/workspace/certificates/assets")
ASSETS.mkdir(parents=True, exist_ok=True)


def _load_logo_icon(size: int = 88) -> Image.Image:
    logo = Image.open(ASSETS / "gcn-logo.png").convert("RGBA")
    # Crop to circular icon portion (left part of wide banner)
    _, h = logo.size
    side = h
    icon = logo.crop((0, 0, side, h)).resize((size, size), Image.Resampling.LANCZOS)
    return icon


def build_seal(path: Path) -> None:
    random.seed(42)
    size = 520
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # Outer stamp ring (Bangladesh corporate seal style: blue + inner red)
    for r, color, width in [
        (238, (18, 72, 140, 210), 10),
        (222, (196, 30, 58, 185), 5),
        (206, (18, 72, 140, 170), 3),
    ]:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=width)

    # Distressed ink specks
    speck = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(speck)
    for _ in range(900):
        x = random.randint(40, size - 40)
        y = random.randint(40, size - 40)
        if math.hypot(x - cx, y - cy) > 120 and math.hypot(x - cx, y - cy) < 245:
            sd.ellipse((x, y, x + 2, y + 2), fill=(18, 72, 140, random.randint(20, 70)))
    speck = speck.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img, speck)

    # Circular text (simplified arcs using repeated chars)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font

    top_text = "GRAMEEN CYBERNET LTD."
    bottom_text = "DHAKA · BANGLADESH"
    for i, ch in enumerate(top_text):
        ang = math.radians(200 + (i / max(len(top_text) - 1, 1)) * 140)
        x = cx + int(188 * math.cos(ang))
        y = cy + int(188 * math.sin(ang))
        ch_img = Image.new("RGBA", (30, 30), (0, 0, 0, 0))
        ImageDraw.Draw(ch_img).text((2, 2), ch, fill=(18, 72, 140, 220), font=font)
        ch_img = ch_img.rotate(-math.degrees(ang) - 90, expand=True)
        img.alpha_composite(ch_img, (x - ch_img.width // 2, y - ch_img.height // 2))

    for i, ch in enumerate(bottom_text):
        ang = math.radians(20 + (i / max(len(bottom_text) - 1, 1)) * 140)
        x = cx + int(170 * math.cos(ang))
        y = cy + int(170 * math.sin(ang))
        ch_img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        ImageDraw.Draw(ch_img).text((1, 1), ch, fill=(196, 30, 58, 210), font=font_sm)
        ch_img = ch_img.rotate(-math.degrees(ang) - 90, expand=True)
        img.alpha_composite(ch_img, (x - ch_img.width // 2, y - ch_img.height // 2))

    icon = _load_logo_icon(120)
    mask = Image.new("L", icon.size, 0)
    ImageDraw.Draw(mask).ellipse((2, 2, icon.size[0] - 2, icon.size[1] - 2), fill=255)
    icon.putalpha(mask)
    img.alpha_composite(icon, (cx - 60, cy - 66))

    est = Image.new("RGBA", (120, 24), (0, 0, 0, 0))
    ImageDraw.Draw(est).text((0, 0), "EST. 1996", fill=(60, 60, 60, 220), font=font_sm)
    img.alpha_composite(est, (cx - 48, cy + 52))

    # Slight rotation + ink bleed for stamped look
    img = img.rotate(-11, resample=Image.Resampling.BICUBIC, expand=True)
    img = img.filter(ImageFilter.GaussianBlur(0.35))
    img.save(path, "PNG")


def build_signature(path: Path) -> None:
    """Stylized MD signature in blue ink (placeholder until HR scan is provided)."""
    w, h = 640, 200
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Pen strokes approximating "Ghulam Mohiuddin"
    ink = (12, 52, 122, 235)
    strokes = [
        [(18, 128), (42, 95), (78, 88), (118, 102), (156, 138)],
        [(168, 92), (198, 78), (236, 86), (268, 118), (292, 142)],
        [(58, 142), (92, 156), (132, 150), (170, 128)],
        [(310, 98), (348, 86), (392, 94), (430, 124), (458, 148)],
        [(472, 88), (508, 76), (548, 88), (586, 118)],
        [(350, 152), (388, 162), (428, 154), (468, 132), (520, 118), (578, 128)],
    ]
    for stroke in strokes:
        for i in range(len(stroke) - 1):
            draw.line([stroke[i], stroke[i + 1]], fill=ink, width=3, joint="curve")
    draw.line([(602, 132), (622, 118)], fill=ink, width=2)

    # Light pressure variation
    blur = img.filter(ImageFilter.GaussianBlur(0.45))
    img = Image.alpha_composite(img, blur)
    img.save(path, "PNG")


def main():
    build_seal(ASSETS / "gcn-company-seal.png")
    build_signature(ASSETS / "ghulam-mohiuddin-signature.png")
    print("Built:", ASSETS / "gcn-company-seal.png", ASSETS / "ghulam-mohiuddin-signature.png")


if __name__ == "__main__":
    main()
