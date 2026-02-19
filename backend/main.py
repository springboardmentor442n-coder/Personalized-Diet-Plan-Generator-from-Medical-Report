# backend/main.py

from fastapi import FastAPI, UploadFile, File
import tempfile
import uuid

from ocr import process_document
from extraction import extract_lab_values
from analysis import evaluate_health, calculate_risk_score
from diet_generator import generate_llm_diet
from rag_chat import rag_chat
from fastapi import Form
from config import settings

if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set")

app = FastAPI()


@app.get("/")
def root():
    return {"status": "Backend running"}


@app.post("/analyze")
async def analyze_report(file: UploadFile = File(...),
                         age: int = Form(...),
                         gender: str = Form(...),
                         region: str = Form(...)):

    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            content = await file.read()
            tmp.write(content)
            temp_path = tmp.name

        # 1️⃣ OCR
        extracted_text = process_document(temp_path)
        print("----- OCR TEXT START -----")
        print(extracted_text)
        print("----- OCR TEXT END -----")


        # 2️⃣ Extract lab values
        labs = extract_lab_values(extracted_text)

        # 3️⃣ Evaluate health
        health_status = evaluate_health(labs)

        # 4️⃣ Risk score
        risk_score = calculate_risk_score(health_status)

        # 5️⃣ Generate diet
        diet_plan = generate_llm_diet(health_status, region)

        session_id = str(uuid.uuid4())
        rag_chat.add_context(session_id, extracted_text, diet_plan)

        return {
            "session_id": session_id,
            "labs": labs,
            "health_status": health_status,
            "risk_score": risk_score,
            "diet_plan": diet_plan,
            "message": "Analysis completed"
        }

    except Exception as e:
        return {
            "error": str(e),
            "labs": {},
            "health_status": {},
            "risk_score": 0,
            "diet_plan": ""
        }

from pydantic import BaseModel
from rag_chat import rag_chat

class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
async def chat_endpoint(data: ChatRequest):
    try:
        response = rag_chat.chat(
            session_id=data.session_id,
            user_message=data.message
        )
        return {"response": response}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
