import json

from app.exceptions.extraction_exceptions import (
    MalformedExtractionResponseError,
)


class ResponseParser:
    """
    Parses LLM responses into structured Python objects.
    """

    @staticmethod
    def parse_json(response: str) -> dict:
        """
        Parse JSON returned by the LLM.

        Automatically removes Markdown code fences if present.
        """

        cleaned = response.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]

        if cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            raise MalformedExtractionResponseError(
                f"Failed to parse LLM response: {e}"
            )