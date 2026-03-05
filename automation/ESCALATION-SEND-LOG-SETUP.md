# Google Sheets Setup — ESCALATION_SEND_LOG (Layer 3)

## Purpose
Permanent, cloud-backed audit trail of every escalation email sent by the n8n engine.
Serves as evidence for EPPO/courts that escalations were sent exactly once per deadline.

## Sheet Name
`ESCALATION_SEND_LOG`

## Create in Google Sheets
1. Open Google Sheets → New Spreadsheet
2. Name it: **Justice-for-John — Escalation Send Log**
3. Sheet 1 tab name: `ESCALATION_SEND_LOG`
4. Add these headers in Row 1:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| timestamp | case_id | protocol_number | sent_to | cc | subject | layer_status |

5. Format column A as "Date time"
6. Freeze Row 1
7. Share with stamatinakyprianou@gmail.com (Editor)

## n8n Wiring

### Node: "Google Sheets Append" (after Gmail Send)
- Operation: Append Row
- Document: Justice-for-John — Escalation Send Log
- Sheet: ESCALATION_SEND_LOG
- Columns: Parse from sheets_log_entry JSON field

### Parse Function Node (between Gmail Send and Google Sheets):
```javascript
const entry = JSON.parse($json.sheets_log_entry);
entry.layer_status = 'L1+L2+L3 ALL RECORDED';
return [{ json: entry }];
```

### OPTIONAL: Pre-check (Google Sheets Search) BEFORE Code node
- Search ESCALATION_SEND_LOG for today's date + case_id
- If found: set sheets_already_sent = true
- Adds Layer 3 read-check (belt + suspenders + duct tape)

## Column Descriptions

| Column | Type | Description |
|--------|------|-------------|
| timestamp | ISO 8601 | Exact time escalation was sent |
| case_id | String | Protocol number / case identifier |
| protocol_number | String | Formal protocol number |
| sent_to | String | Primary recipient email |
| cc | String | CC recipients (comma-separated) |
| subject | String | Email subject line |
| layer_status | String | Which dedup layers recorded this send |

## Audit Value
- Each row = one escalation email = one auditable event
- Timestamped, immutable (append-only)
- Cross-reference with Gmail Sent folder
- Cross-reference with GitHub Issue #1 comments
- Cross-reference with Master Protocol Tracker CSV
- Admissible as evidence of systematic, non-duplicative escalation
