#!/usr/bin/env python3
"""Shared ink-on-paper effects for GCN certificate assets."""
import numpy as np
from PIL import Image, ImageFilter


def blur_channel(channel: np.ndarray, sigma: float = 3.0) -> np.ndarray:
    ch = channel.astype(np.float32)
    lo, hi = ch.min(), ch.max()
    if hi - lo < 1e-6:
        return ch
    norm = (ch - lo) / (hi - lo)
    img = Image.fromarray((norm * 255).astype(np.uint8), mode="L")
    img = img.filter(ImageFilter.GaussianBlur(sigma))
    blurred = np.array(img).astype(np.float32) / 255.0
    return blurred * (hi - lo) + lo


def apply_ink_pad_stamp(seal: Image.Image, seed: int = 42) -> Image.Image:
    """Rubber stamp pressed from ink pad onto paper."""
    rng = np.random.default_rng(seed)
    arr = np.array(seal).astype(np.float32)
    h, w = arr.shape[:2]
    cx, cy = w / 2.0, h / 2.0

    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    max_r = min(cx, cy) * 0.98

    pressure = 1.0 - 0.30 * (dist / max_r) ** 1.35
    pressure *= 1.0 + 0.14 * ((xx - cx) / w + (yy - cy) / h)

    blot = rng.normal(1.0, 0.2, (h, w)).astype(np.float32)
    blot = blur_channel(blot, sigma=16)
    blot = np.clip(blot, 0.42, 1.18)

    grain = rng.normal(1.0, 0.09, (h, w)).astype(np.float32)
    grain = blur_channel(grain, sigma=1.3)
    grain = np.clip(grain, 0.68, 1.28)

    ink_mask = pressure * blot * grain
    skips = rng.random((h, w)) > 0.991
    ink_mask[skips] *= 0.12

    alpha = (arr[:, :, 3] / 255.0) * ink_mask
    alpha = np.clip(alpha, 0, 1)

    rgb = arr[:, :, :3]
    for c in range(3):
        rgb[:, :, c] = rgb[:, :, c] * (0.82 + 0.18 * ink_mask)

    out = np.zeros_like(arr)
    out[:, :, :3] = np.clip(rgb, 0, 255)
    out[:, :, 3] = alpha * 255.0

    result = Image.fromarray(out.astype(np.uint8), "RGBA")
    return result.filter(ImageFilter.GaussianBlur(0.6))


def apply_pen_ink_signature(sig: Image.Image, seed: int = 7) -> Image.Image:
    """Ballpoint / pen ink on paper for G. Mohiuddin signature."""
    rng = np.random.default_rng(seed)
    arr = np.array(sig).astype(np.float32)
    h, w = arr.shape[:2]
    stroke = arr[:, :, 3] / 255.0
    if stroke.max() < 1e-6:
        return sig

    # Pressure variation along signature (darker mid-body, lighter tails)
    yy, xx = np.mgrid[0:h, 0:w]
    x_norm = xx / max(w - 1, 1)
    pressure = 0.75 + 0.35 * np.sin(np.pi * x_norm) ** 0.85
    pressure *= 0.9 + 0.2 * (1.0 - yy / max(h, 1))

    grain = rng.normal(1.0, 0.06, (h, w)).astype(np.float32)
    grain = blur_channel(grain, sigma=0.9)
    grain = np.clip(grain, 0.75, 1.2)

    ink_mask = stroke * pressure * grain
    micro = rng.random((h, w)) > 0.996
    ink_mask[micro] *= 0.2

    # Blue-black pen ink
    ink_rgb = np.array([12, 48, 118], dtype=np.float32)
    out = np.zeros_like(arr)
    for c in range(3):
        out[:, :, c] = ink_rgb[c] * (0.7 + 0.3 * ink_mask)
    out[:, :, 3] = np.clip(ink_mask * 240, 0, 255)

    result = Image.fromarray(out.astype(np.uint8), "RGBA")
    # Feathered bleed into paper fibres
    bleed = result.filter(ImageFilter.GaussianBlur(0.42))
    return Image.alpha_composite(bleed, result)


def on_paper_preview(asset: Image.Image, paper: tuple[int, int, int] = (252, 250, 246)) -> Image.Image:
    """White/cream paper preview for standalone downloads."""
    w, h = asset.size
    base = Image.new("RGB", (w + 80, h + 80), paper)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer.alpha_composite(asset, (40, 40))
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")
