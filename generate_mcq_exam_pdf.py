#!/usr/bin/env python3
"""Generate clean typed A4 PDF — Ideal School SSC Math MCQ Test."""

from fpdf import FPDF

FONT = "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf"
FONT_B = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"


class MCQPDF(FPDF):
    COLS = 3
    COL_GAP = 3

    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=False)
        self.set_margins(10, 9, 10)
        self.add_font("Noto", "", FONT)
        self.add_font("Noto", "B", FONT_B)
        self.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        self.set_fallback_fonts(["DejaVu"], exact_match=False)
        self._col = 0
        self._col_w = 0
        self._start_y = 0
        self._bottom_y = 0

    def footer(self):
        self.set_y(-8)
        self.set_font("Noto", "", 8)
        self.cell(0, 4, f"পৃষ্ঠা {self.page_no()}", align="C")

    def begin_columns(self):
        usable = self.w - self.l_margin - self.r_margin
        self._col_w = (usable - self.COL_GAP * (self.COLS - 1)) / self.COLS
        self._col = 0
        self._start_y = self.get_y()
        self._bottom_y = self._start_y

    def _col_x(self):
        return self.l_margin + self._col * (self._col_w + self.COL_GAP)

    def advance_col(self):
        self._col += 1
        if self._col >= self.COLS:
            self.add_page()
            self.begin_columns()
        self.set_xy(self._col_x(), self._start_y)

    def q(self, num, text, opts):
        lh_q, lh_o = 3.3, 3.0
        needed = lh_q + len(opts) * lh_o + 1.5
        if self._bottom_y + needed > self.h - 14 and self._col < self.COLS - 1:
            self.advance_col()
        elif self._bottom_y + needed > self.h - 14:
            self.add_page()
            self.begin_columns()

        x = self._col_x()
        y = self._bottom_y
        self.set_xy(x, y)
        self.set_font("Noto", "B", 7.6)
        self.multi_cell(self._col_w, lh_q, f"{num}. {text}")
        y = self.get_y()
        self.set_font("Noto", "", 7.2)
        for opt in opts:
            self.set_xy(x, y)
            self.multi_cell(self._col_w, lh_o, opt)
            y = self.get_y()
        self._bottom_y = y + 1


QUESTIONS = [
    (
        "১",
        "১০% ক্ষতিতে বিক্রয়মূল্য : ক্রয়মূল্য = ?",
        ["ক) ৯ : ১০", "খ) ১০ : ৯", "গ) ৯ : ১১", "ঘ) ১১ : ৯"],
    ),
    (
        "২",
        "sin(90° − θ) = √3/2 হলে —\n(i) θ = 60°  (ii) cos36° = 0  (iii) 1 + tan²θ = 4",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
    ),
    (
        "৩",
        "রম্বস আঁকতে কোন তথ্য প্রয়োজন?",
        ["ক) এক বাহু ও একটি কোণ", "খ) দুই বাহু", "গ) তিন বাহু", "ঘ) চার বাহু"],
    ),
    (
        "৪",
        "ক্ষুদ্র চাপে অঙ্কিত কোণ কী ধরনের?",
        ["ক) স্থূলকোণ", "খ) সূক্ষ্মকোণ", "গ) সমকোণ", "ঘ) পূরক কোণ"],
    ),
    (
        "৫",
        "কোন বাহু তিনটি ত্রিভুজ গঠন করতে পারে?",
        ["ক) ৫, ৬, ১৮", "খ) ৬, ৭, ১৯", "গ) ৭, ৮, ১৭", "ঘ) ৯, ৬, ১৩"],
    ),
    (
        "৬",
        "O কেন্দ্রবিশিষ্ট বৃত্তে ∠AOC = 100° হলে ∠ABC = ?",
        ["ক) 50°", "খ) 90°", "গ) 130°", "ঘ) 150°"],
    ),
    (
        "৭",
        "স্থূলকোণী ত্রিভুজের অন্য দুই কোণের সম্ভাব্য মান —",
        ["ক) 30° ও 50°", "খ) 30° ও 60°", "গ) 40° ও 50°", "ঘ) 45° ও 45°"],
    ),
    (
        "৮",
        "tan θ = 1/√3 হলে sin θ = ?",
        ["ক) 1/2", "খ) √3/2", "গ) 1/√3", "ঘ) √3"],
    ),
    (
        "৯",
        "θ = 0° হলে —\n(i) cosecθ · cotθ  (ii) secθ · tanθ  (iii) cosθ · secθ",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
    ),
    (
        "১০",
        "বাহু a সমবাহু বর্গের কর্ণের উপর অঙ্কিত বর্গের ক্ষেত্রফল = ?",
        ["ক) a²", "খ) 2a²", "গ) a²/2", "ঘ) 4a²"],
    ),
    (
        "১১",
        "সমবাহু ত্রিভুজের ক্ষেত্রফল 4√3 বর্গমি. হলে বাহুর দৈর্ঘ্য = ?",
        ["ক) 2 মি.", "খ) 3 মি.", "গ) 4 মি.", "ঘ) 6 মি."],
    ),
    (
        "১২",
        "ABCD সামান্তরিক; ∠DOC = 90°, DC = 5 সে.মি., OC = 4 সে.মি.; BD = ?",
        ["ক) 6 সে.মি.", "খ) 8 সে.মি.", "গ) 10 সে.মি.", "ঘ) 12 সে.মি."],
    ),
    (
        "১৩",
        "উপরোক্ত সামান্তরিকের ক্ষেত্রফল = ?",
        ["ক) 24 ব.সে.মি.", "খ) 25 ব.সে.মি.", "গ) 48 ব.সে.মি.", "ঘ) 50 ব.সে.মি."],
    ),
    (
        "১৪",
        "a : b = 2 : 1, b : c = 2 : 1 হলে —\n(i) a, b, c সান্তরিক  (ii) c : a = 1 : 4  (iii) b² + c² = 2bc",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
    ),
    (
        "১৫",
        "p² = 13 + √168 হলে 1/p = ?",
        ["ক) √13 − 2√2", "খ) √13 + 2√2", "গ) √13 − √42", "ঘ) √13 + √42"],
    ),
    (
        "১৬",
        "ব্যাসার্ধ 5 সে.মি. বৃত্তে, কেন্দ্র হতে 3 সে.মি. দূরে জ্যা; জ্যার দৈর্ঘ্য = ?",
        ["ক) 4 সে.মি.", "খ) 6 সে.মি.", "গ) 8 সে.মি.", "ঘ) 10 সে.মি."],
    ),
    (
        "১৭",
        "নিচের কোনটি বিচ্ছিন্ন চলক?",
        ["ক) তাপমাত্রা", "খ) বয়স", "গ) উচ্চতা", "ঘ) জনসংখ্যা"],
    ),
    (
        "১৮",
        "১ থেকে ৩০ পর্যন্ত মৌলিক সংখ্যার মধ্যমা = ?",
        ["ক) 12", "খ) 13", "গ) 14", "ঘ) 15"],
    ),
    (
        "১৯",
        "১ থেকে ৩০ পর্যন্ত মৌলিক সংখ্যার পরিসর = ?",
        ["ক) 25", "খ) 27", "গ) 28", "ঘ) 29"],
    ),
    (
        "২০",
        "১ থেকে ৩০ পর্যন্ত মৌলিক সংখ্যার গাণিতিক গড় = ?",
        ["ক) 9.5", "খ) 10.7", "গ) 12.5", "ঘ) 13.5"],
    ),
    (
        "২১",
        "A = {1, 2, 3, 4} হলে A এর সঠিক উপসেটের সংখ্যা = ?",
        ["ক) 14", "খ) 15", "গ) 16", "ঘ) 17"],
    ),
    (
        "২২",
        "A = {3, 5}, B = {1, 3, 4}; B \\ A = ?",
        ["ক) {1, 4}", "খ) {1, 3, 4}", "গ) {3, 5}", "ঘ) {1, 3, 4, 5}"],
    ),
    (
        "২৩",
        "f(x) = 3x² + 4kx; f(−2) = 0 হলে k = ?",
        ["ক) −3/2", "খ) 3/2", "গ) −3", "ঘ) 3"],
    ),
    (
        "২৪",
        "U = {2, 6, 7}, A = {2, 7}, B = {2, 6} হলে —\n(i) A ∪ B = U  (ii) (A ∩ B)' = A'  (iii) A − B = {7}",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
    ),
    (
        "২৫",
        "a + b = √5, a − b = 1 হলে 2(a² + b²) = ?",
        ["ক) 4", "খ) 6", "গ) 8", "ঘ) 10"],
    ),
    (
        "২৬",
        "x + 1/x = √5 হলে —\n(i) x² + 1/x² = 3  (ii) x − 1/x = 1  (iii) x³ + 1/x³ = 2√5",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
    ),
    (
        "২৭",
        "x⁴ + 1 = 3x² হলে x − 1/x = ?",
        ["ক) 1", "খ) √5", "গ) −1", "ঘ) −√5"],
    ),
    (
        "২৮",
        "x⁴ + 1 = 3x² হলে x³ + 1/x³ = ?",
        ["ক) 2√5", "খ) 2", "গ) 0", "ঘ) 4"],
    ),
    (
        "২৯",
        "p, q, r সান্তরিক হলে (p² + q²)/(q² + r²) = ?",
        ["ক) p/r", "খ) p/q", "গ) q/r", "ঘ) r/p"],
    ),
    (
        "৩০",
        "x : y = 5 : 6 হলে 3x : 5y = ?",
        ["ক) 1 : 2", "খ) 2 : 3", "গ) 3 : 5", "ঘ) 5 : 6"],
    ),
]


def build(path: str):
    pdf = MCQPDF()
    pdf.add_page()
    pdf.set_font("Noto", "B", 10)
    pdf.cell(0, 5, "১০১. আইডিয়াল স্কুল অ্যান্ড কলেজ, মতিঝিল, ঢাকা", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Noto", "", 9)
    pdf.cell(0, 4.2, "বিষয় : গণিত                    বিষয় কোড : ১০৯", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4.2, "বহুনির্বাচনি অভীক্ষা", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4.2, "সময় : ৩০ মিনিট                              পূর্ণমান : ৩০", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.begin_columns()
    for num, text, opts in QUESTIONS:
        pdf.q(num, text, opts)
    pdf.output(path)


if __name__ == "__main__":
    out = "/workspace/SSC_Math_MCQ_Test.pdf"
    build(out)
    print(f"Created: {out}")
