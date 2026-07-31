from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

print("Fetching available models...\n")

try:
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print("Error:", e)