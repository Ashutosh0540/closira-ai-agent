from agents.summary_agent import SummaryAgent
from utils.state import ConversationState


def main():

    state = ConversationState()

    # Mock conversation history
    state.add_message(
        role="user",
        message="What are your Botox prices?"
    )

    state.add_message(
        role="assistant",
        message="Botox services start from £200."
    )

    # Mock lead qualification
    state.update_lead_data(
        "business_type",
        "Dental Clinic"
    )

    state.update_lead_data(
        "team_size",
        "12"
    )

    state.update_lead_data(
        "current_tools",
        "WhatsApp"
    )

    state.mark_qualification_complete()

    # Mock escalation state
    state.trigger_escalation(
        "Customer frustration detected"
    )

    # Mock SOP gap
    state.add_sop_gap(
        "Asked about laser treatment"
    )

    summary_agent = SummaryAgent()

    summary = summary_agent.generate_summary(
        state
    )

    print("\n=== GENERATED SUMMARY ===\n")

    print(summary)


if __name__ == "__main__":

    main()