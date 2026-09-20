#!/usr/bin/env python3
"""Build seal and signature PNG assets for GCN certificate."""
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ASSETS = Path("/workspace/certificates/assets")
ASSETS.mkdir(parents=True, exist_ok=True)

# Typical rubber-stamp pad inks (Bangladesh corporate seals)
INK_BLUE = np.array([22, 68, 138], dtype=np.float32)
INK_RED = np.array([178, 32, 52], dtype=np.float32)
INK_GRAY = np.array([58, 58, 58], dtype=np.float32)


def _load_logo_icon(size: int = 88) -> Image.Image:
    logo = Image.open(ASSETS / "gcn-logo.png").convert("RGBA")
    _, h = logo.size
    side = h
    icon = logo.crop((0, 0, side, h)).resize((size, size), Image.Resampling.LANCZOS)
    return icon


def _blur_array(channel: np.ndarray, sigma: float = 3.0) -> np.ndarray:
    ch = channel.astype(np.float32)
    lo, hi = ch.min(), ch.max()
    if hi - lo < 1e-6:
        return ch
    norm = (ch - lo) / (hi - lo)
    img = Image.fromarray((norm * 255).astype(np.uint8), mode="L")
    img = img.filter(ImageFilter.GaussianBlur(sigma))
    blurred = np.array(img).astype(np.float32) / 255.0
    return blurred * (hi - lo) + lo


def _apply_ink_pad_effect(seal: Image.Image, seed: int = 42) -> Image.Image:
    """Simulate uneven ink transfer from rubber stamp onto paper."""
    rng = np.random.default_rng(seed)
    arr = np.array(seal).astype(np.float32)
    h, w = arr.shape[:2]
    cx, cy = w / 2.0, h / 2.0

    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    max_r = min(cx, cy) * 0.98

    # Hand-press: slightly heavier on lower-right (common stamp angle)
    pressure = 1.0 - 0.28 * (dist / max_r) ** 1.35
    pressure *= 1.0 + 0.12 * ((xx - cx) / w + (yy - cy) / h)

    # Large blotches (dry pad / uneven sponge)
    blot = rng.normal(1.0, 0.18, (h, w)).astype(np.float32)
    blot = _blur_array(blot, sigma=14)
    blot = np.clip(blot, 0.45, 1.15)

    # Fine grain
    grain = rng.normal(1.0, 0.08, (h, w)).astype(np.float32)
    grain = _blur_array(grain, sigma=1.2)
    grain = np.clip(grain, 0.7, 1.25)

    ink_mask = pressure * blot * grain

    # Occasional micro skips (paper texture / missed ink)
    skips = rng.random((h, w)) > 0.992
    ink_mask[skips] *= 0.15

    alpha = arr[:, :, 3] / 255.0
    alpha = alpha * ink_mask
    alpha = np.clip(alpha, 0, 1)

    # Ink on paper: slightly desaturate + multiply-like darkening on RGB
    rgb = arr[:, :, :3]
    for c in range(3):
        rgb[:, :, c] = rgb[:, :, c] * (0.85 + 0.15 * ink_mask)

    out = np.zeros_like(arr)
    out[:, :, :3] = np.clip(rgb, 0, 255)
    out[:, :, 3] = alpha * 255.0

    result = Image.fromarray(out.astype(np.uint8), "RGBA")
    # Soft stamp edge bleed (ink spreads on paper fibres)
    result = result.filter(ImageFilter.GaussianBlur(0.55))
    return result


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


def build_seal(path: Path) -> None:
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

    # Ink-pad rings (slightly irregular widths)
    for r, ink, width, alpha in [
        (242, INK_BLUE, 11, 200),
        (226, INK_RED, 6, 185),
        (210, INK_BLUE, 4, 165),
    ]:
        col = tuple(ink.astype(int)) + (alpha,)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=width)

    _draw_arc_text(
        img,
        "GRAMEEN CYBERNET LTD.",
        cx,
        cy,
        192,
        200,
        340,
        font,
        INK_BLUE,
        215,
    )
    _draw_arc_text(
        img,
        "DHAKA · BANGLADESH",
        cx,
        cy,
        174,
        22,
        158,
        font_sm,
        INK_RED,
        200,
    )

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

    img = _apply_ink_pad_effect(img, seed=42)
    # Stamp placement angle (pressed onto paper)
    img = img.rotate(-13.5, resample=Image.Resampling.BICUBIC, expand=True)
    img.save(path, "PNG")


def build_signature(path: Path) -> None:
    """Stylized MD signature in blue ink (placeholder until HR scan is provided)."""
    w, h = 640, 200
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

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
