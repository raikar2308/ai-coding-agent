"""
llm.py

Handles communication with the Gemini API.
"""

import time
from typing import Optional

from config import model


class LLMClient:

    def __init__(
        self,
        temperature: float = 0.2,
        max_retries: int = 3,
    ):
        self.temperature = temperature
        self.max_retries = max_retries

    def ask(
            self,
            prompt: str,
            system_prompt: Optional[str] = (
                    "You are an expert software engineer and AI coding agent."
            ),
    ) -> str:

        full_prompt = f"{system_prompt}\n\n{prompt}"

        last_error = None

        for attempt in range(1, self.max_retries + 1):

            try:

                response = model.generate_content(full_prompt)

                if getattr(response, "text", None):
                    return response.text.strip()

                raise RuntimeError("Empty response received.")

            except Exception as e:

                last_error = e
                print(f"[Retry {attempt}/{self.max_retries}] {e}")

                if attempt < self.max_retries:
                    time.sleep(attempt * 2)

        raise RuntimeError(f"Gemini API Error:\n{last_error}")

    def ask_json(self, prompt: str):

        return self.ask(
            prompt,
            "Return ONLY valid JSON."
        )

    def ask_code(self, prompt: str):

        return self.ask(
            prompt,
            "Return ONLY valid source code."
        )

    def ask_patch(self, prompt: str):

        return self.ask(
            prompt,
            "Return ONLY a unified diff patch."
        )

    def ask_summary(self, prompt: str):

        return self.ask(
            prompt,
            "Summarize the implementation clearly."
        )