class QualificationAgent:

    def __init__(self):

        self.questions = [
            {
                "key": "business_type",
                "question": (
                    "What type of business do you run?"
                )
            },
            {
                "key": "team_size",
                "question": (
                    "How many people are on your team?"
                )
            },
            {
                "key": "current_tools",
                "question": (
                    "What customer support tools are you currently using?"
                )
            }
        ]

    def get_next_question(self, state):

        for item in self.questions:

            key = item["key"]

            if not state.lead_data.get(key):

                return item

        return None

    def store_answer(self, state, answer):

        next_question = self.get_next_question(state)

        if not next_question:
            return

        key = next_question["key"]

        state.update_lead_data(
            key=key,
            value=answer
        )

    def qualification_complete(self, state):

        for item in self.questions:

            key = item["key"]

            if not state.lead_data.get(key):

                return False

        return True

    def generate_qualification_summary(self, state):

        return {
            "business_type": state.lead_data.get(
                "business_type"
            ),

            "team_size": state.lead_data.get(
                "team_size"
            ),

            "current_tools": state.lead_data.get(
                "current_tools"
            ),

            "qualification_status": (
                "Complete"
                if state.qualification_complete
                else "Incomplete"
            )
        }

    def handle_qualification(self, user_message, state):

        next_question = self.get_next_question(state)

        if next_question and user_message:

            self.store_answer(
                state=state,
                answer=user_message
            )

        upcoming_question = self.get_next_question(state)

        # Qualification completed
        if not upcoming_question:

            state.mark_qualification_complete()

            summary = (
                self.generate_qualification_summary(
                    state
                )
            )

            return {
                "qualification_complete": True,

                "message": (
                    "Thank you for the information. "
                    "Your qualification process "
                    "is complete."
                ),

                "lead_summary": summary
            }

        # Ask next question
        return {
            "qualification_complete": False,

            "message": upcoming_question["question"]
        }