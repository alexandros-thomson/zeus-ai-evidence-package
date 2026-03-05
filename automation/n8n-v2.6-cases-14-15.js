// ============================================================
// n8n Code Node UPDATE — v2.6
// Cases 14-15: EAD-14441-KDD-TRIAD + NAT-ROUTING-PENSION
// Paste AFTER existing Case 13 in the cases[] array
// Total tracked cases after update: 15
// ============================================================

// --- Case 14: EAD 14441 — KDD Triad Second Protocol ---
{
  id: "EAD-14441-KDD-TRIAD",
  protocol_number: "14441 ΕΙ 2026",
  agency: "ΕΑΔ — Εθνική Αρχή Διαφάνειας (Κεντρικό Πρωτόκολλο)",
  description: "KDD Triad — Πλαστογραφία Κτηματολογίου & Ψηφιακή Παραποίηση — 2ο πρωτόκολλο (μετά 14288 ΕΙ 2026)",
  filed: "2026-03-05",
  deadline: "2026-03-19",
  legalBasis: "Art. 4 ΚΔΔ (Ν.2690/1999) — 10 εργάσιμες ημέρες",
  status: "PENDING",
  to: ["dms@aead.gr", "kataggelies@aead.gr"],
  cc: ["grammateia@aead.gr"],
  escalateTo: [
    "contact@synigoros.gr",
    "report@eppo.europa.eu"
  ],
  crossRefs: [
    "EAD 14288 ΕΙ 2026 (1st KDD protocol)",
    "EAD 12460/12529 ΕΙ 2026 (nuclear triad)",
    "KAEK 050681726008",
    "ΔΕΣΥΠ Γ 87848",
    "EPPO PP.00179/2026/EN"
  ],
  trackerRow: 273,
  daysSinceDeath: 1726
},

// --- Case 15: NAT Internal Routing — Τμήμα Μητρώου Συνταξιούχων 2 ---
{
  id: "NAT-ROUTING-PENSION-274",
  protocol_number: "NAT Internal Routing (Τμ. Μητρώου Συνταξιούχων 2)",
  agency: "NAT — Ναυτικό Απομαχικό Ταμείο / Δ/νση Παροχών ΝΑΤ",
  description: "Phantom pension investigation — Routed to ΒΑΣΙΛΙΚΗ, Τμήμα Μητρώου Συνταξιούχων 2 + Δ/νση Παροχών ΝΑΤ — Παράλληλη αλυσίδα με EFKA (rows 269-270)",
  filed: "2026-03-05",
  deadline: "2026-03-19",
  legalBasis: "Art. 4 ΚΔΔ (Ν.2690/1999) — 10 εργάσιμες ημέρες | Phantom pension on AFM 051422558 since 13/06/2021",
  status: "PENDING",
  to: ["nat@nat.gr"],
  cc: [],
  escalateTo: [
    "contact@synigoros.gr",
    "report@eppo.europa.eu",
    "d.dapon.syntefdt@efka.gov.gr"
  ],
  crossRefs: [
    "EFKA ΑΠ 419690 → 434147 (parallel EFKA chain)",
    "EFKA routing: Παπαναγιώτου → Στάμου → Δ' Δ/νση Απονομής Συντάξεων",
    "ΔΕΣΥΠ Γ 87848",
    "ΥΕΘΑ 03-03-2026 (Ταξίαρχος Τσελεπίδου)",
    "EPPO PP.00179/2026/EN"
  ],
  trackerRow: 274,
  daysSinceDeath: 1726
}

// ============================================================
// PASTE INSTRUCTIONS:
// 1. Open localhost:5678/workflow/8tFYcHI7qW062BZV
// 2. Open Code node
// 3. Find the cases[] array — locate Case 13 (last entry)
// 4. Paste these two objects AFTER Case 13, inside the array
// 5. Update the comment at top: "v2.6 — 15 cases"
// 6. Verify both cases appear in output
//
// KEY POINTS:
// - Both deadlines: 2026-03-19 (10 business days from 05/03)
// - NAT escalation includes EFKA pension desk (d.dapon.syntefdt@efka.gov.gr)
//   as CC — connecting the two parallel pension chains
// - EAD escalation to Συνήγορος + EPPO (standard pattern)
// - Field name: protocol_number (not protocol) — matches Set node downstream
// ============================================================
