#!/usr/bin/env python3
"""Generate Chapter 6.1 test PDF via HTML/WeasyPrint for correct Bengali rendering."""
import os
from pathlib import Path

HTML = r"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;700&family=Times+New+Roman&display=swap" rel="stylesheet">
<style>
  @page { size: A4; margin: 14mm 16mm; }
  * { box-sizing: border-box; }
  body { font-family: 'Noto Sans Bengali', sans-serif; font-size: 11pt; color: #111; }
  .en { font-family: 'Times New Roman', Times, serif; }
  .copy { page-break-inside: avoid; }
  h1 { font-family: 'Times New Roman', Times, serif; font-weight: bold; font-size: 18pt; text-align: center; margin: 0 0 4px; }
  .sub { font-family: 'Times New Roman', Times, serif; text-align: center; margin: 2px 0; }
  .meta { font-family: 'Times New Roman', Times, serif; font-size: 11pt; display: flex; justify-content: space-between; margin: 10px 0 6px; }
  .fields { font-family: 'Times New Roman', Times, serif; font-size: 11pt; margin-bottom: 8px; }
  .instr { font-size: 10pt; margin-bottom: 14px; line-height: 1.5; }
  .cut { text-align: center; font-family: 'Times New Roman', Times, serif; font-size: 9pt; border-top: 1px dashed #666; margin: 14px 0 10px; padding-top: 6px; }
  .section-title { font-weight: 700; font-size: 12pt; margin: 0 0 4px; display: flex; justify-content: space-between; align-items: baseline; }
  .section-note { font-size: 9pt; color: #333; margin-bottom: 10px; }
  .problem { margin-bottom: 12px; }
  .problem-head { font-family: 'Times New Roman', Times, serif; display: flex; justify-content: space-between; margin-bottom: 4px; }
  .prompt { font-family: 'Times New Roman', Times, serif; margin: 0 0 4px 4px; }
  .eqs { font-family: 'Times New Roman', Times, serif; margin: 0 0 2px 24px; line-height: 1.55; }
  .ref { font-size: 8.5pt; color: #444; margin-left: 4px; line-height: 1.35; }
  .ref-en { font-family: 'Times New Roman', Times, serif; font-size: 8.5pt; color: #444; margin-left: 4px; }
  .total { font-family: 'Times New Roman', Times, serif; font-size: 10pt; text-align: right; margin-top: 6px; }
</style>
</head>
<body>

<div class="copy">
  <h1>CLASS TEST</h1>
  <p class="sub">Mathematics</p>
  <p class="sub">Chapter 6.1 — Simultaneous Equations</p>
  <div class="meta">
    <span>Time: 30 minutes</span>
    <span>Full Marks: 20</span>
  </div>
  <div class="fields">Name: _________________________ &nbsp;&nbsp; Roll: __________ &nbsp;&nbsp; Date: __________</div>
  <p class="instr">নির্দেশনা: সব প্রশ্নের উত্তর দাও। প্রতিটি উপ-প্রশ্নের মান ৫। ভগ্নাংশ ব্যবহার করা যাবে না।</p>

  <div class="section-title">
    <span>১. সৃজনশীল প্রশ্ন — অপনয়ন পদ্ধতি</span>
    <span class="en">10</span>
  </div>
  <p class="section-note">অনুশীলনী ৬.১ — প্রশ্ন ৭ ও ৮ (ax + by = ab ধরন)</p>

  <div class="problem">
    <div class="problem-head"><span class="en">(ক)</span><span class="en">5</span></div>
    <p class="prompt">Solve by the elimination method:</p>
    <div class="eqs">2x + y = 6<br>x + 2y = 6</div>
    <div class="ref">[অনুশীলনী ৬.১ — প্রশ্ন ৭]</div>
    <div class="ref-en">ax + by = ab, bx + ay = ab</div>
  </div>
  <div class="problem">
    <div class="problem-head"><span class="en">(খ)</span><span class="en">5</span></div>
    <p class="prompt">Solve by the elimination method:</p>
    <div class="eqs">2x - y = 6<br>x - 2y = 6</div>
    <div class="ref">[অনুশীলনী ৬.১ — প্রশ্ন ৮]</div>
    <div class="ref-en">ax - by = ab, bx - ay = ab</div>
  </div>

  <div class="section-title" style="margin-top:10px;">
    <span>২. সৃজনশীল প্রশ্ন — প্রতিস্থাপন পদ্ধতি</span>
    <span class="en">10</span>
  </div>
  <p class="section-note">অনুশীলনী ৬.১ — প্রশ্ন ৭ ও ৯ (ax + by = ab ধরন)</p>

  <div class="problem">
    <div class="problem-head"><span class="en">(ক)</span><span class="en">5</span></div>
    <p class="prompt">Solve by the substitution method:</p>
    <div class="eqs">2x + y = 6<br>x + 2y = 6</div>
    <div class="ref">[অনুশীলনী ৬.১ — প্রশ্ন ৭]</div>
    <div class="ref-en">ax + by = ab, bx + ay = ab</div>
  </div>
  <div class="problem">
    <div class="problem-head"><span class="en">(খ)</span><span class="en">5</span></div>
    <p class="prompt">Solve by the substitution method:</p>
    <div class="eqs">5x - 2y = 3<br>5x + 2y = 7</div>
    <div class="ref">[অনুশীলনী ৬.১ — প্রশ্ন ৯]</div>
    <div class="ref-en">ax - by = a - b, ax + by = a + b</div>
  </div>

  <p class="total">Total: 4 x 5 = 20</p>
</div>

<div class="cut">— CUT HERE —</div>

<div class="copy">
  <h1>CLASS TEST</h1>
  <p class="sub">Mathematics</p>
  <p class="sub">Chapter 6.1 — Simultaneous Equations</p>
  <div class="meta">
    <span>Time: 30 minutes</span>
    <span>Full Marks: 20</span>
  </div>
  <div class="fields">Name: _________________________ &nbsp;&nbsp; Roll: __________ &nbsp;&nbsp; Date: __________</div>
  <p class="instr">নির্দেশনা: সব প্রশ্নের উত্তর দাও। প্রতিটি উপ-প্রশ্নের মান ৫। ভগ্নাংশ ব্যবহার করা যাবে না।</p>

  <div class="section-title">
    <span>১. সৃজনশীল প্রশ্ন — অপনয়ন পদ্ধতি</span>
    <span class="en">10</span>
  </div>
  <p class="section-note">অনুশীলনী ৬.১ — প্রশ্ন ৭ ও ৮ (ax + by = ab ধরন)</p>

  <div class="problem">
    <div class="problem-head"><span class="en">(ক)</span><span class="en">5</span></div>
    <p class="prompt">Solve by the elimination method:</p>
    <div class="eqs">2x + y = 6<br>x + 2y = 6</div>
    <div class="ref">[অনুশীলনী ৬.১ — প্রশ্ন ৭]</div>
    <div class="ref-en">ax + by = ab, bx + ay = ab</div>
  </div>
  <div class="problem">
    <div class="problem-head"><span class="en">(খ)</span><span class="en">5</span></div>
    <p class="prompt">Solve by the elimination method:</p>
    <div class="eqs">2x - y = 6<br>x - 2y = 6</div>
    <div class="ref">[অনুশীলনী ৬.১ — প্রশ্ন ৮]</div>
    <div class="ref-en">ax - by = ab, bx - ay = ab</div>
  </div>

  <div class="section-title" style="margin-top:10px;">
    <span>২. সৃজনশীল প্রশ্ন — প্রতিস্থাপন পদ্ধতি</span>
    <span class="en">10</span>
  </div>
  <p class="section-note">অনুশীলনী ৬.১ — প্রশ্ন ৭ ও ৯ (ax + by = ab ধরন)</p>

  <div class="problem">
    <div class="problem-head"><span class="en">(ক)</span><span class="en">5</span></div>
    <p class="prompt">Solve by the substitution method:</p>
    <div class="eqs">2x + y = 6<br>x + 2y = 6</div>
    <div class="ref">[অনুশীলনী ৬.১ — প্রশ্ন ৭]</div>
    <div class="ref-en">ax + by = ab, bx + ay = ab</div>
  </div>
  <div class="problem">
    <div class="problem-head"><span class="en">(খ)</span><span class="en">5</span></div>
    <p class="prompt">Solve by the substitution method:</p>
    <div class="eqs">5x - 2y = 3<br>5x + 2y = 7</div>
    <div class="ref">[অনুশীলনী ৬.১ — প্রশ্ন ৯]</div>
    <div class="ref-en">ax - by = a - b, ax + by = a + b</div>
  </div>

  <p class="total">Total: 4 x 5 = 20</p>
</div>

</body>
</html>
"""

SOLUTIONS_HTML = r"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;700&family=Times+New+Roman&display=swap" rel="stylesheet">
<style>
  @page { size: A4; margin: 16mm; }
  body { font-family: 'Noto Sans Bengali', sans-serif; font-size: 10.5pt; line-height: 1.45; }
  .en { font-family: 'Times New Roman', Times, serif; }
  h1 { text-align: center; font-weight: 700; font-size: 14pt; }
  h2 { font-weight: 700; font-size: 11pt; margin-top: 16px; }
  .math { font-family: 'Times New Roman', Times, serif; }
</style>
</head>
<body>
<h1>সমাধান (Answer Key)</h1>
<p class="en" style="text-align:center;">অনুশীলনী ৬.১ — প্রশ্ন ৭, ৮, ৯ | Full Marks: 20</p>

<h2>১. অপনয়ন পদ্ধতি</h2>
<p><strong>(ক) প্রশ্ন ৭:</strong> <span class="math">2x + y = 6, x + 2y = 6</span></p>
<p>সমীকরণ (ii) × 2: <span class="math">2x + 4y = 12</span> ... (iii)</p>
<p>(iii) − (i): <span class="math">3y = 6 → y = 2</span></p>
<p><span class="math">2x + 2 = 6 → x = 2</span></p>
<p><strong>∴ (x, y) = (2, 2)</strong></p>

<p><strong>(খ) প্রশ্ন ৮:</strong> <span class="math">2x - y = 6, x - 2y = 6</span></p>
<p>সমীকরণ (ii) × 2: <span class="math">2x - 4y = 12</span> ... (iii)</p>
<p>(i) − (iii): <span class="math">3y = -6 → y = -2</span></p>
<p><span class="math">2x - (-2) = 6 → x = 2</span></p>
<p><strong>∴ (x, y) = (2, -2)</strong></p>

<h2>২. প্রতিস্থাপন পদ্ধতি</h2>
<p><strong>(ক) প্রশ্ন ৭:</strong> <span class="math">2x + y = 6, x + 2y = 6</span></p>
<p>সমীকরণ (i) থেকে: <span class="math">y = 6 - 2x</span> ... (iii)</p>
<p>সমীকরণ (iii) এর মান (ii) এ: <span class="math">x + 2(6 - 2x) = 6</span></p>
<p><span class="math">x + 12 - 4x = 6 → -3x = -6 → x = 2</span></p>
<p><span class="math">y = 6 - 4 = 2</span></p>
<p><strong>∴ (x, y) = (2, 2)</strong></p>

<p><strong>(খ) প্রশ্ন ৯:</strong> <span class="math">5x - 2y = 3, 5x + 2y = 7</span></p>
<p>সমীকরণ (i) থেকে: <span class="math">5x = 3 + 2y</span> ... (iii)</p>
<p>সমীকরণ (iii) এর মান (ii) এ: <span class="math">3 + 2y + 2y = 7 → 4y = 4 → y = 1</span></p>
<p><span class="math">5x = 5 → x = 1</span></p>
<p><strong>∴ (x, y) = (1, 1)</strong></p>
</body>
</html>
"""


def main():
    workspace = Path("/workspace")
    html_q = workspace / "Class_Test_Chapter_6_1_v6.html"
    html_s = workspace / "Class_Test_Chapter_6_1_v6_Solutions.html"
    pdf_q = workspace / "Class_Test_Chapter_6_1_v6.pdf"
    pdf_s = workspace / "Class_Test_Chapter_6_1_v6_Solutions.pdf"

    html_q.write_text(HTML, encoding="utf-8")
    html_s.write_text(SOLUTIONS_HTML, encoding="utf-8")

    from weasyprint import HTML as WHTML

    WHTML(string=HTML, base_url=str(workspace)).write_pdf(str(pdf_q))
    WHTML(string=SOLUTIONS_HTML, base_url=str(workspace)).write_pdf(str(pdf_s))
    print("Created:", pdf_q, pdf_s)


if __name__ == "__main__":
    main()
