# api/views.py

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse

from .rag import get_medical_context
from .graph_rag import build_graph
from .bert import classify_disease


def test_api(request):
    return JsonResponse({"message": "API is working!"})


@api_view(['POST'])
def analyze_patient(request):
    summary = request.data.get('summary')

    if not summary:
        return Response({"error": "No summary provided"}, status=400)

    try:
        # ✅ RAG
        context = get_medical_context(summary)

        # ✅ GraphRAG
        graph_data = build_graph(summary)

        # ✅ BERT (SMART SIMULATION)
        disease_prediction = classify_disease(summary)

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        # ✅ FINAL PROMPT (ALL COMPONENTS)
        prompt = f"""
        You are a medical AI assistant.

        BERT Prediction:
        Likely Disease Category: {disease_prediction}

        Graph Analysis:
        Symptoms: {graph_data.get('symptoms')}
        Possible Diseases: {graph_data.get('possible_diseases')}

        Medical Context:
        {context}

        Analyze the patient summary and provide:

        1. Final Diagnosis
        2. Treatment Plan (clear steps)

        Patient Summary:
        {summary}
        """

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return Response({
                "error": "API Error",
                "details": response.text
            }, status=500)

        result = response.json()

        ai_output = result.get('choices', [{}])[0].get('message', {}).get('content', 'No AI response')

        return Response({
            "summary": summary,
            "bert_prediction": disease_prediction,
            "graph_data": graph_data,
            "rag_context": context,
            "ai_response": ai_output
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)