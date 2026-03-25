def classify_disease(summary):
    summary = summary.lower()

    if "fever" in summary and "cough" in summary:
        return "Respiratory Infection"

    if "chest pain" in summary:
        return "Cardiovascular Issue"

    if "headache" in summary:
        return "Neurological Condition"

    if "fatigue" in summary:
        return "Chronic Condition / Anemia"

    return "General Illness"