import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse


def test_api(request):
    return JsonResponse({"message": "API is working!"})
@api_view(['POST'])
def analyze_patient(request):
    summary = request.data.get('summary')

    if not summary:
        return Response({"error": "No summary provided"}, status=400)

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        prompt = f"""
        You are a medical AI assistant.

        Analyze the patient summary and give:

        1. Diagnosis
        2. Treatment Plan

        Patient Summary:
        {summary}
        """

        data = {
            "model": "openai/gpt-3.5-turbo",  # ✅ WORKING MODEL
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code != 200:
            return Response({
                "error": "API Error",
                "details": response.text
            }, status=500)

        result = response.json()

        # ✅ SAFE EXTRACTION
        ai_output = result.get('choices', [{}])[0].get('message', {}).get('content', 'No AI response')

        return Response({
            "summary": summary,
            "ai_response": ai_output
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)