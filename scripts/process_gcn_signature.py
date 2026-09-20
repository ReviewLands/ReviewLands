#!/usr/bin/env python3
"""Turn a scanned/photo signature into a transparent PNG for the certificate."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ASSETS = Path("/workspace/certificates/assets")
DEFAULT_SRC = ASSETS / "ghulam-mohiuddin-signature-source.jpg"
OUT = ASSETS / "ghulam-mohiuddin-signature.png"


def process(src: Path, out: Path, target_width: int = 280) -> None:
    img = Image.open(src).convert("RGB")
    arr = np.array(img)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    ink = np.clip((255 - lum) / 255.0, 0, 1)
    ink = np.where(lum < 245, ink, 0)

    r = (12 + (1 - ink) * 255).astype(np.uint8)
    g = (48 + (1 - ink) * 255).astype(np.uint8)
    b = (118 + (1 - ink) * 255).astype(np.uint8)
    a = (ink * 235).astype(np.uint8)

    sig = Image.fromarray(np.dstack([r, g, b, a]).astype(np.uint8), "RGBA")
    sig = sig.filter(ImageFilter.GaussianBlur(0.35))
    arr2 = np.array(sig)
    arr2[:, :, 3] = np.minimum(arr2[:, :, 3], a)
    sig = Image.fromarray(arr2, "RGBA")

    bbox = sig.getbbox()
    if bbox:
        pad = 8
        sig = sig.crop(
            (
                max(0, bbox[0] - pad),
                max(0, bbox[1] - pad),
                min(sig.width, bbox[2] + pad),
                min(sig.height, bbox[3] + pad),
            )
        )

    scale = target_width / sig.width
    sig = sig.resize((target_width, int(sig.height * scale)), Image.Resampling.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    sig.save(out, "PNG")


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    process(src, OUT)
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
