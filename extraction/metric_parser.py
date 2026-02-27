"""
Health Metric Parser Module
Extracts specific health metrics from OCR text
"""
import re
import json

def parse_blood_sugar(text):
    """Extract blood sugar/glucose levels from text"""
    patterns = [
        r'blood\s+sugar[:\s]+(\d+(?:\.\d+)?)',
        r'glucose[:\s]+(\d+(?:\.\d+)?)',
        r'sugar\s+level[:\s]+(\d+(?:\.\d+)?)',
        r'fasting\s+glucose[:\s]+(\d+(?:\.\d+)?)',
        r'random\s+glucose[:\s]+(\d+(?:\.\d+)?)',
        r'(\d+)\s*mg/dl\s+glucose',
        r'(\d+)\s*mg/dl\s+sugar'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            # Validate reasonable range (50-500 mg/dL)
            if 50 <= value <= 500:
                return str(int(value))
    
    return None

def parse_bmi(text):
    """Extract BMI from text"""
    patterns = [
        r'bmi[:\s]+(\d+(?:\.\d+)?)',
        r'body\s+mass\s+index[:\s]+(\d+(?:\.\d+)?)',
        r'b\.m\.i[:\s]+(\d+(?:\.\d+)?)',
        r'bmi\s*=\s*(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)\s+kg/m2'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            # Validate reasonable BMI range (10-60)
            if 10 <= value <= 60:
                return str(round(value, 1))
    
    return None

def parse_cholesterol(text):
    """Extract cholesterol levels from text"""
    patterns = [
        r'cholesterol[:\s]+(\d+(?:\.\d+)?)',
        r'total\s+cholesterol[:\s]+(\d+(?:\.\d+)?)',
        r'chol[:\s]+(\d+(?:\.\d+)?)',
        r'(\d+)\s*mg/dl\s+cholesterol',
        r'ldl[:\s]+(\d+(?:\.\d+)?)',
        r'hdl[:\s]+(\d+(?:\.\d+)?)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            # Validate reasonable cholesterol range (100-400 mg/dL)
            if 100 <= value <= 400:
                return str(int(value))
    
    return None

def parse_blood_pressure(text):
    """Extract blood pressure from text"""
    patterns = [
        r'blood\s+pressure[:\s]+(\d+/\d+)',
        r'bp[:\s]+(\d+/\d+)',
        r'(\d+)\s*/\s*(\d+)\s*mmhg'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) == 1:
                # Pattern like "120/80"
                bp_values = match.group(1)
                systolic, diastolic = bp_values.split('/')
                systolic, diastolic = int(systolic), int(diastolic)
            else:
                # Pattern like "120 / 80 mmHg"
                systolic, diastolic = int(match.group(1)), int(match.group(2))
            
            # Validate reasonable BP range
            if 80 <= systolic <= 200 and 50 <= diastolic <= 120:
                return f"{systolic}/{diastolic}"
    
    return None

def parse_weight_height(text):
    """Extract weight and height from text"""
    weight = None
    height = None
    
    # Weight patterns
    weight_patterns = [
        r'weight[:\s]+(\d+(?:\.\d+)?)\s*kg',
        r'wt[:\s]+(\d+(?:\.\d+)?)\s*kg',
        r'(\d+(?:\.\d+)?)\s*kg\s+weight'
    ]
    
    for pattern in weight_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            if 20 <= value <= 200:  # Reasonable weight range in kg
                weight = str(round(value, 1))
                break
    
    # Height patterns
    height_patterns = [
        r'height[:\s]+(\d+(?:\.\d+)?)\s*cm',
        r'ht[:\s]+(\d+(?:\.\d+)?)\s*cm',
        r'(\d+(?:\.\d+)?)\s*cm\s+height',
        r'height[:\s]+(\d+)\s*feet?\s*(\d+)\s*inch',
        r'(\d+)\'\s*(\d+)\"'
    ]
    
    for pattern in height_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if 'feet' in pattern or '\'' in pattern:
                # Convert feet/inches to cm
                feet = int(match.group(1))
                inches = int(match.group(2)) if len(match.groups()) > 1 else 0
                height_cm = (feet * 12 + inches) * 2.54
                if 100 <= height_cm <= 250:
                    height = str(round(height_cm, 1))
            else:
                value = float(match.group(1))
                if 100 <= value <= 250:  # Reasonable height range in cm
                    height = str(round(value, 1))
            break
    
    return weight, height

def extract_doctor_notes(text):
    """Extract doctor's notes or observations"""
    notes_patterns = [
        r'notes?[:\s]+(.{20,200})',
        r'observation[s]?[:\s]+(.{20,200})',
        r'impression[:\s]+(.{20,200})',
        r'diagnosis[:\s]+(.{20,200})',
        r'remarks?[:\s]+(.{20,200})'
    ]
    
    notes = []
    for pattern in notes_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            note = match.group(1).strip()
            # Clean up the note
            note = re.sub(r'\s+', ' ', note)
            if len(note) > 15:  # Minimum meaningful length
                notes.append(note[:200])  # Limit length
    
    return notes[:3] if notes else []  # Return max 3 notes

def parse_health_metrics(text):
    """
    Main function to parse all health metrics from extracted text
    Returns a dictionary with all found metrics
    """
    if not text:
        return {}
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    metrics = {}
    
    # Extract individual metrics
    blood_sugar = parse_blood_sugar(text_lower)
    if blood_sugar:
        metrics['blood_sugar'] = blood_sugar
    
    bmi = parse_bmi(text_lower)
    if bmi:
        metrics['bmi'] = bmi
    
    cholesterol = parse_cholesterol(text_lower)
    if cholesterol:
        metrics['cholesterol'] = cholesterol
    
    blood_pressure = parse_blood_pressure(text_lower)
    if blood_pressure:
        metrics['blood_pressure'] = blood_pressure
    
    weight, height = parse_weight_height(text_lower)
    if weight:
        metrics['weight'] = weight
    if height:
        metrics['height'] = height
    
    # Calculate BMI if we have weight and height but no BMI
    if weight and height and not bmi:
        try:
            weight_kg = float(weight)
            height_m = float(height) / 100  # Convert cm to m
            calculated_bmi = weight_kg / (height_m ** 2)
            if 10 <= calculated_bmi <= 60:
                metrics['bmi'] = str(round(calculated_bmi, 1))
                metrics['bmi_calculated'] = True
        except:
            pass
    
    # Extract doctor notes
    notes = extract_doctor_notes(text)
    if notes:
        metrics['doctor_notes'] = notes
    
    return metrics

def validate_metrics(metrics):
    """Validate extracted metrics for reasonableness"""
    validated = {}
    
    # Blood sugar validation
    if 'blood_sugar' in metrics:
        try:
            value = float(metrics['blood_sugar'])
            if 50 <= value <= 500:
                validated['blood_sugar'] = metrics['blood_sugar']
        except:
            pass
    
    # BMI validation
    if 'bmi' in metrics:
        try:
            value = float(metrics['bmi'])
            if 10 <= value <= 60:
                validated['bmi'] = metrics['bmi']
                if metrics.get('bmi_calculated'):
                    validated['bmi_calculated'] = True
        except:
            pass
    
    # Cholesterol validation
    if 'cholesterol' in metrics:
        try:
            value = float(metrics['cholesterol'])
            if 100 <= value <= 400:
                validated['cholesterol'] = metrics['cholesterol']
        except:
            pass
    
    # Blood pressure validation
    if 'blood_pressure' in metrics:
        try:
            systolic, diastolic = metrics['blood_pressure'].split('/')
            sys_val, dia_val = int(systolic), int(diastolic)
            if 80 <= sys_val <= 200 and 50 <= dia_val <= 120:
                validated['blood_pressure'] = metrics['blood_pressure']
        except:
            pass
    
    # Weight and height validation
    if 'weight' in metrics:
        try:
            value = float(metrics['weight'])
            if 20 <= value <= 200:
                validated['weight'] = metrics['weight']
        except:
            pass
    
    if 'height' in metrics:
        try:
            value = float(metrics['height'])
            if 100 <= value <= 250:
                validated['height'] = metrics['height']
        except:
            pass
    
    # Copy doctor notes as-is
    if 'doctor_notes' in metrics:
        validated['doctor_notes'] = metrics['doctor_notes']
    
    return validated