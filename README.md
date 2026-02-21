🧠 AI Nutricare

AI Nutricare is a full-stack AI-powered medical lab report analyzer that extracts, interprets, and visualizes structured health insights from uploaded PDF lab reports.

It combines backend medical rule-engine logic with a modern SaaS-style frontend dashboard.

🚀 Features

📄 Upload medical lab report (PDF)

🧠 Automatic lab test extraction

📊 Low / Normal / High classification

🚨 Severity detection (Mild / Moderate / Critical)

❤️ Health score calculation

📈 Abnormal findings summary

🌗 Light / Dark theme support

⚡ Fast API-powered backend

🏗 Architecture
User Upload
     ↓
React Frontend
     ↓
FastAPI Backend
     ↓
PDF Reader
     ↓
Extraction Engine
     ↓
Analyzer (Rule Engine)
     ↓
Structured JSON
     ↓
Dashboard Rendering
🧩 Tech Stack
Backend

FastAPI

Python 3.10+

pdfplumber

Pydantic

Frontend

React 19

TypeScript

Tailwind CSS

Vite

Framer Motion

📁 Project Structure
ai-nutricare/
│
├── backend/
│   ├── analyzer.py
│   ├── extraction.py
│   ├── pdf_reader.py
│   ├── pipeline.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
├── .gitignore
└── README.md
🔧 Installation
1️⃣ Clone Repository
git clone https://github.com/YOUR_USERNAME/ai-nutricare.git
cd ai-nutricare
🖥 Backend Setup
cd backend
python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn main:app --reload

Backend runs at:

http://localhost:8000
🌐 Frontend Setup
cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:3000
📡 API Endpoint
POST /analyze/

Accepts:

Multipart file upload (PDF)

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

This project is for educational and informational purposes only.
It does not replace professional medical advice.

🎯 Current Status

✅ MVP Complete
🔄 Ready for feature expansion:

Authentication

Report history storage

Dockerization

Deployment

Trend tracking

Recommendation engine