// Check Status + Parse — v2.4-EFKA-419690-REPLY
// Last updated: 2026-03-04
// Added: EFKA-419690-REPLY (Case 10) — Reply to ΑΠ 419690/03-03-2026 with identification docs
// Total tracked protocols: 261

const now = new Date();

// Days since John Kyprianou's death (2021-06-13)
const deathDate = new Date('2021-06-13T00:00:00+03:00');
const daysSinceDeath = Math.floor((now - deathDate) / (1000 * 60 * 60 * 24));

function daysRemaining(deadline) {
  const dl = new Date(deadline);
  return Math.ceil((dl - now) / (1000 * 60 * 60 * 24));
}

// ──────────────────────────────────────────
// Protocol cases array
// ──────────────────────────────────────────
const cases = [

  // ── Case 1: AEAD-5995-EI-2026 ──
  {
    protocol_number: 'AEAD-5995-EI-2026',
    agency: 'AEAD',
    submitted_date: '2026-02-12',
    deadline: '2026-03-03T23:59:00+02:00',
    days_remaining: daysRemaining('2026-03-03T23:59:00+02:00'),
    overdue: now > new Date('2026-03-03T23:59:00+02:00'),
    escalated_to: 'kataggelies@aead.gr',
    cc: ['grammateia@aead.gr', 'dms@aead.gr'],
    subject_short: '⚠️ ΟΧΛΗΣΗ — Πρωτ. 5995 ΕΙ 2026 — Υπέρβαση 19ήμερης προθεσμίας',
    risk: 'CRITICAL',
    note: 'Art.4 N.2690/1999 — 19-day statutory deadline expired. Auto-rejection imminent.'
  },

  // ── Case 2: EFKA-PHANTOM-PENSION ──
  {
    protocol_number: 'EFKA-PHANTOM-PENSION',
    agency: 'EFKA',
    submitted_date: '2026-03-02',
    deadline: '2026-03-16T23:59:00+02:00',
    days_remaining: daysRemaining('2026-03-16T23:59:00+02:00'),
    overdue: now > new Date('2026-03-16T23:59:00+02:00'),
    escalated_to: 'protocol@efka.gov.gr',
    cc: ['sdoe@aade.gr', 'gd.sintaxeon@efka.gov.gr'],
    subject_short: `⚠️ PHANTOM PENSION — AFM 051422558 — Day ${daysSinceDeath} post-mortem — KDD Art.4`,
    risk: 'PHANTOM_PENSION_HIGH',
    note: `Hellenic Navy veteran pension likely disbursed ${daysSinceDeath} days post-mortem. NAT bilateral agreement with US SSA requires cross-check.`
  },

  // ── Case 3: MINDIGITAL-5447-EI-2026 ──
  {
    protocol_number: 'MINDIGITAL-5447-EI-2026',
    agency: 'MinDigital',
    submitted_date: '2026-02-06',
    deadline: '2026-03-06T23:59:00+02:00',
    days_remaining: daysRemaining('2026-03-06T23:59:00+02:00'),
    overdue: now > new Date('2026-03-06T23:59:00+02:00'),
    escalated_to: 'minister@mindigital.gr',
    cc: ['grammateia@mindigital.gr'],
    subject_short: '⚠️ ΟΧΛΗΣΗ — Πρωτ. 5447 ΕΙ 2026 — MinDigital deadline breach',
    risk: 'HIGH',
    note: 'Original Feb 21 deadline passed. New March 6 deadline. ΣΗΔΕ 22421920 forwarded by Deputy Minister to Ktimatologio proedros/genikos.'
  },

  // ── Case 4: KTIMATOLOGIO-ND0113 ──
  {
    protocol_number: 'KTIMATOLOGIO-ND0113',
    agency: 'Ktimatologio',
    submitted_date: '2026-02-04',
    deadline: '2026-03-02T23:59:00+02:00',
    days_remaining: daysRemaining('2026-03-02T23:59:00+02:00'),
    overdue: true,
    escalated_to: 'contact@kthma.gr',
    cc: ['kataggelies@aead.gr'],
    subject_short: '⚠️ ΟΧΛΗΣΗ — ND0113/26/06549 — Ktimatologio non-response',
    risk: 'HIGH',
    note: 'ND0113/26/06549 overdue 26+ days. Ticket 4384023 active harassment documentation.'
  },

  // ── Case 5: AADE-DESYP-161184 (NAT Phantom Pension) ──
  {
    protocol_number: 'AADE-DESYP-161184',
    agency: 'AADE-DESYP',
    submitted_date: '2026-03-02',
    deadline: '2026-03-17T23:59:00+02:00',
    days_remaining: daysRemaining('2026-03-17T23:59:00+02:00'),
    overdue: now > new Date('2026-03-17T23:59:00+02:00'),
    escalated_to: 'grammateia@aade.gr',
    cc: ['sdoe@aade.gr', 'gd.sintaxeon@efka.gov.gr'],
    subject_short: `⚠️ ΔΕΣΥΠ Γ 161184 — NAT Phantom Pension — Day ${daysSinceDeath} — AFM 051422558`,
    risk: 'PHANTOM_PENSION_DESYP',
    note: `NAT phantom pension complaint. ${daysSinceDeath} days since death. Cross-ref EFKA-2024-00147, NAT bilateral US-Greece.`
  },

  // ── Case 6: DED-33123-2026 (120-day appeal) ──
  {
    protocol_number: 'DED-33123-2026',
    agency: 'DED',
    submitted_date: '2026-02-14',
    deadline: '2026-06-14T23:59:00+03:00',
    days_remaining: daysRemaining('2026-06-14T23:59:00+03:00'),
    overdue: now > new Date('2026-06-14T23:59:00+03:00'),
    escalated_to: 'ded@aade.gr',
    cc: ['grammateia@aade.gr'],
    subject_short: '⚠️ ΔΕΔ 33123/2026 — 120-day appeal deadline',
    risk: 'HIGH',
    note: '120-day appeal window from 14/02/2026. Auto-escalate to Διοικητικά Δικαστήρια if no decision.'
  },

  // ── Case 7: EISAGGELIKI-PARAGGELIA-258b ──
  {
    protocol_number: 'EISAGGELIKI-PARAGGELIA-258b',
    agency: 'Εισαγγελία Πειραιά',
    submitted_date: '2026-03-03',
    deadline: '2026-04-02T23:59:00+03:00',
    days_remaining: daysRemaining('2026-04-02T23:59:00+03:00'),
    overdue: now > new Date('2026-04-02T23:59:00+03:00'),
    escalated_to: 'eispeira@otenet.gr',
    cc: ['sdoe@aade.gr', 'Athens.Office@eppo.europa.eu'],
    subject_short: `⚠️ ΕΙΣΑΓΓΕΛΙΚΗ ΠΑΡΑΓΓΕΛΙΑ 258b — Αρθ.13 Ν.2830/2000 — Αποκάλυψη 6020/2015 — Day ${daysSinceDeath}`,
    risk: 'CRITICAL',
    note: `Eisaggeliki Paraggelia for disclosure of deed 6020/2015 by Notary Lyrakis. 16 attachments. Protocol mismatch 166 vs 136. Day ${daysSinceDeath} since death. Cross-ref EPPO PP.00179/PP.00267/PP.00281/PP.00310.`
  },

  // ── Case 8: ATTICA-FORWARD-258b ──
  {
    protocol_number: 'ATTICA-FORWARD-258b',
    agency: 'Αποκεντρωμένη Διοίκηση Αττικής',
    submitted_date: '2026-03-03',
    deadline: '2026-04-02T23:59:00+03:00',
    days_remaining: daysRemaining('2026-04-02T23:59:00+03:00'),
    overdue: now > new Date('2026-04-02T23:59:00+03:00'),
    escalated_to: 'protokollo@attica.gr',
    cc: ['epopteiaota@attica.gr'],
    subject_short: '⚠️ Συμπληρωματική Ενημέρωση — Πρωτ. 11494/11676 — Lyrakis Denial Evidence',
    risk: 'HIGH',
    note: 'Forward of Lyrakis denial (Prot. 207/26-02-2026) + protocol mismatch evidence to Attica Admin.'
  },

  // ── Case 9: SYNIGOROS-258-MISMATCH ──
  {
    protocol_number: 'SYNIGOROS-258-MISMATCH',
    agency: 'Συνήγορος του Πολίτη',
    submitted_date: '2026-03-03',
    deadline: '2026-03-17T23:59:00+02:00',
    days_remaining: daysRemaining('2026-03-17T23:59:00+02:00'),
    overdue: now > new Date('2026-03-17T23:59:00+02:00'),
    escalated_to: 'contact@synigoros.gr',
    cc: ['Athens.Office@eppo.europa.eu'],
    subject_short: '⚠️ Protocol Mismatch 166/136 — GDPR Misuse — Notary Obstruction',
    risk: 'HIGH',
    note: 'Synigoros complaint re: administrative obstruction (Lyrakis denial), protocol mismatch 166 vs 136. Cross-ref EPPO PP.00179.'
  },

  // ── Case 10: EFKA-419690-REPLY (NEW — v2.4) ──
  {
    protocol_number: 'EFKA-419690-REPLY',
    agency: 'e-ΕΦΚΑ Δ/νση Διευθέτησης Αναφορών',
    submitted_date: '2026-03-03',
    deadline: '2026-03-16T23:59:00+02:00',
    days_remaining: daysRemaining('2026-03-16T23:59:00+02:00'),
    overdue: now > new Date('2026-03-16T23:59:00+02:00'),
    escalated_to: 'contact@synigoros.gr',
    cc: Array.isArray(['report@eppo.europa.eu', 'tm.anaf.asf@efka.gov.gr']) ? ['report@eppo.europa.eu', 'tm.anaf.asf@efka.gov.gr'] : [],
    subject_short: `⚠️ EFKA ΑΠ 419690 — Ταυτοποίηση Reply — Art.4 KDD 10-day — Day ${daysSinceDeath} post-mortem`,
    risk: 'EFKA_419690_REPLY',
    note: `Reply to ΑΠ 419690/03-03-2026 (κα Ντόκου). Sent identification (Α)(Β)(Γ) + Υπεύθυνη Δήλωση gov.gr + death cert Apostille. 10 εργάσιμες Art.4 KDD deadline 16/03/2026. Auto-escalate to Συνήγορος + EPPO if silent. Cross-ref ΔΕΣΥΠ Γ 87848, ΥΕΘΑ, Cybercrime 568/10/2673, EPPO PP.00179. Day ${daysSinceDeath} since death of John Kyprianos (AFM 051422558).`
  }

];

// ──────────────────────────────────────────
// Return items for downstream nodes
// ──────────────────────────────────────────
return cases.map(c => ({ json: c }));