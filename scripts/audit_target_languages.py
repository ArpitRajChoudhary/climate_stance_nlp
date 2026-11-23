import pandas as pd
from pathlib import Path

source = Path("data/processed/annotations_all.csv")
output = Path("data/processed/language_script_audit.csv")

df = pd.read_csv(source, keep_default_na=False)

# Keep only comments marked Relevant.
df = df[df["relevance"] == "Relevant"].copy()

def detect_script(text):
    has_devanagari = False
    has_bengali = False
    has_latin = False

    for char in str(text):
        code = ord(char)

        if 0x0900 <= code <= 0x097F:
            has_devanagari = True
        elif 0x0980 <= code <= 0x09FF:
            has_bengali = True
        elif (
            0x0041 <= code <= 0x005A
            or 0x0061 <= code <= 0x007A
        ):
            has_latin = True

    scripts = sum([
        has_devanagari,
        has_bengali,
        has_latin
    ])

    if scripts > 1:
        return "Mixed_scripts"
    if has_devanagari:
        return "Devanagari"
    if has_bengali:
        return "Bengali_script"
    if has_latin:
        return "Latin_script"
    return "Other_or_symbols"

df["script_type"] = df["comment_text"].apply(detect_script)

# Preserve the existing language and stance annotations.
columns = [
    "comment_id",
    "comment_text",
    "confirmed_language",
    "script_type",
    "stance",
    "relevance_status",
    "language_review_status",
    "stance_status",
]

audit = df[columns].copy()
audit.to_csv(output, index=False)

print("=" * 55)
print("TARGET LANGUAGE AND SCRIPT AUDIT")
print("=" * 55)

print("\nRelevant comments:", len(audit))

print("\nWriting script distribution:")
print(audit["script_type"].value_counts())

print("\nConfirmed language distribution:")
print(audit["confirmed_language"].value_counts())

print("\nConfirmed language vs writing script:")
print(pd.crosstab(
    audit["confirmed_language"],
    audit["script_type"]
))

print("\nStance distribution:")
print(audit["stance"].value_counts())

print("\nSaved:", output)
