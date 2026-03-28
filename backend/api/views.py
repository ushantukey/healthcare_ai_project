from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import json

from .models import PatientAnalysis
from .rag import get_medical_context
from .graph_rag import build_graph
from .bert import classify_disease


# ------------------ TEST API ------------------
def test_api(request):
    return JsonResponse({"message": "API is working!"})


# ------------------ ENHANCED LLM ------------------
def generate_llm_response(summary, context, graph_data, disease_prediction):

    prompt = f"""
    You are an advanced medical AI.

    STRICTLY return ONLY valid JSON:

    {{
        "diagnosis": "",
        "reasoning": "",
        "confidence": "",
        "risk_level": "",
        "symptoms": [],
        "treatment": [],
        "doctor_advice": [],
        "tests": [],
        "emergency": []
    }}

    Patient Summary: {summary}
    Context: {context}
    Graph Data: {graph_data}
    Prediction: {disease_prediction}
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )

        data = response.json()
        text = data.get("response", "").strip()

        try:
            parsed = json.loads(text)

            return {
                "diagnosis": parsed.get("diagnosis", disease_prediction),
                "reasoning": parsed.get("reasoning", ""),
                "confidence": parsed.get("confidence", "80%"),
                "risk_level": parsed.get("risk_level", "Medium"),
                "symptoms": parsed.get("symptoms", []),
                "treatment": parsed.get("treatment", []),
                "doctor_advice": parsed.get("doctor_advice", []),
                "tests": parsed.get("tests", []),
                "emergency": parsed.get("emergency", [])
            }
        except:
            return None

    except:
        return None


# ------------------ RULE-BASED FALLBACK ------------------
def generate_rule_based_response(summary, context, graph_data, disease_prediction):

    text = summary.lower()
    symptoms = graph_data.get("symptoms", [])

    tests = set()
    treatment = set()
    advice = set()
    emergency = set()

    if any(x in text for x in ["chest pain", "heart", "cardiac"]):
        tests.update(["ECG", "Troponin test", "Chest X-ray"])
        treatment.update(["Aspirin (if prescribed)", "Oxygen support", "Immediate hospitalization"])
        advice.update(["Consult cardiologist immediately", "Avoid physical activity"])
        emergency.add("Heart attack risk – go to hospital immediately")

    if any(x in text for x in ["diabetes", "sugar"]):
        tests.update(["Blood glucose test", "HbA1c"])
        treatment.update(["Insulin / Metformin", "Low sugar diet", "Regular monitoring"])
        advice.update(["Maintain diet", "Check sugar daily", "Visit endocrinologist"])

    if "headache" in text:
        tests.update(["Neurological exam", "CT scan (if severe)"])
        treatment.update(["Pain relievers", "Rest"])
        advice.update(["Sleep properly", "Consult doctor if persistent"])

    if any(x in text for x in ["cough", "fever"]):
        tests.update(["CBC", "Chest X-ray"])
        treatment.update(["Paracetamol", "Hydration"])
        advice.update(["Take rest", "Monitor temperature"])

    if any(x in text for x in ["breathing", "shortness"]):
        emergency.add("Severe breathing issue – urgent care needed")

    if any(x in text for x in ["stroke", "weakness"]):
        emergency.add("Possible stroke – emergency treatment required")

    if not tests:
        tests.add("Basic blood test")

    if not treatment:
        treatment.update(["Rest", "Hydration"])

    if not advice:
        advice.add("Consult doctor if symptoms worsen")

    if not emergency:
        emergency.add("Seek help if symptoms become severe")

    if any(x in text for x in ["chest pain", "stroke", "breathing"]):
        risk = "High"
    elif any(x in text for x in ["fever", "cough", "diabetes"]):
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "diagnosis": disease_prediction,
        "reasoning": f"Based on symptoms: {', '.join(symptoms)}",
        "confidence": "75%",
        "risk_level": risk,
        "symptoms": symptoms,
        "treatment": list(treatment),
        "doctor_advice": list(advice),
        "tests": list(tests),
        "emergency": list(emergency)
    }


# ------------------ MAIN API ------------------
@csrf_exempt
@api_view(['POST'])
def analyze_patient(request):

    summaries = request.data.get('summaries')

    if not summaries:
        single = request.data.get('summary')
        if single:
            summaries = [single]
        else:
            return Response({"error": "Provide summary"}, status=400)

    results = []

    for summary in summaries:
        try:
            context = get_medical_context(summary)
            graph_data = build_graph(summary)
            disease_prediction = classify_disease(summary)

            llm_response = generate_llm_response(
                summary, context, graph_data, disease_prediction
            )

            ai_output = llm_response if llm_response else generate_rule_based_response(
                summary, context, graph_data, disease_prediction
            )

            saved = PatientAnalysis.objects.create(
                summary=summary,
                diagnosis=ai_output.get("diagnosis"),
                reasoning=ai_output.get("reasoning"),
                confidence=ai_output.get("confidence"),
                risk_level=ai_output.get("risk_level")
            )

            # ✅ FIXED PART
            care_plan = list(set(
                ai_output.get("treatment", []) +
                ai_output.get("doctor_advice", [])
            ))

            tests = ai_output.get("tests", []) if ai_output.get("risk_level") == "High" else []

            results.append({
                "id": saved.id,
                "summary": summary,
                "diagnosis": ai_output.get("diagnosis"),
                "confidence": ai_output.get("confidence"),
                "risk": ai_output.get("risk_level"),
                "symptoms": ai_output.get("symptoms"),
                "care_plan": care_plan,
                "tests": tests,
                "emergency": ai_output.get("emergency")
            })

        except Exception as e:
            results.append({
                "summary": summary,
                "error": str(e)
            })

    return Response({
        "total": len(results),
        "results": results
    })


# ------------------ HISTORY ------------------
@api_view(['GET'])
def get_history(request):
    data = PatientAnalysis.objects.all().order_by('-created_at')[:10]

    result = []
    for item in data:
        result.append({
            "id": item.id,
            "summary": item.summary,
            "diagnosis": item.diagnosis,
            "confidence": item.confidence,
            "risk": item.risk_level,
            "date": item.created_at
        })

    return Response(result)


@csrf_exempt
@api_view(['DELETE'])
def delete_history(request, id):
    try:
        record = PatientAnalysis.objects.get(id=id)
        record.delete()
        return Response({"message": "Deleted successfully"})
    except PatientAnalysis.DoesNotExist:
        return Response({"error": "Record not found"}, status=404)


@csrf_exempt
@api_view(['DELETE'])
def delete_all_history(request):
    PatientAnalysis.objects.all().delete()
    return Response({"message": "All records deleted successfully"})