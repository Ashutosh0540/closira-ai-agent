from agents.qualification_agent import QualificationAgent
from utils.state import ConversationState


def main():

    agent = QualificationAgent()

    state = ConversationState()

    print("\n=== Qualification Flow Test ===\n")

    # Start qualification
    result = agent.handle_qualification(
        user_message="",
        state=state
    )

    print(f"AI: {result['message']}")

    while True:

        user_input = input("\nCustomer: ")

        result = agent.handle_qualification(
            user_message=user_input,
            state=state
        )

        print(f"\nAI: {result['message']}")

        if result["qualification_complete"]:

            print("\n=== Lead Qualification Summary ===\n")

            print(result["lead_summary"])

            break


if __name__ == "__main__":

    main()