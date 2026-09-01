#!/usr/bin/env python3
"""Typed A4 SSC Math Special Assignment — matches original Panjeree print layout."""

from fpdf import FPDF

NOTO = "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf"
NOTO_B = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"
DEJA = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class ExamPDF(FPDF):
    COLS = 2
    GAP = 4.5

    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=False)
        self.set_margins(9, 7, 9)
        self.add_font("Noto", "", NOTO)
        self.add_font("Noto", "B", NOTO_B)
        self.add_font("DejaVu", "", DEJA)
        self.add_font("DejaVu", "B", DEJA_B)
        self.set_fallback_fonts(["DejaVu"], exact_match=False)
        self._col = 0
        self._col_w = 0
        self._x0 = 0
        self._y0 = 0
        self._y = 0
        self._bottom = 288

    def begin_page_cols(self):
        self.add_page()
        usable = self.w - self.l_margin - self.r_margin
        self._col_w = (usable - self.GAP) / self.COLS
        self._col = 0
        self._x0 = self.l_margin
        self._y0 = self.get_y()
        self._y = self._y0
        self.set_xy(self._x0, self._y)

    def _cx(self):
        return self._x0 + self._col * (self._col_w + self.GAP)

    def next_col(self):
        self._col = 1
        self._y = self._y0
        self.set_xy(self._cx(), self._y)

    def need(self, h):
        if self._y + h > self._bottom and self._col == 0:
            self.next_col()
        return self._y + h <= self._bottom

    def txt(self, text, size=7.8, bold=False, lh=3.5, ln=0.12, align="L"):
        if not self.need(lh):
            return
        self.set_xy(self._cx(), self._y)
        self.set_font("Noto", "B" if bold else "", size)
        self.multi_cell(self._col_w, lh, text, align=align)
        self._y = self.get_y() + ln

    def row(self, left, mark="", size=7.8, lh=3.5):
        if not self.need(lh):
            return
        self.set_xy(self._cx(), self._y)
        self.set_font("Noto", "", size)
        w = self._col_w
        if mark:
            self.cell(w * 0.9, lh, left)
            self.cell(w * 0.1, lh, mark, align="R", new_x="LMARGIN", new_y="NEXT")
        else:
            self.multi_cell(w, lh, left)
        self._y = self.get_y() + 0.05

    def qhead(self, num, text, size=8.0):
        self.txt(f"▶ {num}. {text}", size, bold=True, lh=3.6, ln=0.08)

    def sub(self, label, text, mark):
        self.row(f"{label}) {text}", mark)

    def draw_code_boxes(self, digits="109"):
        if not self.need(5):
            return
        x = self._cx() + self._col_w * 0.55
        y = self._y
        box = 3.8
        gap = 0.6
        self.set_font("DejaVu", "", 7)
        for i, d in enumerate(digits):
            self.rect(x + i * (box + gap), y, box, box)
            self.set_xy(x + i * (box + gap), y + 0.5)
            self.cell(box, box - 0.5, d, align="C")
        self._y = y + box + 0.3

    def draw_table(self, headers, rows):
        row_h = 3.8
        if not self.need(row_h * (len(rows) + 1) + 1):
            return
        x = self._cx()
        y = self._y
        ncol = len(headers)
        col_w = min(17, (self._col_w - 1) / ncol)
        wtab = col_w * ncol
        self.set_font("Noto", "B", 7.2)
        for i, h in enumerate(headers):
            self.rect(x + i * col_w, y, col_w, row_h)
            self.set_xy(x + i * col_w + 0.4, y + 0.5)
            self.cell(col_w - 0.8, row_h - 1, h, align="C")
        y += row_h
        self.set_font("Noto", "", 7.2)
        for row in rows:
            for i, val in enumerate(row):
                self.rect(x + i * col_w, y, col_w, row_h)
                self.set_xy(x + i * col_w + 0.4, y + 0.5)
                self.cell(col_w - 0.8, row_h - 1, val, align="C")
            y += row_h
        self._y = y + 0.5

    def draw_circle_diagram(self):
        if not self.need(24):
            return
        cx = self._cx() + self._col_w / 2
        cy = self._y + 10
        r = 9
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.18)
        self.ellipse(cx - r, cy - r, 2 * r, 2 * r)
        # diameters PR (vertical) and QS (horizontal)
        self.line(cx, cy - r, cx, cy + r)
        self.line(cx - r, cy, cx + r, cy)
        labels = [("P", cx, cy - r - 2.5), ("Q", cx - r - 3, cy), ("R", cx, cy + r + 0.5), ("S", cx + r + 0.5, cy)]
        self.set_font("DejaVu", "B", 6.8)
        for lab, lx, ly in labels:
            self.set_xy(lx - 1.2, ly - 1.2)
            self.cell(2.4, 2.4, lab, align="C")
        self.set_xy(cx - 1.2, cy - 1.2)
        self.cell(2.4, 2.4, "O", align="C")
        self.set_font("Noto", "", 7)
        self.set_xy(self._cx(), cy + r + 2.5)
        self.cell(self._col_w, 3, "OR = 5.5 সে.মি.", align="C")
        self._y = cy + r + 5.5

    def draw_footer(self):
        y = 289
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.set_xy(self.l_margin, y + 0.5)
        self.set_font("Noto", "", 6.5)
        self.cell(
            0,
            3,
            "[অঃ অধ্যায় ৫ পৃষ্ঠা ১০১ প্রশ্ন ৪] | [অঃ অধ্যায় ৯ পৃষ্ঠা ২৩৪ প্রশ্ন ৪৯]",
            align="C",
        )


def build(path: str):
    pdf = ExamPDF()
    pdf.begin_page_cols()

    # Header — column 1
    pdf.txt("পাঞ্জেরী এসএসসি স্পেশাল অ্যাসাইনমেন্ট ++ | গণিত", 7.2, ln=0.05)
    pdf.txt("৭৩. আইডিয়াল স্কুল অ্যান্ড কলেজ, মতিঝিল, ঢাকা", 9.2, bold=True, ln=0.05)
    pdf.txt("গণিত (সৃজনশীল)", 8.8, bold=True, ln=0.05)
    pdf.row("সময়—২ ঘণ্টা ৩০ মিনিট", "বিষয় কোড:  ১  ০  ৯    পূর্ণমান— ৭০", size=7.8)
    pdf.txt(
        "(দ্রষ্টব্য: সৃজনশীল প্রশ্ন অংশের প্রত্যেক বিভাগ থেকে কমপক্ষে ১টি করে "
        "প্রশ্নের মোট ৪টি এবং সংক্ষিপ্ত-উত্তর প্রশ্ন থেকে যেকোনো ১০টি প্রশ্নের উত্তর দাও।)",
        7.2,
        lh=3.3,
        ln=0.25,
    )
    pdf.txt("সৃজনশীল প্রশ্ন", 8.5, bold=True, ln=0.12)
    pdf.txt("ক-বিভাগ: বীজগণিত", 8.0, bold=True, ln=0.1)

    # Q1
    pdf.qhead(
        "১",
        "U = {x ∈ N : x < 9} সার্বিক সেট। A = {x ∈ N : x² > 5 এবং x³ < 150}, "
        "B = {x ∈ N : x মৌলিক সংখ্যা}, অন্বয় R = {(x, y) : x ∈ B, y ∈ B এবং y = x + 2}",
    )
    pdf.sub("ক", "A সেটকে তালিকা পদ্ধতিতে প্রকাশ কর।", "২")
    pdf.sub("খ", "দেখাও যে, (A ∩ B)' = A' ∪ B'", "৪")
    pdf.sub("গ", "R অন্বয়টিকে তালিকা পদ্ধতিতে প্রকাশ করে তার ডোমেন ও রেঞ্জ নির্ণয় কর।", "৪")

    # Q2
    pdf.qhead("২", "x² = 11 + √120 এবং A = y³ − 3my² + 3y − m")
    pdf.sub("ক", "উৎপাদকে বিশ্লেষণ কর: b² + 8b + 15 − z² + 2z", "২")
    pdf.sub("খ", "প্রমাণ কর যে, x³(x³ + 1/x³) = 922√6", "৪")
    pdf.sub(
        "গ",
        "A = 0 হলে, প্রমাণ কর যে, y = (∛(m+1) + ∛(m−1)) / (∛(m+1) − ∛(m−1))",
        "৪",
    )

    pdf.txt("খ-বিভাগ: জ্যামিতি", 8.0, bold=True, ln=0.1)

    # Q3
    pdf.qhead("৩", "a = 6 সে.মি., b = 7 সে.মি. এবং ∠x = 45°")
    pdf.sub(
        "ক",
        "একটি রম্বস আঁক যার বাহুর দৈর্ঘ্য a এবং একটি কোণ ∠x এর সমান। [অঙ্কনের চিহ্ন আবশ্যক]",
        "২",
    )
    pdf.sub(
        "খ",
        "এমন একটি ত্রিভুজ আঁক যার ভূমির দৈর্ঘ্য (a − 1) সে.মি., ভূমি সংলগ্ন কোণ ∠x "
        "এবং অপর দুই বাহুর সমষ্টি b। [অঙ্কনের চিহ্ন ও বিবরণ আবশ্যক]",
        "৪",
    )
    pdf.sub(
        "গ",
        "'খ' এর বর্ণিত ত্রিভুজের পরিবৃত্ত আঁক। [অঙ্কনের চিহ্ন ও বিবরণ আবশ্যক]",
        "৪",
    )

    # Q4
    pdf.qhead("৪", "চিত্রে, O কেন্দ্র বিশিষ্ট PQRS একটি বৃত্ত এবং OR = 5.5 সে.মি.")
    pdf.draw_circle_diagram()
    pdf.sub("ক", "উদ্দীপকের বৃত্তের পরিধি নির্ণয় কর।", "২")
    pdf.sub("খ", "প্রমাণ কর যে, ∠QPS + ∠QRS = 2 সমকোণ", "৪")
    pdf.sub(
        "গ",
        "PR ও QS কর্ণদ্বয় পরস্পর N বিন্দুতে ছেদ করলে, ∠POQ + ∠ROS = 2∠PNQ প্রমাণ কর।",
        "৪",
    )

    pdf.txt("গ-বিভাগ: ত্রিকোণমিতি ও পরিমিতি", 8.0, bold=True, ln=0.1)

    # Q5
    pdf.qhead("৫", "cot θ + cos θ = p এবং cot θ − cos θ = q")
    pdf.sub("ক", "cot(A − 30°) = 1 হলে, A এর মান নির্ণয় কর।", "২")
    pdf.sub("খ", "প্রমাণ কর যে, cosec²θ = √(pq) · sec²θ", "৪")
    pdf.sub("গ", "p/q = (2+√3)/(2−√3) হলে, θ (< 90°) এর মান নির্ণয় কর।", "৪")

    # Q6 (starts col 1)
    pdf.qhead(
        "৬",
        "একটি লোহার পাইপের ভিতরের ও বাইরের ব্যাস যথাক্রমে ৪ সে.মি. ও ১০ সে.মি. "
        "এবং পাইপের উচ্চতা ৪ মিটার। ১ ঘন সে.মি. লোহার ওজন ৭.২ গ্রাম।",
    )
    pdf.sub("ক", "পাইপের পুরুত্ব কত মিটার নির্ণয় কর।", "২")

    # Column 2
    pdf.next_col()

    pdf.sub("খ", "পাইপের বাইরের বক্রতলের ক্ষেত্রফল নির্ণয় কর।", "৪")
    pdf.sub("গ", "পাইপে ব্যবহৃত লোহার ওজন কত কেজি নির্ণয় কর।", "৪")

    pdf.txt("ঘ-বিভাগ: পরিসংখ্যান", 8.0, bold=True, ln=0.1)

    # Q7
    pdf.qhead("৭", "১০ম শ্রেণির ৬০ জন শিক্ষার্থীর ওজনের (কেজিতে) গণসংখ্যা নিবেশন দেওয়া হলো:")
    pdf.draw_table(
        ["শ্রেণিব্যাপ্তি", "গণসংখ্যা"],
        [
            ["46-50", "6"],
            ["51-55", "9"],
            ["56-60", "21"],
            ["61-65", "16"],
            ["66-70", "8"],
        ],
    )
    pdf.sub("ক", "প্রচুরক শ্রেণির আগের শ্রেণির মধ্যমান নির্ণয় কর।", "২")
    pdf.sub("খ", "প্রদত্ত উপাত্তের গাণিতিক গড় নির্ণয় কর।", "৪")
    pdf.sub("গ", "বর্ণনাসহ প্রদত্ত উপাত্তের অজিভ রেখা অঙ্কন কর।", "৪")

    # Q8
    pdf.qhead(
        "৮",
        "নিচে ৩০ জন শিক্ষার্থীর নির্বাচনী পরীক্ষায় গণিতে প্রাপ্ত নম্বর দেওয়া হলো: "
        "55, 40, 35, 60, 58, 60, 45, 57, 46, 50, 52, 61, 65, 50, 68, 40, 56, 54, 60, 46, 60, 65, 48, 60, 36, 58, 50, 60, 47, 43",
    )
    pdf.sub("ক", "শ্রেণিব্যাপ্তি ৫ হলে শ্রেণি সংখ্যা নির্ণয় কর।", "২")
    pdf.sub("খ", "গণসংখ্যা সারণি তৈরি করে মধ্যক নির্ণয় কর।", "৪")
    pdf.sub("গ", "সারণি হতে বিবরণসহ উপাত্তের গণসংখ্যা বহুভুজ অঙ্কন কর।", "৪")

    pdf.txt("সংক্ষিপ্ত-উত্তর প্রশ্ন", 8.5, bold=True, ln=0.08)
    pdf.txt("[যেকোনো ১০টির উত্তর দাও — প্রতিটি ২]", 7.2, ln=0.12)

    short = [
        ("ক", "X = {1, 3, 5}, Y = {2, 4, 6}, M = X ∩ Y হলে, P(M) নির্ণয় কর।"),
        ("খ", "f(x) = (6x + 6)/(3x + 5) হলে, f(1/3) এর মান নির্ণয় কর।"),
        ("গ", "x⁴ + x² + 1 কে উৎপাদকে বিশ্লেষণ কর।"),
        ("ঘ", "2x − 2/x = 4 হলে, x² + 1/x² এর মান নির্ণয় কর।"),
        ("ঙ", "g(a) = a³ + 3a + 40 কে (a + 3) দ্বারা ভাগ করলে ভাগশেষ কত হবে তা নির্ণয় কর।"),
        ("চ", "দুইটি সংখ্যার অনুপাত 3:5 এবং এদের গ.সা.গু. 5 হলে, সংখ্যা দুটির ল.সা.গু. নির্ণয় কর।"),
        ("ছ", "4, a এবং 9 ক্রমিক সমানুপাতি হলে, a এর মান নির্ণয় কর।"),
        ("জ", "পেন্সিল কম্পাসের সাহায্যে 75° কোণ অঙ্কন কর।"),
        ("ঝ", "কোন বৃত্তের একই চাপের উপর দণ্ডায়মান কেন্দ্রস্থ কোণ x + 40° এবং বৃত্তস্থ কোণ x + 10° হলে, x এর মান নির্ণয় কর।"),
        ("ঞ", "tan x = cot 5x হলে, x এর মান নির্ণয় কর।"),
        ("ট", "cosec²θ + cot²θ = 2 হলে, csc⁴θ − cot⁴θ = কত?"),
        ("ঠ", "একটি রম্বসের কর্ণদ্বয়ের দৈর্ঘ্য 12 সে.মি. ও 16 সে.মি. হলে, রম্বসটির পরিসীমা নির্ণয় কর।"),
        ("ড", "কেন্দ্রীয় প্রবণতা কাকে বলে? এর পরিমাপগুলো লেখ।"),
        ("ঢ", "কোন শ্রেণির উচ্চসীমা 55 এবং মধ্যমান 52.5 হলে ঐ শ্রেণির নিম্নসীমা নির্ণয় কর।"),
        ("ণ", "44, 30, 51, 53, 25, 22, 18, 32 সংখ্যাগুলোর মধ্যক নির্ণয় কর।"),
    ]
    pdf.txt("৯.", 8.0, bold=True, ln=0.04)
    for label, q in short:
        pdf.row(f"   {label}) {q}", "২", size=7.3, lh=3.3)

    pdf.draw_footer()
    pdf.output(path)


if __name__ == "__main__":
    out = "/workspace/SSC_Math_Special_Assignment.pdf"
    build(out)
    print(f"Created: {out}")
