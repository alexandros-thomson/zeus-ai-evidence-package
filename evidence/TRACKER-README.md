# Evidence Tracker Ecosystem

## Canonical Tracker
**`evidence/MASTER-PROTOCOL-TRACKER.csv`** — The single source of truth for all protocols (#1 through #485+).

## Supporting Trackers
| File | Purpose | Rows |
|------|---------|------|
| `evidence/Action-Status.csv` | Action item tracking with deadlines | Active actions |
| `evidence/Target-Ref-Status.csv` | Agency complaint tracker — jurisdiction, ref numbers, channels, status | 29 agencies |
| `evidence/evidence-log.csv` | Supplemental protocol entries (#357-#407) — overflow from main tracker | 6 entries |
| `data/aade-debt-forensics.csv` | Ghost E1 income tax + ENFIA assessment forensics | 4 assessments |
| `irs-ci-package/Layer-Status.csv` | Y1-Y12 binder readiness layers | 12 layers |

## Death Propagation Matrix
**`data/death_propagation_matrix.csv`** — 27 agencies tracked with DeathStatus, Classification, DeathPropagationScore, SilenceClockDeadline. Cross-references Target-Ref-Status.csv by agency name.

## Archived Snapshots
`archive/protocol-tracker-snapshots/` — Historical snapshots from March 16-20, 2026. Superseded by `evidence/MASTER-PROTOCOL-TRACKER.csv`.

## Note on evidence-log.csv
Contains 6 entries (#357-#407) that appear to be overflow or out-of-band logging. These entries ARE also present in the main MASTER-PROTOCOL-TRACKER.csv. Retained for audit trail.

*Last updated: April 9, 2026 (Day 1,762)*
