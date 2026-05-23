from agents.escalation_agent import EscalationAgent
from utils.state import ConversationState


agent = EscalationAgent()

state = ConversationState()

while True:

    message = input("\nCustomer: ")

    if message.lower() == "exit":
        break

    result = agent.check_escalation(
        user_message=message,
        state=state
    )

    print("\nESCALATION RESULT:")
    print(result)