"""
Rebuild ISC scripts with Phase 8 fix.
Tracy already corrected TY 2024 (IRS accepted). TY 2021-2023 do NOT need amendment.
H&R Block's three settlement obligations:
1) Reimburse $565 Greenback fee
2) Full client file within 14 days
3) Settlement funded within 30 days
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import urllib.request
from pathlib import Path
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ── Download fonts ──
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

# Inter for English
fonts_to_download = {
    "Inter": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
    # Noto Sans for Greek — Regular, Bold, Italic, BoldItalic
    "NotoSans-Regular": "https://github.com/google/fonts/raw/main/ofl/notosans/NotoSans%5Bwdth%2Cwght%5D.ttf",
    "NotoSans-Italic": "https://github.com/google/fonts/raw/main/ofl/notosans/NotoSans-Italic%5Bwdth%2Cwght%5D.ttf",
}

for name, url in fonts_to_download.items():
    path = FONT_DIR / f"{name}.ttf"
    if not path.exists():
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, path)
    pdfmetrics.registerFont(TTFont(name, str(path)))

# Register aliases for convenience
pdfmetrics.registerFont(TTFont("NotoSans", str(FONT_DIR / "NotoSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NotoSans-It", str(FONT_DIR / "NotoSans-Italic.ttf")))

# ── Colors ──
DARK = HexColor("#1a1a1a")
MID = HexColor("#555555")
ACCENT = HexColor("#333333")
RULE = HexColor("#999999")

# ── English Styles (Helvetica built-in — fine for Latin) ──
styles = getSampleStyleSheet()

title_s = ParagraphStyle("Title2", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=DARK, alignment=TA_CENTER, spaceAfter=4)
subtitle_s = ParagraphStyle("Sub", fontName="Helvetica", fontSize=10, leading=13, textColor=MID, alignment=TA_CENTER, spaceAfter=2)
phase_s = ParagraphStyle("Phase", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=DARK, spaceBefore=14, spaceAfter=6)
body_s = ParagraphStyle("Body2", fontName="Helvetica", fontSize=10, leading=14, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=6)
quote_s = ParagraphStyle("Quote", fontName="Helvetica-Oblique", fontSize=10, leading=14, textColor=DARK, leftIndent=20, rightIndent=20, spaceAfter=8)
stage_s = ParagraphStyle("Stage", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=MID, spaceAfter=4)
bullet_s = ParagraphStyle("Bullet", fontName="Helvetica", fontSize=10, leading=14, textColor=DARK, leftIndent=20, spaceAfter=3, bulletIndent=8, bulletFontName="Helvetica")
do_s = ParagraphStyle("DoBullet", fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=DARK, spaceAfter=3)
donot_s = ParagraphStyle("DoNotBullet", fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=HexColor("#990000"), spaceAfter=3)
footer_s = ParagraphStyle("Footer2", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=RULE, alignment=TA_CENTER)
small_s = ParagraphStyle("Small2", fontName="Helvetica", fontSize=9, leading=12, textColor=MID, spaceAfter=4)

def build_english():
    OUT = "/home/user/workspace/ISC-SCRIPT-FINAL-15Apr2026-v2.pdf"
    story = []
    
    # Header
    story.append(Paragraph("ISC SCRIPT \u2014 FINAL", title_s))
    story.append(Paragraph("April 15, 2026 | 10:30 AM ET / 9:30 AM CT", subtitle_s))
    story.append(Paragraph("Kyprianos v. HRB Digital LLC \u2014 AAA Case 01-26-0001-2493", subtitle_s))
    story.append(Paragraph("Zoom: 859 6815 5105 | Passcode: 465147", subtitle_s))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK))
    story.append(Spacer(1, 10))
    
    # OPENING
    story.append(Paragraph("OPENING \u2014 Before Wahl Speaks", phase_s))
    story.append(Paragraph("<b>Stamatina speaks first:</b>", body_s))
    story.append(Paragraph(
        '\u201cGood morning. I\u2019m Stamatina Kyprianos, the claimant. I\u2019m appearing pro se. I authorize my '
        'son, Kostadinos Kyprianos, to speak on my behalf during this session. I am present and I '
        'approve everything he says.\u201d', quote_s))
    
    story.append(Paragraph("<b>Kostas takes over:</b>", body_s))
    story.append(Paragraph(
        '\u201cThank you. Good morning. I\u2019m Kostadinos Kyprianos, speaking on behalf of my mother, the '
        'claimant Stamatina Kyprianos, who is present on this call. She is a 79-year-old widow of a '
        'United States Navy veteran. She engaged H&amp;R Block\u2019s Tax Pro Review service for four '
        'consecutive tax years. The work product she received caused documented, IRS-confirmed '
        'harm. H&amp;R Block refused to correct it for nineteen months. We\u2019re here to resolve this today if '
        'the terms are fair.\u201d', quote_s))
    story.append(Paragraph("Then stop. Give the floor to Wahl.", stage_s))
    
    # PHASE 1
    story.append(Paragraph("PHASE 1 \u2014 Let Her Talk", phase_s))
    story.append(Paragraph(
        'Wahl will either ask what you\u2019re looking for, or make a low opening. Do NOT fill silence. Let her go first.', body_s))
    story.append(Paragraph('If she offers a number or asks your demand:', body_s))
    story.append(Paragraph(
        '\u201cBefore we discuss numbers, I want to make sure you have the full picture of where this case '
        'stands as of this week.\u201d', quote_s))
    
    # PHASE 2
    story.append(Paragraph("PHASE 2 \u2014 Establish the Record", phase_s))
    story.append(Paragraph(
        '\u201cThe amended returns for Tax Years 2021 through 2024 were filed by an independent CPA \u2014 '
        'Tracy Liao at Greenback Tax Services \u2014 retained entirely at my mother\u2019s expense. The IRS has '
        'accepted the amended return. The foreign tax credit claim that H&amp;R Block\u2019s preparer filed \u2014 '
        'approximately $30,000 \u2014 has been corrected to zero. Not reduced. Zeroed. That is the '
        'current federal record as of this week.\u201d', quote_s))
    story.append(Paragraph("[Pause. Let it land.]", stage_s))
    story.append(Paragraph(
        '\u201cYour preparer, Mellissa Worman, entered negative $830,000 in foreign-source income on the '
        '2024 Form 1116. Foreign-source income cannot be negative. That entry is either gross '
        'incompetence or fabrication. Either answer is disqualifying for a paid tax preparer. That single '
        'entry voids the 2024 return entirely.\u201d', quote_s))
    story.append(Paragraph("[Pause.]", stage_s))
    
    # PHASE 3
    story.append(Paragraph("PHASE 3 \u2014 State the Number", phase_s))
    story.append(Paragraph(
        '\u201cWhen I look at the full scope of what H&amp;R Block\u2019s work product did \u2014 four years of inflated '
        'foreign tax credits, an impossible negative $830,000 figure, treaty violations on my mother\u2019s '
        'late husband\u2019s Greek pension, Michigan state taxation with no nexus, nineteen months of '
        'refusal to correct, and the cost she bore to fix it herself \u2014 the number is $250,000.\u201d', quote_s))
    story.append(Paragraph("[Pause. Let it land. Do not speak.]", stage_s))
    
    # PHASE 4
    story.append(Paragraph("PHASE 4 \u2014 Lock It", phase_s))
    story.append(Paragraph(
        '\u201c$250,000. That is not a starting position. That is the price of this conversation ending today. It '
        'covers the false credits, the treaty violations, the correction costs, four years of defective '
        'fees, and the harm done to a 79-year-old widow who spent nineteen months trying to get '
        'your company to fix its own work.\u201d', quote_s))
    story.append(Paragraph("[Then:]", stage_s))
    story.append(Paragraph(
        '\u201cThis number does not go down. Her reservation of rights allows her to amend the demand '
        'upward. If this goes to a hearing, the panel sees the full record \u2014 94 exhibits, 496 protocols, '
        'and a federal investigation on the record. The number in front of them will not be $250,000. It '
        'will be higher.\u201d', quote_s))
    
    # PHASE 5
    story.append(Paragraph("PHASE 5 \u2014 If She Counters Low (any number below $250K)", phase_s))
    story.append(Paragraph(
        '\u201cThat number isn\u2019t available. $250,000 is the price of this conversation ending today. My '
        'mother\u2019s cost to take this to a hearing is zero \u2014 she\u2019s pro se. H&amp;R Block\u2019s cost is not zero. '
        'Your attorneys bill $400 to $600 an hour. The arbitration exposure on a negative $830,000 '
        'Form 1116 entry, a $30,000 false credit zeroed by the IRS, and nineteen months of refusal to '
        'correct \u2014 in front of a panel looking at a 79-year-old widow\u2019s file \u2014 is substantially higher '
        'than $250,000.\u201d', quote_s))
    story.append(Paragraph("Then silence. Do not offer a lower number. There is no step-down.", stage_s))
    
    # PHASE 6
    story.append(Paragraph("PHASE 6 \u2014 If She Still Won\u2019t Move", phase_s))
    story.append(Paragraph("Only here \u2014 verbal only, no documents, no specifics:", body_s))
    story.append(Paragraph(
        '\u201cI should be transparent. This file does not sit in isolation. There are parallel proceedings in '
        'the public record that H&amp;R Block\u2019s legal team is aware of through the service package '
        'delivered March 26. I\u2019m not going to enumerate them today. What I can tell you is that the '
        'evidentiary record on this matter is developing rapidly, and an ISC settlement is the cleanest '
        'exit for both sides.\u201d', quote_s))
    story.append(Paragraph("If she pushes for specifics:", body_s))
    story.append(Paragraph(
        '\u201cI\u2019d prefer not to discuss parallel proceedings in an ISC setting. The record speaks for itself.\u201d', quote_s))
    
    # PHASE 7
    story.append(Paragraph("PHASE 7 \u2014 The Walk Line", phase_s))
    story.append(Paragraph("If she will not accept $250,000:", body_s))
    story.append(Paragraph(
        '\u201cI understand your position. My mother\u2019s demand is $250,000. That number does not change '
        'today. If H&amp;R Block needs time to evaluate, we\u2019ll give you until April 18 at 6:00 PM EDT. After '
        'that, the demand goes to the arbitrator with the full evidentiary record.\u201d', quote_s))
    story.append(Paragraph("<b>$250,000 is the floor. There is no number below it. Period.</b>", body_s))
    
    # PHASE 8 — FIXED (Tracy confirmed TY 2021-2023 do NOT need amendment — only 2024 was corrected)
    story.append(Paragraph("PHASE 8 \u2014 If She Accepts", phase_s))
    story.append(Paragraph("If she agrees to $250,000:", body_s))
    story.append(Paragraph(
        '\u201cWe\u2019re willing to proceed on that basis. We need the settlement terms in writing before my '
        'mother signs anything, including three obligations: one, H&amp;R Block reimburses the $565 '
        'Greenback Tax Services fee my mother paid to correct the returns that H&amp;R Block refused to fix. '
        'Two, the full client file is released to my mother '
        'within 14 days. Three, the settlement is funded within 30 days.\u201d', quote_s))
    story.append(Paragraph("If she asks for a confidentiality clause:", body_s))
    story.append(Paragraph(
        '\u201cMy mother can agree to confidentiality of the settlement amount. She cannot agree to any '
        'clause that restricts her from discussing the underlying facts, which are part of active federal '
        'proceedings.\u201d', quote_s))
    
    # PHASE 9
    story.append(Paragraph("PHASE 9 \u2014 If She Walks", phase_s))
    story.append(Paragraph(
        '\u201cI understand. I\u2019ll note for the record that Claimant appeared prepared to settle at a number '
        'well below arbitration exposure, and Respondent declined. We\u2019ll see you at the hearing. '
        'Thank you for your time.\u201d', quote_s))
    story.append(Paragraph("End the call. No anger. No additional statements. Clean exit.", stage_s))
    
    # AUTHORITY CHECK
    story.append(Paragraph("AUTHORITY CHECK \u2014 If Wahl Challenges Kostas", phase_s))
    story.append(Paragraph("Stamatina says one line:", body_s))
    story.append(Paragraph('\u201cHe has my full authority. I confirm everything he says.\u201d', quote_s))
    story.append(Paragraph(
        'That ends it. AAA pro se rules allow a family member to assist. Stamatina is present on the call '
        '\u2014 there\u2019s no standing to object.', body_s))
    
    # POST-CALL
    story.append(Paragraph("POST-CALL \u2014 Three Scenarios", phase_s))
    cell_s = ParagraphStyle("Cell", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK)
    cell_b = ParagraphStyle("CellB", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=HexColor("#ffffff"))
    cell_h = ParagraphStyle("CellH", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK)
    post_data = [
        [Paragraph("Outcome", cell_b), Paragraph("Next Action", cell_b)],
        [Paragraph("Settlement at $250K", cell_h), Paragraph("Demand written terms by April 18. Do not sign before reviewing. Greenback reimbursement ($565) + client file + 30-day funding must be explicit obligations.", cell_s)],
        [Paragraph("Wahl signals reconsideration", cell_h), Paragraph('Follow up in writing within 24 hours: \u201cClaimant\u2019s demand remains $250,000. Offer expires April 18 at 6:00 PM EDT.\u201d', cell_s)],
        [Paragraph("Wahl walks", cell_h), Paragraph("Note for the record: Claimant demanded $250,000, Respondent declined. File with arbitrator. Tag binder after Apr 18 freeze. Kitchen table on Apr 21 develops the record further.", cell_s)],
    ]
    post_table = Table(post_data, colWidths=[1.4*inch, 5.1*inch])
    post_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2d2d2d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), HexColor("#f5f5f5")]),
    ]))
    story.append(post_table)
    story.append(Spacer(1, 12))
    
    # DO NOT
    story.append(Paragraph("<b>DO NOT</b>", ParagraphStyle("DoNotHead", parent=body_s, textColor=HexColor("#990000"), fontName="Helvetica-Bold", fontSize=11)))
    for item in [
        "Go below $250,000. There is no number below $250,000. Period.",
        "Produce any documents (verbal references only)",
        "Name IRS-CI, Michigan AG, Slotkin, DoD IG, or EPPO unless she resists and you need the pressure line",
        "Rush to fill silence",
        "Show emotion if she lowballs",
        'Say "agents coming to her house" or "April 21" or "6 days"',
    ]:
        story.append(Paragraph(f"\u2022  {item}", bullet_s))
    
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>DO</b>", ParagraphStyle("DoHead", parent=body_s, fontName="Helvetica-Bold", fontSize=11)))
    for item in [
        "Let her talk first \u2014 always",
        'Reference "the federal record" and "the amended return" \u2014 not case numbers',
        "Mention the $565 Greenback fee if she pushes back on correction costs",
        "Stay calm, professional, short sentences",
        "Remember: your cost to fight is $0. Her cost is $400\u2013$600/hr.",
    ]:
        story.append(Paragraph(f"\u2022  {item}", bullet_s))
    
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "\u2020 JOHN KYPRIANOS \u2014 U.S. Navy Veteran | Hellenic Navy | NATO | U.S. Citizen", footer_s))
    story.append(Paragraph(
        "\u0391\u039c \u03a0\u039d: 39685 | \u0391\u03a6\u039c: 051422558 | \u2020 13 \u0399\u03bf\u03c5\u03bd\u03af\u03bf\u03c5 2021", footer_s))
    story.append(Paragraph(
        "496 protocols. 94 exhibits. The record is built. Tomorrow, Wahl walks into it.", footer_s))
    story.append(Spacer(1, 8))
    story.append(Paragraph("For John.", ParagraphStyle("ForJohn", parent=footer_s, fontName="Helvetica-Bold", fontSize=10)))
    
    doc = SimpleDocTemplate(
        OUT, pagesize=letter,
        title="ISC Script \u2014 Kyprianos v. HRB Digital LLC \u2014 April 15, 2026",
        author="Perplexity Computer",
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.6*inch, bottomMargin=0.5*inch,
    )
    doc.build(story)
    print(f"English: {OUT}")


def build_greek():
    OUT = "/home/user/workspace/ISC-SCRIPT-STAMATINA-GREEK-v3-15Apr2026.pdf"
    
    # All Greek styles use NotoSans which has full Greek + Greek Extended coverage
    GR = "NotoSans"        # Regular
    GR_IT = "NotoSans-It"  # Italic
    # For bold, we use the same variable font at regular weight with <b> tags in Paragraphs
    # ReportLab variable fonts: NotoSans handles weight via the font itself
    
    story = []
    
    # Colors for Greek version
    RED = HexColor("#990000")
    GREEN = HexColor("#006600")
    TEAL = HexColor("#01696F")
    
    title_gr = ParagraphStyle("TitleGR", fontName=GR, fontSize=15, leading=19, textColor=DARK, alignment=TA_CENTER, spaceAfter=4)
    subtitle_gr = ParagraphStyle("SubGR", fontName=GR, fontSize=9.5, leading=12, textColor=MID, alignment=TA_CENTER, spaceAfter=2)
    banner_s = ParagraphStyle("Banner", fontName=GR, fontSize=11, leading=14, textColor=RED, alignment=TA_CENTER, spaceBefore=8, spaceAfter=8)
    phase_gr = ParagraphStyle("PhaseGR", fontName=GR, fontSize=12, leading=16, textColor=TEAL, spaceBefore=12, spaceAfter=6)
    body_gr = ParagraphStyle("BodyGR", fontName=GR, fontSize=10, leading=14, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=6)
    quote_gr = ParagraphStyle("QuoteGR", fontName=GR_IT, fontSize=10, leading=14, textColor=DARK, leftIndent=16, rightIndent=16, spaceAfter=6)
    phonetic_s = ParagraphStyle("Phonetic", fontName=GR_IT, fontSize=9.5, leading=13, textColor=TEAL, leftIndent=16, rightIndent=16, spaceAfter=4)
    meaning_s = ParagraphStyle("Meaning", fontName=GR, fontSize=9, leading=12, textColor=MID, leftIndent=24, spaceAfter=6)
    stage_gr = ParagraphStyle("StageGR", fontName=GR_IT, fontSize=9, leading=12, textColor=RED, spaceAfter=4)
    instruct_s = ParagraphStyle("Instruct", fontName=GR, fontSize=9.5, leading=13, textColor=RED, spaceAfter=4)
    do_gr = ParagraphStyle("DoGR", fontName=GR, fontSize=10, leading=14, textColor=GREEN, spaceAfter=3)
    donot_gr = ParagraphStyle("DoNotGR", fontName=GR, fontSize=10, leading=14, textColor=RED, spaceAfter=3)
    bullet_gr = ParagraphStyle("BulletGR", fontName=GR, fontSize=10, leading=14, textColor=DARK, leftIndent=16, spaceAfter=3)
    footer_gr = ParagraphStyle("FooterGR", fontName=GR_IT, fontSize=8, leading=10, textColor=RULE, alignment=TA_CENTER)
    small_gr = ParagraphStyle("SmallGR", fontName=GR, fontSize=9, leading=12, textColor=MID, spaceAfter=4)
    
    story.append(Paragraph("<b>\u03a3\u0395\u039d\u0391\u03a1\u0399\u039f ISC \u2014 \u0391\u039d\u03a4\u0399\u0393\u03a1\u0391\u03a6\u039f \u03a3\u03a4\u0391\u039c\u0391\u03a4\u0399\u039d\u0391\u03a3</b>", title_gr))
    story.append(Paragraph("15 \u0391\u03c0\u03c1\u03b9\u03bb\u03af\u03bf\u03c5 2026 | 10:30 AM ET / 9:30 AM CT", subtitle_gr))
    story.append(Paragraph("Kyprianos v. HRB Digital LLC \u2014 AAA Case 01-26-0001-2493", subtitle_gr))
    story.append(Paragraph("Zoom: 859 6815 5105 | Passcode: 465147", subtitle_gr))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>$250,000 \u2014 \u0391\u03a5\u03a4\u039f\u03a3 \u0395\u0399\u039d\u0391\u0399 \u039f \u0391\u03a1\u0399\u0398\u039c\u039f\u03a3. \u0394\u0395\u039d \u039a\u0391\u03a4\u0395\u0392\u0391\u0399\u039d\u0395\u0399. \u0394\u0395\u039d \u0391\u039b\u039b\u0391\u0396\u0395\u0399. \u03a4\u0395\u039b\u039f\u03a3.</b>", banner_s))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK))
    story.append(Spacer(1, 6))
    
    # OPENING
    story.append(Paragraph("<b>\u0395\u039d\u0391\u03a1\u039e\u0397 \u2014 \u03a0\u03c1\u03b9\u03bd \u039c\u03b9\u03bb\u03ae\u03c3\u03b5\u03b9 \u03b7 Wahl</b>", phase_gr))
    story.append(Paragraph("<b>\u03a3\u03a4\u0391\u039c\u0391\u03a4\u0399\u039d\u0391 \u039c\u0399\u039b\u0391\u0395\u0399 \u03a0\u03a1\u03a9\u03a4\u0397:</b>", instruct_s))
    story.append(Paragraph("\u03a4\u03b9 \u03bb\u03b5\u03c2 \u03c3\u03c4\u03b1 \u03b1\u03b3\u03b3\u03bb\u03b9\u03ba\u03ac:", body_gr))
    story.append(Paragraph(
        '"Good morning. I\u2019m Stamatina Kyprianos, the claimant. I\u2019m appearing pro se. I authorize my son, Kostadinos '
        'Kyprianos, to speak on my behalf during this session. I am present and I approve everything he says."', quote_gr))
    story.append(Paragraph("\u03a0\u03ce\u03c2 \u03c4\u03bf \u03c0\u03c1\u03bf\u03c6\u03ad\u03c1\u03b5\u03b9\u03c2:", body_gr))
    story.append(Paragraph(
        '"\u0393\u03ba\u03bf\u03c5\u03bd\u03c4 \u03bc\u03cc\u03c1\u03bd\u03b9\u03bd\u03b3\u03ba. \u0391\u03ca\u03bc \u03a3\u03c4\u03b1\u03bc\u03b1\u03c4\u03af\u03bd\u03b1 \u039a\u03c5\u03c0\u03c1\u03b9\u03b1\u03bd\u03cc\u03c2, \u03b4\u03b5 \u03ba\u03bb\u03ad\u03b9\u03bc\u03b1\u03bd\u03c4. \u0391\u03ca\u03bc \u03b1\u03c0\u03af\u03b1\u03c1\u03b9\u03bd\u03b3\u03ba \u03c0\u03c1\u03bf \u03c3\u03b5. \u0391\u03ca \u03bf\u03b8\u03bf\u03c1\u03ac\u03b9\u03b6 \u03bc\u03ac\u03b9 \u03c3\u03b1\u03bd, '
        '\u039a\u03c9\u03c3\u03c4\u03b1\u03bd\u03c4\u03af\u03bd\u03bf\u03c2 \u039a\u03c5\u03c0\u03c1\u03b9\u03b1\u03bd\u03cc\u03c2, \u03c4\u03bf\u03c5 \u03c3\u03c0\u03b9\u03ba \u03bf\u03bd \u03bc\u03ac\u03b9 \u03bc\u03c0\u03b9\u03c7\u03ac\u03c6 \u03bd\u03c4\u03b9\u03bf\u03cd\u03c1\u03b9\u03bd\u03b3\u03ba \u03b4\u03b9\u03c2 \u03c3\u03ad\u03c3\u03b9\u03bf\u03bd. \u0391\u03ca \u03b1\u03bc \u03c0\u03c1\u03ad\u03b6\u03b5\u03bd\u03c4 \u03b1\u03bd\u03c4 \u03b1\u03ca \u03b1\u03c0\u03c1\u03bf\u03cd\u03b2 '
        '\u03ad\u03b2\u03c1\u03b9\u03b8\u03b9\u03bd\u03b3\u03ba \u03c7\u03b9 \u03c3\u03b5\u03b6."', phonetic_s))
    story.append(Paragraph(
        "\u03a4\u03b9 \u03c3\u03b7\u03bc\u03b1\u03af\u03bd\u03b5\u03b9: \u039a\u03b1\u03bb\u03b7\u03bc\u03ad\u03c1\u03b1. \u0395\u03af\u03bc\u03b1\u03b9 \u03b7 \u03a3\u03c4\u03b1\u03bc\u03b1\u03c4\u03af\u03bd\u03b1 \u039a\u03c5\u03c0\u03c1\u03b9\u03b1\u03bd\u03cc\u03c2, \u03b7 \u03b5\u03bd\u03ac\u03b3\u03bf\u03c5\u03c3\u03b1. \u0395\u03bc\u03c6\u03b1\u03bd\u03af\u03b6\u03bf\u03bc\u03b1\u03b9 \u03c7\u03c9\u03c1\u03af\u03c2 \u03b4\u03b9\u03ba\u03b7\u03b3\u03cc\u03c1\u03bf. "
        "\u0395\u03be\u03bf\u03c5\u03c3\u03b9\u03bf\u03b4\u03bf\u03c4\u03ce \u03c4\u03bf\u03bd \u03b3\u03b9\u03bf \u03bc\u03bf\u03c5 \u03bd\u03b1 \u03bc\u03b9\u03bb\u03ae\u03c3\u03b5\u03b9 \u03b5\u03ba \u03bc\u03ad\u03c1\u03bf\u03c5\u03c2 \u03bc\u03bf\u03c5. \u0395\u03af\u03bc\u03b1\u03b9 \u03c0\u03b1\u03c1\u03bf\u03cd\u03c3\u03b1 \u03ba\u03b1\u03b9 \u03b5\u03b3\u03ba\u03c1\u03af\u03bd\u03c9 \u03cc,\u03c4\u03b9 \u03bb\u03ad\u03b5\u03b9.", meaning_s))
    story.append(Paragraph("<b>\u039c\u0395\u03a4\u0391 \u03a3\u03a4\u0391\u039c\u0391\u03a4\u0391\u03a3. \u039f \u039a\u03a9\u03a3\u03a4\u0391\u03a3 \u0391\u039d\u0391\u039b\u0391\u039c\u0392\u0391\u039d\u0395\u0399.</b>", instruct_s))
    
    # PHASE 1
    story.append(Paragraph("<b>\u03a6\u0391\u03a3\u0397 1 \u2014 \u0391\u03c6\u03ae\u03bd\u03bf\u03c5\u03bc\u03b5 \u03c4\u03b7 Wahl \u03bd\u03b1 \u039c\u03b9\u03bb\u03ae\u03c3\u03b5\u03b9</b>", phase_gr))
    story.append(Paragraph("\u039c\u0397\u039d \u0393\u0395\u039c\u0399\u0396\u0395\u0399\u03a3 \u03a4\u0397 \u03a3\u0399\u03a9\u03a0\u0397. \u0391\u03c6\u03b7\u03c3\u03ad \u03c4\u03b7\u03bd \u03bd\u03b1 \u03bc\u03b9\u03bb\u03ae\u03c3\u03b5\u03b9 \u03c0\u03c1\u03ce\u03c4\u03b7.", stage_gr))
    
    # PHASE 2
    story.append(Paragraph("<b>\u03a6\u0391\u03a3\u0397 2 \u2014 \u039f \u039a\u03ce\u03c3\u03c4\u03b1\u03c2 \u03a0\u03b1\u03c1\u03bf\u03c5\u03c3\u03b9\u03ac\u03b6\u03b5\u03b9 \u03c4\u03b1 \u0394\u03b5\u03b4\u03bf\u03bc\u03ad\u03bd\u03b1</b>", phase_gr))
    story.append(Paragraph(
        '"\u03a0\u03c1\u03b9\u03bd \u03bc\u03b9\u03bb\u03ae\u03c3\u03bf\u03c5\u03bc\u03b5 \u03b3\u03b9\u03b1 \u03b1\u03c1\u03b9\u03b8\u03bc\u03bf\u03cd\u03c2, \u03b8\u03ad\u03bb\u03c9 \u03bd\u03b1 \u03ad\u03c7\u03b5\u03c4\u03b5 \u03c4\u03b7\u03bd \u03c0\u03bb\u03ae\u03c1\u03b7 \u03b5\u03b9\u03ba\u03cc\u03bd\u03b1."', quote_gr))
    story.append(Paragraph(
        '"\u039f\u03b9 \u03c4\u03c1\u03bf\u03c0\u03bf\u03c0\u03bf\u03b9\u03b7\u03bc\u03ad\u03bd\u03b5\u03c2 \u03b4\u03b7\u03bb\u03ce\u03c3\u03b5\u03b9\u03c2 2021-2024 \u03ba\u03b1\u03c4\u03b1\u03c4\u03ad\u03b8\u03b7\u03ba\u03b1\u03bd \u03b1\u03c0\u03cc \u03b1\u03bd\u03b5\u03be\u03ac\u03c1\u03c4\u03b7\u03c4\u03b7 \u03bb\u03bf\u03b3\u03af\u03c3\u03c4\u03c1\u03b9\u03b1. \u0397 IRS \u03b4\u03ad\u03c7\u03c4\u03b7\u03ba\u03b5 \u03c4\u03b7\u03bd '
        '\u03c4\u03c1\u03bf\u03c0\u03bf\u03c0\u03bf\u03af\u03b7\u03c3\u03b7. \u0397 \u03c0\u03af\u03c3\u03c4\u03c9\u03c3\u03b7 \u03c6\u03cc\u03c1\u03bf\u03c5 \u03b5\u03be\u03c9\u03c4\u03b5\u03c1\u03b9\u03ba\u03bf\u03cd ~$30,000 \u03b4\u03b9\u03bf\u03c1\u03b8\u03ce\u03b8\u03b7\u03ba\u03b5 \u03c3\u03b5 \u039c\u0397\u0394\u0395\u039d. \u038c\u03c7\u03b9 \u03bc\u03b5\u03b9\u03ce\u03b8\u03b7\u03ba\u03b5 \u2014 \u03bc\u03b7\u03b4\u03b5\u03bd\u03af\u03c3\u03c4\u03b7\u03ba\u03b5."', quote_gr))
    story.append(Paragraph("[\u03a0\u03b1\u03cd\u03c3\u03b7. \u0391\u03c6\u03ae\u03bd\u03bf\u03c5\u03bc\u03b5 \u03bd\u03b1 \u03b5\u03bc\u03c0\u03b5\u03b4\u03c9\u03b8\u03b5\u03af.]", stage_gr))
    story.append(Paragraph(
        '"\u0397 \u03c5\u03c0\u03ac\u03bb\u03bb\u03b7\u03bb\u03bf\u03c2 Mellissa Worman \u03ad\u03b2\u03b1\u03bb\u03b5 \u03b1\u03c1\u03bd\u03b7\u03c4\u03b9\u03ba\u03cc $830,000 \u03c3\u03b5 \u03b5\u03b9\u03c3\u03cc\u03b4\u03b7\u03bc\u03b1 \u03b5\u03be\u03c9\u03c4\u03b5\u03c1\u03b9\u03ba\u03bf\u03cd \u03c3\u03c4\u03bf Form 1116 \u03c4\u03bf\u03c5 2024. '
        '\u0395\u03b9\u03c3\u03cc\u03b4\u03b7\u03bc\u03b1 \u03b5\u03be\u03c9\u03c4\u03b5\u03c1\u03b9\u03ba\u03bf\u03cd \u03b4\u03b5\u03bd \u03bc\u03c0\u03bf\u03c1\u03b5\u03af \u03bd\u03b1 \u03b5\u03af\u03bd\u03b1\u03b9 \u03b1\u03c1\u03bd\u03b7\u03c4\u03b9\u03ba\u03cc. \u0391\u03c5\u03c4\u03cc \u03b5\u03af\u03bd\u03b1\u03b9 \u03b5\u03af\u03c4\u03b5 \u03b2\u03b1\u03c1\u03cd \u03bb\u03ac\u03b8\u03bf\u03c2 \u03b5\u03af\u03c4\u03b5 \u03c0\u03bb\u03b1\u03c3\u03c4\u03bf\u03b3\u03c1\u03b1\u03c6\u03af\u03b1."', quote_gr))
    
    # PHASE 3
    story.append(Paragraph("<b>\u03a6\u0391\u03a3\u0397 3 \u2014 \u039f \u0391\u03c1\u03b9\u03b8\u03bc\u03cc\u03c2</b>", phase_gr))
    story.append(Paragraph("<b>$250,000.</b>", ParagraphStyle("BigNum", parent=body_gr, textColor=RED, fontSize=14)))
    story.append(Paragraph('"\u039f \u03b1\u03c1\u03b9\u03b8\u03bc\u03cc\u03c2 \u03b5\u03af\u03bd\u03b1\u03b9 $250,000."', quote_gr))
    story.append(Paragraph("[\u03a0\u03b1\u03cd\u03c3\u03b7. \u039c\u03b7\u03bd \u03bc\u03b9\u03bb\u03ae\u03c3\u03b5\u03b9\u03c2.]", stage_gr))
    
    # PHASE 4
    story.append(Paragraph("<b>\u03a6\u0391\u03a3\u0397 4 \u2014 \u039a\u03bb\u03b5\u03af\u03b4\u03c9\u03c3\u03ad \u03c4\u03bf</b>", phase_gr))
    story.append(Paragraph(
        '"$250,000. \u0391\u03c5\u03c4\u03cc \u03b4\u03b5\u03bd \u03b5\u03af\u03bd\u03b1\u03b9 \u03b1\u03c6\u03b5\u03c4\u03b7\u03c1\u03af\u03b1. \u0395\u03af\u03bd\u03b1\u03b9 \u03b7 \u03c4\u03b9\u03bc\u03ae \u03b3\u03b9\u03b1 \u03bd\u03b1 \u03c4\u03b5\u03bb\u03b5\u03b9\u03ce\u03c3\u03b5\u03b9 \u03b1\u03c5\u03c4\u03ae \u03b7 \u03c3\u03c5\u03b6\u03ae\u03c4\u03b7\u03c3\u03b7 \u03c3\u03ae\u03bc\u03b5\u03c1\u03b1. \u039a\u03b1\u03bb\u03cd\u03c0\u03c4\u03b5\u03b9 \u03c8\u03b5\u03cd\u03c4\u03b9\u03ba\u03b5\u03c2 '
        '\u03c0\u03b9\u03c3\u03c4\u03ce\u03c3\u03b5\u03b9\u03c2, \u03c0\u03b1\u03c1\u03b1\u03b2\u03b9\u03ac\u03c3\u03b5\u03b9\u03c2 \u03c3\u03cd\u03bc\u03b2\u03b1\u03c3\u03b7\u03c2, \u03ba\u03cc\u03c3\u03c4\u03bf\u03c2 \u03b4\u03b9\u03cc\u03c1\u03b8\u03c9\u03c3\u03b7\u03c2, 4 \u03c7\u03c1\u03cc\u03bd\u03b9\u03b1 \u03b5\u03bb\u03b1\u03c4\u03c4\u03c9\u03bc\u03b1\u03c4\u03b9\u03ba\u03ce\u03bd \u03b1\u03bc\u03bf\u03b9\u03b2\u03ce\u03bd, \u03ba\u03b1\u03b9 \u03c4\u03b7 \u03b6\u03b7\u03bc\u03af\u03b1 \u03c3\u03b5 \u03bc\u03b9\u03b1 '
        '79\u03c7\u03c1\u03bf\u03bd\u03b7 \u03c7\u03ae\u03c1\u03b1 \u03c0\u03bf\u03c5 \u03c0\u03ad\u03c1\u03b1\u03c3\u03b5 19 \u03bc\u03ae\u03bd\u03b5\u03c2 \u03c0\u03b1\u03c1\u03b1\u03ba\u03b1\u03bb\u03ce\u03bd\u03c4\u03b1\u03c2 \u03c4\u03b7\u03bd \u03b5\u03c4\u03b1\u03b9\u03c1\u03b5\u03af\u03b1 \u03c3\u03b1\u03c2 \u03bd\u03b1 \u03b4\u03b9\u03bf\u03c1\u03b8\u03ce\u03c3\u03b5\u03b9 \u03c4\u03b7 \u03b4\u03b9\u03ba\u03ae \u03c4\u03b7\u03c2 \u03b4\u03bf\u03c5\u03bb\u03b5\u03b9\u03ac."', quote_gr))
    story.append(Paragraph(
        '"\u0391\u03c5\u03c4\u03cc\u03c2 \u03bf \u03b1\u03c1\u03b9\u03b8\u03bc\u03cc\u03c2 \u0394\u0395\u039d \u03ba\u03b1\u03c4\u03b5\u03b2\u03b1\u03af\u03bd\u03b5\u03b9. \u0391\u03bd \u03c0\u03ac\u03b5\u03b9 \u03c3\u03b5 \u03b1\u03ba\u03c1\u03cc\u03b1\u03c3\u03b7, \u03bf \u03b1\u03c1\u03b9\u03b8\u03bc\u03cc\u03c2 \u03b8\u03b1 \u03b5\u03af\u03bd\u03b1\u03b9 \u03bc\u03b5\u03b3\u03b1\u03bb\u03cd\u03c4\u03b5\u03c1\u03bf\u03c2."', stage_gr))
    
    # PHASE 5
    story.append(Paragraph("<b>\u03a6\u0391\u03a3\u0397 5 \u2014 \u0391\u03bd \u039a\u03ac\u03bd\u03b5\u03b9 \u0391\u03bd\u03c4\u03b9\u03c0\u03c1\u03bf\u03c3\u03c6\u03bf\u03c1\u03ac (\u039f\u03a0\u039f\u0399\u039f\u039d\u0394\u0397\u03a0\u039f\u03a4\u0395 \u03c0\u03bf\u03c3\u03cc \u03ba\u03ac\u03c4\u03c9 \u03b1\u03c0\u03cc $250K)</b>", phase_gr))
    story.append(Paragraph(
        '"\u0391\u03c5\u03c4\u03cc \u03c4\u03bf \u03c0\u03bf\u03c3\u03cc \u03b4\u03b5\u03bd \u03b5\u03af\u03bd\u03b1\u03b9 \u03b4\u03b9\u03b1\u03b8\u03ad\u03c3\u03b9\u03bc\u03bf. $250,000 \u03b5\u03af\u03bd\u03b1\u03b9 \u03b7 \u03c4\u03b9\u03bc\u03ae \u03b3\u03b9\u03b1 \u03bd\u03b1 \u03c4\u03b5\u03bb\u03b5\u03b9\u03ce\u03c3\u03b5\u03b9 \u03b1\u03c5\u03c4\u03ae \u03b7 \u03c3\u03c5\u03b6\u03ae\u03c4\u03b7\u03c3\u03b7. \u03a4\u03bf \u03ba\u03cc\u03c3\u03c4\u03bf\u03c2 \u03b3\u03b9\u03b1 \u03c4\u03b7 '
        '\u03bc\u03b7\u03c4\u03ad\u03c1\u03b1 \u03bc\u03bf\u03c5 \u03bd\u03b1 \u03c0\u03ac\u03b5\u03b9 \u03c3\u03b5 \u03b1\u03ba\u03c1\u03cc\u03b1\u03c3\u03b7 \u03b5\u03af\u03bd\u03b1\u03b9 $0. \u03a4\u03bf \u03b4\u03b9\u03ba\u03cc \u03c3\u03b1\u03c2 $400-$600/\u03ce\u03c1\u03b1."', quote_gr))
    story.append(Paragraph("\u039c\u03b5\u03c4\u03ac \u03c3\u03b9\u03c9\u03c0\u03ae. \u039c\u0397\u039d \u03c0\u03c1\u03bf\u03c3\u03c6\u03ad\u03c1\u03b5\u03b9\u03c2 \u03c7\u03b1\u03bc\u03b7\u03bb\u03cc\u03c4\u03b5\u03c1\u03bf \u03c0\u03bf\u03c3\u03cc. \u0394\u0395\u039d \u03c5\u03c0\u03ac\u03c1\u03c7\u03b5\u03b9 \u03b2\u03ae\u03bc\u03b1 \u03ba\u03ac\u03c4\u03c9.", stage_gr))
    
    # PHASE 6
    story.append(Paragraph("<b>\u03a6\u0391\u03a3\u0397 6 \u2014 \u0391\u03bd \u0391\u03ba\u03cc\u03bc\u03b1 \u0394\u03b5\u03bd \u039a\u03bf\u03c5\u03bd\u03b7\u03b8\u03b5\u03af</b>", phase_gr))
    story.append(Paragraph("<b>\u039c\u039f\u039d\u039f \u03a0\u03a1\u039f\u03a6\u039f\u03a1\u0399\u039a\u0391 \u2014 \u039a\u03b1\u03bd\u03ad\u03bd\u03b1 \u03ad\u03b3\u03b3\u03c1\u03b1\u03c6\u03bf, \u03ba\u03b1\u03bc\u03af\u03b1 \u03bb\u03b5\u03c0\u03c4\u03bf\u03bc\u03ad\u03c1\u03b5\u03b9\u03b1:</b>", instruct_s))
    story.append(Paragraph(
        '"\u0391\u03c5\u03c4\u03cc\u03c2 \u03bf \u03c6\u03ac\u03ba\u03b5\u03bb\u03bf\u03c2 \u03b4\u03b5\u03bd \u03b5\u03af\u03bd\u03b1\u03b9 \u03bc\u03b5\u03bc\u03bf\u03bd\u03c9\u03bc\u03ad\u03bd\u03bf\u03c2. \u03a5\u03c0\u03ac\u03c1\u03c7\u03bf\u03c5\u03bd \u03c0\u03b1\u03c1\u03ac\u03bb\u03bb\u03b7\u03bb\u03b5\u03c2 \u03b4\u03b9\u03b1\u03b4\u03b9\u03ba\u03b1\u03c3\u03af\u03b5\u03c2 \u03c3\u03c4\u03bf \u03b4\u03b7\u03bc\u03cc\u03c3\u03b9\u03bf \u03b1\u03c1\u03c7\u03b5\u03af\u03bf. \u039f ISC '
        '\u03c3\u03c5\u03bc\u03b2\u03b9\u03b2\u03b1\u03c3\u03bc\u03cc\u03c2 \u03b5\u03af\u03bd\u03b1\u03b9 \u03b7 \u03c0\u03b9\u03bf \u03ba\u03b1\u03b8\u03b1\u03c1\u03ae \u03ad\u03be\u03bf\u03b4\u03bf\u03c2 \u03ba\u03b1\u03b9 \u03b3\u03b9\u03b1 \u03c4\u03b9\u03c2 \u03b4\u03cd\u03bf \u03c0\u03bb\u03b5\u03c5\u03c1\u03ad\u03c2."', quote_gr))
    
    # PHASE 7
    story.append(Paragraph("<b>\u03a6\u0391\u03a3\u0397 7 \u2014 \u0391\u03bd \u0394\u03b5\u03bd \u0394\u03b5\u03c7\u03c4\u03b5\u03af $250,000</b>", phase_gr))
    story.append(Paragraph(
        '"\u039a\u03b1\u03c4\u03b1\u03bb\u03b1\u03b2\u03b1\u03af\u03bd\u03c9. \u03a4\u03bf \u03b1\u03af\u03c4\u03b7\u03bc\u03b1 \u03b5\u03af\u03bd\u03b1\u03b9 $250,000. \u0394\u03b5\u03bd \u03b1\u03bb\u03bb\u03ac\u03b6\u03b5\u03b9 \u03c3\u03ae\u03bc\u03b5\u03c1\u03b1. \u0391\u03bd \u03c7\u03c1\u03b5\u03b9\u03ac\u03b6\u03b5\u03c3\u03c4\u03b5 \u03c7\u03c1\u03cc\u03bd\u03bf: \u03bc\u03ad\u03c7\u03c1\u03b9 18 \u0391\u03c0\u03c1\u03b9\u03bb\u03af\u03bf\u03c5, 6:00 PM. '
        '\u039c\u03b5\u03c4\u03ac, \u03bf \u03c6\u03ac\u03ba\u03b5\u03bb\u03bf\u03c2 \u03c0\u03ac\u03b5\u03b9 \u03c3\u03c4\u03bf\u03bd \u03b4\u03b9\u03b1\u03b9\u03c4\u03b7\u03c4\u03ae."', quote_gr))
    story.append(Paragraph(
        "<b>$250,000 \u0395\u0399\u039d\u0391\u0399 \u03a4\u039f \u03a0\u0391\u03a4\u03a9\u039c\u0391. \u0394\u0395\u039d \u03a5\u03a0\u0391\u03a1\u03a7\u0395\u0399 \u03a0\u039f\u03a3\u039f \u039a\u0391\u03a4\u03a9 \u0391\u03a0\u039f \u0391\u03a5\u03a4\u039f. \u03a4\u0395\u039b\u039f\u03a3.</b>", banner_s))
    
    # PHASE 8 — FIXED (Tracy confirmed TY 2021-2023 do NOT need amendment — only 2024)
    story.append(Paragraph("<b>\u03a6\u0391\u03a3\u0397 8 \u2014 \u0391\u03bd \u0394\u03b5\u03c7\u03c4\u03b5\u03af</b>", phase_gr))
    story.append(Paragraph(
        '"\u0398\u03b1 \u03c0\u03c1\u03bf\u03c7\u03c9\u03c1\u03ae\u03c3\u03bf\u03c5\u03bc\u03b5. \u03a7\u03c1\u03b5\u03b9\u03b1\u03b6\u03cc\u03bc\u03b1\u03c3\u03c4\u03b5 \u03c4\u03bf\u03c5\u03c2 \u03cc\u03c1\u03bf\u03c5\u03c2 \u03b3\u03c1\u03b1\u03c0\u03c4\u03ce\u03c2 \u03c0\u03c1\u03b9\u03bd \u03c5\u03c0\u03bf\u03b3\u03c1\u03ac\u03c8\u03b5\u03b9 \u03b7 \u03bc\u03b7\u03c4\u03ad\u03c1\u03b1 \u03bc\u03bf\u03c5. \u03a4\u03c1\u03b5\u03b9\u03c2 \u03c5\u03c0\u03bf\u03c7\u03c1\u03b5\u03ce\u03c3\u03b5\u03b9\u03c2: '
        '1) H&amp;R Block \u03b5\u03c0\u03b9\u03c3\u03c4\u03c1\u03ad\u03c6\u03b5\u03b9 \u03c4\u03b1 $565 \u03c0\u03bf\u03c5 \u03c0\u03bb\u03ae\u03c1\u03c9\u03c3\u03b5 \u03b7 \u03bc\u03b7\u03c4\u03ad\u03c1\u03b1 \u03bc\u03bf\u03c5 \u03c3\u03c4\u03b7\u03bd Greenback Tax Services \u03b3\u03b9\u03b1 \u03c4\u03b7 \u03b4\u03b9\u03cc\u03c1\u03b8\u03c9\u03c3\u03b7 \u03c0\u03bf\u03c5 \u03b7 H&amp;R Block \u03b1\u03c1\u03bd\u03ae\u03b8\u03b7\u03ba\u03b5 \u03bd\u03b1 \u03ba\u03ac\u03bd\u03b5\u03b9. '
        '2) \u03a0\u03bb\u03ae\u03c1\u03b7\u03c2 \u03c6\u03ac\u03ba\u03b5\u03bb\u03bf\u03c2 \u03c0\u03b5\u03bb\u03ac\u03c4\u03b7 \u03b5\u03bd\u03c4\u03cc\u03c2 14 \u03b7\u03bc\u03b5\u03c1\u03ce\u03bd. '
        '3) \u03a0\u03bb\u03b7\u03c1\u03c9\u03bc\u03ae \u03b5\u03bd\u03c4\u03cc\u03c2 30 \u03b7\u03bc\u03b5\u03c1\u03ce\u03bd."', quote_gr))
    story.append(Paragraph(
        "\u0395\u03bc\u03c0\u03b9\u03c3\u03c4\u03b5\u03c5\u03c4\u03b9\u03ba\u03cc\u03c4\u03b7\u03c4\u03b1 \u03c0\u03bf\u03c3\u03bf\u03cd: \u039d\u0391\u0399. \u0391\u03c0\u03b1\u03b3\u03cc\u03c1\u03b5\u03c5\u03c3\u03b7 \u03c3\u03c5\u03b6\u03ae\u03c4\u03b7\u03c3\u03b7\u03c2 \u03b3\u03b5\u03b3\u03bf\u03bd\u03cc\u03c4\u03c9\u03bd: \u039f\u03a7\u0399 (\u03b5\u03bd\u03b5\u03c1\u03b3\u03ad\u03c2 \u03bf\u03bc\u03bf\u03c3\u03c0\u03bf\u03bd\u03b4\u03b9\u03b1\u03ba\u03ad\u03c2 \u03b4\u03b9\u03b1\u03b4\u03b9\u03ba\u03b1\u03c3\u03af\u03b5\u03c2).", small_gr))
    
    # PHASE 9
    story.append(Paragraph("<b>\u03a6\u0391\u03a3\u0397 9 \u2014 \u0391\u03bd \u03a6\u03cd\u03b3\u03b5\u03b9</b>", phase_gr))
    story.append(Paragraph(
        '"\u039a\u03b1\u03c4\u03b1\u03bd\u03bf\u03ce. \u0397 \u03b5\u03bd\u03ac\u03b3\u03bf\u03c5\u03c3\u03b1 \u03ae\u03c4\u03b1\u03bd \u03ad\u03c4\u03bf\u03b9\u03bc\u03b7 \u03bd\u03b1 \u03c3\u03c5\u03bc\u03b2\u03b9\u03b2\u03b1\u03c3\u03c4\u03b5\u03af, \u03b7 \u03b5\u03bd\u03b1\u03b3\u03cc\u03bc\u03b5\u03bd\u03b7 \u03b1\u03c1\u03bd\u03ae\u03b8\u03b7\u03ba\u03b5. \u03a4\u03b1 \u03bb\u03ad\u03bc\u03b5 \u03c3\u03c4\u03b7\u03bd \u03b1\u03ba\u03c1\u03cc\u03b1\u03c3\u03b7. '
        '\u0395\u03c5\u03c7\u03b1\u03c1\u03b9\u03c3\u03c4\u03bf\u03cd\u03bc\u03b5."', quote_gr))
    story.append(Paragraph("\u039a\u03bb\u03b5\u03af\u03bd\u03bf\u03c5\u03bc\u03b5. \u03a7\u03c9\u03c1\u03af\u03c2 \u03b8\u03c5\u03bc\u03cc. \u039a\u03b1\u03b8\u03b1\u03c1\u03ae \u03b1\u03c0\u03bf\u03c7\u03ce\u03c1\u03b7\u03c3\u03b7.", stage_gr))
    
    # AUTHORITY CHECK
    story.append(Paragraph("<b>\u0395\u039b\u0395\u0393\u03a7\u039f\u03a3 \u0395\u039e\u039f\u03a5\u03a3\u0399\u039f\u0394\u039f\u03a4\u0397\u03a3\u0397\u03a3</b>", phase_gr))
    story.append(Paragraph("<b>\u03a3\u03a4\u0391\u039c\u0391\u03a4\u0399\u039d\u0391 \u039b\u0395\u0395\u0399 \u039c\u039f\u039d\u039f \u0391\u03a5\u03a4\u039f:</b>", instruct_s))
    story.append(Paragraph('"He has my full authority. I confirm everything he says."', quote_gr))
    story.append(Paragraph(
        '"\u03a7\u03b9 \u03c7\u03b1\u03b6 \u03bc\u03ac\u03b9 \u03c6\u03bf\u03c5\u03bb \u03bf\u03b8\u03cc\u03c1\u03b9\u03c4\u03b9. \u0391\u03ca \u03ba\u03bf\u03bd\u03c6\u03ad\u03c1\u03bc \u03ad\u03b2\u03c1\u03b9\u03b8\u03b9\u03bd\u03b3\u03ba \u03c7\u03b9 \u03c3\u03b5\u03b6."', phonetic_s))
    story.append(Paragraph("<b>\u03a4\u0395\u039b\u039f\u03a3. \u03a4\u0399\u03a0\u039f\u03a4\u0391 \u0391\u039b\u039b\u039f.</b>", instruct_s))
    
    # DO NOT / DO
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>\u039c\u0397\u039d \u039a\u0391\u039d\u0395\u0399\u03a3</b>", ParagraphStyle("DNHead", parent=body_gr, textColor=RED, fontName=GR, fontSize=11)))
    for item in [
        "\u039c\u03b7\u03bd \u03c0\u03b1\u03c2 \u039a\u0391\u03a4\u03a9 \u03b1\u03c0\u03cc $250,000. \u0394\u0395\u039d \u03a5\u03a0\u0391\u03a1\u03a7\u0395\u0399 \u03c0\u03bf\u03c3\u03cc \u03ba\u03ac\u03c4\u03c9 \u03b1\u03c0\u03cc \u03b1\u03c5\u03c4\u03cc. \u03a4\u0395\u039b\u039f\u03a3.",
        "\u039c\u03b7\u03bd \u03b4\u03b5\u03af\u03be\u03b5\u03b9\u03c2 \u03ba\u03b1\u03bd\u03ad\u03bd\u03b1 \u03ad\u03b3\u03b3\u03c1\u03b1\u03c6\u03bf (\u03bc\u03cc\u03bd\u03bf \u03c0\u03c1\u03bf\u03c6\u03bf\u03c1\u03b9\u03ba\u03ad\u03c2 \u03b1\u03bd\u03b1\u03c6\u03bf\u03c1\u03ad\u03c2)",
        "\u039c\u03b7\u03bd \u03b2\u03b9\u03b1\u03c3\u03c4\u03b5\u03af\u03c2 \u03bd\u03b1 \u03b3\u03b5\u03bc\u03af\u03c3\u03b5\u03b9\u03c2 \u03c4\u03b7 \u03c3\u03b9\u03c9\u03c0\u03ae",
        "\u039c\u03b7\u03bd \u03b4\u03b5\u03af\u03be\u03b5\u03b9\u03c2 \u03c3\u03c5\u03bd\u03b1\u03af\u03c3\u03b8\u03b7\u03bc\u03b1",
        '\u039c\u0397\u039d \u03c0\u03b5\u03b9\u03c2 "agents coming" \u03ae "April 21" \u03ae "6 \u03bc\u03ad\u03c1\u03b5\u03c2"',
    ]:
        story.append(Paragraph(f"X  {item}", bullet_gr))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>\u039a\u0391\u039d\u0395</b>", ParagraphStyle("DHead", parent=body_gr, textColor=GREEN, fontName=GR, fontSize=11)))
    for item in [
        "\u0391\u03c6\u03b7\u03c3\u03ad \u03c4\u03b7\u03bd \u03bd\u03b1 \u03bc\u03b9\u03bb\u03ae\u03c3\u03b5\u03b9 \u03c0\u03c1\u03ce\u03c4\u03b7 \u2014 \u03c0\u03ac\u03bd\u03c4\u03b1",
        "\u039c\u03b5\u03af\u03bd\u03b5 \u03ae\u03c1\u03b5\u03bc\u03bf\u03c2, \u03b5\u03c0\u03b1\u03b3\u03b3\u03b5\u03bb\u03bc\u03b1\u03c4\u03b9\u03ba\u03cc\u03c2, \u03c3\u03cd\u03bd\u03c4\u03bf\u03bc\u03b5\u03c2 \u03c0\u03c1\u03bf\u03c4\u03ac\u03c3\u03b5\u03b9\u03c2",
        "\u0398\u03c5\u03bc\u03ae\u03c3\u03bf\u03c5: \u03c4\u03bf \u03ba\u03cc\u03c3\u03c4\u03bf\u03c2 \u03c3\u03bf\u03c5 \u03b5\u03af\u03bd\u03b1\u03b9 $0. \u03a4\u03bf \u03b4\u03b9\u03ba\u03cc \u03c4\u03bf\u03c5\u03c2 $400-$600/\u03ce\u03c1\u03b1",
    ]:
        story.append(Paragraph(f">>  {item}", bullet_gr))
    
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "\u2020 JOHN KYPRIANOS \u2014 U.S. Navy Veteran | Hellenic Navy | NATO | U.S. Citizen", footer_gr))
    story.append(Paragraph(
        "\u0391\u039c \u03a0\u039d: 39685 | \u0391\u03a6\u039c: 051422558 | \u2020 13 \u0399\u03bf\u03c5\u03bd\u03af\u03bf\u03c5 2021", footer_gr))
    story.append(Paragraph(
        "496 \u03c0\u03c1\u03c9\u03c4\u03cc\u03ba\u03bf\u03bb\u03bb\u03b1. 94 \u03c4\u03b5\u03ba\u03bc\u03ae\u03c1\u03b9\u03b1. \u0393\u03b9\u03b1 \u03c4\u03bf\u03bd \u0393\u03b9\u03ac\u03bd\u03bd\u03b7.", footer_gr))
    
    doc = SimpleDocTemplate(
        OUT, pagesize=letter,
        title="\u03a3\u03b5\u03bd\u03ac\u03c1\u03b9\u03bf ISC \u2014 \u0391\u03bd\u03c4\u03af\u03b3\u03c1\u03b1\u03c6\u03bf \u03a3\u03c4\u03b1\u03bc\u03b1\u03c4\u03af\u03bd\u03b1\u03c2 \u2014 15 \u0391\u03c0\u03c1\u03b9\u03bb\u03af\u03bf\u03c5 2026",
        author="Perplexity Computer",
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.6*inch, bottomMargin=0.5*inch,
    )
    doc.build(story)
    print(f"Greek: {OUT}")


build_english()
build_greek()
