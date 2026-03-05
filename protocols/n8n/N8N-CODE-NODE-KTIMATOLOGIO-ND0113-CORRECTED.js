// ================================================================
// n8n Code Node Update — KTIMATOLOGIO-ND0113 CORRECTED COMPLAINT
// Add to "Check Status + Parse" node in workflow 8tFYcHI7qW062BZV
// Version: v2.7-KTIMATOLOGIO-CORRECTED
// Date: 2026-03-05
// ================================================================
//
// INSTRUCTIONS:
// 1. Open http://localhost:5678/workflow/8tFYcHI7qW062BZV
// 2. Double-click the "Check Status + Parse" Code node
// 3. Find the existing `cases` array
// 4. Add this case object BEFORE the closing `];`
// 5. ALSO: Find any existing case referencing contact@kthma.gr
//    and update it to ktimagen@ktimatologio.gr
// 6. Save node, then Save workflow
// 7. Test manually to verify 16 cases output
//
// NEW CASE TO ADD:
// ================================================================

  {
    protocol_number: 'KTIMATOLOGIO-ND0113-CORRECTED',
    agency: 'Ελληνικό Κτηματολόγιο (Κ/Γ Πειραιά + Γ.Δ. + Πρόεδρος + Γ. Διευθυντής)',
    description: 'ΔΙΟΡΘΩΜΕΝΗ ΚΑΤΑΓΓΕΛΙΑ Άρθρου 4 ΚΔΔ — Corrected routing',
    date_filed: '2026-03-05',
    deadline: '2026-05-04',
    overdue: new Date() > new Date('2026-05-04T23:59:00+03:00'),
    days_remaining: Math.floor((new Date('2026-05-04T23:59:00+03:00') - now) / (1000 * 60 * 60 * 24)),
    escalated_to: 'ktimagen@ktimatologio.gr',
    cc: ['info.kt5.23@gmail.com', 'proedros@ktimatologio.gr', 'genikos@ktimatologio.gr', 'contact@synigoros.gr', 'info@eppo.europa.eu'],
    subject_short: 'KTIMATOLOGIO ND0113: CORRECTED complaint — 60-day Art.45 countdown',
    risk: 'CRITICAL',
    note: 'CORRECTED re-send. Original misdirected to contact@kthma.gr (Κυκλάδες). Now sent to 4 correct emails. Deadline 04/05/2026. Days since death: ' + daysSinceDeath,
    afm_targets: ['044594747', '051422558'],
    legal_basis: ['Art.4 N.2690/1999', 'Art.45 N.2690/1999', 'N.2664/1998', 'EU Reg.2017/1939'],
    github_issue: 1
  },

// EMAIL CORRECTION: contact@kthma.gr -> ktimagen@ktimatologio.gr in all cases
// Total cases after adding: 16
