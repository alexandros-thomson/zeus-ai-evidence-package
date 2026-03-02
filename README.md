# Zeus AI Evidence Package 🧠⚖️🚀

Central GitHub repository integrating all tax/legal evidence for Stamatina/John Kyprianos across US-Greece jurisdictions. Powered by Zeus AI for automation, DevOps workflows, CI/CD, and compliance tracking.

## 📋 Key Documents

### Bank Statements
- NBG statements 2021-2025 (shared accounts)
- John/Stamatina tax payment records
- Latest export: `statementexport01-03-2026.xlsx`

### Tax Documents
- ENFIA notices & payments (2020-2025)
- Βεβαιωμένες Στις Δ.Ο.Υ. certificates
- Εκκαθαριστικά (2022-2024)
- AADE tax proofs (`01_2021-01_2026AADE.pdf`)

### Protocol Tracker
- **MASTER-PROTOCOL-TRACKER.csv** - Live tracker with 246 protocols across 30+ agencies
- **DEADLINE-DIGEST.md** - Snapshot of critical deadlines and session outcomes
- Real-time sync with Notion [Deadline Digest](https://www.notion.so/30ffe5f31cb881db96bcda4e7254bc2e)

## 🤖 Zeus AI Integration

### Automation Pipeline
- Zapier/n8n automations for portal monitoring
- Evidence ingestion pipelines via GitHub Actions
- Daily protocol tracker updates (3:00 AM EST)
- Compliance dashboards synced with Notion

### Key Workflows
1. **Evidence Ingestion** (`.github/workflows/ingest-evidence.yml`)
   - Automated PDF/XLSX parsing
   - Tax payment validation
   - Bank statement reconciliation

2. **Protocol Tracking**
   - 246 protocols across AADE, EPPO, EAD, Ktimatologio, MinDigital
   - Deadline monitoring with automated alerts
   - Cross-reference validation

3. **Compliance Monitoring**
   - US-Greece tax treaty compliance
   - GDPR Art. 15 requests
   - Cybercrime/fraud investigations (EPPO, FBI, IRS)

## 🚀 Quick Start

### Clone Repository
```bash
git clone https://github.com/alexandros-thomson/zeus-ai-evidence-package.git
cd zeus-ai-evidence-package
```

### Add Evidence Files
```bash
# Upload tax PDFs/XLSX to /evidence/raw/
cp /path/to/tax-documents/*.pdf evidence/raw/
cp /path/to/bank-statements/*.xlsx evidence/raw/
```

### Run Analysis Scripts
```bash
# Parse bank statements
python scripts/parse_statements.py

# Validate tax totals
python scripts/validate_tax_totals.py
```

### Sync Protocol Tracker
```bash
# Manual sync (automated via GitHub Actions)
git add evidence/MASTER-PROTOCOL-TRACKER.csv
git commit -m "Update protocol tracker"
git push origin main
```

## 📊 Current Status (Mar 1, 2026)

- **Total Protocols:** 246 (↑ from 240)
- **Active/Pending:** 111
- **Overdue:** 3 ⚠️
- **Critical Deadlines (0-7 days):** 2 🔴

### Critical Deadlines
1. **AEAD** (5995 EI 2026) - Mar 3, 2026 (2 days) 🔴
2. **MinDigital** (4633/4505/4314) - Mar 6, 2026 (6 days) 🟡
3. **Ktimatologio** (ND0113/26/06549) - Mar 14, 2026 (14 days) 🟢

### Recent Session (Feb 27-28, 2026)
- **Duration:** 5 hours (8:12 PM – 1:15 AM EST)
- **Fronts Executed:** 5 (Ktimatologio, EAD, Cybercrime, MinDigital x2)
- **New Emails:** 6 (5 delivered + 1 bounce corrected)
- **Protocols Added:** +6 (240 → 246)
- **All Bounces Resolved:** ✅ 4/4

## 🏛️ Agency Breakdown

### Top Agencies (Active Cases)
1. **AADE/ΔΕΣΥΠ** - 13 protocols
2. **AEAD (Εθνική Αρχή Διαφάνειας)** - 9 protocols
3. **AADE Ενδικοφανείς** - 8 protocols
4. **EPPO** - 8 protocols
5. **Greek Consulate Chicago** - 5 protocols

### Investigation Tracks
- **Tax Fraud:** IRS, AADE DESYP, EPPO
- **Cybercrime:** Hellenic Police, MinDigital, FBI IC3
- **EU Fraud:** EPPO (PP.00179/267/281/310), OLAF (FNS-25098)
- **Data Protection:** APDPX GDPR complaints
- **Property Fraud:** Ktimatologio, EAD transparency complaints

## 🔗 Connected Systems

- **Notion:** [⚖️ Justice for John — Deadline Digest](https://www.notion.so/30ffe5f31cb881db96bcda4e7254bc2e)
- **GitHub:** [alexandros-thomson/zeus-ai-evidence-package](https://github.com/alexandros-thomson/zeus-ai-evidence-package)
- **Drive:** Evidence sync via Google Drive/OneDrive/Box
- **Email:** Automated protocol tracking via Gmail API

## 📞 Contact

**Case Manager:** Kostadinos J Kyprianos  
**Company:** Kypria LLC  
**Location:** Roseville, MI  
**GitHub:** [@alexandros-thomson](https://github.com/alexandros-thomson)

---

⚓ **246 protocols. 30+ agencies. 42 days. Battle rhythm confirmed. ⚖️🧠🚀**

---

*Last Updated: March 1, 2026 via Zeus AI*