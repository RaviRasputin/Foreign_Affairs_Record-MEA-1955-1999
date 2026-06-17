# Foreign Affairs Record (MEA) — Markdown Archive (1955–1999)

A plain-text archive of the **Foreign Affairs Record**, the monthly bulletin of India's **Ministry of External Affairs (MEA)**. The Record is the government's official compilation of foreign-policy material — statements, speeches, agreements, treaties, official visits, and parliamentary replies on external affairs. The MEA publishes it as yearly PDF compilations; this repository repackages each year as searchable **Markdown**, **one file per year**, for the period **1955–1999**.

Each year's file (`1955.md` … `1999.md`) is the full text of that year's Record.

| | |
|---|---|
| **Years covered** | 1955–1999 (45 years) |
| **Source volumes** | 45 yearly PDF compilations |
| **Total pages** | 28,363 |
| **Total Markdown** | ~54 MB |
| **Format** | UTF-8 Markdown, one file per year |

> Companion to the Lok Sabha and Rajya Sabha debate archives. Unlike those (which are large and shipped zipped), the Foreign Affairs Record files are small, so they are committed as plain `.md` you can read and search directly on GitHub.

---

## Repository layout

```
.
├── README.md            # this file
├── LICENSE              # licensing for the code in this repo
├── manifest.csv         # per-year stats: pages, source PDF size, markdown size
├── .gitignore
├── 1955.md              # one Markdown file per year …
├── 1956.md
├── ...
├── 1999.md
└── scripts/             # reference implementation of the build pipeline
    ├── 1_download_pdfs.py
    └── 2_extract_to_markdown.py
```

Per-year figures are in [`manifest.csv`](manifest.csv).

## Coverage by decade

| Decade | Years | Pages | Markdown |
|---|---:|---:|---:|
| 1950s | 5  | 3,098 | 6.8 MB  |
| 1960s | 10 | 7,871 | 15.2 MB |
| 1970s | 10 | 7,804 | 13.0 MB |
| 1980s | 10 | 5,783 | 11.9 MB |
| 1990s | 10 | 3,807 | 7.4 MB  |

The 1950s cover 1955–1959 (the Record begins in 1955). Page counts vary year to year with the volume of foreign-affairs activity.

---

## How this archive was built

The archive was produced by a short scripted pipeline: **download the yearly PDFs → extract their text to Markdown.** Reference implementations are in [`scripts/`](scripts/).

### 1. Downloading the source PDFs

The yearly Foreign Affairs Record compilations were **downloaded by a script** from the Ministry of External Affairs' public archive of the Record. Each file is one calendar year (the twelve monthly issues bound together) and is named for its year, e.g. `1955.pdf`. The download is idempotent — files already present are skipped — so a run can be resumed.

### 2. Extracting text to Markdown

The source PDFs carry an embedded **text layer**, so the text was extracted **directly** (with `pdftotext`) rather than re-OCR'd — this gives much cleaner output than image OCR. For each year the extracted text is written to a single `<year>.md` with:

- a top header — `# Foreign Affairs Record — <year>` — and a source line recording the original PDF, its page count, and the extraction date;
- the full text of the year's Record, with the PDF's page breaks preserved as blank lines.

```markdown
# Foreign Affairs Record — 1955

*Source: 1955.pdf — Foreign Affairs Record (monthly), Ministry of External Affairs,
Government of India. 412 pages. Text extracted from the PDF on 2026-06-17.*

---

<full text of the 1955 Record …>
```

Each file is plain UTF-8 Markdown, browsable and searchable directly on GitHub.

## Using the data

Search across all years with `ripgrep`:

```bash
rg -i "non-alignment" *.md
```

List every mention with its year:

```bash
rg -i --with-filename "Simla Agreement" *.md
```

The files work with any text editor, `grep`/`ripgrep`, pandas, or an LLM ingestion pipeline.

## Reproducing the pipeline

The scripts in [`scripts/`](scripts/) are a **reference implementation** of the download → extract pipeline. Adapt the source URLs to your environment before running.

```bash
pip install requests pypdf            # pdftotext comes from poppler-utils
python scripts/1_download_pdfs.py       --out pdfs/
python scripts/2_extract_to_markdown.py --in pdfs/ --out .
```

## Data quality & limitations

- **Extraction artifacts.** Text comes from the PDFs' own text layer; where that layer was produced by older OCR, occasional misrecognised characters, split words, or odd spacing remain. Treat the text as a research and search aid, not a certified transcript.
- **Layout loss.** Multi-column layouts, tables, and the printed contents/index pages are flattened into linear reading order.
- **Source completeness.** The archive contains the years available in the MEA source set (1955–1999); months missing from a source volume are missing here too.
- **Authoritative copy.** For citation, refer back to the original Foreign Affairs Record PDF for the relevant year.

## Source & attribution

The Foreign Affairs Record is published by the **Ministry of External Affairs, Government of India**. The material is an official government publication, reproduced here for research and public access. This repository only converts the PDFs to text; it does not alter their content.

## License

The Record **content** is a Government of India publication; rights in the original material rest with their respective owners. The **code** in this repository (the pipeline in `scripts/`) is released under the MIT License — see [`LICENSE`](LICENSE).
