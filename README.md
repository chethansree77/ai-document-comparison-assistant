# AI Document Comparison Assistant

An AI-powered web application that compares two PDF documents and generates a structured comparison report using Python, Streamlit, and Google's Gemini API.

## Features

- Upload two PDF documents.
- Extract text from PDFs using PyPDF.
- Generate AI-powered summaries of both documents.
- Identify similarities and differences.
- Highlight important facts, dates, and requirements.
- Display comparison results in an organized interface.
- Download a formatted Word comparison report.
- Handle missing uploads and PDFs without readable text.
- Reset the comparison and upload new documents.

## Technologies Used

- Python
- Streamlit
- Google Gemini API (`google-genai`)
- PyPDF
- python-docx
- python-dotenv

## Project Structure

```text
ai-document-comparison-assistant/
├── app.py
├── document_reader.py
├── comparison.py
├── report_generator.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── sample_documents/
```

## Setup and Installation

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

4. Install the dependencies:

```powershell
pip install -r requirements.txt
```

5. Create a `.env` file in the project root and add your Gemini API key:

```text
GEMINI_API_KEY=your_actual_api_key
```

Replace the placeholder with your own API key. Never publish your real API key.

6. Start the application:

```powershell
python -m streamlit run app.py
```

7. Open the local URL shown in your terminal.

## Usage

1. Upload Document A and Document B as PDF files.
2. Click **Compare Documents**.
3. Review the summaries, similarities, differences, and key facts.
4. Download the Word comparison report.
5. Use **Reset Comparison** to start again.

## Security

- Keep your real API key in `.env`.
- Never commit `.env` to GitHub.
- Use `.env.example` as a placeholder template.

## Author

Python and AI project developed as part of practical learning in Generative AI application development.
