import pandas as pd

input_path = "data/processed/annotation_batch_08.csv"
output_path = "data/processed/annotation_batch_08.csv"

# Each entry: (relevance, confirmed_language, stance)
# These are provisional labels and should be manually reviewed.

annotations = {
    1:  ("Relevant",   "Hinglish", "Favour"),
    2:  ("Relevant",   "Hindi",    "Favour"),
    3:  ("Relevant",   "English",  "Favour"),
    4:  ("Relevant",   "Hindi",    "Favour"),
    5:  ("Irrelevant", "Hindi",    "None"),
    6:  ("Relevant",   "Hinglish", "Favour"),
    7:  ("Relevant",   "Hindi",    "None"),
    8:  ("Irrelevant", "Hinglish", "None"),
    9:  ("Relevant",   "Hinglish", "Favour"),
    10: ("Uncertain",  "Hinglish", "None"),
    11: ("Relevant",   "Uncertain", "Favour"),
    12: ("Relevant",   "Hinglish", "Favour"),
    13: ("Relevant",   "Hindi",    "Favour"),
    14: ("Irrelevant", "English",  "None"),
    15: ("Irrelevant", "English",  "None"),
    16: ("Relevant",   "Hinglish", "Favour"),
    17: ("Irrelevant", "Uncertain", "None"),
    18: ("Relevant",   "Hinglish", "Favour"),
    19: ("Irrelevant", "English",  "None"),
    20: ("Irrelevant", "Hindi",    "None"),
    21: ("Irrelevant", "English",  "None"),
    22: ("Relevant",   "Hinglish", "Favour"),
    23: ("Uncertain",  "Hinglish", "None"),
    24: ("Irrelevant", "Hindi",    "None"),
    25: ("Relevant",   "Hinglish", "Favour"),
    26: ("Irrelevant", "Hindi",    "None"),
    27: ("Uncertain",  "Hindi",    "None"),
    28: ("Relevant",   "English",  "Favour"),
    29: ("Irrelevant", "Uncertain", "None"),
    30: ("Relevant",   "English",  "Against"),
    31: ("Relevant",   "Hinglish", "Favour"),
    32: ("Relevant",   "Hinglish", "Favour"),
    33: ("Relevant",   "Hindi",    "Favour"),
    34: ("Relevant",   "Hindi",    "Favour"),
    35: ("Uncertain",  "Hinglish", "None"),
    36: ("Irrelevant", "Hindi",    "None"),
    37: ("Relevant",   "English",  "Favour"),
    38: ("Relevant",   "Hinglish", "Favour"),
    39: ("Relevant",   "Hinglish", "Favour"),
    40: ("Relevant",   "Hinglish", "Favour"),
    41: ("Relevant",   "Hindi",    "None"),
    42: ("Relevant",   "English",  "None"),
    43: ("Relevant",   "Hinglish", "Favour"),
    44: ("Irrelevant", "Hindi",    "None"),
    45: ("Relevant",   "Hindi",    "Against"),
    46: ("Relevant",   "Hindi",    "Favour"),
    47: ("Uncertain",  "English",  "None"),
    48: ("Irrelevant", "English",  "None"),
    49: ("Uncertain",  "Hinglish", "None"),
    50: ("Irrelevant", "Uncertain", "None"),
}

df = pd.read_csv(input_path, keep_default_na=False)

if len(df) != 50:
    raise ValueError(f"Expected 50 comments, found {len(df)}")

if set(annotations.keys()) != set(range(1, 51)):
    raise ValueError("Annotation entries must cover rows 1 through 50.")

df["relevance"] = [annotations[i][0] for i in range(1, 51)]
df["confirmed_language"] = [annotations[i][1] for i in range(1, 51)]
df["stance"] = [annotations[i][2] for i in range(1, 51)]

df["relevance_status"] = "Provisional"
df["language_review_status"] = "Provisional"
df["stance_status"] = "Provisional"

df.to_csv(output_path, index=False)

print("Batch 08 annotations saved.")
print("\nRelevance:")
print(df["relevance"].value_counts())
print("\nLanguage:")
print(df["confirmed_language"].value_counts())
print("\nStance:")
print(df["stance"].value_counts())
print(f"\nOutput: {output_path}")
