#!/usr/bin/env python3
"""Class 8 Chapter 6.1 CLASS TEST — clean layout, integer equations only (no fractions)."""
import os
import urllib.request
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BENGALI_FONT = "/tmp/NotoSansBengali-Regular.ttf"
if not os.path.exists(BENGALI_FONT):
    urllib.request.urlretrieve(
        "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansBengali/NotoSansBengali-Regular.ttf",
        BENGALI_FONT,
    )

pdfmetrics.registerFont(TTFont("Bengali", BENGALI_FONT))
pdfmetrics.registerFont(TTFont("BengaliBold", BENGALI_FONT))

W, H = A4
XM = 48
EN = "Times-Roman"
ENB = "Times-Bold"
BN = "Bengali"
BNB = "BengaliBold"


def draw_centre(c, y, text, font=EN, size=12):
    c.setFont(font, size)
    c.drawCentredString(W / 2, y, text)


def draw_marks(c, y, marks, size=11):
    c.setFont(EN, size)
    c.drawRightString(W - XM, y, str(marks))


def draw_eq_pair(c, x, y, eq1, eq2, indent=20):
    c.setFont(EN, 11)
    c.drawString(x + indent, y, eq1)
    y -= 15
    c.drawString(x + indent, y, eq2)
    return y - 8


def draw_problem(c, y, label, prompt, eq1, eq2):
    c.setFont(EN, 11)
    c.drawString(XM, y, label)
    draw_marks(c, y, 5)
    y -= 16
    c.drawString(XM + 4, y, prompt)
    y -= 16
    y = draw_eq_pair(c, XM, y, eq1, eq2, indent=16)
    return y - 4


def draw_elim_section(c, y, section_num="১"):
    c.setFont(BNB, 11)
    title = f"{section_num}. সৃজনশীল প্রশ্ন — অপনয়ন পদ্ধতি"
    c.drawString(XM, y, title)
    draw_marks(c, y, 15)
    y -= 22

    items = [
        ("(ক)", "Solve by the elimination method:", "x + y = 6", "x - y = 2"),
        ("(খ)", "Solve by the elimination method:", "5x + 3y = 24", "4x - y = 26"),
        ("(গ)", "Solve by the elimination method:", "x + y = 3", "5x - 2y = 29"),
    ]
    for label, prompt, eq1, eq2 in items:
        y = draw_problem(c, y, label, prompt, eq1, eq2)
    return y


def draw_sub_section(c, y, section_num="২"):
    c.setFont(BNB, 11)
    title = f"{section_num}. সৃজনশীল প্রশ্ন — প্রতিস্থাপন পদ্ধতি"
    c.drawString(XM, y, title)
    draw_marks(c, y, 15)
    y -= 22

    items = [
        ("(ক)", "Solve by the substitution method:", "3x + 2y = 5", "3x - 2y = 1"),
        ("(খ)", "Solve by the substitution method:", "2x + 3y = 13", "2x - 3y = -5"),
        ("(গ)", "Solve by the substitution method:", "3x + 2y = 7", "2x - 3y = 1"),
    ]
    for label, prompt, eq1, eq2 in items:
        y = draw_problem(c, y, label, prompt, eq1, eq2)
    return y


def draw_test_copy(c, y_top):
    y = y_top
    draw_centre(c, y, "CLASS TEST", ENB, 18)
    y -= 22
    draw_centre(c, y, "Mathematics", EN, 12)
    y -= 16
    draw_centre(c, y, "Chapter 6.1 — Simultaneous Equations", EN, 11)
    y -= 18
    c.setFont(EN, 11)
    c.drawString(XM, y, "Time: 45 minutes")
    c.drawRightString(W - XM, y, "Full Marks: 30")
    y -= 18
    c.drawString(XM, y, "Name: _________________________    Roll: __________    Date: __________")
    y -= 16
    c.setFont(BN, 10)
    c.drawString(XM, y, "নির্দেশনা: সব প্রশ্নের উত্তর দাও। প্রতিটি উপ-প্রশ্নের মান ৫। (অনুশীলনী ৬.১ — ভগ্নাংশমুক্ত)")
    y -= 22

    y = draw_elim_section(c, y)
    y -= 8
    y = draw_sub_section(c, y)
    c.setFont(EN, 10)
    c.drawRightString(W - XM, y - 6, "Total: 6 x 5 = 30")


def build_question_paper(path):
    c = canvas.Canvas(path, pagesize=A4)
    mid = H / 2

    draw_test_copy(c, H - 42)

    c.setDash(4, 4)
    c.line(XM, mid + 6, W - XM, mid + 6)
    c.setDash()
    c.setFont(EN, 9)
    c.drawCentredString(W / 2, mid - 2, "— CUT HERE —")

    draw_test_copy(c, mid - 44)
    c.save()


def draw_sol_lines(c, y, lines):
    for line in lines:
        if y < 40:
            c.showPage()
            y = H - 42
        if line.startswith("(") and line[1] in "কখগ":
            c.setFont(BNB, 10)
        elif line.endswith("...") or "সমীকরণ" in line[:20]:
            c.setFont(EN, 10)
        else:
            c.setFont(BN, 9.5)
        c.drawString(XM, y, line)
        y -= 12
    return y - 6


def build_solutions(path):
    c = canvas.Canvas(path, pagesize=A4)
    y = H - 42
    draw_centre(c, y, "সমাধান (Answer Key)", BNB, 14)
    y -= 16
    draw_centre(c, y, "Chapter 6.1 — Integer equations | Full Marks: 30", EN, 10)
    y -= 24

    blocks = [
        (
            "১. অপনয়ন পদ্ধতি (অনুশীলনী ৬.১ — ১৯, ২২, ২৬)",
            [
                "(ক) x + y = 6, x − y = 2",
                "যোগ: 2x = 8 → x = 4; y = 6 − 4 = 2",
                "∴ (x, y) = (4, 2)  [প্রশ্ন ১৯]",
                "(খ) 5x + 3y = 24, 4x − y = 26",
                "দ্বিতীয় সমীকরণ: y = 4x − 26 ... (iii)",
                "প্রতিস্থাপন: 5x + 3(4x − 26) = 24 → 17x = 102 → x = 6",
                "y = 4(6) − 26 = −2",
                "∴ (x, y) = (6, −2)  [প্রশ্ন ২২]",
                "(গ) x + y = 3, 5x − 2y = 29",
                "x + y = 3 ... (i); 5x − 2y = 29 ... (ii)",
                "(i) × 2: 2x + 2y = 6 ... (iii)",
                "(ii) + (iii): 7x = 35 → x = 5",
                "y = 3 − 5 = −2",
                "∴ (x, y) = (5, −2)  [প্রশ্ন ২৬; a=5, b=2]",
            ],
        ),
        (
            "২. প্রতিস্থাপন পদ্ধতি (অনুশীলনী ৬.১ — ৪, ১০, ১১)",
            [
                "(ক) 3x + 2y = 5, 3x − 2y = 1",
                "সমীকরণ (ii) থেকে: 3x = 1 + 2y ... (iii)",
                "সমীকরণ (iii) এর মান (i) এ: 1 + 2y + 2y = 5 → y = 1",
                "3x = 3 → x = 1",
                "∴ (x, y) = (1, 1)  [প্রশ্ন ৪]",
                "(খ) 2x + 3y = 13, 2x − 3y = −5",
                "সমীকরণ (ii) থেকে: 2x = −5 + 3y ... (iii)",
                "সমীকরণ (iii) এর মান (i) এ: −5 + 3y + 3y = 13 → y = 3",
                "2x = −5 + 9 = 4 → x = 2",
                "∴ (x, y) = (2, 3)  [প্রশ্ন ১০]",
                "(গ) 3x + 2y = 7, 2x − 3y = 1",
                "সমীকরণ (ii) থেকে: 2x = 1 + 3y ... (iii)",
                "সমীকরণ (iii) এর মান (i) এ: 3(1 + 3y)/2 + 2y = 7",
                "বা, (iii) × 3: 9x = 3 + 9y; (i) × 2: 6x + 4y = 14",
                "সহজ পদ্ধতি: (iii) এ x = (1 + 3y)/2 → 3y + 2 = 7 → y = 1, x = 2",
                "∴ (x, y) = (2, 1)  [প্রশ্ন ১১]",
            ],
        ),
    ]

    for title, lines in blocks:
        c.setFont(BNB, 11)
        c.drawString(XM, y, title)
        y = draw_sol_lines(c, y - 14, lines)
        y -= 8

    c.save()


if __name__ == "__main__":
    q = "/workspace/Class_Test_Chapter_6_1_v5.pdf"
    s = "/workspace/Class_Test_Chapter_6_1_v5_Solutions.pdf"
    build_question_paper(q)
    build_solutions(s)
    print("Created:", q)
    print("Created:", s)
