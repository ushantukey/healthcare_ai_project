def build_graph(summary):
    graph = {
        "fever": ["infection", "flu"],
        "cough": ["respiratory infection"],
        "chest pain": ["heart disease"],
        "headache": ["migraine"],
        "fatigue": ["anemia"]
    }

    detected = []
    related = []

    for symptom, diseases in graph.items():
        if symptom in summary.lower():
            detected.append(symptom)
            related.extend(diseases)

    return {
        "symptoms": detected,
        "possible_diseases": list(set(related))
    }