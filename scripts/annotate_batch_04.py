
import pandas as pd

path = "data/processed/annotation_batch_04.csv"
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
    1: ("Irrelevant", "English", "None", "Generic video praise"),
    2: ("Irrelevant", "Bengali", "None", "Inappropriate personal insult"),
    3: ("Irrelevant", "Bengali", "None", "Asks when the channel will upload again"),
    4: ("Irrelevant", "Bengali", "None", "Generic thanks"),
    5: ("Irrelevant", "Bengali", "None", "Praises the channel's informative content"),
    6: ("Irrelevant", "Bengali", "None", "Requests videos from a particular location"),
    7: ("Irrelevant", "Bengali", "None", "Generic thanks"),
    8: ("Irrelevant", "Bengali", "None", "Praises presentation"),
    9: ("Irrelevant", "Bengali", "None", "Supports the channel"),
    10: ("Irrelevant", "Bengali", "None", "Generic thanks"),
    11: ("Irrelevant", "Bengali", "None", "Thanks for the presentation"),
    12: ("Irrelevant", "Bengali", "None", "Generic praise of the video"),
    13: ("Irrelevant", "English", "None", "Generic thanks"),
    14: ("Irrelevant", "Bengali", "None", "Generic thanks"),
    15: ("Relevant", "Bengali", "Favour", "Says Earth needs to be saved"),
    16: ("Relevant", "Hindi", "Favour", "Criticizes tree cutting and connects forests with cooling India"),
    17: ("Irrelevant", "English", "None", "Generic video praise"),
    18: ("Relevant", "Hindi", "Favour", "Criticizes large-scale tree cutting and environmental hypocrisy"),
    19: ("Irrelevant", "Hindi", "None", "Discusses water pollution from data centres, not the climate claim directly"),
    20: ("Irrelevant", "Hindi", "None", "Unrelated personal message"),
    21: ("Uncertain", "Hindi", "None", "Says the video is edited to frighten people; target of criticism is unclear"),
    22: ("Relevant", "Hindi", "Favour", "Describes environmental crisis, poor air and water quality, and deforestation"),
    23: ("Irrelevant", "Hindi", "None", "Unrelated joke about dates"),
    24: ("Irrelevant", "Hindi", "None", "Praises a newspaper"),
    25: ("Irrelevant", "Hinglish", "None", "Requests exam preparation help"),
    26: ("Irrelevant", "English", "None", "Generic agreement"),
    27: ("Irrelevant", "Hinglish", "None", "Thanks for covering academic chapters"),
    28: ("Irrelevant", "Hinglish", "None", "Requests chapter-wise exam videos"),
    29: ("Irrelevant", "Hinglish", "None", "Requests videos for all textbook chapters"),
    30: ("Irrelevant", "Hinglish", "None", "Requests videos for all chapters"),
    31: ("Irrelevant", "Hinglish", "None", "Requests important exam questions"),
    32: ("Irrelevant", "Hinglish", "None", "Requests videos for multiple academic subjects"),
    33: ("Irrelevant", "Hinglish", "None", "Requests a video about important questions"),
    34: ("Irrelevant", "Hinglish", "None", "Requests a solved previous-year question paper"),
    35: ("Irrelevant", "Hinglish", "None", "Requests exam chapter coverage"),
    36: ("Irrelevant", "Hinglish", "None", "Requests solved question-paper videos"),
    37: ("Irrelevant", "Hinglish", "None", "Mentions an academic course code"),
    38: ("Irrelevant", "Hinglish", "None", "Generic thanks"),
    39: ("Irrelevant", "Hinglish", "None", "Requests videos for postgraduate subjects"),
    40: ("Irrelevant", "Hinglish", "None", "Agrees to a video request"),
    41: ("Irrelevant", "Hinglish", "None", "Asks which study material or book is being used"),
    42: ("Irrelevant", "Hinglish", "None", "Generic agreement"),
    43: ("Irrelevant", "English", "None", "Generic agreement"),
    44: ("Irrelevant", "Hinglish", "None", "Requests solved question-paper videos"),
    45: ("Irrelevant", "Hinglish", "None", "Generic agreement"),
    46: ("Irrelevant", "Hinglish", "None", "Requests academic videos and current-affairs coverage"),
    47: ("Irrelevant", "Hinglish", "None", "Requests question-paper videos"),
    48: ("Irrelevant", "Hinglish", "None", "Requests question and chapter videos"),
    49: ("Irrelevant", "Hinglish", "None", "Generic praise"),
    50: ("Irrelevant", "Hinglish", "None", "Corrects an examination date"),
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

print("Batch 04 annotations saved.")

print("\nRelevance:")
print(df["relevance"].value_counts(dropna=False))

print("\nLanguage:")
print(df["confirmed_language"].value_counts(dropna=False))

print("\nStance:")
print(df["stance"].value_counts(dropna=False))

print("\nOutput:", path)
