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
# Custom CSS for better UI
# -------------------------------
st.markdown(
    """
    <style>
    /* Body background */
    .main {
        background-color: #f5f7fa;
    }
    /* Card style for sections */
    .stCard {
        border-radius: 12px;
        padding: 20px;
        background-color: #ffffff;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    /* Button color */
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        height: 45px;
        width: 100%;
        border-radius: 8px;
    }
    div.stButton > button:hover {
        background-color: #45a049;
        color: white;
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
uploaded_file = st.sidebar.file_uploader("Upload Medical Report (PDF)", type=["pdf"])

# -------------------------------
# Main UI
# -------------------------------
st.title("🥗 AI-Based Personalized Diet Plan Generator")
st.markdown("Welcome! Upload a medical report and get a personalized 7-day diet plan with AI.")

if uploaded_file and st.button("Analyze Report"):

    with st.spinner("🔍 Analyzing your medical report..."):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        result = analyze_report(
            "temp.pdf", age, gender, weight, food_type
        )

    # -------------------------------
    # Lab Values Section
    # -------------------------------
    st.subheader("🧪 Extracted Lab Values")
    st.dataframe(result["values"])

    # -------------------------------
    # Conditions Section
    # -------------------------------
    st.subheader("🩺 Detected Conditions / Risks")
    st.write(result["conditions"])
    st.write(result["risks"])

    # -------------------------------
    # AI Diet Plan Section
    # -------------------------------
    st.subheader("🥗 7-Day Diet Plan")
    st.text_area("AI Generated Diet Plan", value=result["ai_diet"], height=300)

    # -------------------------------
    # Diet Table Section
    # -------------------------------
    st.subheader("📊 Diet Plan Table")
    st.dataframe(result["diet_table"])

    # -------------------------------
    # Download PDF
    # -------------------------------
    pdf_buffer = generate_diet_pdf(
        age=age,
        gender=gender,
        values=result["values"],
        conditions=result["conditions"],
        risks=result["risks"],
        ai_diet=result["ai_diet"]
    )

    st.download_button(
        "⬇️ Download PDF Report",
        data=pdf_buffer,
        file_name="AI_Diet_Report.pdf",
        mime="application/pdf"
    )

st.markdown(
    "<hr><p style='text-align:center;color:gray'>AI NutriCare © 2026</p>",
    unsafe_allow_html=True
)
