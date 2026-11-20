# AI Financial Advisor Bot

A minimal, production-ready multi-agent financial advisory application built with Python, the OpenAI Agents SDK (`openai-agents`), FastAPI, and Streamlit, powered by Groq LLMs.

---

## What It Does

The **AI Financial Advisor Bot** intelligently classifies and routes financial queries across specialized agents with single-hop structured handoffs:

- **Generalist Agent**: Answers general personal finance concepts (e.g. inflation, budgeting, emergency funds) directly. When specialized calculations are needed, it performs a structured handoff with context and reason.
- **Loan Specialist**: Specializes in loans and mortgages, utilizing the `calculate_emi` tool to calculate Equated Monthly Installments (EMI).
- **Investment Specialist**: Specializes in wealth growth and foreign exchange, utilizing `calculate_returns` (compound interest calculation) and `get_exchange_rate` (mock currency exchange lookup).

### Key Architectural Highlights
- **Single-hop Handoffs**: Specialists answer questions directly once routed with zero ping-ponging.
- **Structured Handoff Payloads**: Every handoff transmits structured `{reason, context}` data.
- **Handoff Logging**: Logged in real-time to both console (`[HANDOFF] ...`) and `handoff_log.jsonl`.
- **Dual Interface**: Includes an interactive terminal CLI and a decoupled web stack (FastAPI backend + Streamlit frontend).

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `GROQ_API_KEY` | Your Groq Cloud API key | *Required* |
| `GROQ_MODEL` | Groq LLM model name | `llama-3.3-70b-versatile` |
| `BACKEND_URL` | Base URL of the FastAPI backend for Streamlit | `http://localhost:8000` |

Create a `.env` file from the provided example:
```bash
cp .env.example .env
```
Add your `GROQ_API_KEY` inside `.env`.

---

## How to Run Locally

### 1. Set Up Virtual Environment

```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux / macOS:
# source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Terminal CLI

Run the interactive terminal interface:
```bash
python main.py
```

### 3. FastAPI Backend

Run the REST API backend:
```bash
uvicorn api:app --reload
```
Interactive API documentation is accessible at `http://localhost:8000/docs`.

### 4. Streamlit Frontend

Run the web user interface:
```bash
streamlit run frontend.py
```
Open your browser at `http://localhost:8501`.

---

## Example Queries

### 1. General Financial Question
- **User Query**: `"What is an emergency fund and why do I need one?"`
- **Handled By**: **Generalist**
- **Handoff**: None (answered directly by the Generalist).

### 2. Loan EMI Calculation
- **User Query**: `"Calculate EMI for a loan of 500000 at 9.5% annual interest for 60 months."`
- **Handled By**: **Loan Specialist**
- **Handoff**: `Generalist -> Loan Specialist` | Tool called: `calculate_emi(principal=500000, annual_rate=9.5, tenure_months=60)`
- **Result**: ₹10,500.93 per month.

### 3. Investment & Exchange Rate Query
- **User Query**: `"Calculate compound returns for 50000 at 8% annual rate for 3 years."` or `"What is the exchange rate for USD/INR?"`
- **Handled By**: **Investment Specialist**
- **Handoff**: `Generalist -> Investment Specialist` | Tool called: `calculate_returns` or `get_exchange_rate`
- **Result**: ₹62,985.60 / 1 USD = 86.50 INR.

---

## Live Demo

- App (Streamlit): https://month3sprintaproject-qgmsekinagmxlq3zytksrw.streamlit.app
- API docs (Swagger): https://month3-sprint-a-project.onrender.com/docs

> **Note:** The application is hosted on free tiers. The backend service may spin down during periods of inactivity, so the first request after idle may take about a minute to wake up. In addition, handoff logs (`handoff_log.jsonl`) reset on service restart.

### Deployment Settings

- **Render** (Web Service):
  - **Branch**: `athul-pp`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
  - **Health Check Path**: `/health`
  - **Environment Variables**: `GROQ_API_KEY`
- **Streamlit Community Cloud**:
  - **Branch**: `athul-pp`
  - **Main file path**: `frontend.py`
  - **Secret**: `BACKEND_URL`
