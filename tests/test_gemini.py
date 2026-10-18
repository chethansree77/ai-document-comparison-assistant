
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: Gemini API key not found in .env")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.interactions.create(
            model="gemini-3.8-flash",
            input="Reply with exactly: Gemini connection successful!"
        )

        print("Gemini connection successful!")
        print("AI response:", response.output_text)

    except Exception as error:
        print("Gemini connection failed.")
        print("Error:", error)
