#!/usr/bin/env python3
"""Produce two A4 exam pages: clean crop + school-header replacement only."""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdfcanvas

WORK = Path("/tmp/exam-work")
OUT = Path("/workspace/exam_pages")
OUT.mkdir(parents=True, exist_ok=True)
SRC = Path("/workspace/exam_pages/source")
SRC.mkdir(parents=True, exist_ok=True)

FONT = "/usr/share/fonts/truetype/noto/NotoSerifBengali-Bold.ttf"
NEW_HEADER = "গাজীপুর ফাজিল মাদ্রাসা (চতর), বি.ও.এফ, গাজীপুর"
A4_PX = (2480, 3508)


def order_points(pts):
    pts = np.array(pts, dtype=np.float32)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).ravel()
    return np.array(
        [pts[np.argmin(s)], pts[np.argmin(d)], pts[np.argmax(s)], pts[np.argmax(d)]],
        np.float32,
    )


def warp_quad(img, pts):
    pts = order_points(pts)
    tl, tr, br, bl = pts
    w = int(max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl)))
    h = int(max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl)))
    dst = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], np.float32)
    M = cv2.getPerspectiveTransform(pts, dst)
    return cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_CUBIC)


def enhance(bgr):
    img = bgr.astype(np.float32)
    k = max(41, (min(img.shape[:2]) // 16) | 1)
    bg = cv2.GaussianBlur(img, (k, k), 0)
    mean_bg = float(np.clip(np.mean(bg), 90, 235))
    flat = img / np.maximum(bg, 8.0) * mean_bg
    lo, hi = np.percentile(flat, (0.7, 99.6))
    stretched = (flat - lo) * (255.0 / max(hi - lo, 1.0))
    mix = np.clip(0.32 * img + 0.68 * stretched, 0, 255).astype(np.uint8)
    blur = cv2.GaussianBlur(mix, (0, 0), 0.8)
    return cv2.addWeighted(mix, 1.22, blur, -0.22, 0)


def paint_header(bgr, y0, y1, x0_frac=0.10, x1_frac=0.90):
    h, w = bgr.shape[:2]
    x0, x1 = int(w * x0_frac), int(w * x1_frac)
    # Inpaint only the old school-name ink so paper texture stays natural
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(gray.shape, np.uint8)
    ink = (gray[y0:y1, x0:x1] < 155).astype(np.uint8) * 255
    ink = cv2.dilate(ink, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 5)), iterations=2)
    mask[y0:y1, x0:x1] = ink
    paper = cv2.inpaint(bgr, mask, 5, cv2.INPAINT_TELEA)
    # lift leftover dark specks toward local paper color
    band = paper[y0:y1, x0:x1].astype(np.float32)
    target = np.percentile(band.reshape(-1, 3), 88, axis=0)
    g = cv2.cvtColor(band.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    lift = np.clip((155 - g.astype(np.float32)) / 155.0, 0, 1)[..., None]
    band = band * (1 - 0.85 * lift) + target * (0.85 * lift)
    paper[y0:y1, x0:x1] = np.clip(band, 0, 255).astype(np.uint8)

    rgb = cv2.cvtColor(paper, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    draw = ImageDraw.Draw(pil)
    band_h = y1 - y0
    size = max(26, int(band_h * 0.70))
    font = ImageFont.truetype(FONT, size)
    bbox = draw.textbbox((0, 0), NEW_HEADER, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    while tw > (x1 - x0) * 0.97 and size > 16:
        size -= 1
        font = ImageFont.truetype(FONT, size)
        bbox = draw.textbbox((0, 0), NEW_HEADER, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = y0 + (band_h - th) // 2 - bbox[1]
    draw.text((tx, ty), NEW_HEADER, font=font, fill=(20, 20, 20))
    print(f"  header size={size} y={y0}:{y1} x={x0}:{x1} text=({tx},{ty})")
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)


def fit_a4(bgr, margin=24):
    h, w = bgr.shape[:2]
    canvas = np.full((A4_PX[1], A4_PX[0], 3), 255, np.uint8)
    aw, ah = A4_PX[0] - 2 * margin, A4_PX[1] - 2 * margin
    scale = min(aw / w, ah / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    resized = cv2.resize(bgr, (nw, nh), interpolation=cv2.INTER_CUBIC)
    x0 = (A4_PX[0] - nw) // 2
    y0 = (A4_PX[1] - nh) // 2
    canvas[y0 : y0 + nh, x0 : x0 + nw] = resized
    return canvas


def preview(bgr, name, max_side=980):
    h, w = bgr.shape[:2]
    s = max_side / max(h, w)
    cv2.imwrite(
        str(WORK / f"{name}.jpg"),
        cv2.resize(bgr, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA),
        [int(cv2.IMWRITE_JPEG_QUALITY), 93],
    )


P1 = [(130, 125), (1135, 85), (1160, 1480), (85, 1525)]
P2 = [(110, 80), (1115, 70), (1160, 1515), (70, 1540)]

img1 = cv2.imread(str(WORK / "src1.jpg"))
img2 = cv2.rotate(cv2.imread(str(WORK / "src2.jpg")), cv2.ROTATE_90_CLOCKWISE)

w1 = enhance(warp_quad(img1, P1))
w2 = enhance(warp_quad(img2, P2))
print("warped", w1.shape, w2.shape)

# Measured school-name bands on these warps (from 20px slices)
h1 = paint_header(w1, 38, 104, 0.06, 0.96)
h2 = paint_header(w2, 196, 248, 0.05, 0.96)

# Crop leftover tablecloth / adjacent page
p1 = h1[30:1382, 88:1028]
p2 = h2[184:1446, 32:1058]

preview(p1[: int(p1.shape[0] * 0.14)], "final1_top")
preview(p2[: int(p2.shape[0] * 0.16)], "final2_top")
preview(p1, "final1")
preview(p2, "final2")

a4_1 = fit_a4(p1)
a4_2 = fit_a4(p2)
preview(a4_1, "final1_a4", max_side=880)
preview(a4_2, "final2_a4", max_side=880)

jpg1 = OUT / "page1_creative_a4.jpg"
jpg2 = OUT / "page2_mcq_a4.jpg"
cv2.imwrite(str(jpg1), a4_1, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
cv2.imwrite(str(jpg2), a4_2, [int(cv2.IMWRITE_JPEG_QUALITY), 94])

pdf_path = OUT / "Gazipur_Fazil_Madrasa_Math_2page.pdf"
c = pdfcanvas.Canvas(str(pdf_path), pagesize=A4)
pw, ph = A4
for path in (jpg1, jpg2):
    c.drawImage(ImageReader(str(path)), 0, 0, width=pw, height=ph)
    c.showPage()
c.save()
print("PDF", pdf_path, pdf_path.stat().st_size)
print("JPGs", jpg1.stat().st_size, jpg2.stat().st_size)
