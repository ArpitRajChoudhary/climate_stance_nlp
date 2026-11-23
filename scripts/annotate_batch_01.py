import pandas as pd

path = "data/processed/annotation_batch_01.csv"
df = pd.read_csv(path)
for column in [
    "relevance",
    "confirmed_language",
    "stance",
    "annotation_notes",
]:
    df[column] = df[column].astype("object")

# Format: relevance, confirmed_language, stance, notes
labels = {
    1: ("Irrelevant", "English", "None", "Personal request to creator"),
    2: ("Irrelevant", "Bengali", "None", "Exam-related comment"),
    3: ("Irrelevant", "Bengali", "None", "Thanks to creator"),
    4: ("Irrelevant", "Bengali", "None", "School-related appreciation"),
    5: ("Irrelevant", "Bengali", "None", "Generic appreciation"),
    6: ("Relevant", "Bengali", "None", "Watching for debate competition"),
    7: ("Irrelevant", "Bengali", "None", "Generic appreciation"),
    8: ("Irrelevant", "Bengali", "None", "Generic appreciation"),
    9: ("Irrelevant", "Bengali", "None", "Generic praise"),
    10: ("Irrelevant", "Bengali", "None", "Generic praise"),
    11: ("Irrelevant", "Uncertain", "None", "Emoji only"),
    12: ("Irrelevant", "English", "None", "Generic thanks"),
    13: ("Irrelevant", "English", "None", "Generic thanks"),
    14: ("Irrelevant", "English", "None", "Generic thanks"),
    15: ("Irrelevant", "Hindi", "None", "Praise for teaching"),
    16: ("Irrelevant", "English", "None", "Generic thanks"),
    17: ("Irrelevant", "Uncertain", "None", "Emoji only"),
    18: ("Irrelevant", "English", "None", "Generic thanks"),
    19: ("Relevant", "English", "None", "Calls the topic important without stating a position"),
    20: ("Irrelevant", "English", "None", "Generic appreciation"),
    21: ("Irrelevant", "English", "None", "Generic thanks"),
    22: ("Irrelevant", "English", "None", "Generic praise"),
    23: ("Irrelevant", "Uncertain", "None", "Emoji only"),
    24: ("Irrelevant", "Hindi", "None", "Requests science category"),
    25: ("Irrelevant", "English", "None", "Generic thanks"),
    26: ("Irrelevant", "Hindi", "None", "Requests Hindi version"),
    27: ("Irrelevant", "Bengali", "None", "Comment about quota and leadership, not climate stance"),
    28: ("Relevant", "Hindi", "Favour", "Expresses concern about melting ocean ice"),
    29: ("Relevant", "Hindi", "Favour", "Concern about destruction of public life and forests"),
    30: ("Uncertain", "Mixed", "None", "Lockdown reference lacks context"),
    31: ("Relevant", "Hindi", "None", "Suggests good actions can prevent harm; stance unclear"),
    32: ("Relevant", "Hindi", "None", "Asks about government decisions"),
    33: ("Relevant", "Mixed", "None", "Ambiguous comment about 50-degree temperature"),
    34: ("Relevant", "English", "None", "Asks who is responsible"),
    35: ("Uncertain", "Uncertain", "None", "Emoji and number only"),
    36: ("Relevant", "Hindi", "Against", "Challenges human responsibility and frames disasters as natural"),
    37: ("Relevant", "Hindi", "None", "Population and natural-disaster comment; stance unclear"),
    38: ("Irrelevant", "English", "None", "Unrelated religious-community reference"),
    39: ("Relevant", "Hindi", "None", "Expresses hopelessness; exact stance unclear"),
    40: ("Irrelevant", "Hindi", "None", "Does not express climate-change stance"),
    41: ("Relevant", "Hindi", "Favour", "Suggests saving the world, though proposed solution is religious"),
    42: ("Relevant", "Hindi", "Favour", "Describes environmental destruction"),
    43: ("Irrelevant", "Hindi", "None", "Unrelated short comment"),
    44: ("Relevant", "Hindi", "Favour", "Advocates planting trees and protecting greenery"),
    45: ("Uncertain", "Hindi", "None", "Bakwaas; target of criticism unclear"),
    46: ("Relevant", "Hindi", "Favour", "Attributes environmental damage to population and forest destruction"),
    47: ("Irrelevant", "Hindi", "None", "Religious greeting"),
    48: ("Relevant", "Hindi", "None", "Religious optimism; climate stance unclear"),
    49: ("Irrelevant", "Uncertain", "None", "Number only"),
    50: ("Uncertain", "Hindi", "None", "Difficult-to-interpret text"),
}

if len(df) != 50:
    raise ValueError(f"Expected 50 rows, found {len(df)}")

for i, (relevance, language, stance, notes) in labels.items():
    idx = i - 1
    df.at[idx, "relevance"] = relevance
    df.at[idx, "confirmed_language"] = language
    df.at[idx, "stance"] = stance
    df.at[idx, "annotation_notes"] = notes
    df.at[idx, "annotation_status"] = "Provisional"

df.to_csv(path, index=False)

print("Batch 01 annotations saved.")
print("\nRelevance:")
print(df["relevance"].value_counts().to_string())

print("\nLanguage:")
print(df["confirmed_language"].value_counts().to_string())

print("\nStance:")
print(df["stance"].value_counts().to_string())

print("\nOutput:", path)
