from app.llm.client import GeminiClient
from app.llm.prompts import PromptBuilder
from app.llm.response_parser import ResponseParser


class ExtractionService:
    """
    Coordinates the document extraction pipeline.
    """

    def __init__(self):
        self.llm_client = GeminiClient()

    def extract(self, document_text: str) -> dict:
        """
        Extract structured information from OCR text.
        """

        # Build prompt
        prompt = PromptBuilder.build_extraction_prompt(document_text)

        # Generate LLM response
        response = self.llm_client.generate(prompt)

        # Parse JSON response
        parsed_response = ResponseParser.parse_json(response)

        return parsed_response