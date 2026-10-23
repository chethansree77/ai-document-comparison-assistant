# 🤖 AI Document Comparison Assistant

An AI-powered web application that compares two PDF documents, summarizes their contents, identifies similarities and differences, extracts important facts, and generates a downloadable Word comparison report using Python, Streamlit, and Google's Gemini API.

## 🚀 Live Demo

**Try the application:** [AI Document Comparison Assistant](https://ai-document-comparison-assistant-ddrd7wfomkkjdwb47ulvfm.streamlit.app/)

**Source Code:** [GitHub Repository](https://github.com/chethansree77/ai-document-comparison-assistant)

---

## ✨ Features

- 📄 Upload two PDF documents for comparison.
- 📝 Extract text from PDF files using PyPDF.
- 🧠 Generate AI-powered summaries of both documents.
- 🔍 Identify similarities between documents.
- ⚖️ Highlight differences and changes.
- 📌 Extract important facts, dates, requirements, and key information.
- 📊 Display comparison results in an organized, user-friendly interface.
- 📥 Download a formatted Word comparison report.
- 🔄 Reset the comparison and upload new documents.
- ⚠️ Handle missing uploads and PDFs without readable text.
- 🎨 Enjoy a modern interface with gradient styling, responsive layouts, and interactive hover effects.

## 🖥️ Screenshots

### 1. Application Interface

![AI Document Comparison Assistant Interface](screenshots/app_interface.png)

### 2. AI Comparison Results

![AI-powered PDF comparison results](screenshots/comparison_results.png)

### 3. Word Report Download

![Word comparison report download](screenshots/word_report.png)

> Note: If your screenshot filenames differ from those above, update the image paths to match the actual files in the `screenshots` folder.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and processing |
| Streamlit | Interactive web interface |
| Google Gemini API | AI summaries and document comparison |
| google-genai | Gemini API integration |
| PyPDF | PDF text extraction |
| python-docx | Word report generation |
| python-dotenv | Local environment variable management |
| HTML and CSS | Custom interface styling |

## 📁 Project Structure

```text
ai-document-comparison-assistant/
│
├── app.py
├── comparison.py
├── document_reader.py
├── report_generator.py
├── create_sample_pdfs.py
├── list_models.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── sample_documents/
├── screenshots/
└── tests/
```

## ⚙️ Installation and Setup

### Prerequisites

- Python installed on your computer.
- Git installed on your computer.
- A Google Gemini API key.
- Visual Studio Code or another code editor.

### Step 1: Clone the repository

```bash
git clone https://github.com/chethansree77/ai-document-comparison-assistant.git
```

### Step 2: Open the project directory

```bash
cd ai-document-comparison-assistant
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the Python commands below using the virtual environment's Python executable directly.

### Step 5: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Configure your Gemini API key

Create a `.env` file in the project root directory and add:

```text
GEMINI_API_KEY=your_actual_api_key
```

Replace `your_actual_api_key` with your own Gemini API key.

**Important:** Never commit your real `.env` file or publish your API key on GitHub. The repository provides `.env.example` as a placeholder template.

### Step 7: Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

---

## 📖 How to Use

1. Open the application.
2. Upload the first PDF as **Document A**.
3. Upload the second PDF as **Document B**.
4. Click **Compare Documents**.
5. Review the summaries of both documents.
6. Explore the similarities, differences, and important facts.
7. Download the generated Word comparison report.
8. Use **Reset Comparison** to start a new comparison.

## 🧪 Testing

The repository includes a `tests/` directory for project tests.

To run tests, activate your virtual environment and execute:

```bash
python -m pytest
```

If pytest is not installed, install it using:

```bash
python -m pip install pytest
```

## 🔐 Security

- Store your Gemini API key in a local `.env` file.
- Keep `.env` excluded from Git using `.gitignore`.
- Never hardcode or publish API keys.
- Use `.env.example` to document required environment variables without including secrets.
- Configure deployment secrets through Streamlit Community Cloud's secrets settings.
- Avoid uploading confidential documents unless you are authorized to process them.

## 🌐 Deployment

The application is deployed using Streamlit Community Cloud.

**Live application:** [Open the deployed app](https://ai-document-comparison-assistant-ddrd7wfomkkjdwb47ulvfm.streamlit.app/)

The deployed application requires the appropriate Gemini API key to be configured securely in the Streamlit app's secrets.

## 🎯 Project Objective

The objective of this project is to demonstrate practical skills in Python development, Generative AI integration, PDF processing, document analysis, report generation, and interactive web application development.

This project demonstrates how an AI-powered application can help users understand and compare information across two documents more efficiently.

## 👩‍💻 Author

**Chintha Chethana Sai Sree**

Aspiring Python Developer | Generative AI Enthusiast

**GitHub:** [chethansree77](https://github.com/chethansree77)

---

*Built as a practical Generative AI application development project.*
