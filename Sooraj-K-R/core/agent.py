import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class Agent:
    """A generic agent that communicates with the Groq API."""

    def __init__(self, name: str, system_prompt: str, tools: dict):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")

        self.client = Groq(api_key=api_key)

    def process(self, user_message: str) -> str:
        """Send a user message to the Groq API and return the response."""
        tools_description = "\n".join(
            f"- {name}: {func.__doc__}" for name, func in self.tools.items()
        )

        full_prompt = (
            f"{self.system_prompt}\n\n"
            f"You have access to these financial tools:\n{tools_description}\n\n"
            f"When a calculation is needed, compute it yourself using the formulas "
            f"and include the numbers in your answer. Be concise and helpful."
        )

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.3,
                max_tokens=1024,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Sorry, I encountered an error: {e}"
