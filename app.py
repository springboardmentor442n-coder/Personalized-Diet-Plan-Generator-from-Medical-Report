import streamlit as st
import json
import os
import pandas as pd
from io import StringIO

from pdf_reader import extract_medical_data
from health_analyser import analyze_health
from ai_diet_generator import generate_plan

st.set_page_config(page_title="AI NutriCare", layout="wide")

st.title("AI NutriCare - Personalized Diet Planner")

# ---------------- USER DETAILS ----------------
st.sidebar.header("User Details")

height = st.sidebar.number_input("Height (cm)", 140, 220, 170)
weight = st.sidebar.number_input("Weight (kg)", 40, 150, 60)
age = st.sidebar.number_input("Age", 10, 100, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
st.sidebar.subheader("Diet Preferences")

diet_type = st.sidebar.selectbox(
    "Diet Type",
    ["Vegetarian", "Non-Vegetarian", "Eggetarian"]
)

budget = st.sidebar.selectbox(
    "Budget",
    ["Low", "Medium", "High"]
)

goal = st.sidebar.selectbox(
    "Goal",
    ["Weight Loss", "Maintain", "Weight Gain"]
)

# ---------------- BMI ----------------
bmi = weight / ((height / 100) ** 2)

if bmi < 18.5:
    bmi_status = "Underweight"
elif bmi < 25:
    bmi_status = "Normal"
elif bmi < 30:
    bmi_status = "Overweight"
else:
    bmi_status = "Obese"

st.metric("BMI", round(bmi, 2), bmi_status)

# ---------------- FILE UPLOAD ----------------
st.subheader("Upload Medical Report PDF")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

health = None

if uploaded_file is not None:

    # Save uploaded PDF
    file_path = "data/report.pdf"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded Successfully")

    # ---------------- EXTRACTION ----------------
    raw_data = extract_medical_data(file_path)

    # Save raw data
    with open("outputs/report_data.json", "w") as f:
        json.dump(raw_data, f, indent=4)

    # ---------------- ANALYSIS ----------------
    health = analyze_health(raw_data)

    with open("outputs/analysis.json", "w") as f:
        json.dump(health, f, indent=4)

# ---------------- DASHBOARD ----------------
if health:

    st.subheader("Health Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Diabetes Risk", health.get("diabetes", "N/A"))
    col2.metric("Cholesterol", health.get("cholesterol", "N/A"))
    col3.metric("Vitamin D", health.get("vitamin_d", "N/A"))

    # ---------------- ALERTS ----------------
    st.subheader("Health Alerts")

    if health.get("vitamin_d") == "Deficient":
        st.warning("Vitamin D Deficiency")

    if health.get("hemoglobin") == "Low (Anemia Risk)":
        st.warning("Possible Anemia")

    if health.get("thyroid") == "Hypothyroid":
        st.warning("Thyroid Risk")

    # ---------------- DIET PLAN ----------------
    st.subheader("Personalized Diet Plan")

    user_profile = {
    "age": age,
    "gender": gender,
    "diet_type": diet_type,
    "budget": budget,
    "goal": goal
    }

    plan = generate_plan(user_profile)

    try:
        df = pd.read_csv(StringIO(plan))
        st.table(df)
    except:
        st.text("Table formatting failed, showing raw data:")
        st.text(plan)

    st.download_button(
        label="Download Diet Plan",
        data=plan,
        file_name="diet_plan.txt"
    )

else:
    st.info("Upload a medical report to see health analysis and diet plan.")

