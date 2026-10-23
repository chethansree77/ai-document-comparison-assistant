# 🤖 AI Document Comparison Assistant

An AI-powered web application that compares two PDF documents, summarizes their contents, identifies similarities and differences, extracts important facts, and generates a downloadable Word comparison report using Python, Streamlit, and Google's Gemini API.

## 🚀 Live Demo

**Try the application:** [AI Document Comparison Assistant](https://ai-document-comparison-assistant-ddrd7wfomkkjdwb47ulvfm.streamlit.app/)

**Source code:** [GitHub Repository](https://github.com/chethansree77/ai-document-comparison-assistant)

---

## ✨ Features

- 📄 Upload two PDF documents for comparison.
- 📝 Extract text from PDF files using PyPDF.
- 🧠 Generate AI-powered summaries of both documents.
- 🔍 Identify similarities between documents.
- ⚖️ Highlight differences and changes.
- 📌 Extract important facts, dates, requirements, and key information.
- 📊 Display comparison results in an organized interface.
- 📥 Download a formatted Word comparison report.
- 🔄 Reset the comparison and upload new documents.
- ⚠️ Handle missing uploads and PDFs without readable text.
- 🎨 Responsive interface with gradient styling and hover effects.

## 🖥️ Screenshots

### 1. Application Interface

![AI Document Comparison Assistant Interface](https://raw.githubusercontent.com/chethansree77/ai-document-comparison-assistant/main/screenshots/app_interface.png)

### 2. AI Comparison Results

![AI-powered PDF comparison results](https://raw.githubusercontent.com/chethansree77/ai-document-comparison-assistant/main/screenshots/comparison_results.png)

### 3. Word Report Download

![Word comparison report download](https://raw.githubusercontent.com/chethansree77/ai-document-comparison-assistant/main/screenshots/word_report.png)

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and processing |
| Streamlit | Interactive web interface |
| Google Gemini API | AI summaries and comparison |
| google-genai | Gemini API integration |
| PyPDF | PDF text extraction |
| python-docx | Word report generation |
| python-dotenv | Environment variable management |
| HTML and CSS | Custom interface styling |

## 📁 Project Structure

```text
ai-document-comparison-assistant/
├── app.py
├── comparison.py
├── document_reader.py
├── report_generator.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── sample_documents/
├── screenshots/
└── tests/
```

## ⚙️ Installation and Setup

### Prerequisites

- Python
- Git
- A Google Gemini API key
- Visual Studio Code or another code editor

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

### Step 5: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Configure your Gemini API key

Create a `.env` file in the project root and add:

```text
GEMINI_API_KEY=your_actual_api_key
```

Replace the placeholder with your own API key.

**Security:** Never commit your real `.env` file or publish your API key. Keep `.env` excluded through `.gitignore`. For Streamlit Community Cloud, configure the key in the app's secrets settings.

### Step 7: Run the application

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually http://localhost:8501.

---

## 📖 How to Use

1. Open the application.
2. Upload the first PDF as **Document A**.
3. Upload the second PDF as **Document B**.
4. Click **Compare Documents**.
5. Review both document summaries.
6. Explore similarities, differences, and important facts.
7. Download the Word comparison report.
8. Reset the application to compare another pair of documents.

## 🧪 Testing

If the project includes tests, activate the virtual environment and run:

```bash
python -m pytest
```

If pytest is not installed:

```bash
python -m pip install pytest
```

## 🔐 Security

- Store API credentials in `.env` locally.
- Keep `.env` excluded from Git.
- Never hardcode or publish API keys.
- Use `.env.example` for placeholder configuration.
- Configure deployment secrets securely.
- Do not upload confidential documents unless authorized.

## 🌐 Deployment

The application is deployed using Streamlit Community Cloud.

**Live application:** [Open the deployed app](https://ai-document-comparison-assistant-ddrd7wfomkkjdwb47ulvfm.streamlit.app/)

The deployed app requires the Gemini API key to be configured in its Streamlit secrets.

## 🎯 Project Objective

This project demonstrates practical skills in Python development, Generative AI integration, PDF processing, document analysis, report generation, and interactive web application development.

## 👩‍💻 Author

**Chintha Chethana Sai Sree**

Aspiring Python Developer | Generative AI Enthusiast

**GitHub:** [chethansree77](https://github.com/chethansree77)

---

*Built as a practical Generative AI application development project.*
