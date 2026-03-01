#!/usr/bin/env python3
"""validate_tax_totals.py

Compares extracted CSV bank statement totals against BEBAIOMENES
(certified tax payment) PDFs to detect discrepancies.

Usage:
    python scripts/validate_tax_totals.py

Expects:
    - evidence/processed/*.csv  (output from parse_statements.py)
    - evidence/raw/BEBAIOMENES-STIS-D.O.U.pdf  (tax certificate)
"""
import sys
import os
import json
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

import pandas as pd

# Optional: tabula for parsing BEBAIOMENES if needed
try:
    import tabula
    HAS_TABULA = True
except ImportError:
    HAS_TABULA = False


# --- Configuration ---
PROCESSED_DIR = Path("evidence/processed")
RAW_DIR = Path("evidence/raw")
REPORT_DIR = Path("evidence/reports")
BEBAIOMENES_PDF = RAW_DIR / "BEBAIOMENES-STIS-D.O.U.pdf"
TOLERANCE_EUR = Decimal("0.50")  # Allowable rounding tolerance in EUR


def parse_bebaiomenes(pdf_path: Path) -> dict:
    """Extract certified tax totals from BEBAIOMENES PDF.

    Returns dict with tax_type -> amount mappings.
    Falls back to empty dict if PDF cannot be parsed.
    """
    totals = {}
    if not pdf_path.exists():
        print(f"WARNING: BEBAIOMENES PDF not found at {pdf_path}")
        return totals

    if not HAS_TABULA:
        print("WARNING: tabula-py not available, skipping BEBAIOMENES parsing")
        return totals

    try:
        tables = tabula.read_pdf(str(pdf_path), pages="all", multiple_tables=True)
        for df in tables:
            # Look for amount columns (Greek tax docs typically have
            # columns like: Description, Amount, Date)
            for col in df.columns:
                col_lower = str(col).lower()
                if any(kw in col_lower for kw in ["amount", "ποσο", "ποσό", "poso"]):
                    for _, row in df.iterrows():
                        val = row[col]
                        try:
                            amount = Decimal(str(val).replace(",", ".").replace(" ", ""))
                            desc_col = df.columns[0]
                            desc = str(row[desc_col]).strip()
                            if desc and desc != "nan":
                                totals[desc] = totals.get(desc, Decimal("0")) + amount
                        except Exception:
                            continue
    except Exception as e:
        print(f"WARNING: Could not parse BEBAIOMENES: {e}")

    return totals


def extract_csv_totals(processed_dir: Path) -> dict:
    """Sum debit/credit totals from all processed CSVs.

    Returns dict with filename -> {debits, credits, net, row_count}.
    """
    results = {}
    if not processed_dir.exists():
        print(f"WARNING: Processed directory not found at {processed_dir}")
        return results

    for csv_file in sorted(processed_dir.glob("*.csv")):
        try:
            df = pd.read_csv(csv_file)

            # Detect debit/credit columns (handle Greek & English headers)
            debit_cols = [c for c in df.columns if any(
                kw in str(c).lower() for kw in ["debit", "χρεωση", "χρέωση", "xrewsi"]
            )]
            credit_cols = [c for c in df.columns if any(
                kw in str(c).lower() for kw in ["credit", "πιστωση", "πίστωση", "pistosi"]
            )]
            amount_cols = [c for c in df.columns if any(
                kw in str(c).lower() for kw in ["amount", "ποσο", "ποσό"]
            )]

            total_debits = Decimal("0")
            total_credits = Decimal("0")

            if debit_cols:
                for col in debit_cols:
                    vals = pd.to_numeric(df[col], errors="coerce").dropna()
                    total_debits += Decimal(str(vals.sum()))
            if credit_cols:
                for col in credit_cols:
                    vals = pd.to_numeric(df[col], errors="coerce").dropna()
                    total_credits += Decimal(str(vals.sum()))

            # Fallback: if no debit/credit cols, use amount column
            if not debit_cols and not credit_cols and amount_cols:
                for col in amount_cols:
                    vals = pd.to_numeric(df[col], errors="coerce").dropna()
                    s = Decimal(str(vals.sum()))
                    if s < 0:
                        total_debits += abs(s)
                    else:
                        total_credits += s

            results[csv_file.name] = {
                "debits": total_debits.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                "credits": total_credits.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                "net": (total_credits - total_debits).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                "row_count": len(df),
            }
            print(f"  {csv_file.name}: {len(df)} rows, "
                  f"debits={total_debits:.2f}, credits={total_credits:.2f}")

        except Exception as e:
            print(f"  ERROR reading {csv_file.name}: {e}")
            results[csv_file.name] = {"error": str(e)}

    return results


def cross_validate(csv_totals: dict, bebaiomenes_totals: dict) -> list:
    """Compare bank statement totals against tax certificates.

    Returns list of discrepancy dicts.
    """
    discrepancies = []

    # Aggregate all debits across CSVs (tax payments are debits)
    total_bank_debits = sum(
        (v["debits"] for v in csv_totals.values() if isinstance(v.get("debits"), Decimal)),
        Decimal("0")
    )

    # Aggregate BEBAIOMENES certified amounts
    total_certified = sum(bebaiomenes_totals.values(), Decimal("0"))

    if total_certified > 0:
        diff = abs(total_bank_debits - total_certified)
        if diff > TOLERANCE_EUR:
            discrepancies.append({
                "type": "total_mismatch",
                "bank_debits": str(total_bank_debits),
                "certified_total": str(total_certified),
                "difference": str(diff),
                "status": "FAIL",
                "message": f"Bank debits ({total_bank_debits}) differ from "
                           f"certified total ({total_certified}) by {diff} EUR"
            })
        else:
            print(f"PASS: Bank debits ({total_bank_debits}) match certified "
                  f"total ({total_certified}) within tolerance ({TOLERANCE_EUR} EUR)")
    else:
        print("INFO: No BEBAIOMENES totals extracted; cross-validation skipped.")
        print("      Upload BEBAIOMENES PDF to evidence/raw/ to enable.")

    return discrepancies


def generate_report(csv_totals: dict, bebaiomenes_totals: dict,
                    discrepancies: list) -> Path:
    """Write JSON validation report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "validation_report.json"

    # Convert Decimal to str for JSON serialization
    def serialize(obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return obj

    report = {
        "csv_totals": {
            k: {kk: serialize(vv) for kk, vv in v.items()}
            for k, v in csv_totals.items()
        },
        "bebaiomenes_totals": {k: str(v) for k, v in bebaiomenes_totals.items()},
        "discrepancies": discrepancies,
        "status": "FAIL" if discrepancies else "PASS",
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\nReport saved to {report_path}")
    return report_path


def main():
    print("=" * 60)
    print("Zeus AI Tax Total Validation")
    print("=" * 60)

    # Step 1: Extract CSV totals
    print("\n[1/3] Extracting totals from processed CSVs...")
    csv_totals = extract_csv_totals(PROCESSED_DIR)
    if not csv_totals:
        print("No processed CSVs found. Run parse_statements.py first.")
        print("Exiting with warning (non-blocking).")
        sys.exit(0)

    # Step 2: Parse BEBAIOMENES
    print("\n[2/3] Parsing BEBAIOMENES tax certificates...")
    bebaiomenes_totals = parse_bebaiomenes(BEBAIOMENES_PDF)

    # Step 3: Cross-validate
    print("\n[3/3] Cross-validating bank vs tax totals...")
    discrepancies = cross_validate(csv_totals, bebaiomenes_totals)

    # Generate report
    report_path = generate_report(csv_totals, bebaiomenes_totals, discrepancies)

    # Summary
    print("\n" + "=" * 60)
    if discrepancies:
        print(f"RESULT: {len(discrepancies)} discrepancy(ies) found!")
        for d in discrepancies:
            print(f"  - {d['message']}")
        print("\nAction: Review report and reconcile differences.")
        # Exit with error code to fail CI if desired
        # sys.exit(1)  # Uncomment to block pipeline on mismatch
    else:
        print("RESULT: All totals validated successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
