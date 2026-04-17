#!/usr/bin/env python3
"""Tests for scripts/parse_statements.py — Bank statement PDF/XLSX parser.

Covers: decrypt_pdf(), parse_xlsx(), parse_with_pdfplumber(),
header detection, and the main parse_bank_statements() flow.
"""
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import parse_statements as ps


# ─── decrypt_pdf() tests ─────────────────────────────────────────────────────

class TestDecryptPdf:
    """Test PDF decryption logic."""

    def test_returns_original_if_no_pikepdf(self):
        """Without pikepdf, should return the original path."""
        original = ps.HAS_PIKEPDF
        try:
            ps.HAS_PIKEPDF = False
            dummy = Path("/tmp/dummy.pdf")
            assert ps.decrypt_pdf(dummy) == dummy
        finally:
            ps.HAS_PIKEPDF = original

    def test_returns_original_on_error(self):
        """If decryption fails, should return original path."""
        if not ps.HAS_PIKEPDF:
            pytest.skip("pikepdf not installed")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"not a real pdf")
            tmp = Path(f.name)
        try:
            result = ps.decrypt_pdf(tmp)
            assert result == tmp  # should fall back to original
        finally:
            tmp.unlink(missing_ok=True)


# ─── parse_xlsx() tests ──────────────────────────────────────────────────────

class TestParseXlsx:
    """Test Excel file parsing."""

    def test_single_sheet(self):
        """Parse a simple single-sheet Excel file."""
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            tmp = Path(f.name)
        try:
            df = pd.DataFrame({
                "date": ["2021-06-14", "2021-06-15"],
                "description": ["ΕΝΦΙΑ 2021", "DEH Payment"],
                "debit": [764.92, 49.00],
            })
            df.to_excel(str(tmp), index=False, engine="openpyxl")

            result = ps.parse_xlsx(tmp)
            assert not result.empty
            assert len(result) == 2
            assert "debit" in result.columns
        finally:
            tmp.unlink(missing_ok=True)

    def test_multi_sheet(self):
        """Parse Excel with multiple sheets."""
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            tmp = Path(f.name)
        try:
            with pd.ExcelWriter(str(tmp), engine="openpyxl") as writer:
                pd.DataFrame({"a": [1, 2]}).to_excel(writer, sheet_name="Sheet1", index=False)
                pd.DataFrame({"b": [3, 4]}).to_excel(writer, sheet_name="Sheet2", index=False)

            result = ps.parse_xlsx(tmp)
            assert not result.empty
            assert "_sheet" in result.columns
            assert len(result) == 4  # 2 rows from each sheet
        finally:
            tmp.unlink(missing_ok=True)

    def test_empty_xlsx(self):
        """Empty Excel file should return empty DataFrame."""
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            tmp = Path(f.name)
        try:
            pd.DataFrame().to_excel(str(tmp), index=False, engine="openpyxl")
            result = ps.parse_xlsx(tmp)
            assert result.empty
        finally:
            tmp.unlink(missing_ok=True)

    def test_corrupt_file_returns_empty(self):
        """Corrupt file should return empty DataFrame, not crash."""
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            f.write(b"not an xlsx file at all")
            tmp = Path(f.name)
        try:
            result = ps.parse_xlsx(tmp)
            assert result.empty
        finally:
            tmp.unlink(missing_ok=True)


# ─── Header detection tests ──────────────────────────────────────────────────

class TestHeaderDetection:
    """Test that Greek and English headers are properly detected."""

    def test_greek_keywords_recognized(self):
        """Greek bank statement headers should be in the detection list."""
        keywords = ['ημερομηνια', 'περιγραφη', 'χρεωση', 'πιστωση', 'υπολοιπο']
        expected = ps.parse_with_pdfplumber.__doc__ or ""
        # Check the actual keyword list in the function
        # We test indirectly through the module
        assert 'ημερομηνια' in str(ps.parse_with_pdfplumber.__code__.co_consts)

    def test_english_keywords_recognized(self):
        """English headers should also be detected."""
        assert 'date' in str(ps.parse_with_pdfplumber.__code__.co_consts)
        assert 'debit' in str(ps.parse_with_pdfplumber.__code__.co_consts)


# ─── parse_bank_statements() integration ─────────────────────────────────────

class TestParseBankStatements:
    """Integration test with temp directories."""

    def setup_method(self):
        self._tmpdir = tempfile.mkdtemp()
        self._raw = Path(self._tmpdir) / "raw"
        self._processed = Path(self._tmpdir) / "processed"
        self._raw.mkdir()

    def teardown_method(self):
        import shutil
        shutil.rmtree(self._tmpdir)

    def test_xlsx_produces_csv(self):
        """An XLSX in raw/ should produce a CSV in processed/."""
        ps.RAW_DIR = self._raw
        ps.PROCESSED_DIR = self._processed

        df = pd.DataFrame({
            "Date": ["2021-06-14"],
            "Description": ["Post-mortem ΕΝΦΙΑ"],
            "Debit": [764.92],
        })
        df.to_excel(str(self._raw / "test_statement.xlsx"), index=False, engine="openpyxl")

        ps.parse_bank_statements()

        assert self._processed.exists()
        csvs = list(self._processed.glob("*.csv"))
        assert len(csvs) == 1
        result = pd.read_csv(csvs[0])
        assert len(result) == 1

    def test_empty_raw_no_crash(self):
        """Empty raw directory should complete without error."""
        ps.RAW_DIR = self._raw
        ps.PROCESSED_DIR = self._processed
        ps.parse_bank_statements()  # Should not raise

    def test_decrypted_temp_files_skipped(self):
        """Files starting with _decrypted_ should be skipped."""
        ps.RAW_DIR = self._raw
        ps.PROCESSED_DIR = self._processed

        # Create a fake decrypted temp file
        (self._raw / "_decrypted_something.pdf").write_bytes(b"fake pdf")

        ps.parse_bank_statements()
        # Should not produce a CSV for the _decrypted_ file
        csvs = list(self._processed.glob("*.csv"))
        assert len(csvs) == 0


# ─── Module-level constants ──────────────────────────────────────────────────

class TestModuleConstants:
    """Verify module configuration."""

    def test_has_pdfplumber_flag(self):
        assert isinstance(ps.HAS_PDFPLUMBER, bool)

    def test_has_tabula_flag(self):
        assert isinstance(ps.HAS_TABULA, bool)

    def test_has_pikepdf_flag(self):
        assert isinstance(ps.HAS_PIKEPDF, bool)

    def test_raw_dir_is_path(self):
        assert isinstance(ps.RAW_DIR, Path)

    def test_processed_dir_is_path(self):
        assert isinstance(ps.PROCESSED_DIR, Path)
