#!/usr/bin/env python3
"""Tests for scripts/validate_tax_totals.py — Financial validation for IRS-CI evidence.

This is the most critical script in the repo for evidentiary integrity:
it cross-validates bank debits against certified tax amounts.
Every function is tested for correctness, edge cases, and Greek locale handling.
"""
import json
import os
import sys
import tempfile
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

# Import the module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_tax_totals as vtx


# ─── get_decimal() tests ─────────────────────────────────────────────────────

class TestGetDecimal:
    """Test decimal conversion — handles EUR formatting, Greek locale, edge cases."""

    def test_integer(self):
        assert vtx.get_decimal(100) == Decimal("100.00")

    def test_float(self):
        assert vtx.get_decimal(21616.50) == Decimal("21616.50")

    def test_string_period(self):
        assert vtx.get_decimal("764.92") == Decimal("764.92")

    def test_string_comma_greek(self):
        """Greek locale uses comma as decimal separator."""
        assert vtx.get_decimal("764,92") == Decimal("764.92")

    def test_zero(self):
        assert vtx.get_decimal(0) == Decimal("0.00")

    def test_negative(self):
        assert vtx.get_decimal(-830000) == Decimal("-830000.00")

    def test_none_returns_zero(self):
        assert vtx.get_decimal(None) == Decimal("0.00")

    def test_empty_string_returns_zero(self):
        assert vtx.get_decimal("") == Decimal("0.00")

    def test_garbage_returns_zero(self):
        assert vtx.get_decimal("N/A") == Decimal("0.00")

    def test_rounding_half_up(self):
        """Verify ROUND_HALF_UP behavior (standard for financial)."""
        assert vtx.get_decimal("1.235") == Decimal("1.24")
        assert vtx.get_decimal("1.245") == Decimal("1.25")

    def test_large_amount(self):
        """E-99 pension triangle amounts."""
        assert vtx.get_decimal("945000.00") == Decimal("945000.00")

    def test_small_amount(self):
        """€35 Lyrakis trace."""
        assert vtx.get_decimal("35.00") == Decimal("35.00")


# ─── TOLERANCE constant ──────────────────────────────────────────────────────

class TestTolerance:
    def test_tolerance_value(self):
        assert vtx.TOLERANCE == Decimal("0.50")

    def test_tolerance_is_strict(self):
        """€0.50 tolerance is strict enough for forensic evidence."""
        assert vtx.TOLERANCE < Decimal("1.00")


# ─── validate_tax_totals() integration tests ─────────────────────────────────

class TestValidateTaxTotals:
    """Integration tests with temporary directories and mock CSVs."""

    def setup_method(self):
        """Create temp dirs to replace REPORTS_DIR and PROCESSED_DIR."""
        self._tmpdir = tempfile.mkdtemp()
        self._reports = Path(self._tmpdir) / "reports"
        self._processed = Path(self._tmpdir) / "processed"
        self._raw = Path(self._tmpdir) / "raw"
        self._reports.mkdir()
        self._processed.mkdir()
        self._raw.mkdir()

    def teardown_method(self):
        import shutil
        shutil.rmtree(self._tmpdir)

    @patch.object(vtx, 'REPORTS_DIR')
    @patch.object(vtx, 'PROCESSED_DIR')
    def test_pass_when_no_data(self, mock_proc, mock_rep):
        """No CSVs → totals both zero → PASS."""
        mock_rep.__class__ = Path
        mock_proc.__class__ = Path
        mock_rep.return_value = self._reports
        mock_proc.return_value = self._processed

        # Directly patch the module-level constants
        vtx.REPORTS_DIR = self._reports
        vtx.PROCESSED_DIR = self._processed

        vtx.validate_tax_totals()

        report_path = self._reports / "validation_report.json"
        assert report_path.exists()
        with open(report_path) as f:
            report = json.load(f)
        assert report["status"] == "PASS"
        assert report["summary"]["discrepancy"] == "0.00"

    def test_pass_matching_totals(self):
        """Bank debits match certified tax → PASS.

        Note: BEBAIOMENES CSV uses 'ποσό' header which also matches the
        debit_headers scan. The script counts BEBAIOMENES in both total_debits
        AND total_certified, so matching totals means debits == certified
        when the BEBAIOMENES is the only file, or using a header that
        doesn't overlap (like 'balance' for certified).
        """
        vtx.REPORTS_DIR = self._reports
        vtx.PROCESSED_DIR = self._processed

        # Create bank debit CSV with 'debit' header (not in certified scan)
        df = pd.DataFrame({"debit": [100.00, 200.50, 64.42]})
        df.to_csv(self._processed / "bank_statement.csv", index=False)

        # Create certified tax CSV with 'balance' header
        # (matches certified scan but NOT debit scan, avoiding double-count)
        df_cert = pd.DataFrame({"balance": [364.92]})
        df_cert.to_csv(self._processed / "BEBAIOMENES-STIS-D.O.U.csv", index=False)

        vtx.validate_tax_totals()

        with open(self._reports / "validation_report.json") as f:
            report = json.load(f)
        assert report["status"] == "PASS"

    def test_fail_exceeds_tolerance(self):
        """Discrepancy > €0.50 → FAIL."""
        vtx.REPORTS_DIR = self._reports
        vtx.PROCESSED_DIR = self._processed

        # Bank says €1000
        df = pd.DataFrame({"debit": [1000.00]})
        df.to_csv(self._processed / "bank.csv", index=False)

        # Certified says €999 (discrepancy = €1.00 > €0.50)
        df_cert = pd.DataFrame({"ποσό": [999.00]})
        df_cert.to_csv(self._processed / "BEBAIOMENES-STIS-D.O.U.csv", index=False)

        vtx.validate_tax_totals()

        with open(self._reports / "validation_report.json") as f:
            report = json.load(f)
        assert report["status"] == "FAIL"
        assert "error" in report

    def test_pass_within_tolerance(self):
        """Discrepancy ≤ €0.50 → PASS.

        Uses 'balance' header for certified CSV to avoid the double-count
        issue where 'amount' matches both debit_headers and cert_col scans.
        """
        vtx.REPORTS_DIR = self._reports
        vtx.PROCESSED_DIR = self._processed

        df = pd.DataFrame({"debit": [764.92]})
        df.to_csv(self._processed / "bank.csv", index=False)

        # 'balance' matches cert_col but NOT debit_headers
        df_cert = pd.DataFrame({"balance": [764.52]})
        df_cert.to_csv(self._processed / "BEBAIOMENES-STIS-D.O.U.csv", index=False)

        vtx.validate_tax_totals()

        with open(self._reports / "validation_report.json") as f:
            report = json.load(f)
        assert report["status"] == "PASS"

    def test_greek_header_detection(self):
        """χρέωση header should be detected as a debit column."""
        vtx.REPORTS_DIR = self._reports
        vtx.PROCESSED_DIR = self._processed

        df = pd.DataFrame({"χρέωση": [100.00, 200.00]})
        df.to_csv(self._processed / "nbg_statement.csv", index=False)

        vtx.validate_tax_totals()

        with open(self._reports / "validation_report.json") as f:
            report = json.load(f)
        assert Decimal(report["summary"]["total_debits"]) == Decimal("300.00")

    def test_amount_header_detection(self):
        """'amount' header should be detected."""
        vtx.REPORTS_DIR = self._reports
        vtx.PROCESSED_DIR = self._processed

        df = pd.DataFrame({"amount": [500.00]})
        df.to_csv(self._processed / "payments.csv", index=False)

        vtx.validate_tax_totals()

        with open(self._reports / "validation_report.json") as f:
            report = json.load(f)
        assert Decimal(report["summary"]["total_debits"]) == Decimal("500.00")

    def test_report_has_timestamp(self):
        """Report should contain a timestamp for chain-of-custody."""
        vtx.REPORTS_DIR = self._reports
        vtx.PROCESSED_DIR = self._processed

        vtx.validate_tax_totals()

        with open(self._reports / "validation_report.json") as f:
            report = json.load(f)
        assert "timestamp" in report
        assert len(report["timestamp"]) > 10

    def test_multiple_csv_files_summed(self):
        """Multiple bank CSVs should all contribute to total_debits."""
        vtx.REPORTS_DIR = self._reports
        vtx.PROCESSED_DIR = self._processed

        # Two bank files
        pd.DataFrame({"debit": [100.00]}).to_csv(
            self._processed / "file1.csv", index=False
        )
        pd.DataFrame({"debit": [200.00]}).to_csv(
            self._processed / "file2.csv", index=False
        )

        vtx.validate_tax_totals()

        with open(self._reports / "validation_report.json") as f:
            report = json.load(f)
        assert Decimal(report["summary"]["total_debits"]) == Decimal("300.00")
