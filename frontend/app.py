import streamlit as st
import requests
import io

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

# ---------------- CONFIG ----------------
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI NutriCare",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE INIT ----------------
defaults = {
    "labs": {},
    "health_status": {},
    "risk_score": 0,
    "diet_plan": "",
    "session_id": "",
    "chat_history": [],
    "active_tab": "Dashboard"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- DARK + GREEN THEME ----------------
st.markdown("""
<style>
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    padding-top: 1rem;
}

.stApp {
    background: linear-gradient(to right, #0f172a, #020617);
    color: #ffffff;
}

[data-testid="stSidebar"] {
    background-color: #0b1220;
    color: white;
}

h1, h2, h3, h4 {
    color: #ffffff !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(34,197,94,0.4);
}

[data-testid="stFileUploader"] button {
    background: linear-gradient(90deg, #16a34a, #15803d) !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #0f2e1f, #092016);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(34,197,94,0.4);
    box-shadow: 0 0 15px rgba(34,197,94,0.2);
}

[data-testid="stMetricLabel"] {
    color: #a7f3d0 !important;
    font-size: 14px !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stSelectbox div {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 8px !important;
}

textarea {
    background-color: #1f2937 !important;
    color: white !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #16a34a, #15803d);
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
}

.stDownloadButton>button {
    background: linear-gradient(90deg, #16a34a, #15803d);
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

st.title("🩺 AI NutriCare - Clinical AI Platform")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📋 Patient Details")

    uploaded_file = st.file_uploader(
        "Upload Medical Report",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    age = st.number_input("Age", 1, 120, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    region = st.selectbox("Region", ["Indian", "Mediterranean", "Western"])

    st.markdown("---")
    st.subheader("⚖️ BMI Calculator")

    height = st.number_input("Height (cm)", 100, 250, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 70)

    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Normal"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    st.metric("BMI", f"{bmi:.2f} ({bmi_status})")

    st.markdown("---")

    analyze_btn = st.button("🚀 Analyze Report")

# ---------------- ANALYZE ----------------
if analyze_btn and uploaded_file:
    with st.spinner("Processing report..."):
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            files={"file": (uploaded_file.name, uploaded_file.getvalue())},
            data={"age": age, "gender": gender, "region": region}
        )

        result = response.json()

        st.session_state.labs = result.get("labs", {})
        st.session_state.health_status = result.get("health_status", {})
        st.session_state.risk_score = result.get("risk_score", 0)
        st.session_state.diet_plan = result.get("diet_plan", "")
        st.session_state.session_id = result.get("session_id", "")
        st.session_state.chat_history = []
        st.session_state.active_tab = "Dashboard"

    st.success("Analysis Completed!")

# ---------------- MAIN CONTENT ----------------
if st.session_state.session_id:

    tabs = ["Dashboard", "Diet Plan", "AI Chat", "Final Report"]

    selected_tab = st.radio(
        "",
        tabs,
        horizontal=True,
        index=tabs.index(st.session_state.active_tab)
    )

    st.session_state.active_tab = selected_tab

    # -------- DASHBOARD --------
    if selected_tab == "Dashboard":
        st.header("📊 Health Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🧪 Lab Summary")
            for k, v in st.session_state.labs.items():
                st.metric(k, v)

        with col2:
            st.subheader("📈 Health Status")
            for k, v in st.session_state.health_status.items():
                st.write(f"**{k}:** {v}")

        with col3:
            st.subheader("❤️ Overall Health")
            st.metric("Risk Score", f"{st.session_state.risk_score}/100")
            st.metric("BMI", f"{bmi:.2f} ({bmi_status})")

    # -------- DIET --------
    if selected_tab == "Diet Plan":
        st.header("🥗 7-Day Personalized Diet Plan")
        st.markdown(st.session_state.diet_plan)

    # -------- CHAT --------
    if selected_tab == "AI Chat":
        st.header("💬 AI Health Assistant")

        user_input = st.text_input("Ask a question")

        if st.button("Ask") and user_input:
            st.session_state.active_tab = "AI Chat"

            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={
                    "session_id": st.session_state.session_id,
                    "message": user_input
                }
            )

            reply = response.json().get("response", "No response")

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", reply))

        for role, msg in reversed(st.session_state.chat_history):
            st.write(f"**{role}:** {msg}")

    # -------- FINAL REPORT --------
    if selected_tab == "Final Report":
        st.header("📄 Final Health Report")

        summary_text = f"""
Age: {age}
Gender: {gender}
Region: {region}
BMI: {bmi:.2f} ({bmi_status})
Risk Score: {st.session_state.risk_score}/100
"""

        st.text_area("Summary Preview", summary_text, height=200)
        st.text_area("Diet Plan Preview", st.session_state.diet_plan, height=300)

        def generate_pdf(summary, diet):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()

            elements.append(Paragraph("AI NutriCare - Health Report", styles["Heading1"]))
            elements.append(Spacer(1, 0.3 * inch))

            for line in summary.split("\n"):
                elements.append(Paragraph(line, styles["Normal"]))
                elements.append(Spacer(1, 0.1 * inch))

            elements.append(PageBreak())

            for line in diet.split("\n"):
                elements.append(Paragraph(line, styles["Normal"]))
                elements.append(Spacer(1, 0.1 * inch))

            doc.build(elements)
            buffer.seek(0)
            return buffer

        pdf = generate_pdf(summary_text, st.session_state.diet_plan)

        st.download_button(
            "📥 Download Report",
            pdf,
            "AI_NutriCare_Report.pdf",
            "application/pdf"
        )
