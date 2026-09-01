#!/usr/bin/env python3
"""Landscape fold-layout SSC Math MCQ test — WeasyPrint for Bengali shaping."""

from __future__ import annotations

import html
from pathlib import Path

from weasyprint import HTML

NOTO = "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf"
NOTO_B = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"

SCHOOL = "গাজীপুর ফাজিল মাদরাসা (চতর), বি.ও.এফ, গাজীপুর - ১৭০৩"

QUESTIONS = [
    (
        "১",
        "১০% ক্ষতিতে বিক্রয়মূল্য : ক্রয়মূল্য = ?",
        ["ক) ৯ : ১০", "খ) ১০ : ৯", "গ) ৯ : ১১", "ঘ) ১১ : ৯"],
        None,
    ),
    (
        "২",
        "sin(90° − θ) = √3/2 হলে —<br>(i) θ = 60° &nbsp; (ii) cos36° = 0 &nbsp; (iii) 1 + tan²θ = 4",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
        None,
    ),
    (
        "৩",
        "রম্বস আঁকতে কোন তথ্য প্রয়োজন?",
        ["ক) এক বাহু ও একটি কোণ", "খ) দুই বাহু", "গ) তিন বাহু", "ঘ) চার বাহু"],
        None,
    ),
    (
        "৪",
        "ক্ষুদ্র চাপে অঙ্কিত কোণ কী ধরনের?",
        ["ক) স্থূলকোণ", "খ) সূক্ষ্মকোণ", "গ) সমকোণ", "ঘ) পূরক কোণ"],
        None,
    ),
    (
        "৫",
        "কোন বাহু তিনটি ত্রিভুজ গঠন করতে পারে?",
        ["ক) ৫, ৬, ১৮", "খ) ৬, ৭, ১৯", "গ) ৭, ৮, ১৭", "ঘ) ৯, ৬, ১৩"],
        None,
    ),
    (
        "৬",
        "O কেন্দ্রবিশিষ্ট বৃত্তে ∠AOC = 100° হলে ∠ABC = ?",
        ["ক) 50°", "খ) 90°", "গ) 130°", "ঘ) 150°"],
        "circle",
    ),
    (
        "৭",
        "স্থূলকোণী ত্রিভুজের অন্য দুই কোণের সম্ভাব্য মান —",
        ["ক) 30° ও 50°", "খ) 30° ও 60°", "গ) 40° ও 50°", "ঘ) 45° ও 45°"],
        None,
    ),
    (
        "৮",
        "tan θ = 1/√3 হলে sin θ = ?",
        ["ক) 1/2", "খ) √3/2", "গ) 1/√3", "ঘ) √3"],
        None,
    ),
    (
        "৯",
        "θ = 0° হলে —<br>(i) cosecθ · cotθ &nbsp; (ii) secθ · tanθ &nbsp; (iii) cosθ · secθ",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
        None,
    ),
    (
        "১০",
        "বাহু a সমবাহু বর্গের কর্ণের উপর অঙ্কিত বর্গের ক্ষেত্রফল = ?",
        ["ক) a²", "খ) 2a²", "গ) a²/2", "ঘ) 4a²"],
        None,
    ),
    (
        "১১",
        "সমবাহু ত্রিভুজের ক্ষেত্রফল 4√3 বর্গমি. হলে বাহুর দৈর্ঘ্য = ?",
        ["ক) 2 মি.", "খ) 3 মি.", "গ) 4 মি.", "ঘ) 6 মি."],
        None,
    ),
    (
        "১২",
        "ABCD সামান্তরিক; ∠DOC = 90°, DC = 5 সে.মি., OC = 4 সে.মি.; BD = ?",
        ["ক) 6 সে.মি.", "খ) 8 সে.মি.", "গ) 10 সে.মি.", "ঘ) 12 সে.মি."],
        "parallelogram",
    ),
    (
        "১৩",
        "উপরোক্ত সামান্তরিকের ক্ষেত্রফল = ?",
        ["ক) 24 ব.সে.মি.", "খ) 25 ব.সে.মি.", "গ) 48 ব.সে.মি.", "ঘ) 50 ব.সে.মি."],
        None,
    ),
    (
        "১৪",
        "a : b = 2 : 1, b : c = 2 : 1 হলে —<br>(i) a, b, c সান্তরিক &nbsp; (ii) c : a = 1 : 4 &nbsp; (iii) b² + c² = 2bc",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
        None,
    ),
    (
        "১৫",
        "p² = 13 + √168 হলে 1/p = ?",
        ["ক) √13 − 2√2", "খ) √13 + 2√2", "গ) √13 − √42", "ঘ) √13 + √42"],
        None,
    ),
    (
        "১৬",
        "ব্যাসার্ধ 5 সে.মি. বৃত্তে, কেন্দ্র হতে 3 সে.মি. দূরে জ্যা; জ্যার দৈর্ঘ্য = ?",
        ["ক) 4 সে.মি.", "খ) 6 সে.মি.", "গ) 8 সে.মি.", "ঘ) 10 সে.মি."],
        None,
    ),
    (
        "১৭",
        "নিচের কোনটি বিচ্ছিন্ন চলক?",
        ["ক) তাপমাত্রা", "খ) বয়স", "গ) উচ্চতা", "ঘ) জনসংখ্যা"],
        None,
    ),
    (
        "১৮",
        "১ থেকে ৩০ পর্যন্ত মৌলিক সংখ্যার মধ্যমা = ?",
        ["ক) 12", "খ) 13", "গ) 14", "ঘ) 15"],
        None,
    ),
    (
        "১৯",
        "১ থেকে ৩০ পর্যন্ত মৌলিক সংখ্যার পরিসর = ?",
        ["ক) 25", "খ) 27", "গ) 28", "ঘ) 29"],
        None,
    ),
    (
        "২০",
        "১ থেকে ৩০ পর্যন্ত মৌলিক সংখ্যার গাণিতিক গড় = ?",
        ["ক) 9.5", "খ) 10.7", "গ) 12.5", "ঘ) 13.5"],
        None,
    ),
    (
        "২১",
        "A = {1, 2, 3, 4} হলে A এর সঠিক উপসেটের সংখ্যা = ?",
        ["ক) 14", "খ) 15", "গ) 16", "ঘ) 17"],
        None,
    ),
    (
        "২২",
        "A = {3, 5}, B = {1, 3, 4}; B \\ A = ?",
        ["ক) {1, 4}", "খ) {1, 3, 4}", "গ) {3, 5}", "ঘ) {1, 3, 4, 5}"],
        None,
    ),
    (
        "২৩",
        "f(x) = 3x² + 4kx; f(−2) = 0 হলে k = ?",
        ["ক) −3/2", "খ) 3/2", "গ) −3", "ঘ) 3"],
        None,
    ),
    (
        "২৪",
        "U = {2, 6, 7}, A = {2, 7}, B = {2, 6} হলে —<br>(i) A ∪ B = U &nbsp; (ii) (A ∩ B)' = A' &nbsp; (iii) A − B = {7}",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
        None,
    ),
    (
        "২৫",
        "a + b = √5, a − b = 1 হলে 2(a² + b²) = ?",
        ["ক) 4", "খ) 6", "গ) 8", "ঘ) 10"],
        None,
    ),
    (
        "২৬",
        "x + 1/x = √5 হলে —<br>(i) x² + 1/x² = 3 &nbsp; (ii) x − 1/x = 1 &nbsp; (iii) x³ + 1/x³ = 2√5",
        ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"],
        None,
    ),
    (
        "২৭",
        "x⁴ + 1 = 3x² হলে x − 1/x = ?",
        ["ক) 1", "খ) √5", "গ) −1", "ঘ) −√5"],
        None,
    ),
    (
        "২৮",
        "x⁴ + 1 = 3x² হলে x³ + 1/x³ = ?",
        ["ক) 2√5", "খ) 2", "গ) 0", "ঘ) 4"],
        None,
    ),
    (
        "২৯",
        "p, q, r সান্তরিক হলে (p² + q²)/(q² + r²) = ?",
        ["ক) p/r", "খ) p/q", "গ) q/r", "ঘ) r/p"],
        None,
    ),
    (
        "৩০",
        "x : y = 5 : 6 হলে 3x : 5y = ?",
        ["ক) 1 : 2", "খ) 2 : 3", "গ) 3 : 5", "ঘ) 5 : 6"],
        None,
    ),
]

DIAGRAMS = {
    "circle": """
<div class="diagram">
  <svg viewBox="0 0 90 70" xmlns="http://www.w3.org/2000/svg">
    <circle cx="45" cy="35" r="24" fill="none" stroke="#000" stroke-width="0.9"/>
    <line x1="45" y1="11" x2="45" y2="59" stroke="#000" stroke-width="0.7"/>
    <line x1="21" y1="35" x2="69" y2="35" stroke="#000" stroke-width="0.7"/>
    <text x="45" y="9" text-anchor="middle" font-size="7" font-family="DejaVu Sans">A</text>
    <text x="71" y="38" font-size="7" font-family="DejaVu Sans">C</text>
    <text x="45" y="66" text-anchor="middle" font-size="7" font-family="DejaVu Sans">B</text>
    <text x="45" y="38" text-anchor="middle" font-size="7" font-family="DejaVu Sans">O</text>
    <text x="58" y="24" font-size="6.5" font-family="DejaVu Sans">100°</text>
  </svg>
</div>""",
    "parallelogram": """
<div class="diagram">
  <svg viewBox="0 0 100 55" xmlns="http://www.w3.org/2000/svg">
    <polygon points="18,45 38,12 82,12 62,45" fill="none" stroke="#000" stroke-width="0.9"/>
    <line x1="18" y1="45" x2="82" y2="12" stroke="#000" stroke-width="0.7"/>
    <line x1="38" y1="12" x2="62" y2="45" stroke="#000" stroke-width="0.7"/>
    <text x="12" y="48" font-size="7" font-family="DejaVu Sans">A</text>
    <text x="34" y="10" font-size="7" font-family="DejaVu Sans">B</text>
    <text x="84" y="14" font-size="7" font-family="DejaVu Sans">C</text>
    <text x="64" y="50" font-size="7" font-family="DejaVu Sans">D</text>
    <text x="50" y="30" font-size="7" font-family="DejaVu Sans">O</text>
  </svg>
</div>""",
}


def header_block() -> str:
    return f"""
<div class="header">
  <div class="school">{html.escape(SCHOOL)}</div>
  <div class="subject">গণিত</div>
  <div class="exam-title">বহুনির্বাচনি অভীক্ষা</div>
  <div class="meta">
    <span>সময়— ৩০ মিনিট</span>
    <span>বিষয় কোড: ১&nbsp;&nbsp;০&nbsp;&nbsp;৯</span>
    <span>পূর্ণমান— ৩০</span>
  </div>
  <div class="note">(নির্দেশনা: প্রশ্নপত্রে দেওয়া চারটি বিকল্পের মধ্যে সঠিক উত্তরের বৃত্ত ভরে কালো কালি দিয়ে পূর্ণ করতে হবে।)</div>
</div>"""


def render_question(num: str, text: str, opts: list[str], diagram: str | None) -> str:
    diag = DIAGRAMS.get(diagram, "") if diagram else ""
    opt_html = "".join(f'<div class="opt">{html.escape(o)}</div>' for o in opts)
    return f"""
<div class="mcq">
  <div class="qtext"><span class="num">{html.escape(num)}.</span> {text}</div>
  {diag}
  {opt_html}
</div>"""


def render_panel(questions: list) -> str:
    body = "".join(render_question(num, text, opts, diag) for num, text, opts, diag in questions)
    return f'{header_block()}<div class="inner-cols">{body}</div>'


def build_html() -> str:
    split = len(QUESTIONS) // 2
    left = QUESTIONS[:split]   # Q1–15
    right = QUESTIONS[split:]  # Q16–30

    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8">
<style>
@font-face {{
  font-family: "Noto Bengali";
  src: url("file://{NOTO}");
  font-weight: normal;
  font-style: normal;
}}
@font-face {{
  font-family: "Noto Bengali";
  src: url("file://{NOTO_B}");
  font-weight: bold;
  font-style: normal;
}}
@page {{ size: A4 landscape; margin: 5mm 7mm 6mm 7mm; }}
* {{ box-sizing: border-box; }}
body {{
  font-family: "Noto Bengali", sans-serif;
  font-size: 6.7pt;
  line-height: 1.28;
  color: #000;
  margin: 0;
}}
.sheet {{
  display: flex;
  align-items: stretch;
}}
.panel {{
  flex: 1;
  padding: 0 1.5mm;
  min-width: 0;
}}
.fold-gap {{
  width: 22mm;
  flex-shrink: 0;
}}
.inner-cols {{
  column-count: 2;
  column-gap: 3mm;
}}
.header {{
  margin-bottom: 1mm;
  text-align: center;
  column-span: all;
}}
.header .school {{
  font-size: 8.8pt;
  font-weight: bold;
  margin-bottom: 0.2mm;
}}
.header .subject {{
  font-size: 8pt;
  font-weight: bold;
}}
.header .exam-title {{
  font-size: 7.8pt;
  font-weight: bold;
  margin: 0.15mm 0;
}}
.header .meta {{
  display: flex;
  justify-content: space-between;
  font-size: 7pt;
  margin: 0.3mm 0;
  text-align: left;
}}
.header .note {{
  font-size: 6.4pt;
  margin-bottom: 0.6mm;
  text-align: justify;
}}
.mcq {{
  margin-bottom: 0.65mm;
  break-inside: avoid;
}}
.qtext {{
  font-weight: bold;
  font-size: 6.75pt;
  margin-bottom: 0.1mm;
}}
.qtext .num {{ margin-right: 0.4mm; }}
.opt {{
  font-size: 6.55pt;
  padding-left: 2mm;
  margin: 0.02mm 0;
}}
.diagram {{
  text-align: center;
  margin: 0.15mm 0 0.2mm;
}}
.diagram svg {{
  width: 13mm;
  height: auto;
}}
</style>
</head>
<body>
<div class="sheet">
  <div class="panel left">{render_panel(left)}</div>
  <div class="fold-gap" aria-hidden="true"></div>
  <div class="panel right">{render_panel(right)}</div>
</div>
</body>
</html>"""


def build(path: str) -> None:
    HTML(string=build_html(), base_url=str(Path("/workspace"))).write_pdf(path)


if __name__ == "__main__":
    out = "/workspace/SSC_Math_MCQ_Test.pdf"
    build(out)
    print(f"Created: {out}")
