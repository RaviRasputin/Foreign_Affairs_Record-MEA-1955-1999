#!/usr/bin/env python3
"""
Stage 1 — Download the Foreign Affairs Record yearly PDFs.

Reference implementation of the bulk download step. It fetches the Ministry of
External Affairs' yearly Foreign Affairs Record compilations and saves them as
``<year>.pdf`` (e.g. ``1955.pdf``). The run is idempotent: files already present
(non-zero size) are skipped, so an interrupted download can be resumed.

NOTE: plug the MEA archive listing into ``iter_pdf_urls()``.

    python scripts/1_download_pdfs.py --out pdfs/
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Iterator

import requests

USER_AGENT = "far-mea-archiver/1.0 (+research; contact: you@example.com)"
REQUEST_TIMEOUT = 60
RETRIES = 3
PAUSE_SECONDS = 1.0


def iter_pdf_urls() -> Iterator[tuple[str, str]]:
    """Yield ``(filename, url)`` pairs, one per year, e.g.
    ``('1955.pdf', 'https://.../1955.pdf')``.

    Replace the body with the enumeration for your source (the MEA Foreign
    Affairs Record archive). Filenames should be ``<year>.pdf`` so stage 2 can
    map each file to its year.
    """
    raise NotImplementedError(
        "Provide the MEA Foreign Affairs Record listing here as (filename, url) tuples."
    )


def download_one(url: str, dest: Path, session: requests.Session) -> bool:
    for attempt in range(1, RETRIES + 1):
        try:
            with session.get(url, stream=True, timeout=REQUEST_TIMEOUT) as r:
                r.raise_for_status()
                tmp = dest.with_suffix(dest.suffix + ".part")
                with open(tmp, "wb") as fh:
                    for chunk in r.iter_content(chunk_size=1 << 16):
                        fh.write(chunk)
                tmp.replace(dest)
            return True
        except Exception as exc:  # noqa: BLE001 - reference script
            print(f"  attempt {attempt}/{RETRIES} failed for {url}: {exc}")
            time.sleep(2 * attempt)
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description="Download Foreign Affairs Record PDFs.")
    ap.add_argument("--out", type=Path, default=Path("pdfs"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    ok = skipped = failed = 0
    for filename, url in iter_pdf_urls():
        dest = args.out / filename
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            continue
        print(f"downloading {filename}")
        ok += 1 if download_one(url, dest, session) else 0
        failed += 0 if dest.exists() else 1
        time.sleep(PAUSE_SECONDS)

    print(f"\nDone. downloaded={ok} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()
