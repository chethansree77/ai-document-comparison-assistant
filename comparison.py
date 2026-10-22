
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

Use concise bullet points. For differences, clearly state the
value or rule in Document A and the corresponding value or rule
in Document B. Mark items as changed, new, removed, or unchanged
where the documents support that conclusion.
"""

    # Start with one lightweight model to avoid sequential fallbacks.
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
