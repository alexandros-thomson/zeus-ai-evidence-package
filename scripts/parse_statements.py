import tabula
import pandas as pd
from pathlib import Path

def parse_bank_statements():
    raw_dir = Path('evidence/raw')
    processed_dir = Path('evidence/processed')
    processed_dir.mkdir(parents=True, exist_ok=True)

    print(f"Scanning {raw_dir} for PDFs...")
    
    for pdf in raw_dir.glob('*.pdf'):
        try:
            print(f"Parsing {pdf.name}...")
            # multiple_tables=True handles complex bank layouts better
            tables = tabula.read_pdf(str(pdf), pages='all', multiple_tables=True)
            if not tables:
                print(f"No tables found in {pdf.name}")
                continue
                
            df = pd.concat(tables, ignore_index=True)
            
            # Basic cleaning (can be refined per NBG layout)
            # Standard NBG columns often include: Date, Description, Debit, Credit, Balance
            csv_out = processed_dir / f"{pdf.stem}.csv"
            df.to_csv(csv_out, index=False)
            print(f"Successfully saved to {csv_out}")
        except Exception as e:
            print(f"Error parsing {pdf.name}: {e}")

if __name__ == "__main__":
    parse_bank_statements()
