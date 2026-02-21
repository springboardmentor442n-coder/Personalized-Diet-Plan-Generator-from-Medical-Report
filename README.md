# 🧠 AI Nutricare

AI Nutricare is a full-stack AI-powered medical lab report analyzer that extracts, interprets, and visualizes structured health insights from uploaded PDF lab reports.

This project demonstrates backend rule-based medical analysis combined with a modern SaaS-style frontend dashboard.

---

## 🚀 Features

- Upload medical lab report (PDF)
- Automatic lab test extraction
- Low / Normal / High classification
- Severity detection (Mild / Moderate / Critical)
- Health score calculation
- Abnormal findings summary
- Modern responsive dashboard
- Light / Dark theme support

---

## 🏗 System Architecture
User Upload
↓
React Frontend (File Upload)
↓
FastAPI Backend (/analyze/)
↓
PDF Reader
↓
Extraction Module
↓
Analyzer (Rule Engine)
↓
Structured JSON Response
↓
Dashboard Visualization

---

## 🧩 Tech Stack

### Backend

- Python 3.10+
- FastAPI
- pdfplumber
- Pydantic

### Frontend

- React 19
- TypeScript
- Tailwind CSS
- Vite
- Framer Motion

---

## 📁 Project Structure
backend/ → API + analysis engine
frontend/ → UI dashboard

---

## 🔧 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone <repository-url>
cd ai-nutricare
```

🖥 Backend Setup
```bash
cd backend
python -m venv venv
```
Activate:

Windows
```bash
venv\Scripts\activate
```
Mac/Linux
```bash
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run server:
```bash
uvicorn main:app --reload
```
Backend runs at:

http://localhost:8000

🌐 Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

http://localhost:3000

📡 API Endpoint
POST /analyze/

Accepts:

Multipart PDF file upload

Returns:

{
  "patientInfo": {},
  "healthScore": 63,
  "summary": {
    "totalTests": 55,
    "normalTests": 47,
    "abnormalTests": 8
  },
  "findings": []
}

⚠ Disclaimer

This project is for educational and demonstration purposes only.
It does not replace professional medical advice.

📌 Project Status

MVP Completed.

Ready for further enhancements such as:

-User authentication

-Report history storage

-Trend analysis

-Deployment

---

### ✅ What This Fixes

- Proper headings
- Proper bullet points
- Proper code blocks
- Proper JSON formatting
- Clean section separation
- Professional evaluation-ready layout

Now when you switch to **Preview**, everything will render correctly.

This version is internship-review safe 💼✨

If you want, I can also help you add a clean “Engineering Decisions” section — that impresses evaluators a lot.
