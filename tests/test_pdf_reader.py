
from pathlib import Path
from document_reader import extract_text_from_pdf

pdf_path = Path("sample_documents/document_b.pdf")

with pdf_path.open("rb") as pdf_file:
    result = extract_text_from_pdf(pdf_file)

print("PDF reader test successful!")
print("Pages:", result["page_count"])
print("Characters:", result["character_count"])
print("\nExtracted text preview:\n")
print(result["text"][:1000])
