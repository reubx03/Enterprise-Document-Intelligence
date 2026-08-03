from textwrap import dedent


class PromptBuilder:
    """
    Builds prompts for document information extraction.

    Output contract (required by DocumentProcessingService / persistence):
    {
        "document_type": "...",
        "fields": {
            "<field_name>": {
                "value": <string | number | list | null>,
                "confidence": <float 0.0-1.0>
            },
            ...
        },
        "overall_confidence": <float 0.0-1.0>,
        "requires_review": <bool>
    }
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

        example_fields = ",\n".join(
            f'        "{field}": {{"value": null, "confidence": 0.0}}'
            for field in fields
        )

        return dedent(f"""
        You are an expert document intelligence system.

        Analyze the document carefully.

        Extract ONLY the following fields:

        {field_list}

        For EACH field, provide:
        - "value": the extracted value (string, number, or list as appropriate),
          or null if the field is not present in the document.
        - "confidence": a float between 0.0 and 1.0 representing how directly
          and clearly this value appears in the document. Use 1.0 only when
          the value is stated explicitly and unambiguously. Use lower values
          when the value is inferred, partially visible, or uncertain due to
          poor OCR quality. Use 0.0 when the field could not be found at all.

        Rules:
        - Return ONLY valid JSON. No explanations, no markdown, no code fences.
        - Do not invent information. If a value is missing, "value" must be null
          and "confidence" must be 0.0.
        - Base every confidence score strictly on evidence in the document text,
          not on general assumptions about the document type.

        Return your response in EXACTLY this JSON shape:

        {{
            "document_type": "{document_type}",
            "fields": {{
        {example_fields}
            }},
            "overall_confidence": 0.0,
            "requires_review": true
        }}

        Where:
        - "document_type" is the type of document you identified
          (e.g. "invoice", "resume", "contract", "receipt", "purchase_order",
          "bank_statement", or "unknown" if it does not match any known type).
        - "overall_confidence" is the average of all field confidence scores
          above, as a float between 0.0 and 1.0.
        - "requires_review" is true if overall_confidence is below 0.75,
          OR if any individual required field has confidence below 0.5,
          OR if more than one field could not be found. Otherwise false.

        Document Type Hint:
        {document_type}

        Document:

        {document_text}
        """).strip()