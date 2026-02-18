# 🥗 AI NutriCare

AI-based Personalized Diet Plan Generator from Medical Reports.

## Features
- Upload medical reports (PDF / Image / TXT)
- Automatic condition detection
- 7-day personalized diet plan
- Day-wise PDF download
- Clean medical dashboard UI

## Tech Stack
- Python
- Streamlit
- Groq LLM
- OCR (PyMuPDF)
- ReportLab (PDF export)

## How to Run
```backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```frontend
cd frontend
streamlit run app.py


## Project Structure

Personalized-Diet-Plan-Generator-from-Medical-Report/

│
├── backend/
│   ├── app.py
│   ├── analysis.py
│   ├── ocr.py
│   └── ...
│
├── frontend/
│   └── app.py
│
├── README.md
└── requirements.txt
