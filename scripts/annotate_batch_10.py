import pandas as pd

path = "data/processed/annotation_batch_10.csv"

# Format: (relevance, confirmed_language, stance)
# Labels are provisional and require review.

annotations = {
    1:  ("Relevant",   "Hinglish", "None"),
    2:  ("Relevant",   "Hinglish", "Favour"),
    3:  ("Relevant",   "Hinglish", "Favour"),
    4:  ("Irrelevant", "Hindi",    "None"),
    5:  ("Relevant",   "Hindi",    "None"),
    6:  ("Relevant",   "Hindi",    "Favour"),
    7:  ("Relevant",   "Hindi",    "None"),
    8:  ("Irrelevant", "English",  "None"),
    9:  ("Relevant",   "Hinglish", "Favour"),
    10: ("Irrelevant", "English",  "None"),
    11: ("Irrelevant", "Uncertain", "None"),
    12: ("Uncertain",  "Uncertain", "None"),
    13: ("Relevant",   "Hindi",    "None"),
    14: ("Uncertain",  "English",  "None"),
    15: ("Uncertain",  "Hindi",    "None"),
    16: ("Relevant",   "Hinglish", "Favour"),
    17: ("Relevant",   "Hinglish", "Favour"),
    18: ("Relevant",   "Hinglish", "Favour"),
    19: ("Relevant",   "English",  "Against"),
    20: ("Irrelevant", "Uncertain", "None"),
    21: ("Uncertain",  "Uncertain", "None"),
    22: ("Irrelevant", "Bengali",  "None"),
    23: ("Irrelevant", "English",  "None"),
    24: ("Irrelevant", "English",  "None"),
    25: ("Irrelevant", "English",  "None"),
    26: ("Irrelevant", "Bengali",  "None"),
    27: ("Irrelevant", "Bengali",  "None"),
    28: ("Irrelevant", "Bengali",  "None"),
    29: ("Irrelevant", "Bengali",  "None"),
    30: ("Irrelevant", "Bengali",  "None"),
    31: ("Irrelevant", "Bengali",  "None"),
    32: ("Irrelevant", "Bengali",  "None"),
    33: ("Irrelevant", "Bengali",  "None"),
    34: ("Irrelevant", "Bengali",  "None"),
    35: ("Irrelevant", "Bengali",  "None"),
    36: ("Irrelevant", "Bengali",  "None"),
    37: ("Irrelevant", "Bengali",  "None"),
    38: ("Irrelevant", "English",  "None"),
    39: ("Irrelevant", "Bengali",  "None"),
    40: ("Irrelevant", "Bengali",  "None"),
    41: ("Irrelevant", "English",  "None"),
    42: ("Irrelevant", "Bengali",  "None"),
    43: ("Irrelevant", "Bengali",  "None"),
    44: ("Irrelevant", "English",  "None"),
    45: ("Irrelevant", "Bengali",  "None"),
    46: ("Irrelevant", "English",  "None"),
    47: ("Irrelevant", "Bengali",  "None"),
    48: ("Irrelevant", "Bengali",  "None"),
    49: ("Irrelevant", "Bengali",  "None"),
    50: ("Irrelevant", "English",  "None"),
}

df = pd.read_csv(path, keep_default_na=False)

if len(df) != 50:
    raise ValueError(f"Expected 50 comments, found {len(df)}")

if set(annotations) != set(range(1, 51)):
    raise ValueError("Annotations must cover rows 1 through 50.")

df["relevance"] = [annotations[i][0] for i in range(1, 51)]
df["confirmed_language"] = [annotations[i][1] for i in range(1, 51)]
df["stance"] = [annotations[i][2] for i in range(1, 51)]

df["relevance_status"] = "Provisional"
df["language_review_status"] = "Provisional"
df["stance_status"] = "Provisional"

df.to_csv(path, index=False)

print("Batch 10 annotations saved.")
print("\nRelevance:")
print(df["relevance"].value_counts())
print("\nLanguage:")
print(df["confirmed_language"].value_counts())
print("\nStance:")
print(df["stance"].value_counts())
print(f"\nOutput: {path}")
