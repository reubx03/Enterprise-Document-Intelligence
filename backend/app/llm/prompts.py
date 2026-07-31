from textwrap import dedent


class PromptBuilder:
    """
    Builds prompts for document information extraction.
    """

    FIELD_TEMPLATES = {
        "invoice": [
            "invoice_number",
            "vendor",
            "customer",
            "invoice_date",
            "due_date",
            "subtotal",
            "tax_amount",
            "total_amount",
        ],
        "resume": [
            "candidate_name",
            "email",
            "phone",
            "skills",
            "experience_years",
            "latest_role",
        ],
    }

    @classmethod
    def build_extraction_prompt(
        cls,
        document_text: str,
        document_type: str = "auto",
    ) -> str:

        fields = cls.FIELD_TEMPLATES.get(document_type)

        if fields is None:
            fields = [
                "title",
                "document_type",
                "date",
                "author",
                "summary",
                "key_entities",
                "key_value_pairs",
            ]

        field_list = "\n".join(f"- {field}" for field in fields)

        return dedent(f"""
        You are an expert document intelligence system.

        Analyze the document carefully.

        Extract ONLY the following fields:

        {field_list}

        Rules:
        - Return ONLY valid JSON.
        - Do not include explanations.
        - If a value is missing, return null.
        - Do not invent information.

        Document Type:
        {document_type}

        Document:

        {document_text}
        """).strip()