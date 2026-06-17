#!/usr/bin/env python3
"""
Stage 2 — Extract each yearly PDF to a Markdown file.

The Foreign Affairs Record PDFs carry an embedded text layer, so text is
extracted directly with ``pdftotext`` (from poppler-utils) — no image OCR. Each
``<year>.pdf`` becomes a ``<year>.md`` with a header and the full text, page
breaks preserved as blank lines.

Output format (matches the files shipped in this repository):

    # Foreign Affairs Record — <year>

    *Source: <year>.pdf — Foreign Affairs Record (monthly), Ministry of External
    Affairs, Government of India. <pages> pages. Text extracted from the PDF on <date>.*

    ---

    <full text>

    python scripts/2_extract_to_markdown.py --in pdfs/ --out .

Requires: poppler-utils (`pdftotext`, `pdfinfo`); optional `pypdf` as a fallback.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
from pathlib import Path

YEAR_RE = re.compile(r"(\d{4})")


def page_count(pdf: Path) -> str:
    try:
        out = subprocess.run(
            ["pdfinfo", str(pdf)], capture_output=True, text=True, check=True
        ).stdout
        for line in out.splitlines():
            if line.startswith("Pages"):
                return line.split()[1]
    except Exception:
        pass
    return "?"


def extract_text(pdf: Path) -> str:
    """Extract text via pdftotext; fall back to pypdf if pdftotext is absent."""
    try:
        out = subprocess.run(
            ["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True
        ).stdout
        return out.replace("\f", "\n")  # page breaks -> blank lines
    except FileNotFoundError:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf))
        return "\n\n".join((p.extract_text() or "") for p in reader.pages)


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract yearly PDFs to Markdown.")
    ap.add_argument("--in", dest="src", type=Path, default=Path("pdfs"))
    ap.add_argument("--out", dest="dst", type=Path, default=Path("."))
    args = ap.parse_args()
    args.dst.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()

    for pdf in sorted(args.src.glob("*.pdf")):
        m = YEAR_RE.search(pdf.stem)
        if not m:
            print(f"  ! no year in {pdf.name} — skipping")
            continue
        year = m.group(1)
        pages = page_count(pdf)
        print(f"  {year}: {pages} pages")
        body = extract_text(pdf)
        text = (
            f"# Foreign Affairs Record — {year}\n\n"
            f"*Source: {pdf.name} — Foreign Affairs Record (monthly), Ministry of "
            f"External Affairs, Government of India. {pages} pages. "
            f"Text extracted from the PDF on {today}.*\n\n---\n\n{body}"
        )
        (args.dst / f"{year}.md").write_text(text, encoding="utf-8")

    print(f"\nDone. Markdown written to {args.dst}/")


if __name__ == "__main__":
    main()
