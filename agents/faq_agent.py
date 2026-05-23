import json

from utils.llm import LLMClient


class FAQAgent:

    def __init__(self, sop_path):

        self.llm = LLMClient()

        with open(sop_path, "r") as file:

            self.sop_data = json.load(file)

    def build_system_prompt(self):

        sop_content = json.dumps(
            self.sop_data,
            indent=2
        )

        system_prompt = f"""
You are an AI customer support assistant for Bloom Aesthetics Clinic.

Your responsibility is to answer customer questions ONLY using the provided SOP information.

IMPORTANT RULES:

1. NEVER hallucinate, invent, or assume information.

2. ONLY use information explicitly available in the SOP.

3. If the requested information is NOT available in the SOP:
   - clearly state that the information is unavailable in the SOP
   - do NOT guess or generate fake details
   - politely offer escalation to a human support agent if appropriate

4. Keep responses:
   - concise
   - professional
   - customer-friendly

5. For pricing, booking, clinic hours, and services:
   - answer naturally using SOP context
   - support semantic understanding of customer wording

6. If confidence is low or the request is outside SOP scope:
   - set "answered_from_sop" to false
   - set "needs_escalation" to true

7. Return ONLY valid JSON.
Do NOT include markdown.
Do NOT include explanations outside JSON.

SOP INFORMATION:
{sop_content}

Required JSON format:
{{
    "response": "...",
    "confidence": 0.95,
    "answered_from_sop": true,
    "needs_escalation": false,
    "escalation_reason": null
}}
"""

        return system_prompt

    def answer_question(self, user_message):

        system_prompt = self.build_system_prompt()

        user_prompt = f"""
Customer Question:
{user_message}
"""

        try:

            result = self.llm.generate_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.2
            )

            # Basic validation
            required_keys = [
                "response",
                "confidence",
                "answered_from_sop",
                "needs_escalation",
                "escalation_reason"
            ]

            for key in required_keys:

                if key not in result:

                    raise ValueError(
                        f"Missing required key: {key}"
                    )

            return result

        except Exception:

            # Graceful fallback
            return {
                "response": (
                    "I’m unable to confidently answer "
                    "that using the current SOP information. "
                    "I can escalate this to a human support "
                    "agent if needed."
                ),

                "confidence": 0.0,

                "answered_from_sop": False,

                "needs_escalation": True,

                "escalation_reason": (
                    "FAQ processing failure"
                )
            }