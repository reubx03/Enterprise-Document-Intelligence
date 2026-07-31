from textwrap import dedent


class PromptBuilder:
    """
    Builds prompts for document information extraction.
    """

    @staticmethod
    def build_extraction_prompt(document_text: str) -> str:
        return dedent(f"""
        You are an expert document intelligence system.

        Analyze the following document and extract the important information.

        Return ONLY valid JSON.

        If a field cannot be found, use null.

        Document:

        {document_text}
        """).strip()