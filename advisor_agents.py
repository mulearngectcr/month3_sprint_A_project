"""Multi-agent setup with Generalist and Specialists using OpenAI Agents SDK and Groq."""

import asyncio
import concurrent.futures
from datetime import datetime, timezone
import json
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI, NotFoundError
from pydantic import BaseModel

from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    handoff,
    set_default_openai_client,
    set_tracing_disabled,
)
from tools import (
    calculate_emi_tool,
    calculate_returns_tool,
    get_exchange_rate_tool,
)

load_dotenv()
set_tracing_disabled(True)

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
FALLBACK_MODEL = "openai/gpt-oss-120b"
LOG_FILE = "handoff_log.jsonl"


class HandoffPayload(BaseModel):
    reason: str
    context: str


def get_groq_client() -> AsyncOpenAI:
    api_key = os.getenv("GROQ_API_KEY", "")
    client = AsyncOpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
    set_default_openai_client(client)
    return client


def make_specialist_handoff(specialist_agent: Agent, from_name: str, to_name: str):
    def on_handoff(ctx, payload: HandoffPayload):
        timestamp = datetime.now(timezone.utc).isoformat()
        log_entry = {
            "timestamp": timestamp,
            "from_agent": from_name,
            "to_agent": to_name,
            "reason": payload.reason,
            "context": payload.context,
        }

        # Append one JSON line to handoff_log.jsonl
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as err:
            print(f"Error writing to {LOG_FILE}: {err}")

        # Print console message as specified
        print(f"[HANDOFF] {from_name} -> {to_name} | reason: {payload.reason}")

        # Record handoff details into the run context
        if isinstance(ctx.context, dict):
            ctx.context["handoff"] = {
                "from": from_name,
                "to": to_name,
                "reason": payload.reason,
                "context": payload.context,
            }

    return handoff(
        specialist_agent,
        input_type=HandoffPayload,
        on_handoff=on_handoff,
    )


def build_agents(model_name: str):
    client = get_groq_client()
    model = OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    loan_specialist = Agent(
        name="Loan Specialist",
        instructions=(
            "You are a Loan Specialist financial advisor. "
            "You handle questions regarding loans, mortgages, borrowing, and EMI calculations. "
            "Always use the calculate_emi tool when the user asks to calculate or estimate an EMI. "
            "Provide accurate, clear, and concise answers. You do NOT have any handoffs."
        ),
        tools=[calculate_emi_tool],
        model=model,
    )

    investment_specialist = Agent(
        name="Investment Specialist",
        instructions=(
            "You are an Investment Specialist financial advisor. "
            "You handle questions regarding investments, wealth growth, returns calculations, and currency exchange rates. "
            "Always use the calculate_returns tool when asked to calculate investment growth or returns. "
            "Always use the get_exchange_rate tool when asked for currency exchange rates. "
            "Provide accurate, clear, and concise answers. You do NOT have any handoffs."
        ),
        tools=[calculate_returns_tool, get_exchange_rate_tool],
        model=model,
    )

    loan_h = make_specialist_handoff(loan_specialist, "Generalist", "Loan Specialist")
    invest_h = make_specialist_handoff(investment_specialist, "Generalist", "Investment Specialist")

    generalist = Agent(
        name="Generalist",
        instructions=(
            "You are a Generalist Financial Advisor. "
            "Answer general financial questions directly and concisely (e.g., budgeting, emergency funds, inflation, personal finance basics). "
            "If the question involves loans, mortgages, or calculating loan EMI, immediately hand off to the Loan Specialist with reason and context. "
            "If the question involves investments, calculating investment returns, or currency exchange rates, immediately hand off to the Investment Specialist with reason and context. "
            "Do NOT calculate loan EMIs, investment returns, or exchange rates yourself."
        ),
        handoffs=[loan_h, invest_h],
        model=model,
    )

    return generalist


async def _run_query_async(text: str) -> dict:
    query_ctx = {"handoff": None}
    preferred_model = os.getenv("GROQ_MODEL", DEFAULT_MODEL)
    agent = build_agents(preferred_model)

    try:
        result = await Runner.run(agent, text, context=query_ctx)
    except NotFoundError:
        # Fallback if the configured model is not available on the current Groq account
        agent = build_agents(FALLBACK_MODEL)
        result = await Runner.run(agent, text, context=query_ctx)

    answered_by = result.last_agent.name if result.last_agent else "Generalist"
    return {
        "answer": str(result.final_output),
        "answered_by": answered_by,
        "handoff": query_ctx.get("handoff"),
    }


def run_query(text: str) -> dict:
    """Run a query through the financial agent system.

    Returns:
        dict: {
            'answer': str,
            'answered_by': str,
            'handoff': {'from': str, 'to': str, 'reason': str, 'context': str} or None
        }
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, _run_query_async(text)).result()
    else:
        return asyncio.run(_run_query_async(text))
