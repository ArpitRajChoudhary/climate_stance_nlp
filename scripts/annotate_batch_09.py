import pandas as pd

input_path = "data/processed/annotation_batch_09.csv"

# Format: (relevance, confirmed_language, stance)
# All labels are provisional and should be reviewed.

annotations = {
    1:  ("Uncertain",  "Hinglish", "None"),
    2:  ("Relevant",   "Hinglish", "Favour"),
    3:  ("Relevant",   "Hinglish", "Favour"),
    4:  ("Irrelevant", "Hindi",    "None"),
    5:  ("Relevant",   "Hindi",    "Favour"),
    6:  ("Uncertain",  "Uncertain", "None"),
    7:  ("Relevant",   "Hinglish", "Favour"),
    8:  ("Relevant",   "Hinglish", "Favour"),
    9:  ("Relevant",   "Hindi",    "None"),
    10: ("Relevant",   "Hinglish", "Favour"),
    11: ("Irrelevant", "Hinglish", "None"),
    12: ("Irrelevant", "English",  "None"),
    13: ("Relevant",   "Hindi",    "Favour"),
    14: ("Irrelevant", "Hindi",    "None"),
    15: ("Relevant",   "Hindi",    "Favour"),
    16: ("Relevant",   "English",  "Favour"),
    17: ("Relevant",   "English",  "None"),
    18: ("Relevant",   "Hinglish", "Favour"),
    19: ("Relevant",   "English",  "Against"),
    20: ("Relevant",   "Hinglish", "Favour"),
    21: ("Relevant",   "Hindi",    "Favour"),
    22: ("Irrelevant", "Hinglish", "None"),
    23: ("Irrelevant", "Uncertain", "None"),
    24: ("Relevant",   "Hinglish", "Favour"),
    25: ("Relevant",   "Hinglish", "Favour"),
    26: ("Relevant",   "Hindi",    "Favour"),
    27: ("Irrelevant", "English",  "None"),
    28: ("Irrelevant", "English",  "None"),
    29: ("Relevant",   "English",  "Favour"),
    30: ("Relevant",   "Hindi",    "Favour"),
    31: ("Relevant",   "English",  "Favour"),
    32: ("Uncertain",  "English",  "None"),
    33: ("Relevant",   "Hinglish", "Favour"),
    34: ("Relevant",   "English",  "Favour"),
    35: ("Irrelevant", "English",  "None"),
    36: ("Irrelevant", "English",  "None"),
    37: ("Irrelevant", "English",  "None"),
    38: ("Irrelevant", "Hindi",    "None"),
    39: ("Irrelevant", "English",  "None"),
    40: ("Relevant",   "Hinglish", "None"),
    41: ("Relevant",   "English",  "Favour"),
    42: ("Irrelevant", "Hindi",    "None"),
    43: ("Irrelevant", "English",  "None"),
    44: ("Relevant",   "Hindi",    "Favour"),
    45: ("Uncertain",  "Hindi",    "None"),
    46: ("Relevant",   "Hinglish", "None"),
    47: ("Relevant",   "Hinglish", "Favour"),
    48: ("Irrelevant", "Uncertain", "None"),
    49: ("Relevant",   "Hindi",    "Favour"),
    50: ("Relevant",   "Hinglish", "Favour"),
}

df = pd.read_csv(input_path, keep_default_na=False)

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

df.to_csv(input_path, index=False)

print("Batch 09 annotations saved.")
print("\nRelevance:")
print(df["relevance"].value_counts())
print("\nLanguage:")
print(df["confirmed_language"].value_counts())
print("\nStance:")
print(df["stance"].value_counts())
print(f"\nOutput: {input_path}")
