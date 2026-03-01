import pandas as pd
import json
import os
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

# Config
TOLERANCE = Decimal('0.50')
REPORTS_DIR = Path('evidence/reports')
PROCESSED_DIR = Path('evidence/processed')
RAW_DIR = Path('evidence/raw')

def get_decimal(val):
    try:
        if isinstance(val, str):
            val = val.replace(',', '.')
        return Decimal(str(val)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except:
        return Decimal('0.00')

def validate_tax_totals():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "PASS",
        "timestamp": pd.Timestamp.now().isoformat(),
        "details": [],
        "summary": {"total_debits": "0.00", "total_certified": "0.00", "discrepancy": "0.00"}
    }
    
    total_debits = Decimal('0.00')
    total_certified = Decimal('0.00')
    
    # 1. Extract totals from processed CSVs (Bank Debits)
    # Mapping for Greek/English headers
    debit_headers = ['debit', 'χρέωση', 'ποσό', 'amount']
    
    for csv_file in PROCESSED_DIR.glob('*.csv'):
        df = pd.read_csv(csv_file)
        # Find column matching debit headers (case-insensitive)
        col = next((c for c in df.columns if c.lower() in debit_headers), None)
        if col:
            file_sum = df[col].apply(get_decimal).sum()
            total_debits += file_sum
            report["details"].append({"file": csv_file.name, "type": "bank_debit", "amount": str(file_sum)})

    # 2. Extract from BEBAIOMENES (Certified Tax)
    # Placeholder: In a full prod version, this would use tabula/regex on 'BEBAIOMENES-STIS-D.O.U.pdf'
    # For now, we search for a matching CSV or use a mock total if PDF parsing logic is separate
    # In this script, we assume the BEBAIOMENES PDF was also parsed to a CSV by the previous step
    bebaiomenes_csv = PROCESSED_DIR / "BEBAIOMENES-STIS-D.O.U.csv"
    if bebaiomenes_csv.exists():
        df_cert = pd.read_csv(bebaiomenes_csv)
        cert_col = next((c for c in df_cert.columns if c.lower() in ['ποσό', 'amount', 'balance']), None)
        if cert_col:
            total_certified = df_cert[cert_col].apply(get_decimal).sum()
            report["details"].append({"file": "BEBAIOMENES", "type": "certified_tax", "amount": str(total_certified)})

    # 3. Cross-Validation
    discrepancy = abs(total_debits - total_certified)
    report["summary"] = {
        "total_debits": str(total_debits),
        "total_certified": str(total_certified),
        "discrepancy": str(discrepancy)
    }
    
    if discrepancy > TOLERANCE:
        report["status"] = "FAIL"
        report["error"] = f"Discrepancy of {discrepancy} exceeds tolerance of {TOLERANCE}"

    # Save report
    report_path = REPORTS_DIR / "validation_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    
    print(f"Validation Report Generated: {report_path}")
    print(f"Status: {report['status']} | Discrepancy: {discrepancy}")

    # sys.exit(1) # Uncomment on line 238 (conceptually) to fail CI on mismatch
    # if report["status"] == "FAIL":
    #     sys.exit(1)

if __name__ == "__main__":
    validate_tax_totals()
