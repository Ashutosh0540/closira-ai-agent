from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class EscalationState:

    needed: bool = False

    reason: Optional[str] = None


@dataclass
class ConversationState:

    customer_name: Optional[str] = None

    intent: Optional[str] = None

    workflow_stage: str = "faq"

    qualification_complete: bool = False

    lead_data: Dict = field(default_factory=lambda: {
        "business_type": None,
        "team_size": None,
        "current_tools": None
    })

    conversation_history: List[Dict] = field(
        default_factory=list
    )

    unanswered_questions: int = 0

    successful_faq_responses: int = 0

    answered_faq_questions: List[str] = field(
        default_factory=list
    )

    sop_gaps: List[str] = field(
        default_factory=list
    )

    escalation_history: List[Dict] = field(
        default_factory=list
    )

    escalation: EscalationState = field(
        default_factory=EscalationState
    )

    def add_message(self, role: str, message: str):

        self.conversation_history.append({
            "role": role,
            "message": message
        })

    def increment_unanswered(self):

        self.unanswered_questions += 1

    def reset_unanswered(self):

        self.unanswered_questions = 0

    def increment_successful_faq(self):

        self.successful_faq_responses += 1

    def add_answered_question(self, question: str):

        normalized_question = (
            question.strip().lower()
        )

        if (
            normalized_question
            not in self.answered_faq_questions
        ):

            self.answered_faq_questions.append(
                normalized_question
            )

            self.increment_successful_faq()

    def add_sop_gap(self, question: str):

        self.sop_gaps.append(question)

    def update_lead_data(self, key: str, value: str):

        if key in self.lead_data:

            self.lead_data[key] = value

    def set_intent(self, intent: str):

        self.intent = intent

    def set_workflow_stage(self, stage: str):

        self.workflow_stage = stage

    def mark_qualification_complete(self):

        self.qualification_complete = True

    def trigger_escalation(self, reason: str):

        self.escalation.needed = True

        self.escalation.reason = reason

        self.escalation_history.append({
            "reason": reason
        })