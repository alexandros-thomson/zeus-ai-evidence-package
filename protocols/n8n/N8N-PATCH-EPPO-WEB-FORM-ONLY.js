// ================================================================
// n8n Code Node PATCH — EPPO Email Limitation
// Apply to ALL cases in "Check Status + Parse" node
// Workflow: 8tFYcHI7qW062BZV
// Date: 2026-03-05
// ================================================================
//
// CONFIRMED: EPPO auto-reply received 05/03/2026 11:29 AM EST
// from EPPO-Info@eppo.europa.eu stating:
// "Οι ποινικές καταγγελίες που λαμβάνονται σε αυτό το γραμματοκιβώτιο
//  ΔΕΝ ΘΑ ΔΙΕΚΠΕΡΑΙΩΝΟΝΤΑΙ"
//
// INSTRUCTIONS:
// Add this constant after `const now = new Date();` in Code node:
// ================================================================

const EPPO_NOTE = '⚠️ EPPO: info@eppo.europa.eu does NOT process complaints (auto-reply confirmed 05/03/2026). ' +
                  'MUST file via web form: https://eppo.europa.eu/en/reporting-crime-eppo — ' +
                  'Form does NOT support attachments — mention them in text and team will follow up. ' +
                  'CC in emails is symbolic/documentary only.';

// ================================================================
// In each case note that mentions EPPO escalation, append:
//   `\n${EPPO_NOTE}`
//
// Cases affected (7 of 16):
// - KEFODE-ATT-164685-EX-2026
// - ATTICA-14678-04-03-2026  
// - AADE-33077-33046-33047-33079-2026
// - EFKA-419690-REPLY
// - EAD-14441-KDD-TRIAD
// - NAT-ROUTING-PENSION-274
// - KTIMATOLOGIO-ND0113-CORRECTED
// ================================================================
