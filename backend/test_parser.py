from app.llm.response_parser import ResponseParser

response = """
{
    "vendor": "ABC Technologies",
    "amount": 5000,
    "currency": "INR"
}
"""

parsed = ResponseParser.parse_json(response)

print(parsed)
print(type(parsed))