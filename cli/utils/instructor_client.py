import os
import instructor
from openai import OpenAI


def get_client_and_model():
    if os.getenv("OPENAI_API_KEY", False):
        client = instructor.from_openai(OpenAI())
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    else:
        client = instructor.from_openai(
            OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",  # required, but unused
            ),
            mode=instructor.Mode.JSON,
        )
        model = os.getenv("OLLAMA_MODEL", "llama3:8b")
    return client, model
