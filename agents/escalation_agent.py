from utils.llm import LLMClient


class EscalationAgent:

    def __init__(self):

        self.llm = LLMClient()

        # Deterministic escalation keywords
        self.complaint_keywords = [
            "complaint",
            "frustrated",
            "angry",
            "disappointed",
            "upset",
            "terrible",
            "bad service",
            "not happy"
        ]

        self.medical_keywords = [
            "side effects",
            "medical advice",
            "allergy",
            "infection",
            "pain",
            "reaction",
            "safe medically"
        ]

        self.negotiation_keywords = [
            "discount",
            "cheaper",
            "lower price",
            "best price",
            "negotiate",
            "offer"
        ]

        self.human_request_keywords = [
            "human",
            "real person",
            "agent",
            "someone from support",
            "talk to a person"
        ]

        # Messages requiring semantic sentiment analysis
        self.semantic_trigger_words = [
            "issue",
            "problem",
            "annoyed",
            "unhappy",
            "frustrating",
            "disappointing",
            "poor experience",
            "bad experience"
        ]

    def contains_keyword(self, message: str, keywords: list):

        message = message.lower()

        for keyword in keywords:

            if keyword in message:
                return True

        return False

    def rule_based_detection(self, user_message: str):

        if self.contains_keyword(
            user_message,
            self.complaint_keywords
        ):

            return {
                "needed": True,
                "reason": "Complaint or frustration detected"
            }

        if self.contains_keyword(
            user_message,
            self.medical_keywords
        ):

            return {
                "needed": True,
                "reason": "Medical question detected"
            }

        if self.contains_keyword(
            user_message,
            self.negotiation_keywords
        ):

            return {
                "needed": True,
                "reason": "Pricing negotiation detected"
            }

        if self.contains_keyword(
            user_message,
            self.human_request_keywords
        ):

            return {
                "needed": True,
                "reason": "Explicit request for human agent"
            }

        return {
            "needed": False,
            "reason": None
        }

    def requires_semantic_analysis(self, user_message: str):

        message = user_message.lower()

        for word in self.semantic_trigger_words:

            if word in message:
                return True

        return False

    def llm_sentiment_check(self, user_message: str):

        system_prompt = """
You are an escalation detection system.

Your task:
Determine whether the customer message indicates:
- frustration
- anger
- complaint
- aggressive tone
- escalation need

Return ONLY valid JSON.

Required JSON format:
{
    "needs_escalation": true,
    "reason": "..."
}
"""

        user_prompt = f"""
Customer message:
{user_message}
"""

        try:

            result = self.llm.generate_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1
            )

            # Safety validation
            if "needs_escalation" not in result:

                return {
                    "needs_escalation": False,
                    "reason": None
                }

            return result

        except Exception:

            # Graceful degradation
            return {
                "needs_escalation": False,
                "reason": "LLM sentiment analysis unavailable"
            }

    def check_escalation(self, user_message: str, state):

        # STEP 1 — deterministic rules first
        rule_result = self.rule_based_detection(user_message)

        if rule_result["needed"]:

            return rule_result

        # STEP 2 — unanswered question threshold
        if state.unanswered_questions > 2:

            return {
                "needed": True,
                "reason": "More than 2 unanswered questions"
            }

        # STEP 3 — selective semantic analysis
        if self.requires_semantic_analysis(user_message):

            llm_result = self.llm_sentiment_check(
                user_message
            )

            if llm_result.get("needs_escalation"):

                return {
                    "needed": True,
                    "reason": llm_result.get(
                        "reason",
                        "Negative sentiment detected"
                    )
                }

        # No escalation required
        return {
            "needed": False,
            "reason": None
        }