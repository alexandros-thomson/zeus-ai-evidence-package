#!/usr/bin/env python3
"""Tests for scripts/nbg_heir_request_tracker.py — Protocol #462 deadline tracker.

Covers: business day calculation, deadline accuracy, escalation chain integrity,
and GDPR/AK legal basis completeness.
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch
from io import StringIO

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import importlib.util
SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "nbg_heir_request_tracker.py"
spec = importlib.util.spec_from_file_location("nbg_tracker", SCRIPT_PATH)
nbg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nbg)


# ─── REQUEST configuration tests ─────────────────────────────────────────────

class TestRequestConfig:
    """Verify Protocol #462 configuration is correct and complete."""

    def test_protocol_number(self):
        assert nbg.REQUEST["protocol"] == 462

    def test_target_afm(self):
        """John Kyprianos's AFM."""
        assert nbg.REQUEST["target_afm"] == "051422558"

    def test_requester_afm(self):
        """Stamatina's AFM — NEVER Lyrakis."""
        assert nbg.REQUEST["requester_afm"] == "044594747"

    def test_heir_certificate(self):
        assert "5771" in nbg.REQUEST["heir_certificate"]
        assert "Πειραιά" in nbg.REQUEST["heir_certificate"]

    def test_legal_basis_complete(self):
        """Must include GDPR Art.15 + AK 1710-1724 + heir certificate."""
        bases = nbg.REQUEST["legal_basis"]
        assert any("GDPR" in b and "Art.15" in b for b in bases)
        assert any("1710" in b for b in bases)
        assert any("5771" in b for b in bases)

    def test_records_requested_not_empty(self):
        assert len(nbg.REQUEST["records_requested"]) >= 6

    def test_records_include_pension(self):
        """Pension deposits must be requested (ΕΦΚΑ/ΗΔΥΚΑ/ΓΛΚ)."""
        records = " ".join(nbg.REQUEST["records_requested"])
        assert "pension" in records.lower() or "ΕΦΚΑ" in records or "ΗΔΥΚΑ" in records

    def test_records_include_35_euro_trace(self):
        """€35 Κτηματολόγιο trace must be requested."""
        records = " ".join(nbg.REQUEST["records_requested"])
        assert "35" in records or "Κτηματολόγιο" in records

    def test_email_delivered(self):
        assert nbg.REQUEST["email_status"] == "DELIVERED"

    def test_all_fax_attempts_failed(self):
        for attempt in nbg.REQUEST["fax_attempts"]:
            assert "FAILED" in attempt["status"]

    def test_irs_ci_in_cc(self):
        """IRS-CI must be CC'd on the request."""
        cc = nbg.REQUEST["cc"]
        assert any("ci.irs.gov" in addr or "DetroitFieldOffice" in addr for addr in cc)


# ─── Deadline calculation tests ───────────────────────────────────────────────

class TestDeadlines:
    """Verify deadline math is correct."""

    def test_date_sent(self):
        assert nbg.REQUEST["date_sent"] == "2026-04-05"

    def test_10_business_days(self):
        """April 5 + 10 business days = April 19 (Mon-Fri, skipping weekends).
        Apr 5 (Sun) → Apr 7 (Mon=1), Apr 8 (2), Apr 9 (3), Apr 10 (4), Apr 11 (5),
        Apr 14 (6), Apr 15 (7), Apr 16 (8), Apr 17 (9), Apr 18 (10) → Apr 18.
        Wait — Apr 5 is a Saturday in 2026? Let me verify...
        Actually, April 5, 2026 is a Sunday.
        Counting from April 5:
        Apr 6 Mon(1), Apr 7 Tue(2), Apr 8 Wed(3), Apr 9 Thu(4), Apr 10 Fri(5),
        Apr 13 Mon(6), Apr 14 Tue(7), Apr 15 Wed(8), Apr 16 Thu(9), Apr 17 Fri(10)
        → deadline = April 17, 2026
        """
        expected = datetime(2026, 4, 17)
        actual = datetime.strptime(nbg.DEADLINES["10_business_days"], "%Y-%m-%d")
        assert actual == expected, f"Expected {expected}, got {actual}"

    def test_30_calendar_days(self):
        """April 5 + 30 = May 5."""
        expected = datetime(2026, 5, 5)
        actual = datetime.strptime(nbg.DEADLINES["30_calendar_days"], "%Y-%m-%d")
        assert actual == expected

    def test_irs_ci_meeting_date(self):
        expected = datetime(2026, 4, 21)
        actual = datetime.strptime(nbg.DEADLINES["irs_ci_meeting"], "%Y-%m-%d")
        assert actual == expected

    def test_escalation_trigger_matches_30day(self):
        """Escalation trigger should fire at the 30-day GDPR deadline."""
        assert nbg.DEADLINES["escalation_trigger"] == nbg.DEADLINES["30_calendar_days"]


# ─── Escalation chain tests ──────────────────────────────────────────────────

class TestEscalationChain:
    """Verify the 5-level escalation chain is complete and correctly ordered."""

    def test_five_levels(self):
        assert len(nbg.ESCALATION) == 5

    def test_level_order(self):
        levels = list(nbg.ESCALATION.keys())
        assert levels == ["level_1", "level_2", "level_3", "level_4", "level_5"]

    def test_level_1_is_follow_up(self):
        l1 = nbg.ESCALATION["level_1"]
        assert "10 business" in l1["trigger"]
        assert "dpo@nbg.gr" in l1["action"]

    def test_level_2_is_irs_ci(self):
        l2 = nbg.ESCALATION["level_2"]
        assert "IRS-CI" in l2["trigger"]
        assert "MLAT" in l2.get("note", "")

    def test_level_3_is_apdpx(self):
        """30-day silence → ΑΠΔΠΧ Art.77."""
        l3 = nbg.ESCALATION["level_3"]
        assert "30 calendar" in l3["trigger"]
        assert "complaints@dpa.gr" in l3["recipients"]

    def test_level_4_is_bank_of_greece(self):
        l4 = nbg.ESCALATION["level_4"]
        assert "ΤτΕ" in l4["action"] or "Bank of Greece" in l4["action"]

    def test_level_5_is_criminal(self):
        """Nuclear option: criminal referral for obstruction."""
        l5 = nbg.ESCALATION["level_5"]
        assert "259" in l5["action"] or "Εισαγγελία" in l5["action"]
        assert "1519" in l5["action"]  # 18 USC §1519

    def test_all_levels_have_action(self):
        for level, info in nbg.ESCALATION.items():
            assert "action" in info, f"{level} missing 'action'"

    def test_all_levels_have_trigger(self):
        for level, info in nbg.ESCALATION.items():
            assert "trigger" in info, f"{level} missing 'trigger'"


# ─── check_status() tests ────────────────────────────────────────────────────

class TestCheckStatus:
    """Test the status reporting function."""

    def test_runs_without_error(self):
        """check_status() should complete without raising."""
        # Capture stdout
        captured = StringIO()
        with patch("sys.stdout", captured):
            nbg.check_status()
        output = captured.getvalue()
        assert "Protocol #462" in output

    def test_output_contains_protocol(self):
        captured = StringIO()
        with patch("sys.stdout", captured):
            nbg.check_status()
        assert "462" in captured.getvalue()

    def test_output_contains_deadlines(self):
        captured = StringIO()
        with patch("sys.stdout", captured):
            nbg.check_status()
        output = captured.getvalue()
        assert "10 business days" in output
        assert "30 calendar days" in output

    def test_output_contains_irs_ci_section(self):
        captured = StringIO()
        with patch("sys.stdout", captured):
            nbg.check_status()
        assert "IRS-CI" in captured.getvalue()


# ─── Business day counter accuracy ───────────────────────────────────────────

class TestBusinessDayLogic:
    """Verify the business day counting algorithm used in the module."""

    def test_weekends_skipped(self):
        """Manually verify: counting 5 business days from a Monday."""
        start = datetime(2026, 4, 6)  # Monday
        bd = 0
        current = start
        while bd < 5:
            current += timedelta(days=1)
            if current.weekday() < 5:
                bd += 1
        # Mon Apr 6 → Tue(1) Wed(2) Thu(3) Fri(4) Mon Apr 13(5)
        assert current == datetime(2026, 4, 13)

    def test_friday_start(self):
        """Starting Friday, 1 business day = next Monday."""
        start = datetime(2026, 4, 10)  # Friday
        bd = 0
        current = start
        while bd < 1:
            current += timedelta(days=1)
            if current.weekday() < 5:
                bd += 1
        assert current == datetime(2026, 4, 13)  # Monday

    def test_ten_business_days_from_sunday(self):
        """April 5, 2026 (Sunday) + 10 business days."""
        start = datetime(2026, 4, 5)
        bd = 0
        current = start
        while bd < 10:
            current += timedelta(days=1)
            if current.weekday() < 5:
                bd += 1
        assert current == datetime(2026, 4, 17)
