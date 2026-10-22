
from pypdf import PdfReader
import io


def extract_text_from_pdf(uploaded_file):
    """
    Extract text and basic information from an uploaded PDF.
    """

    try:
        # Read the uploaded PDF
        pdf_bytes = uploaded_file.getvalue()
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))

        # Extract text from every page
        extracted_text = []

        for page in pdf_reader.pages:
            page_text = page.extract_text() or ""
            extracted_text.append(page_text)

        # Combine the extracted page text
        full_text = "\n".join(extracted_text).strip()

        # Validate the extracted content
        if not full_text:
            raise ValueError(
                "No readable text was found. "
                "Please upload a text-based PDF."
            )

        return {
            "text": full_text,
            "page_count": len(pdf_reader.pages),
            "character_count": len(full_text),
        }

    except Exception as error:
        raise ValueError(
            f"Could not read the PDF: {error}"
        ) from error
