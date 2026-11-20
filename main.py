"""Terminal loop interface for AI Financial Advisor Bot."""

import sys
from advisor_agents import run_query


def main():
    print("=" * 60)
    print(" AI Financial Advisor Bot")
    print(" Type your question below, or type 'quit' to exit.")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        result = run_query(user_input)
        print(f"\n[{result['answered_by']}]: {result['answer']}\n")


if __name__ == "__main__":
    main()
