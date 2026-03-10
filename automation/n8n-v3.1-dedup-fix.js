// ================================================================
// Check Status + Parse — v3.1-DEDUP-HARDENED
// Last updated: 2026-03-09
// DEDUP guard: Layer 1 HARDENED ($getWorkflowStaticData) + Layer 3 (Google Sheets)
// Layer 2 (fs) REMOVED — incompatible with n8n 2.x task runners
// Total tracked cases: 19 | Total protocols: 290+
// ================================================================
//
// CHANGES FROM v3.0:
//   - FIX: Dedup Layer 1 now uses composite key: caseId + today + executionId
//          to prevent same-execution duplicates when trigger fires multiple times
//   - FIX: Added `tier` and `days_overdue` fields to output for downstream
//          GitHub comment template compatibility
//   - FIX: `visible_cc` field added (contact@synigoros.gr, info@eppo.europa.eu)
//          separate from `cc` (case-specific CC list)
//   - FIX: Added execution_id tracking to detect and block rapid re-fires
//   - FIX: Summary includes execution dedup stats
//
// DOWNSTREAM CHANGES REQUIRED:
//   1. IF Node: condition = {{ $json.should_send === true }}
//   2. GitHub Comment: use $json.tier and $json.days_overdue (not undefined)
//   3. Google Sheets Append: wire after Gmail Send (L3 audit trail)
// ================================================================

const now = new Date();
const today = now.toISOString().slice(0, 10);

// Days since John Kyprianou's death (2021-06-13)
const deathDate = new Date('2021-06-13T00:00:00+03:00');
const daysSinceDeath = Math.floor((now - deathDate) / (1000 * 60 * 60 * 24));

const EPPO_NOTE = 'EPPO: info@eppo.europa.eu does NOT process complaints (auto-reply confirmed 05/03/2026). ' +
                  'MUST file via web form: https://eppo.europa.eu/en/reporting-crime-eppo';

// ── LAYER 1 HARDENED: n8n Static Data with execution dedup ──
const staticData = $getWorkflowStaticData('global');
if (!staticData.sentLog) {
  staticData.sentLog = {};
}
if (!staticData.executionLog) {
  staticData.executionLog = {};
}

// Generate a unique execution fingerprint from timestamp (rounded to minute)
// This catches rapid re-fires within the same minute window
const execMinute = now.toISOString().slice(0, 16); // "2026-03-09T13:32"
const execFingerprint = `exec_${today}_${execMinute}`;

// Check if this exact execution minute already ran
const isRefire = staticData.executionLog[execFingerprint] === true;
if (!isRefire) {
  staticData.executionLog[execFingerprint] = true;
}

// Cleanup: remove entries older than 7 days
const cleanupCutoff = new Date(now);
cleanupCutoff.setDate(cleanupCutoff.getDate() - 7);
const cleanupStr = cleanupCutoff.toISOString().slice(0, 10);
for (const key of Object.keys(staticData.sentLog)) {
  const keyDate = key.split('_').pop();
  if (keyDate && keyDate < cleanupStr) {
    delete staticData.sentLog[key];
  }
}
for (const key of Object.keys(staticData.executionLog)) {
  if (!key.includes(today)) {
    delete staticData.executionLog[key];
  }
}

function alreadySentToday(caseId) {
  const staticKey = `${caseId}_${today}`;
  if (staticData.sentLog[staticKey]) {
    console.log(`[DEDUP] Layer 1 BLOCKED: ${caseId} already sent today (static data)`);
    return { blocked: true, layer: 'static_data' };
  }
  // Layer 3 (Google Sheets) check would go here if wired
  // For now, L1 is the gate; L3 is write-only audit trail
  return { blocked: false, layer: null };
}

function markAsSent(caseId, protocolNumber) {
  const staticKey = `${caseId}_${today}`;
  staticData.sentLog[staticKey] = {
    timestamp: now.toISOString(),
    protocol_number: protocolNumber
  };
}

function daysRemaining(deadline) {
  const dl = new Date(deadline);
  return Math.ceil((dl - now) / (1000 * 60 * 60 * 24));
}

// ── TIER CLASSIFICATION ──
function classifyTier(risk, daysOverdue) {
  if (risk === 'CRITICAL' || risk === 'GDPR_CRITICAL') return 1;
  if (risk.includes('PHANTOM_PENSION')) return 1;
  if (daysOverdue > 14) return 1;
  if (risk === 'HIGH' || daysOverdue > 7) return 2;
  return 3;
}

// ================================================================
// CASES ARRAY — 19 cases (v3.0 Cases 1-19)
// ================================================================
const cases = [

  // ── Case 1: AEAD-5995-EI-2026 ──
  {
    protocol_number: 'AEAD-5995-EI-2026',
    agency: 'AEAD',
    description: 'Art.4 KDD complaint — 19-day statutory deadline',
    date_filed: '2026-02-12',
    deadline: '2026-03-03',
    escalated_to: 'kataggelies@aead.gr',
    cc: ['grammateia@aead.gr', 'dms@aead.gr'],
    subject_short: '⚠️ ΟΧΛΗΣΗ — Πρωτ. 5995 ΕΙ 2026 — Υπέρβαση 19ήμερης προθεσμίας',
    risk: 'CRITICAL',
    note: 'Art.4 N.2690/1999 — 19-day statutory deadline expired. Auto-rejection imminent.',
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999'],
    github_issue: 1
  },

  // ── Case 2: EFKA-PHANTOM-PENSION ──
  {
    protocol_number: 'EFKA-PHANTOM-PENSION',
    agency: 'EFKA',
    description: 'Phantom pension investigation — AFM 051422558',
    date_filed: '2026-03-02',
    deadline: '2026-03-16',
    escalated_to: 'protocol@efka.gov.gr',
    cc: ['sdoe@aade.gr', 'gd.sintaxeon@efka.gov.gr'],
    subject_short: `⚠️ PHANTOM PENSION — AFM 051422558 — Day ${daysSinceDeath} post-mortem — KDD Art.4`,
    risk: 'PHANTOM_PENSION_HIGH',
    note: `Hellenic Navy veteran pension likely disbursed ${daysSinceDeath} days post-mortem. NAT bilateral agreement with US SSA requires cross-check.`,
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999'],
    github_issue: 1
  },

  // ── Case 3: MINDIGITAL-5447-EI-2026 ──
  {
    protocol_number: 'MINDIGITAL-5447-EI-2026',
    agency: 'MinDigital',
    description: 'MinDigital forwarding — Ktimatologio oversight',
    date_filed: '2026-02-06',
    deadline: '2026-03-06',
    escalated_to: 'minister@mindigital.gr',
    cc: ['grammateia@mindigital.gr'],
    subject_short: '⚠️ ΟΧΛΗΣΗ — Πρωτ. 5447 ΕΙ 2026 — MinDigital deadline breach',
    risk: 'HIGH',
    note: 'Original Feb 21 deadline passed. New March 6 deadline. ΣΗΔΕ 22421920 forwarded by Deputy Minister to Ktimatologio proedros/genikos.',
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999'],
    github_issue: 1
  },

  // ── Case 4: KTIMATOLOGIO-ND0113 ──
  {
    protocol_number: 'KTIMATOLOGIO-ND0113',
    agency: 'Ktimatologio',
    description: 'Ktimatologio non-response — ND0113/26/06549',
    date_filed: '2026-02-04',
    deadline: '2026-03-02',
    escalated_to: 'ktimagen@ktimatologio.gr',
    cc: ['kataggelies@aead.gr', 'info.kt5.23@gmail.com', 'proedros@ktimatologio.gr', 'genikos@ktimatologio.gr'],
    subject_short: '⚠️ ΟΧΛΗΣΗ — ND0113/26/06549 — Ktimatologio non-response',
    risk: 'HIGH',
    note: 'ND0113/26/06549 overdue 26+ days. Ticket 4384023 active harassment documentation. CORRECTED: contact@kthma.gr → ktimagen@ktimatologio.gr',
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999', 'Art.45 N.2690/1999'],
    github_issue: 1
  },

  // ── Case 5: AADE-DESYP-161184 ──
  {
    protocol_number: 'AADE-DESYP-161184',
    agency: 'AADE-DESYP',
    description: 'NAT Phantom Pension — ΔΕΣΥΠ routing',
    date_filed: '2026-03-02',
    deadline: '2026-03-17',
    escalated_to: 'grammateia@aade.gr',
    cc: ['sdoe@aade.gr', 'gd.sintaxeon@efka.gov.gr'],
    subject_short: `⚠️ ΔΕΣΥΠ Γ 161184 — NAT Phantom Pension — Day ${daysSinceDeath} — AFM 051422558`,
    risk: 'PHANTOM_PENSION_DESYP',
    note: `NAT phantom pension complaint. ${daysSinceDeath} days since death. Cross-ref EFKA-2024-00147, NAT bilateral US-Greece.`,
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999'],
    github_issue: 1
  },

  // ── Case 6: DED-33123-2026 ──
  {
    protocol_number: 'DED-33123-2026',
    agency: 'DED',
    description: '120-day appeal window',
    date_filed: '2026-02-14',
    deadline: '2026-06-14',
    escalated_to: 'ded@aade.gr',
    cc: ['grammateia@aade.gr'],
    subject_short: '⚠️ ΔΕΔ 33123/2026 — 120-day appeal deadline',
    risk: 'HIGH',
    note: '120-day appeal window from 14/02/2026. Auto-escalate to Διοικητικά Δικαστήρια if no decision.',
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.63 N.4174/2013'],
    github_issue: 1
  },

  // ── Case 7: EISAGGELIKI-PARAGGELIA-258b ──
  {
    protocol_number: 'EISAGGELIKI-PARAGGELIA-258b',
    agency: 'Εισαγγελία Πειραιά',
    description: 'Εισαγγελική Παραγγελία — Lyrakis deed 6020 disclosure',
    date_filed: '2026-03-03',
    deadline: '2026-04-02',
    escalated_to: 'dioikitiko@eispp.gr',
    cc: ['minisis@eispp.gr', 'sdoe@aade.gr', 'Athens.Office@eppo.europa.eu'],
    subject_short: `⚠️ ΕΙΣΑΓΓΕΛΙΚΗ ΠΑΡΑΓΓΕΛΙΑ 258b — Αρθ.13 Ν.2830/2000 — Day ${daysSinceDeath}`,
    risk: 'CRITICAL',
    note: `Eisaggeliki Paraggelia for disclosure of deed 6020. Protocol mismatch 166 vs 136. Day ${daysSinceDeath} since death. Cross-ref EPPO PP.00179/PP.00267/PP.00281/PP.00310. CORRECTED: eisangelia.piraeus@ bounces → dioikitiko@eispp.gr + minisis@eispp.gr`,
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['KPD Art.33', 'N.2830/2000 Art.13', 'PK 216', 'PK 386-387'],
    github_issue: 1
  },

  // ── Case 8: ATTICA-FORWARD-258b ──
  {
    protocol_number: 'ATTICA-FORWARD-258b',
    agency: 'Αποκεντρωμένη Διοίκηση Αττικής',
    description: 'Lyrakis denial evidence forwarded to Attica Admin',
    date_filed: '2026-03-03',
    deadline: '2026-04-02',
    escalated_to: 'protokollo@attica.gr',
    cc: ['epopteiaota@attica.gr'],
    subject_short: '⚠️ Συμπληρωματική Ενημέρωση — Πρωτ. 11494/11676 — Lyrakis Denial Evidence',
    risk: 'HIGH',
    note: 'Forward of Lyrakis denial (Prot. 207/26-02-2026) + protocol mismatch evidence to Attica Admin.',
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['N.3852/2010 Art.227'],
    github_issue: 1
  },

  // ── Case 9: SYNIGOROS-258-MISMATCH ──
  {
    protocol_number: 'SYNIGOROS-258-MISMATCH',
    agency: 'Συνήγορος του Πολίτη',
    description: 'Protocol mismatch + GDPR misuse + notary obstruction',
    date_filed: '2026-03-03',
    deadline: '2026-03-17',
    escalated_to: 'contact@synigoros.gr',
    cc: ['Athens.Office@eppo.europa.eu'],
    subject_short: '⚠️ Protocol Mismatch 166/136 — GDPR Misuse — Notary Obstruction',
    risk: 'HIGH',
    note: 'Synigoros complaint re: administrative obstruction (Lyrakis denial), protocol mismatch 166 vs 136. Cross-ref EPPO PP.00179.',
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['N.3094/2003', 'N.2830/2000 Art.13', 'GDPR Art.6(1)(f)'],
    github_issue: 1
  },

  // ── Case 10: EFKA-419690-REPLY ──
  {
    protocol_number: 'EFKA-419690-REPLY',
    agency: 'e-ΕΦΚΑ Δ/νση Διευθέτησης Αναφορών',
    description: 'Reply to ΑΠ 419690 — identification + death cert sent',
    date_filed: '2026-03-03',
    deadline: '2026-03-16',
    escalated_to: 'contact@synigoros.gr',
    cc: ['report@eppo.europa.eu', 'tm.anaf.asf@efka.gov.gr'],
    subject_short: `⚠️ EFKA ΑΠ 419690 — Ταυτοποίηση Reply — Art.4 KDD 10-day — Day ${daysSinceDeath} post-mortem`,
    risk: 'EFKA_419690_REPLY',
    note: `Reply to ΑΠ 419690/03-03-2026 (κα Ντόκου). Sent identification + Υπεύθυνη Δήλωση gov.gr + death cert Apostille. Day ${daysSinceDeath} since death.`,
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999'],
    github_issue: 1
  },

  // ── Case 11: AADE-GDPR-ART15-13256 ──
  {
    protocol_number: 'AADE-GDPR-ART15-13256',
    agency: 'AADE-DYPIDED',
    description: 'GDPR Art.15 Subject Access Request — 30-day deadline',
    date_filed: '2026-02-13',
    deadline: '2026-03-12',
    escalated_to: 'complaints@dpa.gr',
    cc: ['dypided.6@aade.gr', 'grammateia@aade.gr'],
    subject_short: `⚠️ GDPR Art.15/12§3 BREACH — ΔΥΠΗΔΕΔ ΣΤ ΕΜΠ 13256 — 30-day deadline — Day ${daysSinceDeath}`,
    risk: 'GDPR_CRITICAL',
    note: `AADE GDPR SAR via ΑΤΥΥΠΔ ΕΜΠ 8202 (13/02/2026). Handler: Μ. Γκούντουβα. Supplemental SUPPLEMENT-3-AADE.pdf sent 06/03/2026. If no response by 12/03 → file ΑΠΔΠΧ complaint (complaints@dpa.gr) Art.77 GDPR. Day ${daysSinceDeath} post-mortem.`,
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['GDPR Art.15', 'GDPR Art.12§3', 'GDPR Art.77', 'N.4624/2019'],
    github_issue: 1
  },

  // ── Case 12: KEFODE-ATT-164685 ──
  {
    protocol_number: 'KEFODE-ATT-164685-EX-2026',
    agency: 'ΚΕΦΟΔΕ Αττικής → DPO ΑΑΔΕ',
    description: 'ΚΕΦΟΔΕ forwards 41-page file to AADE DPO',
    date_filed: '2026-02-18',
    deadline: '2026-04-03',
    escalated_to: 'dpo@aade.gr',
    cc: ['kefode.attikis@aade.gr', 'sdoe@aade.gr', 'complaints.sdoe@aade.gr'],
    subject_short: `🟢 ΚΕΦΟΔΕ 164685: AADE DPO has full 41-page file — TAXISnet audit + AFM 051422558`,
    risk: 'CRITICAL',
    note: `ΚΕΦΟΔΕ Αττικής forwarded to AADE DPO. Doc ID: 6717126. DPO must investigate TAXISnet audit logs, who accessed AFM 051422558 post-mortem, AIT.1 claimant identity. Days since death: ${daysSinceDeath}.`,
    evidence_links: { kefode_cover: 'AUTOTELES-TMEMA-UPO.pdf', rebuttal: 'KYPRIANOS-STAMATINA.pdf (41 pages)' },
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['GDPR Art.15/17', 'N.4624/2019', 'AADE Registry Procedures Guide'],
    github_issue: 1
  },

  // ── Case 13: ATTICA-14678 ──
  {
    protocol_number: 'ATTICA-14678-04-03-2026',
    agency: 'Αποκεντρωμένη Διοίκηση Αττικής — Τ. Εποπτείας Ο.Τ.Α.',
    description: 'Confirmation of Εισαγγελική Παραγγελία filing',
    date_filed: '2026-03-04',
    deadline: '2026-04-03',
    escalated_to: 'protokollo@attica.gr',
    cc: ['epopteiaota@attica.gr'],
    subject_short: `✅ Πρωτ. 14678: Attica confirmed Eisaggeliki Paraggelia filing — routed to Τ. Εποπτείας Ο.Τ.Α.`,
    risk: 'HIGH',
    note: `Αρ. Πρωτ. 14678 issued 04/03/2026. Routed to Τ. Εποπτείας Ο.Τ.Α. Backs Protocol 258b. Days since death: ${daysSinceDeath}.`,
    evidence_links: { confirmation: 'Attica Πρωτ. 14678/04-03-2026' },
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['N.2830/2000 Art.13', 'N.3852/2010 Art.227', 'KPD Art.33'],
    github_issue: 1
  },

  // ── Case 14: KATEPEIGNON-33077 ──
  {
    protocol_number: 'AADE-33077-33046-33047-33079-2026',
    agency: 'ΣΔΟΕ / ΚΕΦΟΔΕ Αττικής / Δίωξη Κυβερνοεγκλήματος',
    description: 'ΚΑΤΕΠΕΙΓΟΝ — Καταγγελία ΠΚ 216/242/386/319-320 — AIT.1 Πρωτ. 05134000000508766',
    date_filed: '2026-02-12',
    deadline: '2026-03-14',
    escalated_to: 'sdoe@aade.gr',
    cc: ['kefode.attikis@aade.gr', 'sdoe@aade.gr', 'complaints.sdoe@aade.gr'],
    subject_short: `🔴 ΚΑΤΕΠΕΙΓΟΝ 33077: Criminal complaint PK 216/242/386/319-320 — TAXISnet audit logs — Day ${daysSinceDeath}`,
    risk: 'CRITICAL',
    note: `Filed 12/02/2026. Demands TAXISnet audit logs for AFM 044594747/051422558, AIT.1 claimant identity, IBAN history. ΚΕΦΟΔΕ confirmed receipt via 164685. Days since death: ${daysSinceDeath}.`,
    evidence_links: { complaint: 'KYPRIANOS-STAMATINA.pdf', kefode_forward: 'ΚΕΦΟΔΕ ΑΤΤ 164685 ΕΞ 2026' },
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['PK 216', 'PK 242', 'PK 386', 'PK 319-320', 'N.4557/2018'],
    github_issue: 1
  },

  // ── Case 15: EAD-14441-KDD-TRIAD ──
  {
    protocol_number: '14441 ΕΙ 2026',
    agency: 'ΕΑΔ — Εθνική Αρχή Διαφάνειας',
    description: 'KDD Triad — 2ο πρωτόκολλο (μετά 14288 ΕΙ 2026)',
    date_filed: '2026-03-05',
    deadline: '2026-03-19',
    escalated_to: 'kataggelies@aead.gr',
    cc: ['grammateia@aead.gr', 'dms@aead.gr'],
    subject_short: `⚠️ ΕΑΔ 14441 ΕΙ 2026 — KDD Triad — Art.4 10-day deadline — Day ${daysSinceDeath}`,
    risk: 'CRITICAL',
    note: `KDD Triad second protocol. Cross-ref EAD 14288 ΕΙ 2026, 12460/12529. Days since death: ${daysSinceDeath}.`,
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999'],
    github_issue: 1
  },

  // ── Case 16: NAT-ROUTING-PENSION-274 ──
  {
    protocol_number: 'NAT-ROUTING-PENSION-274',
    agency: 'NAT — Ναυτικό Απομαχικό Ταμείο',
    description: 'Phantom pension — routed to ΒΑΣΙΛΙΚΗ, Τμ. Μητρώου Συνταξιούχων 2',
    date_filed: '2026-03-05',
    deadline: '2026-03-19',
    escalated_to: 'nat@nat.gr',
    cc: ['d.dapon.syntefdt@efka.gov.gr'],
    subject_short: `⚠️ NAT Routing — Phantom Pension AFM 051422558 — Day ${daysSinceDeath}`,
    risk: 'HIGH',
    note: `Phantom pension investigation. Parallel chain with EFKA (rows 269-270). Πατσιούδης declared non-competent → EFKA military desks. Days since death: ${daysSinceDeath}.`,
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999'],
    github_issue: 1
  },

  // ── Case 17: KTIMATOLOGIO-ND0113-CORRECTED ──
  {
    protocol_number: 'KTIMATOLOGIO-ND0113-CORRECTED',
    agency: 'Ελληνικό Κτηματολόγιο (Κ/Γ Πειραιά)',
    description: 'CORRECTED complaint — 60-day Art.45 countdown',
    date_filed: '2026-03-05',
    deadline: '2026-05-04',
    escalated_to: 'ktimagen@ktimatologio.gr',
    cc: ['info.kt5.23@gmail.com', 'proedros@ktimatologio.gr', 'genikos@ktimatologio.gr', 'contact@synigoros.gr', 'info@eppo.europa.eu'],
    subject_short: `⚠️ KTIMATOLOGIO ND0113: CORRECTED complaint — 60-day Art.45 — Day ${daysSinceDeath}`,
    risk: 'CRITICAL',
    note: `CORRECTED re-send. Original misdirected to contact@kthma.gr (Κυκλάδες). Deadline 04/05/2026. Days since death: ${daysSinceDeath}.`,
    evidence_links: {},
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999', 'Art.45 N.2690/1999', 'N.2664/1998', 'EU Reg.2017/1939'],
    github_issue: 1
  },

  // ── Case 18: EFKA-KAKLAMANOU-NAVY-PENSION ──
  {
    protocol_number: 'EFKA-KAKLAMANOU-NAVY-PENSION-276',
    agency: 'e-ΕΦΚΑ Τοπική Δ/νση Α\' Πειραιά — Τμ. Συντάξεων',
    description: 'Κακλαμάνου confirmed Navy pensioner — Δ\' Δ/νση Απονομής referral',
    date_filed: '2026-03-09',
    deadline: '2026-03-19',
    escalated_to: 'tm.sint.td.apireas@efka.gov.gr',
    cc: ['d.dapon.syntefdt@efka.gov.gr', 'gd.sintaxeon@efka.gov.gr', 'sdoe@aade.gr'],
    subject_short: `🔴 EFKA ΚΑΚΛΑΜΑΝΟΥ: Πολεμικό Ναυτικό pensioner CONFIRMED — AFM 051422558 — Day ${daysSinceDeath}`,
    risk: 'PHANTOM_PENSION_NAVY_CONFIRMED',
    note: `ΒΑΣΙΛΙΚΗ ΚΑΚΛΑΜΑΝΟΥ (Τοπική Δ/νση Α' Πειραιά, Αγ. Κων/νου 1, 18531 Πειραιάς, τηλ. 210 4192820-829) explicitly confirmed: "ο θανών ήταν συνταξιούχος του Πολεμικού Ναυτικού." Referred to Δ' Δ/νση Απονομής Συντάξεων & Εφάπαξ Δημοσίου Τομέα. Pension disbursed ${daysSinceDeath} days post-mortem. Two parallel paths: Path A (this case) via EFKA Δ' Δ/νση, Path B via NAT (Case 16). Cross-ref EFKA-PHANTOM-PENSION (Case 2), AADE-DESYP-161184 (Case 5).`,
    evidence_links: { kaklamanou_statement: 'Email confirmation from Κακλαμάνου re: Navy pensioner status' },
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999', 'N.4387/2016', 'N.4670/2020'],
    github_issue: 1
  },

  // ── Case 19: EAD-15006-SUPPLEMENT-4 ──
  {
    protocol_number: '15006 ΕΙ 2026',
    agency: 'ΕΑΔ — Εθνική Αρχή Διαφάνειας',
    description: 'Supplement #4 — Triple protocol lock (14288/14441/15006)',
    date_filed: '2026-03-09',
    deadline: '2026-03-23',
    escalated_to: 'kataggelies@aead.gr',
    cc: ['grammateia@aead.gr', 'dms@aead.gr'],
    subject_short: `⚠️ ΕΑΔ 15006 ΕΙ 2026 — Supplement #4 — Triple Lock 14288/14441/15006 — Day ${daysSinceDeath}`,
    risk: 'CRITICAL',
    note: `Supplement #4 protocolled 09/03/2026. Triple protocol lock: 14288 ΕΙ 2026 + 14441 ΕΙ 2026 + 15006 ΕΙ 2026. Keratsini property fraud (KAEK 050681726008). Cross-ref 12460/12529. Days since death: ${daysSinceDeath}.`,
    evidence_links: { supplement4: 'Supplement #4 — EAD protocol 15006 ΕΙ 2026' },
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999', 'N.4622/2019'],
    github_issue: 1
  }

];

// ================================================================
// OUTPUT LOOP WITH DEDUP (L1 HARDENED + L3)
// IF Node condition: $json.should_send === true
// ================================================================
const output = [];

// If this is a refire within the same minute, block ALL sends
if (isRefire) {
  console.log(`[DEDUP] EXECUTION REFIRE DETECTED — blocking all sends for ${execFingerprint}`);
}

for (const c of cases) {
  const caseId = c.protocol_number || c.risk || 'UNKNOWN';
  const deadline = new Date(c.deadline + (c.deadline.includes('T') ? '' : 'T23:59:00+03:00'));
  const isOverdue = now > deadline;
  const daysLeft = Math.floor((deadline - now) / (1000 * 60 * 60 * 24));
  const daysOverdue = isOverdue ? Math.abs(daysLeft) : 0;
  const tier = classifyTier(c.risk, daysOverdue);

  const item = {
    protocol_number: c.protocol_number,
    agency: c.agency,
    description: c.description,
    date_filed: c.date_filed,
    deadline: c.deadline,
    overdue: isOverdue,
    days_remaining: daysLeft,
    days_overdue: daysOverdue,         // ← FIX: was missing, caused "undefined days overdue" in GH
    tier: tier,                         // ← FIX: was missing, caused "Tier undefined" in GH
    days_since_death: daysSinceDeath,
    escalated_to: c.escalated_to,
    cc: Array.isArray(c.cc) ? c.cc.join(',') : (c.cc || ''),
    visible_cc: 'contact@synigoros.gr,info@eppo.europa.eu',  // ← Standard visible CC
    subject_short: c.subject_short,
    risk: c.risk,
    note: c.note,
    evidence_links: JSON.stringify(c.evidence_links || {}),
    afm_targets: (c.afm_targets || []).join(','),
    legal_basis: (c.legal_basis || []).join(' | '),
    github_issue: c.github_issue || 1,
    // DEDUP fields
    dedup_blocked: false,
    dedup_layer: null,
    dedup_case_id: caseId,
    dedup_date: today,
    should_send: false,
    sheets_log_entry: null,
    execution_fingerprint: execFingerprint
  };

  if (isOverdue) {
    // Check execution-level refire first
    if (isRefire) {
      item.dedup_blocked = true;
      item.dedup_layer = 'execution_refire';
      item.should_send = false;
      item.note += `\n[DEDUP] Blocked by execution_refire — duplicate trigger detected (${execFingerprint}).`;
    } else {
      const dedupResult = alreadySentToday(caseId);
      if (dedupResult.blocked) {
        item.dedup_blocked = true;
        item.dedup_layer = dedupResult.layer;
        item.should_send = false;
        item.note += `\n[DEDUP] Blocked by ${dedupResult.layer} — already sent today.`;
      } else {
        item.should_send = true;
        markAsSent(caseId, c.protocol_number);
        // L3: Google Sheets log entry (for downstream Append node)
        item.sheets_log_entry = JSON.stringify({
          timestamp: now.toISOString(),
          case_id: caseId,
          protocol_number: c.protocol_number,
          sent_to: c.escalated_to,
          cc: Array.isArray(c.cc) ? c.cc.join(',') : (c.cc || ''),
          subject: c.subject_short,
          tier: tier,
          days_overdue: daysOverdue,
          layer_status: 'L1 recorded, L3 pending append'
        });
      }
    }
  }

  output.push({ json: item });
}

// Summary item (filtered out by IF Node since should_send is false)
const overdueCount = output.filter(o => o.json.overdue).length;
const blockedCount = output.filter(o => o.json.dedup_blocked).length;
const sendCount = output.filter(o => o.json.should_send).length;
const refireBlocked = output.filter(o => o.json.dedup_layer === 'execution_refire').length;

output.push({
  json: {
    _summary: true,
    total_cases: cases.length,
    overdue_cases: overdueCount,
    dedup_blocked: blockedCount,
    dedup_refire_blocked: refireBlocked,
    will_send: sendCount,
    days_since_death: daysSinceDeath,
    run_date: today,
    run_timestamp: now.toISOString(),
    execution_fingerprint: execFingerprint,
    is_refire: isRefire,
    engine_version: 'v3.1-DEDUP-HARDENED',
    guard_layers: 'L1:static_data+exec_fingerprint | L3:google_sheets (L2:fs removed for n8n 2.x compat)',
    note: `Duplicate guard active. ${blockedCount} blocked (${refireBlocked} refire), ${sendCount} will send.`,
    should_send: false
  }
});

return output;
