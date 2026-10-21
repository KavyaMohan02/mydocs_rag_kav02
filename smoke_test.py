import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not found. Check your .env file.")

client = genai.Client(api_key=api_key)

models = ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-flash-latest"]

for model in models:
    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model=model,
                contents="Say hello in Tamil and English.",
            )
            print(f"Worked with {model}:")
            print(resp.text)
            raise SystemExit(0)
        except SystemExit:
            raise
        except Exception as e:
            print(f"{model}, attempt {attempt + 1} failed: {str(e)[:120]}")
            time.sleep(5)

print("All models failed. Try again in a few minutes.")