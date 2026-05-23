import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClient:

    def __init__(self):

        self.client = OpenAI(

            api_key=os.getenv(
                "GROQ_API_KEY"
            ),

            base_url="https://api.groq.com/openai/v1"
        )

        self.model = "llama-3.3-70b-versatile"

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2
    ) -> dict:

        response = self.client.chat.completions.create(

            model=self.model,

            temperature=temperature,

            response_format={
                "type": "json_object"
            },

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        content = (
            response.choices[0]
            .message.content
        )

        return json.loads(content)