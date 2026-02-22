import streamlit as st
import os
import tempfile
from fpdf import FPDF
import pandas as pd

from preprocessing.pdf_to_image import pdf_to_images
from preprocessing.image_cleaning import preprocess_medical_image
from ocr.ocr_engine import extract_text_from_images
from NLP.text_cleaning import clean_ocr_text
from NLP.entity_extraction import extract_entities
from diet_engine.diet_recommender import generate_diet_plan
from llm.groq_llm import build_llm_prompt, call_groq_llm
from preprocessing.pdf_text_extractor import extract_text_direct

REFERENCE_RANGES = {
    "glucose": "70 - 110 mg/dL",
    "hba1c": "4.0 - 5.6 %",
    "cholesterol": "< 200 mg/dL",
    "ldl": "< 130 mg/dL",
    "hdl": "> 40 mg/dL",
    "triglycerides": "< 150 mg/dL",
    "vitamin d": "30 - 100 ng/mL",
    "vitamin b12": "200 - 900 pg/mL",
    "creatinine": "0.7 - 1.3 mg/dL",
    "tsh": "0.4 - 4.5 mIU/L",
    "hemoglobin": "13.0 - 17.0 g/dL"
}

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AI-Generated Diet Plan", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

st.set_page_config(
    page_title="AI-Based Diet Recommendation System",
    page_icon="🥗",
    layout="wide",
)

st.markdown("""
<style>
    /* 1. GLOBAL & MAIN VIEW */
    .stApp { background: linear-gradient(135deg, #0F172A 0%, #020617 100%); }
    header[data-testid="stHeader"] { background-color: transparent !important; }

    /* Main Content Text (Forced White) */
    [data-testid="stMainView"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stMainView"] li, [data-testid="stMainView"] h1, 
    [data-testid="stMainView"] h2, [data-testid="stMainView"] h3 {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* 2. SIDEBAR (MID-GREY & ELECTRIC BLUE) */
    section[data-testid="stSidebar"] { background-color: #1F2937 !important; border-right: 1px solid #334155; }
    
    /* Sidebar Labels & Text - Electric Blue */
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] .stMarkdown p {
        color: #38BDF8 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px;
    }
    
    /* Radio Choices specifically */
    section[data-testid="stSidebar"] .stRadio label p { color: #38BDF8 !important; }

    /* 3. ELITE GLASSMORPHISM CONDITION CARDS */
    .condition-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(8px);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 6px solid #EF4444; /* Alert Red Bar */
        margin-bottom: 15px;
        color: #FFFFFF !important;
        font-weight: 600;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .condition-card:hover {
        transform: translateX(8px);
        background: rgba(30, 41, 59, 0.6);
        border-left: 8px solid #F87171;
    }

    /* 4. BUTTONS */
    /* Download Button - Realistic Success Green with Black Text */
    .stDownloadButton > button {
        background-color: #22C55E !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        border-radius: 10px !important;
        width: 100%;
        box-shadow: 0px 4px 15px rgba(34, 197, 94, 0.4) !important;
    }

    /* Sidebar Reset Button - Alert Red */
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #EF4444 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        width: 100%;
    }

    /* 5. TABS & DATA TABLES */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #94A3B8 !important; font-weight: 700 !important; }
    .stTabs [data-baseweb="tab--active"] { color: #38BDF8 !important; border-bottom-color: #38BDF8 !important; }
    
    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        background-color: #111827 !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 12px !important;
    }
            
    /* Target the specific Markdown container inside the main view */
    [data-testid="stMainView"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stMainView"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stMainView"] [data-testid="stMarkdownContainer"] span {
        color: #FFFFFF !important;
        opacity: 1 !important;
        font-size: 1.05rem !important;
    }

    /* Target the Subheaders (like 'Weekly AI-Generated Diet Plan') */
    [data-testid="stMainView"] h2, 
    [data-testid="stMainView"] h3 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    .stMarkdown {
        color: #FFFFFF !important;
    }
            
    /* Targets the text specifically within any Subheader in the Main View */
    [data-testid="stMainView"] [data-testid="stHeaderBlock"] h3,
    [data-testid="stMainView"] .stMarkdown h3,
    [data-testid="stMainView"] h3 div {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }

    [data-testid="stMainView"] h3 {
        color: #FFFFFF !important;
        background: transparent !important;
    }

    /* This targets the grey 'Secondary Text' class Streamlit often injects */
    .st-emotion-cache-10trblm, .st-emotion-cache-zt5igj {
        color: #FFFFFF !important;
    }
            
    /* Targets 'Settings', 'Personal Details', and 'BMI' specifically */
    section[data-testid="stSidebar"] h2 {
        color: #FFFFFF !important; 
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border-bottom: 2px solid rgba(56, 189, 248, 0.3); 
        padding-bottom: 5px;
        margin-top: 20px !important;
    }

    /* Keeps all other sidebar text (Age, Gender, etc.) Electric Blue */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #38BDF8 !important;
        font-weight: 600 !important;
    }

</style>
""", unsafe_allow_html=True)

if "results" not in st.session_state:
    st.session_state["results"] = {
        "done": False,
        "weekly_plan": "",
        "entities": {},
        "diet_data": {}
    }

st.markdown("<h1 style='text-align: center; color: #ffffff;'>🥗 AI-Based Diet Recommendation System</h1>", unsafe_allow_html=True)
st.info(
    "Upload your medical report (PDF). "
    "The system will analyze it and generate a personalized weekly diet plan."
)

with st.sidebar:
    st.header("Settings")
    diet_type = st.radio(
        "Diet Preference",
        ["Veg", "Non-Veg"],
        horizontal=True
    )

    st.header("Personal Details")

    age = st.number_input("Age", min_value=5, max_value=150, value=24)
    gender = st.radio("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=80, max_value=250, value=160)
    weight = st.number_input("Weight (kg)", min_value=40, max_value=400, value=70)

    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        bmi_category = "Underweight"
    elif bmi < 25:
        bmi_category = "Normal"
    elif bmi < 30:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obese"

    st.header("BMI")
    st.write(f"**BMI:** {bmi}")
    st.write(f"**Category:** {bmi_category}")

    if st.button("Reset Analysis", use_container_width=True):
        st.session_state["results"]["done"] = False
        st.session_state["results"]["weekly_plan"] = ""
        st.session_state["results"]["entities"] = {}
        st.session_state["results"]["diet_data"] = {}
        st.rerun()

uploaded_file = st.file_uploader("Upload medical report (PDF)", type=["pdf"])
if uploaded_file is not None and not st.session_state["results"]["done"]:
    with st.spinner("Analyzing your medical report..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                pdf_path = tmp_file.name

            direct_text = extract_text_direct(pdf_path)
            if len(direct_text.strip()) > 200:
                raw_text = direct_text
            else:
                st.info("Scanned PDF detected. Running OCR...")
                images = pdf_to_images(pdf_path, dpi=120)  
                raw_text = extract_text_from_images(images)
            clean_text = clean_ocr_text(raw_text)
            entities = extract_entities(clean_text)
            st.write("Extracted Entities Count:", len(entities))

            diet_data = generate_diet_plan(
                entities=entities,
                bmi=bmi,
                bmi_category=bmi_category
            )
            prompt = build_llm_prompt(diet_data, diet_type)
            weekly_plan = call_groq_llm(prompt)
            st.session_state["results"] = {
                "done": True,
                "weekly_plan": weekly_plan,
                "entities": entities,
                "diet_data": diet_data
            }

            os.unlink(pdf_path)
            st.rerun()
        except Exception as e:
            st.error("An error occurred while processing the report.")
            st.code(str(e), language="python")

if st.session_state["results"]["done"]:
    tab_med, tab_diet = st.tabs(["Medical Analysis", "Your Weekly Diet Plan"])
    with tab_med:
        col1, col2 = st.columns([1,1.5])
        with col1:
            st.markdown("<h2>Conditions Identified:</h2>", unsafe_allow_html=True)
            conditions = st.session_state["results"]["diet_data"].get("Detected Conditions", [])

            if conditions:
                for c in conditions:
                    st.markdown(
                     f"<div class='condition-card'>{c}</div>",
                    unsafe_allow_html=True
                    )
            else:
                st.success("No critical issues detected")
        with col2:
            st.subheader("Extracted Lab Values")
            entities = st.session_state["results"]["entities"]
            key_rows, other_rows = [], []

            for k, v in entities.items():
                row = {
                    "Test": k, 
                    "Result": v.get("value"), 
                    "Unit": v.get("unit"), 
                    "Normal Range": "N/A"
                }
                
                is_key = False
                for key_term, range_val in REFERENCE_RANGES.items():
                    if key_term in k.lower():
                        row["Normal Range"] = range_val
                        is_key = True
                        break
                
                if is_key: key_rows.append(row)
                else: other_rows.append(row)

            if key_rows:
                st.dataframe(pd.DataFrame(key_rows), hide_index=True, use_container_width=True)

            if other_rows:
                with st.expander("View Additional Laboratory Data"):
                    st.dataframe(pd.DataFrame(other_rows), hide_index=True, use_container_width=True)

    with tab_diet:
        st.subheader("Weekly AI-Generated Diet Plan")
        weekly_plan = st.session_state["results"]["weekly_plan"]
        st.markdown(weekly_plan)
        pdf_data = create_pdf(weekly_plan)
        st.download_button(
            label="Download Diet Plan as PDF",
            data=pdf_data,
            file_name="My_Diet_Plan_AI.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    st.info(
        "**Disclaimer:** Please consult a doctor before making any changes in the diet."
    )