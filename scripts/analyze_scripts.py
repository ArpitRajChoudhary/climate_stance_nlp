import pandas as pd
import re

df = pd.read_csv("data/raw/youtube_comments.csv")

def classify_script(text):
    if pd.isna(text) or not str(text).strip():
        return "Empty"

    text = str(text)

    has_devanagari = bool(re.search(r"[\u0900-\u097F]", text))
    has_bengali = bool(re.search(r"[\u0980-\u09FF]", text))
    has_latin = bool(re.search(r"[A-Za-z]", text))

    if has_devanagari and has_bengali:
        return "Mixed Indic scripts"
    if has_devanagari:
        return "Devanagari"
    if has_bengali:
        return "Bengali"
    if has_latin:
        return "Latin / Romanized"
    return "Other"

df["script_type"] = df["comment_text"].apply(classify_script)

print("\n===== SCRIPT DISTRIBUTION =====")
print(df["script_type"].value_counts().to_string())

print("\n===== LATIN SCRIPT SAMPLES =====")
latin = df[df["script_type"] == "Latin / Romanized"]

for i, text in enumerate(latin["comment_text"].dropna().head(30), 1):
    print(f"\n{i}. {text[:250]}")

print("\n===== SEARCH LANGUAGE DISTRIBUTION =====")
print(df["search_language"].value_counts(dropna=False).to_string())

print("\n===== EXISTING LANGUAGE DETECTION =====")
print(df["detected_language"].value_counts(dropna=False).to_string())
