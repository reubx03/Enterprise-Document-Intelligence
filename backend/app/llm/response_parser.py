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
        try:
            return json.loads(response)

        except json.JSONDecodeError as e:
            raise MalformedExtractionResponseError(
                f"Failed to parse LLM response: {e}"
            )