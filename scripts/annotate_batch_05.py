
import pandas as pd

path = "data/processed/annotation_batch_05.csv"
df = pd.read_csv(path, keep_default_na=False)

for column in [
    "relevance",
    "confirmed_language",
    "stance",
    "annotation_notes",
]:
    df[column] = df[column].astype("object")

# Format: relevance, confirmed_language, stance, notes
labels = {
    1: ("Irrelevant", "Hinglish", "None", "Requests information about important academic topics"),
    2: ("Irrelevant", "English", "None", "Generic acknowledgement"),
    3: ("Irrelevant", "English", "None", "Generic praise"),
    4: ("Irrelevant", "Hinglish", "None", "Agrees with an academic video suggestion"),
    5: ("Irrelevant", "Hinglish", "None", "Asks about completion of academic chapters"),
    6: ("Irrelevant", "Hinglish", "None", "Requests videos about MGPE008 chapters"),
    7: ("Irrelevant", "Hinglish", "None", "Thanks and praises the explanation"),
    8: ("Irrelevant", "Hinglish", "None", "Requests likely examination questions"),
    9: ("Irrelevant", "English", "None", "Requests important questions"),
    10: ("Irrelevant", "Hinglish", "None", "Requests coverage of all academic material"),
    11: ("Irrelevant", "Hinglish", "None", "Requests a previous-year examination video"),
    12: ("Irrelevant", "Hinglish", "None", "Requests an academic chapter upload"),
    13: ("Irrelevant", "English", "None", "Generic thanks"),
    14: ("Irrelevant", "English", "None", "Generic request"),
    15: ("Irrelevant", "English", "None", "Likely typo for thank you; generic thanks"),
    16: ("Irrelevant", "Hinglish", "None", "Requests videos for other academic subjects"),
    17: ("Irrelevant", "English", "None", "Thanks for the video"),
    18: ("Irrelevant", "Hinglish", "None", "Requests examination preparation questions"),
    19: ("Irrelevant", "Hinglish", "None", "Requests a video about important questions"),
    20: ("Irrelevant", "Hinglish", "None", "Requests solved previous-year question papers"),
    21: ("Irrelevant", "Hinglish", "None", "Thanks and requests more academic videos"),
    22: ("Irrelevant", "English", "None", "Generic video praise"),
    23: ("Irrelevant", "English", "None", "Agrees to a video suggestion"),
    24: ("Irrelevant", "Hinglish", "None", "Requests MED 8 examination questions"),
    25: ("Irrelevant", "Hinglish", "None", "Requests MGPE 008 videos"),
    26: ("Irrelevant", "Hinglish", "None", "Requests an academic playlist"),
    27: ("Irrelevant", "English", "None", "Generic thanks"),
    28: ("Irrelevant", "English", "None", "Mentions an academic subject code"),
    29: ("Irrelevant", "Hinglish", "None", "Asks about examination answer length"),
    30: ("Irrelevant", "Hinglish", "None", "Requests academic teaching"),
    31: ("Irrelevant", "Hinglish", "None", "Agrees with an academic video suggestion"),
    32: ("Irrelevant", "Hinglish", "None", "Requests an MGPE010 video"),
    33: ("Irrelevant", "Hinglish", "None", "Generic praise"),
    34: ("Irrelevant", "Hinglish", "None", "Requests important academic topics and chapters"),
    35: ("Irrelevant", "Hinglish", "None", "Requests previous-year question paper links"),
    36: ("Irrelevant", "Hinglish", "None", "Requests urgent examination preparation help"),
    37: ("Irrelevant", "Hinglish", "None", "Incomplete academic-related message"),
    38: ("Irrelevant", "English", "None", "Generic thanks"),
    39: ("Irrelevant", "English", "None", "Praises the educational videos"),
    40: ("Irrelevant", "Hinglish", "None", "Requests academic video assistance"),
    41: ("Irrelevant", "English", "None", "Generic thanks"),
    42: ("Irrelevant", "Hinglish", "None", "Praises teaching and requests selected questions"),
    43: ("Irrelevant", "Hindi", "None", "Brief affirmative response"),
    44: ("Irrelevant", "Hinglish", "None", "Requests important examination questions"),
    45: ("Irrelevant", "Hinglish", "None", "Generic praise"),
    46: ("Irrelevant", "Hinglish", "None", "Requests question-paper videos"),
    47: ("Irrelevant", "English", "None", "Brief affirmative response"),
    48: ("Irrelevant", "Hinglish", "None", "Requests important questions and answers"),
    49: ("Irrelevant", "Hinglish", "None", "Requests examination questions"),
    50: ("Irrelevant", "Hinglish", "None", "Thanks for academic videos"),
}

if len(df) != 50 or len(labels) != len(df):
    raise ValueError("Expected exactly 50 comments and 50 annotations.")

for row_number, (relevance, language, stance, notes) in labels.items():
    idx = row_number - 1

    df.at[idx, "relevance"] = relevance
    df.at[idx, "confirmed_language"] = language
    df.at[idx, "stance"] = stance
    df.at[idx, "annotation_notes"] = notes
    df.at[idx, "annotation_status"] = "Provisional"

df.to_csv(path, index=False)

print("Batch 05 annotations saved.")

print("\nRelevance:")
print(df["relevance"].value_counts(dropna=False))

print("\nLanguage:")
print(df["confirmed_language"].value_counts(dropna=False))

print("\nStance:")
print(df["stance"].value_counts(dropna=False))

print("\nOutput:", path)
