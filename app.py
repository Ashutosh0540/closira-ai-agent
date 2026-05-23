from agents.faq_agent import FAQAgent
from agents.escalation_agent import EscalationAgent
from agents.qualification_agent import QualificationAgent
from agents.summary_agent import SummaryAgent

from utils.state import ConversationState
from utils.logger import LoggerManager


def main():

    print("\n=== Closira AI Support Workflow ===\n")

    faq_agent = FAQAgent("data/sop.json")

    escalation_agent = EscalationAgent()

    qualification_agent = QualificationAgent()

    summary_agent = SummaryAgent()

    logger = LoggerManager()

    state = ConversationState()

    print("AI: Hello! Welcome to Bloom Aesthetics Clinic.")
    print("AI: How may I assist you today?\n")

    qualification_started = False

    while True:

        user_message = input("Customer: ")

        # Exit
        if user_message.lower() == "exit":

            print("\nGenerating conversation summary...\n")

            summary = summary_agent.generate_summary(
                state
            )

            print("=== Conversation Summary ===\n")

            print(summary)

            logger.log_ai_response(summary)

            print("\nSession ended.")

            break

        logger.log_user_message(user_message)

        state.add_message(
            role="user",
            message=user_message
        )

        # ==================================================
        # QUALIFICATION STAGE ROUTING
        # ==================================================

        if (
            qualification_started
            and not state.qualification_complete
        ):

            qualification_result = (
                qualification_agent.handle_qualification(
                    user_message=user_message,
                    state=state
                )
            )

            print(
                f"\nAI: {qualification_result['message']}\n"
            )

            logger.log_ai_response(
                qualification_result["message"]
            )

            # Qualification completed
            if qualification_result.get(
                "qualification_complete"
            ):

                print(
                    "\n=== Lead Qualification Summary ===\n"
                )

                print(
                    qualification_result[
                        "lead_summary"
                    ]
                )

                logger.log_ai_response(
                    qualification_result[
                        "lead_summary"
                    ]
                )

                state.set_workflow_stage(
                    "completed"
                )

            continue

        # ==================================================
        # ESCALATION CHECK
        # ==================================================

        escalation_result = (
            escalation_agent.check_escalation(
                user_message=user_message,
                state=state
            )
        )

        if escalation_result["needed"]:

            state.trigger_escalation(
                escalation_result["reason"]
            )

            logger.log_escalation(
                escalation_result["reason"]
            )

            ai_response = (
                "I’m escalating this conversation "
                "to a human support agent.\n"
                f"Reason: {escalation_result['reason']}"
            )

            print(f"\nAI: {ai_response}\n")

            logger.log_ai_response(ai_response)

            state.add_message(
                role="assistant",
                message=ai_response
            )

            continue

        # ==================================================
        # FAQ HANDLING
        # ==================================================

        faq_result = faq_agent.answer_question(
            user_message
        )
        # Confidence-based escalation

        if faq_result["confidence"] < 0.75:

            state.trigger_escalation(
                "Low confidence response"
            )

            logger.log_escalation(
                "Low confidence response"
            )

            ai_response = (
                faq_result["response"]
            )

            print(f"\nAI: {ai_response}\n")

            logger.log_ai_response(
                ai_response
            )

            continue

        ai_response = faq_result["response"]

        print(f"\nAI: {ai_response}\n")

        logger.log_ai_response(ai_response)

        state.add_message(
            role="assistant",
            message=ai_response
        )

        # FAQ tracking
        if faq_result["answered_from_sop"]:

            state.add_answered_question(
                user_message
            )

            state.reset_unanswered()

        else:

            state.increment_unanswered()

            state.add_sop_gap(user_message)

            logger.log_sop_gap(user_message)

        # ==================================================
        # NATURAL QUALIFICATION TRANSITION
        # ==================================================

        if (
            state.successful_faq_responses >= 2
            and not qualification_started
        ):

            qualification_started = True

            state.set_workflow_stage(
                "qualification"
            )

            ai_message = (
                "Before we continue, I’d like "
                "to ask a few quick questions "
                "to better understand your needs."
            )

            print(f"AI: {ai_message}\n")

            logger.log_ai_response(ai_message)

            qualification_result = (
                qualification_agent.handle_qualification(
                    user_message="",
                    state=state
                )
            )

            print(
                f"AI: {qualification_result['message']}\n"
            )

            logger.log_ai_response(
                qualification_result["message"]
            )


if __name__ == "__main__":

    main()