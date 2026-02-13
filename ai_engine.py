import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use a valid model
model = genai.GenerativeModel("gemini-1.5-flash")

print("Asking the AI for your plan... please wait...")

response = model.generate_content("Give me a 1-day meal plan for 2500 calories.")

print(response.text)
