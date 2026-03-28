# api/bert.py

def classify_disease(summary):
    text = summary.lower()

    
    if "chest pain" in text and ("shortness of breath" in text or "severe" in text):
        return "Cardiovascular Disease"

    if "fever" in text and "cough" in text:
        return "Respiratory Infection"

    if "headache" in text:
        return "Neurological Disorder"

    if "diabetes" in text:
        return "Metabolic Disorder"

    return "General Condition"