import pandas as pd

path = "data/processed/annotation_batch_11.csv"

# Format: (relevance, confirmed_language, stance)
# All labels are provisional.

annotations = {
    1:  ("Irrelevant", "English",  "None"),
    2:  ("Irrelevant", "English",  "None"),
    3:  ("Irrelevant", "Bengali",  "None"),
    4:  ("Irrelevant", "Bengali",  "None"),
    5:  ("Irrelevant", "Bengali",  "None"),
    6:  ("Irrelevant", "Bengali",  "None"),
    7:  ("Irrelevant", "Bengali",  "None"),
    8:  ("Irrelevant", "Bengali",  "None"),
    9:  ("Irrelevant", "English",  "None"),
    10: ("Irrelevant", "Bengali",  "None"),
    11: ("Irrelevant", "Uncertain", "None"),
    12: ("Irrelevant", "Uncertain", "None"),
    13: ("Relevant",   "Bengali",  "None"),
    14: ("Irrelevant", "English",  "None"),
    15: ("Irrelevant", "Bengali",  "None"),
    16: ("Irrelevant", "Bengali",  "None"),
    17: ("Irrelevant", "Bengali",  "None"),
    18: ("Irrelevant", "Bengali",  "None"),
    19: ("Irrelevant", "Bengali",  "None"),
    20: ("Irrelevant", "Bengali",  "None"),
    21: ("Irrelevant", "Bengali",  "None"),
    22: ("Irrelevant", "Uncertain", "None"),
    23: ("Irrelevant", "Uncertain", "None"),
    24: ("Irrelevant", "English",  "None"),
    25: ("Irrelevant", "Bengali",  "None"),
    26: ("Irrelevant", "Bengali",  "None"),
    27: ("Irrelevant", "Bengali",  "None"),
    28: ("Irrelevant", "Bengali",  "None"),
    29: ("Irrelevant", "Bengali",  "None"),
    30: ("Irrelevant", "Bengali",  "None"),
    31: ("Irrelevant", "Bengali",  "None"),
    32: ("Irrelevant", "Uncertain", "None"),
    33: ("Irrelevant", "Bengali",  "None"),
    34: ("Relevant",   "Hindi",    "Favour"),
    35: ("Relevant",   "English",  "Favour"),
    36: ("Relevant",   "English",  "Favour"),
    37: ("Uncertain",  "English",  "None"),
    38: ("Relevant",   "English",  "Favour"),
    39: ("Relevant",   "Bengali",  "Favour"),
    40: ("Relevant",   "Bengali",  "Favour"),
    41: ("Relevant",   "English",  "None"),
    42: ("Irrelevant", "English",  "None"),
    43: ("Irrelevant", "English",  "None"),
    44: ("Irrelevant", "Bengali",  "None"),
    45: ("Relevant",   "Bengali",  "None"),
    46: ("Relevant",   "Bengali",  "None"),
    47: ("Uncertain",  "English",  "None"),
    48: ("Relevant",   "Hindi",    "Favour"),
    49: ("Relevant",   "Hinglish", "Favour"),
    50: ("Relevant",   "Hindi",    "Against"),
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

print("Batch 11 annotations saved.")
print("\nRelevance:")
print(df["relevance"].value_counts())
print("\nLanguage:")
print(df["confirmed_language"].value_counts())
print("\nStance:")
print(df["stance"].value_counts())
print(f"\nOutput: {path}")
