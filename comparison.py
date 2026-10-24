
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def compare_documents(text_a, text_b):
    """Compare two documents using Gemini and return a report as text."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    if not text_a or not text_a.strip():
        raise ValueError("Document A contains no extractable text.")

    if not text_b or not text_b.strip():
        raise ValueError("Document B contains no extractable text.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an AI Document Comparison Assistant.

Compare the two documents accurately. Be concise, structured,
and specific. Do not invent facts.

DOCUMENT A:
{text_a}

DOCUMENT B:
{text_b}

Return these exact section headings, using Markdown:

## 1. Summary of Document A
## 2. Summary of Document B
## 3. Key Similarities
## 4. Key Differences
## 5. New or Changed Requirements
## 6. Important Dates and Facts
## 7. Overall Conclusion

IMPORTANT FORMATTING RULES:
- Write all sentences with normal spaces between words.
- Never join separate words together.
- Use normal English spelling, punctuation, and sentence spacing.
- Do not remove spaces between words in any section.
- Keep each section heading exactly as specified.
- Use readable Markdown with proper line breaks.
- Use concise bullet points where appropriate.

COMPARISON RULES:
- Compare the documents accurately and objectively.
- For differences, clearly state the value or rule in Document A
  and the corresponding value or rule in Document B.
- Mark items as changed, new, removed, or unchanged where the
  documents support that conclusion.
- Do not invent facts, dates, requirements, or conclusions.
- Distinguish between information explicitly stated in a document
  and information that cannot be determined from the document.

OVERALL CONCLUSION RULES:
- In Section 7, write a clear overall conclusion in 2–4 complete
  sentences.
- Use normal spaces between every word.
- Summarize the most important similarities and differences.
- Explain the practical impact of the major changes when supported
  by the documents.
- Mention important restrictions or new requirements when relevant.
- Do not repeat every comparison detail.
- Do not put the entire conclusion into one unspaced word.
- Ensure the conclusion is readable plain English.

Return all seven sections in the specified order.
"""

    # Use one lightweight model to avoid sequential fallbacks.
    model_name = "gemini-flash-lite-latest"

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 3000,
            },
        )

        result = getattr(response, "text", None)

        if result and result.strip():
            return result.strip()

        raise RuntimeError(
            f"{model_name} returned an empty response. Please try again."
        )

    except Exception as error:
        raise RuntimeError(
            "Gemini could not complete the comparison. "
            "Check your internet connection, API quota, and model availability, "
            "then try again. Details: "
            f"{error}"
        ) from error
