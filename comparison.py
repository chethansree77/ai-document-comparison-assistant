
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

client = genai.Client(api_key=API_KEY)


def compare_documents(document_a_text, document_b_text):
    """Compare two documents and return Gemini's analysis."""

    prompt = f"""
You are an AI document comparison assistant.

Compare the following two documents carefully.

DOCUMENT A:
{document_a_text}

DOCUMENT B:
{document_b_text}

Return your analysis using these sections:

1. SUMMARY OF DOCUMENT A
Summarize its main points.

2. SUMMARY OF DOCUMENT B
Summarize its main points.

3. SIMILARITIES
List the information shared by both documents.

4. DIFFERENCES
Explain the changes between the documents.
Include the old and new values where applicable.

5. KEY FACTS
Compare dates, numbers, deadlines, eligibility rules,
requirements, and other important details.

6. NEW OR REMOVED REQUIREMENTS
Identify requirements appearing in only one document.

7. OVERALL CONCLUSION
Briefly explain the most important changes.

Rules:
- Use only information provided in the documents.
- Do not invent facts.
- Clearly identify which document each fact comes from.
- If information is missing, say it is not specified.
"""

    try:
        response = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt
        )

        result = getattr(response, "output_text", None)

        if not result:
            raise ValueError(
                "Gemini returned an empty comparison."
            )

        return result

    except Exception as error:
        raise RuntimeError(
            f"Document comparison failed: {error}"
        ) from error
