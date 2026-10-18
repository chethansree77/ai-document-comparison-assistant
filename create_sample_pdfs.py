
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

OUTPUT_DIR = Path("sample_documents")
OUTPUT_DIR.mkdir(exist_ok=True)

styles = getSampleStyleSheet()


def create_pdf(filename, title, sections):
    file_path = OUTPUT_DIR / filename

    document = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    story = [Paragraph(title, styles["Title"]), Spacer(1, 20)]

    for heading, content in sections:
        story.append(Paragraph(heading, styles["Heading2"]))
        story.append(Paragraph(content, styles["BodyText"]))
        story.append(Spacer(1, 12))

    document.build(story)
    print(f"Created: {file_path}")


document_a = [
    ("Policy Date", "Effective date: 1 January 2025"),
    ("Annual Leave", "Eligible full-time employees receive 12 days of annual leave per year."),
    ("Sick Leave", "Employees receive 8 days of sick leave per year."),
    ("Eligibility", "Employees become eligible after completing 3 months of service."),
    ("Leave Approval", "Employees should submit leave requests to their manager at least 5 days in advance."),
    ("Carry Forward", "Employees may carry forward up to 5 unused annual leave days to the next year."),
    ("Public Holidays", "The company observes 10 public holidays each year."),
]

document_b = [
    ("Policy Date", "Effective date: 1 January 2026"),
    ("Annual Leave", "Eligible full-time employees receive 15 days of annual leave per year."),
    ("Sick Leave", "Employees receive 8 days of sick leave per year."),
    ("Eligibility", "Employees become eligible after completing 6 months of service."),
    ("Leave Approval", "Employees should submit leave requests to their manager at least 7 days in advance."),
    ("Carry Forward", "Employees may carry forward up to 3 unused annual leave days to the next year."),
    ("Public Holidays", "The company observes 12 public holidays each year."),
    ("New Rule", "Employees must submit a handover note before taking 3 or more consecutive working days of leave."),
]

create_pdf(
    "document_a.pdf",
    "Employee Leave Policy - Version A",
    document_a,
)

create_pdf(
    "document_b.pdf",
    "Employee Leave Policy - Version B",
    document_b,
)

print("\nBoth sample PDFs have been created successfully!")
