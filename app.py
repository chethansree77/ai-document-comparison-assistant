
import html
import re
from html.parser import HTMLParser
from pathlib import Path

import streamlit as st

from document_reader import extract_text_from_pdf
from comparison import compare_documents
from report_generator import generate_comparison_report


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Document Comparison Assistant",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
    /* Reduce the empty space at the top */
.block-container {
    padding-top: 1rem !important;
}

/* Keep the title banner closer to the top */
h1 {
    margin-top: 0 !important;
}
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: Poppins, sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f7f8ff, #edf5ff);
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 30px;
        border-radius: 24px;
        color: white;
        background: linear-gradient(120deg, #4338ca, #6366f1, #0ea5e9);
        box-shadow: 0 12px 30px #4338ca25;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 2.1rem;
        font-weight: 800;
    }

    .hero p {
        color: #eef2ff;
        margin-bottom: 0;
    }

    .section-heading {
        color: #252b60;
        font-weight: 800;
        font-size: 1.35rem;
        margin-top: 22px;
        margin-bottom: 12px;
    }

    .upload-card, .summary-card, .difference-card, .plain-card, .metric-card {
        background: white;
        border: 1px solid #e0e7ff;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 7px 22px #28326410;
        margin-bottom: 14px;
        overflow-wrap: anywhere;
    }

    .upload-card { min-height: 100px; }

    .doc-a { color: #4338ca; }
    .doc-b { color: #047857; }

    .summary-card { border-top: 5px solid #6366f1; }
    .summary-b { border-top-color: #10b981; }

    .summary-card h3 {
        font-size: 1.05rem;
        margin-top: 0;
        margin-bottom: 15px;
    }

    .summary-point {
        display: flex;
        gap: 12px;
        align-items: flex-start;
        background: #f8faff;
        border: 1px solid #edf0ff;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .summary-point-number {
        min-width: 30px;
        height: 30px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 9px;
        background: #e0e7ff;
        color: #4338ca;
        font-size: .8rem;
        font-weight: 800;
    }

    .summary-point-text {
        color: #334155;
        font-size: .91rem;
        line-height: 1.65;
    }

    .difference-title {
        color: #312e81;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .difference-row {
        padding: 11px 13px;
        border-radius: 10px;
        margin-bottom: 9px;
        line-height: 1.65;
    }

    .difference-a { background: #eef2ff; color: #3730a3; }
    .difference-b { background: #ecfdf5; color: #065f46; }
    .difference-change { background: #fff7ed; color: #9a3412; }

    .metric-label { color: #64748b; font-size: .85rem; }
    .metric-value { color: #3730a3; font-size: 1.6rem; font-weight: 800; }

    div.stButton > button {
        border: 0;
        border-radius: 12px;
        min-height: 46px;
        color: white;
        font-weight: 700;
        background: linear-gradient(110deg, #4f46e5, #0284c7);
    }

    div.stButton > button:hover {
        color: white;
        box-shadow: 0 8px 20px #4f46e540;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CLEAN HTML WITHOUT LOSING TEXT
# =========================================================

class VisibleTextParser(HTMLParser):
    """Extract visible text from HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        value = data.strip()
        if value:
            self.parts.append(value)


def clean_text(value):
    """Clean escaped HTML and tags from AI output."""

    if value is None:
        return ""

    text = str(value).strip()

    # Decode nested HTML entities.
    for _ in range(4):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded

    # Remove code fences.
    text = re.sub(
        r"^\s*```(?:html|markdown|md|text)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\s*```\s*$", "", text)

    # If HTML exists, parse its visible text.
    if re.search(r"<\s*(?:div|p|span|li|h[1-6]|br)\b", text, re.I):
        parser = VisibleTextParser()
        try:
            parser.feed(text)
            parser.close()
            if parser.parts:
                text = "\n".join(parser.parts)
        except Exception:
            pass

    # Remove any leftover tags.
    text = re.sub(r"<[^>]*>", " ", text)

    # Remove Markdown heading markers, but keep the heading words.
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)

    # Clean stray formatting and whitespace.
    text = text.replace("**", "").replace("__", "")
    text = re.sub(r"[ \t]+", " ", text)

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)

    return "\n".join(lines).strip()


# =========================================================
# SECTION PARSER
# =========================================================

SECTION_NAMES = {
    1: "Summary of Document A",
    2: "Summary of Document B",
    3: "Key Similarities",
    4: "Key Differences",
    5: "New or Changed Requirements",
    6: "Important Dates and Facts",
    7: "Overall Conclusion",
}


def normalize_heading(line):
    """Return the section number if a line is a recognized heading."""

    line = html.unescape(str(line)).strip()

    # Remove HTML tags without deleting their content.
    line = re.sub(r"<[^>]*>", " ", line)
    line = re.sub(r"^\s*#{1,6}\s*", "", line)
    line = line.replace("**", "").replace("__", "")
    line = line.strip()

    match = re.match(r"^\s*(\d+)\s*[.)\-:]\s*(.*?)\s*$", line)
    if not match:
        return None

    number = int(match.group(1))
    heading = match.group(2).strip().rstrip(":").lower()

    if number not in SECTION_NAMES:
        return None

    expected = SECTION_NAMES[number].lower()

    # The numbered heading must match the expected heading.
    if heading == expected:
        return number

    return None


def split_sections(raw_result):
    """
    Split the raw model output into numbered sections BEFORE
    cleaning the section content. This prevents one section from
    swallowing all later sections.
    """

    if not raw_result:
        return {}

    raw = str(raw_result)

    # Decode escaped HTML so headings inside entities become visible.
    for _ in range(3):
        decoded = html.unescape(raw)
        if decoded == raw:
            break
        raw = decoded

    # Convert HTML heading tags into separate lines.
    raw = re.sub(
        r"<\s*(?:h[1-6]|p|div)\b[^>]*>",
        "\n",
        raw,
        flags=re.IGNORECASE,
    )
    raw = re.sub(
        r"<\s*/\s*(?:h[1-6]|p|div)\s*>",
        "\n",
        raw,
        flags=re.IGNORECASE,
    )
    raw = re.sub(r"<\s*br\s*/?\s*>", "\n", raw, flags=re.IGNORECASE)

    lines = raw.splitlines()
    sections = {}
    current_number = None
    buffer = []

    def save_current():
        if current_number is not None:
            sections[current_number] = clean_text("\n".join(buffer))

    for line in lines:
        number = normalize_heading(line)

        if number is not None:
            save_current()
            current_number = number
            buffer = []
        elif current_number is not None:
            buffer.append(line)

    save_current()

    return sections


def split_points(section_text):
    """Turn a section into readable individual points."""

    text = clean_text(section_text)

    if not text:
        return []

    points = []

    for line in text.splitlines():
        line = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", line).strip()

        # Ignore stray HTML fragments and empty heading artifacts.
        if not line:
            continue
        if re.fullmatch(r"</?[a-zA-Z][^>]*>", line):
            continue

        points.append(line)

    # If the result is one paragraph, split into sentences.
    if len(points) == 1 and len(points[0]) > 220:
        points = [
            item.strip()
            for item in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", points[0])
            if item.strip()
        ]

    # Deduplicate without changing order.
    unique = []
    for point in points:
        if point not in unique:
            unique.append(point)

    return unique


# =========================================================
# DISPLAY HELPERS
# =========================================================

def render_summary_card(title, text, css_class, title_class):
    points = split_points(text)

    st.markdown(
        f'<div class="summary-card {css_class}">'
        f'<h3 class="{title_class}">{html.escape(title)}</h3>',
        unsafe_allow_html=True,
    )

    if not points:
        st.info("No separate summary was returned for this document.")
    else:
        # Render each item independently. Do not inject AI-generated HTML.
        for index, point in enumerate(points, start=1):
            number, content = st.columns([1, 10])

            with number:
                st.markdown(
                    f"""
                    <div class="summary-point-number">{index:02d}</div>
                    """,
                    unsafe_allow_html=True,
                )

            with content:
                st.markdown(
                    f"""
                    <div class="summary-point-text">
                        {html.escape(point)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)


def render_section_card(title, text, color_class):
    points = split_points(text)

    st.markdown(
        f"""
        <div class="difference-card">
            <div class="difference-title">{html.escape(title)}</div>
        """,
        unsafe_allow_html=True,
    )

    if not points:
        st.markdown(
            '<div class="difference-row difference-a">'
            'No information was returned for this section.'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        for point in points:
            st.markdown(
                f"""
                <div class="difference-row {color_class}">
                    {html.escape(point)}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(label)}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "comparison_result": None,
    "document_a_name": "",
    "document_b_name": "",
    "document_a_pages": 0,
    "document_b_pages": 0,
    "document_a_chars": 0,
    "document_b_chars": 0,
    "report_bytes": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HEADER AND SIDEBAR
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>📑 AI Document Comparison Assistant</h1>
        <p>
            Compare two PDFs to identify similarities, differences,
            changed requirements, important dates and facts.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🧭 How to use")
    st.markdown(
        """
        1. Upload the first PDF.
        2. Upload the second PDF.
        3. Click Compare Documents.
        4. Review each comparison section.
        5. Download the Word report.
        """
    )
    st.divider()
    st.markdown("### ✨ Features")
    st.markdown(
        """
        - PDF text extraction
        - AI-powered comparison
        - Separate summaries
        - Similarities and differences
        - Important dates and facts
        - Changed requirements
        - Downloadable Word report
        """
    )


# =========================================================
# UPLOAD
# =========================================================

st.markdown(
    '<div class="section-heading">📤 Upload your documents</div>',
    unsafe_allow_html=True,
)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(
        """
        <div class="upload-card">
            <h3 class="doc-a">📘 Document A — Original</h3>
            <p>Choose the original PDF.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    file_a = st.file_uploader(
        "Choose Document A",
        type=["pdf"],
        key="upload_a",
    )

with col_b:
    st.markdown(
        """
        <div class="upload-card">
            <h3 class="doc-b">📗 Document B — Updated</h3>
            <p>Choose the updated PDF.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    file_b = st.file_uploader(
        "Choose Document B",
        type=["pdf"],
        key="upload_b",
    )


# =========================================================
# COMPARE
# =========================================================

st.markdown("---")

if st.button("🔎 Compare Documents", use_container_width=True):
    if not file_a or not file_b:
        st.error("Please upload both PDF documents.")
    else:
        try:
            with st.spinner("📖 Reading Document A..."):
                data_a = extract_text_from_pdf(file_a)

            with st.spinner("📖 Reading Document B..."):
                data_b = extract_text_from_pdf(file_b)

            text_a = clean_text(data_a.get("text", ""))
            text_b = clean_text(data_b.get("text", ""))

            if not text_a or not text_b:
                st.error(
                    "No readable text was found in one or both PDFs. "
                    "Scanned PDFs may need OCR."
                )
            else:
                st.success("Both documents were read successfully.")

                with st.spinner("🧠 Comparing documents with AI..."):
                    raw_result = compare_documents(text_a, text_b)

                if not raw_result or not str(raw_result).strip():
                    st.error("The AI returned an empty comparison.")
                else:
                    # IMPORTANT: keep raw result for section parsing.
                    st.session_state["comparison_result"] = str(raw_result)
                    st.session_state["document_a_name"] = file_a.name
                    st.session_state["document_b_name"] = file_b.name
                    st.session_state["document_a_pages"] = data_a.get("page_count", 0)
                    st.session_state["document_b_pages"] = data_b.get("page_count", 0)
                    st.session_state["document_a_chars"] = data_a.get(
                        "character_count", len(text_a)
                    )
                    st.session_state["document_b_chars"] = data_b.get(
                        "character_count", len(text_b)
                    )
                    st.session_state["report_bytes"] = None

                    st.success("🎉 Comparison completed successfully!")

        except Exception as exc:
            st.error("Comparison failed.")
            st.exception(exc)


# =========================================================
# RESULTS
# =========================================================

raw_result = st.session_state.get("comparison_result")

if raw_result:
    sections = split_sections(raw_result)

    st.markdown("---")
    st.markdown(
        '<div class="section-heading">📊 Comparison Dashboard</div>',
        unsafe_allow_html=True,
    )

    metrics = st.columns(4)

    with metrics[0]:
        metric_card("📘 Document A Pages", st.session_state["document_a_pages"])
    with metrics[1]:
        metric_card("📗 Document B Pages", st.session_state["document_b_pages"])
    with metrics[2]:
        metric_card(
            "📝 Document A Characters",
            f'{st.session_state["document_a_chars"]:,}',
        )
    with metrics[3]:
        metric_card(
            "📝 Document B Characters",
            f'{st.session_state["document_b_chars"]:,}',
        )

    # Summaries
    st.markdown(
        '<div class="section-heading">📝 Document Summaries</div>',
        unsafe_allow_html=True,
    )

    sum_a, sum_b = st.columns(2)

    with sum_a:
        render_summary_card(
            f'📘 {st.session_state["document_a_name"]}',
            sections.get(1, ""),
            "",
            "doc-a",
        )

    with sum_b:
        render_summary_card(
            f'📗 {st.session_state["document_b_name"]}',
            sections.get(2, ""),
            "summary-b",
            "doc-b",
        )

    # Similarities
    st.markdown(
        '<div class="section-heading">🤝 Key Similarities</div>',
        unsafe_allow_html=True,
    )
    render_section_card(
        "What both documents have in common",
        sections.get(3, ""),
        "difference-a",
    )

    # Differences
    st.markdown(
        '<div class="section-heading">🔍 Key Differences</div>',
        unsafe_allow_html=True,
    )
    render_section_card(
        "Changes between the two documents",
        sections.get(4, ""),
        "difference-change",
    )

    # Requirements
    st.markdown(
        '<div class="section-heading">📋 New or Changed Requirements</div>',
        unsafe_allow_html=True,
    )
    render_section_card(
        "Requirements to review",
        sections.get(5, ""),
        "difference-change",
    )

    # Facts
    st.markdown(
        '<div class="section-heading">📌 Important Dates and Facts</div>',
        unsafe_allow_html=True,
    )
    render_section_card(
        "Dates, numbers and important facts",
        sections.get(6, ""),
        "difference-a",
    )

    # Conclusion
    st.markdown(
        '<div class="section-heading">💡 Overall Conclusion</div>',
        unsafe_allow_html=True,
    )
    render_section_card(
        "AI comparison conclusion",
        sections.get(7, ""),
        "difference-b",
    )

    with st.expander("📄 View cleaned full comparison"):
        st.text(clean_text(raw_result))

    # Report download
    st.markdown("---")
    st.markdown(
        '<div class="section-heading">📥 Download your report</div>',
        unsafe_allow_html=True,
    )
    st.write("Generate an editable Microsoft Word report.")

    if st.button("🛠️ Generate Word Report", use_container_width=True):
        try:
            with st.spinner("Creating Word report..."):
                report_file = generate_comparison_report(
                    st.session_state["document_a_name"],
                    st.session_state["document_b_name"],
                    clean_text(raw_result),
                )

                if isinstance(report_file, bytes):
                    report_bytes = report_file
                elif isinstance(report_file, bytearray):
                    report_bytes = bytes(report_file)
                elif hasattr(report_file, "getvalue"):
                    report_bytes = report_file.getvalue()
                elif isinstance(report_file, (str, Path)):
                    report_path = Path(report_file)
                    report_bytes = report_path.read_bytes()
                else:
                    raise TypeError(
                        "generate_comparison_report must return bytes, "
                        "a file-like object, or a file path."
                    )

                st.session_state["report_bytes"] = report_bytes

            st.success("Your Word report is ready!")

        except Exception as exc:
            st.error("Could not generate the Word report.")
            st.exception(exc)

    if st.session_state.get("report_bytes"):
        st.download_button(
            "⬇️ Download Word Report (.docx)",
            data=st.session_state["report_bytes"],
            file_name="document_comparison_report.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )

else:
    st.markdown(
        """
        <div class="plain-card">
            <h3>🚀 Ready to compare your documents?</h3>
            <p>
                Upload two text-based PDF files and click
                <strong>Compare Documents</strong> to see organized results.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(
    "AI Document Comparison Assistant · Verify important findings "
    "against the original documents."
)
