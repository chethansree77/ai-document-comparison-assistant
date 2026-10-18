
from io import BytesIO
from datetime import datetime
import re

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT


def clean_markdown(text):
    """Remove common Markdown formatting from text."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    return text.strip()


def generate_comparison_report(
    document_a_name,
    document_b_name,
    comparison_text
):
    """Generate a professionally formatted Word comparison report."""

    report = Document()

    section = report.sections[0]
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    # Document-wide font
    normal = report.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10)
    normal.font.color.rgb = RGBColor(45, 55, 72)

    # Title
    title = report.add_heading(
        "AI Document Comparison Report", level=0
    )
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = report.add_paragraph(
        "AI-powered analysis of two PDF documents"
    )
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    date_paragraph = report.add_paragraph(
        f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
    )
    date_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Document information
    report.add_heading("Documents Compared", level=1)
    report.add_paragraph(f"Document A: {document_a_name}")
    report.add_paragraph(f"Document B: {document_b_name}")

    report.add_heading("Comparison Analysis", level=1)

    lines = comparison_text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].strip()

        if not line or line == "---":
            index += 1
            continue

        # Markdown table
        if line.startswith("|") and index + 1 < len(lines):
            table_lines = [line]
            index += 1

            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1

            rows = []

            for row_line in table_lines:
                cells = [
                    cell.strip()
                    for cell in row_line.strip("|").split("|")
                ]

                # Skip Markdown separator rows such as |---|---|
                if all(
                    re.fullmatch(r":?-{3,}:?", cell.replace(" ", ""))
                    for cell in cells
                ):
                    continue

                rows.append(cells)

            if rows:
                column_count = max(len(row) for row in rows)
                table = report.add_table(
                    rows=1,
                    cols=column_count
                )
                table.style = "Table Grid"
                table.alignment = WD_TABLE_ALIGNMENT.CENTER

                # Header row
                header_cells = table.rows[0].cells
                for column, value in enumerate(rows[0]):
                    header_cells[column].text = clean_markdown(value)
                    header_cells[column].vertical_alignment = (
                        WD_CELL_VERTICAL_ALIGNMENT.CENTER
                    )
                    for run in header_cells[column].paragraphs[0].runs:
                        run.bold = True
                        run.font.color.rgb = RGBColor(31, 78, 121)

                # Remaining rows
                for row_data in rows[1:]:
                    cells = table.add_row().cells
                    for column in range(column_count):
                        value = (
                            row_data[column]
                            if column < len(row_data)
                            else ""
                        )
                        cells[column].text = clean_markdown(value)
                        cells[column].vertical_alignment = (
                            WD_CELL_VERTICAL_ALIGNMENT.CENTER
                        )

            continue

        # Headings
        if line.startswith("### "):
            report.add_heading(clean_markdown(line[4:]), level=2)
        elif line.startswith("## "):
            report.add_heading(clean_markdown(line[3:]), level=1)
        elif line.startswith("# "):
            report.add_heading(clean_markdown(line[2:]), level=1)

        # Bullet points
        elif line.startswith(("- ", "* ")):
            report.add_paragraph(
                clean_markdown(line[2:]),
                style="List Bullet"
            )

        # Numbered lists
        elif re.match(r"^\d+[\.)]\s+", line):
            item = re.sub(r"^\d+[\.)]\s+", "", line)
            report.add_paragraph(
                clean_markdown(item),
                style="List Number"
            )

        # Ordinary text
        else:
            report.add_paragraph(clean_markdown(line))

        index += 1

    # Footer
    for current_section in report.sections:
        footer = current_section.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer.add_run(
            "AI Document Comparison Assistant | Generated Report"
        )

    output = BytesIO()
    report.save(output)
    output.seek(0)

    return output.getvalue()
