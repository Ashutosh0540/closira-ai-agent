import streamlit as st

from agents.faq_agent import FAQAgent
from agents.escalation_agent import EscalationAgent
from agents.qualification_agent import QualificationAgent
from agents.summary_agent import SummaryAgent

from utils.state import ConversationState


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Closira AI Workflow",
    page_icon="🤖",
    layout="wide"
)


# ======================================================
# INITIALIZE SESSION STATE
# ======================================================

if "conversation_state" not in st.session_state:

    st.session_state.conversation_state = (
        ConversationState()
    )

if "messages" not in st.session_state:

    st.session_state.messages = []

if "qualification_started" not in st.session_state:

    st.session_state.qualification_started = False

if "summary_generated" not in st.session_state:

    st.session_state.summary_generated = None


# ======================================================
# LOAD AGENTS
# ======================================================

faq_agent = FAQAgent("data/sop.json")

escalation_agent = EscalationAgent()

qualification_agent = QualificationAgent()

summary_agent = SummaryAgent()


state = st.session_state.conversation_state


# ======================================================
# UI HEADER
# ======================================================

st.title("🤖 Closira AI Support Workflow")

st.markdown(
    """
AI-powered SMB customer support workflow with:
- SOP-grounded FAQ answering
- lead qualification
- escalation handling
- conversation summarization
"""
)


# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.header("Workflow State")

    st.write(
        f"**Current Stage:** {state.workflow_stage}"
    )

    st.write(
        f"**Escalation Needed:** {state.escalation.needed}"
    )

    if state.escalation.reason:

        st.error(
            f"Escalation Reason: "
            f"{state.escalation.reason}"
        )

    st.divider()

    st.header("Lead Information")

    st.json(state.lead_data)

    st.divider()

    st.header("SOP Gaps")

    if state.sop_gaps:

        for gap in state.sop_gaps:

            st.warning(gap)

    else:

        st.success("No SOP gaps detected")


# ======================================================
# CHAT DISPLAY
# ======================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ======================================================
# INITIAL BOT MESSAGE
# ======================================================

if len(st.session_state.messages) == 0:

    welcome_message = (
        "Hello! Welcome to Bloom Aesthetics Clinic.\n\n"
        "How may I assist you today?"
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome_message
    })

    st.rerun()


# ======================================================
# USER INPUT
# ======================================================

user_input = st.chat_input(
    "Type your message..."
)

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    state.add_message(
        role="user",
        message=user_input
    )

    ai_response = ""


    # ==================================================
    # EXIT / SUMMARY
    # ==================================================

    if user_input.lower() == "exit":

        summary = summary_agent.generate_summary(
            state
        )

        st.session_state.summary_generated = summary

        ai_response = (
            "Conversation summary generated."
        )


    # ==================================================
    # QUALIFICATION ROUTING
    # ==================================================

    elif (
        st.session_state.qualification_started
        and not state.qualification_complete
    ):

        qualification_result = (
            qualification_agent.handle_qualification(
                user_message=user_input,
                state=state
            )
        )

        ai_response = (
            qualification_result["message"]
        )

        if qualification_result.get(
            "qualification_complete"
        ):

            state.set_workflow_stage(
                "completed"
            )


    # ==================================================
    # ESCALATION CHECK
    # ==================================================

    else:

        escalation_result = (
            escalation_agent.check_escalation(
                user_message=user_input,
                state=state
            )
        )

        if escalation_result["needed"]:

            state.trigger_escalation(
                escalation_result["reason"]
            )

            ai_response = (
                "I’m escalating this conversation "
                "to a human support agent.\n\n"
                f"Reason: "
                f"{escalation_result['reason']}"
            )

        else:

            faq_result = (
                faq_agent.answer_question(
                    user_input
                )
            )

            ai_response = faq_result["response"]

            # Confidence escalation
            if faq_result["confidence"] < 0.75:

                state.trigger_escalation(
                    "Low confidence response"
                )

            # FAQ tracking
            # FAQ tracking

            if faq_result["answered_from_sop"]:

                state.add_answered_question(
                    user_input
                )

                state.reset_unanswered()

            else:

                state.increment_unanswered()

                # Prevent duplicate SOP gaps
                if user_input not in state.sop_gaps:

                    state.add_sop_gap(
                        user_input
                    )

            # Trigger escalation for unsupported questions
            if faq_result["needs_escalation"]:

                state.trigger_escalation(
                    faq_result.get(
                        "escalation_reason",
                        "Unsupported question"
                    )
                )

            # Qualification trigger
            if (
                state.successful_faq_responses >= 2
                and not st.session_state
                .qualification_started
            ):

                st.session_state.qualification_started = True

                state.set_workflow_stage(
                    "qualification"
                )

                ai_response += (
                    "\n\nBefore we continue, "
                    "I’d like to ask a few "
                    "quick questions to "
                    "better understand your needs."
                    "\n\nWhat type of business "
                    "do you run?"
                )

    # ==================================================
    # ADD AI MESSAGE
    # ==================================================

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

    state.add_message(
        role="assistant",
        message=ai_response
    )

    st.rerun()


# ======================================================
# SUMMARY DISPLAY
# ======================================================

if st.session_state.summary_generated:

    st.divider()

    st.header("Conversation Summary")

    st.json(
        st.session_state.summary_generated
    )