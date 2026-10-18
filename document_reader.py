
from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):
    """Extract readable text and page details from a PDF."""

    page_texts = []
    all_text = []

    try:
        reader = PdfReader(pdf_file)

        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()

            page_texts.append({
                "page": page_number,
                "text": text
            })

            if text:
                all_text.append(f"[Page {page_number}]\n{text}")

        full_text = "\n\n".join(all_text)

        if not full_text.strip():
            raise ValueError(
                "No readable text found. The PDF may be empty or scanned."
            )

        return {
            "text": full_text,
            "pages": page_texts,
            "page_count": len(reader.pages),
            "character_count": len(full_text)
        }

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(f"Could not read this PDF: {error}") from error
