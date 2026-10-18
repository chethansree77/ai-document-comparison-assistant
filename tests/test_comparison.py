
from document_reader import extract_text_from_pdf
from comparison import compare_documents

# Extract text from Document A
with open("sample_documents/document_a.pdf", "rb") as pdf_a:
    document_a = extract_text_from_pdf(pdf_a)

# Extract text from Document B
with open("sample_documents/document_b.pdf", "rb") as pdf_b:
    document_b = extract_text_from_pdf(pdf_b)

print("Comparing documents with Gemini...")
print("Please wait...\n")

try:
    result = compare_documents(
        document_a["text"],
        document_b["text"]
    )

    print("=" * 60)
    print("AI DOCUMENT COMPARISON RESULTS")
    print("=" * 60)
    print(result)

except Exception as error:
    print("Comparison test failed:")
    print(error)
