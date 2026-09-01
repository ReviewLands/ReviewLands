#!/usr/bin/env python3
"""Generate creative SSC Math exam page (landscape fold layout)."""

from generate_ssc_math_exam_pdf import build_creative

if __name__ == "__main__":
    out = "/workspace/SSC_Math_Special_Assignment.pdf"
    build_creative(out)
    print(f"Created: {out}")
