import os
from dotenv import load_dotenv
from openai import OpenAI


class LLMClient:
    """"""

    def __init__(self):
        load_dotenv()
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise ValueError("HF_TOKEN is not set.")

        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_token,
        )

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.responses.create(
                model="openai/gpt-oss-120b",
                instructions="You are a helpful AI assistant.",
                input=prompt,
            )
            return response.output_text

        except Exception as exc:
            raise RuntimeError("LLM request failed.") from exc
