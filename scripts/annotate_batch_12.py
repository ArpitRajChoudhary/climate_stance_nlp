import pandas as pd

path = "data/processed/annotation_batch_12.csv"

# Format: (relevance, confirmed_language, stance)
# Provisional labels; review ambiguous comments before final training.

annotations = {
    1:  ("Relevant",   "English",  "Favour"),
    2:  ("Relevant",   "Hinglish", "Favour"),
    3:  ("Relevant",   "Hindi",    "Favour"),
    4:  ("Relevant",   "English",  "Favour"),
    5:  ("Relevant",   "English",  "Favour"),
    6:  ("Relevant",   "Hindi",    "None"),
    7:  ("Relevant",   "Hindi",    "Favour"),
    8:  ("Relevant",   "Hindi",    "Favour"),
    9:  ("Irrelevant", "Hinglish", "None"),
    10: ("Relevant",   "Hinglish", "None"),
    11: ("Relevant",   "Hinglish", "Favour"),
    12: ("Irrelevant", "Hindi",    "None"),
    13: ("Relevant",   "Hinglish", "Favour"),
    14: ("Relevant",   "English",  "Favour"),
    15: ("Uncertain",  "Hinglish", "None"),
    16: ("Relevant",   "English",  "Favour"),
    17: ("Irrelevant", "English",  "None"),
    18: ("Relevant",   "Hinglish", "Favour"),
    19: ("Relevant",   "Hinglish", "Favour"),
    20: ("Relevant",   "English",  "Favour"),
    21: ("Irrelevant", "Hinglish", "None"),
    22: ("Irrelevant", "English",  "None"),
    23: ("Uncertain",  "English",  "None"),
    24: ("Irrelevant", "English",  "None"),
    25: ("Uncertain",  "English",  "None"),
    26: ("Uncertain",  "Hinglish", "None"),
    27: ("Relevant",   "English",  "Favour"),
    28: ("Irrelevant", "Hindi",    "None"),
    29: ("Irrelevant", "Hinglish", "None"),
    30: ("Irrelevant", "English",  "None"),
    31: ("Irrelevant", "English",  "None"),
    32: ("Irrelevant", "Hinglish", "None"),
    33: ("Relevant",   "Hindi",    "Favour"),
    34: ("Irrelevant", "Hinglish", "None"),
    35: ("Relevant",   "Hindi",    "Favour"),
    36: ("Irrelevant", "English",  "None"),
    37: ("Relevant",   "English",  "None"),
    38: ("Relevant",   "Hindi",    "Favour"),
    39: ("Relevant",   "English",  "Favour"),
    40: ("Irrelevant", "Hinglish", "None"),
    41: ("Uncertain",  "English",  "None"),
    42: ("Irrelevant", "Hinglish", "None"),
    43: ("Uncertain",  "English",  "None"),
    44: ("Relevant",   "English",  "Favour"),
    45: ("Uncertain",  "Hindi",    "None"),
    46: ("Relevant",   "English",  "None"),
    47: ("Relevant",   "Hindi",    "Favour"),
    48: ("Relevant",   "Hindi",    "Favour"),
    49: ("Irrelevant", "English",  "None"),
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

print("Batch 12 annotations saved.")
print("\nRelevance:")
print(df["relevance"].value_counts())
print("\nLanguage:")
print(df["confirmed_language"].value_counts())
print("\nStance:")
print(df["stance"].value_counts())
print(f"\nOutput: {path}")
