import streamlit as st
from analysis_pipeline import analyze_report
from utils.pdf_generator import generate_diet_pdf

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="AI NutriCare",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------
# Modern Gradient UI CSS
# -------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(120deg, #e8f5e9, #f1f8e9);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2e7d32, #43a047);
        padding: 20px;
    }

    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select {
        background-color: white !important;
        color: black !important;
        border-radius: 8px !important;
    }

    h1 {
        color: #2e7d32;
        font-weight: 700;
    }

    div.stButton > button {
        background-color: #2e7d32;
        color: white;
        font-size: 16px;
        height: 45px;
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
    }

    div.stDownloadButton > button {
        background-color: #1976d2;
        color: white;
        border-radius: 10px;
        height: 45px;
        font-weight: 600;
    }

    /* Active Tab Red Highlight */
    button[data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #e53935 !important;
        border-bottom: 3px solid #e53935 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("🥗 AI NutriCare Settings")

age = st.sidebar.number_input("Age", 1, 100, 30)
weight = st.sidebar.number_input("Weight (kg)", 30, 200, 60)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
food_type = st.sidebar.selectbox(
    "Food Preference",
    ["Vegetarian", "Non-Vegetarian", "Both"]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Medical Report (PDF)",
    type=["pdf"]
)

# -------------------------------
# Main UI
# -------------------------------
st.title("🥗 AI-Based Personalized Diet Plan Generator")
st.markdown(
    "Upload a medical report and get a **personalized 7-day AI diet plan** instantly."
)

st.markdown("---")

# -------------------------------
# Top Navigation Tabs
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🧪 Lab Report", "🩺 Health Analysis", "🥗 Diet Plan", "📊 Nutrition Analytics"]
)

# -------------------------------
# Analysis
# -------------------------------
if uploaded_file and st.button("🚀 Analyze Report"):

    with st.spinner("🔍 Analyzing your medical report..."):

        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        result = analyze_report(
            "temp.pdf", age, gender, weight, food_type
        )

    st.success("✅ Analysis Complete!")

    # -------------------------------
    # 🧪 LAB REPORT TAB
    # -------------------------------
    with tab1:
        st.subheader("🧪 Extracted Lab Values")
        st.dataframe(result["values"], use_container_width=True)

    # -------------------------------
    # 🩺 HEALTH ANALYSIS TAB
    # -------------------------------
    with tab2:
        st.subheader("📈 Health Risk Meter")

        risk_text = str(result["risks"]).lower()

        if "high" in risk_text:
            risk_level = "High"
            risk_value = 90
            color = "🔴"
        elif "moderate" in risk_text:
            risk_level = "Moderate"
            risk_value = 60
            color = "🟠"
        else:
            risk_level = "Low"
            risk_value = 30
            color = "🟢"

        st.progress(risk_value)
        st.markdown(f"### {color} Risk Level: {risk_level}")

        st.markdown("### 🩺 Detected Conditions")
        st.write(result["conditions"])

        st.markdown("### 📋 Risk Analysis")
        st.write(result["risks"])

    # -------------------------------
    # 🥗 DIET PLAN TAB
    # -------------------------------
    with tab3:
        st.subheader("🥗 7-Day AI Generated Diet Plan")
        st.text_area(
            "Diet Plan",
            value=result["ai_diet"],
            height=400
        )

    # -------------------------------
    # 📊 NUTRITION ANALYTICS TAB
    # -------------------------------
    with tab4:
        st.subheader("📊 Structured Diet Plan Table")
        st.dataframe(result["diet_table"], use_container_width=True)

        pdf_buffer = generate_diet_pdf(
            age=age,
            gender=gender,
            values=result["values"],
            conditions=result["conditions"],
            risks=result["risks"],
            ai_diet=result["ai_diet"]
        )

        st.download_button(
            "⬇️ Download Full AI Diet Report (PDF)",
            data=pdf_buffer,
            file_name="AI_Diet_Report.pdf",
            mime="application/pdf"
        )

# -------------------------------
# Footer
# -------------------------------
st.markdown(
    "<hr><p style='text-align:center;color:gray'>AI NutriCare © 2026 | Powered by AI</p>",
    unsafe_allow_html=True
)

