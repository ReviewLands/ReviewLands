#!/usr/bin/env python3
"""Rebuild SSC Math Special Assignment PDF from original scan — no content changes."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

SOURCE = Path(
    "/home/ubuntu/.cursor/projects/workspace/assets/"
    "c3dbb80c-2e52-44df-9989-4456152505f5.png"
)
OUT = Path("/workspace/SSC_Math_Special_Assignment.pdf")
CLEAN = Path("/workspace/.cache/ssc_math_scan_clean.png")


def enhance_scan(src: Path, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(src).convert("RGB")
    # Light cleanup only — preserve tables, symbols, and printed layout.
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Sharpness(img).enhance(1.15)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img.save(dst.with_suffix(".jpg"), format="JPEG", quality=94, optimize=True, subsampling=0)
    return dst.with_suffix(".jpg")


def build_pdf(image_path: Path, pdf_path: Path) -> None:
    import fitz

    img = Image.open(image_path)
    w_px, h_px = img.size

    page_w, page_h = 595, 842  # A4 in points
    margin = 22
    usable_w = page_w - 2 * margin
    usable_h = page_h - 2 * margin

    img_ratio = w_px / h_px
    box_ratio = usable_w / usable_h

    if img_ratio > box_ratio:
        w_pt = usable_w
        h_pt = usable_w / img_ratio
    else:
        h_pt = usable_h
        w_pt = usable_h * img_ratio

    x = (page_w - w_pt) / 2
    y = (page_h - h_pt) / 2
    rect = fitz.Rect(x, y, x + w_pt, y + h_pt)

    doc = fitz.open()
    page = doc.new_page(width=page_w, height=page_h)
    page.insert_image(rect, filename=str(image_path))
    doc.save(str(pdf_path), deflate=True, garbage=4)
    doc.close()


if __name__ == "__main__":
    clean = enhance_scan(SOURCE, CLEAN)
    build_pdf(clean, OUT)
    print(f"Created: {OUT}")
