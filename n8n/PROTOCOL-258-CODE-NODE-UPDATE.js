// ================================================================
// n8n Code Node Update — Protocol 258 (Lyrakis Denial Response)
// Add to "Check Status + Parse" node in workflow 8tFYcHI7qW062BZV
// Version: v2.3-PROTOCOL-258
// Date: 2026-03-03
// ================================================================
// PASTE THESE 4 CASES INTO YOUR EXISTING cases ARRAY:

  // Case 258a: Notarial Association Response
  {
    protocol_number: 'NOTARIAL-SYLLOGOS-207-2026',
    agency: 'Συμβολαιογραφικός Σύλλογος Εφετείων',
    description: 'Πρωτ. 207/26-02-2026 — Απάντηση Λυράκη',
    date_filed: '2026-02-26',
    deadline: '2026-03-17',
    escalated_to: 'notaries@notariat.gr',
    cc: ['contact@synigoros.gr', 'info@eppo.europa.eu'],
    risk: 'CRITICAL',
    note: 'Protocol mismatch 166/136 + Deed 6020 conflict + GDPR shield + SLAPP threat',
    legal_basis: ['N.2830/2000 Art.13', 'GDPR Art.6(1)(f)', 'PK 367§1'],
    github_issue: 1
  },

  // Case 258b: Eisaggeliki Paraggelia
  {
    protocol_number: 'EISAGGELIKI-PARAGGELIA-PIRAEUS-LYRAKIS',
    agency: 'Εισαγγελία Πρωτοδικών Πειραιώς',
    description: 'Αίτηση εξέτασης αρχείου Λυράκη — πράξη 6020 — KAEK 050681726008',
    date_filed: '2026-03-03',
    deadline: '2026-04-02',
    escalated_to: 'eisaggeleas@protodikeio-piraeus.gr',
    cc: ['sdoe@aade.gr', 'info@eppo.europa.eu'],
    risk: 'CRITICAL',
    note: 'Lyrakis acknowledges compliance only with prosecutorial order',
    legal_basis: ['KPD Art.33', 'N.2830/2000 Art.13', 'PK 216', 'PK 386-387'],
    github_issue: 1
  },

  // Case 258c: Synigoros tou Politi
  {
    protocol_number: 'SYNIGOROS-PROTOCOL-258',
    agency: 'Συνήγορος του Πολίτη',
    description: 'GDPR abuse + SLAPP threat + Syllogos failure',
    date_filed: '2026-03-03',
    deadline: '2026-04-17',
    escalated_to: 'contact@synigoros.gr',
    cc: ['info@eppo.europa.eu'],
    risk: 'HIGH',
    note: 'Connected to Protocol 221 (prior filing)',
    legal_basis: ['N.3094/2003', 'N.2830/2000 Art.13', 'GDPR Art.6(1)(f)'],
    github_issue: 1
  },

  // Case 258d: EPPO + EAD Supplemental
  {
    protocol_number: 'EPPO-EAD-LYRAKIS-SUPPLEMENT',
    agency: 'EPPO + EAD',
    description: 'Supplemental: Lyrakis denial + protocol mismatch + GDPR shield',
    date_filed: '2026-03-03',
    deadline: '2026-03-17',
    escalated_to: 'info@eppo.europa.eu',
    cc: ['dms@aead.gr', 'sdoe@aade.gr'],
    risk: 'NORMAL',
    note: 'New investigative leads from Lyrakis response for PP.00179 + EAD 12460/12529',
    legal_basis: ['EPPO Reg. 2017/1939', 'N.4557/2018', 'PK 386-387'],
    github_issue: 1
  },