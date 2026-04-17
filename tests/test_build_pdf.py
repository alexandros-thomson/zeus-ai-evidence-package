#!/usr/bin/env python3
"""Tests for scripts/build-pdf.py — IRS-CI Evidence Binder PDF builder.

Covers: clean(), build_table(), md_to_paragraphs(), TAB_ORDER integrity,
and end-to-end PDF generation from markdown tabs.
"""
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add project root to path so we can import the script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

# Import functions under test
from importlib import import_module

# build-pdf has a hyphen, so we need importlib
import importlib.util

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "build-pdf.py"
spec = importlib.util.spec_from_file_location("build_pdf", SCRIPT_PATH)
build_pdf_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_pdf_mod)

clean = build_pdf_mod.clean
build_table = build_pdf_mod.build_table
md_to_paragraphs = build_pdf_mod.md_to_paragraphs
get_styles = build_pdf_mod.get_styles
build_pdf = build_pdf_mod.build_pdf
TAB_ORDER = build_pdf_mod.TAB_ORDER


# ─── clean() tests ───────────────────────────────────────────────────────────

class TestClean:
    """Test markdown-to-XML cleaning for ReportLab Paragraph objects."""

    def test_bold(self):
        assert "<b>test</b>" in clean("**test**")

    def test_italic(self):
        assert "<i>test</i>" in clean("*test*")

    def test_inline_code(self):
        result = clean("`code`")
        assert '<font face="Courier">code</font>' in result

    def test_link_stripped(self):
        result = clean("[click here](https://example.com)")
        assert "click here" in result
        assert "https://example.com" not in result

    def test_ampersand_escaped(self):
        result = clean("A & B")
        assert "&amp;" in result

    def test_angle_brackets_escaped(self):
        result = clean("a < b > c")
        assert "&lt;" in result
        assert "&gt;" in result

    def test_combined_formatting(self):
        result = clean("**bold** and *italic* with `code`")
        assert "<b>bold</b>" in result
        assert "<i>italic</i>" in result
        assert '<font face="Courier">code</font>' in result

    def test_empty_string(self):
        assert clean("") == ""

    def test_plain_text_passthrough(self):
        assert clean("no formatting here") == "no formatting here"

    def test_bold_does_not_eat_ampersand(self):
        """Ensure XML entity escaping doesn't break bold tags."""
        result = clean("**A & B**")
        assert "<b>A &amp; B</b>" in result

    def test_nested_bold_italic(self):
        """Bold wrapping italic: ***text*** or **bold *italic* here**."""
        result = clean("**bold *inner* end**")
        assert "<b>" in result
        assert "<i>inner</i>" in result


# ─── build_table() tests ─────────────────────────────────────────────────────

class TestBuildTable:
    """Test table construction from parsed rows."""

    @pytest.fixture
    def styles(self):
        return get_styles()

    def test_empty_rows(self, styles):
        from reportlab.platypus import Spacer
        result = build_table([], styles)
        assert isinstance(result, Spacer)

    def test_single_row(self, styles):
        from reportlab.platypus import LongTable
        result = build_table([["Header1", "Header2"]], styles)
        assert isinstance(result, LongTable)

    def test_uneven_rows_padded(self, styles):
        """Rows with different column counts should be padded."""
        from reportlab.platypus import LongTable
        rows = [["A", "B", "C"], ["D", "E"]]
        result = build_table(rows, styles)
        assert isinstance(result, LongTable)

    def test_all_empty_cells(self, styles):
        """Rows with all empty cells should be filtered."""
        from reportlab.platypus import Spacer
        result = build_table([[], []], styles)
        assert isinstance(result, Spacer)

    def test_numeric_cells(self, styles):
        """Numeric values should be str-converted without error."""
        from reportlab.platypus import LongTable
        rows = [["ID", "Amount"], [1, 21616.00]]
        result = build_table(rows, styles)
        assert isinstance(result, LongTable)


# ─── md_to_paragraphs() tests ────────────────────────────────────────────────

class TestMdToParagraphs:
    """Test markdown → flowable conversion."""

    @pytest.fixture
    def styles(self):
        return get_styles()

    def test_heading_h1(self, styles):
        result = md_to_paragraphs("# Title", styles)
        assert len(result) >= 1
        # First element should be a Paragraph
        from reportlab.platypus import Paragraph as P
        assert isinstance(result[0], P)

    def test_heading_h2(self, styles):
        result = md_to_paragraphs("## Section", styles)
        assert any(hasattr(f, 'text') for f in result)

    def test_bullet_list(self, styles):
        result = md_to_paragraphs("- item one\n- item two", styles)
        # Should produce 2 Paragraphs (bullets) + possible spacers
        from reportlab.platypus import Paragraph as P
        bullets = [f for f in result if isinstance(f, P)]
        assert len(bullets) == 2

    def test_checkbox(self, styles):
        result = md_to_paragraphs("- [x] done\n- [ ] todo", styles)
        from reportlab.platypus import Paragraph as P
        paragraphs = [f for f in result if isinstance(f, P)]
        assert len(paragraphs) == 2

    def test_blockquote(self, styles):
        result = md_to_paragraphs("> quoted text", styles)
        from reportlab.platypus import Paragraph as P
        assert any(isinstance(f, P) for f in result)

    def test_table_parsing(self, styles):
        md = "| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |"
        result = md_to_paragraphs(md, styles)
        from reportlab.platypus import LongTable
        tables = [f for f in result if isinstance(f, LongTable)]
        assert len(tables) == 1

    def test_table_separator_row_excluded(self, styles):
        """The |---|---| row should be skipped, not treated as data."""
        md = "| H1 | H2 |\n|---|---|\n| V1 | V2 |"
        result = md_to_paragraphs(md, styles)
        from reportlab.platypus import LongTable
        tables = [f for f in result if isinstance(f, LongTable)]
        assert len(tables) == 1

    def test_empty_input(self, styles):
        result = md_to_paragraphs("", styles)
        # Should produce at least spacers
        assert isinstance(result, list)

    def test_mixed_content(self, styles):
        """Headers, body, table, bullets in one document."""
        md = """# Title

Some body text.

| Col1 | Col2 |
|------|------|
| A    | B    |

- bullet 1
- bullet 2

> a blockquote
"""
        result = md_to_paragraphs(md, styles)
        assert len(result) > 5  # should produce multiple flowables


# ─── TAB_ORDER validation ────────────────────────────────────────────────────

class TestTabOrder:
    """Verify TAB_ORDER references real files and is in correct sequence."""

    def test_tab_order_not_empty(self):
        assert len(TAB_ORDER) > 0

    def test_tab1_is_first(self):
        assert TAB_ORDER[0] == "tab1-executive-summary.md"

    def test_all_tabs_are_markdown(self):
        for fname in TAB_ORDER:
            assert fname.endswith(".md"), f"{fname} is not a .md file"

    def test_tab_order_matches_repo(self):
        """Every file in TAB_ORDER should exist in irs-ci-package/tabs/."""
        tabs_dir = Path(__file__).resolve().parent.parent / "irs-ci-package" / "tabs"
        for fname in TAB_ORDER:
            assert (tabs_dir / fname).exists(), f"Missing tab: {fname}"

    def test_no_duplicates(self):
        assert len(TAB_ORDER) == len(set(TAB_ORDER))


# ─── End-to-end PDF generation ───────────────────────────────────────────────

class TestBuildPDF:
    """Integration test: build a PDF from the actual tabs directory."""

    def test_build_produces_file(self):
        tabs_dir = Path(__file__).resolve().parent.parent / "irs-ci-package" / "tabs"
        if not tabs_dir.exists():
            pytest.skip("irs-ci-package/tabs not found (not in repo checkout)")

        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "test-binder.pdf")
            build_pdf(str(tabs_dir), output, "test123")
            assert os.path.exists(output)
            assert os.path.getsize(output) > 1000  # should be at least 1KB

    def test_build_minimal_tabs(self):
        """Build from a directory with a single minimal .md file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tabs = os.path.join(tmpdir, "tabs")
            os.makedirs(tabs)
            # Create a minimal tab1
            with open(os.path.join(tabs, "tab1-executive-summary.md"), "w") as f:
                f.write("# Executive Summary\n\nThis is a test.\n\n| A | B |\n|---|---|\n| 1 | 2 |\n")

            output = os.path.join(tmpdir, "out.pdf")
            build_pdf(tabs, output, "abc1234")
            assert os.path.exists(output)
            assert os.path.getsize(output) > 500

    def test_build_empty_directory(self):
        """Building from an empty directory should still produce a PDF (cover only)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tabs = os.path.join(tmpdir, "empty_tabs")
            os.makedirs(tabs)
            output = os.path.join(tmpdir, "empty.pdf")
            build_pdf(tabs, output, "empty_test")
            assert os.path.exists(output)
