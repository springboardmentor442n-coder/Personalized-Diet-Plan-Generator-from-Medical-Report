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
    layout="wide"
)

st.title("🩺 AI NutriCare - Clinical AI Platform")

# ---------------- SESSION STATE INIT ----------------
defaults = {
    "labs": {},
    "health_status": {},
    "risk_score": 0,
    "diet_plan": "",
    "session_id": "",
    "chat_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📋 Patient Details")

    uploaded_file = st.file_uploader(
        "Upload Medical Report (PDF or Image)",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    age = st.number_input("Age", 1, 120, 30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    region = st.selectbox("Region", ["Indian", "Mediterranean", "Western"])

    analyze_btn = st.button("🚀 Analyze Report")

# ---------------- ANALYZE ----------------
if analyze_btn and uploaded_file:

    with st.spinner("Processing report with AI..."):

        response = requests.post(
            f"{API_BASE_URL}/analyze",
            files={"file": (uploaded_file.name, uploaded_file.getvalue())},
            data={"age": age,
                  "gender": gender,
                  "region": region
                  } 
        )

        if response.status_code != 200:
            st.error(f"Server Error: {response.text}")
            st.stop()

        try:
            result = response.json()
        except Exception:
            st.error("Invalid response from backend.")
            st.write(response.text)
            st.stop()

        if "error" in result:
            st.error(f"Backend Error: {result['error']}")
            st.stop()

        # Normal success
        st.session_state.labs = result.get("labs", {})
        st.session_state.health_status = result.get("health_status", {})
        st.session_state.risk_score = result.get("risk_score", 0)
        st.session_state.diet_plan = result.get("diet_plan", "")
        st.session_state.session_id = result.get("session_id", "")

    st.success("✅ Analysis Completed!")


elif analyze_btn and not uploaded_file:
    st.warning("⚠️ Please upload a report first.")

# ---------------- PDF GENERATOR ----------------
def generate_pdf(summary_text, diet_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("AI NutriCare - Final Health Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Patient Summary", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    for line in summary_text.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(PageBreak())

    elements.append(Paragraph("7-Day Personalized Diet Plan", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    for line in diet_text.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ---------------- MAIN TABS ----------------
if st.session_state.labs:

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard",
        "🥗 Diet Plan",
        "💬 AI Chat",
        "📄 Final Report"
    ])

    # =====================================================
    # DASHBOARD TAB
    # =====================================================
    with tab1:
        st.header("📊 Health Dashboard")

        col1, col2, col3 = st.columns(3)
        score = st.session_state.risk_score

        # LAB SUMMARY
        with col1:
            st.subheader("🧪 Lab Summary")
            for k, v in st.session_state.labs.items():
                st.metric(label=k, value=v)

        # HEALTH STATUS
        with col2:
            st.subheader("📈 Health Status")

            for k, v in st.session_state.health_status.items():
                if v in ["High", "Diabetic", "Kidney Risk"]:
                    color = "red"
                elif v in ["Prediabetic", "Borderline", "Insufficient"]:
                    color = "orange"
                elif v == "Deficient":
                    color = "blue"
                else:
                    color = "green"


                st.markdown(
                    f"<span style='color:{color}; font-weight:bold;'>{k}: {v}</span>",
                    unsafe_allow_html=True
                )

        # RISK SCORE
        with col3:
            st.subheader("❤️ Overall Risk")

            if score < 30:
                level = "Low Risk"
                color = "green"
            elif score < 60:
                level = "Moderate Risk"
                color = "orange"
            else:
                level = "High Risk"
                color = "red"

            st.metric("Risk Score", f"{score}/100")
            st.markdown(
                f"<span style='color:{color}; font-weight:bold;'>{level}</span>",
                unsafe_allow_html=True
            )

        if score >= 70:
            st.error("⚠️ Immediate medical consultation recommended.")
        elif score >= 40:
            st.warning("⚠️ Lifestyle modifications strongly advised.")

        # BMI SECTION
        st.divider()
        st.header("⚖️ Body Mass Index (BMI)")

        bmi_value = None

        if "BMI" in st.session_state.labs:
            bmi_value = st.session_state.labs["BMI"]
            st.info(f"BMI detected from report: {bmi_value}")
        else:
            weight = st.number_input("Enter Weight (kg)", min_value=1.0)
            height = st.number_input("Enter Height (cm)", min_value=1.0)

            if weight and height:
                bmi_value = round(weight / ((height / 100) ** 2), 2)

        if bmi_value:
            if bmi_value < 18.5:
                bmi_status = "Underweight"
                bmi_color = "blue"
            elif bmi_value < 25:
                bmi_status = "Normal"
                bmi_color = "green"
            elif bmi_value < 30:
                bmi_status = "Overweight"
                bmi_color = "orange"
            else:
                bmi_status = "Obese"
                bmi_color = "red"

            st.metric("BMI", bmi_value)
            st.markdown(
                f"<span style='color:{bmi_color}; font-weight:bold;'>{bmi_status}</span>",
                unsafe_allow_html=True
            )

    # =====================================================
    # DIET TAB
    # =====================================================
    with tab2:
        st.header("🥗 7-Day Personalized Diet Plan")

        if st.session_state.diet_plan:
            formatted = st.session_state.diet_plan.replace("**", "")
            for line in formatted.split("\n"):
                if not line.strip():
                    st.write("")
                elif ":" in line and len(line) < 40:
                    st.markdown(f"### {line}")
                else:
                    st.markdown(line)

    # =====================================================
    # CHAT TAB
    # =====================================================
    with tab3:
        st.header("💬 AI Health Assistant")

        user_input = st.text_input("Ask a question about your report:")

        if st.button("Ask") and user_input:
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={
                    "session_id": st.session_state.session_id,
                    "message": user_input
                }
            )
            reply = response.json()["response"]

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", reply))

        for role, msg in reversed(st.session_state.chat_history):
            if role == "You":
                st.markdown(
                    f"<div style='background:#1E293B;padding:10px;border-radius:8px;margin-bottom:5px;color:white;'><b>You:</b> {msg}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                     f"<div style='background:#111827;padding:10px;border-radius:8px;margin-bottom:10px;color:white;'><b>AI:</b> {msg}</div>",
                    unsafe_allow_html=True
                )

    # =====================================================
    # FINAL REPORT TAB
    # =====================================================
    with tab4:
        st.header("📄 Final Health Report")

        summary_text = f"""
Age: {age}
Gender: {gender}
Region: {region}

Risk Score: {st.session_state.risk_score}/100

Health Status:
{st.session_state.health_status}

Lab Values:
{st.session_state.labs}
"""

        st.text_area("Summary Preview", summary_text, height=200)

        st.divider()
        st.subheader("Diet Plan Preview")
        st.text_area("Diet", st.session_state.diet_plan, height=300)

        pdf_buffer = generate_pdf(summary_text, st.session_state.diet_plan)

        st.download_button(
            label="📥 Download Complete Report (PDF)",
            data=pdf_buffer,
            file_name="AI_NutriCare_Report.pdf",
            mime="application/pdf"
        )
