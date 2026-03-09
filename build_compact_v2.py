#!/usr/bin/env python3
"""
IRS-CI Compact Interview Package v2 — Updated March 9, 2026 (afternoon)
Adds Tab 10 (AADE Institutional Obstruction), Q14, updated Parallel Investigations,
and March 9 afternoon developments.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register DejaVu Sans for Greek characters
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'))

# Colors
TEAL = HexColor('#01696F')
TEAL_HOVER = HexColor('#0C4E54')
DARK = HexColor('#28251D')
MUTED = HexColor('#7A7974')
BG = HexColor('#F7F6F2')
RED = HexColor('#A13544')
RED_BG = HexColor('#FFF0F0')
SURFACE = HexColor('#F9F8F5')
BORDER = HexColor('#D4D1CA')
ORANGE = HexColor('#964219')
GREEN_BG = HexColor('#F0F8F0')

W, H = letter
output_path = '/home/user/workspace/IRS-CI-COMPACT-INTERVIEW-PACKAGE-2026-03-11-v2.pdf'

doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    title='IRS-CI Interview — Compact Package v2',
    author='Perplexity Computer',
    topMargin=0.5*inch,
    bottomMargin=0.55*inch,
    leftMargin=0.65*inch,
    rightMargin=0.65*inch
)

styles = getSampleStyleSheet()

# === STYLES ===
hero_style = ParagraphStyle(
    'Hero', parent=styles['Title'],
    fontName='DejaVuSans-Bold', fontSize=18, leading=22,
    textColor=DARK, alignment=TA_CENTER, spaceAfter=2
)
hero_sub = ParagraphStyle(
    'HeroSub', parent=styles['Normal'],
    fontName='DejaVuSans', fontSize=10, leading=13,
    textColor=MUTED, alignment=TA_CENTER, spaceAfter=6
)
h1 = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontName='DejaVuSans-Bold', fontSize=13, leading=16,
    textColor=TEAL, spaceBefore=12, spaceAfter=5
)
h2 = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontName='DejaVuSans-Bold', fontSize=11, leading=14,
    textColor=DARK, spaceBefore=8, spaceAfter=4
)
h2_teal = ParagraphStyle(
    'H2Teal', parent=h2, textColor=TEAL
)
body = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontName='DejaVuSans', fontSize=9, leading=12.5,
    textColor=DARK, spaceAfter=5
)
body_bold = ParagraphStyle(
    'BodyBold', parent=body, fontName='DejaVuSans-Bold'
)
body_red = ParagraphStyle(
    'BodyRed', parent=body, textColor=RED, fontName='DejaVuSans-Bold'
)
body_orange = ParagraphStyle(
    'BodyOrange', parent=body, textColor=ORANGE, fontName='DejaVuSans-Bold'
)
small = ParagraphStyle(
    'Small', parent=styles['Normal'],
    fontName='DejaVuSans', fontSize=7.5, leading=10,
    textColor=MUTED, spaceAfter=3
)
small_bold = ParagraphStyle(
    'SmallBold', parent=small, fontName='DejaVuSans-Bold'
)
bullet = ParagraphStyle(
    'Bullet', parent=body,
    leftIndent=18, bulletIndent=6, spaceBefore=1.5, spaceAfter=1.5
)
q_style = ParagraphStyle(
    'Question', parent=body,
    fontName='DejaVuSans-Bold', spaceBefore=7, spaceAfter=2
)
a_style = ParagraphStyle(
    'Answer', parent=body, spaceAfter=5
)
italic_style = ParagraphStyle(
    'Italic', parent=body,
    fontName='DejaVuSans-Oblique', textColor=MUTED
)
footer_style = ParagraphStyle(
    'Footer', parent=small, alignment=TA_CENTER
)
confidential_style = ParagraphStyle(
    'Confidential', parent=small,
    fontName='DejaVuSans-Bold', textColor=MUTED, alignment=TA_CENTER, fontSize=7
)

def make_table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style_cmds = [
        ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('LEADING', (0,0), (-1,-1), 11),
        ('TEXTCOLOR', (0,0), (-1,-1), DARK),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
    ]
    if header:
        style_cmds += [
            ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold'),
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('TEXTCOLOR', (0,0), (-1,0), white),
            ('FONTSIZE', (0,0), (-1,0), 7.5),
        ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), SURFACE))
    t.setStyle(TableStyle(style_cmds))
    return t

def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('DejaVuSans', 7)
    canvas.setFillColor(MUTED)
    page_num = doc.page
    canvas.drawString(0.65*inch, 0.35*inch,
        f'IRS-CI Compact Interview Package v2 \u2014 Kyprianos Case \u2014 Page {page_num}')
    canvas.drawRightString(W - 0.65*inch, 0.35*inch,
        'CONFIDENTIAL \u2014 LAW ENFORCEMENT SENSITIVE')
    canvas.restoreState()

story = []

# ============================================================
# PAGE 1: COVER
# ============================================================
story.append(Spacer(1, 10))
story.append(Paragraph('IRS-CI INTERVIEW \u2014 COMPACT PACKAGE', hero_style))
story.append(Paragraph('SA Zacheranik | March 11, 2026 | 9:00 AM | 16441 Waterman Dr, Roseville MI', hero_sub))
story.append(HRFlowable(width='100%', color=TEAL, thickness=2, spaceAfter=10))

story.append(Paragraph('YOUR STATUS', h1))
story.append(Paragraph(
    'You are a <b>VICTIM and WITNESS</b> \u2014 not a target. This investigation was triggered by YOUR congressional inquiry '
    'through Senator Slotkin. SA Zacheranik is here to investigate the fraud against you and John.', body))

story.append(Paragraph('KEY CASE NUMBERS', h1))
key_data = [
    ['Field', 'Value', 'Field', 'Value'],
    ['Your SSN', '364-76-6987', 'Your AFM', '044594747'],
    ["John's AFM", '051422558 (deceased)', "John's DOD", 'June 13, 2021'],
    ['Form 14157', 'Case 26236541', 'FBI IC3', 'eaa5459ac...82'],
    ['Congressional', 'IMA00176193', 'EPPO', 'PP.00179 + 4 more'],
    ['Perpetrator AFM', 'Efthalia: 05282816', 'AADE Removal', 'Prot. 76022'],
    ['IRS RPO', 'Ref 26-70151', 'Contact', 'G. Smith 470-639-2599'],
]
t = make_table(key_data, col_widths=[85, 130, 85, 130])
story.append(t)
story.append(Spacer(1, 8))

story.append(Paragraph('THE FRAUD IN ONE SENTENCE', h1))
story.append(Paragraph(
    'John died June 13, 2021 in Roseville, MI. Greek authorities kept his tax ID active for 5 years. '
    'Efthalia Kyprianou (AFM 05282816) used his identity as unauthorized tax representative. H&amp;R Block '
    'filed U.S. returns with ~$30,000 in false foreign tax credits (only $5,984 paid) including a -$830,000 '
    'negative foreign income entry on Form 1116. EFKA confirmed on March 9, 2026 that John was a Greek Navy '
    'pensioner \u2014 a pension John and Stamatina never received, indicating possible phantom collection by a third party.',
    body))

story.append(Paragraph('YOUR RIGHTS', h1))
rights = [
    'Right to be accompanied by counsel (26 CFR 601.107(b)(1))',
    'Right to refuse any question that might incriminate you (5th Amendment)',
    'Everything documented in a Memorandum of Interview (MOI)',
    'As a victim: right to protection, notification, fairness, and respect',
]
for r in rights:
    story.append(Paragraph(r, bullet, bulletText='\u2022'))

story.append(Paragraph('DOCUMENTS ON TABLE', h1))
docs_on_table = [
    'This Compact Package (v2 \u2014 updated March 9 PM)',
    'Evidence Package (21 pages)',
    'Physical binder (2 copies)',
    'IRS Account Transcripts 2020\u20132024',
    'Form 1116 with -$830,000 entry',
    'Death certificate',
    'AADE removal order (Prot. 76022)',
    'DEI bills (Feb 2026)',
    'IRS RPO Letter 4924 (Ref 26-70151)',
    'EFKA pension confirmation email (March 9, 2026)',
    '<b>AADE 7-Ticket Institutional Obstruction Filing (March 9, 2026) \u2014 NEW</b>',
]
for d in docs_on_table:
    story.append(Paragraph(d, bullet, bulletText='\u2022'))

# ============================================================
# PAGE 2: INTERVIEW DISCIPLINE + BINDER INDEX
# ============================================================
story.append(PageBreak())
story.append(Paragraph('INTERVIEW DISCIPLINE', h1))
disc = [
    'Say: "This shows" / "This is consistent with" \u2014 NEVER "This proves"',
    'Core: Deceased identity + false US returns + unauthorized representation + phantom pension + institutional obstruction',
    'If unsure: "I will need to check my records"',
    'Separate: What I know / What documents show / What needs investigation',
    '<b>NEW: Greek tax authorities actively obstructed the investigation \u2014 this is documented evidence for IRS-CI</b>',
]
for d in disc:
    story.append(Paragraph(d, bullet, bulletText='\u2022'))

story.append(Spacer(1, 8))
story.append(Paragraph('EVIDENCE BINDER \u2014 DOCUMENT INDEX', hero_style))
story.append(Paragraph('Bring TWO copies \u2014 one for SA Zacheranik, one for your records', hero_sub))
story.append(HRFlowable(width='100%', color=TEAL, thickness=1, spaceAfter=8))

# Tab 1
story.append(Paragraph('Tab 1 \u2014 Case Summary', h2_teal))
t1_data = [['#', 'Document'], ['1.1', 'IRS-CI Evidence Package (21 pages)'], ['1.2', 'This Compact Interview Package (v2)']]
story.append(make_table(t1_data, col_widths=[50, 390]))

# Tab 2
story.append(Paragraph('Tab 2 \u2014 IRS Forms Filed', h2_teal))
t2_data = [
    ['#', 'Document'],
    ['2.1', 'Form 14157 \u2014 Preparer Complaint (Case 26236541)'],
    ['2.2', 'Form 3949-A \u2014 Information Referral'],
    ['2.3', 'Form 14039 \u2014 Identity Theft Affidavit + fax'],
    ['2.4', 'Form 8802 \u2014 U.S. Residency Certification'],
    ['2.5', 'IRS RPO Letter 4924 \u2014 Ref 26-70151 (Feb 26, 2026)'],
]
story.append(make_table(t2_data, col_widths=[50, 390]))

# Tab 3
story.append(Paragraph('Tab 3 \u2014 IRS Account Transcripts', h2_teal))
t3_data = [
    ['#', 'Document'],
    ['3.1\u20133.5', 'Account Transcripts 2020\u20132024'],
    ['3.6', 'IRS Notice CP25 (April 21, 2025)'],
    ['3.7', 'Form 6166 \u2014 U.S. Tax Residency Certificate'],
]
story.append(make_table(t3_data, col_widths=[50, 390]))

# Tab 4
story.append(Paragraph('Tab 4 \u2014 H&amp;R Block Evidence', h2_teal))
t4_data = [
    ['#', 'Document'],
    ['4.1', '2024 Form 1116 showing -$830,000 (SMOKING GUN)'],
    ['4.2', 'Form 1040 returns 2021\u20132024 as filed'],
    ['4.3', 'H&R Block payment receipt ($59.99)'],
    ['4.4', 'Bree Cox correspondence (Jan + Feb 2026)'],
    ['4.5', 'Mellissa Worman refusal to correct (Jun 2025)'],
    ['4.6', 'H&R Block Complaint Narrative (Jan 2026)'],
]
story.append(make_table(t4_data, col_widths=[50, 390]))

# ============================================================
# PAGE 3: TABS 5-10
# ============================================================
story.append(PageBreak())

# Tab 5
story.append(Paragraph('Tab 5 \u2014 Greek Tax Documents', h2_teal))
t5_data = [
    ['#', 'Document'],
    ['5.1', 'ENFIA 2021\u20132024 \u2014 AFM 044594747 (your actual taxes)'],
    ['5.2', 'ENFIA 2020\u20132023 \u2014 AFM 051422558 (post-mortem)'],
    ['5.3', 'E1 Income Tax Returns 2022\u20132024'],
    ['5.4', 'Ekkatharistika (assessments) 2022\u20132024'],
    ['5.5', 'Bank statements \u2014 AADE payments'],
    ['5.6', 'AADE payment history 2021\u20132025'],
    ['5.7', 'AADE removal order \u2014 Prot. 76022/20260114'],
    ['5.8', 'AADE GDPR Art. 15 request (Prot. ATYYP 8202)'],
]
story.append(make_table(t5_data, col_widths=[50, 390]))

# Tab 6
story.append(Paragraph('Tab 6 \u2014 Property &amp; Identity', h2_teal))
t6_data = [
    ['#', 'Document'],
    ['6.1', 'U.S. Death Certificate \u2014 John (June 13, 2021)'],
    ['6.2', 'Dowry deed 2777 (April 6, 1972)'],
    ['6.3', 'Ktimatologio Cert. SN003794 (Dec 20, 2024)'],
    ['6.4\u20136.7', 'Passports, SSN cards, licenses, naturalization'],
    ['6.8', 'DEI bills Feb 2026 \u2014 5 meters, 0 kWh (supporting)'],
]
story.append(make_table(t6_data, col_widths=[50, 390]))

# Tab 7
story.append(Paragraph('Tab 7 \u2014 Law Enforcement &amp; Congressional', h2_teal))
t7_data = [
    ['#', 'Document'],
    ['7.1', 'FBI IC3 complaint confirmation'],
    ['7.2', 'EPPO references (PP.00179/267/281/310/464)'],
    ['7.3', 'OLAF FNS 25098'],
    ['7.4', 'U.S. Consulate Chicago letter (Jan 2026)'],
    ['7.5', 'Senator Slotkin correspondence (IMA00176193)'],
    ['7.6', 'SA Zacheranik email (March 4, 2026)'],
    ['7.7', 'Slotkin staff replies (Wolken + Lopez)'],
]
story.append(make_table(t7_data, col_widths=[50, 390]))

# Tab 8
story.append(Paragraph('Tab 8 \u2014 Greek Pension Investigation (NEW)', h2_teal))
t8_data = [
    ['#', 'Document'],
    ['8.1', 'EFKA email \u2014 Kaklamanou confirms PN pension (Mar 9, 2026)'],
    ['8.2', 'NAT response \u2014 Patsioudis: not competent authority (Mar 6)'],
    ['8.3', 'NAT \u2192 EFKA routing chain (Mar 3\u20139, 2026)'],
]
story.append(make_table(t8_data, col_widths=[50, 390]))

# Tab 9
story.append(Paragraph('Tab 9 \u2014 Optional / Master Tracker', h2_teal))
t9_data = [
    ['#', 'Document'],
    ['9.1', 'Master Protocol Tracker (297+ entries)'],
    ['9.2', 'Tax Prep Action Plan for CPA'],
    ['9.3', 'Greek Tax Evidence Package (complete)'],
]
story.append(make_table(t9_data, col_widths=[50, 390]))

# Tab 10 — NEW
story.append(Spacer(1, 4))
story.append(Paragraph('Tab 10 \u2014 AADE Institutional Obstruction (NEW \u2014 March 9, 2026)', h2_teal))
t10_data = [
    ['#', 'Document'],
    ['10.1', '7-Ticket \u039a\u0391\u03a4\u0391\u0393\u0393\u0395\u039b\u0399\u0391 filed to AADE protocol@aade.gr (Mar 9, 2026)'],
    ['10.2', '\u039a\u0395\u03a6\u039f\u0394\u0395 A4\u2019 hostile response: \u00ab\u03bc\u03b7\u03bd \u03b5\u03c0\u03b1\u03bd\u03ad\u03c1\u03c7\u03b5\u03c3\u03b8\u03b5 \u03bc\u03b5 \u03ba\u03b1\u03c4\u03b1\u03b3\u03b3\u03b5\u03bb\u03af\u03b5\u03c2\u00bb (Req. 190731)'],
    ['10.3', 'Wrong-AFM refund evidence (Req. 257636 \u2014 money sent to wrong AFM)'],
    ['10.4', 'No income declarations after 2021 death (AADE confirmed)'],
    ['10.5', '\u0395\u0391\u0394 15063 EI 2026 \u2014 Art.4 \u039a\u0394\u0394 + EPPO notification (Mar 9)'],
    ['10.6', 'CC to \u0395\u03c0\u03bf\u03c0\u03c4\u03b5\u03af\u03b1 \u039f\u03a4\u0391 Attica (epopteiaota@attica.gr) re: \u0394\u03ae\u03bc\u03bf\u03c2 \u03a3\u03c0\u03b5\u03c4\u03c3\u03ce\u03bd obstruction'],
    ['10.7', 'All 7 myAADE responses with analysis (full text)'],
]
story.append(make_table(t10_data, col_widths=[50, 390]))

# ============================================================
# PAGE 4: Q&A PREP (Q1-Q10)
# ============================================================
story.append(PageBreak())
story.append(Paragraph('INTERVIEW Q&amp;A PREP \u2014 BILINGUAL', hero_style))
story.append(Paragraph('14 Likely Questions + Model Answers + 8 Questions for SA Zacheranik', hero_sub))
story.append(HRFlowable(width='100%', color=TEAL, thickness=1, spaceAfter=8))

qa = [
    ('Q1: How did you discover the fraud?',
     'I saw inconsistencies between actual Greek tax obligations and records linked to John\u2019s AFM and my US returns. '
     'The pattern showed post-mortem use of his Greek tax identity and unauthorized representation.'),
    ('Q2: What is the single most important fact?',
     'John died in Michigan on June 13, 2021, but his Greek AFM stayed active for years, enabling tax, property, '
     'and identity consequences.'),
    ('Q3: Why isn\u2019t this just a mistake?',
     'The pattern is prolonged, multi-systemic, and benefits third parties. It involves post-mortem identity use, '
     'unauthorized representation, property consequences, and US return positions inconsistent with actual Greek amounts.'),
    ("Q4: What is H&amp;R Block's role?",
     'H&amp;R Block prepared my 2021\u20132024 US returns and claimed foreign tax credits far beyond what was actually paid to '
     'Greece, including a -$830,000 negative foreign income entry on Form 1116.'),
    ('Q5: Did you authorize these return positions?',
     'No. I relied on the preparer\u2019s expertise. I did not authorize false numbers or fabricated credits.'),
    ('Q6: What evidence do you have on the preparer?',
     'Filed returns, Form 1116 with -$830,000, payment receipt for Tax Pro Review, complaint materials, and the IRS RPO '
     'letter confirming receipt. \u2192 Show Tab 2 and Tab 4.'),
    ('Q7: Who is the unauthorized person?',
     'Efthalia Kyprianou, AFM 05282816. She was unauthorized tax representative on John\u2019s AFM until AADE removed her '
     'January 14, 2026. \u2192 Show Tab 5, item 5.7.'),
    ("Q8: What happened in Greece after John's death?",
     'His AFM remained active, enabling ongoing tax, property, and pension consequences. On March 9, 2026, EFKA '
     'confirmed John was a Greek Navy pensioner \u2014 a pension we never received. Someone may have been collecting it. '
     'EFKA has forwarded the case to their military pension division for investigation.'),
    ('Q9: What personal damages have you suffered?',
     'Direct financial harm: Greek tax burdens, property charges, and US tax exposure from returns I believe were false. '
     'We are also victims of possible phantom pension collection in Greece. Significant time and money spent documenting '
     'and reporting.'),
    ('Q10: What does the DEI exhibit show?',
     'DEI bills show ongoing charges on my AFM including municipal taxes, even with zero electricity consumption. This '
     'confirms continuing financial harm. It is supporting evidence, not the core proof. \u2192 Do NOT lead with this.'),
]

for q_text, a_text in qa:
    story.append(Paragraph(q_text, q_style))
    story.append(Paragraph(a_text, a_style))

# ============================================================
# PAGE 5: Q11-Q14 + QUESTIONS FOR SA ZACHERANIK
# ============================================================
story.append(PageBreak())

qa2 = [
    ('Q11: What do you know firsthand vs. inference?',
     'Firsthand: John died in MI. I received/paid certain taxes. I received records. I filed complaints. '
     'My US returns were filed with these entries. John and I never received a Greek Navy pension. '
     'Inference: internal coordination, systems used, full money trail.'),
    ('Q12: What do you want IRS-CI to do?',
     'Investigate the false US returns, the use of my deceased husband\u2019s identity in relation to tax fraud, the preparer\u2019s '
     'role, and any cross-border coordination affecting my returns or federal tax administration.'),
    ('Q13: What about the Greek Navy pension? (NEW)',
     'EFKA confirmed on March 9, 2026 that John was a Greek Navy pensioner. He lived in the US since 1976 and we '
     'never received any Greek pension. If a pension was being paid, someone else was collecting it without our '
     'knowledge. EFKA\u2019s military pension division is now investigating. We are victims on both sides of the Atlantic.'),
]

for q_text, a_text in qa2:
    story.append(Paragraph(q_text, q_style))
    story.append(Paragraph(a_text, a_style))

# Q14 — NEW
story.append(Spacer(1, 4))
story.append(Paragraph('Q14: What is the Greek tax authority doing about all this? (NEW \u2014 March 9)', q_style))
story.append(Paragraph(
    'On March 9, 2026, I received responses to 7 formal requests I filed through the AADE (Greek IRS) portal. '
    'The results show a pattern of institutional obstruction:', a_style))
q14_bullets = [
    'One office (\u039a\u0395\u03a6\u039f\u0394\u0395 A4\u2019) explicitly told me to <b>stop filing complaints</b> \u2014 '
    'a hostile response to a fraud victim.',
    'A tax refund was sent to the <b>wrong taxpayer ID</b> \u2014 money that should have gone to my AFM went elsewhere. '
    'This is consistent with embezzlement.',
    'AADE confirmed <b>no income tax returns were filed</b> for John\u2019s AFM after 2021 \u2014 yet property transfers '
    'and E9 modifications continued on his account. This is phantom administration of a dead man\u2019s estate.',
    'Every office refers me to another office. <b>No one takes responsibility</b>.',
    'The local municipality (\u0394\u03ae\u03bc\u03bf\u03c2 \u03a3\u03c0\u03b5\u03c4\u03c3\u03ce\u03bd) blocks the inheritance certificates '
    'needed to close the loop.',
]
for b in q14_bullets:
    story.append(Paragraph(b, bullet, bulletText='\u2022'))
story.append(Paragraph(
    'I filed a formal 7-ticket complaint (\u039a\u0391\u03a4\u0391\u0393\u0393\u0395\u039b\u0399\u0391) to AADE this morning '
    'and copied the regional government oversight authority (\u0395\u03c0\u03bf\u03c0\u03c4\u03b5\u03af\u03b1 \u039f\u03a4\u0391). '
    'The independent anti-corruption authority (\u0395\u0391\u0394) received it and referred the matter to EPPO under Art.4 \u039a\u0394\u0394. '
    'All of this is in Tab 10. \u2192 Show Tab 10.', a_style))

story.append(Spacer(1, 10))
story.append(Paragraph('8 QUESTIONS FOR SA ZACHERANIK', h1))
sa_qs = [
    'Based on what you\u2019ve reviewed, is IRS-CI looking at preparer fraud, identity theft, or both?',
    'Should I structure today\u2019s discussion as: US returns, Greek identity abuse, supporting property evidence?',
    'Which documents are most useful for you to copy today?',
    'Would a smaller core package first work better, with international materials as supplements?',
    'Should I identify, document-by-document, what I know firsthand vs. what needs investigation?',
    'Should I continue preserving and collecting current records (DEI bills, AADE notices, protocol responses)?',
    'If additional evidence arrives after today, what is the best channel and reference number?',
    'Are there specific record categories you recommend I prioritize \u2014 bank records, preparer communications, '
    'access logs, or identity documents?',
]
for i, q in enumerate(sa_qs, 1):
    story.append(Paragraph(f'{i}. {q}', body))

# ============================================================
# PAGE 6: TAB 10 DETAIL — AADE INSTITUTIONAL OBSTRUCTION
# ============================================================
story.append(PageBreak())
story.append(Paragraph('TAB 10 \u2014 AADE INSTITUTIONAL OBSTRUCTION', hero_style))
story.append(Paragraph('7-Ticket \u039a\u0391\u03a4\u0391\u0393\u0393\u0395\u039b\u0399\u0391 Filed March 9, 2026 \u2014 Summary for SA Zacheranik', hero_sub))
story.append(HRFlowable(width='100%', color=TEAL, thickness=1.5, spaceAfter=8))

story.append(Paragraph(
    'On March 9, 2026, Stamatina received responses to 7 formal requests filed through the myAADE portal '
    '(Greek tax authority online system). Instead of investigating a documented fraud case, the responses reveal '
    'a pattern of institutional obstruction, circular referrals, and in one case, <b>open hostility toward the victim</b>.', body))

story.append(Paragraph('Why This Matters for IRS-CI', h2))
story.append(Paragraph(
    'The Greek tax authority\'s failure to investigate means the underlying fraud infrastructure remains intact. '
    'The unauthorized person who filed false Greek returns (used by H&amp;R Block to calculate false US credits) '
    'has never been held accountable by Greek authorities. This obstruction directly impacts the IRS-CI investigation '
    'because it explains why false data continues to exist in the Greek system.', body))

story.append(Spacer(1, 4))

# Obstruction summary table
obs_data = [
    ['#', 'Office', 'Issue', 'Obstruction Type'],
    ['1', '\u039a\u0395\u03a6\u039f\u0394\u0395 A4\u2019', 'Told victim: \u00ab\u03bc\u03b7\u03bd \u03b5\u03c0\u03b1\u03bd\u03ad\u03c1\u03c7\u03b5\u03c3\u03b8\u03b5\u00bb\n(stop filing complaints)',
     'HOSTILE\n\u2014 intimidation'],
    ['2', '\u039a\u0395\u03a6\u039f\u0394\u0395 A3\u2019', 'Refund sent to wrong AFM\n(not Stamatina\u2019s 044594747)',
     'FINANCIAL FRAUD\n\u2014 embezzlement'],
    ['3', '\u039a\u0395\u03a6\u039f\u0394\u0395 A3\u2019', 'Withheld tax on unauthorized returns',
     'CIRCULAR\n\u2014 \u00abpreviously answered\u00bb'],
    ['4', '\u039a\u0395\u03a6\u039f\u0394\u0395 A4\u2019', 'Claims Stamatina taxed\nonly on Greek-source income',
     'EVASION\n\u2014 who files returns?'],
    ['5', '\u039a\u0395\u03a6\u039f\u0394\u0395 \u03931\u2019', 'Death declaration requirements\n(documents blocked by municipality)',
     'SYSTEMIC\n\u2014 circular deadlock'],
    ['6', '\u039a\u0395\u03a6\u039f\u0394\u0395 \u03931\u2019', 'No income declarations\nfiled after 2021 death',
     'PHANTOM ADMIN\n\u2014 estate in limbo'],
    ['7', '\u039a\u0395.\u03a6\u039f.\u039a.', 'E9 modifications on\ndeceased\u2019s account',
     'CONCEALMENT\n\u2014 who modified E9?'],
]
t_obs = Table(obs_data, colWidths=[22, 72, 175, 145])
t_obs.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
    ('FONTSIZE', (0,0), (-1,-1), 7.5),
    ('LEADING', (0,0), (-1,-1), 10),
    ('TEXTCOLOR', (0,0), (-1,-1), DARK),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER),
    ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold'),
    ('BACKGROUND', (0,0), (-1,0), TEAL),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    # Row 1 highlight — hostile
    ('BACKGROUND', (0,1), (-1,1), RED_BG),
    ('TEXTCOLOR', (3,1), (3,1), RED),
    ('FONTNAME', (3,1), (3,1), 'DejaVuSans-Bold'),
    # Row 2 highlight — financial
    ('BACKGROUND', (0,2), (-1,2), RED_BG),
    ('TEXTCOLOR', (3,2), (3,2), RED),
    ('FONTNAME', (3,2), (3,2), 'DejaVuSans-Bold'),
    # Alternating for rest
    ('BACKGROUND', (0,4), (-1,4), SURFACE),
    ('BACKGROUND', (0,6), (-1,6), SURFACE),
]))
story.append(t_obs)

story.append(Spacer(1, 8))
story.append(Paragraph('Pattern Summary', h2))
story.append(Paragraph(
    'The 7 responses reveal a <b>five-layer obstruction pattern</b>:', body))
pattern_items = [
    '<b>Intimidation</b> \u2014 \u039a\u0395\u03a6\u039f\u0394\u0395 A4\u2019 explicitly told the victim to stop reporting fraud',
    '<b>Financial misrouting</b> \u2014 Tax refund sent to wrong AFM (possible embezzlement)',
    '<b>Phantom administration</b> \u2014 No income returns filed after death, yet property transfers continue',
    '<b>Circular referrals</b> \u2014 Each office refers to another; no office investigates',
    '<b>Municipal blockade</b> \u2014 \u0394\u03ae\u03bc\u03bf\u03c2 \u03a3\u03c0\u03b5\u03c4\u03c3\u03ce\u03bd blocks inheritance certificates, '
    'closing the deadlock loop',
]
for p in pattern_items:
    story.append(Paragraph(p, bullet, bulletText='\u2022'))

story.append(Spacer(1, 6))
story.append(Paragraph('Actions Taken March 9, 2026', h2))
action_items = [
    'Formal \u039a\u0391\u03a4\u0391\u0393\u0393\u0395\u039b\u0399\u0391 filed to AADE (protocol@aade.gr, dpo@aade.gr, desyp@aade.gr)',
    'CC sent to \u0395\u03c0\u03bf\u03c0\u03c4\u03b5\u03af\u03b1 \u039f\u03a4\u0391 Attica (epopteiaota@attica.gr) re: \u0394\u03ae\u03bc\u03bf\u03c2 \u03a3\u03c0\u03b5\u03c4\u03c3\u03ce\u03bd',
    '\u0395\u0391\u0394 (Independent Authority for Anti-Corruption) receipt confirmed: 15063 EI 2026',
    '\u0395\u0391\u0394 invoked Art.4 \u039a\u0394\u0394 and notified EPPO (European Public Prosecutor)',
    '\u0391\u03a0\u0394\u03a0\u03a7 (Data Protection Authority) case 2026/1314 already open re: AADE GDPR violations',
]
for a in action_items:
    story.append(Paragraph(a, bullet, bulletText='\u2022'))

# ============================================================
# PAGE 7: CORRECTIONS & UPDATES + PARALLEL INVESTIGATIONS
# ============================================================
story.append(PageBreak())
story.append(Paragraph('CORRECTIONS &amp; UPDATES', hero_style))
story.append(Paragraph('Updated March 9, 2026 \u2014 PM Edition (v2)', hero_sub))
story.append(HRFlowable(width='100%', color=TEAL, thickness=1.5, spaceAfter=8))

# EFKA section (carried over)
story.append(Paragraph('BREAKING: EFKA CONFIRMS GREEK NAVY PENSION (March 9, 2026 AM)', h2))
story.append(Paragraph(
    'At 5:31 AM EST, Vasiliki Kaklamanou (Head of Pensions, EFKA Local Directorate A\u2019 Piraeus) confirmed that '
    'John Kyprianos (AFM 051422558) "was a pensioner of the Hellenic Navy" '
    '(\u03bf \u03b8\u03b1\u03bd\u03ce\u03bd \u03ae\u03c4\u03b1\u03bd \u03c3\u03c5\u03bd\u03c4\u03b1\u03be\u03b9\u03bf\u03cd\u03c7\u03bf\u03c2 '
    '\u03c4\u03bf\u03c5 \u03a0\u03bf\u03bb\u03b5\u03bc\u03b9\u03ba\u03bf\u03cd \u039d\u03b1\u03c5\u03c4\u03b9\u03ba\u03bf\u03cd).', body))

efka_bullets = [
    'John lived in the USA since 1976. Stamatina confirms they never received a Greek Navy pension.',
    'If a pension was being paid on AFM 051422558, someone else was collecting it without the Kyprianos family\u2019s knowledge.',
    'EFKA forwarded to \u0394\u2019 \u0394\u03b9\u03b5\u03cd\u03b8\u03c5\u03bd\u03c3\u03b7 \u0391\u03c0\u03bf\u03bd\u03bf\u03bc\u03ae\u03c2 '
    '\u03a3\u03c5\u03bd\u03c4\u03ac\u03be\u03b5\u03c9\u03bd (Military Pension Division) to investigate payment records and IBAN.',
    'Third fraud vector: Greece (phantom pension), USA (false tax returns), Identity (post-mortem AFM abuse).',
]
for b in efka_bullets:
    story.append(Paragraph(b, bullet, bulletText='\u2022'))

# NEW — afternoon developments
story.append(Spacer(1, 6))
story.append(Paragraph('NEW: AADE INSTITUTIONAL OBSTRUCTION DOCUMENTED (March 9, 2026 PM)', h2))
story.append(Paragraph(
    '7 myAADE responses received and analyzed. Key findings: \u039a\u0395\u03a6\u039f\u0394\u0395 A4\u2019 hostile response '
    '(\u00ab\u03bc\u03b7\u03bd \u03b5\u03c0\u03b1\u03bd\u03ad\u03c1\u03c7\u03b5\u03c3\u03b8\u03b5\u00bb), wrong-AFM refund (Req. 257636), '
    'no income declarations after 2021 death, E9 modification concealment. '
    'Full \u039a\u0391\u03a4\u0391\u0393\u0393\u0395\u039b\u0399\u0391 filed. \u0395\u0391\u0394 acknowledged under 15063 EI 2026 and invoked Art.4 \u039a\u0394\u0394 + EPPO. '
    'See Tab 10 for full documentation.', body))

# Spetses correction (carried over)
story.append(Spacer(1, 6))
story.append(Paragraph('CORRECTION: SPETSES PROPERTY MANAGEMENT', h2))
story.append(Paragraph(
    'Stamatina\u2019s son Konstantinos manages authorized Airbnb rentals on Spetses properties with her explicit permission. '
    'This is a legitimate family arrangement. Konstantinos is NOT involved in the fraud scheme. '
    'The fraud concerns are limited to:', body))
fraud_actors = [
    'Efthalia Kyprianou \u2014 unauthorized tax representative on deceased John\u2019s AFM 051422558',
    'H&amp;R Block \u2014 false US tax returns with fabricated foreign tax credits',
    'Unknown party \u2014 possible phantom Greek Navy pension collection (under EFKA investigation)',
]
for f in fraud_actors:
    story.append(Paragraph(f, bullet, bulletText='\u2022'))

# PARALLEL INVESTIGATIONS TABLE — UPDATED
story.append(Spacer(1, 8))
story.append(Paragraph('PARALLEL INVESTIGATIONS \u2014 CURRENT STATUS', h1))

inv_data = [
    ['Agency', 'Reference', 'Filed', 'Status'],
    ['IRS-CI', 'IMA00176193 / F3949A', 'Jan 2026', 'Interview Mar 11'],
    ['FBI IC3', 'eaa5459ac...82', 'Jan 27', 'Pending'],
    ['EPPO', 'PP.00179/267/281/310/464', 'Jan\u2013Mar', '5 cases open'],
    ['OLAF', 'FNS 25098', 'Feb 17', 'Open'],
    ['Greek SDOE/\u0393\u0394 \u0394\u0395\u039f\u03a3', '\u039a\u0391\u03a4\u0395\u03a0\u0395\u0399\u0393\u039f\u039d 33077', 'Jan 23', 'Deadline Mar 14'],
    ['Eisaggeleia Piraeus', '\u03a0\u03b1\u03c1\u03b1\u03b3\u03b3\u03b5\u03bb\u03af\u03b1 258b', 'Feb', 'Open'],
    ['Sen. Slotkin', 'IMA00176193', 'Jan', 'Active'],
    ['\u0395\u0391\u0394', '15063 EI 2026', 'Mar 9', 'Art.4 \u039a\u0394\u0394 + EPPO'],
    ['EFKA \u0394\u2019 \u0394/\u03bd\u03c3\u03b7', 'Via Kaklamanou', 'Mar 9', 'PN pension investigation'],
    ['AADE GDPR', '\u0394\u03a5\u03a0\u0397\u0394\u0395\u0394 13256', '\u2014', 'Deadline Mar 12'],
    ['\u0391\u03a0\u0394\u03a0\u03a7', 'Case 2026/1314', 'Mar 5', 'Open \u2014 Prot. 1086'],
    ['AADE \u039a\u0391\u03a4\u0391\u0393\u0393\u0395\u039b\u0399\u0391', '7-ticket filing', 'Mar 9', 'Filed + CC \u0395\u03c0\u03bf\u03c0\u03c4\u03b5\u03af\u03b1 \u039f\u03a4\u0391'],
]
t_inv = make_table(inv_data, col_widths=[95, 130, 55, 145])
story.append(t_inv)

# ============================================================
# PAGE 8: SA ZACHERANIK CONTACT + CLOSING
# ============================================================
story.append(PageBreak())
story.append(Paragraph('SA ZACHERANIK CONTACT', h1))
story.append(Paragraph(
    'SA Clint J. Zacheranik, CPA | IRS-CI Detroit, Team 02 | 985 Michigan Ave, Rm 709, Detroit MI 48226 | '
    'Cell: 517-877-0162 | Clint.Zacheranik@ci.irs.gov', body))

story.append(Spacer(1, 14))
story.append(HRFlowable(width='60%', color=BORDER, thickness=0.5, spaceAfter=6))
story.append(Paragraph(
    '<i>Justice for John \u2014 Greek Navy (NATO) Veteran \u2014 Day 1,730</i>', italic_style))
story.append(Spacer(1, 10))

story.append(Paragraph(
    'Remember: You initiated this investigation. SA Zacheranik is here because your congressional inquiry worked. '
    'Be cooperative, be organized, be precise.', body))
story.append(Spacer(1, 8))
story.append(Paragraph(
    'You and John are victims on both sides of the Atlantic. H&amp;R Block fabricated credits in America. '
    'Someone collected John\u2019s pension in Greece. Greek tax authorities told you to stop complaining. '
    'You are here for justice \u2014 for both of you.', body))

story.append(Spacer(1, 14))
story.append(Paragraph('WHAT\u2019S NEW IN v2 (March 9 PM)', h2))
v2_bullets = [
    '<b>Tab 10 added</b> \u2014 AADE Institutional Obstruction (7-ticket \u039a\u0391\u03a4\u0391\u0393\u0393\u0395\u039b\u0399\u0391 + analysis)',
    '<b>Q14 added</b> \u2014 Interview prep for "What is the Greek tax authority doing?"',
    '<b>Parallel Investigations table updated</b> \u2014 Added \u0391\u03a0\u0394\u03a0\u03a7, AADE \u039a\u0391\u03a4\u0391\u0393\u0393\u0395\u039b\u0399\u0391, '
    'updated \u0395\u0391\u0394 to 15063 + Art.4 \u039a\u0394\u0394',
    '<b>Tracker updated</b> \u2014 297+ entries (was 285+)',
    '<b>Interview Discipline updated</b> \u2014 Added institutional obstruction as core theme',
    '<b>Documents on Table</b> \u2014 Added AADE 7-Ticket filing',
]
for v in v2_bullets:
    story.append(Paragraph(v, bullet, bulletText='\u2022'))

story.append(Spacer(1, 14))
story.append(HRFlowable(width='100%', color=BORDER, thickness=0.5, spaceAfter=6))
story.append(Paragraph(
    'IRS-CI Compact Interview Package v2 \u2014 Kyprianos Case \u2014 March 11, 2026',
    small))
story.append(Paragraph(
    'Prepared by Perplexity Computer for Stamatina Kyprianou',
    small))

# BUILD
doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
print(f'PDF generated: {output_path}')
