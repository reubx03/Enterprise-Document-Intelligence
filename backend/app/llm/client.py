from google import genai

from app.core.config import settings
from app.exceptions.extraction_exceptions import (
    LLMProviderError,
)


class GeminiClient:
    """
    Client for interacting with the Gemini API.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

        self.model = settings.gemini_model

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Sends a prompt to Gemini and returns the response text.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            return response.text

        except Exception as e:
            raise LLMProviderError(
                f"Gemini API Error: {e}"
            )