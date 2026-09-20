from core.agent import Agent
from tools.financial_tools import (
    calculate_emi,
    calculate_simple_interest,
    calculate_compound_interest,
    calculate_sip_returns,
    calculate_returns,
)


INVESTMENT_PROMPT = (
    "You are an Investment Advisor. You help users with SIP calculations, "
    "investment returns, compound interest, and general investment questions. "
    "Use the available tools to perform calculations when needed. "
    "Always show the numbers clearly."
)

LOAN_PROMPT = (
    "You are a Loan Advisor. You help users with EMI calculations, loan "
    "interest, repayment schedules, and loan-related questions. "
    "Use the available tools to perform calculations when needed. "
    "Always show the numbers clearly."
)

GENERAL_PROMPT = (
    "You are a General Finance Advisor. You help users with budgeting, "
    "savings tips, and general financial guidance. Give practical, "
    "easy-to-understand advice."
)

INVESTMENT_TOOLS = {
    "calculate_sip_returns": calculate_sip_returns,
    "calculate_returns": calculate_returns,
    "calculate_compound_interest": calculate_compound_interest,
}

LOAN_TOOLS = {
    "calculate_emi": calculate_emi,
    "calculate_simple_interest": calculate_simple_interest,
    "calculate_compound_interest": calculate_compound_interest,
}

GENERAL_TOOLS = {
    "calculate_simple_interest": calculate_simple_interest,
    "calculate_compound_interest": calculate_compound_interest,
}

# Keywords used for simple routing
INVESTMENT_KEYWORDS = ["sip", "invest", "mutual fund", "compound interest", "returns", "portfolio", "stocks"]
LOAN_KEYWORDS = ["emi", "loan", "borrow", "repay", "mortgage", "debt", "credit"]


class Orchestrator:
    """Routes user queries to the appropriate specialist agent."""

    def __init__(self):
        self.agents = {
            "investment": Agent("Investment Agent", INVESTMENT_PROMPT, INVESTMENT_TOOLS),
            "loan": Agent("Loan Agent", LOAN_PROMPT, LOAN_TOOLS),
            "general": Agent("General Finance Agent", GENERAL_PROMPT, GENERAL_TOOLS),
        }

    def route(self, message: str) -> str:
        """Pick the best agent based on keywords in the user's message."""
        lower = message.lower()

        for keyword in LOAN_KEYWORDS:
            if keyword in lower:
                return "loan"

        for keyword in INVESTMENT_KEYWORDS:
            if keyword in lower:
                return "investment"

        return "general"

    def handle(self, message: str) -> tuple[str, str]:
        """Route the message and return (agent_name, response)."""
        agent_key = self.route(message)
        agent = self.agents[agent_key]
        response = agent.process(message)
        return agent.name, response
