# E-117a — Chain-of-Custody Hash Anchor for HDPA Portal HTTP 403 Capture

**Status:** POST-FREEZE LIVING EXHIBIT — forensic anchor record
**Bates:** E-117a (channel-obstruction evidence)
**Capture event:** 2026-04-28 ~09:30 EDT (16:30 EEST), Day 1,780
**Ground truth:** ΑΠΔΠΧ web form returned HTTP 403 from US-origin IP **24.192.40.33** on both `/syndesi/katagelies` and `/polites/katagelia_apo_polites`.
**WAF identifiers:** Attack ID **20000009**; Message IDs **003412165799** and **003412169361**.

This document is the **immutable chain-of-custody anchor** recommended by Claude Opus 4.7 Thinking in the three-model triangulation (see E-118). It records both forensic-preservation methods (GPT-5.5 Thinking + Claude Opus 4.7 Thinking) and commits the SHA-256 hash of every artifact to git history, so the capture authenticity is anchored in a public commit timestamp before any respondent can challenge it.

---

## Why This Matters

A US-resident data subject was blocked at the WAF layer of the supervisory authority's own complaint portal. The block evidences a public body's portal frustrating an Art. 77 GDPR complaint route from outside the EU — the very channel the Authority publishes for that purpose. The forensic value of this fact is proportional to the authenticity of the capture. Without immutable timestamping, a hostile respondent can claim fabrication. With a SHA-256 anchored in git's commit graph (which is itself a Merkle tree of cryptographic hashes), the timestamp and content are mathematically provable.

---

## Forensic Preservation Triad (Both Models Combined)

### Layer 1 — Visual / Repeatability (GPT-5.5 Thinking)

For each `/syndesi/katagelies` and `/polites/katagelia_apo_polites` attempt, capture:

1. **Full-page screenshot** (PNG, lossless) showing the 403 response body.
2. **Full URL** in the address bar.
3. **System clock timestamp** (UTC + local) visible in the screenshot.
4. **Browser + OS context** — User-Agent string, OS version (kostass-mac-mini macOS), browser version.
5. **Public IP** — `24.192.40.33` (confirm via `curl ifconfig.me`).
6. **Geo-resolution** — `whois 24.192.40.33` snippet showing US allocation (Comcast / Roseville MI region).

### Layer 2 — Network Forensic (Claude Opus 4.7 Thinking)

For each attempt, capture:

1. **Raw HTTP response headers** — full `Date`, `Server`, `X-Cache`, `X-Cache-Hits`, `X-Akamai-*` / `X-Sucuri-*` / WAF vendor headers, `Set-Cookie`, `Content-Length`, plus the WAF-specific `X-WAF-Attack-ID: 20000009` and `X-WAF-Message-ID` fields.
2. **TLS handshake timestamp** — record from `openssl s_client -connect <host>:443 -servername <host>` showing `Server certificate` validity period and `Verify return code: 0 (ok)`.
3. **Referring URL** — what page linked into the form (proves the path was discovered through the published HDPA navigation, not guessed).
4. **HAR file export** — Chrome / Firefox DevTools Network tab → Save as HAR → contains every request/response in JSON.
5. **DNS resolution** — `dig www.dpa.gr +short` and `dig +trace` output to anchor what IP the host resolved to at capture time.

### Layer 3 — Hash Anchor (this document)

After all artifacts are saved into `irs-ci-package/exhibits/E-117a-portal-block-captures/`, run:

```bash
cd irs-ci-package/exhibits/E-117a-portal-block-captures/
for f in *; do sha256sum "$f"; done > ../E-117a-MANIFEST.sha256
sha256sum ../E-117a-MANIFEST.sha256 > ../E-117a-MANIFEST.sha256.root
```

Both files (`E-117a-MANIFEST.sha256` and `E-117a-MANIFEST.sha256.root`) are committed to git. The git commit hash itself is then a Merkle-rooted timestamp that no party can backdate or alter without breaking every downstream commit hash. This is the immutable anchor.

---

## Capture Checklist (when Stamatina is at the keyboard)

- [ ] Open Chrome / Safari, DevTools → Network tab → "Preserve log" + "Disable cache" enabled
- [ ] Visit `https://www.dpa.gr/syndesi/katagelies`. Capture screenshot + HAR.
- [ ] Visit `https://www.dpa.gr/polites/katagelia_apo_polites`. Capture screenshot + HAR.
- [ ] Run from terminal: `curl -v -A "Mozilla/5.0 ..." https://www.dpa.gr/syndesi/katagelies > capture-syndesi.headers 2>&1`
- [ ] Run from terminal: `curl -v -A "Mozilla/5.0 ..." https://www.dpa.gr/polites/katagelia_apo_polites > capture-polites.headers 2>&1`
- [ ] Run: `openssl s_client -connect www.dpa.gr:443 -servername www.dpa.gr -showcerts < /dev/null > capture-tls.txt 2>&1`
- [ ] Run: `dig www.dpa.gr +short > capture-dns.txt; dig +trace www.dpa.gr >> capture-dns.txt`
- [ ] Run: `curl -s ifconfig.me > capture-publicip.txt`
- [ ] Run: `whois 24.192.40.33 > capture-whois.txt`
- [ ] Save all into `E-117a-portal-block-captures/` and run hash anchor commands above
- [ ] Commit with message: `E-117a forensic capture: HDPA portal HTTP 403 obstruction — Day 1,780`

---

## Why The Hash Anchor Wins

If, at any point in the next 12 months, AADE or HDPA argues the capture is fabricated, the response is:

> "The full forensic bundle is committed at git commit `<HASH>` of `alexandros-thomson/zeus-ai-evidence-package`, made on 28-29 April 2026. The commit hash is a SHA-1 (or SHA-256, post-2027 transition) Merkle root over the entire repo state at that timestamp. Tampering with any file would invalidate every subsequent commit in the chain. The repository is publicly archived on github.com and mirrored on Kypria-LLC. Authenticity is mathematically anchored, not asserted."

That argument is unanswerable unless the respondent wants to argue that GitHub's commit graph is forged — which they will not.

---

## Cross-Reference

- E-115 — Push 8 master record (HDPA Art. 77 καταγγελία)
- E-117 — Filing payload
- E-117b — Email submission record
- E-118 — Three-model triangulation memo (Claude Opus 4.7 Thinking's chain-of-custody recommendation source)
- Issue #1 Comment 4336081404

---

*Compiled Day 1,780. The hash anchor is the difference between "I got blocked" and "I have admissible, mathematically verifiable evidence I got blocked." Claude Opus 4.7 Thinking's unique contribution.*
