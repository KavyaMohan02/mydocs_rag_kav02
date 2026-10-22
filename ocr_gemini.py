import os
import sys
import time
import pymupdf
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not found. Check your .env file.")

client = genai.Client(api_key=api_key)
MODEL = "gemini-flash-latest"
PROMPT = (
    "Transcribe all the text on this page exactly as written, in its original "
    "language(s) (Tamil and/or English). Do not translate, summarize, or correct "
    "anything. Keep tables as Markdown tables. If a part is unreadable, write "
    "[illegible]. Output only the transcribed text."
)

os.makedirs("data/text", exist_ok=True)
os.makedirs("data/ocr_cache", exist_ok=True)


def ocr_page(png_bytes):
    for attempt in range(4):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=[types.Part.from_bytes(data=png_bytes, mime_type="image/png"), PROMPT],
            )
            if not resp.text:
                reason = resp.candidates[0].finish_reason if resp.candidates else "no candidates"
                print(f"  empty result, reason: {reason}")
                return "EMPTY"
            return resp.text
        except Exception as e:
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                print("  Quota reached. Wait a few minutes (or until tomorrow) and run again.")
                return "QUOTA"
            print(f"  retry {attempt + 1}: {msg[:100]}")
            time.sleep(5 * (attempt + 1))
    return None


files = sys.argv[1:]
if not files:
    raise SystemExit("Usage: python ocr_gemini.py data/G.O.56.pdf")

for path in files:
    name = os.path.splitext(os.path.basename(path))[0]
    out_path = f"data/text/{name}.txt"
    if os.path.exists(out_path):
        print(f"SKIP (already done): {name}")
        continue

    doc = pymupdf.open(path)
    parts = []
    for i, page in enumerate(doc):
        cache = f"data/ocr_cache/{name}_p{i + 1}.txt"
        if os.path.exists(cache):
            with open(cache, encoding="utf-8") as f:
                text = f.read()
            print(f"  page {i + 1}/{len(doc)} loaded from cache")
        else:
            png = page.get_pixmap(dpi=200).tobytes("png")
            text = ocr_page(png)
            if text == "QUOTA":
                raise SystemExit(f"Stopped at page {i + 1} of {name}. Progress is saved.")
            if text in (None, "EMPTY"):
                print(f"NOT SAVED: {name} (page {i + 1} failed)")
                parts = None
                break
            with open(cache, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  page {i + 1}/{len(doc)} done")
            time.sleep(8)
        parts.append(f"[Page {i + 1}]\n{text}")

    if parts is None:
        continue
    out = "\n".join(parts)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"SAVED: {name} | pages={len(parts)} | chars={len(out)}")