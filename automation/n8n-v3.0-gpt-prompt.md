# GPT Node Prompt Template — v3.0 Escalation Email Generator

## n8n Node Configuration

**Node Type:** OpenAI Chat Model (or AI Agent)
**Model:** gpt-4o (or gpt-4o-mini for cost savings)
**Temperature:** 0.3 (factual, formal tone)
**Placement:** After IF Node (`should_send === true`), before Gmail Send node

---

## System Prompt

```
You are a legal escalation drafting assistant for Σταματίνα Κυπριανού (Stamatina Kyprianou), a 79-year-old US citizen, widow and sole heir of Ιωάννης Κυπριανός (John Kyprianos, AFM 051422558), a Hellenic Navy veteran who died 13/06/2021.

Your job: generate a formal escalation email in Greek (with English summary paragraph at the end) based on the structured case data provided.

RULES:
1. Address the agency by name. Use formal Greek register (σας, παρακαλώ, Αξιότιμε/η).
2. Open with: "Αξιότιμε/η κ. [agency contact or Προϊστάμενε/η],"
3. Reference the protocol number, date filed, statutory deadline, and days overdue.
4. Cite the exact legal basis (e.g., Αρθ.4 Ν.2690/1999) and the consequence of non-compliance.
5. Include the days_since_death counter as moral/legal pressure: "Έχουν παρέλθει {days_since_death} ημέρες από τον θάνατο του συζύγου μου."
6. If risk contains "PHANTOM_PENSION" or "NAVY", emphasize that the pension was confirmed as a Hellenic Navy pension by EFKA official Κακλαμάνου.
7. If the case involves EPPO, add this note verbatim: "Σημείωση: Η αναφορά στο EPPO έχει κατατεθεί μέσω της ηλεκτρονικής φόρμας (eppo.europa.eu/en/reporting-crime-eppo). Το info@eppo.europa.eu δεν επεξεργάζεται καταγγελίες."
8. Close with: "Αναμένω γραπτή απάντηση εντός [deadline window]. Σε διαφορετική περίπτωση, θα προχωρήσω σε [next escalation step]."
9. Add English summary paragraph: "English Summary: [1-2 sentence translation of the core request]."
10. Sign as:
    Σταματίνα Κυπριανού
    AFM: 044594747
    Χήρα και μοναδική κληρονόμος Ιωάννη Κυπριανού (AFM 051422558)
    Email: stamatinakyprianou@gmail.com

ESCALATION LADDER (use for "next escalation step"):
- AEAD/EAD complaints → Συνήγορος του Πολίτη, ΑΠΔΠΧ
- EFKA/NAT pension → ΣΔΟΕ, Εισαγγελία Πειραιά
- AADE GDPR → ΑΠΔΠΧ (complaints@dpa.gr)
- Ktimatologio → Αποκεντρωμένη Διοίκηση Αττικής, Εισαγγελία
- Criminal matters → Εισαγγελία, EPPO, OLAF
- All cases → EPPO web form as last resort

DO NOT invent protocol numbers, dates, or facts. Use ONLY the data provided in the input fields.
```

---

## User Message Template (n8n expression)

```
Generate a formal escalation email for the following case:

Protocol: {{ $json.protocol_number }}
Agency: {{ $json.agency }}
Description: {{ $json.description }}
Date Filed: {{ $json.date_filed }}
Deadline: {{ $json.deadline }}
Days Overdue: {{ Math.abs($json.days_remaining) }}
Days Since Death: {{ $json.days_since_death }}
Send To: {{ $json.escalated_to }}
CC: {{ $json.cc }}
Risk Level: {{ $json.risk }}
Case Notes: {{ $json.note }}
Legal Basis: {{ $json.legal_basis }}
AFM Targets: {{ $json.afm_targets }}
Evidence Links: {{ $json.evidence_links }}

Generate the subject line and email body. Use the subject_short as basis: {{ $json.subject_short }}
```

---

## Output Parsing

The GPT node output should be parsed to extract:
- `email_subject` — the generated subject line
- `email_body` — the full email body (HTML or plain text)

**Recommended:** Use a Code node after GPT to split the response:

```javascript
const response = $json.text || $json.message?.content || '';

// Split on first double newline — subject is first line, body is rest
const lines = response.split('\n');
let subject = '';
let body = '';

for (let i = 0; i < lines.length; i++) {
  if (lines[i].startsWith('Subject:') || lines[i].startsWith('Θέμα:')) {
    subject = lines[i].replace(/^(Subject:|Θέμα:)\s*/, '').trim();
  } else if (subject && lines[i].trim() !== '') {
    body = lines.slice(i).join('\n');
    break;
  }
}

// Fallback: use subject_short from upstream
if (!subject) {
  subject = $('Code').item.json.subject_short || 'Escalation — No Subject Parsed';
}

return [{
  json: {
    ...$json,
    email_subject: subject,
    email_body: body || response,
    // Pass through fields for Gmail node
    escalated_to: $('Code').item.json.escalated_to,
    cc: $('Code').item.json.cc,
    protocol_number: $('Code').item.json.protocol_number,
    risk: $('Code').item.json.risk
  }
}];
```

---

## Gmail Node Configuration

After the GPT + parser:
- **To:** `{{ $json.escalated_to }}`
- **CC:** `{{ $json.cc }}`
- **Subject:** `{{ $json.email_subject }}`
- **Body:** `{{ $json.email_body }}`
- **From:** stamatinakyprianou@gmail.com
- **Reply-To:** stamatinakyprianou@gmail.com

---

## Flow Summary

```
Schedule Trigger (Mon-Fri 09:00 Athens)
  → Code Node (v3.0 — 19 cases, dedup guard)
    → IF Node ($json.should_send === true)
      → GPT Node (system prompt + case data → email draft)
        → Code Node (parse subject/body)
          → Gmail Send
            → Google Sheets Append (ESCALATION_SEND_LOG — L3 audit)
```
