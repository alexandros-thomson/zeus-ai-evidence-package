#!/usr/bin/env python3
"""parse_statements.py

Extract tables from bank statement PDFs and XLSX files.
Uses pdfplumber (primary) with tabula-py fallback.
Handles encrypted/protected NBG PDFs via pikepdf.
"""
import sys
from pathlib import Path

import pandas as pd

# Optional imports with graceful fallback
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import tabula
    HAS_TABULA = True
except ImportError:
    HAS_TABULA = False

try:
    import pikepdf
    HAS_PIKEPDF = True
except ImportError:
    HAS_PIKEPDF = False


RAW_DIR = Path('evidence/raw')
PROCESSED_DIR = Path('evidence/processed')


def decrypt_pdf(pdf_path: Path) -> Path:
    """Attempt to remove PDF encryption/restrictions using pikepdf.
    Returns path to decrypted file (or original if not encrypted).
    """
    if not HAS_PIKEPDF:
        return pdf_path
    try:
        pdf = pikepdf.open(str(pdf_path), password='')
        decrypted = pdf_path.parent / f"_decrypted_{pdf_path.name}"
        pdf.save(str(decrypted))
        pdf.close()
        print(f"  Decrypted: {pdf_path.name}")
        return decrypted
    except Exception:
        return pdf_path


def parse_with_pdfplumber(pdf_path: Path) -> pd.DataFrame:
    """Extract tables using pdfplumber (handles complex layouts)."""
    all_rows = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if table and len(table) > 0:
                        # First row as header if it looks like one
                        header = table[0]
                        rows = table[1:]
                        for row in rows:
                            if row and any(cell for cell in row if cell):
                                all_rows.append(row)
                # Use first table's header
                if table and len(table[0]) > 0 and not all_rows:
                    continue
            else:
                # Try extracting text lines as fallback
                text = page.extract_text()
                if text:
                    for line in text.strip().split('\n'):
                        parts = line.split()
                        if len(parts) >= 3:
                            all_rows.append(parts)

    if not all_rows:
        return pd.DataFrame()

    # Try to build DataFrame with detected headers
    # NBG statements typically have: Date, Description, Debit, Credit, Balance
    max_cols = max(len(r) for r in all_rows)
    # Pad rows to same length
    padded = [r + [None] * (max_cols - len(r)) for r in all_rows]
    df = pd.DataFrame(padded)

    # Auto-detect header row (contains keywords)
    header_keywords = ['date', 'description', 'debit', 'credit', 'balance',
                       'ημερομηνια', 'περιγραφη', 'χρεωση', 'πιστωση', 'υπολοιπο']
    for idx, row in df.head(5).iterrows():
        row_text = ' '.join(str(v).lower() for v in row if v)
        if any(kw in row_text for kw in header_keywords):
            df.columns = [str(v).strip() if v else f'col_{i}' for i, v in enumerate(row)]
            df = df.iloc[idx + 1:].reset_index(drop=True)
            break

    return df


def parse_with_tabula(pdf_path: Path) -> pd.DataFrame:
    """Extract tables using tabula-py (Java-based, good for structured tables)."""
    tables = tabula.read_pdf(str(pdf_path), pages='all', multiple_tables=True)
    if not tables:
        return pd.DataFrame()
    return pd.concat(tables, ignore_index=True)


def parse_xlsx(xlsx_path: Path) -> pd.DataFrame:
    """Parse Excel files directly."""
    try:
        # Try reading all sheets
        sheets = pd.read_excel(str(xlsx_path), sheet_name=None, engine='openpyxl')
        frames = []
        for name, df in sheets.items():
            if not df.empty:
                df['_sheet'] = name
                frames.append(df)
        if frames:
            return pd.concat(frames, ignore_index=True)
    except Exception as e:
        print(f"  openpyxl failed, trying xlrd: {e}")
        try:
            return pd.read_excel(str(xlsx_path), engine='xlrd')
        except Exception as e2:
            print(f"  xlrd also failed: {e2}")
    return pd.DataFrame()


def parse_bank_statements():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Scanning {RAW_DIR} for files...")
    parsed_count = 0
    error_count = 0

    # Process XLSX files
    for xlsx in sorted(RAW_DIR.glob('*.xlsx')):
        print(f"Parsing {xlsx.name}...")
        try:
            df = parse_xlsx(xlsx)
            if not df.empty:
                csv_out = PROCESSED_DIR / f"{xlsx.stem}.csv"
                df.to_csv(csv_out, index=False)
                print(f"  Saved {csv_out} ({len(df)} rows)")
                parsed_count += 1
            else:
                print(f"  No data extracted from {xlsx.name}")
        except Exception as e:
            print(f"  Error parsing {xlsx.name}: {e}")
            error_count += 1

    # Process PDF files
    for pdf in sorted(RAW_DIR.glob('*.pdf')):
        # Skip decrypted temp files
        if pdf.name.startswith('_decrypted_'):
            continue
        print(f"Parsing {pdf.name}...")
        try:
            # Step 1: Try decrypting if protected
            work_pdf = decrypt_pdf(pdf)

            # Step 2: Try pdfplumber first
            df = pd.DataFrame()
            if HAS_PDFPLUMBER:
                try:
                    df = parse_with_pdfplumber(work_pdf)
                    if not df.empty:
                        print(f"  pdfplumber extracted {len(df)} rows")
                except Exception as e:
                    print(f"  pdfplumber failed: {e}")

            # Step 3: Fall back to tabula
            if df.empty and HAS_TABULA:
                try:
                    df = parse_with_tabula(work_pdf)
                    if not df.empty:
                        print(f"  tabula extracted {len(df)} rows")
                except Exception as e:
                    print(f"  tabula failed: {e}")

            # Step 4: Save result
            if not df.empty:
                csv_out = PROCESSED_DIR / f"{pdf.stem}.csv"
                df.to_csv(csv_out, index=False)
                print(f"  Saved {csv_out}")
                parsed_count += 1
            else:
                print(f"  WARNING: No tables extracted from {pdf.name}")
                print(f"    - PDF may be image-based (needs OCR)")
                print(f"    - Or has non-standard table layout")
                error_count += 1

            # Clean up decrypted temp file
            if work_pdf != pdf and work_pdf.exists():
                work_pdf.unlink()

        except Exception as e:
            print(f"  Error parsing {pdf.name}: {e}")
            error_count += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"Parsing complete: {parsed_count} files parsed, {error_count} errors")
    total_csvs = list(PROCESSED_DIR.glob('*.csv'))
    print(f"CSVs in {PROCESSED_DIR}: {len(total_csvs)}")
    for csv in total_csvs:
        print(f"  - {csv.name}")
    print(f"{'='*50}")


if __name__ == '__main__':
    parse_bank_statements()
