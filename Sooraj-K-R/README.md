# Financial Advisor Bot

## What is this?

A CLI-based financial advisor chatbot built with Python and the Groq API. It uses an **Agent + Orchestrator** architecture to route your finance questions to the right specialist agent.

## Features

- **Investment Agent** — SIP calculations, investment returns, compound interest
- **Loan Agent** — EMI calculations, loan interest, repayment questions
- **General Finance Agent** — Budgeting tips, savings advice, general finance
- Simple keyword-based routing via an Orchestrator
- Built-in financial calculation tools

## How It Works

```
User → Orchestrator → Specialist Agent → Financial Tools → Response
```

1. You type a question.
2. The Orchestrator picks the best agent (Investment, Loan, or General).
3. The agent uses the Groq LLM API (with financial tool descriptions) to generate an answer.
4. The response is printed in the terminal.

## Project Structure

```
Sooraj-K-R/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── SYSTEM_DESIGN.md
├── main.py
├── core/
│   ├── __init__.py
│   ├── agent.py
│   └── orchestrator.py
└── tools/
    ├── __init__.py
    └── financial_tools.py
```

## Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key to .env
#    Edit .env and replace "your_api_key_here" with your actual key

# 4. Run the bot
python main.py
```

## Example

```
You: Calculate EMI for a ₹5 lakh loan at 10% for 5 years

[Loan Agent]
Your estimated EMI is ₹10,624.25 per month...

You: How much will a ₹5000 monthly SIP grow in 10 years at 12%?

[Investment Agent]
Your SIP will grow to approximately ₹11,61,695...

You: exit
Goodbye!
```

## Disclaimer

This is an **educational project** built for learning purposes. It does **not** provide professional financial advice. Always consult a qualified financial advisor for real financial decisions.
