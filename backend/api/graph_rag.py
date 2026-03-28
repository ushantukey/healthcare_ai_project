# api/graph_rag.py

def build_graph(summary):
    text = summary.lower()

    symptoms = []
    diseases = []

    if "fever" in text:
        symptoms.append("Fever")
        diseases.append("Viral Infection")

    if "cough" in text:
        symptoms.append("Cough")
        diseases.append("Flu")

    # ✅ FIX: chest pain alone ≠ heart disease
    if "chest pain" in text:
        symptoms.append("Chest Pain")

        if "shortness of breath" in text or "severe" in text:
            diseases.append("Heart Disease")  # only if serious indicators
        else:
            diseases.append("Respiratory Infection")

    if "headache" in text:
        symptoms.append("Headache")
        diseases.append("Migraine")

    return {
        "symptoms": list(set(symptoms)),
        "possible_diseases": list(set(diseases))
    }