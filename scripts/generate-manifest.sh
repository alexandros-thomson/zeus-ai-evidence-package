#!/usr/bin/env bash
# generate-manifest.sh — Machine-generated chain-of-custody manifest
# Produces SHA-256 hashes for all binder source files plus commit metadata.
# Output is written into Appendix A and also as a standalone JSON manifest.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TABS_DIR="${REPO_ROOT}/irs-ci-package/tabs"
EXHIBITS_DIR="${REPO_ROOT}/irs-ci-package/exhibits"
APPENDIX="${TABS_DIR}/appendix-a-chain-of-custody.md"
MANIFEST_JSON="${REPO_ROOT}/irs-ci-package/manifest.json"
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BUILD_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
BUILD_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
SHORT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

echo "=== Chain-of-Custody Manifest Generator ==="
echo "Build date:   $BUILD_DATE"
echo "Build commit: $BUILD_COMMIT"
echo "Build branch: $BUILD_BRANCH"
echo ""

# ---------- Collect all binder source files ----------
declare -a FILES=()
for f in "$TABS_DIR"/*.md; do
  [ -f "$f" ] && FILES+=("$f")
done
for f in "$EXHIBITS_DIR"/*; do
  [ -f "$f" ] && FILES+=("$f")
done
# Include key root-level files
for f in "$REPO_ROOT/irs-ci-package/README.md" \
         "$REPO_ROOT/evidence/MASTER-PROTOCOL-TRACKER.csv" \
         "$REPO_ROOT/evidence-log.csv"; do
  [ -f "$f" ] && FILES+=("$f")
done

echo "Files to manifest: ${#FILES[@]}"
echo ""

# ---------- Generate manifest table rows ----------
MANIFEST_ROWS=""
JSON_ENTRIES=""

for f in "${FILES[@]}"; do
  rel_path=$(realpath --relative-to="$REPO_ROOT" "$f" 2>/dev/null || echo "$f")
  sha256=$(sha256sum "$f" | awk '{print $1}')
  short_hash=$(echo "$sha256" | cut -c1-16)

  # Get last commit for this file
  last_commit=$(git log -1 --format="%H" -- "$f" 2>/dev/null || echo "uncommitted")
  last_commit_short=$(echo "$last_commit" | cut -c1-7)
  last_date=$(git log -1 --format="%ai" -- "$f" 2>/dev/null || echo "$BUILD_DATE")
  last_date_short=$(echo "$last_date" | cut -c1-10)

  MANIFEST_ROWS="${MANIFEST_ROWS}| \`${rel_path}\` | \`${short_hash}...\` | \`${last_commit_short}\` | ${last_date_short} |\n"

  # JSON entry
  JSON_ENTRIES="${JSON_ENTRIES}    {\"file\": \"${rel_path}\", \"sha256\": \"${sha256}\", \"last_commit\": \"${last_commit}\", \"last_modified\": \"${last_date_short}\"},"
done

# Remove trailing comma from JSON
JSON_ENTRIES="${JSON_ENTRIES%,}"

# ---------- Write JSON manifest ----------
cat > "$MANIFEST_JSON" << JSONEOF
{
  "build_metadata": {
    "build_date": "${BUILD_DATE}",
    "build_commit": "${BUILD_COMMIT}",
    "build_branch": "${BUILD_BRANCH}",
    "repository": "alexandros-thomson/zeus-ai-evidence-package",
    "generator": "scripts/generate-manifest.sh",
    "protocol_count": "405+",
    "exhibit_count": 37
  },
  "files": [
${JSON_ENTRIES}
  ]
}
JSONEOF

echo "Wrote JSON manifest: $MANIFEST_JSON"

# ---------- Update Appendix A with build metadata ----------
if [ -f "$APPENDIX" ]; then
  # Replace build metadata placeholders using awk to avoid sed delimiter issues
  awk -v bd="$BUILD_DATE" -v bc="$BUILD_COMMIT" -v bb="$BUILD_BRANCH" '
    /Build Date \| \*\(populated at build time\)\*/ { gsub(/\*\(populated at build time\)\*/, bd) }
    /Build Commit \| \*\(populated at build time\)\*/ { gsub(/\*\(populated at build time\)\*/, "`" bc "`") }
    /Build Branch \| \*\(populated at build time\)\*/ { gsub(/\*\(populated at build time\)\*/, bb) }
    /\*\*Date:\*\* \*\(populated at build time\)\*/ { gsub(/\*\(populated at build time\)\*/, bd) }
    /\*\*Build Commit:\*\* \*\(populated at build time\)\*/ { gsub(/\*\(populated at build time\)\*/, "`" bc "`") }
    { print }
  ' "$APPENDIX" > "${APPENDIX}.tmp" && mv "${APPENDIX}.tmp" "$APPENDIX"

  # Replace manifest table
  MANIFEST_TABLE="| File | SHA-256 | Last Modified Commit | Date |\n|------|---------|---------------------|------|\n${MANIFEST_ROWS}"

  # Use awk to replace between MANIFEST_START and MANIFEST_END markers
  awk -v table="$MANIFEST_TABLE" '
    /<!-- MANIFEST_START/ { print; printf "%s", table; skip=1; next }
    /<!-- MANIFEST_END/ { skip=0 }
    !skip { print }
  ' "$APPENDIX" > "${APPENDIX}.tmp" && mv "${APPENDIX}.tmp" "$APPENDIX"

  echo "Updated Appendix A: $APPENDIX"
fi

echo ""
echo "=== Manifest generation complete ==="
echo "Files manifested: ${#FILES[@]}"
echo "JSON output:      $MANIFEST_JSON"
echo "Appendix updated: $APPENDIX"
