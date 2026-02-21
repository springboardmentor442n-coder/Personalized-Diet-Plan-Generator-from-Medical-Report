import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import pdfplumber
import pytesseract
from PIL import Image
import io
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch


# ---------------- Load API Key ----------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key="")

# ---------------- Tesseract Setup ----------------
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# 
st.set_page_config(page_title="AI Nutrition Planner", layout="wide", page_icon="🥗")

if 'page' not in st.session_state:
    st.session_state.page = "Intro"

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

#  CSS ----------------
st.markdown("""
<style>
/* General body & background */
body {
    background-color: #121212;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Page heading */
h1, h2 {
    text-align: center;
    font-weight: bold;
}
h1 { font-size: 3em; margin-bottom: 0.2em; }
h2 { font-size: 1.5em; margin-bottom: 2em; color: #b3b3b3; }

/* Card container (grid layout like Spotify playlists) */
.card-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5em;
    padding: 1em 3em;
}

/* Card style */
.card {
    background: linear-gradient(145deg, #1db954, #1ed760, #1db954);
    background-size: 200% 200%;
    animation: gradient 5s ease infinite;
    border-radius: 15px;
    padding: 1.5em;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    text-align: center;
}
.card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.card h3 {
    font-size: 1.4em;
    margin-bottom: 0.5em;
}
.card p {
    font-size: 0.95em;
    color: #f0f0f0;
}

/* Gradient animation */
@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Buttons */
.stButton button {
    background-color: #1db954;
    color: white;
    font-weight: bold;
    border-radius: 25px;
    padding: 0.5em 2em;
    transition: transform 0.2s;
}
.stButton button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- Extract Text ----------------
def extract_text(file):
    text = ""
    try:
        if file.type == "application/pdf":
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        else:
            image = Image.open(file)
            text = pytesseract.image_to_string(image)
    except Exception as e:
        st.error(f"Error extracting text: {e}")
    return text

# ---------------- Diet Plan Generator ----------------
def generate_diet_plan(age, weight, height, goal, diet_type, activity,allergy_details="", report_text="", preferred_ingredients=""):
    prompt = f"""
You are a professional clinical nutritionist.

User Details:
Age: {age}
Weight: {weight} kg
Height: {height} cm
Goal: {goal}
Diet Type: {diet_type}
Activity Level: {activity}
Food Allergies:
{allergy_details if allergy_details else "None"}

Medical Report Data:
{report_text}

Create a structured 7-day diet plan including Breakfast, Lunch, Dinner, Snacks, daily calories, and health precautions.
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


def create_pdf(plan_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()

    # Day Style
    day_style = ParagraphStyle(
        'DayStyle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=10,
        textColor=colors.darkgreen
    )

    # Meal Style
    meal_style = ParagraphStyle(
        'MealStyle',
        parent=styles['Heading2'],
        fontSize=13,
        spaceAfter=6,
        textColor=colors.black
    )

    # Health Precaution Style (Highlighted)
    precaution_style = ParagraphStyle(
        'PrecautionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.red
    )

    normal_style = styles["Normal"]

    lines = plan_text.split("\n")

    for line in lines:
        clean_line = line.strip()

        # Day headings
        if re.search(r'Day\s*\d+', clean_line):
            elements.append(Spacer(1, 0.3 * inch))
            elements.append(Paragraph(clean_line.replace("*", ""), day_style))

        # Meals
        elif any(meal in clean_line for meal in ["Breakfast", "Lunch", "Dinner", "Snacks", "Total Calories"]):
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph(clean_line.replace("*", ""), meal_style))

        # Health Precautions (highlighted in red)
        elif "Health Precautions" in clean_line:
            elements.append(Spacer(1, 0.4 * inch))
            elements.append(Paragraph(clean_line.replace("*", ""), precaution_style))

        elif clean_line:
            elements.append(Paragraph(clean_line.replace("*", ""), normal_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def show_chatbot(context_info="", chat_key="chat"):

    st.markdown("### 💬 AI Nutrition Chat")

    if chat_key not in st.session_state:
        st.session_state[chat_key] = []

    for msg in st.session_state[chat_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask your question...")

    if user_input:

        st.session_state[chat_key].append(
            {"role": "user", "content": user_input}
        )

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
You are a certified clinical nutritionist.
Answer only health, diet, fitness related questions.
User context:
{context_info}
""",
                    }
                ] + st.session_state[chat_key],
            )

            reply = response.choices[0].message.content

        except Exception as e:
            reply = f"Error: {e}"

        st.session_state[chat_key].append(
            {"role": "assistant", "content": reply}
        )

        st.rerun()

    if st.button("🗑 Clear Chat", key=f"clear_{chat_key}"):
        st.session_state[chat_key] = []
        st.rerun()

# ---------------- Generate Plan Section ----------------
def show_generate_plan_section(age=None, weight=None, height=None, goal=None, diet_type=None, activity=None, report_text=""):
    if st.button("🚀 Generate AI Diet Plan"):
        with st.spinner("Generating personalized diet plan..."):
            plan = generate_diet_plan(
                age if age else 25,
                weight if weight else 60,
                height if height else 165,
                goal if goal else "Maintain Weight",
                diet_type if diet_type else "Vegetarian",
                activity if activity else "Moderate",
                report_text
            )
            st.success("✅ Your Personalized Plan is Ready!")
            st.write(plan)

            

# ---------------- Intro  Page ----------------
if st.session_state.page == "Intro":
    st.markdown("<h1>🥗 AI Nutrition Planner</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Pick an option to get started</h2>", unsafe_allow_html=True)

    st.markdown("<div class='card-container'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("📝 Enter Details Manually"):
            st.session_state.page = "Home"
        st.markdown("""
        <div class='card'>
            <h3>Enter Your Details</h3>
            <p>Manually input your age, weight, height, goal, diet preference, and activity level.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("📄 Upload Medical Report"):
            st.session_state.page = "Upload"
            
        st.markdown("""
        <div class='card'>
            <h3>Upload Medical Reports</h3>
            <p>Upload your medical reports to generate a personalized diet plan.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- Home Page ----------------
elif st.session_state.page == "Home":

    # Top Right Back Button
    top1, top2 = st.columns([8, 1])

    with top2:
        st.markdown("<div style='text-align:center; font-size:14px;'>🤖 Ask AI Nutritionist</div>", unsafe_allow_html=True)
        if st.button("💬 Open Chat"):
            st.session_state.chat_open = not st.session_state.chat_open
    if st.button("⬅️ Back"):
        st.session_state.page = "Intro"

    st.markdown("<h1 style='text-align:center;'>📝 Enter Your Personal Details</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Two Columns
    col1, col2 = st.columns(2, gap="large")

    with col1:
        age = st.number_input("🎂 Age", 10, 100, 25)
        height = st.number_input("📏 Height (cm)", 100, 250, 165)
        goal = st.selectbox(
            "🎯 Your Goal",
            ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintain Weight"]
        )

    with col2:
        weight = st.number_input("⚖️ Weight (kg)", 30, 200, 60)
        diet_type = st.selectbox(
            "🥗 Diet Preference",
            ["Vegetarian", "Non-Vegetarian", "Both"]
        )
        activity = st.selectbox(
            "🏃 Activity Level",
            ["Low", "Moderate", "High"]
        )

    st.markdown("### 📊 Your Health Overview")

    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal Weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"

    st.info(f"🧮 BMI: {round(bmi, 1)} ({category})")


    # Allergies
    st.markdown("### ⚠️ Food Allergies")

    has_allergy = st.radio(
        "Do you have any food allergies?",
        ["No", "Yes"],
        horizontal=True
    )

    allergy_details = ""
    if has_allergy == "Yes":
        allergy_details = st.text_input(
            "Mention your allergies (e.g., peanuts, dairy, gluten)"
        )


    # Preferred Ingredients
    st.markdown("### 🥦 Preferred Ingredients (Optional)")

    preferred_ingredients = st.text_area(
        "Enter ingredients you would like in your diet plan (comma separated)",
        placeholder="e.g., oats, brown rice, almond milk, eggs, spinach"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Generate Button
    if st.button("🚀 Generate AI Diet Plan", use_container_width=True):
        with st.spinner("Generating personalized diet plan..."):
            plan = generate_diet_plan(
                age,
                weight,
                height,
                goal,
                diet_type,
                activity,
                allergy_details,
                report_text="", preferred_ingredients=""
            )

            st.success("✅ Your Personalized Plan is Ready!")
            st.write(plan)

        
            
        pdf_file = create_pdf(plan)

        st.download_button(
            label="📥 Download Plan as PDF",
            data=pdf_file,
            file_name="AI_Diet_Plan.pdf",
            mime="application/pdf"
        )

    context_home = f"""
Age: {age}
Weight: {weight}
Height: {height}
Goal: {goal}
Diet: {diet_type}
Activity: {activity}
"""

    if st.session_state.chat_open:
        with st.sidebar:
            show_chatbot(context_home, chat_key="home_chat")

 





# ---------------- Upload Page ----------------
elif st.session_state.page == "Upload":

    # Top Right Back Button
    top1, top2 = st.columns([8, 1])
    with top2:
        st.markdown("<div style='text-align:center; font-size:14px;'>🤖 Ask AI Nutritionist</div>", unsafe_allow_html=True)
        if st.button("💬 Open Chat"):
            st.session_state.chat_open = not st.session_state.chat_open
    if st.button("⬅️ Back"):
        st.session_state.page = "Intro"

    st.header("Upload Medical Report")

    st.markdown("<h1>📄 Upload Your Medical Report</h1>", unsafe_allow_html=True)

       
    if "report_text" not in st.session_state:
        st.session_state.report_text = ""

    uploaded_file = st.file_uploader(
        "Upload PDF / Image",
        type=["pdf","png","jpg","jpeg"]
    )

    if uploaded_file:
        with st.spinner("Extracting text from report..."):
            st.session_state.report_text = extract_text(uploaded_file)

    # Show extracted text
    if st.session_state.report_text:
        st.text_area(
            "Extracted Text",
            st.session_state.report_text,
            height=300
        )

    context_upload = f"""
Medical Report:
{st.session_state.report_text if st.session_state.report_text else "No report uploaded yet."}
"""

   
    if st.session_state.chat_open:
        with st.sidebar:
            show_chatbot(context_upload, chat_key="upload_chat")

    # ---------------- Allergies ----------------
    st.markdown("### ⚠️ Food Allergies")

    has_allergy = st.radio(
        "Do you have any food allergies?",
        ["No", "Yes"],
        horizontal=True,
        key="upload_allergy_radio"
    )

    allergy_details = ""
    if has_allergy == "Yes":
        allergy_details = st.text_input(
            "Mention your allergies",
            key="upload_allergy_input"
        )

    # ---------------- Diet Type ----------------
    st.markdown("### 🥗 Diet Preference")

    upload_diet_type = st.selectbox(
        "Select Diet Type",
        ["Vegetarian", "Non-Vegetarian", "Both"],
        key="upload_diet_type"
    )

    # ---------------- Generate Plan ----------------
    if st.button("🚀 Generate AI Diet Plan", use_container_width=True):

        with st.spinner("Generating personalized diet plan..."):

            plan = generate_diet_plan(
                age=None,
                weight=None,
                height=None,
                goal="Based on Medical Report",
                diet_type=upload_diet_type,
                activity=None,
                allergy_details=allergy_details,
                report_text=st.session_state.report_text
            )
            st.success("✅ Your Personalized Plan is Ready!")
            st.write(plan)

            pdf_file = create_pdf(plan)

            st.download_button(
                label="📥 Download Plan as PDF",
                data=pdf_file,
                file_name="AI_Diet_Plan.pdf",
                mime="application/pdf"
            )
