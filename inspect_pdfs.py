import glob
import pymupdf

for path in sorted(glob.glob("data/*.pdf")):
    try:
        doc = pymupdf.open(path)
        pages = len(doc)
        text = "".join(doc[i].get_text() for i in range(min(3, pages)))
        letters = [c for c in text if c.isalpha()]
        tamil = [c for c in letters if "\u0b80" <= c <= "\u0bff"]
        if len(text.strip()) < 50:
            kind, lang = "scanned", "unknown"
        else:
            kind = "digital"
            lang = "Tamil" if letters and len(tamil) / len(letters) > 0.3 else "English"
        print(f"{path} | pages={pages} | type={kind} | language={lang}")
    except Exception as e:
        print(f"{path} | error: {e}")