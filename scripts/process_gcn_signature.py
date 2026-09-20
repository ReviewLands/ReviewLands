#!/usr/bin/env python3
"""Turn uploaded G. Mohiuddin signature into pen-ink PNG for the certificate."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from gcn_ink_effects import apply_pen_ink_signature, on_paper_preview

ASSETS = Path("/workspace/certificates/assets")
CERTS = Path("/workspace/certificates")
DEFAULT_SRC = ASSETS / "ghulam-mohiuddin-signature-source.jpg"
OUT = ASSETS / "ghulam-mohiuddin-signature.png"
OUT_NAMED = CERTS / "G_Mohiuddin_signature_ink_style.png"
OUT_PREVIEW = CERTS / "G_Mohiuddin_signature_on_paper_preview.png"


def extract_signature_rgba(img: Image.Image) -> Image.Image:
    arr = np.array(img.convert("RGB"))
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    ink = np.clip((255 - lum) / 255.0, 0, 1)
    ink = np.where(lum < 245, ink, 0)
    a = (ink * 255).astype(np.uint8)
    rgba = np.zeros((*arr.shape[:2], 4), dtype=np.uint8)
    rgba[:, :, 3] = a
    return Image.fromarray(rgba, "RGBA")


def process(src: Path, out: Path, target_width: int = 300) -> Image.Image:
    img = Image.open(src).convert("RGB")
    sig = extract_signature_rgba(img)
    sig = apply_pen_ink_signature(sig)

    bbox = sig.getbbox()
    if bbox:
        pad = 10
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
    sig = sig.filter(ImageFilter.GaussianBlur(0.15))

    out.parent.mkdir(parents=True, exist_ok=True)
    sig.save(out, "PNG")
    return sig


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    sig = process(src, OUT)
    sig.save(OUT_NAMED, "PNG")
    on_paper_preview(sig).save(OUT_PREVIEW, "JPEG", quality=92)
    print("Wrote", OUT, OUT_NAMED, OUT_PREVIEW)


if __name__ == "__main__":
    main()
