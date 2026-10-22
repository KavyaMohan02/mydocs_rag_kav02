import glob
import os
import pymupdf

os.makedirs("data/text", exist_ok=True)

for path in sorted(glob.glob("data/*.pdf")):
    name = os.path.splitext(os.path.basename(path))[0]
    doc = pymupdf.open(path)
    pages = [page.get_text() for page in doc]
    total_chars = sum(len(p.strip()) for p in pages)

    if total_chars < 50 * len(pages):
        print(f"SKIP (needs OCR): {name} | pages={len(pages)} | chars={total_chars}")
        continue

    out = "\n".join(f"[Page {i + 1}]\n{text}" for i, text in enumerate(pages))
    with open(f"data/text/{name}.txt", "w", encoding="utf-8") as f:
        f.write(out)
    print(f"SAVED: {name} | pages={len(pages)} | chars={total_chars}")