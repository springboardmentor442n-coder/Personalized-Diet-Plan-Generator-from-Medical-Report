from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from backend.pipeline import run_pipeline  # adjust this import

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_pipeline(temp_path)

    os.remove(temp_path)

    return {
    "patientInfo": {
        "name": result["patient_information"]["name"],
        "age": result["patient_information"]["age"],
        "gender": result["patient_information"]["gender"],
        "labNumber": result["patient_information"]["lab_number"],
        "collectionDate": result["patient_information"]["collection_datetime"],
        "reportDate": result["patient_information"]["report_datetime"],
    },
    "healthScore": result["health_score"],
    "summary": {
        "totalTests": result["total_tests"],
        "normalTests": result["normal_tests"],
        "abnormalTests": result["abnormal_count"],
    },
    "findings": [
        {
            "name": t["test_name"],
            "value": t["value"],
            "unit": t["units"],
            "referenceRange": t["reference_range"],
            "interpretation": t["interpretation"].capitalize(),
            "severity": t["severity"].capitalize(),
        }
        for t in result["tests"]
    ]
}