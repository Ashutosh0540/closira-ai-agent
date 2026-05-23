from utils.llm import LLMClient


class SummaryAgent:

    def __init__(self):

        self.llm = LLMClient()

    def build_system_prompt(self):

        return """
You are an AI conversation summarization system.

Your task:
Generate a structured customer support summary.

IMPORTANT RULES:
1. Use ONLY provided conversation data.
2. Do NOT hallucinate missing information.
3. Be concise and professional.
4. Clearly summarize:
   - customer intent
   - lead qualification details
   - escalation history
   - SOP gaps
   - recommended next action
5. Return ONLY valid JSON.

Required JSON format:
{
    "customer_intent": "...",

    "lead_summary": {
        "business_type": "...",
        "team_size": "...",
        "current_tools": "...",
        "qualification_status": "Complete"
    },

    "escalation_summary": {
        "escalation_needed": true,
        "reason": "..."
    },

    "sop_gaps_identified": [],

    "workflow_stage": "...",

    "recommended_next_action": "..."
}
"""

    def generate_summary(self, state):

        system_prompt = self.build_system_prompt()

        qualification_status = (
            "Complete"
            if state.qualification_complete
            else "Incomplete"
        )

        user_prompt = f"""
Conversation History:
{state.conversation_history}

Lead Data:
{state.lead_data}

Qualification Status:
{qualification_status}

Escalation State:
Needed: {state.escalation.needed}
Reason: {state.escalation.reason}

Escalation History:
{state.escalation_history}

SOP Gaps:
{state.sop_gaps}

Workflow Stage:
{state.workflow_stage}

Unanswered Questions:
{state.unanswered_questions}
"""

        result = self.llm.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2
        )

        return result