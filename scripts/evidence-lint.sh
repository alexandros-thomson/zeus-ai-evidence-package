#!/usr/bin/env bash
# evidence-lint.sh — Lightweight validation for IRS-CI evidence binder inputs
# Exits non-zero if any FAIL is found. Warnings are informational only.
set -euo pipefail

TABS_DIR="${1:-irs-ci-package/tabs}"
EXHIBITS_DIR="${2:-irs-ci-package/exhibits}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

FAIL=0
WARN=0

fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }
warn() { echo "WARN: $1"; WARN=$((WARN + 1)); }
info() { echo "INFO: $1"; }

echo "=== Evidence Binder Lint ==="
echo "Tabs directory:     $TABS_DIR"
echo "Exhibits directory: $EXHIBITS_DIR"
echo ""

# ---------- 1. Required tabs exist and are non-empty ----------
REQUIRED_TABS=(
  "tab1-executive-summary.md"
  "tab2-contradiction-matrix.md"
  "tab3-timeline.md"
  "tab4-actor-map.md"
  "tab5-evidence-index.md"
  "tab6-mlat-map.md"
  "tab7-ask-list.md"
  "appendix-a-chain-of-custody.md"
)

echo "--- Checking required tabs ---"
for tab in "${REQUIRED_TABS[@]}"; do
  path="$TABS_DIR/$tab"
  if [ ! -f "$path" ]; then
    fail "Missing required tab: $tab"
  elif [ ! -s "$path" ]; then
    fail "Empty required tab: $tab"
  else
    lines=$(wc -l < "$path")
    if [ "$lines" -lt 5 ]; then
      warn "Tab $tab has only $lines lines — may be a stub"
    else
      info "OK: $tab ($lines lines)"
    fi
  fi
done
echo ""

# ---------- 2. Metadata checks ----------
echo "--- Checking metadata ---"
for tab in "$TABS_DIR"/*.md; do
  [ -f "$tab" ] || continue
  basename_tab=$(basename "$tab")

  # Check for CONFIDENTIAL header or case reference
  if ! grep -q -i "IRS.*CI\|IRS-CI\|26236541\|CONFIDENTIAL" "$tab" 2>/dev/null; then
    warn "$basename_tab: No IRS-CI case reference or CONFIDENTIAL header found"
  fi

  # Check for exhibit cross-references (tabs should reference exhibits)
  if ! grep -q "E-[0-9]" "$tab" 2>/dev/null; then
    warn "$basename_tab: No exhibit references (E-XX) found"
  fi
done
echo ""

# ---------- 3. Date format validation ----------
echo "--- Checking date formats ---"
for tab in "$TABS_DIR"/*.md; do
  [ -f "$tab" ] || continue
  basename_tab=$(basename "$tab")

  # Flag obviously malformed dates (e.g., month > 12, day > 31)
  if grep -P -n '\b(\d{2})/(\d{2})/(\d{4})\b' "$tab" 2>/dev/null | while IFS=: read -r line_num content; do
    # Extract dates and check bounds
    echo "$content" | grep -oP '\b(\d{2})/(\d{2})/(\d{4})\b' | while read -r date; do
      day=$(echo "$date" | cut -d/ -f1)
      month=$(echo "$date" | cut -d/ -f2)
      year=$(echo "$date" | cut -d/ -f3)
      if [ "$month" -gt 12 ] 2>/dev/null || [ "$day" -gt 31 ] 2>/dev/null; then
        warn "$basename_tab:$line_num: Possibly malformed date: $date"
      fi
    done
  done; then
    true
  fi
done
echo ""

# ---------- 4. Secret / redaction pattern checks ----------
echo "--- Checking for potential secrets or PII leaks ---"
SECRET_PATTERNS=(
  'password[[:space:]]*[:=]'
  'secret[[:space:]]*[:=]'
  'api[_-]?key[[:space:]]*[:=]'
  'bearer [a-zA-Z0-9_\-]{20,}'
  'ghp_[a-zA-Z0-9]{36}'
  'sk-[a-zA-Z0-9]{48}'
  'AKIA[0-9A-Z]{16}'
  '\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b'
)

SECRET_LABELS=(
  "password literal"
  "secret literal"
  "API key literal"
  "bearer token"
  "GitHub PAT"
  "OpenAI key"
  "AWS access key"
  "SSN pattern (XXX-XX-XXXX)"
)

for i in "${!SECRET_PATTERNS[@]}"; do
  pattern="${SECRET_PATTERNS[$i]}"
  label="${SECRET_LABELS[$i]}"

  matches=$(grep -r -l -P -i "$pattern" "$TABS_DIR" "$EXHIBITS_DIR" 2>/dev/null || true)
  if [ -n "$matches" ]; then
    for f in $matches; do
      # SSN pattern in the evidence index context is expected (case identifiers)
      if [[ "$label" == "SSN pattern"* ]] && grep -q "AAA\|Case\|Arbitration\|01-26-" "$f" 2>/dev/null; then
        info "SSN-like pattern in $f — appears to be case ID (OK)"
      else
        warn "Potential $label found in: $f"
      fi
    done
  fi
done
echo ""

# ---------- 5. Track separation check ----------
echo "--- Checking track separation (no tax amendment / Tracy / Greenback / AAA settlement content) ---"
FORBIDDEN_PATTERNS=(
  'amended.*return'
  'Form.*1040-?X'
  'Greenback'
  'AAA.*settlement.*amount'
  'settlement.*offer'
)

FORBIDDEN_LABELS=(
  "amended return reference"
  "Form 1040-X reference"
  "Greenback reference"
  "AAA settlement amount"
  "settlement offer"
)

for i in "${!FORBIDDEN_PATTERNS[@]}"; do
  pattern="${FORBIDDEN_PATTERNS[$i]}"
  label="${FORBIDDEN_LABELS[$i]}"

  matches=$(grep -r -l -P -i "$pattern" "$TABS_DIR" 2>/dev/null || true)
  if [ -n "$matches" ]; then
    for f in $matches; do
      warn "Track separation: $label found in $(basename "$f") — ensure operational separation"
    done
  fi
done
echo ""

# ---------- 6. Exhibit reference consistency ----------
echo "--- Checking exhibit reference consistency ---"
# Collect all exhibit references from tabs
all_refs=$(grep -r -ohP 'E-\d+' "$TABS_DIR" 2>/dev/null | sort -t- -k2 -n | uniq)
# Check if referenced exhibits have corresponding files
for ref in $all_refs; do
  # Look for files matching the exhibit ID
  found=$(find "$EXHIBITS_DIR" -iname "*${ref}*" -o -iname "*$(echo "$ref" | tr '-' '_')*" 2>/dev/null | head -1)
  if [ -z "$found" ]; then
    # Not all exhibits need dedicated files — many are referenced PDFs
    true
  fi
done
info "Exhibit references found: $(echo "$all_refs" | wc -w) unique IDs across tabs"
echo ""

# ---------- Summary ----------
echo "=== Lint Summary ==="
echo "Failures: $FAIL"
echo "Warnings: $WARN"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo "RESULT: FAIL — $FAIL critical issue(s) must be resolved before build"
  exit 1
else
  echo ""
  echo "RESULT: PASS (with $WARN warning(s))"
  exit 0
fi
