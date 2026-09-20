from core.orchestrator import Orchestrator


def main():
    print("=" * 40)
    print("       Financial Advisor Bot")
    print("=" * 40)
    print("Ask me anything about investments, loans, or personal finance.")
    print("Type 'exit', 'quit', or 'bye' to leave.\n")

    try:
        orchestrator = Orchestrator()
    except ValueError as e:
        print(f"Error: {e}")
        return

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "bye"):
            print("Goodbye!")
            break

        agent_name, response = orchestrator.handle(user_input)
        print(f"\n[{agent_name}]")
        print(f"{response}\n")


if __name__ == "__main__":
    main()
