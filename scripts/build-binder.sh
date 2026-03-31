#!/usr/bin/env bash
# build-binder.sh — Assembles IRS-CI evidence binder from Markdown tabs into PDF + ZIP
# Requires: pandoc, a LaTeX engine (tectonic or xelatex)
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TABS_DIR="${REPO_ROOT}/irs-ci-package/tabs"
EXHIBITS_DIR="${REPO_ROOT}/irs-ci-package/exhibits"
OUTPUT_DIR="${REPO_ROOT}/build"
BUILD_DATE=$(date -u +"%Y-%m-%d")
BUILD_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

echo "=== IRS-CI Evidence Binder Builder ==="
echo "Build date:   $BUILD_DATE"
echo "Build commit: $BUILD_COMMIT"
echo ""

mkdir -p "$OUTPUT_DIR"

# ---------- 1. Generate manifest (updates Appendix A in-place) ----------
echo "--- Step 1: Generating chain-of-custody manifest ---"
bash "${REPO_ROOT}/scripts/generate-manifest.sh"
echo ""

# ---------- 2. Assemble combined Markdown ----------
echo "--- Step 2: Assembling binder Markdown ---"

COMBINED="${OUTPUT_DIR}/binder-combined.md"
cat > "$COMBINED" << 'HEADER'
---
title: "IRS-CI Evidence Package — Case 26236541"
subtitle: "Cross-Border Identity Theft, Tax Fraud & Estate Exploitation"
author: "Prepared for SA Clint Zacheranik + SA Henry Pletscher, IRS Criminal Investigation"
date: "April 20, 2026"
subject: "AFM 051422558 (deceased) / AFM 044594747 (widow)"
keywords: [IRS-CI, MLAT, evidence, cross-border fraud]
lang: en
geometry: margin=1in
fontsize: 11pt
toc: true
toc-depth: 2
header-includes:
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhead[L]{IRS-CI Case 26236541}
  - \fancyhead[R]{CONFIDENTIAL}
  - \fancyfoot[C]{\thepage}
  - \fancyfoot[R]{Zeus AI Evidence Architecture}
  - \usepackage{longtable}
  - \usepackage{booktabs}
---

\newpage
HEADER

# Ordered tab assembly
TABS=(
  "tab1-executive-summary.md"
  "tab2-contradiction-matrix.md"
  "tab3-timeline.md"
  "tab4-actor-map.md"
  "tab5-evidence-index.md"
  "tab6-mlat-map.md"
  "tab7-ask-list.md"
  "appendix-a-chain-of-custody.md"
)

for tab in "${TABS[@]}"; do
  path="${TABS_DIR}/${tab}"
  if [ -f "$path" ]; then
    echo "  Adding: $tab"
    cat "$path" >> "$COMBINED"
    echo -e "\n\n\\\\newpage\n\n" >> "$COMBINED"
  else
    echo "  SKIP (not found): $tab"
  fi
done

echo "Combined Markdown: $(wc -l < "$COMBINED") lines"
echo ""

# ---------- 3. Compile PDF ----------
echo "--- Step 3: Compiling PDF ---"
PDF_OUTPUT="${OUTPUT_DIR}/IRS-CI-Evidence-Package-${BUILD_DATE}.pdf"

# Try pandoc with different PDF engines in order of preference
PDF_SUCCESS=false

# Attempt 1: pandoc with tectonic (fast, self-contained)
if command -v pandoc &>/dev/null; then
  for engine in tectonic xelatex pdflatex lualatex; do
    if command -v "$engine" &>/dev/null || [ "$engine" = "pdflatex" ]; then
      echo "  Trying pandoc + $engine..."
      if pandoc "$COMBINED" \
        -o "$PDF_OUTPUT" \
        --pdf-engine="$engine" \
        --standalone \
        --toc \
        --number-sections \
        -V colorlinks=true \
        -V linkcolor=blue \
        -V urlcolor=blue \
        -V toccolor=black \
        2>/dev/null; then
        echo "  PDF compiled successfully with $engine"
        PDF_SUCCESS=true
        break
      else
        echo "  $engine failed, trying next..."
      fi
    fi
  done

  # Attempt 2: pandoc HTML-to-PDF via wkhtmltopdf or weasyprint
  if [ "$PDF_SUCCESS" = false ]; then
    for html_engine in wkhtmltopdf weasyprint; do
      if command -v "$html_engine" &>/dev/null; then
        echo "  Trying pandoc → HTML → $html_engine..."
        HTML_TMP="${OUTPUT_DIR}/binder-combined.html"
        pandoc "$COMBINED" -o "$HTML_TMP" --standalone --toc 2>/dev/null || true
        if [ -f "$HTML_TMP" ]; then
          if [ "$html_engine" = "wkhtmltopdf" ]; then
            wkhtmltopdf "$HTML_TMP" "$PDF_OUTPUT" 2>/dev/null && PDF_SUCCESS=true
          elif [ "$html_engine" = "weasyprint" ]; then
            weasyprint "$HTML_TMP" "$PDF_OUTPUT" 2>/dev/null && PDF_SUCCESS=true
          fi
          [ "$PDF_SUCCESS" = true ] && echo "  PDF compiled via $html_engine"
          rm -f "$HTML_TMP"
          break
        fi
      fi
    done
  fi
fi

if [ "$PDF_SUCCESS" = false ]; then
  echo "  WARNING: PDF compilation failed. Producing HTML fallback."
  pandoc "$COMBINED" \
    -o "${OUTPUT_DIR}/IRS-CI-Evidence-Package-${BUILD_DATE}.html" \
    --standalone \
    --toc \
    --metadata title="IRS-CI Evidence Package — Case 26236541" \
    2>/dev/null || echo "  HTML fallback also failed. Combined Markdown still available."
fi
echo ""

# ---------- 4. Build ZIP package ----------
echo "--- Step 4: Building ZIP package ---"
ZIP_OUTPUT="${OUTPUT_DIR}/IRS-CI-Evidence-Package-${BUILD_DATE}.zip"

# Create a staging directory
STAGE="${OUTPUT_DIR}/stage"
rm -rf "$STAGE"
mkdir -p "$STAGE/tabs" "$STAGE/exhibits" "$STAGE/evidence"

# Copy tabs
cp "$TABS_DIR"/*.md "$STAGE/tabs/" 2>/dev/null || true

# Copy exhibits
cp "$EXHIBITS_DIR"/* "$STAGE/exhibits/" 2>/dev/null || true

# Copy key evidence files
cp "$REPO_ROOT/irs-ci-package/README.md" "$STAGE/" 2>/dev/null || true
cp "$REPO_ROOT/irs-ci-package/manifest.json" "$STAGE/" 2>/dev/null || true

# Copy PDF if it was built
[ -f "$PDF_OUTPUT" ] && cp "$PDF_OUTPUT" "$STAGE/"

# Copy combined Markdown
cp "$COMBINED" "$STAGE/"

# Build ZIP
(cd "$STAGE" && zip -r "$ZIP_OUTPUT" . -x "*.DS_Store" 2>/dev/null) || \
(cd "$STAGE" && tar czf "${ZIP_OUTPUT%.zip}.tar.gz" . 2>/dev/null && echo "  Used tar.gz fallback")

rm -rf "$STAGE"

echo ""

# ---------- Summary ----------
echo "=== Build Summary ==="
echo "Combined Markdown: ${COMBINED}"
[ -f "$PDF_OUTPUT" ] && echo "PDF Binder:        ${PDF_OUTPUT}" && echo "PDF size:          $(du -h "$PDF_OUTPUT" | cut -f1)"
[ -f "$ZIP_OUTPUT" ] && echo "ZIP Package:       ${ZIP_OUTPUT}" && echo "ZIP size:          $(du -h "$ZIP_OUTPUT" | cut -f1)"
[ -f "${ZIP_OUTPUT%.zip}.tar.gz" ] && echo "TAR.GZ Package:    ${ZIP_OUTPUT%.zip}.tar.gz"
echo "Manifest JSON:     ${REPO_ROOT}/irs-ci-package/manifest.json"
echo ""
echo "Build artifacts are in: $OUTPUT_DIR/"
echo "=== Build complete ==="
