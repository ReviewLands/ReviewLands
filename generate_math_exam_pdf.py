#!/usr/bin/env python3
"""Generate clean typed A4 PDF — Ideal School SSC Math Special Assignment."""

from fpdf import FPDF

FONT = "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf"
FONT_B = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"


class ExamPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=True, margin=14)
        self.set_margins(16, 14, 16)
        self.add_font("Noto", "", FONT)
        self.add_font("Noto", "B", FONT_B)
        self.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        self.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        self.set_fallback_fonts(["DejaVu"], exact_match=False)

    def footer(self):
        self.set_y(-10)
        self.set_font("Noto", "", 9)
        self.cell(0, 5, f"পৃষ্ঠা {self.page_no()}", align="C")

    def txt(self, text, size=10.5, bold=False, lh=5.2, ln=0.2):
        self.set_font("Noto", "B" if bold else "", size)
        self.multi_cell(0, lh, text)
        self.ln(ln)

    def row(self, left, right="", size=10.5, bold=False):
        self.set_font("Noto", "B" if bold else "", size)
        w = self.w - self.l_margin - self.r_margin
        self.cell(w * 0.72, 5.2, left)
        self.cell(w * 0.28, 5.2, right, align="R", new_x="LMARGIN", new_y="NEXT")


def build(path: str):
    pdf = ExamPDF()
    pdf.add_page()

    # Header
    pdf.txt("৭৩. আইডিয়াল স্কুল অ্যান্ড কলেজ, মতিঝিল, ঢাকা", 12, bold=True, ln=0.5)
    pdf.row("বিষয় : গণিত (সৃজনশীল)", "বিষয় কোড : ১০৯")
    pdf.row("সময় : ২ ঘণ্টা ৩০ মিনিট", "পূর্ণমান : ৭০")
    pdf.ln(1)
    pdf.txt(
        "নির্দেশনা : প্রতিটি সৃজনশীল বিভাগ থেকে একটি করে প্রশ্নের উত্তর দিতে হবে। "
        "সংক্ষিপ্ত-উত্তর বিভাগ থেকে ১০টি প্রশ্নের উত্তর দিতে হবে।",
        10,
    )
    pdf.ln(1.5)
    pdf.txt("১. সৃজনশীল প্রশ্ন", 11.5, bold=True)
    pdf.ln(0.5)

    # Section A
    pdf.txt("ক-বিভাগ : বীজগণিত", 11, bold=True)
    pdf.ln(0.3)

    pdf.txt("১.", 10.5, bold=True, ln=0)
    pdf.txt(
        "U = {x ∈ N : x ≤ ৯}, A = {x ∈ N : x² > ২৫}, B = {x ∈ N : x² < ১৫০}, "
        "R = {(x, y) : x ∈ B, y ∈ B, y = x² + ২}।",
        10,
    )
    pdf.row("ক) সেট A কে তালিকা পদ্ধতিতে প্রকাশ কর।", "২")
    pdf.row("খ) (A ∩ B)' = A' ∪ B' প্রমাণ কর।", "৪")
    pdf.row("গ) R সম্পর্কের Domain ও Range নির্ণয় কর।", "৪")
    pdf.ln(0.8)

    pdf.txt("২.", 10.5, bold=True, ln=0)
    pdf.txt("x² = ১১ + ২√৩০, A = y³ − 3my² + 3y − m।", 10)
    pdf.row("ক) b² + 8b + 15 − z² + 2z, কে উৎপাদকে বিশ্লেষণ কর।", "২")
    pdf.row("খ) x²(x³ + 1/x³) = 922√6 প্রমাণ কর।", "৪")
    pdf.row("গ) A = 0 হলে, y = (m+1)/(m−1) প্রমাণ কর।", "৪")
    pdf.ln(1)

    # Section B
    pdf.txt("খ-বিভাগ : জ্যামিতি", 11, bold=True)
    pdf.ln(0.3)

    pdf.txt("৩.", 10.5, bold=True, ln=0)
    pdf.txt("a = ৬ সে.মি., b = ৭ সে.মি., ∠x = ৪৫°।", 10)
    pdf.row("ক) a ও ∠x দ্বারা একটি রম্বস আঁক।", "২")
    pdf.row("খ) ভূমি (a−1), ভূমি-সন্নিহিত কোণ ∠x ও অন্য দুই বাহুর সমষ্টি b দ্বারা একটি ত্রিভুজ আঁক।", "৪")
    pdf.row("গ) 'খ' এর ত্রিভুজের পরিবৃত্ত আঁক।", "৪")
    pdf.ln(0.8)

    pdf.txt("৪.", 10.5, bold=True, ln=0)
    pdf.txt("O কেন্দ্রবিশিষ্ট বৃত্তে PQRS চতুর্ভুজ। OR = ৫.৫ সে.মি.।", 10)
    pdf.row("ক) বৃত্তের পরিধি নির্ণয় কর।", "২")
    pdf.row("খ) ∠QPS + ∠QRS = ২ সমকোণ প্রমাণ কর।", "৪")
    pdf.row("গ) PR ও QS পরস্পর N বিন্দুতে ছেদ করলে, ∠POQ + ∠ROS = 2∠PNQ প্রমাণ কর।", "৪")
    pdf.ln(1)

    # Section C
    pdf.txt("গ-বিভাগ : ত্রিকোণমিতি ও পরিমিতি", 11, bold=True)
    pdf.ln(0.3)

    pdf.txt("৫.", 10.5, bold=True, ln=0)
    pdf.txt("cot θ + cos θ = p, cot θ − cos θ = q।", 10)
    pdf.row("ক) cot(A − 30°) = 1 হলে, A এর মান নির্ণয় কর।", "২")
    pdf.row("খ) cosec²θ = √(pq) · sec²θ প্রমাণ কর।", "৪")
    pdf.row("গ) p ও q এর মান দিয়ে θ (< 90°) নির্ণয় কর।", "৪")
    pdf.ln(0.8)

    pdf.txt("৬.", 10.5, bold=True, ln=0)
    pdf.txt(
        "একটি লোহার পাইপের ভিতরের/বাইরের ব্যাসার্ধ ৮/১০ সে.মি., উচ্চতা ৪ মি., "
        "লোহার ঘনত্ব ৭.৮ গ্রাম/সে.মি.³।",
        10,
    )
    pdf.row("ক) পাইপের পুরুত্ব (মিটারে) নির্ণয় কর।", "২")
    pdf.row("খ) বাইরের তলের ক্ষেত্রফল নির্ণয় কর।", "৪")
    pdf.row("গ) পাইপের মোট ওজন (কেজিতে) নির্ণয় কর।", "৪")

    # Page 2
    pdf.add_page()

    # Section D
    pdf.txt("ঘ-বিভাগ : পরিসংখ্যান", 11, bold=True)
    pdf.ln(0.3)

    pdf.txt("৭.", 10.5, bold=True, ln=0)
    pdf.txt("৬০ জন শিক্ষার্থীর ওজন (কেজি) :", 10)
    pdf.txt(
        "┌──────────┬──────────┐\n"
        "│ ওজন শ্রেণি │ শিক্ষার্থী │\n"
        "├──────────┼──────────┤\n"
        "│  ৪৬–৫০   │    ৫     │\n"
        "│  ৫১–৫৫   │   ১০     │\n"
        "│  ৫৬–৬০   │   ১৫     │\n"
        "│  ৬১–৬৫   │   ২০     │\n"
        "│  ৬৬–৭০   │   ১০     │\n"
        "└──────────┴──────────┘",
        9.5,
        lh=4.5,
    )
    pdf.row("ক) গড় শ্রেণির পূর্ববর্তী শ্রেণির মধ্যমান নির্ণয় কর।", "২")
    pdf.row("খ) গাণিতিক গড় নির্ণয় কর।", "৪")
    pdf.row("গ) Ogive রেখা আঁক।", "৪")
    pdf.ln(0.8)

    pdf.txt("৮.", 10.5, bold=True, ln=0)
    pdf.txt(
        "গণিত পরীক্ষায় প্রাপ্ত ৩০টি নম্বর :\n"
        "৫৫, ৪০, ৩৫, ৬০, ৫৮, ৬০, ৪৫, ৫৭, ৪৬, ৫০, ৫২, ৬১, ৬৫, ৫০, ৬৫, "
        "৪০, ৫৬, ৫৪, ৬০, ৪৬, ৬০, ৬৫, ৪৮, ৬০, ৩৬, ৫৮, ৫০, ৬০, ৪৭, ৪৩।",
        10,
    )
    pdf.row("ক) শ্রেণিব্যবধান ৫ হলে শ্রেণির সংখ্যা নির্ণয় কর।", "২")
    pdf.row("খ) শ্রেণিবিন্যাস তৈরি করে মধ্যমা নির্ণয় কর।", "৪")
    pdf.row("গ) Frequency Polygon আঁক।", "৪")
    pdf.ln(1.2)

    # Short answers
    pdf.txt("২. সংক্ষিপ্ত-উত্তর প্রশ্ন", 11.5, bold=True)
    pdf.txt("(১০টি প্রশ্নের উত্তর দিতে হবে — প্রতিটি ২ নম্বর)", 10)
    pdf.ln(0.5)

    short = [
        ("ক", "X = {১, ৩, ৫}, Y = {২, ৪, ৬}, M = X ∪ Y; P(M) = ?"),
        ("খ", "F(x) = x² − 5; F(5) = ?"),
        ("গ", "x² + x + 1/x² + 1/x = ৭; x + 1/x = ?"),
        ("ঘ", "f(a) = a² + 3a + 40; (a+3) দ্বারা f(a) ভাগ করলে ভাগশেষ = ?"),
        ("ঙ", "৩ : ৫ :: x : ৭.৫; x = ?"),
        ("চ", "a : b = ৭ : ৯, a = ২১.৯; b = ?"),
        ("ছ", "a, b, c সান্তরিক; a = ৪, b = ৬; c = ?"),
        ("জ", "রুলার ও কম্পাস দিয়ে ৭৫° কোণ অঙ্কন কর।"),
        ("ঝ", "O কেন্দ্রবিষয়ক ∠AOC = ১০০°, ∠ABC = x°; x = ?"),
        ("ঞ", "tan x = cot 5x; x = ?"),
        ("ট", "cosec²θ + cot²θ = ২, cosec θ < 0; cot²θ = ?"),
        ("ঠ", "রম্বসের কর্ণ ১২ ও ১৬; পরিসীমা = ?"),
        ("ড", "কেন্দ্রীয় প্রবণতা কী?"),
        ("ঢ", "উর্ধ্বসীমা ৬০, মধ্যমান ৫৭.৫; নিম্নসীমা = ?"),
        ("ণ", "৫, ৬, ১৮, ৭, ১৯, ৯, ৬, ১৩ — মধ্যমা = ?"),
    ]
    for label, q in short:
        pdf.row(f"{label}) {q}", "২")

    pdf.output(path)


if __name__ == "__main__":
    out = "/workspace/SSC_Math_Special_Assignment.pdf"
    build(out)
    print(f"Created: {out}")
