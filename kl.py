import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import pdfplumber
import pytesseract
from PIL import Image

# ---------------- Load API Key ----------------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API Key not found. Please set GROQ_API_KEY in environment variables.")
    st.stop()

client = Groq(api_key=api_key)


# ---------------- Tesseract Path (Windows Only) ----------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="AI Diet Planner", layout="centered")
st.title("🥗 AI-Based Personalized Diet Plan Generator")

st.write("Enter your details and/or upload your medical report")

# ---------------- User Inputs ----------------
age = st.number_input("Age", min_value=10, max_value=100)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200)
height = st.number_input("Height (cm)", min_value=100, max_value=250)

goal = st.selectbox(
    "Your Goal",
    ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintain Weight"]
)

diet_type = st.selectbox(
    "Diet Preference",
    ["Vegetarian", "Non-Vegetarian"]
)

activity = st.selectbox(
    "Activity Level",
    ["Low", "Moderate", "High"]
)

# ---------------- File Upload ----------------
uploaded_file = st.file_uploader(
    "Upload Medical Report (PDF / Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

# ---------------- Extract Text Function ----------------
def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    else:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)

    return text

# ---------------- AI Generator ----------------
def generate_diet_plan(report_text):

    prompt = f"""
    You are a professional clinical nutritionist.

    User Details:
    Age: {age}
    Weight: {weight} kg
    Height: {height} cm
    Goal: {goal}
    Diet Type: {diet_type}
    Activity Level: {activity}

    Medical Report Data:
    {report_text}

    Based on the above information:
    - Analyze health conditions
    - Identify risks
    - Create a personalized 7-day diet plan
    - Include Breakfast, Lunch, Dinner, Snacks
    - Mention daily calories
    - Provide important health precautions

    Make it structured and easy to read.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert medical diet planner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


# ---------------- Generate Button ----------------
if st.button("Generate AI Diet Plan"):

    report_text = ""

    if uploaded_file:
        with st.spinner("Extracting text from report..."):
            report_text = extract_text(uploaded_file)
            st.subheader("📄 Extracted Report Text")
            st.text(report_text)

    with st.spinner("Generating personalized diet plan..."):
        plan = generate_diet_plan(report_text)
        st.subheader("📋 Your AI Generated Diet Plan")
        st.write(plan)
