// ================================================================
// n8n Code Node Update — ΚΕΦΟΔΕ 164685 + Protocol 14678
// Add to "Check Status + Parse" node in workflow 8tFYcHI7qW062BZV
// Version: v2.5-KEFODE-164685
// Date: 2026-03-04
// ================================================================
// 
// INSTRUCTIONS:
// 1. Open http://localhost:5678/workflow/8tFYcHI7qW062BZV
// 2. Double-click the "Check Status + Parse" Code node
// 3. Find the existing `cases` array
// 4. Add these 3 new case objects BEFORE the closing `];`
// 5. Save node, then Save workflow
// 6. Test manually to verify 269+ items output
//
// NEW CASES TO ADD (paste inside the cases array):
// ================================================================

  // ── ΚΕΦΟΔΕ 164685: AADE DPO Forwarding (INBOUND) ─────────────
  {
    protocol_number: 'KEFODE-ATT-164685-EX-2026',
    agency: 'ΚΕΦΟΔΕ Αττικής → DPO ΑΑΔΕ (dpo@aade.gr)',
    description: 'ΕΙΣΕΡΧΟΜΕΝΟ — ΔΙΑΒΙΒΑΣΗ ΕΓΓΡΑΦΟΥ — ΚΕΦΟΔΕ forwards 41-page rebuttal/complaint to Αυτοτελές Τμήμα Υποστήριξης Υπεύθυνου Προστασίας Δεδομένων ΑΑΔΕ',
    date_filed: '2026-02-18',
    deadline: '2026-04-03',
    overdue: new Date() > new Date('2026-04-03T23:59:00+02:00'),
    days_remaining: Math.floor((new Date('2026-04-03T23:59:00+02:00') - now) / (1000 * 60 * 60 * 24)),
    escalated_to: 'dpo@aade.gr',
    cc: ['kefode.attikis@aade.gr', 'sdoe@aade.gr', 'complaints.sdoe@aade.gr'],
    subject_short: `🟢 ΚΕΦΟΔΕ 164685: AADE DPO now has full 41-page file — TAXISnet audit + AFM 051422558 post-mortem access`,
    risk: 'CRITICAL',
    note: `ΚΕΦΟΔΕ Αττικής (Μαρίνα Δρυμαλίτου) forwarded complete file to AADE Data Protection Officer. Doc ID: 6717126. Issued 18/02/2026, delivered 03/03/2026, digitally signed 04/03/2026 08:12 by Vasiliki Magkou. File contains: (1) 10-page gov.gr certified REBUTTAL to Protocol 214142 (dAf3e-syqtUEeg-vkKR69w), (2) ΚΑΤΕΠΕΙΓΟΝ complaint Πρωτ. 33077/33046/33047/33079/2026 — PK 216/242/386/319-320. DPO must investigate: TAXISnet audit logs, who accessed AFM 051422558 post-mortem, AIT.1 claimant identity. If no DPO response by deadline → escalate to ADAE. Contact: Αγγελική Βοΐλα, 213 141 1443, kefode.attikis@aade.gr. Days since death: ${daysSinceDeath}.`,
    evidence_links: {
      kefode_cover: 'AUTOTELES-TMEMA-UPO.pdf',
      rebuttal: 'KYPRIANOS-STAMATINA.pdf (41 pages)',
      tracker: 'MASTER-PROTOCOL-TRACKER entries 257-259'
    },
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['GDPR Art.15/17', 'N.4624/2019', 'AADE Registry Procedures Guide', 'PK 216/242/386'],
    github_issue: 1
  },

  // ── Protocol 14678: Αποκεντρωμένη Διοίκηση Αττικής Confirmation (INBOUND) ──
  {
    protocol_number: 'ATTICA-14678-04-03-2026',
    agency: 'Αποκεντρωμένη Διοίκηση Αττικής — Τ. Εποπτείας Ο.Τ.Α.',
    description: 'ΕΙΣΕΡΧΟΜΕΝΟ — ΒΕΒΑΙΩΣΗ ΚΑΤΑΧΩΡΗΣΗΣ — Αίτηση Εισαγγελικής Παραγγελίας κατ Άρθρο 13 Ν. 2830/2000 — Λυράκη / Σύμβαση 6020',
    date_filed: '2026-03-04',
    deadline: '2026-04-03',
    overdue: new Date() > new Date('2026-04-03T23:59:00+03:00'),
    days_remaining: Math.floor((new Date('2026-04-03T23:59:00+03:00') - now) / (1000 * 60 * 60 * 24)),
    escalated_to: 'protokollo@attica.gr',
    cc: ['epopteiaota@attica.gr'],
    subject_short: `✅ Πρωτ. 14678: Attica confirmed Eisaggeliki Paraggelia filing — routed to Τ. Εποπτείας Ο.Τ.Α.`,
    risk: 'HIGH',
    note: `Αρ. Πρωτ. 14678 issued 04/03/2026 07:35 Athens. 3-hour turnaround. Routed to Τ. Εποπτείας Ο.Τ.Α. (OTA Supervision Section). 10 attachments: Death Certificate, ΔΕΣΥΠ Γ 87848, ND0113 2η Απάντηση, ND0105, KAEK-050681726008-8-Sheets, Ap1-4, Πιστοποιητικό 5771. Connected: Πρωτ. 11494/11676/2026 (existing Attica protocols). Backs Protocol 258b (Εισαγγελία Πρωτοδικών Πειραιώς — deadline 02/04/2026). Days since death: ${daysSinceDeath}.`,
    evidence_links: {
      confirmation: 'Attica Πρωτ. 14678/04-03-2026',
      eisaggeliki: 'Protocol 258b (EISAGGELIKI-258b-EMAIL)',
      tracker: 'MASTER-PROTOCOL-TRACKER entries 253-256'
    },
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['N.2830/2000 Art.13', 'N.3852/2010 Art.227', 'KPD Art.33'],
    github_issue: 1
  },

  // ── ΚΑΤΕΠΕΙΓΟΝ 33077: ΣΔΟΕ/ΚΕΦΟΔΕ/Δίωξη Criminal Complaint (OUTBOUND) ──
  {
    protocol_number: 'AADE-33077-33046-33047-33079-2026',
    agency: 'ΣΔΟΕ / ΚΕΦΟΔΕ Αττικής / Δίωξη Κυβερνοεγκλήματος',
    description: 'ΚΑΤΕΠΕΙΓΟΝ — Καταγγελία ΠΚ 216/242/386/319-320 — Μεταθανάτια χρήση ΑΦΜ 051422558 — AIT.1 Πρωτ. 05134000000508766',
    date_filed: '2026-02-12',
    deadline: '2026-03-14',
    overdue: new Date() > new Date('2026-03-14T23:59:00+02:00'),
    days_remaining: Math.floor((new Date('2026-03-14T23:59:00+02:00') - now) / (1000 * 60 * 60 * 24)),
    escalated_to: 'kataggelies@sdoe.gr',
    cc: ['kefode.attikis@aade.gr', 'ccu@cybercrimeunit.gov.gr', 'sdoe@aade.gr', 'aead@aead.gr'],
    subject_short: `🔴 ΚΑΤΕΠΕΙΓΟΝ 33077: Criminal complaint PK 216/242/386/319-320 — TAXISnet audit logs demanded`,
    risk: 'CRITICAL',
    note: `Filed 12/02/2026 20:36 with 7 attachments. Demands: (1) TAXISnet/myAADE audit logs for AFM 044594747/051422558 from 2011, (2) AIT.1 Πρωτ. 05134000000508766 claimant identity, (3) IBAN history/changes, (4) KAEK cross-reference with 05134000000508766, (5) Written confirmation of receipt. CC: yoikastv@astynomia.gr, Athens.Office@eppo.europa.eu, Ana_Wolken@slotkin.senate.gov. Now confirmed received — ΚΕΦΟΔΕ forwarded to DPO via 164685. Days since death: ${daysSinceDeath}.`,
    evidence_links: {
      complaint: 'KYPRIANOS-STAMATINA.pdf (pages 1-2)',
      kefode_forward: 'ΚΕΦΟΔΕ ΑΤΤ - Τ/Γ1 164685 ΕΞ 2026',
      tracker: 'MASTER-PROTOCOL-TRACKER entry 258'
    },
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['PK 216', 'PK 242', 'PK 386', 'PK 319-320', 'N.4557/2018'],
    github_issue: 1
  },

// ================================================================
// After adding, total case count in Code node: previous + 3
// (258a-d + KEFODE-164685 + ATTICA-14678 + KATEPEIGNON-33077 = +7 since v2.2)
// ================================================================
