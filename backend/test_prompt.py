from app.llm.prompts import PromptBuilder

text = """
Invoice #12345
Vendor: ABC Technologies
Total: ₹5,000
"""

prompt = PromptBuilder.build_extraction_prompt(text)

print(prompt)