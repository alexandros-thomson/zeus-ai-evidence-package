#!/usr/bin/env python3
"""
NBG Heir Request Tracker — Protocol #462
Tracks the GDPR Art.15 + AK 1710-1724 request to National Bank of Greece
for account statements on AFM 051422558 (deceased Ioannis Kyprianos).

Sent: 05/04/2026
To: dpo@nbg.gr
CC: customer.service@nbg.gr, DetroitFieldOffice@ci.irs.gov
Basis: Heir certificate #5771/2021 + GDPR Art.15 + AK 1710-1724
10 business day deadline: ~19/04/2026
30 calendar day deadline: ~05/05/2026

If silent → ΑΠΔΠΧ Art.77 + ΤτΕ (Bank of Greece) + Εισαγγελία
"""

import json
from datetime import datetime, timedelta

# === CONFIGURATION ===
REQUEST = {
    "protocol": 462,
    "date_sent": "2026-04-05",
    "recipient": "dpo@nbg.gr",
    "cc": ["customer.service@nbg.gr", "DetroitFieldOffice@ci.irs.gov"],
    "subject": "GDPR Art.15 + Αρθ. 1710-1724 ΑΚ — Αίτημα αντιγράφων κίνησης λογαριασμών (ΑΦΜ 051422558)",
    "target_afm": "051422558",
    "target_name": "ΚΥΠΡΙΑΝΟΣ ΙΩΑΝΝΗΣ (deceased 13/06/2021)",
    "requester_afm": "044594747",
    "requester_name": "ΚΥΠΡΙΑΝΟΥ ΣΤΑΜΑΤΙΝΑ",
    "heir_certificate": "Πρωτοδικείο Πειραιά #5771/2021",
    "iban_requester": "GR0301104700000047074777757",
    "legal_basis": [
        "GDPR Art.15 (Right of Access)",
        "ΑΚ 1710-1724 (Heir rights over deceased's assets)",
        "Πρωτοδικείο Πειραιά #5771/2021 (Sole heir certificate)"
    ],
    "records_requested": [
        "All account statements AFM 051422558, 13/06/2021 to present",
        "All authorized signatories post-mortem",
        "All standing orders / direct debits",
        "Any pension deposits (ΕΦΚΑ/ΗΔΥΚΑ/ΓΛΚ)",
        "Any ENFIA / tax payments (AADE)",
        "Any Κτηματολόγιο / e-Paravolo payments (€35 trace)",
        "Any card transactions",
        "Account closure status"
    ],
    "fax_attempts": [
        {"number": "+30 210 647 5628", "time": "13:25", "status": "FAILED — Invalid destination"},
        {"number": "+30 210 334 7740", "time": "13:29 + 13:36", "status": "FAILED — No answer"},
        {"number": "+30 210 334 6510", "time": "13:34 + 13:35", "status": "FAILED — No answer"}
    ],
    "email_status": "DELIVERED"
}

# === DEADLINES ===
date_sent = datetime.strptime(REQUEST["date_sent"], "%Y-%m-%d")

# 10 business days (skip weekends)
business_days = 0
current = date_sent
while business_days < 10:
    current += timedelta(days=1)
    if current.weekday() < 5:  # Mon-Fri
        business_days += 1
deadline_10bd = current

# 30 calendar days (GDPR maximum)
deadline_30cd = date_sent + timedelta(days=30)

# IRS-CI meeting
irs_ci_meeting = datetime(2026, 4, 21)

DEADLINES = {
    "10_business_days": deadline_10bd.strftime("%Y-%m-%d"),
    "30_calendar_days": deadline_30cd.strftime("%Y-%m-%d"),
    "irs_ci_meeting": irs_ci_meeting.strftime("%Y-%m-%d"),
    "escalation_trigger": deadline_30cd.strftime("%Y-%m-%d")
}

# === ESCALATION CHAIN ===
ESCALATION = {
    "level_1": {
        "trigger": "10 business days silence",
        "date": DEADLINES["10_business_days"],
        "action": "Follow-up email to dpo@nbg.gr + customer.service@nbg.gr",
        "cc": "DetroitFieldOffice@ci.irs.gov"
    },
    "level_2": {
        "trigger": "IRS-CI meeting (regardless of NBG response)",
        "date": DEADLINES["irs_ci_meeting"],
        "action": "Present NBG request + silence status to SA Zacheranik",
        "note": "If NBG silent → supports MLAT A-7 ask for bank records"
    },
    "level_3": {
        "trigger": "30 calendar days silence",
        "date": DEADLINES["30_calendar_days"],
        "action": "ΑΠΔΠΧ Art.77 complaint against NBG (GDPR Art.15 violation)",
        "recipients": ["complaints@dpa.gr"]
    },
    "level_4": {
        "trigger": "Post-ΑΠΔΠΧ or concurrent",
        "action": "ΤτΕ (Bank of Greece) complaint — banking supervision",
        "recipients": ["dep.bankingsupervision@bankofgreece.gr"]
    },
    "level_5": {
        "trigger": "If NBG obstructs or destroys records",
        "action": "Εισαγγελία criminal referral — Art.259 ΠΚ (obstruction) + 18 USC §1519 (evidence destruction)",
        "recipients": ["protokollo@eispa.gr", "minisis@eispp.gr"]
    }
}

# === STATUS CHECK ===
def check_status():
    today = datetime.now()
    date_sent_dt = datetime.strptime(REQUEST["date_sent"], "%Y-%m-%d")
    days_elapsed = (today - date_sent_dt).days
    
    # Calculate business days elapsed
    bd_elapsed = 0
    current = date_sent_dt
    while current < today:
        current += timedelta(days=1)
        if current.weekday() < 5:
            bd_elapsed += 1
    
    deadline_10 = datetime.strptime(DEADLINES["10_business_days"], "%Y-%m-%d")
    deadline_30 = datetime.strptime(DEADLINES["30_calendar_days"], "%Y-%m-%d")
    irs_meeting = datetime.strptime(DEADLINES["irs_ci_meeting"], "%Y-%m-%d")
    
    print("=" * 60)
    print("NBG HEIR REQUEST TRACKER — Protocol #462")
    print("=" * 60)
    print(f"Date sent:          {REQUEST['date_sent']}")
    print(f"Days elapsed:       {days_elapsed} calendar / {bd_elapsed} business")
    print(f"Email status:       {REQUEST['email_status']}")
    print(f"Fax attempts:       3 FAILED (documented)")
    print()
    print("DEADLINES:")
    print(f"  10 business days: {DEADLINES['10_business_days']}", end="")
    if today > deadline_10:
        print(f"  ⚠️  EXPIRED ({(today - deadline_10).days} days ago)")
    else:
        print(f"  ({(deadline_10 - today).days} days remaining)")
    
    print(f"  IRS-CI meeting:   {DEADLINES['irs_ci_meeting']}", end="")
    if today > irs_meeting:
        print(f"  ✅ PAST")
    else:
        print(f"  ({(irs_meeting - today).days} days remaining)")
    
    print(f"  30 calendar days: {DEADLINES['30_calendar_days']}", end="")
    if today > deadline_30:
        print(f"  🔴 EXPIRED — File ΑΠΔΠΧ Art.77")
    else:
        print(f"  ({(deadline_30 - today).days} days remaining)")
    
    print()
    print("RESPONSE STATUS: ❌ NO RESPONSE RECEIVED")
    print()
    print("WHAT NBG'S RECORDS WOULD REVEAL:")
    for i, record in enumerate(REQUEST["records_requested"], 1):
        print(f"  {i}. {record}")
    
    print()
    print("ESCALATION CHAIN:")
    for level, info in ESCALATION.items():
        status = "⏳"
        if "date" in info:
            level_date = datetime.strptime(info["date"], "%Y-%m-%d")
            if today > level_date:
                status = "🔴 TRIGGERED"
            elif (level_date - today).days <= 3:
                status = "⚠️  IMMINENT"
        print(f"  {level}: {info['trigger']} — {status}")
        print(f"    Action: {info['action']}")
    
    print()
    print("=" * 60)
    print("FOR IRS-CI (April 21):")
    print("If NBG is silent by meeting date, this supports MLAT Ask A-7")
    print("for compelled production of AFM 051422558 bank records.")
    print("The €35 Κτηματολόγιο fee, pension deposits, and post-mortem")
    print("ENFIA payments are all in those records.")
    print("=" * 60)

if __name__ == "__main__":
    check_status()
