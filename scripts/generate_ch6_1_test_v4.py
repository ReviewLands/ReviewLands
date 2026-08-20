#!/usr/bin/env python3
"""Generate Class 8 Chapter 6.1 creative test PDF (v4)."""
import os
import urllib.request
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_PATH = "/tmp/NotoSansBengali-Regular.ttf"
if not os.path.exists(FONT_PATH):
    urllib.request.urlretrieve(
        "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansBengali/NotoSansBengali-Regular.ttf",
        FONT_PATH,
    )

pdfmetrics.registerFont(TTFont("Bengali", FONT_PATH))
pdfmetrics.registerFont(TTFont("BengaliBold", FONT_PATH))
FONT, FB = "Bengali", "BengaliBold"
W, H = A4
XM = 42
MAX_W = W - 2 * XM


def draw_wrapped(c, x, y, text, leading=12):
    c.setFont(FONT, 9.5)
    words = text.split(" ")
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, FONT, 9.5) <= MAX_W:
            line = test
        else:
            if line:
                c.drawString(x, y, line)
                y -= leading
            line = word
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_section_header(c, y, title, marks):
    c.setFont(FB, 11)
    c.drawString(XM, y, title)
    c.drawRightString(W - XM, y, str(marks))
    return y - 18


def draw_creative_q(c, y, num, stem_lines, ka, kha, ga):
    c.setFont(FB, 10)
    c.drawString(XM, y, f"সৃজনশীল প্রশ্ন {num}.")
    c.drawRightString(W - XM, y, "১০")
    y -= 14
    c.setFont(FONT, 9.5)
    for line in stem_lines:
        c.drawString(XM, y, line)
        y -= 12
    c.drawString(XM, y, f"(ক) {ka}")
    c.drawRightString(W - XM, y, "২")
    y -= 12
    c.drawString(XM, y, f"(খ) {kha}")
    c.drawRightString(W - XM, y, "৪")
    y -= 12
    c.drawString(XM, y, f"(গ) {ga}")
    c.drawRightString(W - XM, y, "৪")
    return y - 14


def draw_sol_block(c, y, title, lines):
    if y < 60:
        c.showPage()
        y = H - 42
    c.setFont(FB, 10.5)
    c.drawString(XM, y, title)
    y -= 14
    c.setFont(FONT, 9)
    for line in lines:
        if y < 40:
            c.showPage()
            y = H - 42
            c.setFont(FONT, 9)
        c.drawString(XM, y, line)
        y -= 11
    return y - 8


def build_question_paper(path):
    c = canvas.Canvas(path, pagesize=A4)
    y = H - 42
    c.setFont(FB, 17)
    c.drawCentredString(W / 2, y, "CLASS TEST")
    y -= 22
    c.setFont(FONT, 12)
    c.drawCentredString(W / 2, y, "Mathematics")
    y -= 16
    c.drawCentredString(W / 2, y, "Chapter 6.1 — Simultaneous Equations (অভিন্ন সহ সমীকরণ)")
    y -= 20
    c.setFont(FONT, 11)
    c.drawString(XM, y, "Time: 60 minutes")
    c.drawRightString(W - XM, y, "Full Marks: 60")
    y -= 18
    c.drawString(XM, y, "Name: _________________________    Roll: __________    Date: __________")
    y -= 16
    y = draw_wrapped(
        c,
        XM,
        y,
        "নির্দেশনা: সব প্রশ্নের উত্তর দাও। অনুশীলনী ৬.১ (পৃ. ১০৫) থেকে নির্বাচিত। প্রতিটি সৃজনশীল প্রশ্নের মান ১০। (ক = ২, খ = ৪, গ = ৪)",
    )
    y -= 6

    y = draw_section_header(
        c,
        y,
        "ক. প্রতিস্থাপন পদ্ধতি (অনুশীলনী ৬.১ — প্রশ্ন ৪, ১০, ১১)",
        "৩০",
    )

    sub_qs = [
        (
            "১",
            [
                "নিচের সমীকরণদ্বয় দেওয়া আছে (a ≠ 0, b ≠ 0):",
                "    x/a + y/b = 1/a + 1/b",
                "    x/a − y/b = 1/a − 1/b",
            ],
            "সমীকরণদ্বয়ের চলকগুলো কত ঘাতের?",
            "সমীকরণদ্বয় প্রতিস্থাপন পদ্ধতিতে সমাধান কর।",
            "সমীকরণদ্বয় অপনয়ন পদ্ধতিতে সমাধান কর।",
        ),
        (
            "২",
            [
                "নিচের সমীকরণদ্বয় দেওয়া আছে:",
                "    1/x + 1/y = 5/6",
                "    1/x − 1/y = 1/6",
            ],
            "সমীকরণদ্বয়ের চলক চিহ্নিত কর।",
            "সমীকরণদ্বয় প্রতিস্থাপন পদ্ধতিতে সমাধান কর।",
            "প্রাপ্ত সমাধানের শুদ্ধি পরীক্ষা কর।",
        ),
        (
            "৩",
            [
                "নিচের সমীকরণদ্বয় দেওয়া আছে (a ≠ 0, b ≠ 0):",
                "    x/a + y/b = 2/a + 1/b",
                "    x/b − y/a = 2/b − 1/a",
            ],
            "সমীকরণদ্বয়ে কোন কোন চলক ব্যবহৃত হয়েছে?",
            "সমীকরণদ্বয় প্রতিস্থাপন পদ্ধতিতে সমাধান কর।",
            "সমীকরণদ্বয় অপনয়ন পদ্ধতিতে সমাধান কর।",
        ),
    ]

    for num, stem, ka, kha, ga in sub_qs:
        y = draw_creative_q(c, y, num, stem, ka, kha, ga)

    c.setFont(FONT, 9)
    c.drawRightString(W - XM, y, "Section ক: 3 × 10 = 30")

    c.showPage()
    y = H - 42
    c.setFont(FB, 12)
    c.drawCentredString(W / 2, y, "CLASS TEST — (খ অংশ)")
    y -= 22
    y = draw_section_header(
        c,
        y,
        "খ. অপনয়ন পদ্ধতি (অনুশীলনী ৬.১ — প্রশ্ন ১৯, ২২, ২৬)",
        "৩০",
    )

    elim_qs = [
        (
            "৪",
            [
                "নিচের সমীকরণদ্বয় দেওয়া আছে:",
                "    x/2 + y/2 = 3",
                "    x/2 − y/2 = 1",
            ],
            "সমীকরণদ্বয় কোন ধরনের সমীকরণ?",
            "সমীকরণদ্বয় অপনয়ন পদ্ধতিতে সমাধান কর।",
            "সমীকরণদ্বয় প্রতিস্থাপন পদ্ধতিতে সমাধান কর।",
        ),
        (
            "৫",
            [
                "নিচের সমীকরণদ্বয় দেওয়া আছে:",
                "    x/3 + 2/y = 1",
                "    x/4 − 3/y = 3",
            ],
            "প্রথম সমীকরণে x এর ঘাত কত?",
            "সমীকরণদ্বয় অপনয়ন পদ্ধতিতে সমাধান কর।",
            "প্রাপ্ত সমাধানের শুদ্ধি পরীক্ষা কর।",
        ),
        (
            "৬",
            [
                "নিচের সমীকরণদ্বয় দেওয়া আছে (a, b ধনাত্মক):",
                "    x + y = a − b",
                "    ax − by = a² + b²",
            ],
            "দ্বিতীয় সমীকরণে y এর ঘাত কত?",
            "সমীকরণদ্বয় অপনয়ন পদ্ধতিতে সমাধান কর।",
            "সমীকরণদ্বয় প্রতিস্থাপন পদ্ধতিতে সমাধান কর।",
        ),
    ]

    for num, stem, ka, kha, ga in elim_qs:
        y = draw_creative_q(c, y, num, stem, ka, kha, ga)

    c.setFont(FONT, 9)
    c.drawRightString(W - XM, y, "Section খ: 3 × 10 = 30")
    c.drawRightString(W - XM, y - 12, "Total: 6 × 10 = 60")
    c.save()


def build_solutions(path):
    c = canvas.Canvas(path, pagesize=A4)
    y = H - 42
    c.setFont(FB, 14)
    c.drawCentredString(W / 2, y, "সমাধান (Answer Key)")
    y -= 14
    c.setFont(FONT, 10)
    c.drawCentredString(W / 2, y, "অনুশীলনী ৬.১ — Chapter 6.1 | Full Marks: 60")
    y -= 24

    solutions = [
        (
            "১নং প্রশ্ন (অনুশীলনী ৬.১ — ৪)",
            [
                "দেওয়া: x/a + y/b = 1/a + 1/b  ... (i)",
                "      x/a − y/b = 1/a − 1/b  ... (ii)",
                "(ক) উভয় সমীকরণে x ও y এর ঘাত ১। ∴ চলকগুলোর ঘাত ১।",
                "(খ) প্রতিস্থাপন:",
                "সমীকরণ (ii) থেকে, x/a = 1/a − 1/b + y/b  ... (iii)",
                "সমীকরণ (iii) এর x/a এর মান (i) এ বসিয়ে ও সরল করলে: y = 1",
                "সমীকরণ (iii) এ y = 1: x/a = 1/a − 1/b + 1/b = 1/a → x = 1",
                "∴ নির্ণেয় সমাধান (x, y) = (1, 1)",
                "(গ) অপনয়ন:",
                "সমীকরণ (i) + (ii): 2x/a = 2/a → x = 1",
                "সমীকরণ (i) − (ii): 2y/b = 2/b → y = 1",
                "∴ (x, y) = (1, 1)",
            ],
        ),
        (
            "২নং প্রশ্ন (অনুশীলনী ৬.১ — ১০)",
            [
                "দেওয়া: 1/x + 1/y = 5/6  ... (i)",
                "      1/x − 1/y = 1/6  ... (ii)",
                "(ক) চলক: x ও y।",
                "(খ) প্রতিস্থাপন:",
                "সমীকরণ (ii) থেকে, 1/x = 1/y + 1/6  ... (iii)",
                "সমীকরণ (iii) এর মান (i) এ: 1/y + 1/6 + 1/y = 5/6",
                "2/y + 1/6 = 5/6 → 2/y = 4/6 = 2/3 → y = 3",
                "সমীকরণ (iii) এ: 1/x = 1/3 + 1/6 = 1/2 → x = 2",
                "∴ (x, y) = (2, 3)",
                "(গ) শুদ্ধি: 1/2 + 1/3 = 5/6 ✓; 1/2 − 1/3 = 1/6 ✓",
            ],
        ),
        (
            "৩নং প্রশ্ন (অনুশীলনী ৬.১ — ১১)",
            [
                "দেওয়া: x/a + y/b = 2/a + 1/b  ... (i)",
                "      x/b − y/a = 2/b − 1/a  ... (ii)",
                "(ক) চলক: x ও y।",
                "(খ) প্রতিস্থাপন:",
                "সমীকরণ (ii) থেকে, x/b = 2/b − 1/a + y/a  ... (iii)",
                "সমীকরণ (iii) এর x/b এর মান (i) এ বসিয়ে ও সরল করলে: y = 1",
                "সমীকরণ (iii) এ y = 1: x/b = 2/b − 1/a + 1/a = 2/b → x = 2",
                "∴ (x, y) = (2, 1)",
                "(গ) অপনয়ন:",
                "সমীকরণ (i) × b: x + by/b = 2b/a + 1 → x + y = 2b/a + 1",
                "সমীকরণ (ii) × a: ax/b − y = 2a/b − 1",
                "সরল করলে: x = 2, y = 1",
                "∴ (x, y) = (2, 1)",
            ],
        ),
        (
            "৪নং প্রশ্ন (অনুশীলনী ৬.১ — ১৯)",
            [
                "দেওয়া: x/2 + y/2 = 3  ... (i)  →  x + y = 6  ... (iii)",
                "      x/2 − y/2 = 1  ... (ii)  →  x − y = 2  ... (iv)",
                "(ক) দুটি সরল সমীকরণ (এক ঘাত দুই চলক)।",
                "(খ) অপনয়ন:",
                "সমীকরণ (iii) + (iv): 2x = 8 → x = 4",
                "সমীকরণ (iii) − (iv): 2y = 4 → y = 2",
                "∴ (x, y) = (4, 2)",
                "(গ) প্রতিস্থাপন:",
                "সমীকরণ (iv) থেকে, x = y + 2  ... (v)",
                "সমীকরণ (v) এর মান (iii) এ: y + 2 + y = 6 → y = 2, x = 4",
                "∴ (x, y) = (4, 2)",
            ],
        ),
        (
            "৫নং প্রশ্ন (অনুশীলনী ৬.১ — ২২)",
            [
                "দেওয়া: x/3 + 2/y = 1  ... (i)",
                "      x/4 − 3/y = 3  ... (ii)",
                "(ক) x এর ঘাত ১।",
                "(খ) অপনয়ন:",
                "ধরি, 1/y = u। সমীকরণ (i): x/3 + 2u = 1  ... (iii)",
                "সমীকরণ (ii): x/4 − 3u = 3  ... (iv)",
                "সমীকরণ (iii) × 12: 4x + 24u = 12  ... (v)",
                "সমীকরণ (iv) × 12: 3x − 36u = 36  ... (vi)",
                "সমীকরণ (v) − (vi): x + 60u = −24",
                "সমীকরণ (iii) ও (iv) থেকে: u = −1/2 → 1/y = −1/2 → y = −2",
                "সমীকরণ (i) এ: x/3 + 2/(−2) = 1 → x/3 = 2 → x = 6",
                "∴ (x, y) = (6, −2)",
                "(গ) শুদ্ধি: 6/3 + 2/(−2) = 2 − 1 = 1 ✓",
                "6/4 − 3/(−2) = 1.5 + 1.5 = 3 ✓",
            ],
        ),
        (
            "৬নং প্রশ্ন (অনুশীলনী ৬.১ — ২৬)",
            [
                "দেওয়া: x + y = a − b  ... (i)",
                "      ax − by = a² + b²  ... (ii)",
                "(ক) y এর ঘাত ১।",
                "(খ) অপনয়ন:",
                "সমীকরণ (i) × b: bx + by = ab − b²  ... (iii)",
                "সমীকরণ (ii) + (iii): ax + bx = a² + b² + ab − b²",
                "x(a + b) = a² + ab = a(a + b) → x = a  (a + b ≠ 0)",
                "সমীকরণ (i) এ: a + y = a − b → y = −b",
                "∴ (x, y) = (a, −b)",
                "(গ) প্রতিস্থাপন:",
                "সমীকরণ (i) থেকে, y = a − b − x  ... (iii)",
                "সমীকরণ (iii) এর মান (ii) এ: ax − b(a − b − x) = a² + b²",
                "ax − ab + b² + bx = a² + b² → x(a + b) = a² + ab → x = a",
                "y = a − b − a = −b",
                "∴ (x, y) = (a, −b)",
            ],
        ),
    ]

    for title, lines in solutions:
        y = draw_sol_block(c, y, title, lines)

    c.save()


if __name__ == "__main__":
    q_path = "/workspace/Class_Test_Chapter_6_1_Creative_v4.pdf"
    s_path = "/workspace/Class_Test_Chapter_6_1_Creative_v4_Solutions.pdf"
    build_question_paper(q_path)
    build_solutions(s_path)
    print("Created:", q_path)
    print("Created:", s_path)
