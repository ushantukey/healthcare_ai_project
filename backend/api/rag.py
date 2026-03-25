def get_medical_context(summary):
    knowledge_base = [
        {
            "keywords": ["fever", "cough"],
            "context": "Possible respiratory infection like flu or COVID-19."
        },
        {
            "keywords": ["chest pain", "breath"],
            "context": "May indicate heart disease or lung condition."
        },
        {
            "keywords": ["headache", "vomiting"],
            "context": "Possible migraine or neurological issue."
        },
        {
            "keywords": ["fatigue", "weakness"],
            "context": "May be due to anemia or chronic illness."
        }
    ]

    matched_contexts = []

    for item in knowledge_base:
        for keyword in item["keywords"]:
            if keyword.lower() in summary.lower():
                matched_contexts.append(item["context"])

    return " ".join(matched_contexts)