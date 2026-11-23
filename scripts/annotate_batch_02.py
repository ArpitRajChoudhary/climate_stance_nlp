
import pandas as pd

path = "data/processed/annotation_batch_02.csv"
df = pd.read_csv(path)

# Ensure annotation columns can store text labels.
for column in [
    "relevance",
    "confirmed_language",
    "stance",
    "annotation_notes",
]:
    df[column] = df[column].astype("object")

# Format: relevance, confirmed_language, stance, notes
labels = {
    1: ("Irrelevant", "English", "None", "Generic greeting"),
    2: ("Relevant", "Hindi", "Favour", "Suggests planting trees to reduce pollution"),
    3: ("Uncertain", "Hindi", "None", "Romanized Hindi; meaning unclear"),
    4: ("Relevant", "Hindi", "Favour", "Says it may be too late and Earth faces serious damage"),
    5: ("Irrelevant", "Hindi", "None", "Religious devotional message"),
    6: ("Uncertain", "Hindi", "None", "Political statement; reference is unclear"),
    7: ("Relevant", "Hindi", "None", "Asks that the information be shared with Modi"),
    8: ("Irrelevant", "Uncertain", "None", "Emoji only"),
    9: ("Uncertain", "Hindi", "None", "Meaning unclear"),
    10: ("Relevant", "Hindi", "None", "Discusses Ganga pollution; no clear climate stance"),
    11: ("Relevant", "Hindi", "None", "Asks whether the 1.5 degree threshold has been reached"),
    12: ("Irrelevant", "Uncertain", "None", "Gujarati text and emojis; not clearly climate-related"),
    13: ("Relevant", "Hindi", "None", "Refers to the current situation"),
    14: ("Irrelevant", "Hindi", "None", "Religious greeting"),
    15: ("Relevant", "Hindi", "Favour", "Predicts places will be submerged by the sea"),
    16: ("Uncertain", "Hindi", "None", "Abusive and unclear comparison"),
    17: ("Irrelevant", "Uncertain", "None", "Mostly emojis and unclear text"),
    18: ("Irrelevant", "English", "None", "Religious claim unrelated to climate stance"),
    19: ("Relevant", "Hindi", "Favour", "Criticizes deforestation in the name of development"),
    20: ("Relevant", "Hindi", "Against", "Dismisses the topic as nonsense"),
    21: ("Irrelevant", "English", "None", "Unrelated religious reference"),
    22: ("Irrelevant", "Hindi", "None", "Political criticism without a clear climate reference"),
    23: ("Relevant", "Hindi", "Favour", "Agrees with a warning about humanity's future"),
    24: ("Uncertain", "Hindi", "None", "Too vague to establish relevance or stance"),
    25: ("Relevant", "Hindi", "Favour", "Criticizes giving forests to Adani and encourages action"),
    26: ("Irrelevant", "Hindi", "None", "Religious greeting"),
    27: ("Relevant", "Bengali", "Favour", "Says humanity has very little time left"),
    28: ("Relevant", "Bengali", "Favour", "Explicitly links human activity to warming and serious future risks"),
    29: ("Irrelevant", "Bengali", "None", "Compliments the presenter"),
    30: ("Irrelevant", "Bengali", "None", "Generic video praise"),
    31: ("Relevant", "English", "Favour", "Mentions pollution and deforestation as environmental problems"),
    32: ("Relevant", "Bengali", "Favour", "Attributes the problem to population; accepts that a problem exists"),
    33: ("Irrelevant", "Bengali", "None", "Requests a video about antibodies and antigens"),
    34: ("Irrelevant", "English", "None", "Praises the programme"),
    35: ("Relevant", "Bengali", "Favour", "Expresses helplessness about the situation"),
    36: ("Relevant", "Bengali", "Favour", "Warns about Earth's future and says it must be saved; exact wording partly unclear"),
    37: ("Irrelevant", "Bengali", "None", "Generic praise"),
    38: ("Relevant", "Bengali", "Favour", "Warns of danger and criticizes lack of implementation of solutions"),
    39: ("Relevant", "Bengali", "Favour", "Expresses fear that Earth may no longer be saved"),
    40: ("Irrelevant", "Bengali", "None", "Thanks the presenter"),
    41: ("Irrelevant", "Bengali", "None", "Encouragement to the channel"),
    42: ("Irrelevant", "Bengali", "None", "Generic thanks"),
    43: ("Irrelevant", "Uncertain", "None", "Heart emojis only"),
    44: ("Relevant", "Bengali", "Favour", "Requests research and action to save Earth"),
    45: ("Irrelevant", "English", "None", "Generic thanks"),
    46: ("Irrelevant", "English", "None", "Generic thanks"),
    47: ("Relevant", "Bengali", "None", "Requests more videos on the topic"),
    48: ("Irrelevant", "Bengali", "None", "Personal compliment"),
    49: ("Relevant", "Bengali", "Favour", "Encourages public discussion and action by world leaders"),
    50: ("Relevant", "Bengali", "Favour", "Expresses sadness about Earth's condition"),
}

# Apply annotations.
for row_number, (relevance, language, stance, notes) in labels.items():
    idx = row_number - 1

    df.at[idx, "relevance"] = relevance
    df.at[idx, "confirmed_language"] = language
    df.at[idx, "stance"] = stance
    df.at[idx, "annotation_notes"] = notes
    df.at[idx, "annotation_status"] = "Provisional"

df.to_csv(path, index=False)

print("Batch 02 annotations saved.")

print("\nRelevance:")
print(df["relevance"].value_counts())

print("\nLanguage:")
print(df["confirmed_language"].value_counts())

print("\nStance:")
print(df["stance"].value_counts())

print("\nOutput:", path)
