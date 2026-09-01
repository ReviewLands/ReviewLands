#!/usr/bin/env python3
"""Combined SSC Math exam PDF — page 1 MCQ, page 2 Creative (landscape fold layout)."""

from __future__ import annotations

import html
from pathlib import Path

from weasyprint import HTML

NOTO = "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf"
NOTO_B = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"
SCHOOL = "গাজীপুর ফাজিল মাদরাসা (চতর), বি.ও.এফ, গাজীপুর - ১৭০৩"

FONTS = f"""
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
"""

MCQ_QUESTIONS = [
    ("১", "১০% ক্ষতিতে বিক্রয়মূল্য : ক্রয়মূল্য = ?", ["ক) ৯ : ১০", "খ) ১০ : ৯", "গ) ৯ : ১১", "ঘ) ১১ : ৯"], None),
    ("২", "sin(90° − θ) = √3/2 হলে —<br>(i) θ = 60° &nbsp; (ii) cos36° = 0 &nbsp; (iii) 1 + tan²θ = 4", ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"], None),
    ("৩", "রম্বস আঁকতে কোন তথ্য প্রয়োজন?", ["ক) এক বাহু ও একটি কোণ", "খ) দুই বাহু", "গ) তিন বাহু", "ঘ) চার বাহু"], None),
    ("৪", "ক্ষুদ্র চাপে অঙ্কিত কোণ কী ধরনের?", ["ক) স্থূলকোণ", "খ) সূক্ষ্মকোণ", "গ) সমকোণ", "ঘ) পূরক কোণ"], None),
    ("৫", "কোন বাহু তিনটি ত্রিভুজ গঠন করতে পারে?", ["ক) ৫, ৬, ১৮", "খ) ৬, ৭, ১৯", "গ) ৭, ৮, ১৭", "ঘ) ৯, ৬, ১৩"], None),
    ("৬", "O কেন্দ্রবিশিষ্ট বৃত্তে ∠AOC = 100° হলে ∠ABC = ?", ["ক) 50°", "খ) 90°", "গ) 130°", "ঘ) 150°"], "circle"),
    ("৭", "স্থূলকোণী ত্রিভুজের অন্য দুই কোণের সম্ভাব্য মান —", ["ক) 30° ও 50°", "খ) 30° ও 60°", "গ) 40° ও 50°", "ঘ) 45° ও 45°"], None),
    ("৮", "tan θ = 1/√3 হলে sin θ = ?", ["ক) 1/2", "খ) √3/2", "গ) 1/√3", "ঘ) √3"], None),
    ("৯", "θ = 0° হলে —<br>(i) cosecθ · cotθ &nbsp; (ii) secθ · tanθ &nbsp; (iii) cosθ · secθ", ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"], None),
    ("১০", "বাহু a সমবাহু বর্গের কর্ণের উপর অঙ্কিত বর্গের ক্ষেত্রফল = ?", ["ক) a²", "খ) 2a²", "গ) a²/2", "ঘ) 4a²"], None),
    ("১১", "সমবাহু ত্রিভুজের ক্ষেত্রফল 4√3 বর্গমি. হলে বাহুর দৈর্ঘ্য = ?", ["ক) 2 মি.", "খ) 3 মি.", "গ) 4 মি.", "ঘ) 6 মি."], None),
    ("১২", "ABCD সামান্তরিক; ∠DOC = 90°, DC = 5 সে.মি., OC = 4 সে.মি.; BD = ?", ["ক) 6 সে.মি.", "খ) 8 সে.মি.", "গ) 10 সে.মি.", "ঘ) 12 সে.মি."], "parallelogram"),
    ("১৩", "উপরোক্ত সামান্তরিকের ক্ষেত্রফল = ?", ["ক) 24 ব.সে.মি.", "খ) 25 ব.সে.মি.", "গ) 48 ব.সে.মি.", "ঘ) 50 ব.সে.মি."], None),
    ("১৪", "a : b = 2 : 1, b : c = 2 : 1 হলে —<br>(i) a, b, c সান্তরিক &nbsp; (ii) c : a = 1 : 4 &nbsp; (iii) b² + c² = 2bc", ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"], None),
    ("১৫", "p² = 13 + √168 হলে 1/p = ?", ["ক) √13 − 2√2", "খ) √13 + 2√2", "গ) √13 − √42", "ঘ) √13 + √42"], None),
    ("১৬", "ব্যাসার্ধ 5 সে.মি. বৃত্তে, কেন্দ্র হতে 3 সে.মি. দূরে জ্যা; জ্যার দৈর্ঘ্য = ?", ["ক) 4 সে.মি.", "খ) 6 সে.মি.", "গ) 8 সে.মি.", "ঘ) 10 সে.মি."], None),
    ("১৭", "নিচের কোনটি বিচ্ছিন্ন চলক?", ["ক) তাপমাত্রা", "খ) বয়স", "গ) উচ্চতা", "ঘ) জনসংখ্যা"], None),
    ("১৮", "১ থেকে ৩০ পর্যন্ত মৌলিক সংখ্যার মধ্যমা = ?", ["ক) 12", "খ) 13", "গ) 14", "ঘ) 15"], None),
    ("১৯", "১ থেকে ৩০ পর্যন্ত মৌলিক সংখ্যার পরিসর = ?", ["ক) 25", "খ) 27", "গ) 28", "ঘ) 29"], None),
    ("২০", "১ থেকে ৩০ পর্যন্ত মৌলিক সংখ্যার গাণিতিক গড় = ?", ["ক) 9.5", "খ) 10.7", "গ) 12.5", "ঘ) 13.5"], None),
    ("২১", "A = {1, 2, 3, 4} হলে A এর সঠিক উপসেটের সংখ্যা = ?", ["ক) 14", "খ) 15", "গ) 16", "ঘ) 17"], None),
    ("২২", "A = {3, 5}, B = {1, 3, 4}; B \\ A = ?", ["ক) {1, 4}", "খ) {1, 3, 4}", "গ) {3, 5}", "ঘ) {1, 3, 4, 5}"], None),
    ("২৩", "f(x) = 3x² + 4kx; f(−2) = 0 হলে k = ?", ["ক) −3/2", "খ) 3/2", "গ) −3", "ঘ) 3"], None),
    ("২৪", "U = {2, 6, 7}, A = {2, 7}, B = {2, 6} হলে —<br>(i) A ∪ B = U &nbsp; (ii) (A ∩ B)' = A' &nbsp; (iii) A − B = {7}", ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"], None),
    ("২৫", "a + b = √5, a − b = 1 হলে 2(a² + b²) = ?", ["ক) 4", "খ) 6", "গ) 8", "ঘ) 10"], None),
    ("২৬", "x + 1/x = √5 হলে —<br>(i) x² + 1/x² = 3 &nbsp; (ii) x − 1/x = 1 &nbsp; (iii) x³ + 1/x³ = 2√5", ["ক) i ও ii", "খ) ii ও iii", "গ) i ও iii", "ঘ) i, ii ও iii"], None),
    ("২৭", "x⁴ + 1 = 3x² হলে x − 1/x = ?", ["ক) 1", "খ) √5", "গ) −1", "ঘ) −√5"], None),
    ("২৮", "x⁴ + 1 = 3x² হলে x³ + 1/x³ = ?", ["ক) 2√5", "খ) 2", "গ) 0", "ঘ) 4"], None),
    ("২৯", "p, q, r সান্তরিক হলে (p² + q²)/(q² + r²) = ?", ["ক) p/r", "খ) p/q", "গ) q/r", "ঘ) r/p"], None),
    ("৩০", "x : y = 5 : 6 হলে 3x : 5y = ?", ["ক) 1 : 2", "খ) 2 : 3", "গ) 3 : 5", "ঘ) 5 : 6"], None),
]

MCQ_DIAGRAMS = {
    "circle": """<div class="diagram"><svg viewBox="0 0 90 70" xmlns="http://www.w3.org/2000/svg"><circle cx="45" cy="35" r="24" fill="none" stroke="#000" stroke-width="0.9"/><line x1="45" y1="11" x2="45" y2="59" stroke="#000" stroke-width="0.7"/><line x1="21" y1="35" x2="69" y2="35" stroke="#000" stroke-width="0.7"/><text x="45" y="9" text-anchor="middle" font-size="7" font-family="DejaVu Sans">A</text><text x="71" y="38" font-size="7" font-family="DejaVu Sans">C</text><text x="45" y="66" text-anchor="middle" font-size="7" font-family="DejaVu Sans">B</text><text x="45" y="38" text-anchor="middle" font-size="7" font-family="DejaVu Sans">O</text><text x="58" y="24" font-size="6.5" font-family="DejaVu Sans">100°</text></svg></div>""",
    "parallelogram": """<div class="diagram"><svg viewBox="0 0 100 55" xmlns="http://www.w3.org/2000/svg"><polygon points="18,45 38,12 82,12 62,45" fill="none" stroke="#000" stroke-width="0.9"/><line x1="18" y1="45" x2="82" y2="12" stroke="#000" stroke-width="0.7"/><line x1="38" y1="12" x2="62" y2="45" stroke="#000" stroke-width="0.7"/><text x="12" y="48" font-size="7" font-family="DejaVu Sans">A</text><text x="34" y="10" font-size="7" font-family="DejaVu Sans">B</text><text x="84" y="14" font-size="7" font-family="DejaVu Sans">C</text><text x="64" y="50" font-size="7" font-family="DejaVu Sans">D</text><text x="50" y="30" font-size="7" font-family="DejaVu Sans">O</text></svg></div>""",
}

CIRCLE_DIAGRAM = """<div class="diagram"><svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="34" fill="none" stroke="#000" stroke-width="1"/><line x1="50" y1="16" x2="50" y2="84" stroke="#000" stroke-width="0.8"/><line x1="16" y1="50" x2="84" y2="50" stroke="#000" stroke-width="0.8"/><text x="50" y="12" text-anchor="middle" font-size="8" font-family="DejaVu Sans">P</text><text x="10" y="53" text-anchor="middle" font-size="8" font-family="DejaVu Sans">Q</text><text x="50" y="96" text-anchor="middle" font-size="8" font-family="DejaVu Sans">R</text><text x="90" y="53" text-anchor="middle" font-size="8" font-family="DejaVu Sans">S</text><text x="50" y="54" text-anchor="middle" font-size="8" font-family="DejaVu Sans">O</text></svg><div class="cap">OR = 5.5 সে.মি.</div></div>"""

FREQ_TABLE = """<table class="freq"><tr><th>শ্রেণিব্যাপ্তি</th><th>গণসংখ্যা</th></tr><tr><td>46-50</td><td>6</td></tr><tr><td>51-55</td><td>9</td></tr><tr><td>56-60</td><td>21</td></tr><tr><td>61-65</td><td>16</td></tr><tr><td>66-70</td><td>8</td></tr></table>"""

SHORT_ANSWERS = [
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


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def mcq_header() -> str:
    return f"""
<div class="header">
  <div class="school">{esc(SCHOOL)}</div>
  <div class="subject">গণিত</div>
  <div class="exam-title">বহুনির্বাচনি অভীক্ষা</div>
  <div class="meta"><span>সময়— ৩০ মিনিট</span><span>বিষয় কোড: ১&nbsp;&nbsp;০&nbsp;&nbsp;৯</span><span>পূর্ণমান— ৩০</span></div>
  <div class="note">(নির্দেশনা: প্রশ্নপত্রে দেওয়া চারটি বিকল্পের মধ্যে সঠিক উত্তরের বৃত্ত ভরে কালো কালি দিয়ে পূর্ণ করতে হবে।)</div>
</div>"""


def creative_header() -> str:
    return f"""
<div class="header">
  <div class="school">{esc(SCHOOL)}</div>
  <div class="subject">গণিত (সৃজনশীল)</div>
  <div class="meta"><span>সময়—২ ঘণ্টা ৩০ মিনিট</span><span>বিষয় কোড: ১&nbsp;&nbsp;০&nbsp;&nbsp;৯</span><span>পূর্ণমান— ৭০</span></div>
  <div class="note">(দ্রষ্টব্য: সৃজনশীল প্রশ্ন অংশের প্রত্যেক বিভাগ থেকে কমপক্ষে ১টি করে প্রশ্নের মোট ৪টি এবং সংক্ষিপ্ত-উত্তর প্রশ্ন থেকে যেকোনো ১০টি প্রশ্নের উত্তর দাও।)</div>
</div>"""


def mcq_item(num: str, text: str, opts: list[str], diagram: str | None) -> str:
    diag = MCQ_DIAGRAMS.get(diagram, "") if diagram else ""
    opt_html = "".join(f'<div class="opt">{esc(o)}</div>' for o in opts)
    return f'<div class="mcq"><div class="qtext"><span class="num">{esc(num)}.</span> {text}</div>{diag}{opt_html}</div>'


def creative_sub(label: str, text: str, mark: str) -> str:
    return f'<div class="sub"><span class="label">{esc(label)})</span><span class="text">{esc(text)}</span><span class="mark">{esc(mark)}</span></div>'


def creative_qhead(num: str, text: str) -> str:
    return f'<div class="q">▶ {esc(num)}. {esc(text)}</div>'


def mcq_panel(questions: list) -> str:
    body = "".join(mcq_item(*q) for q in questions)
    return mcq_header() + f'<div class="inner-cols">{body}</div>'


def creative_left() -> str:
    return f"""{creative_header()}
<div class="title">সৃজনশীল প্রশ্ন</div>
<div class="section">ক-বিভাগ: বীজগণিত</div>
{creative_qhead("১", "U = {{x ∈ N : x < 9}} সার্বিক সেট। A = {{x ∈ N : x² > 5 এবং x³ < 150}}, B = {{x ∈ N : x মৌলিক সংখ্যা}}, অন্বয় R = {{(x, y) : x ∈ B, y ∈ B এবং y = x + 2}}")}
{creative_sub("ক", "A সেটকে তালিকা পদ্ধতিতে প্রকাশ কর।", "২")}
{creative_sub("খ", "দেখাও যে, (A ∩ B)' = A' ∪ B'", "৪")}
{creative_sub("গ", "R অন্বয়টিকে তালিকা পদ্ধতিতে প্রকাশ করে তার ডোমেন ও রেঞ্জ নির্ণয় কর।", "৪")}
{creative_qhead("২", "x² = 11 + √120 এবং A = y³ − 3my² + 3y − m")}
{creative_sub("ক", "উৎপাদকে বিশ্লেষণ কর: b² + 8b + 15 − z² + 2z", "২")}
{creative_sub("খ", "প্রমাণ কর যে, x³(x³ + 1/x³) = 922√6", "৪")}
{creative_sub("গ", "A = 0 হলে, প্রমাণ কর যে, y = (∛(m+1) + ∛(m−1)) / (∛(m+1) − ∛(m−1))", "৪")}
<div class="section">খ-বিভাগ: জ্যামিতি</div>
{creative_qhead("৩", "a = 6 সে.মি., b = 7 সে.মি. এবং ∠x = 45°")}
{creative_sub("ক", "একটি রম্বস আঁক যার বাহুর দৈর্ঘ্য a এবং একটি কোণ ∠x এর সমান। [অঙ্কনের চিহ্ন আবশ্যক]", "২")}
{creative_sub("খ", "এমন একটি ত্রিভুজ আঁক যার ভূমির দৈর্ঘ্য (a − 1) সে.মি., ভূমি সংলগ্ন কোণ ∠x এবং অপর দুই বাহুর সমষ্টি b। [অঙ্কনের চিহ্ন ও বিবরণ আবশ্যক]", "৪")}
{creative_sub("গ", "'খ' এর বর্ণিত ত্রিভুজের পরিবৃত্ত আঁক। [অঙ্কনের চিহ্ন ও বিবরণ আবশ্যক]", "৪")}
{creative_qhead("৪", "চিত্রে, O কেন্দ্র বিশিষ্ট PQRS একটি বৃত্ত এবং OR = 5.5 সে.মি.")}
{CIRCLE_DIAGRAM}
{creative_sub("ক", "উদ্দীপকের বৃত্তের পরিধি নির্ণয় কর।", "২")}
{creative_sub("খ", "প্রমাণ কর যে, ∠QPS + ∠QRS = 2 সমকোণ", "৪")}
{creative_sub("গ", "PR ও QS কর্ণদ্বয় পরস্পর N বিন্দুতে ছেদ করলে, ∠POQ + ∠ROS = 2∠PNQ প্রমাণ কর।", "৪")}
<div class="section">গ-বিভাগ: ত্রিকোণমিতি ও পরিমিতি</div>
{creative_qhead("৫", "cot θ + cos θ = p এবং cot θ − cos θ = q")}
{creative_sub("ক", "cot(A − 30°) = 1 হলে, A এর মান নির্ণয় কর।", "২")}
{creative_sub("খ", "প্রমাণ কর যে, cosec²θ = √(pq) · sec²θ", "৪")}
{creative_sub("গ", "p/q = (2+√3)/(2−√3) হলে, θ (< 90°) এর মান নির্ণয় কর।", "৪")}
{creative_qhead("৬", "একটি লোহার পাইপের ভিতরের ও বাইরের ব্যাস যথাক্রমে ৪ সে.মি. ও ১০ সে.মি. এবং পাইপের উচ্চতা ৪ মিটার। ১ ঘন সে.মি. লোহার ওজন ৭.২ গ্রাম।")}
{creative_sub("ক", "পাইপের পুরুত্ব কত মিটার নির্ণয় কর।", "২")}"""


def creative_right() -> str:
    short_html = "".join(creative_sub(l, t, "২") for l, t in SHORT_ANSWERS)
    return f"""{creative_header()}
{creative_sub("খ", "পাইপের বাইরের বক্রতলের ক্ষেত্রফল নির্ণয় কর।", "৪")}
{creative_sub("গ", "পাইপে ব্যবহৃত লোহার ওজন কত কেজি নির্ণয় কর।", "৪")}
<div class="section">ঘ-বিভাগ: পরিসংখ্যান</div>
{creative_qhead("৭", "১০ম শ্রেণির ৬০ জন শিক্ষার্থীর ওজনের (কেজিতে) গণসংখ্যা নিবেশন দেওয়া হলো:")}
{FREQ_TABLE}
{creative_sub("ক", "প্রচুরক শ্রেণির আগের শ্রেণির মধ্যমান নির্ণয় কর।", "২")}
{creative_sub("খ", "প্রদত্ত উপাত্তের গাণিতিক গড় নির্ণয় কর।", "৪")}
{creative_sub("গ", "বর্ণনাসহ প্রদত্ত উপাত্তের অজিভ রেখা অঙ্কন কর।", "৪")}
{creative_qhead("৮", "নিচে ৩০ জন শিক্ষার্থীর নির্বাচনী পরীক্ষায় গণিতে প্রাপ্ত নম্বর দেওয়া হলো: 55, 40, 35, 60, 58, 60, 45, 57, 46, 50, 52, 61, 65, 50, 68, 40, 56, 54, 60, 46, 60, 65, 48, 60, 36, 58, 50, 60, 47, 43")}
{creative_sub("ক", "শ্রেণিব্যাপ্তি ৫ হলে শ্রেণি সংখ্যা নির্ণয় কর।", "২")}
{creative_sub("খ", "গণসংখ্যা সারণি তৈরি করে মধ্যক নির্ণয় কর।", "৪")}
{creative_sub("গ", "সারণি হতে বিবরণসহ উপাত্তের গণসংখ্যা বহুভুজ অঙ্কন কর।", "৪")}
<div class="short-head">সংক্ষিপ্ত-উত্তর প্রশ্ন</div>
<div class="short-note">[যেকোনো ১০টির উত্তর দাও — প্রতিটি ২]</div>
<div class="q">৯.</div>
{short_html}"""


def build_html(mcq_only: bool = False, creative_only: bool = False) -> str:
    split = len(MCQ_QUESTIONS) // 2
    mcq_left = MCQ_QUESTIONS[:split]
    mcq_right = MCQ_QUESTIONS[split:]

    mcq_page = f"""
<div class="page mcq-page">
  <div class="sheet">
    <div class="panel left">{mcq_panel(mcq_left)}</div>
    <div class="fold-gap"></div>
    <div class="panel right">{mcq_panel(mcq_right)}</div>
  </div>
</div>"""

    creative_page = f"""
<div class="page creative-page">
  <div class="sheet">
    <div class="col left">{creative_left()}</div>
    <div class="fold-gap"></div>
    <div class="col right">{creative_right()}</div>
  </div>
</div>"""

    if mcq_only:
        body = mcq_page
    elif creative_only:
        body = creative_page
    else:
        body = mcq_page + creative_page

    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8">
<style>
{FONTS}
@page {{ size: A4 landscape; margin: 4.5mm 6mm 5mm 6mm; }}
* {{ box-sizing: border-box; }}
body {{
  font-family: "Noto Bengali", sans-serif;
  color: #000;
  margin: 0;
}}
.page {{ page-break-after: always; }}
.page:last-child {{ page-break-after: auto; }}

/* MCQ page */
.mcq-page {{
  font-size: 7.6pt;
  line-height: 1.32;
}}
.mcq-page .sheet {{ display: flex; align-items: stretch; }}
.mcq-page .panel {{ flex: 1; padding: 0 2mm; min-width: 0; }}
.mcq-page .fold-gap {{ width: 22mm; flex-shrink: 0; }}
.mcq-page .inner-cols {{ column-count: 2; column-gap: 3.5mm; }}
.mcq-page .header {{ margin-bottom: 1.2mm; text-align: center; }}
.mcq-page .header .school {{ font-size: 10pt; font-weight: bold; }}
.mcq-page .header .subject {{ font-size: 9pt; font-weight: bold; }}
.mcq-page .header .exam-title {{ font-size: 8.8pt; font-weight: bold; margin: 0.2mm 0; }}
.mcq-page .header .meta {{ display: flex; justify-content: space-between; font-size: 8pt; margin: 0.4mm 0; }}
.mcq-page .header .note {{ font-size: 7.2pt; margin-bottom: 0.8mm; text-align: justify; }}
.mcq-page .mcq {{ margin-bottom: 0.75mm; break-inside: avoid; }}
.mcq-page .qtext {{ font-weight: bold; font-size: 7.7pt; }}
.mcq-page .opt {{ font-size: 7.4pt; padding-left: 2.5mm; margin: 0.05mm 0; }}
.mcq-page .diagram {{ text-align: center; margin: 0.2mm 0; }}
.mcq-page .diagram svg {{ width: 14mm; height: auto; }}

/* Creative page */
.creative-page {{
  font-size: 8.4pt;
  line-height: 1.36;
}}
.creative-page .sheet {{ display: flex; align-items: stretch; min-height: 100%; }}
.creative-page .col {{ flex: 1; padding: 0 2.5mm; min-width: 0; }}
.creative-page .fold-gap {{ width: 22mm; flex-shrink: 0; }}
.creative-page .header {{ margin-bottom: 1.5mm; text-align: center; }}
.creative-page .header .school {{ font-size: 10.5pt; font-weight: bold; }}
.creative-page .header .subject {{ font-size: 9.5pt; font-weight: bold; }}
.creative-page .header .meta {{ display: flex; justify-content: space-between; font-size: 8.4pt; margin: 0.5mm 0; }}
.creative-page .header .note {{ font-size: 7.8pt; margin-bottom: 1mm; text-align: justify; }}
.creative-page .section {{ font-weight: bold; font-size: 8.8pt; margin: 0.8mm 0 0.3mm; }}
.creative-page .title {{ font-weight: bold; font-size: 9.2pt; margin: 0.3mm 0; }}
.creative-page .q {{ font-weight: bold; font-size: 8.8pt; margin: 0.7mm 0 0.15mm; break-inside: avoid; }}
.creative-page .sub {{
  display: grid;
  grid-template-columns: 4.5mm 1fr 5mm;
  gap: 0.5mm;
  margin: 0.12mm 0;
  font-size: 8.2pt;
  break-inside: avoid;
}}
.creative-page .sub .mark {{ text-align: right; }}
.creative-page table.freq {{
  border-collapse: collapse;
  margin: 0.7mm auto;
  font-size: 7.8pt;
  break-inside: avoid;
}}
.creative-page table.freq th, .creative-page table.freq td {{
  border: 0.35pt solid #000;
  padding: 0.7mm 2.8mm;
  text-align: center;
}}
.creative-page .diagram {{ text-align: center; margin: 0.4mm 0; break-inside: avoid; }}
.creative-page .diagram svg {{ width: 21mm; height: 21mm; }}
.creative-page .diagram .cap {{ font-size: 7.6pt; }}
.creative-page .short-head {{ font-weight: bold; font-size: 8.8pt; margin-top: 0.6mm; }}
.creative-page .short-note {{ font-size: 7.8pt; margin-bottom: 0.2mm; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def _write(path: str, mcq_only: bool = False, creative_only: bool = False) -> None:
    HTML(string=build_html(mcq_only=mcq_only, creative_only=creative_only), base_url=str(Path("/workspace"))).write_pdf(path)


def build(path: str) -> None:
    _write(path)


def build_mcq(path: str) -> None:
    _write(path, mcq_only=True)


def build_creative(path: str) -> None:
    _write(path, creative_only=True)


if __name__ == "__main__":
    build("/workspace/SSC_Math_Exam.pdf")
    build_mcq("/workspace/SSC_Math_MCQ_Test.pdf")
    build_creative("/workspace/SSC_Math_Special_Assignment.pdf")
    print("Created: SSC_Math_Exam.pdf, SSC_Math_MCQ_Test.pdf, SSC_Math_Special_Assignment.pdf")
