import re
import html
import textwrap
import streamlit as st

from document_reader import extract_text_from_pdf
from comparison import compare_documents
from report_generator import generate_comparison_report


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="DocuCompare AI | Document Intelligence",
    page_icon="ðŸ“‘",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background:
            radial-gradient(circle at 5% 0%, rgba(129, 140, 248, 0.17), transparent 30%),
            radial-gradient(circle at 95% 5%, rgba(45, 212, 191, 0.13), transparent 28%),
            #f7f8fc;
        font-family: 'Inter', sans-serif;
    }


/* Responsive main workspace */
.stApp [data-testid="stMainBlockContainer"] {
    width: 100% !important;
    max-width: none !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    padding-top: 3rem !important;
    padding-bottom: 3.5rem !important;
    box-sizing: border-box !important;
}


    /* Larger default text and more comfortable line spacing */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        font-size: 21px;
        line-height: 1.8;
        color: #26364b;
    }

    [data-testid="stMarkdownContainer"] h2 {
        font-size: 35px;
        line-height: 1.35;
        margin-top: 1.1rem;
        margin-bottom: .65rem;
        color: #172554;
    }

    [data-testid="stMarkdownContainer"] h3 {
        font-size: 29px;
        line-height: 1.4;
        color: #1e293b;
    }

    [data-testid="stCaptionContainer"] p {
        font-size: 19px;
        line-height: 1.8;
    }

    [data-testid="stDataFrame"] {
        font-size: 18px;
    }

    /* Readability improvements for comparison output and Streamlit widgets */
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stAlert"] p,
    [data-testid="stTable"] th,
    [data-testid="stTable"] td,
    [data-testid="stDataFrame"] {
        font-size: 19px !important;
        line-height: 1.75 !important;
    }

    [data-testid="stExpander"] details summary p,
    [data-testid="stButton"] button,
    [data-testid="stFileUploader"] {
        font-size: 18px !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 30px;
        font-weight: 800;
    }


.hero {
    position: relative;
    overflow: hidden;
    margin-top: 18px;
    padding: 35px 32px;
    border: 1px solid rgba(255, 255, 255, 0.28);
    border-radius: 24px;
    background: linear-gradient(
        120deg,
        #4338ca 0%,
        #6366f1 45%,
        #0891b2 100%
    );
    background-size: 200% 200%;
    color: white;
    margin-bottom: 26px;
    box-shadow: 0 12px 35px rgba(79, 70, 229, 0.20);
    transition:
        transform 0.35s ease,
        box-shadow 0.35s ease,
        background-position 0.6s ease;
}


.hero:hover {
    transform: translateY(-5px) scale(1.008);
    background-position: 100% 50%;
    box-shadow:
        0 24px 50px rgba(79, 70, 229, 0.30),
        0 0 26px rgba(99, 102, 241, 0.15);
    border-color: rgba(165, 180, 252, 0.9);
}


    .hero-tag {
        display: inline-block;
        padding: 6px 12px;
        border: 1px solid rgba(255,255,255,0.35);
        background: rgba(255,255,255,0.12);
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.6px;
    }

    .hero h1 {
        color: white;
        font-size: clamp(28px, 4vw, 42px);
        font-weight: 800;
        margin: 18px 0 10px 0;
        line-height: 1.2;
    }

    .hero p {
        color: #eef2ff;
        font-size: 19px;
        line-height: 1.8;
        max-width: 760px;
        margin-bottom: 0;
    }

    .section-heading {
        color: #1e293b;
        font-size: 23px;
        font-weight: 750;
        margin-top: 24px;
        margin-bottom: 6px;
    }

    .section-description {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 18px;
    }



.upload-card {
    position: relative;
    padding: 22px;
    border: 1px solid #dbe4ff;
    border-radius: 20px;
    background: linear-gradient(135deg, #ffffff 0%, #f5f7ff 60%, #eef2ff 100%);
    min-height: 125px;
    margin-bottom: 8px;
    box-shadow:
        0 6px 18px rgba(71, 85, 105, 0.07),
        0 0 10px rgba(99, 102, 241, 0.03);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease,
        background 0.3s ease;
}


.upload-card:hover {
    transform: translateY(-5px) scale(1.015);
    border-color: #818cf8;
    background: linear-gradient(145deg, #ffffff, #eef2ff);
    box-shadow: 0 14px 28px rgba(79, 70, 229, 0.16);
}


    .upload-card h3 {
        color: #334155;
        font-size: 18px;
        margin-bottom: 8px;
    }

    .upload-card p {
        color: #64748b;
        font-size: 13px;
        line-height: 1.6;
    }



.feature-card {
    position: relative;
    background: linear-gradient(
        135deg,
        #ffffff 0%,
        #f8faff 55%,
        #eef2ff 100%
    );
    border: 1px solid #dbe4ff;
    border-radius: 19px;
    padding: 19px;
    min-height: 115px;
    box-shadow:
        0 6px 18px rgba(71, 85, 105, 0.07),
        0 0 10px rgba(99, 102, 241, 0.03);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease,
        background 0.3s ease;
}



.feature-card:hover {
    transform: translateY(-6px) scale(1.025);
    border-color: #818cf8;
    box-shadow:
        0 18px 34px rgba(79, 70, 229, 0.20),
        0 0 18px rgba(129, 140, 248, 0.12);
    filter: saturate(1.08);
}



    .feature-card .feature-icon { font-size: 24px; }

    .feature-card h4 {
        color: #334155;
        font-size: 14px;
        margin: 8px 0 5px 0;
    }

    .feature-card p {
        color: #64748b;
        font-size: 12px;
        line-height: 1.6;
        margin-bottom: 0;
    }

   .result-intro {
    padding: 18px 20px;
    border: 1px solid #c7d2fe;
    background: linear-gradient(120deg, #eef2ff, #f0fdfa);
    border-radius: 18px;
    margin: 10px 0 20px 0;
    box-shadow: 0 5px 15px rgba(79, 70, 229, 0.07);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;
}

.result-intro:hover {
    transform: translateY(-4px) scale(1.008);
    box-shadow:
        0 15px 30px rgba(79, 70, 229, 0.14),
        0 0 14px rgba(13, 148, 136, 0.08);
    border-color: #a5b4fc;
}

    .result-intro h3 {
        margin: 0 0 6px 0;
        color: #312e81;
        font-size: 20px;
    }

    .result-intro p {
        margin: 0;
        color: #475569;
        font-size: 19px;
        line-height: 1.8;
    }

    .mini-label {
        color: #64748b;
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .5px;
    }

    /* Soft-colour summary cards; the rest of the original design is unchanged */

.summary-card {
    height: 100%;
    min-height: 350px;
    border-radius: 20px;
    padding: 24px 25px;
    background: linear-gradient(
        135deg,
        #ffffff 0%,
        #f8faff 65%,
        #f1f5ff 100%
    );
    border: 1px solid #e0e7ff;
    box-shadow:
        0 6px 18px rgba(15, 23, 42, 0.05),
        0 0 10px rgba(99, 102, 241, 0.03);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease,
        background 0.3s ease;
}


    .summary-card {
        animation: summary-card-enter .55s ease both;
    }

    .summary-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(15, 23, 42, .07);
    }


@keyframes summary-card-enter {
    from {
        opacity: 0;
        transform: translateY(18px) scale(0.985);
    }

    70% {
        opacity: 1;
        transform: translateY(-2px) scale(1.002);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}


    .summary-card-a {
        background: #f0f7ff;
        border: 1px solid #c7e0ff;
    }

    .summary-card-b {
        background: #f0fbf7;
        border: 1px solid #b7efdc;
    }

    .summary-card .summary-title {
        font-size: 27px;
        font-weight: 800;
        line-height: 1.4;
        margin: 0 0 5px 0;
    }
   .summary-card-a:hover .summary-title {
    color: #7c3aed !important;
    transform: scale(1.05);
    transform-origin: left center;
    transition: color 0.3s ease, transform 0.3s ease;
}


    .summary-card-a .summary-title { color: #2875dc; }

    .summary-card-b:hover .summary-title {
    color: #047857 !important;
    transform: scale(1.05);
    transform-origin: left center;
    transition: color 0.3s ease, transform 0.3s ease;
}


    .summary-card-b .summary-title { color: #079b72; }

   .summary-card-b:hover .summary-file {
    color: #059669 !important;
    transform: translateX(4px);
    transition: color 0.3s ease, transform 0.3s ease;
}
    .summary-card .summary-file {
        color: #64748b;
        font-size: 16px;
        line-height: 1.7;
        overflow-wrap: anywhere;
    }
   .summary-card-a:hover .summary-file {
    color: #4f46e5 !important;
    transform: translateX(4px);
    transition: color 0.3s ease, transform 0.3s ease;
}



    .summary-card .summary-divider {
        border: none;
        border-top: 1px solid #cbd5e1;
        margin: 17px 0;
    }

    .summary-card-a .summary-divider { border-color: #bfdbfe; }
    .summary-card-b .summary-divider { border-color: #a7f3d0; }

    .summary-point-card {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 14px;
        margin: 10px 0;
        border-radius: 12px;
        background: rgba(255, 255, 255, .88);
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 10px rgba(30, 41, 59, .04);
        transition: transform .18s ease, box-shadow .18s ease;
    }

    .summary-point-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 16px rgba(30, 41, 59, .08);
    }

    .summary-point-number {
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 0 0 32px;
        width: 32px;
        height: 32px;
        border-radius: 9px;
        font-size: 12px;
        font-weight: 800;
    }

    .summary-card-a .summary-point-card { border-color: #d7e7ff; }
    .summary-card-a .summary-point-number { background: #dbeafe; color: #1d4ed8; }
    .summary-card-b .summary-point-card { border-color: #c9f0df; }
    .summary-card-b .summary-point-number { background: #d1fae5; color: #047857; }

    .summary-point-text {
        flex: 1;
        color: #35405a;
        font-size: 15px;
        line-height: 1.75;
        overflow-wrap: anywhere;
    }

    .summary-card .summary-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .summary-card .summary-list li {
        color: #334155;
        font-size: 18px;
        line-height: 1.65;
        margin-bottom: 11px;
        overflow-wrap: anywhere;
    }

    .summary-card .summary-list strong {
        color: #172554;
        font-size: 18px;
        font-weight: 750;
    }

    .summary-card .new-requirement {
        margin-top: 14px;
        padding: 12px 14px;
        border-radius: 12px;
        background: #fce7f3;
        border: 1px solid #fbcfe8;
        color: #9d174d;
        font-size: 17px;
        line-height: 1.7;
    }

    /* Design 4: professional summary with icons, headings and dividers */
    .professional-summary-card {
        min-height: 350px;
        padding: 24px;
    }
    .professional-summary-header { display: flex; flex-direction: column; gap: 5px; }
    .professional-summary-header .summary-title { font-size: 22px; letter-spacing: -.35px; }
    .professional-summary-card { position: relative; overflow: hidden; }
    .professional-summary-card:before { content: ""; display: block; height: 5px; position: absolute; top: 0; left: 0; right: 0; }
    .summary-card-a.professional-summary-card:before { background: linear-gradient(90deg, #2563eb, #60a5fa, #a5b4fc); }
    .summary-card-b.professional-summary-card:before { background: linear-gradient(90deg, #059669, #34d399, #a7f3d0); }
    .professional-summary-point { background: rgba(255,255,255,.58); margin: 7px 0; padding: 13px 12px; border: 1px solid rgba(255,255,255,.8); box-shadow: 0 2px 7px rgba(15,23,42,.035); }
    .professional-summary-icon { display: flex; align-items: center; justify-content: center; flex: 0 0 38px; width: 38px; height: 38px; border-radius: 12px; font-size: 19px; background: #fff; box-shadow: 0 2px 7px rgba(15,23,42,.06); }
    .summary-card-a .professional-summary-icon { color: #1d4ed8; border: 1px solid #dbeafe; }
    .summary-card-b .professional-summary-icon { color: #047857; border: 1px solid #d1fae5; }
    .professional-summary-heading { font-size: 14px; font-weight: 800; margin-bottom: 3px; color: #172554; }
    .professional-summary-text { color: #475569; font-size: 14px; line-height: 1.6; overflow-wrap: anywhere; }
    .professional-summary-list { display: flex; flex-direction: column; gap: 0; }
    .professional-summary-point {
        display: flex; align-items: flex-start; gap: 15px;
        padding: 17px 10px; border-bottom: 1px solid #dbe4ef; border-radius: 10px;
        transition: background .2s ease, transform .2s ease;
    }
    .summary-card-a .professional-summary-point { border-bottom-color: #d6e6fa; }
    .summary-card-b .professional-summary-point { border-bottom-color: #ccefe1; }
    .professional-summary-point:last-child { border-bottom: none; }
    .professional-summary-point {
        animation: summary-point-enter .42s ease both;
    }
    .professional-summary-point:nth-child(2) { animation-delay: .04s; }
    .professional-summary-point:nth-child(3) { animation-delay: .08s; }
    .professional-summary-point:nth-child(4) { animation-delay: .12s; }
    .professional-summary-point:nth-child(5) { animation-delay: .16s; }
    .professional-summary-point:nth-child(n+6) { animation-delay: .20s; }
    /* Colorful hover effects for summary points */
.summary-card-a .professional-summary-point:hover {
    background: linear-gradient(135deg, #dbeafe, #ede9fe, #f5f3ff);
    border: 1px solid #818cf8;
    transform: translateX(5px) scale(1.015);
    box-shadow: 0 10px 24px rgba(79, 70, 229, 0.16);
}

.summary-card-a .professional-summary-point:hover .professional-summary-heading {
    color: #6d28d9 !important;
}

.summary-card-a .professional-summary-point:hover .professional-summary-text {
    color: #1e40af !important;
}

.summary-card-b .professional-summary-point:hover {
    background: linear-gradient(135deg, #d1fae5, #ccfbf1, #ecfdf5);
    border: 1px solid #34d399;
    transform: translateX(5px) scale(1.015);
    box-shadow: 0 10px 24px rgba(5, 150, 105, 0.16);
}

.summary-card-b .professional-summary-point:hover .professional-summary-heading {
    color: #047857 !important;
}

.summary-card-b .professional-summary-point:hover .professional-summary-text {
    color: #065f46 !important;
}
    @keyframes summary-point-enter {
        from { opacity: 0; transform: translateY(7px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 700px) {
        .summary-card.professional-summary-card { min-height: 0; padding: 20px 15px; border-radius: 15px; }
        .professional-summary-header .summary-title { font-size: 19px; }
        .summary-card .summary-file { font-size: 13px; }
        .professional-summary-point { gap: 10px; padding: 11px 8px; }
        .professional-summary-icon { flex-basis: 32px; width: 32px; height: 32px; font-size: 16px; border-radius: 10px; }
        .professional-summary-text { font-size: 13px; }
    }

    @media (prefers-reduced-motion: reduce) {
        .summary-card, .professional-summary-point {
            animation: none !important;
            transition: none !important;
        }
    }
    .professional-summary-icon {
        display: flex; align-items: center; justify-content: center; flex: 0 0 43px;
        width: 43px; height: 43px; border-radius: 13px; background: #e0e7ff; font-size: 22px;
    }
    .summary-card-b .professional-summary-icon { background: #d1fae5; }
    .professional-summary-content { flex: 1; min-width: 0; }
    .professional-summary-heading {
        color: #172554; font-size: 19px; font-weight: 800; line-height: 1.5;
        margin: 0 0 4px 0; overflow-wrap: anywhere;
    }
    .professional-summary-text { color: #475569; font-size: 18px; line-height: 1.8; overflow-wrap: anywhere; }
    .summary-card-a .professional-summary-heading { color: #2855a6; }
    .summary-card-b .professional-summary-heading { color: #087653; }
    .professional-summary-empty {
        display: flex; align-items: center; gap: 14px; padding: 18px; color: #475569;
        background: rgba(255,255,255,.8); border-radius: 12px; font-size: 18px; line-height: 1.7;
    }

    @media (max-width: 700px) {
        .summary-card { min-height: auto; padding: 18px; }
        .summary-card .summary-title { font-size: 22px; }
        .summary-card .summary-list li,
        .summary-card .summary-list strong { font-size: 17px; }
        .professional-summary-point { gap: 10px; padding: 14px 6px; }
        .professional-summary-icon { flex-basis: 36px; width: 36px; height: 36px; font-size: 19px; }
        .professional-summary-heading { font-size: 17px; }
        .professional-summary-text { font-size: 16px; line-height: 1.7; }
        .summary-card .summary-file { font-size: 14px; }
    }

    .readable-panel {
    background: linear-gradient(135deg, #ffffff 0%, #f5f7ff 100%);
    border: 1px solid #dbe3ef;
    border-radius: 18px;
    padding: 20px 24px;
    margin: 10px 0 16px 0;
    box-shadow: 0 5px 15px rgba(30, 41, 59, 0.05);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;
}

.readable-panel:hover {
    transform: translateY(-4px) scale(1.008);
    box-shadow:
        0 15px 30px rgba(79, 70, 229, 0.12),
        0 0 12px rgba(99, 102, 241, 0.06);
    border-color: #a5b4fc;
}

    .readable-panel p,
    .readable-panel li {
        color: #334155;
        font-size: 19px;
        line-height: 1.9;
    }


/* Change status text â€” colorful hover effects */
.change-up {
    color: #047857;
    font-weight: 750;
    transition: color 0.3s ease, transform 0.3s ease,
                text-shadow 0.3s ease;
    display: inline-block;
}

.change-up:hover {
    color: #059669;
    transform: scale(1.12) translateX(3px);
    text-shadow: 0 3px 12px rgba(5, 150, 105, 0.25);
}

.change-down {
    color: #b45309;
    font-weight: 750;
    transition: color 0.3s ease, transform 0.3s ease,
                text-shadow 0.3s ease;
    display: inline-block;
}

.change-down:hover {
    color: #ea580c;
    transform: scale(1.12) translateX(3px);
    text-shadow: 0 3px 12px rgba(234, 88, 12, 0.25);
}

.change-new {
    color: #4338ca;
    font-weight: 750;
    transition: color 0.3s ease, transform 0.3s ease,
                text-shadow 0.3s ease;
    display: inline-block;
}

.change-new:hover {
    color: #7c3aed;
    transform: scale(1.12) translateX(3px);
    text-shadow: 0 3px 12px rgba(124, 58, 237, 0.25);
}

@media (prefers-reduced-motion: reduce) {
    .change-up,
    .change-down,
    .change-new {
        transition: none;
    }

    .change-up:hover,
    .change-down:hover,
    .change-new:hover {
        transform: none;
        text-shadow: none;
    }
}


    .finding-card {
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
    padding: 16px;
    min-height: 105px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;
}

.finding-card:hover {
    transform: translateY(-5px) scale(1.015);
    box-shadow:
        0 16px 30px rgba(79, 70, 229, 0.13),
        0 0 12px rgba(99, 102, 241, 0.06);
    border-color: #a5b4fc;
}

    .finding-card .finding-title {
        color: #64748b;
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .4px;
        margin-bottom: 8px;
    }

    .finding-card .finding-value {
        color: #1e293b;
        font-size: 25px;
        font-weight: 800;
        line-height: 1.35;
    }

    .finding-card .finding-note {
        color: #64748b;
        font-size: 15px;
        margin-top: 5px;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #4f46e5, #0891b2);
        color: white;
        border: none;
        border-radius: 12px;
        min-height: 48px;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 7px 18px rgba(79, 70, 229, 0.23);
        transform: translateY(-1px);
    }

    div.stButton > button { border-radius: 10px; }

    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 12px;
    }

    [data-testid="stFileUploaderDropzone"] {
        border: 1.5px dashed #c7d2fe;
        border-radius: 12px;
        background: #fafaff;
    }

    [data-testid="stAlert"] { border-radius: 12px; }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding-top: 28px;
    }

    @media (max-width: 700px) {
        .hero { padding: 23px; }
        .block-container { padding-top: 1rem; }
    }
    /* Clear, larger comparison tables and result content */
    [data-testid="stTable"] table,
    [data-testid="stDataFrame"] {
        width: 100%;
        font-size: 18px !important;
    }

    [data-testid="stTable"] th,
    [data-testid="stTable"] td {
        font-size: 18px !important;
        line-height: 1.7 !important;
        padding: 14px 16px !important;
        color: #24344d;
    }

    [data-testid="stAlert"] p {
        font-size: 20px !important;
        line-height: 1.8 !important;
    }

    [data-testid="stExpander"] summary p {
        font-size: 19px !important;
        font-weight: 700;
    }

    .stButton button, .stDownloadButton button {
        font-size: 18px !important;
    }


    /* Individual side-by-side difference cards */
    .difference-card-title {
        font-size: 23px;
        font-weight: 750;
        line-height: 1.5;
        color: #172554;
        margin: 2px 0 16px 0;
    }
    .document-value-card {
    height: 100%;
    min-height: 105px;
    border: 1px solid #dbe4f0;
    border-radius: 16px;
    padding: 18px 20px;
    background: linear-gradient(135deg, #ffffff 0%, #f5f8ff 100%);
    margin: 4px 0 10px 0;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease,
        background 0.3s ease;
}

.document-value-card:hover {
    transform: translateY(-5px) scale(1.015);
    box-shadow:
        0 16px 32px rgba(79, 70, 229, 0.13),
        0 0 14px rgba(99, 102, 241, 0.07);
    border-color: #a5b4fc;
}
    .document-a-card {
        background: #f0f7ff;
        border-color: #bfdbfe;
    }
    .document-b-card {
        background: #f0fdfa;
        border-color: #99f6e4;
    }
    .document-value-label {
        font-size: 17px;
        font-weight: 750;
        color: #475569;
        margin-bottom: 10px;
    }
    .document-value-text {
        font-size: 21px;
        line-height: 1.75;
        color: #172554;
        overflow-wrap: anywhere;
    }
    .difference-status {
        display: inline-block;
        font-size: 16px;
        font-weight: 750;
        padding: 6px 12px;
        border-radius: 999px;
        margin: 3px 0 8px 0;
    }
    .status-changed {
        color: #92400e;
        background: #fef3c7;
    }
    .status-same {
        color: #065f46;
        background: #d1fae5;
    }



    /* Dedicated colourful UI for Key Changes Identified only */

.key-change-card {
    position: relative;
    overflow: hidden;
    margin: 14px 0;
    padding: 24px 26px;
    border: 1px solid #c7d2fe;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #ffffff 0%,
        #f5f7ff 55%,
        #ecfeff 100%
    );
    box-shadow:
        0 8px 24px rgba(79, 70, 229, 0.08),
        0 0 12px rgba(99, 102, 241, 0.03);
    animation: key-change-enter .45s ease both;
    transition:
        transform .3s ease,
        box-shadow .3s ease,
        border-color .3s ease,
        background .3s ease;
}

    .key-change-card:before {
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 5px;
        background: linear-gradient(180deg, #3b82f6, #8b5cf6, #10b981);
    }
    .key-change-card:hover {
    transform: translateY(-5px) scale(1.015);
    box-shadow:
        0 18px 36px rgba(79, 70, 229, 0.16),
        0 0 14px rgba(99, 102, 241, 0.08);
    border-color: #a5b4fc;
}
    .key-change-top { display: flex; align-items: center; gap: 12px; margin-bottom: 15px; }
    .key-change-icon {
        display: flex; align-items: center; justify-content: center;
        flex: 0 0 46px; width: 46px; height: 46px; border-radius: 14px;
        background: linear-gradient(135deg, #dbeafe, #ede9fe); font-size: 23px;
    }
    .key-change-heading { margin: 0; color: #172554; font-size: 20px; font-weight: 800; line-height: 1.35; }
    .key-change-tag { display: inline-block; margin-top: 4px; padding: 3px 9px; border-radius: 999px; background: #ede9fe; color: #6d28d9; font-size: 11px; font-weight: 800; letter-spacing: .45px; text-transform: uppercase; }
    .key-change-values { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin: 14px 0; }
    .key-change-value { min-width: 0; padding: 13px 15px; border-radius: 13px; }
    .key-change-value-a { background: #eff6ff; border: 1px solid #bfdbfe; }
    .key-change-value-b { background: #ecfdf5; border: 1px solid #a7f3d0; }
    .key-change-label { display: block; margin-bottom: 5px; font-size: 11px; font-weight: 800; letter-spacing: .55px; text-transform: uppercase; }
    .key-change-value-a .key-change-label { color: #2563eb; }
    .key-change-value-b .key-change-label { color: #047857; }
    .key-change-value-text { color: #1e293b; font-size: 16px; font-weight: 700; line-height: 1.55; overflow-wrap: anywhere; }
    .key-change-explanation { margin: 13px 0 0; padding-top: 12px; border-top: 1px solid #e2e8f0; color: #475569; font-size: 14px; line-height: 1.75; }

    /* Wider sidebar for a spacious, balanced dashboard layout */
    [data-testid="stSidebar"] {
        min-width: 390px;
        max-width: 390px;
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 390px;
    }
    [data-testid="stSidebarContent"] {
        padding-left: 1.15rem;
        padding-right: 1.15rem;
    }
    @media (max-width: 700px) {
        [data-testid="stSidebar"] {
            min-width: min(88vw, 390px);
            max-width: min(88vw, 390px);
        }
        [data-testid="stSidebar"] > div:first-child {
            width: min(88vw, 390px);
        }
    }

    /* Design 1: dark navy sidebar with colorful gradient capability cards */
    [data-testid="stSidebar"] .workspace-capability-panel {
        margin: 8px 0 14px; padding: 20px 15px 17px;
        border: 1px solid rgba(129, 140, 248, .35); border-radius: 22px;
        background: linear-gradient(145deg, #10152b 0%, #20284a 58%, #25204b 100%);
        box-shadow: 0 12px 30px rgba(15, 23, 42, .24);
    }
    [data-testid="stSidebar"] .workspace-capability-title {
        color: #ffffff; font-size: 28px; line-height: 1.35; font-weight: 850;
        margin: 0 0 8px; letter-spacing: -.25px;
    }
    [data-testid="stSidebar"] .workspace-capability-subtitle {
        color: #c3cbe5; font-size: 17px; line-height: 1.7; margin: 0 0 19px;
    }
    [data-testid="stSidebar"] .workspace-capability-item {
        display: flex; align-items: flex-start; gap: 14px; padding: 17px 14px;
        margin-top: 12px; border-radius: 16px;
        border: 1px solid rgba(255,255,255,.12);
        box-shadow: 0 5px 14px rgba(0,0,0,.12);
        transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
    }
    [data-testid="stSidebar"] .workspace-capability-item:nth-of-type(1) {
        background: linear-gradient(125deg, #2a2b59 0%, #252f56 100%);
    }
    [data-testid="stSidebar"] .workspace-capability-item:nth-of-type(2) {
        background: linear-gradient(125deg, #203b4f 0%, #253958 100%);
    }
    [data-testid="stSidebar"] .workspace-capability-item:nth-of-type(3) {
        background: linear-gradient(125deg, #49304e 0%, #3b2c50 100%);
    }
    [data-testid="stSidebar"] .workspace-capability-item:hover {
        transform: translateY(-3px); box-shadow: 0 10px 22px rgba(0,0,0,.22);
        border-color: rgba(196,181,253,.65);
    }
    [data-testid="stSidebar"] .workspace-capability-icon {
        display: flex; align-items: center; justify-content: center; flex: 0 0 46px;
        width: 52px; height: 52px; border-radius: 15px; font-size: 29px;
        box-shadow: 0 5px 12px rgba(0,0,0,.14);
    }
    [data-testid="stSidebar"] .workspace-capability-icon.blue { background: linear-gradient(135deg, #8066ff, #6345dc); }
    [data-testid="stSidebar"] .workspace-capability-icon.purple { background: linear-gradient(135deg, #22c9bb, #07998f); }
    [data-testid="stSidebar"] .workspace-capability-icon.green { background: linear-gradient(135deg, #f28ab8, #db5598); }
    [data-testid="stSidebar"] .workspace-capability-item h4 {
        color: #ffffff; font-size: 20px; font-weight: 800; margin: 1px 0 7px; line-height: 1.4;
    }
    [data-testid="stSidebar"] .workspace-capability-item p {
        color: #e0e7ff; font-size: 17px; line-height: 1.65; margin: 0;
    }
    @media (prefers-reduced-motion: reduce) {
        [data-testid="stSidebar"] .workspace-capability-item { transition: none; }
        [data-testid="stSidebar"] .workspace-capability-item:hover { transform: none; }
    }

    @keyframes key-change-enter { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    @media (max-width: 600px) {
        .key-change-card { padding: 18px 16px 18px 19px; }
        .key-change-heading { font-size: 18px; }
        .key-change-values { grid-template-columns: 1fr; gap: 8px; }
        .key-change-value { padding: 11px 13px; }
    }
    @media (prefers-reduced-motion: reduce) {
        .key-change-card { animation: none; transition: none; }
        .key-change-card:hover { transform: none; }
    }

    /* Redesigned PDF upload area only */
    .pdf-upload-card {
        position: relative;
        overflow: hidden;
        min-height: 168px;
        padding: 24px 25px 20px;
        border-radius: 22px;
        margin-bottom: 10px;
        box-shadow: 0 12px 28px rgba(30, 41, 59, 0.07);
        transition: transform .2s ease, box-shadow .2s ease;
    }
    .pdf-upload-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 17px 34px rgba(30, 41, 59, 0.12);
    }
    .pdf-upload-card-a {
        background: linear-gradient(135deg, #eef5ff 0%, #f8fbff 58%, #e7f0ff 100%);
        border: 1px solid #c6dcff;
    }
    .pdf-upload-card-b {
        background: linear-gradient(135deg, #eafbf4 0%, #f8fffc 58%, #ddf8ed 100%);
        border: 1px solid #b8ead5;
    }
    .pdf-upload-topline {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 13px;
    }
    .pdf-upload-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 0 0 54px;
        width: 54px;
        height: 54px;
        border-radius: 16px;
        font-size: 28px;
        background: rgba(255,255,255,.82);
        box-shadow: 0 5px 13px rgba(30, 41, 59, .08);
    }
    .pdf-upload-card-a .pdf-upload-icon { color: #245fce; }
    .pdf-upload-card-b .pdf-upload-icon { color: #087b57; }
    .pdf-upload-eyebrow {
        margin: 0 0 3px 0;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.1px;
        text-transform: uppercase;
        color: #64748b;
    }
    .pdf-upload-card h3 {
        margin: 0;
        font-size: 24px;
        line-height: 1.3;
        font-weight: 800;
        color: #172554;
    }
    .pdf-upload-card-b h3 { color: #064e3b; }
    .pdf-upload-card p {
        margin: 0;
        font-size: 16px;
        line-height: 1.65;
        color: #475569;
    }
    /* Style uploader widgets within this upload area without affecting other file inputs */
    [data-testid="stColumn"]:has(.pdf-upload-card-a) [data-testid="stFileUploader"] section {
        border: 2px dashed #8bb5ff;
        border-radius: 18px;
        background: linear-gradient(180deg, #f8fbff, #edf4ff);
        padding: 18px;
    }
    [data-testid="stColumn"]:has(.pdf-upload-card-b) [data-testid="stFileUploader"] section {
        border: 2px dashed #7bd5b1;
        border-radius: 18px;
        background: linear-gradient(180deg, #f7fffb, #eafaf3);
        padding: 18px;
    }
    [data-testid="stColumn"]:has(.pdf-upload-card-a) [data-testid="stFileUploader"] button {
        border-radius: 10px;
        border: 1px solid #9bbcff;
        background: #ffffff;
        color: #245fce;
        font-weight: 700;
    }
    [data-testid="stColumn"]:has(.pdf-upload-card-b) [data-testid="stFileUploader"] button {
        border-radius: 10px;
        border: 1px solid #8eddbd;
        background: #ffffff;
        color: #087b57;
        font-weight: 700;
    }
    @media (max-width: 700px) {
        .pdf-upload-card { padding: 19px; min-height: auto; }
        .pdf-upload-card h3 { font-size: 21px; }
        .pdf-upload-card p { font-size: 15px; }
    }



    /* PREMIUM MOTION LAYER â€” visual styling only */
    .hero {
        position: relative;
        isolation: isolate;
        overflow: hidden;
        background: linear-gradient(120deg, #3730a3, #6366f1, #0891b2, #0f766e);
        background-size: 260% 260%;
        animation: hero-gradient-flow 12s ease infinite, hero-enter .75s ease both;
        box-shadow: 0 18px 42px rgba(79, 70, 229, .25), 0 5px 15px rgba(8, 145, 178, .12);
        border: 1px solid rgba(255,255,255,.22);
    }
    .hero::before, .hero::after {
        content: "";
        position: absolute;
        z-index: -1;
        border-radius: 50%;
        pointer-events: none;
        filter: blur(1px);
    }
    .hero::before {
        width: 230px; height: 230px;
        right: 7%; top: -105px;
        background: radial-gradient(circle, rgba(255,255,255,.22), rgba(255,255,255,0));
        animation: hero-orb-float 8s ease-in-out infinite;
    }
    .hero::after {
        width: 170px; height: 170px;
        right: 28%; bottom: -105px;
        background: radial-gradient(circle, rgba(45,212,191,.25), rgba(45,212,191,0));
        animation: hero-orb-float 10s ease-in-out infinite reverse;
    }
    .hero .hero-tag {
        backdrop-filter: blur(8px);
        box-shadow: inset 0 1px 0 rgba(255,255,255,.18);
        animation: hero-content-enter .7s .08s ease both;
    }
    .hero h1 {
        text-shadow: 0 4px 20px rgba(15,23,42,.2);
        animation: hero-content-enter .75s .14s ease both;
    }
    .hero p { animation: hero-content-enter .8s .22s ease both; }

    .pdf-upload-card, .feature-card, .finding-card, .document-value-card,
    .readable-panel, .result-intro, .summary-card, .key-change-card,
    [data-testid="stMetric"] {
        transition: transform .24s ease, box-shadow .24s ease, border-color .24s ease;
    }
    .pdf-upload-card:hover, .feature-card:hover, .finding-card:hover,
    .document-value-card:hover, .readable-panel:hover, .result-intro:hover,
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px) scale(1.008);
        box-shadow: 0 14px 30px rgba(30,41,59,.11);
        border-color: #c7d2fe;
    }
   .summary-card:hover {
    transform: translateY(-5px) scale(1.015);
    box-shadow:
        0 18px 36px rgba(30, 41, 59, 0.12),
        0 0 16px rgba(99, 102, 241, 0.08);
    border-color: #a5b4fc;
}

   /* Enhanced hover effects for existing buttons */
div.stButton > button,
.stDownloadButton button {
    border-radius: 12px;
    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        filter 0.25s ease,
        border-color 0.25s ease;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.10);
    will-change: transform;
}

div.stButton > button:hover,
.stDownloadButton button:hover {
    transform: translateY(-4px) scale(1.025);
    box-shadow:
        0 16px 30px rgba(79, 70, 229, 0.24),
        0 0 16px rgba(99, 102, 241, 0.12);
    filter: saturate(1.2) brightness(1.02);
}

div.stButton > button:active,
.stDownloadButton button:active {
    transform: translateY(0) scale(0.98);
    box-shadow: 0 3px 8px rgba(79, 70, 229, 0.12);
}
    div.stButton > button:hover, .stDownloadButton button:hover {
        transform: translateY(-2px) scale(1.015);
        box-shadow: 0 9px 20px rgba(79,70,229,.18);
        filter: saturate(1.08);
    }
    [data-testid="stFileUploaderDropzone"] {
        transition: border-color .2s ease, box-shadow .2s ease, background .2s ease;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #818cf8;
        box-shadow: 0 0 0 4px rgba(129,140,248,.12);
    }

    @keyframes hero-gradient-flow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    @keyframes hero-orb-float {
        0%, 100% { transform: translate3d(0,0,0) scale(1); }
        50% { transform: translate3d(-14px,12px,0) scale(1.06); }
    }
    @keyframes hero-enter {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes hero-content-enter {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @media (prefers-reduced-motion: reduce) {
        .hero, .hero .hero-tag, .hero h1, .hero p, .hero::before, .hero::after {
            animation: none !important;
        }
        .pdf-upload-card, .feature-card, .finding-card, .document-value-card,
        .readable-panel, .result-intro, .summary-card, .key-change-card,
        [data-testid="stMetric"], div.stButton > button, .stDownloadButton button,
        [data-testid="stFileUploaderDropzone"] {
            transition: none !important;
        }
        .pdf-upload-card:hover, .feature-card:hover, .finding-card:hover,
        .document-value-card:hover, .readable-panel:hover, .result-intro:hover,
        .summary-card:hover, .key-change-card:hover, [data-testid="stMetric"]:hover,
        div.stButton > button:hover, .stDownloadButton button:hover {
            transform: none !important;
        }
    }


/* ==========================================
   DOCUCOMPARE AI - PREMIUM UI ENHANCEMENTS
   Main content only; sidebar stays unchanged
========================================== */

.main .block-container {
    width: 100%;
    max-width: none !important;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    box-sizing: border-box;
    margin-left: 0;
    margin-right: 0;
    transition: max-width 0.3s ease, padding 0.3s ease;
}

/* Soft gradient background */
.stApp {
    background:
        radial-gradient(
            circle at 8% 5%,
            rgba(99, 102, 241, 0.09),
            transparent 28rem
        ),
        radial-gradient(
            circle at 92% 20%,
            rgba(6, 182, 212, 0.07),
            transparent 25rem
        ),
        linear-gradient(
            135deg,
            #fbfcff,
            #f3f5ff,
            #f9fcff
        );
}

/* Headings */
.main h1,
.main h2,
.main h3 {
    letter-spacing: -0.025em;
}

.main h2 {
    color: #312e81;
    text-shadow: 0 2px 5px rgba(49, 46, 129, 0.08);
}

.main h3 {
    color: #4338ca;
}

/* General content cards */
.main [data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px;
    border-color: rgba(129, 140, 248, 0.25);
    box-shadow: 0 8px 24px rgba(49, 46, 129, 0.06);
    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease;
}

.main [data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);
    border-color: rgba(99, 102, 241, 0.48);
    box-shadow: 0 14px 30px rgba(49, 46, 129, 0.12);
}

/* Horizontal dividers */
.main hr {
    border: none;
    height: 2px;
    background: linear-gradient(
        90deg,
        transparent,
        #a5b4fc,
        #67e8f9,
        transparent
    );
    margin: 1.5rem 0;
}

/* Tables */
.main [data-testid="stTable"] {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(30, 41, 59, 0.06);
}

/* Success, warning and error messages */
.main [data-testid="stAlert"] {
    border-radius: 14px;
    box-shadow: 0 5px 16px rgba(30, 41, 59, 0.05);
}

/* Accessible reduced-motion support */
@media (prefers-reduced-motion: reduce) {
    .main [data-testid="stVerticalBlockBorderWrapper"] {
        transition: none !important;
    }

    .main [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: none !important;
    }
}


/* ==========================================
   TABS AND EXPANDABLE SECTIONS
========================================== */

.main [data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 8px;
    padding: 7px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.85);
    box-shadow: 0 6px 20px rgba(49, 46, 129, 0.07);
}

.main [data-testid="stTabs"] button[data-baseweb="tab"] {
    border-radius: 11px;
    padding: 10px 15px;
    transition:
        background 0.2s ease,
        transform 0.2s ease;
}


.main [data-testid="stTabs"] button[data-baseweb="tab"]:hover {
    background: linear-gradient(135deg, #eef2ff, #ecfeff);
    transform: translateY(-4px) scale(1.025);
    box-shadow:
        0 10px 22px rgba(79, 70, 229, 0.16),
        0 0 12px rgba(99, 102, 241, 0.08);
}


.main [data-testid="stTabs"] button[aria-selected="true"] {
   background: linear-gradient(135deg, #4338ca, #6366f1, #0891b2);
    background-size: 200% 200%;
    border-radius: 12px;
    box-shadow:
        0 7px 18px rgba(79, 70, 229, 0.25),
        0 0 10px rgba(99, 102, 241, 0.10);
    transition:
        background-position 0.4s ease,
        box-shadow 0.3s ease;
}


.main [data-testid="stTabs"] button[aria-selected="true"]:hover {
    background-position: 100% 50%;
    box-shadow: 0 10px 23px rgba(79, 70, 229, 0.30);
}


.main [data-testid="stTabs"] button[aria-selected="true"] p {
    color: white !important;
    font-weight: 750;
}

/* Expanders */
.main [data-testid="stExpander"] {
    border: 1px solid #e0e7ff;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.88);
    box-shadow: 0 5px 18px rgba(49, 46, 129, 0.05);
    transition: box-shadow 0.25s ease;
}

.main [data-testid="stExpander"]:hover {
    box-shadow: 0 10px 25px rgba(49, 46, 129, 0.1);
}


/* ==========================================
   TABS AND EXPANDABLE SECTIONS
========================================== */

.main [data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 8px;
    padding: 7px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.85);
    box-shadow: 0 6px 20px rgba(49, 46, 129, 0.07);
}

.main [data-testid="stTabs"] button[data-baseweb="tab"] {
    border-radius: 11px;
    padding: 10px 15px;
    transition:
        background 0.2s ease,
        transform 0.2s ease;
}

.main [data-testid="stTabs"] button[data-baseweb="tab"]:hover {
    background: #eef2ff;
    transform: translateY(-2px);
}

.main [data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    border-radius: 11px;
    box-shadow: 0 5px 14px rgba(79, 70, 229, 0.22);
}

.main [data-testid="stTabs"] button[aria-selected="true"] p {
    color: white !important;
    font-weight: 750;
}

/* Expanders */
.main [data-testid="stExpander"] {
    border: 1px solid #e0e7ff;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.88);
    box-shadow: 0 5px 18px rgba(49, 46, 129, 0.05);
    transition: box-shadow 0.25s ease;
}

.main [data-testid="stExpander"]:hover {
    box-shadow: 0 10px 25px rgba(49, 46, 129, 0.1);
}


/* ==========================================
   FILE UPLOADERS AND FORM INPUTS
========================================== */

/* Enhanced PDF upload area */
.main [data-testid="stFileUploader"] {
    border: 1px solid #e0e7ff;
    border-radius: 20px;
    padding: 8px;
    background: linear-gradient(
        135deg,
        rgba(238, 242, 255, 0.55),
        rgba(240, 253, 250, 0.65)
    );
    box-shadow: 0 5px 16px rgba(79, 70, 229, 0.06);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;
}

.main [data-testid="stFileUploader"]:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow:
        0 16px 32px rgba(79, 70, 229, 0.15),
        0 0 14px rgba(13, 148, 136, 0.07);
    border-color: #a5b4fc;
}

/* Text boxes and select controls */
.main [data-baseweb="input"] > div,
.main [data-baseweb="textarea"] > div,
.main [data-baseweb="select"] > div {
    border-radius: 12px;
    transition: box-shadow 0.2s ease;
}

.main [data-baseweb="input"] > div:focus-within,
.main [data-baseweb="textarea"] > div:focus-within,
.main [data-baseweb="select"] > div:focus-within {
    box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.18);
}

/* Mobile layout */
@media (max-width: 700px) {
    .main .block-container {
        padding: 1rem 0.8rem 2rem;
    }

    .main [data-testid="stMetric"] {
    padding: 16px;
    border: 1px solid #e0e7ff;
    border-radius: 16px;
    background: linear-gradient(135deg, #ffffff 0%, #f5f7ff 100%);
    box-shadow: 0 5px 15px rgba(79, 70, 229, 0.06);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;
}

.main [data-testid="stMetric"]:hover {
    transform: translateY(-4px) scale(1.015);
    box-shadow:
        0 15px 28px rgba(79, 70, 229, 0.13),
        0 0 12px rgba(99, 102, 241, 0.07);
    border-color: #a5b4fc;
}

    .main [data-testid="stTabs"] [data-baseweb="tab-list"] {
      border-radius: 12px;
    padding: 11px 17px;
    transition:
        background 0.3s ease,
        transform 0.3s ease,
        box-shadow 0.3s ease;
    }
}

/* Respect reduced-motion preferences */
@media (prefers-reduced-motion: reduce) {
    .main [data-testid="stMetric"],
    .main div.stButton > button,
    .main .stDownloadButton button {
        transition: none !important;
    }

    .main [data-testid="stMetric"]:hover,
    .main div.stButton > button:hover,
    .main .stDownloadButton button:hover {
        transform: none !important;
    }
}




/* ==========================================
   DOCUMENT OVERVIEW - INTERACTIVE CARDS
========================================== */

/* Common document overview card styling */
.main [data-testid="stVerticalBlockBorderWrapper"]:has(
    [data-testid="stMarkdownContainer"] strong
) {
    transition:
        background 0.35s ease,
        border-color 0.35s ease,
        box-shadow 0.35s ease,
        transform 0.35s ease;
}

/* Document A and B card hover effect */
.main .doc-overview-card {
    border: 1px solid #dbeafe;
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(
        135deg,
        #ffffff 0%,
        #eff6ff 100%
    );
    box-shadow: 0 8px 22px rgba(37, 99, 235, 0.10);
    transition:
        background 0.35s ease,
        border-color 0.35s ease,
        box-shadow 0.35s ease,
        transform 0.35s ease;
}

.main .doc-overview-card:hover {
    background: linear-gradient(
        135deg,
        #dbeafe 0%,
        #c7d2fe 55%,
        #e0e7ff 100%
    );
    border-color: #818cf8;
    box-shadow: 0 16px 34px rgba(79, 70, 229, 0.23);
    transform: translateY(-5px) scale(1.015);
}

/* Document A blue accent */
.main .document-a-card {
    border-top: 4px solid #3b82f6;
}

.main .document-a-card:hover {
    background: linear-gradient(
        135deg,
        #dbeafe,
        #c7d2fe
    );
    box-shadow: 0 16px 34px rgba(59, 130, 246, 0.25);
}

/* Document B green accent */
.main .document-b-card {
    border-top: 4px solid #10b981;
    background: linear-gradient(
        135deg,
        #ffffff,
        #ecfdf5
    );
    box-shadow: 0 8px 22px rgba(16, 185, 129, 0.10);
}

.main .document-b-card:hover {
    background: linear-gradient(
        135deg,
        #d1fae5,
        #a7f3d0
    );
    border-color: #34d399;
    box-shadow: 0 16px 34px rgba(5, 150, 105, 0.22);
}

/* Metric labels */
.main .doc-overview-card [data-testid="stMetricLabel"] {
    color: #475569;
    font-weight: 700;
    transition: color 0.3s ease;
}

.main .doc-overview-card [data-testid="stMetricValue"] {
    color: #1e40af;
    font-weight: 850;
    transition: color 0.3s ease;
}

.main .document-b-card [data-testid="stMetricValue"] {
    color: #047857;
}

/* Keep animations subtle for accessibility */
@media (prefers-reduced-motion: reduce) {
    .main .doc-overview-card {
        transition: none !important;
    }

    .main .doc-overview-card:hover {
        transform: none !important;
    }
}


    /* Document overview: full-card hover effects */
    .st-key-document_a_card,
    .st-key-document_b_card {
        border: 1px solid #dbe4ff;
        border-radius: 20px;
        padding: 20px;
        background: linear-gradient(135deg, #ffffff, #f5f3ff);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.08);
        transition: background 0.35s ease, border-color 0.35s ease,
                    box-shadow 0.35s ease, transform 0.35s ease;
    }

    .st-key-document_a_card:hover,
    .st-key-document_b_card:hover {
        border-color: #818cf8;
        background: linear-gradient(135deg, #eef2ff, #ede9fe);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.10),
                    0 16px 35px rgba(79, 70, 229, 0.20);
        transform: translateY(-5px);
    }

    .st-key-document_a_card [data-testid="stMetric"],
    .st-key-document_b_card [data-testid="stMetric"] {
        border: 1px solid #dbe4ff;
        border-radius: 14px;
        padding: 14px;
        background: rgba(255, 255, 255, 0.82);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.06);
        transition: background 0.3s ease, border-color 0.3s ease,
                    box-shadow 0.3s ease, transform 0.3s ease;
    }

    .st-key-document_a_card [data-testid="stMetric"]:hover,
    .st-key-document_b_card [data-testid="stMetric"]:hover {
        border-color: #6366f1;
        background: linear-gradient(135deg, #dbeafe, #e0e7ff);
        box-shadow: 0 10px 24px rgba(79, 70, 229, 0.18);
        transform: translateY(-3px) scale(1.01);
    }

    @media (prefers-reduced-motion: reduce) {
        .st-key-document_a_card,
        .st-key-document_b_card,
        .st-key-document_a_card [data-testid="stMetric"],
        .st-key-document_b_card [data-testid="stMetric"] {
            transition: none !important;
        }
        .st-key-document_a_card:hover,
        .st-key-document_b_card:hover,
        .st-key-document_a_card [data-testid="stMetric"]:hover,
        .st-key-document_b_card [data-testid="stMetric"]:hover {
            transform: none !important;
        }
    }


    /* Responsive main workspace when sidebar opens or closes */
.stApp [data-testid="stMain"] {
    min-width: 0;
}

.stApp [data-testid="stMainBlockContainer"] {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Let content sections shrink and expand with the workspace */
.stApp [data-testid="stMainBlockContainer"] > div {
    min-width: 0;
    max-width: 100%;
    box-sizing: border-box;
}

/* Smooth transitions for the main workspace */
.stApp [data-testid="stMain"],
.stApp [data-testid="stMainBlockContainer"] {
    transition: width 0.3s ease, padding 0.3s ease;
}



/* =========================================
   IMPORTANT CHANGES â€” COLORFUL HOVER CARDS
========================================= */

.change-glance-card {
    height: 100%;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #dbeafe;
    border-left: 5px solid #6366f1;
    background: linear-gradient(145deg, #ffffff, #f5f3ff);
    box-shadow: 0 5px 16px rgba(79, 70, 229, 0.08);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease,
        background 0.3s ease;
    overflow-wrap: anywhere;
}

.change-glance-card:hover {
    transform: translateY(-6px) scale(1.025);
    box-shadow: 0 16px 32px rgba(79, 70, 229, 0.18);
    border-color: #a5b4fc;
    background: linear-gradient(145deg, #eef2ff, #fdf4ff);
}

.change-glance-title {
    color: #172554;
    font-size: 16px;
    font-weight: 800;
    transition: color 0.3s ease, transform 0.3s ease;
}

.change-glance-card:hover .change-glance-title {
    color: #6d28d9;
    transform: translateX(3px);
}

.change-glance-status {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    background: #fce7f3;
    color: #a21caf;
    font-size: 12px;
    font-weight: 800;
    transition: color 0.3s ease, background 0.3s ease;
}

.change-glance-card:hover .change-glance-status {
    color: #ffffff;
    background: linear-gradient(90deg, #7c3aed, #db2777);
}

.change-glance-value-a,
.change-glance-value-b {
    font-size: 14px;
    font-weight: 800;
    margin-top: 5px;
    overflow-wrap: anywhere;
    transition: color 0.3s ease, transform 0.3s ease;
}

.change-glance-value-a {
    color: #1e40af;
}

.change-glance-value-b {
    color: #047857;
}

.change-glance-card:hover .change-glance-value-a {
    color: #4338ca;
    transform: scale(1.04);
}

.change-glance-card:hover .change-glance-value-b {
    color: #059669;
    transform: scale(1.04);
}

.change-glance-arrow {
    color: #64748b;
    font-weight: 800;
    transition: color 0.3s ease, transform 0.3s ease;
}

.change-glance-card:hover .change-glance-arrow {
    color: #7c3aed;
    transform: translateX(4px) scale(1.15);
}

.change-glance-explanation {
    font-size: 12px;
    color: #475569;
    margin-top: 12px;
    line-height: 1.6;
    transition: color 0.3s ease;
}

.change-glance-card:hover .change-glance-explanation {
    color: #312e81;
}

@media (prefers-reduced-motion: reduce) {
    .change-glance-card,
    .change-glance-title,
    .change-glance-status,
    .change-glance-value-a,
    .change-glance-value-b,
    .change-glance-arrow,
    .change-glance-explanation {
        transition: none;
    }

    .change-glance-card:hover,
    .change-glance-card:hover .change-glance-title,
    .change-glance-card:hover .change-glance-value-a,
    .change-glance-card:hover .change-glance-value-b,
    .change-glance-card:hover .change-glance-arrow {
        transform: none;
    }
}

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR: WORKSPACE CAPABILITIES
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="workspace-capability-panel">
            <div class="workspace-capability-title">ðŸš€ What this workspace can do</div>
            <p class="workspace-capability-subtitle">Your quick guide to the document comparison tools.</p>
            <div class="workspace-capability-item">
                <div class="workspace-capability-icon blue">ðŸ“</div>
                <div><h4>Content Analysis</h4><p>Analyze the contents of both documents using AI.</p></div>
            </div>
            <div class="workspace-capability-item">
                <div class="workspace-capability-icon purple">ðŸ”</div>
                <div><h4>Difference Detection</h4><p>Review similarities, differences, and key requirements.</p></div>
            </div>
            <div class="workspace-capability-item">
                <div class="workspace-capability-icon green">ðŸ“¥</div>
                <div><h4>Downloadable Report</h4><p>Save your findings in a Word document.</p></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# HELPERS: PARSE AI RESPONSE INTO SECTIONS
# --------------------------------------------------
def normalize_heading(line):
    """Remove Markdown heading markers and surrounding whitespace."""
    return re.sub(r"^\s*#+\s*", "", line).strip()


def parse_comparison_sections(text):
    """
    Split Gemini's response by numbered section headings.
    Supports plain text and Markdown headings such as:
    '2. SUMMARY OF DOCUMENT B' and '### 2. SUMMARY OF DOCUMENT B'.
    """
    heading_pattern = re.compile(
        r"^\s*(?:#+\s*)?(\d+)\.\s+(.+?)\s*$",
        re.IGNORECASE,
    )

    sections = {}
    current_number = None
    current_lines = []

    def save_current():
        if current_number is not None:
            content = "\n".join(current_lines).strip()
            sections[current_number] = {
                "heading": current_heading,
                "content": content,
            }

    current_heading = ""

    for line in text.splitlines():
        cleaned = normalize_heading(line)
        match = heading_pattern.match(cleaned)

        if match:
            save_current()
            current_number = int(match.group(1))
            current_heading = match.group(2).strip()
            current_lines = []
        elif current_number is not None:
            current_lines.append(line)

    save_current()
    return sections


def find_section(sections, number, title_fragment=None):
    """Get a section by number and optionally confirm its heading."""
    section = sections.get(number)
    if not section:
        return ""

    if title_fragment and title_fragment.lower() not in section["heading"].lower():
        # If numbering differs, search for a matching heading instead.
        for candidate in sections.values():
            if title_fragment.lower() in candidate["heading"].lower():
                return candidate["content"]
        return ""

    return section["content"]


def parse_value_pairs(differences_text):
    """Parse structured and natural-language Document A / Document B comparisons."""
    if not differences_text:
        return []

    text = html.unescape(str(differences_text))
    text = re.sub(r"```(?:\w+)?", "", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\r", "")
    rows = []
    known_labels = [
        "Effective Date", "Annual Leave", "Sick Leave", "Eligibility Period",
        "Eligibility", "Leave Approval Notice", "Leave Approval Notice Period",
        "Advance Notice for Leave Approval", "Carry Forward", "Carry-Forward",
        "Public Holidays", "Handover Note Requirement", "Handover Requirement",
    ]

    def add_row(label, a, b):
        label = re.sub(r"[*_`#]", "", str(label)).strip(" :-")
        a = re.sub(r"[*_`]", "", str(a)).strip(" \t\n,.;:")
        b = re.sub(r"[*_`]", "", str(b)).strip(" \t\n,.;:")
        if not label or not a or not b:
            return
        label = label.replace("-", " ")
        if any(x["Item"].casefold() == label.casefold() for x in rows):
            return
        rows.append({"Item": label, "Document A": a, "Document B": b,
                     "Change": describe_change(a, b)})

    # First support the exact natural-language format:
    # Effective Date (Changed): Document A is effective ...; Document B is effective ...
    label_pattern = r"(?:" + "|".join(re.escape(x) for x in sorted(known_labels, key=len, reverse=True)) + r")"
    chunks = re.split(r"(?=(?:^|\n)\s*(?:[-*â€¢]\s*)?(?:\*\*)?" + label_pattern + r"(?:\s*\([^\n)]*\))?(?:\*\*)?\s*:)", text, flags=re.I)
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        m = re.match(r"(?:[-*â€¢]\s*)?(?:\*\*)?(.+?)(?:\*\*)?\s*(?:\(\s*(?:Changed|Unchanged|No change)\s*\))?\s*:\s*(.*)", chunk, flags=re.I|re.S)
        if not m:
            continue
        label, body = m.group(1).strip(" *_`"), m.group(2).strip()
        # Ensure this is a known comparison heading, not arbitrary prose.
        if not any(label.casefold() == known.casefold() for known in known_labels):
            continue
        a_match = re.search(r"\b(?:Document|Doc)\s*A\b\s*", body, flags=re.I)
        b_match = re.search(r"\b(?:Document|Doc)\s*B\b\s*", body, flags=re.I)
        if a_match and b_match and a_match.start() < b_match.start():
            a = body[a_match.end():b_match.start()].strip(" \t\n,;:-")
            b = body[b_match.end():].strip(" \t\n,;:-")
            # Remove connective words and trailing explanatory punctuation only.
            a = re.sub(r"^(?:states that|says that)\s+", "", a, flags=re.I)
            b = re.sub(r"^(?:states that|says that)\s+", "", b, flags=re.I)
            b = re.sub(r"\s+(?:This means|This shows|Therefore)\b.*$", "", b, flags=re.I)
            add_row(label, a, b)

    # Also support headings followed by separate Document A / Document B lines.
    current_label = None
    value_a = value_b = ""
    def save_current():
        if current_label and (value_a or value_b):
            add_row(current_label, value_a or "Not specified", value_b or "Not specified")
    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("-â€¢ ").strip()
        if not line:
            continue
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line).strip()
        line = re.sub(r"\s*\((?:Changed|Unchanged|No change)\)\s*", " ", line, flags=re.I).strip()
        lm = re.match(r"^(.{2,55}?):\s*$", line)
        if lm and any(lm.group(1).strip().casefold() == x.casefold() for x in known_labels):
            save_current(); current_label = lm.group(1).strip(); value_a = value_b = ""; continue
        am = re.match(r"(?:Document|Doc)\s*A\s*:\s*(.+)", line, re.I)
        bm = re.match(r"(?:Document|Doc)\s*B\s*:\s*(.+)", line, re.I)
        if am and current_label: value_a = am.group(1).strip()
        elif bm and current_label: value_b = bm.group(1).strip()
    save_current()
    return rows

def describe_change(value_a, value_b):
    """Give a simple label for matching or changed values."""
    a = re.sub(r"\s+", " ", value_a.lower()).strip()
    b = re.sub(r"\s+", " ", value_b.lower()).strip()

    if not a or not b:
        return "Review"
    if a == b:
        return "No change"

    # Recognize a few common numeric patterns without assuming all numbers
    # represent an increase/decrease of the same kind.
    number_a = re.search(r"\d+(?:\.\d+)?", a)
    number_b = re.search(r"\d+(?:\.\d+)?", b)

    if number_a and number_b:
        try:
            n_a = float(number_a.group())
            n_b = float(number_b.group())
            if n_b > n_a:
                return "Increased"
            if n_b < n_a:
                return "Decreased"
        except ValueError:
            pass

    return "Changed"


def professional_value(label, value):
    """Convert verbose AI wording into a concise, professional card value."""
    raw = re.sub(r"\s+", " ", str(value or "")).strip().strip(" .;:")
    key = re.sub(r"[^a-z]", "", str(label).lower())

    if not raw or raw.lower() in {"not specified", "unknown", "n/a"}:
        return raw or "Not specified"

    # Keep dates short and consistent.
    date_match = re.search(
        r"\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b",
        raw, re.I,
    )
    if date_match and ("date" in key or "effective" in key):
        return f"{date_match.group(1)} {date_match.group(2)[:3]} {date_match.group(3)}"

    number_match = re.search(r"\b(\d+(?:\.\d+)?)\b", raw)
    number = number_match.group(1) if number_match else None

    if number:
        if "annualleave" in key:
            return f"{number} days per year"
        if "sickleave" in key:
            return f"{number} days per year"
        if "eligibility" in key:
            return f"{number} months of service" if "month" in raw.lower() else f"{number}"
        if "approval" in key or "notice" in key:
            return f"{number} days' notice"
        if "carryforward" in key:
            return f"{number} days maximum"
        if "publicholiday" in key:
            return f"{number} days per year"

    if "handover" in key or "handover" in raw.lower():
        if re.search(r"3\s+or\s+more|three\s+or\s+more|3\+", raw, re.I):
            return "Required for 3+ consecutive working days of leave"
        return "Handover note required"

    # Strip repeated document references and turn long prose into a compact phrase.
    raw = re.sub(r"^(?:Document [AB]|Doc [AB])\s*(?:states|says|requires|allows|grants|provides|offers|has|:)?\s*", "", raw, flags=re.I)
    raw = re.sub(r"\b(?:whereas|while)\b.*$", "", raw, flags=re.I).strip(" ,.;:")
    if len(raw) > 100:
        raw = raw[:97].rsplit(" ", 1)[0] + "â€¦"
    return raw[:1].upper() + raw[1:] if raw else "Not specified"


def change_explanation(label, value_a, value_b, status):
    """Create a short, readable sentence explaining the detected change."""
    a = professional_value(label, value_a)
    b = professional_value(label, value_b)
    key = re.sub(r"[^a-z]", "", str(label).lower())
    if status == "No change":
        return f"No change: both documents specify {a.lower()}."
    if "annualleave" in key or "sickleave" in key or "publicholiday" in key:
        na = re.search(r"\d+(?:\.\d+)?", a)
        nb = re.search(r"\d+(?:\.\d+)?", b)
        if na and nb:
            diff = abs(float(nb.group()) - float(na.group()))
            amount = str(int(diff)) if diff.is_integer() else str(diff)
            unit = "day" if diff == 1 else "days"
            direction = "increased" if float(nb.group()) > float(na.group()) else "decreased"
            return f"{label} {direction} by {amount} {unit}, from {a.lower()} to {b.lower()}."
    if "eligibility" in key:
        return f"The required service period changed from {a.lower()} to {b.lower()}."
    if "approval" in key or "notice" in key:
        return f"The advance notice period changed from {a.lower()} to {b.lower()}."
    if "carryforward" in key:
        return f"The carry-forward limit changed from {a.lower()} to {b.lower()}."
    if "date" in key or "effective" in key:
        return f"The policy effective date moved from {a} to {b}."
    if "handover" in key:
        return "A new handover-note requirement was added in Document B."
    return f"Updated from {a.lower()} to {b.lower()}."


def make_bullets(text):
    """Turn lines from an AI section into a readable list."""
    if not text:
        return []

    items = []
    for line in text.splitlines():
        cleaned = line.strip()
        cleaned = re.sub(r"^[-*â€¢]\s*", "", cleaned)
        cleaned = re.sub(r"^\d+[.)]\s*", "", cleaned)
        if cleaned:
            items.append(cleaned)
    return items


def display_readable_bullets(text, empty_message="No details were provided."):
    """Render source-backed AI content as large, readable bullet points."""
    items = make_bullets(text)
    if not items and text.strip():
        # For paragraph-style output, split at sentence boundaries conservatively.
        items = [
            part.strip()
            for part in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text.strip())
            if part.strip()
        ]

    if not items:
        st.info(empty_message)
        return

    for item in items:
        st.markdown(f"- {item}")


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "reset_count" not in st.session_state:
    st.session_state["reset_count"] = 0


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <span class="hero-tag">âœ¨ AI-POWERED DOCUMENT INTELLIGENCE</span>
        <h1>DocuCompare AI</h1>
        <p>
            Understand what changed between two documents.
            Discover similarities, identify important differences,
            and generate a professional comparison report â€” all in one workspace.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# TOP ACTIONS
# --------------------------------------------------
top_left, top_right = st.columns([5, 1])

with top_left:
    st.markdown(
        """
        <div class="section-heading">ðŸ“‚ Compare your documents</div>
        <div class="section-description">
            Upload two PDF files to begin your comparison.
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    st.write("")
    st.write("")
    if st.button("ðŸ”„ Reset", use_container_width=True):
        for key in [
            "comparison_result",
            "document_a_name",
            "document_b_name",
            "document_a_details",
            "document_b_details",
            "comparison_error",
        ]:
            st.session_state.pop(key, None)

        st.session_state["reset_count"] += 1
        st.rerun()


# --------------------------------------------------
# PDF UPLOADS â€” redesigned section only
# --------------------------------------------------
col_a, col_b = st.columns(2, gap="large")

with col_a:
    st.markdown(
        """
        <div class="pdf-upload-card pdf-upload-card-a">
            <div class="pdf-upload-topline">
                <div class="pdf-upload-icon">ðŸ“˜</div>
                <div>
                    <div class="pdf-upload-eyebrow">STEP 01 Â· ORIGINAL</div>
                    <h3>Document A</h3>
                </div>
            </div>
            <p>Upload the original document or the first version you want to analyze.</p>
        </div>
        <div class="pdf-upload-widget-a"></div>
        """,
        unsafe_allow_html=True,
    )

    pdf_a = st.file_uploader(
        "Choose your first PDF",
        type=["pdf"],
        key=f"document_a_{st.session_state['reset_count']}",
    )

with col_b:
    st.markdown(
        """
        <div class="pdf-upload-card pdf-upload-card-b">
            <div class="pdf-upload-topline">
                <div class="pdf-upload-icon">ðŸ“—</div>
                <div>
                    <div class="pdf-upload-eyebrow">STEP 02 Â· REVISED</div>
                    <h3>Document B</h3>
                </div>
            </div>
            <p>Upload the revised document or the second version you want to compare.</p>
        </div>
        <div class="pdf-upload-widget-b"></div>
        """,
        unsafe_allow_html=True,
    )

    pdf_b = st.file_uploader(
        "Choose your second PDF",
        type=["pdf"],
        key=f"document_b_{st.session_state['reset_count']}",
    )

st.caption(
    "ðŸ“Œ Supported format: PDF. Text-based PDFs generally work best. "
    "Scanned PDFs may require OCR."
)


# --------------------------------------------------
# COMPARE BUTTON
# --------------------------------------------------
st.write("")
compare_clicked = st.button(
    "âœ¨ Compare Documents with AI",
    type="primary",
    use_container_width=True,
)

if compare_clicked:
    if pdf_a is None or pdf_b is None:
        st.warning("Please upload both PDF documents before comparing.")

    elif pdf_a.size == 0 or pdf_b.size == 0:
        st.error("One or both uploaded files are empty.")

    else:
        try:
            with st.spinner("ðŸ“– Extracting text from your PDFs..."):
                document_a = extract_text_from_pdf(pdf_a)
                document_b = extract_text_from_pdf(pdf_b)

            if not document_a.get("text", "").strip():
                st.error(
                    "No readable text was found in Document A. "
                    "Try a text-based PDF or an OCR-processed version."
                )
                st.stop()

            if not document_b.get("text", "").strip():
                st.error(
                    "No readable text was found in Document B. "
                    "Try a text-based PDF or an OCR-processed version."
                )
                st.stop()

            with st.spinner("ðŸ§  Gemini is analyzing similarities and differences..."):
                comparison_result = compare_documents(
                    document_a["text"],
                    document_b["text"],
                )

            if not comparison_result:
                st.error("The AI returned an empty comparison. Please try again.")
            else:
                st.session_state["comparison_result"] = comparison_result
                st.session_state["document_a_name"] = pdf_a.name
                st.session_state["document_b_name"] = pdf_b.name

                st.session_state["document_a_details"] = {
                    "pages": document_a["page_count"],
                    "characters": document_a["character_count"],
                }
                st.session_state["document_b_details"] = {
                    "pages": document_b["page_count"],
                    "characters": document_b["character_count"],
                }

                st.session_state.pop("comparison_error", None)
                st.success("Your document comparison is ready!")

        except Exception as error:
            st.session_state["comparison_error"] = str(error)
            st.error(
                "We couldn't complete the comparison. "
                "Check your API availability, connection, and PDF files."
            )
            with st.expander("Technical details"):
                st.code(str(error))


# --------------------------------------------------
# RESULTS DASHBOARD
# --------------------------------------------------
if (
    "comparison_result" in st.session_state
    and "document_a_details" in st.session_state
    and "document_b_details" in st.session_state
):
    result = st.session_state["comparison_result"]
    sections = parse_comparison_sections(result)

    summary_a = find_section(sections, 1, "SUMMARY OF DOCUMENT A")
    summary_b = find_section(sections, 2, "SUMMARY OF DOCUMENT B")
    similarities = find_section(sections, 3, "SIMILARITIES")
    differences = find_section(sections, 4, "DIFFERENCES")
    key_facts = find_section(sections, 5, "KEY FACTS")
    requirements = find_section(sections, 6, "REQUIREMENTS")
    conclusion = find_section(sections, 7, "OVERALL CONCLUSION")

    st.markdown("---")
    st.markdown(
        """
        <div class="result-intro">
            <h3>âœ¨ Your comparison dashboard is ready</h3>
            <p>
                Start with the key changes, compare the documents side by side,
                and open the detailed AI analysis only when you need more context.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Document overview
    st.markdown("## ðŸ“Š Document overview")
    overview_a, overview_b = st.columns(2, gap="large")

    with overview_a:
        with st.container(key="document_a_card"):
            st.markdown("**ðŸ“˜ Document A**")
            st.write(st.session_state["document_a_name"])
            metric_a1, metric_a2 = st.columns(2)
            metric_a1.metric("Pages", st.session_state["document_a_details"]["pages"])
            metric_a2.metric(
                "Characters",
                f"{st.session_state['document_a_details']['characters']:,}",
            )

    with overview_b:
        with st.container(key="document_b_card"):
            st.markdown("**ðŸ“— Document B**")
            st.write(st.session_state["document_b_name"])
            metric_b1, metric_b2 = st.columns(2)
            metric_b1.metric("Pages", st.session_state["document_b_details"]["pages"])
            metric_b2.metric(
                "Characters",
                f"{st.session_state['document_b_details']['characters']:,}",
            )

    # Side-by-side Document A and Document B summary cards.
    st.markdown("---")
    st.markdown("## ðŸ“ Document Summaries")
    st.caption("Each key point appears in its own card. Blue represents Document A; green represents Document B.")

    summary_col_a, summary_col_b = st.columns(2, gap="large")

    def summary_items(text):
        """Clean AI summary text and extract readable points, never raw HTML."""
        if not text:
            return []

        cleaned = str(text).strip()

        # Decode repeatedly because the model may return escaped HTML entities.
        for _ in range(3):
            decoded = html.unescape(cleaned)
            if decoded == cleaned:
                break
            cleaned = decoded

        # Remove Markdown code fences / inline code markers around generated HTML.
        cleaned = re.sub(r"```\s*(?:html|markdown|text)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.replace("```", "").replace("`", "")

        # Prefer the actual text inside each summary card, discarding wrappers.
        card_texts = re.findall(
            r'<div\b[^>]*class\s*=\s*["\'][^"\']*summary-point-text[^"\']*["\'][^>]*>(.*?)</div\s*>',
            cleaned,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if card_texts:
            # Keep only meaningful text before the first card, if any.
            first_card = re.search(
                r'<div\b[^>]*class\s*=\s*["\'][^"\']*summary-point-card[^"\']*["\'][^>]*>',
                cleaned,
                flags=re.IGNORECASE,
            )
            prefix = cleaned[:first_card.start()] if first_card else ""
            prefix = re.sub(r"(?is)<[^>]+>", " ", prefix)
            prefix = re.sub(r"\s+", " ", prefix).strip()
            extracted = []
            for item in card_texts:
                item = html.unescape(item)
                item = re.sub(r"(?is)<[^>]+>", " ", item)
                item = re.sub(r"\*{1,3}([^*]+?)\*{1,3}", r"\1", item)
                item = re.sub(r"\s+", " ", item).strip()
                if item:
                    extracted.append(item)
            items = ([prefix] if prefix and not re.search(r"summary-point-card", prefix, re.I) else []) + extracted
        else:
            # Plain text or other HTML: convert block boundaries to separate lines.
            cleaned = re.sub(r"(?i)<br\s*/?>", "\n", cleaned)
            cleaned = re.sub(r"(?i)</(?:div|p|li|h[1-6])\s*>", "\n", cleaned)
            cleaned = re.sub(r"(?i)<li\b[^>]*>", "- ", cleaned)
            cleaned = re.sub(r"(?is)<[^>]+>", " ", cleaned)
            cleaned = html.unescape(cleaned)
            items = cleaned.splitlines()

        # If the AI returns one long paragraph instead of separate bullets,
        # split it into individual sentences so each fact gets its own visual row.
        if len(items) == 1 and len(items[0]) > 180:
            paragraph = re.sub(r"\s+", " ", items[0]).strip()
            sentence_items = re.split(r"(?<=[.!?])\s+(?=[A-ZðŸ“…â˜€ï¸ðŸ’šðŸ—“ï¸ðŸ‘¥âœ…ðŸ“ŒðŸ“‹â±ï¸])", paragraph)
            sentence_items = [part.strip() for part in sentence_items if part.strip()]
            if len(sentence_items) > 1:
                items = sentence_items

        result = []
        for item in items:
            item = item.strip()
            item = re.sub(r"^\s*(?:[-*â€¢]|\d+[.)])\s*", "", item)
            item = re.sub(r"\*{1,3}([^*]+?)\*{1,3}", r"\1", item)
            item = re.sub(r"_{1,2}([^_]+?)_{1,2}", r"\1", item)
            item = re.sub(r"(?is)<[^>]+>", "", item)
            item = re.sub(r"\s+", " ", item).strip()
            # Never render HTML fragments or empty strings as card content.
            if item and not re.search(r"</?div\b|summary-point-(?:card|text|number)", item, re.I):
                result.append(item)

        # De-duplicate any repeated text introduced by malformed markup.
        deduped = []
        for item in result:
            if item not in deduped:
                deduped.append(item)
        return deduped

    def summary_icon_and_heading(point):
        """Choose a relevant icon and concise heading for a summary point."""
        value = str(point).strip()
        lower = value.lower()
        rules = [
            (("effective date", "effective from", "takes effect", "policy date", "start date", "date of issue", "issued on"), ("ðŸ“…", "Important date")),
            (("annual leave", "vacation", "yearly leave"), ("â˜€ï¸", "Annual leave")),
            (("sick leave", "medical leave", "illness"), ("ðŸ’š", "Sick leave")),
            (("public holiday", "holiday"), ("ðŸ—“ï¸", "Public holidays")),
            (("eligibility", "eligible", "service period", "probation"), ("ðŸ‘¥", "Eligibility")),
            (("approval", "manager", "notice period", "advance notice"), ("âœ…", "Approval and notice")),
            (("carry forward", "carry-forward", "unused leave"), ("ðŸ“Œ", "Carry-forward rules")),
            (("requirement", "required", "must ", "mandatory", "condition", "conditions"), ("ðŸ“‹", "Requirements")),
            (("certificate", "certifies", "completed", "completion"), ("ðŸ†", "Certification")),
            (("duration", "period", "months", "years", "days"), ("â±ï¸", "Duration and limits")),
            (("purpose", "focuses on", "subject", "covers", "overview"), ("ðŸ“˜", "Document overview")),
        ]
        for keywords, result in rules:
            if any(keyword in lower for keyword in keywords):
                return result
        match = re.match(r"^([^:]{3,48}):\s*(.+)$", value)
        if match:
            return "ðŸ”Ž", match.group(1).strip().strip("*_")
        return "ðŸ“", "Key point"

    def render_summary_cards(title, filename, text, card_class):
        """Render clean, professional summary points with icons and dividers."""
        points = summary_items(text)
        safe_title = html.escape(title)
        safe_filename = html.escape(str(filename))

        if points:
            point_blocks = []
            for item in points:
                icon, heading = summary_icon_and_heading(item)
                label_match = re.match(r"^([^:]{3,48}):\s*(.+)$", item)
                if label_match:
                    heading = label_match.group(1).strip().strip("*_")
                    body = label_match.group(2).strip()
                else:
                    body = item
                point_blocks.append(
                    '<div class="professional-summary-point">'
                    f'<div class="professional-summary-icon">{icon}</div>'
                    '<div class="professional-summary-content">'
                    f'<div class="professional-summary-heading">{html.escape(heading)}</div>'
                    f'<div class="professional-summary-text">{html.escape(body)}</div>'
                    '</div></div>'
                )
            points_html = '<div class="professional-summary-list">' + ''.join(point_blocks) + '</div>'
        else:
            points_html = (
                '<div class="professional-summary-empty">'
                '<span class="professional-summary-icon">ðŸ“</span>'
                '<span>A summary was not provided in the AI response.</span></div>'
            )

        st.markdown(
            f'<div class="summary-card {card_class} professional-summary-card">'
            '<div class="professional-summary-header">'
            f'<div class="summary-title">{safe_title}</div>'
            f'<div class="summary-file">{safe_filename}</div>'
            '</div><div class="summary-divider"></div>'
            f'{points_html}</div>',
            unsafe_allow_html=True,
        )

    with summary_col_a:
        render_summary_cards(
            "ðŸ“˜ Document A Â· Original",
            st.session_state["document_a_name"],
            summary_a,
            "summary-card-a",
        )

    with summary_col_b:
        render_summary_cards(
            "ðŸ“— Document B Â· Updated",
            st.session_state["document_b_name"],
            summary_b,
            "summary-card-b",
        )

    # Quick findings + detailed comparison cards. Only these two sections are redesigned.
    st.markdown("---")
    st.markdown("## ðŸ”Ž Important Changes at a Glance")
    st.caption("A compact before-and-after overview of the key changes found in your documents.")

    rows = parse_value_pairs(differences)
    if rows:
        changed_rows = [row for row in rows if row["Change"] != "No change"]
        unchanged_rows = [row for row in rows if row["Change"] == "No change"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Items compared", len(rows))
        c2.metric("Items with changes", len(changed_rows))
        c3.metric("Items unchanged", len(unchanged_rows))

        icon_map = {
            "date": "ðŸ“…", "leave": "ðŸŒ¿", "eligibility": "ðŸ‘¥", "notice": "â±ï¸",
            "approval": "â±ï¸", "carry": "ðŸ“„", "holiday": "ðŸŽ‰", "handover": "ðŸ“",
        }
        for row_start in range(0, len(rows), 3):
            cols = st.columns(3, gap="medium")
            for col, item in zip(cols, rows[row_start:row_start + 3]):
                key = item["Item"].lower()
                icon = next((v for k, v in icon_map.items() if k in key), "ðŸ”Ž")
                status = item.get("Change", "Changed")
                status_color = "#059669" if status == "No change" else "#c026d3"

                with col:
                    title = html.escape(str(item["Item"]))
                    value_a = html.escape(
                        str(professional_value(item["Item"], item["Document A"]))
                    )
                    value_b = html.escape(
                        str(professional_value(item["Item"], item["Document B"]))
                    )
                    explanation = html.escape(
                        str(change_explanation(
                            item["Item"],
                            item["Document A"],
                            item["Document B"],
                            status,
                        ))
                    )
                    safe_status = html.escape(str(status))

                    st.html(
                        textwrap.dedent(f"""
                        <div class="change-glance-card">
                            <div style="display:flex;align-items:center;gap:9px;margin-bottom:14px;">
                                <span style="font-size:25px;">{icon}</span>
                                <b class="change-glance-title">{title}</b>
                            </div>

                            <div class="change-glance-status">
                                {safe_status}
                            </div>

                            <div style="display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);gap:7px;align-items:stretch;margin-top:12px;">
                                <div style="padding:11px 7px;border-radius:11px;background:linear-gradient(145deg,#eff6ff,#dbeafe);text-align:center;min-width:0;">
                                    <div style="font-size:10px;color:#4f46e5;font-weight:800;">DOCUMENT A</div>
                                    <div class="change-glance-value-a">{value_a}</div>
                                </div>

                                <span class="change-glance-arrow" style="align-self:center;">â†’</span>

                                <div style="padding:11px 7px;border-radius:11px;background:linear-gradient(145deg,#ecfdf5,#d1fae5);text-align:center;min-width:0;">
                                    <div style="font-size:10px;color:#059669;font-weight:800;">DOCUMENT B</div>
                                    <div class="change-glance-value-b">{value_b}</div>
                                </div>
                            </div>

                            <div class="change-glance-explanation">
                                â„¹ï¸ {explanation}
                            </div>
                        </div>
                        """).strip(),
                    )

    else:
        st.info("No structured A/B comparisons could be extracted from the difference section. The original AI analysis remains available below.")

    st.markdown("## ðŸ“‹ Detailed Differences")
    st.markdown("<p style=\"font-size:18px;line-height:1.7;color:#475569;margin:0 0 18px 0;letter-spacing:normal;word-spacing:normal;\">Explore each difference in a colorful side-by-side view, with the explanation kept in its own full-width card.</p>", unsafe_allow_html=True)
    if rows:
        for index, item in enumerate(rows, start=1):
            status = item.get("Change", "Changed")
            status_color = "#047857" if status == "No change" else "#a21caf"
            status_bg = "#d1fae5" if status == "No change" else "#fae8ff"
            key = item["Item"].lower()
            icon = next((v for k, v in icon_map.items() if k in key), "ðŸ”Ž")
            value_a = html.escape(str(professional_value(item["Item"], item["Document A"])))
            value_b = html.escape(str(professional_value(item["Item"], item["Document B"])))
            explanation = html.escape(str(change_explanation(item["Item"], item["Document A"], item["Document B"], status)))

            # Keep each difference self-contained; scoped inline styles prevent long values
            # from overflowing their cards or inheriting letter spacing from other UI areas.

            with st.container(border=True):
                st.html(
                    textwrap.dedent(f"""
                    <div style="width:100%;max-width:100%;min-width:0;box-sizing:border-box;
                    display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:0 0 16px 0;
                    padding:12px 14px;border-radius:13px;
                    background:linear-gradient(110deg,#eef2ff 0%,#fdf4ff 55%,#ecfeff 100%);
                    border:1px solid #e0e7ff;letter-spacing:normal;word-spacing:normal;
                    white-space:normal;overflow-wrap:anywhere;">
                        <span style="font-size:25px;line-height:1.2;flex:0 0 auto">{icon}</span>
                        <div style="flex:1 1 180px;min-width:0;font-size:24px;line-height:1.4;
                        font-weight:800;color:#172554;overflow-wrap:anywhere;word-break:normal;">
                            {index}. {html.escape(str(item['Item']))}
                        </div>
                        <span style="display:inline-block;max-width:100%;box-sizing:border-box;
                        padding:5px 10px;border-radius:999px;background:{status_bg};
                        color:{status_color};font-size:15px;line-height:1.5;font-weight:800;
                        white-space:normal;overflow-wrap:anywhere;">
                            {html.escape(str(status))}
                        </span>
                    </div>
                    """).strip(),
                )

                before_col, after_col = st.columns(2, gap="medium")
                with before_col:

                    st.html(
                        textwrap.dedent(f"""
                        <div style="width:100%;max-width:100%;min-width:0;box-sizing:border-box;
                        padding:15px;border-radius:13px;
                        background:linear-gradient(145deg,#eff6ff,#e0e7ff);
                        border:1px solid #c7d2fe;border-top:4px solid #6366f1;
                        overflow-wrap:anywhere;word-break:normal;white-space:normal;letter-spacing:normal;">
                            <div style="font-size:15px;line-height:1.5;color:#4338ca;font-weight:800;letter-spacing:.04em;">
                                DOCUMENT A Â· BEFORE
                            </div>
                            <div style="font-size:21px;line-height:1.65;color:#1e3a8a;font-weight:750;margin-top:10px;
                            overflow-wrap:anywhere;word-break:normal;white-space:normal;">
                                {value_a}
                            </div>
                        </div>
                        """).strip(),
                    )

                with after_col:

                    st.html(
                        textwrap.dedent(f"""
                        <div style="width:100%;max-width:100%;min-width:0;box-sizing:border-box;
                        padding:15px;border-radius:13px;
                        background:linear-gradient(145deg,#ecfdf5,#ccfbf1);
                        border:1px solid #a7f3d0;border-top:4px solid #10b981;
                        overflow-wrap:anywhere;word-break:normal;white-space:normal;letter-spacing:normal;">
                            <div style="font-size:15px;line-height:1.5;color:#047857;font-weight:800;letter-spacing:.04em;">
                                DOCUMENT B Â· AFTER
                            </div>
                            <div style="font-size:21px;line-height:1.65;color:#065f46;font-weight:750;margin-top:10px;
                            overflow-wrap:anywhere;word-break:normal;white-space:normal;">
                                {value_b}
                            </div>
                        </div>
                        """).strip(),
                    )



                st.html(
                    textwrap.dedent(f"""
                    <div style="width:100%;max-width:100%;min-width:0;box-sizing:border-box;
                    margin-top:13px;padding:14px 15px;border-radius:12px;
                    background:linear-gradient(110deg,#fff7ed,#fff1f2 60%,#fdf4ff);
                    border:1px solid #fed7aa;border-left:4px solid #f97316;
                    overflow-wrap:anywhere;word-break:normal;white-space:normal;letter-spacing:normal;">
                        <div style="font-size:15px;line-height:1.5;color:#9a3412;font-weight:800;letter-spacing:.04em;">
                            ðŸ’¡ WHAT CHANGED
                        </div>
                        <div style="font-size:19px;line-height:1.8;color:#334155;margin-top:9px;
                        overflow-wrap:anywhere;word-break:normal;white-space:normal;">
                            {explanation}
                        </div>
                    </div>
                    """).strip(),
                )

    elif differences:
        # Keep unparseable AI text visible rather than discarding it.
        fallback_items = make_bullets(differences) or [line.strip() for line in differences.splitlines() if line.strip()]
        for index, item_text in enumerate(fallback_items, start=1):
            with st.container(border=True):
                st.markdown(f"**ðŸ”Ž Difference {index}**")
                st.write(item_text)
    else:
        st.info("No clearly labelled differences section was found in the AI response.")

    # Similarities
    st.markdown("---")
    st.markdown("## ðŸ¤ What stayed the same")
    if similarities:
        with st.container(border=True):
            display_readable_bullets(similarities)
    else:
        st.info("No clearly labelled similarities section was found.")

    # New / changed requirements â€” redesigned section only.
    # Parse common natural-language requirement lines without changing other sections.
    st.markdown("## ðŸ†• New or Changed Requirements")
    st.caption("Key updates, additions and new requirements found in the uploaded documents.")

    def parse_requirement_cards(raw_text):
        if not raw_text:
            return []
        clean_text = html.unescape(str(raw_text))
        clean_text = re.sub(r"```(?:\w+)?", "", clean_text)
        clean_text = re.sub(r"<[^>]+>", " ", clean_text)
        clean_text = clean_text.replace("\r", "")
        lines = []
        for raw_line in clean_text.splitlines():
            line = re.sub(r"^\s*(?:[-*â€¢]+|\d+[.)])\s*", "", raw_line).strip()
            line = re.sub(r"\*{1,3}|_{1,3}|`", "", line).strip()
            if line:
                lines.append(line)
        joined = "\n".join(lines)
        # Also split multiple labelled requirements if the model puts them on one line.
        starts = re.compile(
            r"(?i)(?=(?:Eligibility Period|Eligibility|Advance Notice|Leave Approval Notice|"
            r"Carry Forward Limit|Carry Forward|Carry-Forward Limit|Handover Note|"
            r"Handover Note Requirement)\s*(?:\([^)]*\))?\s*:)"
        )
        chunks = [part.strip(" \n;â€¢-") for part in starts.split(joined) if part.strip(" \n;â€¢-")]
        items = []
        aliases = {
            "eligibility period": "Eligibility Period", "eligibility": "Eligibility Period",
            "advance notice": "Advance Notice", "leave approval notice": "Advance Notice",
            "carry forward limit": "Carry Forward Limit", "carry forward": "Carry Forward Limit",
            "carry-forward limit": "Carry Forward Limit", "handover note": "Handover Note",
            "handover note requirement": "Handover Note",
        }
        for chunk in chunks:
            match = re.match(
                r"^\s*(Eligibility Period|Eligibility|Advance Notice|Leave Approval Notice|"
                r"Carry Forward Limit|Carry Forward|Carry-Forward Limit|Handover Note Requirement|Handover Note)"
                r"\s*(?:\((Changed|New|Added|Updated|Unchanged)[^)]*\))?\s*:\s*(.*)$",
                chunk, re.I | re.S,
            )
            if not match:
                continue
            raw_label, raw_status, body = match.groups()
            label = aliases.get(raw_label.casefold(), raw_label.title())
            body = re.sub(r"\s+", " ", body).strip(" .;\t")
            status = "New" if (raw_status and raw_status.casefold() in {"new", "added"}) or label == "Handover Note" else "Changed"
            a_value = b_value = explanation = ""

            # Explicit Document A / Document B natural-language comparisons.
            a_match = re.search(r"\bDocument\s*A\b\s*", body, re.I)
            b_match = re.search(r"\bDocument\s*B\b\s*", body, re.I)
            if a_match and b_match and a_match.start() < b_match.start():
                a_value = body[a_match.end():b_match.start()].strip(" ,;:-")
                b_value = body[b_match.end():].strip(" ,;:-.")
            elif label == "Eligibility Period":
                nums = re.findall(r"\b(\d+)\s*months?\b", body, re.I)
                if len(nums) >= 2:
                    a_value, b_value = f"{nums[0]} months of service", f"{nums[1]} months of service"
                explanation = f"The eligibility period has been extended from {a_value or 'the original period'} to {b_value or 'the updated period'}."
            elif label == "Advance Notice":
                nums = re.findall(r"\b(\d+)\s*days?\b", body, re.I)
                if len(nums) >= 2:
                    a_value, b_value = f"{nums[0]} days in advance", f"{nums[1]} days in advance"
                explanation = f"The advance notice period has been increased from {a_value or 'the original period'} to {b_value or 'the updated period'} for leave requests."
            elif label == "Carry Forward Limit":
                nums = re.findall(r"\b(\d+)\s*days?\b", body, re.I)
                if len(nums) >= 2:
                    a_value, b_value = f"{nums[0]} days of unused leave", f"{nums[1]} days of unused leave"
                explanation = f"The carry forward limit has been reduced from {a_value or 'the original limit'} to {b_value or 'the updated limit'} of unused annual leave."
            elif label == "Handover Note":
                a_value, b_value = "Not mentioned in policy", "Required for 3 or more consecutive working days of leave"
                explanation = "A new requirement has been added for employees to submit a handover note before taking 3 or more consecutive working days of leave."

            # Extract values from concise wording such as "Extended from 3 months to 6 months".
            if label == "Eligibility Period" and (not a_value or not b_value):
                nums = re.findall(r"\b(\d+)\s*months?\b", body, re.I)
                if len(nums) >= 2: a_value, b_value = f"{nums[0]} months of service", f"{nums[1]} months of service"
            if label == "Advance Notice" and (not a_value or not b_value):
                nums = re.findall(r"\b(\d+)\s*days?\b", body, re.I)
                if len(nums) >= 2: a_value, b_value = f"{nums[0]} days in advance", f"{nums[1]} days in advance"
            if label == "Carry Forward Limit" and (not a_value or not b_value):
                nums = re.findall(r"\b(\d+)\s*days?\b", body, re.I)
                if len(nums) >= 2: a_value, b_value = f"{nums[0]} days of unused leave", f"{nums[1]} days of unused leave"

            if label == "Handover Note":
                status = "New"
                a_value = a_value or "Not mentioned in policy"
                b_value = b_value or "Required for 3 or more consecutive working days of leave"
                explanation = explanation or body
            else:
                explanation = explanation or body
            if a_value and b_value:
                if not any(item["label"] == label for item in items):
                    items.append({"label": label, "status": status, "a": a_value, "b": b_value, "explanation": explanation})
        return items

    requirement_items = parse_requirement_cards(requirements)
    if requirement_items:
        st.markdown(
            f"<div style='display:flex;align-items:center;justify-content:space-between;gap:12px;margin:8px 0 18px;'>"
            f"<span style='color:#475569;font-size:13px'>Detailed view of all new and updated policy requirements.</span>"
            f"<span style='padding:7px 13px;border-radius:22px;background:#ede9fe;color:#6d28d9;font-weight:700;font-size:12px'>âœ¦ {len(requirement_items)} items found</span></div>",
            unsafe_allow_html=True,
        )
        requirement_icons = {"eligibility period": "ðŸ‘¥", "advance notice": "ðŸ•’", "carry forward limit": "ðŸ—“ï¸", "handover note": "ðŸ“„"}
        for item in requirement_items:
            icon = requirement_icons.get(item["label"].casefold(), "ðŸ“Œ")
            is_new = item["status"] == "New"
            badge_bg = "#d1fae5" if is_new else "#fae8ff"
            badge_color = "#047857" if is_new else "#a21caf"
            with st.container(border=True):
                left, values, explanation_col = st.columns([1.05, 1.75, 1.0], gap="medium")
                with left:
                    st.markdown(
                        f"<div style='padding:8px 0 4px'><div style='font-size:30px;margin-bottom:8px'>{icon}</div>"
                        f"<span style='display:inline-block;padding:4px 11px;border-radius:20px;background:{badge_bg};color:{badge_color};font-size:11px;font-weight:800'>{item['status']}</span>"
                        f"<div style='font-size:19px;font-weight:800;color:#172554;margin-top:10px'>{html.escape(item['label'])}</div></div>",
                        unsafe_allow_html=True,
                    )
                with values:
                    st.markdown(
                        f"<div style='display:grid;grid-template-columns:1fr auto 1fr;gap:9px;align-items:stretch;margin:8px 0;'>"
                        f"<div style='border:1px solid #bfdbfe;border-radius:12px;overflow:hidden;background:#f8fbff;text-align:center;'>"
                        f"<div style='padding:9px 5px;background:#eaf3ff;color:#1d4ed8;font-size:12px;font-weight:800'>ðŸ“„ Document A (Original)</div>"
                        f"<div style='padding:15px 8px;color:#1e3a8a;font-size:16px;font-weight:800;min-height:67px;display:flex;align-items:center;justify-content:center'>{html.escape(item['a'])}</div>"
                        f"<div style='margin:0 9px 9px;padding:6px;border-radius:8px;background:#eaf3ff;color:#2563eb;font-size:11px;font-weight:700'>Original value</div></div>"
                        f"<div style='display:flex;align-items:center;justify-content:center;color:#6d28d9;font-size:23px;font-weight:800'>âžœ</div>"
                        f"<div style='border:1px solid #a7f3d0;border-radius:12px;overflow:hidden;background:#f5fffb;text-align:center;'>"
                        f"<div style='padding:9px 5px;background:#e3faf1;color:#047857;font-size:12px;font-weight:800'>ðŸ“„ Document B (Updated)</div>"
                        f"<div style='padding:15px 8px;color:#065f46;font-size:16px;font-weight:800;min-height:67px;display:flex;align-items:center;justify-content:center'>{html.escape(item['b'])}</div>"
                        f"<div style='margin:0 9px 9px;padding:6px;border-radius:8px;background:#e3faf1;color:#047857;font-size:11px;font-weight:700'>{'New requirement' if is_new else 'Updated value'}</div></div></div>",
                        unsafe_allow_html=True,
                    )
                with explanation_col:
                    st.markdown(
                        f"<div style='height:100%;padding:14px;border-radius:12px;background:linear-gradient(135deg,#f5f3ff,#f8fafc);'>"
                        f"<div style='font-size:14px;font-weight:800;color:#4f46e5;margin-bottom:10px'>ðŸ’¡ Explanation</div>"
                        f"<div style='font-size:13px;line-height:1.65;color:#334155'>{html.escape(item['explanation'])}</div>"
                        f"<div style='display:inline-block;margin-top:12px;padding:5px 11px;border-radius:20px;background:{badge_bg};color:{badge_color};font-size:11px;font-weight:800'>âœ“ {item['status']}</div></div>",
                        unsafe_allow_html=True,
                    )
    else:
        st.info(
            "No separate requirements could be structured from the AI response. "
            "Check the detailed analysis for possible requirement changes."
        )

    # Key facts and conclusion, placed in compact expanders.
    with st.expander("ðŸ“… View key facts and important deadlines", expanded=False):
        if key_facts:
            display_readable_bullets(key_facts)
        else:
            st.info("No clearly labelled key facts section was found.")


    if conclusion:
        # Handle both string and list formats safely.
        if isinstance(conclusion, str):
            conclusion_text = conclusion.strip()
        else:
            conclusion_text = " ".join(
                re.sub(
                    r"^\s*(?:[-*â€¢]|\d+[.)])\s*",
                    "",
                    str(part),
                ).strip()
                for part in conclusion
                if str(part).strip()
            )

        conclusion_text = html.unescape(conclusion_text)
        conclusion_text = re.sub(r"\s+", " ", conclusion_text).strip()

        # Detect AI conclusions that have lost their word spacing.
        normalized_text = re.sub(
            r"[^a-z0-9]",
            "",
            conclusion_text.casefold(),
        )

        missing_spaces = (
            len(normalized_text) > 40
            and len(conclusion_text.split()) <= 2
        )

        # If spacing is broken, rebuild the conclusion using
        # the structured comparison results.
        if missing_spaces:
            conclusion_parts = []

            for item in rows:
                if item.get("Change") == "No change":
                    continue

                label = str(item.get("Item", "")).strip()

                value_a = professional_value(
                    label,
                    item.get("Document A", ""),
                )
                value_b = professional_value(
                    label,
                    item.get("Document B", ""),
                )

                if label and value_a and value_b:
                    conclusion_parts.append(
                        f"{label}: Document A specifies {value_a}; "
                        f"Document B specifies {value_b}"
                    )

            if conclusion_parts:
                conclusion_text = (
                    "The documents differ in the following key areas: "
                    + "; ".join(conclusion_parts)
                    + ". Please review the detailed comparison for context."
                )

            elif requirement_items:
                requirement_summaries = [
                    str(item.get("explanation", "")).strip()
                    for item in requirement_items
                    if str(item.get("explanation", "")).strip()
                ]

                if requirement_summaries:
                    conclusion_text = " ".join(requirement_summaries)
                else:
                    conclusion_text = (
                        "The AI-generated conclusion could not be displayed "
                        "reliably. Please review the complete AI analysis below."
                    )
            else:
                conclusion_text = (
                    "The AI-generated conclusion could not be displayed "
                    "reliably because its word spacing is missing. "
                    "Please review the complete AI analysis below."
                )

        # Escape text before displaying it as HTML.
        safe_conclusion = html.escape(conclusion_text)

        st.markdown(
            f"""
            <style>
                .overall-conclusion-card {{
                    position: relative;
                    overflow: hidden;
                    margin: 8px 0 22px;
                    padding: 26px 28px 25px;
                    border: 1px solid #c7d2fe;
                    border-radius: 22px;
                    background: linear-gradient(135deg, #eef2ff 0%, #ffffff 52%, #ecfdf5 100%);
                    box-shadow: 0 12px 30px rgba(79, 70, 229, .10);
                    animation: conclusion-enter .55s ease both;
                }}
                .overall-conclusion-card:before {{
                    content: "";
                    position: absolute;
                    inset: 0 auto 0 0;
                    width: 6px;
                    background: linear-gradient(180deg, #6366f1, #06b6d4, #10b981);
                }}
                .overall-conclusion-top {{
                    display: flex; align-items: center; gap: 14px; margin-bottom: 15px;
                }}
                .overall-conclusion-icon {{
                    display: flex; align-items: center; justify-content: center;
                    flex: 0 0 52px; width: 52px; height: 52px; border-radius: 16px;
                    background: linear-gradient(135deg, #e0e7ff, #d1fae5);
                    box-shadow: inset 0 0 0 1px rgba(99,102,241,.12); font-size: 27px;
                }}
                .overall-conclusion-kicker {{
                    margin: 0 0 3px; color: #6366f1; font-size: 11px;
                    font-weight: 800; letter-spacing: 1.4px; text-transform: uppercase;
                }}
                .overall-conclusion-title {{ margin: 0; color: #172554; font-size: 23px; font-weight: 850; line-height: 1.3; }}
                .overall-conclusion-subtitle {{ margin: 5px 0 0; color: #64748b; font-size: 13px; }}
                .overall-conclusion-divider {{ height: 1px; margin: 0 0 16px; background: linear-gradient(90deg, #c7d2fe, #d1fae5, transparent); }}
                .overall-conclusion-text {{ margin: 0; color: #334155; font-size: 16px; line-height: 1.9; overflow-wrap: anywhere; }}
                .overall-conclusion-foot {{ display: flex; align-items: center; gap: 8px; margin-top: 18px; color: #475569; font-size: 12px; font-weight: 700; }}
                .overall-conclusion-foot span {{ display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 8px; background: #d1fae5; color: #047857; }}
                @keyframes conclusion-enter {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
                @media (max-width: 700px) {{
                    .overall-conclusion-card {{ padding: 20px 17px 20px 21px; border-radius: 17px; }}
                    .overall-conclusion-icon {{ flex-basis: 43px; width: 43px; height: 43px; font-size: 23px; border-radius: 13px; }}
                    .overall-conclusion-title {{ font-size: 20px; }}
                    .overall-conclusion-text {{ font-size: 14px; line-height: 1.8; }}
                }}
                @media (prefers-reduced-motion: reduce) {{ .overall-conclusion-card {{ animation: none; }} }}
            </style>
            <div class="section-heading">
                <span class="section-icon">ðŸ§ </span>
                <div>
                    <h3>Overall Conclusion</h3>
                    <p>Summary of the comparison results</p>
                </div>
            </div>

            <div class="overall-conclusion-card">
                <div class="overall-conclusion-top">
                    <div class="overall-conclusion-icon">ðŸ§ </div>
                    <div>
                        <p class="overall-conclusion-kicker">AI comparison insight</p>
                        <h4 class="overall-conclusion-title">Overall Conclusion</h4>
                        <p class="overall-conclusion-subtitle">What changed between the original and updated documents</p>
                    </div>
                </div>
                <div class="overall-conclusion-divider"></div>
                <p class="overall-conclusion-text">{safe_conclusion}</p>
                <div class="overall-conclusion-foot"><span>âœ“</span> Review the detailed comparison for individual changes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Display the key changes identified by the comparison.
    if rows:
        changed_rows = [
            item
            for item in rows
            if str(item.get("Change", "")).strip().casefold()
            not in {"no change", "unchanged", "same"}
        ]

        if changed_rows:
            st.markdown(
                """
                <div class="section-heading">
                    <span class="section-icon">ðŸ“Œ</span>
                    <div>
                        <h3>Key Changes Identified</h3>
                        <p>Important differences between the two documents</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


            for item in changed_rows:
                label = str(item.get("Item", "Difference")).strip()

                value_a = professional_value(
                    label,
                    item.get("Document A", ""),
                )
                value_b = professional_value(
                    label,
                    item.get("Document B", ""),
                )

                status = str(item.get("Change", "Changed")).strip()

                explanation = change_explanation(
                    label,
                    value_a,
                    value_b,
                    status,
                )




                st.markdown(
                    f"""
                    <div style="width:100%;max-width:100%;min-width:0;box-sizing:border-box;
                    display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:0 0 16px 0;
                    padding:12px 14px;border-radius:13px;
                    background:linear-gradient(110deg,#eef2ff 0%,#fdf4ff 55%,#ecfeff 100%);
                    border:1px solid #e0e7ff;letter-spacing:normal;word-spacing:normal;
                    white-space:normal;overflow-wrap:anywhere;">
                        <span style="font-size:25px;line-height:1.2;flex:0 0 auto">{icon}</span>
                        <div style="flex:1 1 180px;min-width:0;font-size:24px;line-height:1.4;
                        font-weight:800;color:#172554;overflow-wrap:anywhere;word-break:normal;">
                            {index}. {html.escape(str(item['Item']))}
                        </div>
                        <span style="display:inline-block;max-width:100%;box-sizing:border-box;
                        padding:5px 10px;border-radius:999px;background:{status_bg};
                        color:{status_color};font-size:15px;line-height:1.5;font-weight:800;
                        white-space:normal;overflow-wrap:anywhere;">
                            {html.escape(str(status))}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


        else:
            st.markdown(
                """
                <div class="summary-card">
                    <h4>âœ… No major changes identified</h4>
                    <p>The structured comparison did not identify
                    any changed items.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Keep the complete AI analysis expander below this section.


    with st.expander("ðŸ” Need more details? Open complete AI analysis", expanded=False):
        st.caption(
            "This is the original AI response. It may contain more detail than the dashboard above."
        )
        st.markdown(result)

    # Word report
    st.markdown("---")
    st.markdown("## ðŸ“¥ Export your results")
    st.caption("Download the complete AI analysis as a Word document.")

    try:
        report_bytes = generate_comparison_report(
            st.session_state["document_a_name"],
            st.session_state["document_b_name"],
            result,
        )

        st.download_button(
            label="â¬‡ï¸ Download Word Comparison Report",
            data=report_bytes,
            file_name="AI_Document_Comparison_Report.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            type="primary",
            use_container_width=True,
        )

        st.caption("Your Word report contains the complete comparison analysis.")

    except Exception as error:
        st.error("Could not generate the Word report.")
        with st.expander("Technical details"):
            st.code(str(error))


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Built with Python, Streamlit, Gemini AI and PyPDF
        <br>
        DocuCompare AI Â· Document Intelligence Workspace
    </div>
    """,
    unsafe_allow_html=True,
)
