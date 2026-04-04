# IRS-CI Evidence Package — April 20, 2026

**Prepared for:** SA Clint Zacheranik + SA Henry Pletscher, IRS Criminal Investigation
**Prepared by:** Stamatina Kyprianos (also appearing in Greek records as Σταματίνα Κυπριανού)
**Case References:** IRS-CI Case 26236541 | IRS Form 14157 | FBI IC3 eaa5459ac668431abdb33a7f545c3282
**Subject:** Cross-Border Identity Theft, Tax Fraud & Estate Exploitation — AFM 051422558 (deceased) / AFM 044594747 (widow)
**Meeting:** April 21, 2026 (confirmed) — 16441 Waterman Dr, Roseville, MI 48066

## Package Contents

| Tab | Title | Status |
|-----|-------|--------|
| Cover | [Cover Sheet](tabs/cover-sheet.md) | ✅ Complete |
| 1 | [Executive Summary](tabs/tab1-executive-summary.md) | ✅ Draft |
| 2 | [Contradiction Matrix](tabs/tab2-contradiction-matrix.md) | ✅ Draft |
| 3 | [Master Timeline](tabs/tab3-timeline.md) | ✅ Draft |
| 4 | [Actor Map](tabs/tab4-actor-map.md) | ✅ Draft |
| 5 | [Evidence Index](tabs/tab5-evidence-index.md) | ✅ Skeleton |
| 6 | [MLAT / Record-Compulsion Map](tabs/tab6-mlat-map.md) | ✅ Draft |
| 7 | [Ask List](tabs/tab7-ask-list.md) | ✅ Draft |
| A | [Chain of Custody / Source Authentication](tabs/appendix-a-chain-of-custody.md) | ✅ Auto-generated |

## Architecture

- **Source of truth:** This GitHub repository (Markdown files)
- **PDF output:** Generated from Markdown via Pandoc + XeLaTeX (GitHub Actions)
- **Evidence files:** `/exhibits/` folder
- **Audit trail:** Every change has a commit hash, timestamp, and author — this IS the chain of custody
- **Chain of custody:** Machine-generated manifest with SHA-256 hashes (Appendix A + `manifest.json`)

## Building the Binder

### Automatic (GitHub Actions)

The binder builds automatically on:
- **Push** to `irs-ci-package/**` or `scripts/build-binder.sh`
- **Manual trigger** via Actions → "Build Investigator Binder" → Run workflow
- **Release** creation

Artifacts appear in the workflow run's Artifacts section:
- `irs-ci-binder-pdf` — The compiled PDF binder
- `irs-ci-binder-package` — ZIP package with all source files + PDF
- `chain-of-custody-manifest` — `manifest.json` with SHA-256 hashes
- `binder-combined-markdown` — Single combined Markdown file

### Local Build

```bash
# Prerequisites: pandoc, texlive-xetex, zip
sudo apt-get install pandoc texlive-xetex texlive-latex-extra texlive-fonts-recommended lmodern zip

# Run the build
bash scripts/build-binder.sh

# Output in build/ directory
ls build/
```

### Evidence Lint (Validation)

```bash
bash scripts/evidence-lint.sh
```

Checks: required tabs exist, metadata present, date formats valid, no secrets/PII leaks, track separation enforced, exhibit references consistent.

### Chain-of-Custody Manifest

```bash
bash scripts/generate-manifest.sh
```

Generates `irs-ci-package/manifest.json` and updates Appendix A with SHA-256 hashes and commit metadata.

## Build Status

- Package started: March 30, 2026
- Pipeline added: March 31, 2026
- Last updated: March 31, 2026
- Target freeze: April 18, 2026
- Meeting date: ~April 20, 2026
- Protocol count at creation: 445++
