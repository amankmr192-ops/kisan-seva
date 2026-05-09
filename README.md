# 🌾 Kisan Seva — AI-Powered Government Scheme Finder for Indian Farmers

> Final Year MCA Project | Python + LangChain + Ollama + FastAPI

---

## 📌 Problem Statement

Millions of Indian farmers are unaware of government schemes they are eligible for.
Even when aware, they struggle to understand eligibility criteria, required documents,
and application procedures — due to complex language and lack of personalized guidance.

**Kisan Seva** solves this by combining RAG (Retrieval-Augmented Generation) with a
personalized eligibility engine to give every farmer a tailored, actionable answer
in Hinglish — their natural language.

---

## 💡 How Is This Different from ChatGPT?

| ChatGPT / Gemini | Kisan Seva |
|---|---|
| Generic answers | Personalized to farmer's profile |
| May hallucinate scheme details | Answers grounded in official PDFs |
| English only | Hinglish (Hindi + English) |
| No eligibility checking | Real-time eligibility engine |
| No document checklist | Downloadable checklist per scheme |
| Requires internet | Runs 100% offline (Ollama) |
| No source citation | Shows which PDF the answer came from |

> "ChatGPT tells you what PM-KISAN is. Kisan Seva tells Ramesh Kumar from Bihar —
> who owns 2.5 acres — that he is eligible, needs these 4 documents, and should
> visit his nearest CSC centre before March 31st."

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND (HTML)                    │
│         Farmer Profile Form + Scheme Cards           │
│              Hinglish AI Chat Widget                 │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP (fetch API)
┌───────────────────────▼─────────────────────────────┐
│                 FASTAPI BACKEND                      │
│   /api/eligibility  │  /api/chat  │  /api/schemes   │
└──────────┬──────────┴──────┬──────────────────────┘
           │                 │
┌──────────▼──────┐  ┌───────▼────────────────────────┐
│  Eligibility    │  │      LangChain RAG Chain         │
│  Engine         │  │  ConversationalRetrievalChain    │
│  (Rule-based)   │  └───────┬──────────────┬──────────┘
└─────────────────┘          │              │
                    ┌────────▼───┐  ┌───────▼────────┐
                    │   FAISS    │  │  Ollama Mistral │
                    │ VectorStore│  │  (Local LLM)   │
                    └────────────┘  └────────────────┘
                         ▲
                ┌────────┴────────┐
                │  PDF Documents  │
                │  PM-KISAN       │
                │  PMFBY          │
                │  KCC            │
                └─────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| LLM | Ollama + Mistral 7B | Local AI, no internet needed |
| Orchestration | LangChain 0.2.x | RAG chain, memory, prompts |
| Vector Store | FAISS | Fast similarity search |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 | Text to vectors |
| PDF Loader | PyMuPDF | Extract text from scheme PDFs |
| Backend | FastAPI + Uvicorn | REST API server |
| Frontend | HTML + Tailwind CSS + Vanilla JS | Farmer-friendly UI |
| Language | Python 3.11 | Core language |

---

## 📁 Project Structure

```
kisan-seva/
├── data/
│   └── schemes/              ← Government scheme PDFs
│       ├── pm_kisan.pdf
│       ├── pmfby.pdf
│       └── kisan_credit_card.pdf
├── vectorstore/
│   └── faiss_index/          ← Auto-generated, do not edit
├── backend/
│   ├── main.py               ← FastAPI app + all routes
│   ├── rag_chain.py          ← LangChain RAG pipeline
│   ├── eligibility.py        ← Farmer profile + scheme matching
│   └── ingest.py             ← PDF → chunks → FAISS index
├── frontend/
│   ├── index.html            ← Complete UI (single file)
│   └── app.js                ← (reserved for future use)
├── venv/                     ← Python virtual environment
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- macOS / Linux / Windows
- Python 3.10 or 3.11
- [Ollama](https://ollama.com) installed
- Mistral model downloaded

### Step 1 — Clone & Setup

```bash
git clone <your-repo-url>
cd kisan-seva
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Download Ollama Model

```bash
ollama pull mistral
```

### Step 4 — Add Scheme PDFs

Download official government scheme PDFs and place them in `data/schemes/`:

| File | Source |
|---|---|
| `pm_kisan.pdf` | pmkisan.gov.in |
| `pmfby.pdf` | pmfby.gov.in |
| `kisan_credit_card.pdf` | rbi.org.in |

### Step 5 — Build Vector Store

```bash
python3 backend/ingest.py
```

### Step 6 — Start the Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Step 7 — Open the App

```
http://localhost:8000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serve frontend UI |
| GET | `/health` | Check server + RAG status |
| GET | `/api/schemes` | List all loaded schemes |
| POST | `/api/eligibility` | Check farmer eligibility |
| POST | `/api/chat` | RAG-powered AI chat |

### Example — Eligibility Check

```bash
curl -X POST http://localhost:8000/api/eligibility \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Bihar",
    "land_acres": 2.5,
    "category": "General",
    "annual_income": 80000,
    "crop_type": "wheat",
    "has_bank_account": true,
    "has_aadhaar": true
  }'
```

### Example — AI Chat

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "PM-KISAN ke liye documents kya chahiye?"}'
```

Interactive API docs available at: `http://localhost:8000/docs`

---

## 🌟 Key Features

### 1. Personalized Eligibility Engine
Farmer fills a simple form → system checks all 6 schemes against their profile
(land size, state, category, income) → shows eligible and non-eligible schemes instantly.

### 2. RAG-Powered Hinglish Chatbot
Questions answered from actual government PDF documents.
Responses in Hinglish (Roman Hindi + English) — natural for Indian farmers.
Every answer cites its source PDF.

### 3. Document Checklist Download
One click generates a personalized PDF checklist of documents needed
for all eligible schemes — farmer can print and carry to CSC centre.

### 4. 100% Offline
Entire system runs locally using Ollama. No API keys, no internet
dependency, no data privacy concerns. Perfect for rural deployment.

---

## 🎯 Schemes Covered

| Scheme | Benefit |
|---|---|
| PM-KISAN | ₹6,000/year direct income support |
| PMFBY | Crop insurance at 2% premium |
| Kisan Credit Card | Credit up to ₹3 lakh at 4% interest |
| SMAM Subsidy | Up to 50% subsidy on farm machinery |
| Soil Health Card | Free soil testing + fertilizer advice |
| eNAM | Online marketplace for best crop prices |

---

## 🔮 Future Scope

- Voice input in Hindi/Bhojpuri using OpenAI Whisper
- WhatsApp bot integration for rural farmers
- State-specific scheme variations (Bihar vs UP vs Maharashtra)
- Multilingual support (Tamil, Telugu, Marathi, Bengali)
- Nearest CSC centre locator using Google Maps API
- Real-time scheme deadline alerts

---

## 👨‍💻 Developed By

**Aman Kumar**
Final Year MCA Student
*"Technology should serve those who need it most."*

---

## 📄 License

MIT License — Free to use, modify, and distribute.