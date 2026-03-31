# STAGED SILENCE EXHIBITS — Deploy Instructions

## Status: ARMED — Ready for Apr 2-5, 2026

| Exhibit | Agency | Deploy Date | Protocol | Commit Message |
|---------|--------|-------------|----------|----------------|
| E-41 | Εισαγγελία Πειραιά | Apr 2 | 14678/2026 | `evidence(#408)` |
| E-42 | Αποκεντρωμένη Διοίκηση | Apr 2 | 18058/19466 | `evidence(#409)` |
| E-43 | ΚΕΦΟΔΕ DPO | Apr 3 | GDPR SAR | `evidence(#410)` |
| E-44 | AAA v. HRB | Apr 4 | 01-26-0001-2493 | `evidence(#411)` |
| E-45 | Δήμος Σπετσών | Apr 5 | 18058 | `evidence(#412)` |

## Deploy Procedure (per exhibit)

```bash
# 1. Navigate to exhibits directory
cd irs-ci-package/exhibits

# 2. Move the exhibit out of staged/
mv staged/E-XX-*.md ./

# 3. Edit the file: replace [TIMESTAMP] with current date/time
# Example: 2 April 2026, 00:01 EDT

# 4. Remove the STAGED status line

# 5. Commit with the pre-drafted message
git add E-XX-*.md
git commit -m "evidence(#NNN): [pre-drafted message from file]"
git push
```

## Single-Command Deploy (Apr 2 — both E-41 and E-42)

```bash
cd irs-ci-package/exhibits
for f in staged/E-4{1,2}-*-20260402.md; do
  sed -i 's/\[TIMESTAMP.*\]/2 April 2026, 00:01 EDT/' "$f"
  sed -i '/STATUS: STAGED/d' "$f"
  mv "$f" ./
done
git add E-41-* E-42-*
git commit -m "evidence(#408-409): Apr 2 deadline captures — Eisangelia + Apokentromeni silence"
git push
```

## Rules

1. **DO NOT** deploy before the deadline date
2. **DO NOT** draft new content — only capture and commit
3. Each deployed exhibit automatically feeds: Tab 3, Tab 5, Lane 3, ECHR timeline
4. Update MASTER-PROTOCOL-TRACKER after each deploy
5. The git commit hash IS the chain of custody

---
*Created: March 31, 2026 — Day 1,752*
*Author: Zeus AI Engine + alexandros-thomson*
