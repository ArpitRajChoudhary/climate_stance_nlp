
import pandas as pd

path = "data/processed/annotation_batch_03.csv"
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
    1: ("Uncertain", "Uncertain", "None", "Single Bengali character; meaning unclear"),
    2: ("Relevant", "Bengali", "None", "States that China produces 25% of greenhouse gases; no explicit stance"),
    3: ("Irrelevant", "Bengali", "None", "Channel subscription and notification promotion"),
    4: ("Irrelevant", "English", "None", "Praises presentation and requests an aviation video"),
    5: ("Relevant", "Bengali", "None", "Expresses sadness after hearing the information"),
    6: ("Irrelevant", "Bengali", "None", "Thanks the presenter"),
    7: ("Irrelevant", "Bengali", "None", "Generic praise"),
    8: ("Irrelevant", "Bengali", "None", "Asks why the channel has not uploaded a new video"),
    9: ("Relevant", "Bengali", "None", "Requests more videos about climate change"),
    10: ("Irrelevant", "Bengali", "None", "Personal insult unrelated to the topic"),
    11: ("Irrelevant", "Bengali", "None", "Praises presentation style"),
    12: ("Uncertain", "Bengali", "None", "Says we cannot protect our home; context is ambiguous"),
    13: ("Irrelevant", "English", "None", "Generic thanks"),
    14: ("Uncertain", "Uncertain", "None", "Garbled English-like text; meaning unclear"),
    15: ("Irrelevant", "Bengali", "None", "Praises the video and presentation"),
    16: ("Irrelevant", "Bengali", "None", "Praises the presenter"),
    17: ("Irrelevant", "Bengali", "None", "Thanks and praises the channel"),
    18: ("Irrelevant", "Bengali", "None", "Generic praise of the report"),
    19: ("Irrelevant", "English", "None", "Generic thanks"),
    20: ("Irrelevant", "Bengali", "None", "Generic praise"),
    21: ("Irrelevant", "Bengali", "None", "Asks about earthquakes"),
    22: ("Irrelevant", "Uncertain", "None", "Heart emojis only"),
    23: ("Relevant", "Bengali", "Favour", "Says the timely video should spread quickly and action should not be delayed"),
    24: ("Irrelevant", "English", "None", "Generic praise"),
    25: ("Irrelevant", "Bengali", "None", "Generic positive reaction"),
    26: ("Relevant", "Bengali", "Favour", "Supports tree planting and environmental action"),
    27: ("Relevant", "Bengali", "None", "Romanized Bengali; asks for arguments on both sides"),
    28: ("Irrelevant", "English", "None", "Generic praise"),
    29: ("Irrelevant", "Bengali", "None", "Requests an alien-related video"),
    30: ("Irrelevant", "Bengali", "None", "Asks about the Solar System series"),
    31: ("Relevant", "Bengali", "Favour", "Says humanity is damaging Earth and may destroy everything through selfish needs"),
    32: ("Irrelevant", "Uncertain", "None", "Heart emojis only"),
    33: ("Irrelevant", "Bengali", "None", "Requests a video about black holes and thanks the team"),
    34: ("Relevant", "Bengali", "Favour", "Expresses concern for the survival of other species"),
    35: ("Uncertain", "Uncertain", "None", "Only the number 25"),
    36: ("Irrelevant", "English", "None", "Generic thanks"),
    37: ("Relevant", "Bengali", "None", "Requests a video about the impacts of climate change"),
    38: ("Irrelevant", "Bengali", "None", "Generic praise"),
    39: ("Relevant", "Bengali", "Favour", "Romanized Bengali; refers to Amazon rainforest fires and Earth's lungs"),
    40: ("Irrelevant", "Bengali", "None", "Discusses depletion of energy resources, not climate change directly"),
    41: ("Relevant", "Bengali", "Favour", "Blames human greed and exploitation for Earth's condition"),
    42: ("Irrelevant", "English", "None", "Generic thanks"),
    43: ("Irrelevant", "Bengali", "None", "Praises the channel"),
    44: ("Relevant", "Bengali", "Favour", "Says the video raises awareness and encourages sharing and climate education"),
    45: ("Irrelevant", "English", "None", "Video timestamp comment"),
    46: ("Irrelevant", "Bengali", "None", "Negative opinion about the channel without a climate stance"),
    47: ("Irrelevant", "Bengali", "None", "Requests a video about cloning"),
    48: ("Irrelevant", "Bengali", "None", "Praises presentation"),
    49: ("Irrelevant", "Bengali", "None", "Generic praise"),
    50: ("Irrelevant", "Bengali", "None", "Criticizes the discussion format, not the climate claim"),
}

if len(df) != 50 or len(labels) != len(df):
    raise ValueError("Expected exactly 50 comments and 50 annotations.")

# Apply annotations.
for row_number, (relevance, language, stance, notes) in labels.items():
    idx = row_number - 1

    df.at[idx, "relevance"] = relevance
    df.at[idx, "confirmed_language"] = language
    df.at[idx, "stance"] = stance
    df.at[idx, "annotation_notes"] = notes
    df.at[idx, "annotation_status"] = "Provisional"

df.to_csv(path, index=False)

print("Batch 03 annotations saved.")

print("\nRelevance:")
print(df["relevance"].value_counts())

print("\nLanguage:")
print(df["confirmed_language"].value_counts())

print("\nStance:")
print(df["stance"].value_counts())

print("\nOutput:", path)
