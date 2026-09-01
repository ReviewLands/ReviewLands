#!/usr/bin/env python3
"""Generate MCQ SSC Math exam page (landscape fold layout)."""

from generate_ssc_math_exam_pdf import build_mcq

if __name__ == "__main__":
    out = "/workspace/SSC_Math_MCQ_Test.pdf"
    build_mcq(out)
    print(f"Created: {out}")
