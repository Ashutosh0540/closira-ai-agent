import logging
import os


class LoggerManager:

    def __init__(self):

        os.makedirs("logs", exist_ok=True)

        logging.basicConfig(
            filename="logs/conversation.log",
            level=logging.INFO,
            format=(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
        )

        self.logger = logging.getLogger("ClosiraAI")

    def log_user_message(self, message):

        self.logger.info(
            f"USER MESSAGE: {message}"
        )

    def log_ai_response(self, response):

        self.logger.info(
            f"AI RESPONSE: {response}"
        )

    def log_escalation(self, reason):

        self.logger.warning(
            f"ESCALATION TRIGGERED: {reason}"
        )

    def log_sop_gap(self, question):

        self.logger.warning(
            f"SOP GAP IDENTIFIED: {question}"
        )

    def log_error(self, error):

        self.logger.error(
            f"SYSTEM ERROR: {error}"
        )