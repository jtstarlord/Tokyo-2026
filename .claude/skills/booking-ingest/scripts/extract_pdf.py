#!/usr/bin/env python3
"""Extract all text from a booking-confirmation PDF (typically a Gmail print-to-PDF).

Usage: python3 extract_pdf.py "<path.pdf>" [--pages N-M]
Prints every page; the booking payload is usually on page 2-3 past the Gmail headers.
"""
import sys

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    r = PdfReader(path)
    print(f"--- {len(r.pages)} pages ---")
    for i, p in enumerate(r.pages, start=1):
        t = (p.extract_text() or "").strip()
        if not t:
            continue
        print(f"=== PAGE {i} ===")
        print(t)

if __name__ == "__main__":
    main()
