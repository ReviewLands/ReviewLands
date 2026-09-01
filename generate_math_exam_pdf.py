#!/usr/bin/env python3
"""Typed A4 SSC Math Special Assignment — WeasyPrint for correct Bengali shaping."""

from __future__ import annotations

import html
from pathlib import Path

from weasyprint import HTML

NOTO = "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf"
NOTO_B = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def sub(label: str, text: str, mark: str) -> str:
    return (
        f'<div class="sub"><span class="label">{esc(label)})</span>'
        f'<span class="text">{esc(text)}</span>'
        f'<span class="mark">{esc(mark)}</span></div>'
    )


def qhead(num: str, text: str) -> str:
    return f'<div class="q">▶ {esc(num)}. {esc(text)}</div>'


def build_html() -> str:
    short = [
        ("ক", "X = {1, 3, 5}, Y = {2, 4, 6}, M = X ∩ Y হলে, P(M) নির্ণয় কর।"),
        ("খ", "f(x) = (6x + 6)/(3x + 5) হলে, f(1/3) এর মান নির্ণয় কর।"),
        ("গ", "x⁴ + x² + 1 কে উৎপাদকে বিশ্লেষণ কর।"),
        ("ঘ", "2x − 2/x = 4 হলে, x² + 1/x² এর মান নির্ণয় কর।"),
        ("ঙ", "g(a) = a³ + 3a + 40 কে (a + 3) দ্বারা ভাগ করলে ভাগশেষ কত হবে তা নির্ণয় কর।"),
        ("চ", "দুইটি সংখ্যার অনুপাত 3:5 এবং এদের গ.সা.গু. 5 হলে, সংখ্যা দুটির ল.সা.গু. নির্ণয় কর।"),
        ("ছ", "4, a এবং 9 ক্রমিক সমানুপাতি হলে, a এর মান নির্ণয় কর।"),
        ("জ", "পেন্সিল কম্পাসের সাহায্যে 75° কোণ অঙ্কন কর।"),
        (
            "ঝ",
            "কোন বৃত্তের একই চাপের উপর দণ্ডায়মান কেন্দ্রস্থ কোণ x + 40° এবং "
            "বৃত্তস্থ কোণ x + 10° হলে, x এর মান নির্ণয় কর।",
        ),
        ("ঞ", "tan x = cot 5x হলে, x এর মান নির্ণয় কর।"),
        ("ট", "cosec²θ + cot²θ = 2 হলে, csc⁴θ − cot⁴θ = কত?"),
        ("ঠ", "একটি রম্বসের কর্ণদ্বয়ের দৈর্ঘ্য 12 সে.মি. ও 16 সে.মি. হলে, রম্বসটির পরিসীমা নির্ণয় কর।"),
        ("ড", "কেন্দ্রীয় প্রবণতা কাকে বলে? এর পরিমাপগুলো লেখ।"),
        ("ঢ", "কোন শ্রেণির উচ্চসীমা 55 এবং মধ্যমান 52.5 হলে ঐ শ্রেণির নিম্নসীমা নির্ণয় কর।"),
        ("ণ", "44, 30, 51, 53, 25, 22, 18, 32 সংখ্যাগুলোর মধ্যক নির্ণয় কর।"),
    ]
    short_html = "\n".join(sub(l, t, "২") for l, t in short)

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
@page {{ size: A4; margin: 7mm 9mm 9mm 9mm; }}
* {{ box-sizing: border-box; }}
body {{
  font-family: "Noto Bengali", sans-serif;
  font-size: 7.6pt;
  line-height: 1.38;
  color: #000;
  margin: 0;
}}
.header {{ margin-bottom: 1.5mm; }}
.header .brand {{ font-size: 7.2pt; }}
.header .school {{ font-size: 9.2pt; font-weight: bold; margin: 0.4mm 0; }}
.header .subject {{ font-size: 8.8pt; font-weight: bold; }}
.header .meta {{
  display: flex;
  justify-content: space-between;
  font-size: 7.8pt;
  margin: 0.5mm 0;
}}
.header .note {{
  font-size: 7.2pt;
  margin: 0.8mm 0 1.2mm;
  text-align: justify;
}}
.section {{ font-weight: bold; font-size: 8pt; margin: 1mm 0 0.4mm; }}
.title {{ font-weight: bold; font-size: 8.5pt; margin: 0.6mm 0; }}
.columns {{ column-count: 2; column-gap: 4.5mm; }}
.q {{ font-weight: bold; font-size: 8pt; margin: 0.8mm 0 0.2mm; break-inside: avoid; }}
.sub {{
  display: grid;
  grid-template-columns: 4mm 1fr 4mm;
  gap: 0.5mm;
  margin: 0.15mm 0;
  font-size: 7.6pt;
  break-inside: avoid;
}}
.sub .label {{ white-space: nowrap; }}
.sub .text {{ text-align: left; }}
.sub .mark {{ text-align: right; white-space: nowrap; }}
table.freq {{
  border-collapse: collapse;
  margin: 0.8mm auto;
  font-size: 7.2pt;
  break-inside: avoid;
}}
table.freq th, table.freq td {{
  border: 0.35pt solid #000;
  padding: 0.6mm 2.5mm;
  text-align: center;
}}
.diagram {{
  text-align: center;
  margin: 0.5mm 0;
  break-inside: avoid;
}}
.diagram svg {{ width: 22mm; height: 22mm; }}
.diagram .cap {{ font-size: 7pt; margin-top: 0.3mm; }}
.short-head {{ font-weight: bold; font-size: 8pt; margin-top: 0.8mm; }}
.short-note {{ font-size: 7.2pt; margin-bottom: 0.3mm; }}
.footer {{
  margin-top: 2mm;
  padding-top: 0.8mm;
  border-top: 0.35pt solid #000;
  text-align: center;
  font-size: 6.5pt;
}}
</style>
</head>
<body>
<div class="header">
  <div class="brand">পাঞ্জেরী এসএসসি স্পেশাল অ্যাসাইনমেন্ট ++ | গণিত</div>
  <div class="school">৭৩. আইডিয়াল স্কুল অ্যান্ড কলেজ, মতিঝিল, ঢাকা</div>
  <div class="subject">গণিত (সৃজনশীল)</div>
  <div class="meta">
    <span>সময়—২ ঘণ্টা ৩০ মিনিট</span>
    <span>বিষয় কোড: ১&nbsp;&nbsp;০&nbsp;&nbsp;৯</span>
    <span>পূর্ণমান— ৭০</span>
  </div>
  <div class="note">(দ্রষ্টব্য: সৃজনশীল প্রশ্ন অংশের প্রত্যেক বিভাগ থেকে কমপক্ষে ১টি করে প্রশ্নের মোট ৪টি এবং সংক্ষিপ্ত-উত্তর প্রশ্ন থেকে যেকোনো ১০টি প্রশ্নের উত্তর দাও।)</div>
</div>

<div class="columns">
  <div class="title">সৃজনশীল প্রশ্ন</div>
  <div class="section">ক-বিভাগ: বীজগণিত</div>

  {qhead("১", "U = {{x ∈ N : x < 9}} সার্বিক সেট। A = {{x ∈ N : x² > 5 এবং x³ < 150}}, B = {{x ∈ N : x মৌলিক সংখ্যা}}, অন্বয় R = {{(x, y) : x ∈ B, y ∈ B এবং y = x + 2}}")}
  {sub("ক", "A সেটকে তালিকা পদ্ধতিতে প্রকাশ কর।", "২")}
  {sub("খ", "দেখাও যে, (A ∩ B)' = A' ∪ B'", "৪")}
  {sub("গ", "R অন্বয়টিকে তালিকা পদ্ধতিতে প্রকাশ করে তার ডোমেন ও রেঞ্জ নির্ণয় কর।", "৪")}

  {qhead("২", "x² = 11 + √120 এবং A = y³ − 3my² + 3y − m")}
  {sub("ক", "উৎপাদকে বিশ্লেষণ কর: b² + 8b + 15 − z² + 2z", "২")}
  {sub("খ", "প্রমাণ কর যে, x³(x³ + 1/x³) = 922√6", "৪")}
  {sub("গ", "A = 0 হলে, প্রমাণ কর যে, y = (∛(m+1) + ∛(m−1)) / (∛(m+1) − ∛(m−1))", "৪")}

  <div class="section">খ-বিভাগ: জ্যামিতি</div>

  {qhead("৩", "a = 6 সে.মি., b = 7 সে.মি. এবং ∠x = 45°")}
  {sub("ক", "একটি রম্বস আঁক যার বাহুর দৈর্ঘ্য a এবং একটি কোণ ∠x এর সমান। [অঙ্কনের চিহ্ন আবশ্যক]", "২")}
  {sub("খ", "এমন একটি ত্রিভুজ আঁক যার ভূমির দৈর্ঘ্য (a − 1) সে.মি., ভূমি সংলগ্ন কোণ ∠x এবং অপর দুই বাহুর সমষ্টি b। [অঙ্কনের চিহ্ন ও বিবরণ আবশ্যক]", "৪")}
  {sub("গ", "'খ' এর বর্ণিত ত্রিভুজের পরিবৃত্ত আঁক। [অঙ্কনের চিহ্ন ও বিবরণ আবশ্যক]", "৪")}

  {qhead("৪", "চিত্রে, O কেন্দ্র বিশিষ্ট PQRS একটি বৃত্ত এবং OR = 5.5 সে.মি.")}
  <div class="diagram">
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="50" r="34" fill="none" stroke="#000" stroke-width="1"/>
      <line x1="50" y1="16" x2="50" y2="84" stroke="#000" stroke-width="0.8"/>
      <line x1="16" y1="50" x2="84" y2="50" stroke="#000" stroke-width="0.8"/>
      <text x="50" y="12" text-anchor="middle" font-size="8" font-family="DejaVu Sans, sans-serif">P</text>
      <text x="10" y="53" text-anchor="middle" font-size="8" font-family="DejaVu Sans, sans-serif">Q</text>
      <text x="50" y="96" text-anchor="middle" font-size="8" font-family="DejaVu Sans, sans-serif">R</text>
      <text x="90" y="53" text-anchor="middle" font-size="8" font-family="DejaVu Sans, sans-serif">S</text>
      <text x="50" y="54" text-anchor="middle" font-size="8" font-family="DejaVu Sans, sans-serif">O</text>
    </svg>
    <div class="cap">OR = 5.5 সে.মি.</div>
  </div>
  {sub("ক", "উদ্দীপকের বৃত্তের পরিধি নির্ণয় কর।", "২")}
  {sub("খ", "প্রমাণ কর যে, ∠QPS + ∠QRS = 2 সমকোণ", "৪")}
  {sub("গ", "PR ও QS কর্ণদ্বয় পরস্পর N বিন্দুতে ছেদ করলে, ∠POQ + ∠ROS = 2∠PNQ প্রমাণ কর।", "৪")}

  <div class="section">গ-বিভাগ: ত্রিকোণমিতি ও পরিমিতি</div>

  {qhead("৫", "cot θ + cos θ = p এবং cot θ − cos θ = q")}
  {sub("ক", "cot(A − 30°) = 1 হলে, A এর মান নির্ণয় কর।", "২")}
  {sub("খ", "প্রমাণ কর যে, cosec²θ = √(pq) · sec²θ", "৪")}
  {sub("গ", "p/q = (2+√3)/(2−√3) হলে, θ (< 90°) এর মান নির্ণয় কর।", "৪")}

  {qhead("৬", "একটি লোহার পাইপের ভিতরের ও বাইরের ব্যাস যথাক্রমে ৪ সে.মি. ও ১০ সে.মি. এবং পাইপের উচ্চতা ৪ মিটার। ১ ঘন সে.মি. লোহার ওজন ৭.২ গ্রাম।")}
  {sub("ক", "পাইপের পুরুত্ব কত মিটার নির্ণয় কর।", "২")}
  {sub("খ", "পাইপের বাইরের বক্রতলের ক্ষেত্রফল নির্ণয় কর।", "৪")}
  {sub("গ", "পাইপে ব্যবহৃত লোহার ওজন কত কেজি নির্ণয় কর।", "৪")}

  <div class="section">ঘ-বিভাগ: পরিসংখ্যান</div>

  {qhead("৭", "১০ম শ্রেণির ৬০ জন শিক্ষার্থীর ওজনের (কেজিতে) গণসংখ্যা নিবেশন দেওয়া হলো:")}
  <table class="freq">
    <tr><th>শ্রেণিব্যাপ্তি</th><th>গণসংখ্যা</th></tr>
    <tr><td>46-50</td><td>6</td></tr>
    <tr><td>51-55</td><td>9</td></tr>
    <tr><td>56-60</td><td>21</td></tr>
    <tr><td>61-65</td><td>16</td></tr>
    <tr><td>66-70</td><td>8</td></tr>
  </table>
  {sub("ক", "প্রচুরক শ্রেণির আগের শ্রেণির মধ্যমান নির্ণয় কর।", "২")}
  {sub("খ", "প্রদত্ত উপাত্তের গাণিতিক গড় নির্ণয় কর।", "৪")}
  {sub("গ", "বর্ণনাসহ প্রদত্ত উপাত্তের অজিভ রেখা অঙ্কন কর।", "৪")}

  {qhead("৮", "নিচে ৩০ জন শিক্ষার্থীর নির্বাচনী পরীক্ষায় গণিতে প্রাপ্ত নম্বর দেওয়া হলো: 55, 40, 35, 60, 58, 60, 45, 57, 46, 50, 52, 61, 65, 50, 68, 40, 56, 54, 60, 46, 60, 65, 48, 60, 36, 58, 50, 60, 47, 43")}
  {sub("ক", "শ্রেণিব্যাপ্তি ৫ হলে শ্রেণি সংখ্যা নির্ণয় কর।", "২")}
  {sub("খ", "গণসংখ্যা সারণি তৈরি করে মধ্যক নির্ণয় কর।", "৪")}
  {sub("গ", "সারণি হতে বিবরণসহ উপাত্তের গণসংখ্যা বহুভুজ অঙ্কন কর।", "৪")}

  <div class="short-head">সংক্ষিপ্ত-উত্তর প্রশ্ন</div>
  <div class="short-note">[যেকোনো ১০টির উত্তর দাও — প্রতিটি ২]</div>
  <div class="q">৯.</div>
  {short_html}
</div>

<div class="footer">[অঃ অধ্যায় ৫ পৃষ্ঠা ১০১ প্রশ্ন ৪] | [অঃ অধ্যায় ৯ পৃষ্ঠা ২৩৪ প্রশ্ন ৪৯]</div>
</body>
</html>"""


def build(path: str) -> None:
    html_doc = build_html()
    HTML(string=html_doc, base_url=str(Path("/workspace"))).write_pdf(path)


if __name__ == "__main__":
    out = "/workspace/SSC_Math_Special_Assignment.pdf"
    build(out)
    print(f"Created: {out}")
