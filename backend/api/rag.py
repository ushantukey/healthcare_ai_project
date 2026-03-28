from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

knowledge_base = [
    {
        "keywords": ["fever", "cough"],
        "text": "Possible viral infection or flu. Recommend rest, hydration, and paracetamol."
    },
    {
        "keywords": ["chest pain", "severe", "shortness of breath"],
        "text": "Possible cardiac issue. ECG and immediate consultation required."
    },
    {
        "keywords": ["diabetes"],
        "text": "Monitor blood sugar, take insulin or metformin, maintain diet."
    },
    {
        "keywords": ["headache"],
        "text": "Possible migraine or stress. Suggest rest and hydration."
    }
]


def get_medical_context(summary):
    text = summary.lower()

    contexts = []

    for item in knowledge_base:
        for keyword in item["keywords"]:
            if keyword in text:
                contexts.append(item["text"])
                break

    if not contexts:
        return "General medical advice required."

    return "\n".join(list(set(contexts)))