#!/usr/bin/env python3
"""Build IRS-CI Evidence Binder PDF from markdown tabs.

Usage:
    python scripts/build-pdf.py --source irs-ci-package/tabs --output build/irs-ci-evidence-binder.pdf --commit abc1234
"""
import argparse
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    LongTable,
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER


TAB_ORDER = [
    "tab1-executive-summary.md",
    "tab2-contradiction-matrix.md",
    "tab3-timeline.md",
    "tab4-actor-map.md",
    "tab5-evidence-index.md",
    "tab6-mlat-map.md",
    "tab7-ask-list.md",
    "ASK-PB1-binder-tab7.md",
    "appendix-a-chain-of-custody.md",
]


def parse_args():
    p = argparse.ArgumentParser(description="Build evidence binder PDF")
    p.add_argument("--source", required=True, help="Directory containing tab .md files")
    p.add_argument("--output", required=True, help="Output PDF path")
    p.add_argument("--commit", default="unknown", help="Git commit hash for footer")
    return p.parse_args()


def clean(text):
    """Strip markdown formatting for PDF rendering."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # Escape XML special chars that aren't already tags
    text = text.replace('&', '&amp;')
    text = text.replace('<b>', '\x00B').replace('</b>', '\x00b')
    text = text.replace('<i>', '\x00I').replace('</i>', '\x00i')
    text = text.replace('<font face="Courier">', '\x00F').replace('</font>', '\x00f')
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('\x00B', '<b>').replace('\x00b', '</b>')
    text = text.replace('\x00I', '<i>').replace('\x00i', '</i>')
    text = text.replace('\x00F', '<font face="Courier">').replace('\x00f', '</font>')
    return text


def build_table(rows, styles):
    """Build a reportlab Table from parsed rows."""
    if not rows:
        return Spacer(1, 0)
    # Filter out rows with no cells
    rows = [r for r in rows if r and len(r) > 0]
    if not rows:
        return Spacer(1, 0)
    # Normalize column count
    ncols = max(len(r) for r in rows)
    if ncols == 0:
        return Spacer(1, 0)
    # Pad short rows
    for i in range(len(rows)):
        while len(rows[i]) < ncols:
            rows[i].append("")
    # Wrap cells in Paragraphs
    styled = []
    for i, row in enumerate(rows):
        styled_row = []
        for cell in row:
            style = styles["table_header"] if i == 0 else styles["table_cell"]
            try:
                styled_row.append(Paragraph(clean(str(cell)), style))
            except Exception:
                styled_row.append(Paragraph(str(cell), style))
        styled.append(styled_row)
    col_width = (7.0 * inch) / ncols
    t = LongTable(styled, colWidths=[col_width] * ncols, repeatRows=1, splitInRow=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d333b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
    ]))
    return t


def md_to_paragraphs(md_text, styles):
    """Convert markdown text to reportlab flowables."""
    flowables = []
    lines = md_text.split("\n")
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if in_table and table_rows:
                tbl = build_table(table_rows, styles)
                if tbl:
                    flowables.append(tbl)
                table_rows = []
                in_table = False
            flowables.append(Spacer(1, 6))
            continue

        # Table rows
        if stripped.startswith("|") and stripped.endswith("|"):
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if cells:
                table_rows.append(cells)
                in_table = True
            continue

        # Flush pending table
        if in_table and table_rows:
            tbl = build_table(table_rows, styles)
            if tbl:
                flowables.append(tbl)
            table_rows = []
            in_table = False

        # Headers
        if stripped.startswith("# "):
            flowables.append(Paragraph(clean(stripped[2:]), styles["h1"]))
            flowables.append(Spacer(1, 12))
        elif stripped.startswith("## "):
            flowables.append(Paragraph(clean(stripped[3:]), styles["h2"]))
            flowables.append(Spacer(1, 8))
        elif stripped.startswith("### "):
            flowables.append(Paragraph(clean(stripped[4:]), styles["h3"]))
            flowables.append(Spacer(1, 6))
        elif stripped.startswith("#### "):
            flowables.append(Paragraph(clean(stripped[5:]), styles["h4"]))
            flowables.append(Spacer(1, 4))
        elif stripped.startswith("- [ ] ") or stripped.startswith("- [x] "):
            check = "[x]" if stripped.startswith("- [x]") else "[ ]"
            text = stripped[6:]
            flowables.append(Paragraph(f"{check} {clean(text)}", styles["bullet"]))
        elif stripped.startswith("- "):
            flowables.append(Paragraph(f"\u2022 {clean(stripped[2:])}", styles["bullet"]))
        elif stripped.startswith("> "):
            flowables.append(Paragraph(clean(stripped[2:]), styles["blockquote"]))
        else:
            try:
                flowables.append(Paragraph(clean(stripped), styles["body"]))
            except Exception:
                flowables.append(Paragraph(stripped, styles["body"]))

    if in_table and table_rows:
        tbl = build_table(table_rows, styles)
        if tbl:
            flowables.append(tbl)

    return flowables


def get_styles():
    """Build custom paragraph styles."""
    ss = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=ss["Title"], fontSize=20, spaceAfter=20),
        "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontSize=16, spaceAfter=8),
        "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontSize=13, spaceAfter=6),
        "h3": ParagraphStyle("h3", parent=ss["Heading3"], fontSize=11, spaceAfter=4),
        "h4": ParagraphStyle("h4", parent=ss["Heading4"], fontSize=10, spaceAfter=4),
        "body": ParagraphStyle("body", parent=ss["BodyText"], fontSize=9, leading=12),
        "bullet": ParagraphStyle("bullet", parent=ss["BodyText"], fontSize=9, leftIndent=20, leading=12),
        "blockquote": ParagraphStyle("bq", parent=ss["BodyText"], fontSize=9, leftIndent=30,
                                       textColor=colors.HexColor("#555555"), leading=12),
        "table_header": ParagraphStyle("th", parent=ss["BodyText"], fontSize=7,
                                         textColor=colors.white, leading=9),
        "table_cell": ParagraphStyle("tc", parent=ss["BodyText"], fontSize=7, leading=9),
        "footer": ParagraphStyle("footer", parent=ss["Normal"], fontSize=7,
                                   textColor=colors.grey, alignment=TA_CENTER),
    }


def build_pdf(source_dir, output_path, commit):
    """Main build routine."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    styles = get_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.8 * inch,
    )

    story = []

    # Cover page
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("IRS-CI Evidence Binder", styles["title"]))
    story.append(Paragraph("Justice for John Kyprianos", styles["h2"]))
    story.append(Spacer(1, 0.5 * inch))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    story.append(Paragraph(f"Generated: {now}", styles["body"]))
    story.append(Paragraph(f"Commit: {commit}", styles["body"]))
    story.append(Paragraph("CONFIDENTIAL \u2014 LAW ENFORCEMENT SENSITIVE", styles["h3"]))
    story.append(PageBreak())

    # Process tabs in order
    source = Path(source_dir)
    processed = set()

    for fname in TAB_ORDER:
        fpath = source / fname
        if fpath.exists():
            print(f"  Processing: {fname}")
            md_text = fpath.read_text(encoding="utf-8")
            story.extend(md_to_paragraphs(md_text, styles))
            story.append(PageBreak())
            processed.add(fname)
        else:
            print(f"  Skipping (not found): {fname}")

    # Process remaining .md files
    for fpath in sorted(source.glob("*.md")):
        if fpath.name not in processed:
            print(f"  Processing (extra): {fpath.name}")
            md_text = fpath.read_text(encoding="utf-8")
            story.extend(md_to_paragraphs(md_text, styles))
            story.append(PageBreak())

    if len(story) <= 3:
        print("WARNING: No tab files found, generating minimal PDF")
        story.append(Paragraph("No tab content found in source directory.", styles["body"]))

    print(f"  Building PDF: {output_path}")
    doc.build(story)
    size = os.path.getsize(output_path)
    print(f"  Done. PDF size: {size:,} bytes")


if __name__ == "__main__":
    args = parse_args()
    print("Build IRS-CI Evidence Binder PDF")
    print(f"  Source: {args.source}")
    print(f"  Output: {args.output}")
    print(f"  Commit: {args.commit}")
    build_pdf(args.source, args.output, args.commit)
