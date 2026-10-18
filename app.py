
import streamlit as st

from document_reader import extract_text_from_pdf
from comparison import compare_documents
from report_generator import generate_comparison_report


st.set_page_config(
    page_title="AI Document Comparison Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Comparison Assistant")



if st.button("🔄 Reset Comparison"):
    for key in [
        "comparison_result",
        "document_a_name",
        "document_b_name"
    ]:
        st.session_state.pop(key, None)

    st.session_state["reset_count"] = (
        st.session_state.get("reset_count", 0) + 1
    )

    st.rerun()




st.write(
    "Upload two PDF documents to compare their summaries, "
    "similarities, differences, and important requirements."
)

st.info(
    "For best results, upload text-based PDFs. "
    "Scanned PDFs without readable text may not work."
)

col_a, col_b = st.columns(2)

with col_a:
    pdf_a = st.file_uploader(
        "📘 Upload Document A",
        type=["pdf"],
        key=f"document_a_{st.session_state.get('reset_count', 0)}"
    )

with col_b:
    pdf_b = st.file_uploader(
        "📗 Upload Document B",
        type=["pdf"],
        key=f"document_b_{st.session_state.get('reset_count', 0)}"
    )

if st.button("🔍 Compare Documents", type="primary"):
    if pdf_a is None or pdf_b is None:
        st.warning("Please upload both PDF documents.")
    elif pdf_a.size == 0 or pdf_b.size == 0:
        st.error("One or both uploaded files are empty.")
    else:
        try:
            with st.spinner("Extracting text from your PDFs..."):
                document_a = extract_text_from_pdf(pdf_a)
                document_b = extract_text_from_pdf(pdf_b)

            st.success("Text extracted from both PDFs successfully.")

            with st.expander("📘 Document A details"):
                st.write("Pages:", document_a["page_count"])
                st.write("Characters:", document_a["character_count"])

            with st.expander("📗 Document B details"):
                st.write("Pages:", document_b["page_count"])
                st.write("Characters:", document_b["character_count"])

            with st.spinner("Gemini is comparing your documents..."):
                comparison_result = compare_documents(
                    document_a["text"],
                    document_b["text"]
                )

            st.session_state["comparison_result"] = comparison_result
            st.session_state["document_a_name"] = pdf_a.name
            st.session_state["document_b_name"] = pdf_b.name

        except Exception as error:
            st.error(f"Could not compare documents: {error}")

if "comparison_result" in st.session_state:
    st.divider()
    st.header("📊 Comparison Results")

    st.markdown(st.session_state["comparison_result"])

    st.divider()
    st.subheader("📥 Download Your Report")

    try:
        report_bytes = generate_comparison_report(
            st.session_state["document_a_name"],
            st.session_state["document_b_name"],
            st.session_state["comparison_result"]
        )

        st.download_button(
            label="⬇️ Download Word Report",
            data=report_bytes,
            file_name="AI_Document_Comparison_Report.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        )

    except Exception as error:
        st.error(f"Could not generate the report: {error}")
