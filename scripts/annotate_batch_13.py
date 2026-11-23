import pandas as pd

path = "data/processed/annotation_batch_13.csv"

# Format: (relevance, confirmed_language, stance)
# Provisional labels.

annotations = {
    1:  ("Irrelevant", "English",  "None"),
    2:  ("Relevant",   "Hinglish", "Favour"),
    3:  ("Irrelevant", "English",  "None"),
    4:  ("Irrelevant", "Hindi",    "None"),
    5:  ("Irrelevant", "English",  "None"),
    6:  ("Irrelevant", "Hinglish", "None"),
    7:  ("Irrelevant", "English",  "None"),
    8:  ("Relevant",   "English",  "None"),
    9:  ("Uncertain",  "English",  "None"),
    10: ("Irrelevant", "English",  "None"),
    11: ("Irrelevant", "Uncertain", "None"),
}

df = pd.read_csv(path, keep_default_na=False)

if len(df) != 11:
    raise ValueError(f"Expected 11 comments, found {len(df)}")

if set(annotations) != set(range(1, 12)):
    raise ValueError("Annotations must cover rows 1 through 11.")

df["relevance"] = [annotations[i][0] for i in range(1, 12)]
df["confirmed_language"] = [annotations[i][1] for i in range(1, 12)]
df["stance"] = [annotations[i][2] for i in range(1, 12)]

df["relevance_status"] = "Provisional"
df["language_review_status"] = "Provisional"
df["stance_status"] = "Provisional"

df.to_csv(path, index=False)

print("Batch 13 annotations saved.")
print("\nRelevance:")
print(df["relevance"].value_counts())
print("\nLanguage:")
print(df["confirmed_language"].value_counts())
print("\nStance:")
print(df["stance"].value_counts())
print(f"\nOutput: {path}")
