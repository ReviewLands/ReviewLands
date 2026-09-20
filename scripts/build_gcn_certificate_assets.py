#!/usr/bin/env python3
"""Build seal and signature PNG assets for GCN certificate."""
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from gcn_ink_effects import apply_ink_pad_stamp, on_paper_preview

ASSETS = Path("/workspace/certificates/assets")
CERTS = Path("/workspace/certificates")
ASSETS.mkdir(parents=True, exist_ok=True)

INK_BLUE = np.array([22, 68, 138], dtype=np.float32)
INK_RED = np.array([178, 32, 52], dtype=np.float32)
INK_GRAY = np.array([58, 58, 58], dtype=np.float32)


def _load_logo_icon(size: int = 88) -> Image.Image:
    logo = Image.open(ASSETS / "gcn-logo.png").convert("RGBA")
    _, h = logo.size
    side = h
    icon = logo.crop((0, 0, side, h)).resize((size, size), Image.Resampling.LANCZOS)
    return icon


def _draw_arc_text(
    base: Image.Image,
    text: str,
    cx: int,
    cy: int,
    radius: int,
    start_deg: float,
    end_deg: float,
    font: ImageFont.FreeTypeFont,
    ink: np.ndarray,
    alpha: int,
) -> None:
    for i, ch in enumerate(text):
        t = i / max(len(text) - 1, 1)
        ang = math.radians(start_deg + (end_deg - start_deg) * t)
        x = cx + int(radius * math.cos(ang))
        y = cy + int(radius * math.sin(ang))
        ch_img = Image.new("RGBA", (34, 34), (0, 0, 0, 0))
        color = tuple(ink.astype(int)) + (alpha,)
        ImageDraw.Draw(ch_img).text((2, 2), ch, fill=color, font=font)
        ch_img = ch_img.rotate(-math.degrees(ang) - 90, expand=True)
        base.alpha_composite(ch_img, (x - ch_img.width // 2, y - ch_img.height // 2))


def _build_seal_artwork() -> Image.Image:
    random.seed(42)
    size = 560
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 23)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font

    for r, ink, width, alpha in [
        (242, INK_BLUE, 11, 200),
        (226, INK_RED, 6, 185),
        (210, INK_BLUE, 4, 165),
    ]:
        col = tuple(ink.astype(int)) + (alpha,)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=width)

    _draw_arc_text(img, "GRAMEEN CYBERNET LTD.", cx, cy, 192, 200, 340, font, INK_BLUE, 215)
    _draw_arc_text(img, "DHAKA · BANGLADESH", cx, cy, 174, 22, 158, font_sm, INK_RED, 200)

    icon = _load_logo_icon(124)
    mask = Image.new("L", icon.size, 0)
    ImageDraw.Draw(mask).ellipse((2, 2, icon.size[0] - 2, icon.size[1] - 2), fill=255)
    icon.putalpha(mask)
    img.alpha_composite(icon, (cx - 62, cy - 68))

    est = Image.new("RGBA", (130, 26), (0, 0, 0, 0))
    ImageDraw.Draw(est).text(
        (0, 0), "EST. 1996", fill=tuple(INK_GRAY.astype(int)) + (210,), font=font_sm
    )
    img.alpha_composite(est, (cx - 50, cy + 54))
    return img


def build_seal(path: Path) -> Image.Image:
    img = apply_ink_pad_stamp(_build_seal_artwork(), seed=42)
    img = img.rotate(-13.5, resample=Image.Resampling.BICUBIC, expand=True)
    img.save(path, "PNG")

    named = CERTS / "GCN_seal_inkpad_stamp.png"
    preview = CERTS / "GCN_seal_on_paper_preview.jpg"
    img.save(named, "PNG")
    on_paper_preview(img).save(preview, "JPEG", quality=92)
    return img


def build_signature(path: Path) -> None:
    w, h = 640, 200
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ink = (12, 52, 122, 235)
    strokes = [
        [(18, 128), (42, 95), (78, 88), (118, 102), (156, 138)],
        [(168, 92), (198, 78), (236, 86), (268, 118), (292, 142)],
    ]
    for stroke in strokes:
        for i in range(len(stroke) - 1):
            draw.line([stroke[i], stroke[i + 1]], fill=ink, width=3, joint="curve")
    blur = img.filter(ImageFilter.GaussianBlur(0.45))
    img = Image.alpha_composite(img, blur)
    img.save(path, "PNG")


def main():
    build_seal(ASSETS / "gcn-company-seal.png")
    sig_path = ASSETS / "ghulam-mohiuddin-signature.png"
    if not sig_path.exists():
        build_signature(sig_path)
    print("Built:", ASSETS / "gcn-company-seal.png", sig_path)


if __name__ == "__main__":
    main()
