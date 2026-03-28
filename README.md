# 🏥 Healthcare AI System

## 🚀 Overview

The **Healthcare AI System** is an intelligent full-stack application that analyzes patient discharge summaries and generates **diagnosis, treatment plans, and risk levels** using a hybrid AI pipeline.

The system combines **RAG, Graph-based reasoning, BERT classification, and LLM-based intelligence** to provide structured and meaningful medical insights.

---

## 🎯 Key Features

* ✅ **Multi-Patient Support**

  * Accepts multiple discharge summaries (up to 30 patients)
  * Processes each patient independently

* 🧠 **BERT-Based Prediction**

  * Predicts disease category from symptoms

* 🔗 **GraphRAG (Graph Reasoning)**

  * Maps symptoms → related diseases

* 📚 **RAG (Medical Context Injection)**

  * Enhances AI accuracy using knowledge base

* 🤖 **LLM Integration (Ollama / OpenRouter)**

  * Generates structured diagnosis & treatment

* ⚠️ **Risk Level Detection**

  * Low / Medium / High classification

* 💊 **Care Plan & Emergency Advice**

  * Step-by-step treatment suggestions
  * When to seek medical help

* 🎨 **Professional UI**

  * Built with Next.js + Material UI
  * Clean, responsive, and interactive design

---

## 🧩 System Architecture

```text
User Input (Multiple Patients)
        ↓
RAG (Medical Knowledge Retrieval)
        ↓
GraphRAG (Symptom → Disease Mapping)
        ↓
BERT (Disease Classification)
        ↓
LLM (Diagnosis + Treatment + Risk)
        ↓
Frontend Display (Cards per Patient)
```

---

## 🛠️ Tech Stack

### 💻 Frontend

* Next.js (React)
* Material UI

### ⚙️ Backend

* Django (Python)
* Django REST Framework

### 🧠 AI Components

* LLM (Ollama - LLaMA3 / OpenRouter)
* BioBERT (Simulated)
* RAG (Custom knowledge base)
* GraphRAG (Custom graph logic)

### 🗄️ Database

* SQLite

---

## 📂 Project Structure

```bash
healthcare-ai-project/
│
├── backend/
│   ├── api/
│   │   ├── views.py
│   │   ├── rag.py
│   │   ├── graph_rag.py
│   │   ├── bert.py
│   │
│   ├── backend/
│   ├── manage.py
│
├── frontend/
│   ├── app/
│   │   ├── page.js
│   ├── package.json
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 🔧 Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows

pip install django djangorestframework requests python-dotenv django-cors-headers

python manage.py runserver
```

---

### 🎨 Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔌 API Usage

### Endpoint

```bash
POST /analyze/
```

---

### 📥 Input (Multiple Patients)

```json
{
  "summaries": [
    "Patient has fever and cough",
    "Patient has chest pain and fatigue",
    "Patient has headache and vomiting"
  ]
}
```

---

### 📤 Output (Example)

```json
{
  "total_patients": 3,
  "results": [
    {
      "summary": "Patient has fever and cough",
      "bert_prediction": "Respiratory Infection",
      "graph_data": {
        "symptoms": ["fever", "cough"],
        "possible_diseases": ["infection"]
      },
      "ai_response": {
        "diagnosis": "Respiratory Infection",
        "risk_level": "Medium",
        "treatment_plan": [
          "Hydration",
          "Paracetamol",
          "Rest"
        ]
      }
    }
  ]
}
```

---

## 🧠 How It Works

1. User enters multiple patient summaries
2. RAG fetches relevant medical knowledge
3. GraphRAG maps symptoms to diseases
4. BERT predicts disease category
5. LLM generates diagnosis, treatment & risk
6. UI displays structured results per patient

---

## 🎥 Demo

📺 **Project Demo Video:**  
👉 [Watch here](https://drive.google.com/file/d/1_xdkxFolPD8MSSwrrk-XeAu7sqQEAjHY/view?usp=drive_link)

---

## 📌 Future Enhancements

* Real BioBERT model integration
* Graph database (Neo4j)
* Patient history tracking
* PDF report generation
* Authentication system

---


