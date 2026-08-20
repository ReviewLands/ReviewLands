#!/usr/bin/env python3
"""Chapter 6.1 CLASS TEST — compact 2-column, dual copy on one A4."""
from pathlib import Path

COPY_BLOCK = """
<div class="copy-half">
  <h1>CLASS TEST</h1>
  <p class="sub">Mathematics</p>
  <p class="sub">Chapter 6.1 — Simultaneous Equations</p>
  <div class="meta">
    <span>Time: 45 minutes</span>
    <span>Full Marks: 30</span>
  </div>
  <div class="fields">Name: _________________________ &nbsp; Roll: __________ &nbsp; Date: __________</div>
  <p class="instr">নির্দেশনা: সব প্রশ্নের উত্তর দাও। প্রতিটি উপ-প্রশ্নের মান ৫। ভগ্নাংশ ব্যবহার করা যাবে না।</p>

  <div class="columns">
    <div class="section">
      <div class="section-head">
        <span>১. সৃজনশীল প্রশ্ন — অপনয়ন পদ্ধতি</span>
        <span class="en">15</span>
      </div>
      <div class="problem">
        <div class="problem-head"><span class="en">(ক)</span><span class="en">5</span></div>
        <div class="eqs">2x + y = 6<br>x + 2y = 6</div>
      </div>
      <div class="problem">
        <div class="problem-head"><span class="en">(খ)</span><span class="en">5</span></div>
        <div class="eqs">2x - y = 6<br>x - 2y = 6</div>
      </div>
      <div class="problem">
        <div class="problem-head"><span class="en">(গ)</span><span class="en">5</span></div>
        <div class="eqs">ax + by = ab<br>bx + ay = ab</div>
      </div>
    </div>

    <div class="section">
      <div class="section-head">
        <span>২. সৃজনশীল প্রশ্ন — প্রতিস্থাপন পদ্ধতি</span>
        <span class="en">15</span>
      </div>
      <div class="problem">
        <div class="problem-head"><span class="en">(ক)</span><span class="en">5</span></div>
        <div class="eqs">2x + y = 6<br>x + 2y = 6</div>
      </div>
      <div class="problem">
        <div class="problem-head"><span class="en">(খ)</span><span class="en">5</span></div>
        <div class="eqs">5x - 2y = 3<br>5x + 2y = 7</div>
      </div>
      <div class="problem">
        <div class="problem-head"><span class="en">(গ)</span><span class="en">5</span></div>
        <div class="eqs">ax - by = a - b<br>ax + by = a + b</div>
      </div>
    </div>
  </div>

  <p class="total en">Total: 6 x 5 = 30</p>
</div>
"""

HTML = f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;700&family=Times+New+Roman&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4; margin: 5mm 8mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Noto Sans Bengali', sans-serif; font-size: 9.5pt; color: #111; margin: 0; }}
  .en {{ font-family: 'Times New Roman', Times, serif; }}
  .sheet {{ width: 100%; }}

  .copy-half {{
    height: 138mm;
    max-height: 138mm;
    overflow: hidden;
    padding: 0 1mm;
  }}

  h1 {{
    font-family: 'Times New Roman', Times, serif;
    font-weight: bold;
    font-size: 14pt;
    text-align: center;
    margin: 0 0 1px;
    line-height: 1.1;
  }}
  .sub {{
    font-family: 'Times New Roman', Times, serif;
    text-align: center;
    margin: 0;
    font-size: 9.5pt;
    line-height: 1.25;
  }}
  .meta {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 9pt;
    display: flex;
    justify-content: space-between;
    margin: 5px 0 2px;
  }}
  .fields {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 9pt;
    margin-bottom: 3px;
  }}
  .instr {{
    font-size: 8.5pt;
    margin: 0 0 5px;
    line-height: 1.3;
  }}

  .columns {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6mm;
    align-items: start;
  }}
  .section-head {{
    font-weight: 700;
    font-size: 9.5pt;
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    line-height: 1.25;
  }}
  .problem {{ margin-bottom: 5px; }}
  .problem-head {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 9.5pt;
    display: flex;
    justify-content: space-between;
    margin-bottom: 1px;
  }}
  .eqs {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 9.5pt;
    margin-left: 10px;
    line-height: 1.35;
  }}
  .total {{
    font-size: 8.5pt;
    text-align: right;
    margin: 3px 0 0;
  }}

  .cut-zone {{
    border-top: 1px dashed #444;
    text-align: center;
    font-family: 'Times New Roman', Times, serif;
    font-size: 8pt;
    color: #444;
    padding: 1.5mm 0;
    margin: 1mm 0;
    line-height: 1;
  }}
</style>
</head>
<body>
<div class="sheet">
{COPY_BLOCK}
  <div class="cut-zone">— CUT HERE —</div>
{COPY_BLOCK}
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
  @page { size: A4; margin: 14mm; }
  body { font-family: 'Noto Sans Bengali', sans-serif; font-size: 10pt; line-height: 1.4; }
  .math { font-family: 'Times New Roman', Times, serif; }
  h1 { text-align: center; font-weight: 700; font-size: 14pt; }
  h2 { font-weight: 700; font-size: 11pt; margin-top: 14px; }
</style>
</head>
<body>
<h1>সমাধান (Answer Key)</h1>
<p class="math" style="text-align:center;">অনুশীলনী ৬.১ — প্রশ্ন ৭, ৮, ৯ | Full Marks: 30</p>

<h2>১. অপনয়ন পদ্ধতি</h2>
<p><strong>(ক)</strong> <span class="math">2x + y = 6, x + 2y = 6</span> → <strong>(2, 2)</strong></p>
<p><strong>(খ)</strong> <span class="math">2x - y = 6, x - 2y = 6</span> → <strong>(2, -2)</strong></p>
<p><strong>(গ)</strong> <span class="math">ax + by = ab, bx + ay = ab</span></p>
<p>(i)+(ii): <span class="math">(a+b)(x+y)=2ab</span>; (i)−(ii): <span class="math">(a-b)(x-y)=0 → x=y</span> (a≠b)</p>
<p><strong>∴ (x, y) = (ab/(a+b), ab/(a+b))</strong></p>

<h2>২. প্রতিস্থাপন পদ্ধতি</h2>
<p><strong>(ক)</strong> <span class="math">2x + y = 6, x + 2y = 6</span> → <strong>(2, 2)</strong></p>
<p><strong>(খ)</strong> <span class="math">5x - 2y = 3, 5x + 2y = 7</span> → <strong>(1, 1)</strong></p>
<p><strong>(গ)</strong> <span class="math">ax - by = a - b, ax + by = a + b</span> → <strong>(1, 1)</strong></p>
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
