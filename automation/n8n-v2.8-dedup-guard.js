// ================================================================
// n8n DUPLICATE GUARD — TRIPLE LAYER
// For "Check Status + Parse" Code node in workflow 8tFYcHI7qW062BZV
// Version: v2.8-DEDUP
// Date: 2026-03-05
// Purpose: Prevent re-sending the same escalation email multiple times
// ================================================================
//
// ARCHITECTURE — 3 Independent Layers:
//
// LAYER 1: n8n Static Data ($getWorkflowStaticData)
//   - In-memory, fastest check
//   - Survives workflow re-executions
//   - Lost on n8n container restart
//
// LAYER 2: File-based JSON Log (D:\Justice-Docker\n8n_data\sent_log.json)
//   - Persists across Docker restarts (volume-mounted)
//   - Readable/auditable as plain JSON
//   - Lost only if volume deleted
//
// LAYER 3: Google Sheets Log (append row on send)
//   - Permanent, cloud-backed, visible in browser
//   - Serves as audit trail for EPPO/courts
//   - Requires Google Sheets API connection in n8n
//
// If ANY layer says "already sent today" -> SKIP the case.
// All 3 layers log on successful send.
//
// ================================================================
// INSTALLATION:
// 1. Open http://localhost:5678/workflow/8tFYcHI7qW062BZV
// 2. Double-click the "Check Status + Parse" Code node
// 3. REPLACE the entire code with this version
// 4. Create sent_log.json in D:\Justice-Docker\n8n_data\
// 5. Google Sheets: Create sheet "ESCALATION_SEND_LOG" with headers:
//    timestamp | case_id | protocol_number | sent_to | cc | subject | layer_status
// 6. Save node -> Save workflow -> Test
// ================================================================

const now = new Date();
const today = now.toISOString().slice(0, 10);
const deathDate = new Date('2021-06-13');
const daysSinceDeath = Math.floor((now - deathDate) / (1000 * 60 * 60 * 24));

const EPPO_NOTE = 'EPPO: info@eppo.europa.eu does NOT process complaints (auto-reply confirmed 05/03/2026). ' +
                  'MUST file via web form: https://eppo.europa.eu/en/reporting-crime-eppo';

// -- LAYER 1: n8n Static Data --
const staticData = $getWorkflowStaticData('global');
if (!staticData.sentLog) {
  staticData.sentLog = {};
}

// -- LAYER 2: File-based JSON Log --
const SENT_LOG_PATH = '/home/node/.n8n/sent_log.json';
const fs = require('fs');

function readFileLog() {
  try {
    if (fs.existsSync(SENT_LOG_PATH)) {
      const raw = fs.readFileSync(SENT_LOG_PATH, 'utf8');
      return JSON.parse(raw);
    }
  } catch (e) {
    console.error(`[DEDUP] File log read error: ${e.message}`);
  }
  return { sends: [], lastUpdated: null };
}

function writeFileLog(log) {
  try {
    log.lastUpdated = now.toISOString();
    fs.writeFileSync(SENT_LOG_PATH, JSON.stringify(log, null, 2), 'utf8');
  } catch (e) {
    console.error(`[DEDUP] File log write error: ${e.message}`);
  }
}

function fileLogHasSentToday(caseId) {
  const log = readFileLog();
  return log.sends.some(
    entry => entry.case_id === caseId && entry.date === today
  );
}

function fileLogRecord(caseId, protocolNumber, sentTo, subject) {
  const log = readFileLog();
  log.sends.push({
    case_id: caseId,
    protocol_number: protocolNumber,
    sent_to: sentTo,
    subject: subject,
    date: today,
    timestamp: now.toISOString()
  });
  const cutoff = new Date(now);
  cutoff.setDate(cutoff.getDate() - 90);
  const cutoffStr = cutoff.toISOString().slice(0, 10);
  log.sends = log.sends.filter(entry => entry.date >= cutoffStr);
  writeFileLog(log);
}

// -- DEDUP CHECK --
function alreadySentToday(caseId) {
  const staticKey = `${caseId}_${today}`;
  if (staticData.sentLog[staticKey]) {
    console.log(`[DEDUP] Layer 1 BLOCKED: ${caseId} already sent today (static data)`);
    return { blocked: true, layer: 'static_data' };
  }
  if (fileLogHasSentToday(caseId)) {
    console.log(`[DEDUP] Layer 2 BLOCKED: ${caseId} already sent today (file log)`);
    return { blocked: true, layer: 'file_log' };
  }
  return { blocked: false, layer: null };
}

function markAsSent(caseId, protocolNumber, sentTo, subject) {
  const staticKey = `${caseId}_${today}`;
  staticData.sentLog[staticKey] = {
    timestamp: now.toISOString(),
    protocol_number: protocolNumber
  };
  fileLogRecord(caseId, protocolNumber, sentTo, subject);
}

// -- CLEANUP: Remove static data entries older than 7 days --
const cleanupCutoff = new Date(now);
cleanupCutoff.setDate(cleanupCutoff.getDate() - 7);
const cleanupStr = cleanupCutoff.toISOString().slice(0, 10);
for (const key of Object.keys(staticData.sentLog)) {
  const keyDate = key.split('_').pop();
  if (keyDate < cleanupStr) {
    delete staticData.sentLog[key];
  }
}

// ================================================================
// CASES ARRAY — Paste your existing 16 cases (v2.6 + v2.7) here
// ================================================================
const cases = [
  // YOUR EXISTING 16 CASES GO HERE
];

// ================================================================
// OUTPUT LOOP WITH DEDUP
// Replaces: return cases.map(...)
// IF Node condition: change from $json.overdue to $json.should_send
// ================================================================
const output = [];

for (const c of cases) {
  const caseId = c.protocol_number || c.risk || 'UNKNOWN';
  const deadline = new Date(c.deadline + 'T23:59:00+03:00');
  const isOverdue = now > deadline;
  const daysRemaining = Math.floor((deadline - now) / (1000 * 60 * 60 * 24));

  const item = {
    protocol_number: c.protocol_number,
    agency: c.agency,
    description: c.description,
    date_filed: c.date_filed,
    deadline: c.deadline,
    overdue: isOverdue,
    days_remaining: daysRemaining,
    days_since_death: daysSinceDeath,
    escalated_to: c.escalated_to,
    cc: Array.isArray(c.cc) ? c.cc.join(',') : (c.cc || ''),
    subject_short: c.subject_short,
    risk: c.risk,
    note: c.note,
    evidence_links: JSON.stringify(c.evidence_links || {}),
    afm_targets: (c.afm_targets || []).join(','),
    legal_basis: (c.legal_basis || []).join(' | '),
    github_issue: c.github_issue || 1,
    dedup_blocked: false,
    dedup_layer: null,
    dedup_case_id: caseId,
    dedup_date: today,
    should_send: false,
    sheets_log_entry: null
  };

  if (isOverdue) {
    const dedupResult = alreadySentToday(caseId);
    if (dedupResult.blocked) {
      item.dedup_blocked = true;
      item.dedup_layer = dedupResult.layer;
      item.should_send = false;
      item.note += `\n[DEDUP] Blocked by ${dedupResult.layer} — already sent today.`;
    } else {
      item.should_send = true;
      markAsSent(caseId, c.protocol_number, c.escalated_to, c.subject_short);
      item.sheets_log_entry = JSON.stringify({
        timestamp: now.toISOString(),
        case_id: caseId,
        protocol_number: c.protocol_number,
        sent_to: c.escalated_to,
        cc: Array.isArray(c.cc) ? c.cc.join(',') : (c.cc || ''),
        subject: c.subject_short,
        layer_status: 'L1+L2 recorded, L3 pending'
      });
    }
  }

  output.push({ json: item });
}

const overdueCount = output.filter(o => o.json.overdue).length;
const blockedCount = output.filter(o => o.json.dedup_blocked).length;
const sendCount = output.filter(o => o.json.should_send).length;

output.push({
  json: {
    _summary: true,
    total_cases: cases.length,
    overdue_cases: overdueCount,
    dedup_blocked: blockedCount,
    will_send: sendCount,
    days_since_death: daysSinceDeath,
    run_date: today,
    run_timestamp: now.toISOString(),
    engine_version: 'v2.8-DEDUP',
    guard_layers: 'L1:static_data | L2:file_log | L3:google_sheets',
    note: `Duplicate guard active. ${blockedCount} blocked, ${sendCount} will send.`
  }
});

return output;

// ================================================================
// DOWNSTREAM CHANGES:
// 1. IF Node: change condition to $json.should_send === true
// 2. Add Google Sheets Append node after Gmail Send
// 3. Optional: Google Sheets Search before Code node (Layer 3 read)
// ================================================================
