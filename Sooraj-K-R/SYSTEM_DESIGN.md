# SYSTEM_DESIGN.md

## 1. Overview

The Financial Advisor Bot is a CLI-based chatbot that answers personal finance questions. It uses a multi-agent architecture where an Orchestrator routes user queries to one of three specialist agents (Investment, Loan, or General Finance), each backed by the Groq LLM API and a set of financial calculation tools.

## 2. Architecture

```
User
  │
  ▼
CLI (main.py)
  │
  ▼
Orchestrator
  │
  ▼
┌───────────────┬───────────────┬───────────────┐
│  Investment   │     Loan      │    General    │
│    Agent      │     Agent     │  Finance Agent│
└───────────────┴───────────────┴───────────────┘
        │
        ▼
 Financial Tools
 (Pure Python functions)
```

## 3. Components

### `main.py`
The entry point. Runs a simple input loop, sends user messages to the Orchestrator, and prints the response.

### `Orchestrator` (`core/orchestrator.py`)
Creates the three specialist agents at startup. When a message arrives, it checks for keywords to decide which agent should handle it, then forwards the message and returns the response.

### `Agent` (`core/agent.py`)
A generic class that wraps the Groq API. Each agent has a name, a system prompt (defining its personality/expertise), and a set of tool functions. The same `Agent` class is reused for all three specialists — only the prompt and tools differ.

### `Financial Tools` (`tools/financial_tools.py`)
Pure Python functions for EMI, simple interest, compound interest, SIP returns, and lump-sum returns. They have no external dependencies and can be tested independently.

## 4. Request Flow

Example: *"Calculate EMI for a ₹5 lakh loan at 10% for 5 years"*

```
User types the question
        │
        ▼
main.py passes it to Orchestrator
        │
        ▼
Orchestrator sees "EMI" / "loan" → picks Loan Agent
        │
        ▼
Loan Agent sends the question to Groq API
(system prompt includes tool descriptions)
        │
        ▼
Groq returns a helpful answer with the calculation
        │
        ▼
Response is printed back to the user
```

## 5. LLD Principles Used

- **Separation of Concerns** — Routing logic lives in the Orchestrator, LLM communication lives in the Agent, and calculations live in Financial Tools. Each module has a clear job.

- **Single Responsibility** — The Agent class only handles API communication. It does not decide which queries it should receive; that is the Orchestrator's job.

- **Reusability** — The same `Agent` class is instantiated three times with different prompts and tools. The financial tool functions can be used anywhere, not just inside agents.

- **Dependency Injection** — Agents receive their tools and prompts as constructor arguments instead of creating them internally. This makes it easy to add new agents or swap tools.
