from app.llm.client import GeminiClient
from app.llm.prompts import PromptBuilder
from app.llm.response_parser import ResponseParser


class ExtractionService:
    """
    Coordinates the document extraction pipeline.
    """

    def __init__(self):
        self.llm_client = GeminiClient()

    def extract(
        self,
        document_text: str,
        document_type: str = "auto",
    ) -> dict:
        """
        Extract structured information from OCR text.
        """

        # -----------------------------
        # Build Prompt
        # -----------------------------
        prompt = PromptBuilder.build_extraction_prompt(
            document_text=document_text,
            document_type=document_type,
        )

        # -----------------------------
        # Generate LLM Response
        # -----------------------------
        response = self.llm_client.generate(prompt)

        print("\n========== RAW GEMINI RESPONSE ==========")
        print(response)
        print("=========================================\n")

        # -----------------------------
        # Parse JSON Response
        # -----------------------------
        parsed_response = ResponseParser.parse_json(response)

        print("\n========== PARSED GEMINI RESPONSE ==========")
        print(parsed_response)
        print("============================================\n")

        return parsed_response