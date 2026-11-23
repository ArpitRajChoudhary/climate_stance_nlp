
import pandas as pd

path = "data/processed/annotation_batch_07.csv"
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
    1: ("Irrelevant", "Hindi", "None", "Religious greeting"),
    2: ("Irrelevant", "Uncertain", "None", "Thumbs-up emojis only"),
    3: ("Uncertain", "English", "None", "Possibly says Save Earth; text is incomplete"),
    4: ("Irrelevant", "English", "None", "Explains why the user watched the video"),
    5: ("Irrelevant", "Hindi", "None", "Encourages tree planting and wildlife protection without a clear climate reference"),
    6: ("Irrelevant", "Hinglish", "None", "Generic praise of the information"),
    7: ("Relevant", "Hinglish", "Favour", "Attributes environmental problems to humans"),
    8: ("Relevant", "Hindi", "Favour", "Links meat consumption with climate change and greenhouse gases"),
    9: ("Irrelevant", "English", "None", "Thanks the channel"),
    10: ("Irrelevant", "Hinglish", "None", "Praises the channel"),
    11: ("Irrelevant", "English", "None", "Generic praise"),
    12: ("Relevant", "Hindi", "Favour", "Explains how meat production, deforestation and greenhouse gases contribute to warming"),
    13: ("Relevant", "Hinglish", "Favour", "Reports planting trees every year"),
    14: ("Irrelevant", "Uncertain", "None", "Sad emoji only"),
    15: ("Irrelevant", "English", "None", "Generic praise"),
    16: ("Relevant", "English", "Favour", "Encourages saving trees and Earth"),
    17: ("Irrelevant", "Hinglish", "None", "Thanos reference unrelated to a clear climate stance"),
    18: ("Irrelevant", "Hinglish", "None", "Asks which news channel is better"),
    19: ("Relevant", "Hinglish", "Favour", "Expresses concern about rising temperatures and protecting future generations"),
    20: ("Relevant", "Hindi", "Favour", "Suggests higher dairy and beef prices as an environmental measure"),
    21: ("Irrelevant", "Hinglish", "None", "Requests a Punjabi-language video"),
    22: ("Relevant", "Hindi", "Favour", "Expresses concern about rising temperatures and calls for collective action"),
    23: ("Irrelevant", "Hinglish", "None", "Unrelated meme-like response"),
    24: ("Relevant", "Hinglish", "Favour", "Identifies population growth as a major climate-change cause"),
    25: ("Irrelevant", "English", "None", "Praises the channel"),
    26: ("Relevant", "Hinglish", "Favour", "Warns about risks to humanity and encourages saving Earth"),
    27: ("Irrelevant", "English", "None", "Generic video praise"),
    28: ("Relevant", "English", "Favour", "Attributes climate change to capitalist systems; wording is unusual"),
    29: ("Relevant", "Hindi", "Favour", "Attributes climate change to human behaviour and excessive consumption"),
    30: ("Uncertain", "Uncertain", "None", "External video link without an explanatory comment"),
    31: ("Relevant", "Hindi", "Favour", "Argues population control is necessary to reduce environmental pressure and emissions"),
    32: ("Irrelevant", "English", "None", "Generic praise"),
    33: ("Relevant", "Hinglish", "Favour", "Raises methane emissions from household sanitation and asks for solutions"),
    34: ("Relevant", "Hindi", "None", "Agrees that the issue deserves attention; position is not explicit"),
    35: ("Uncertain", "Hinglish", "None", "Says the sooner something ends the better; target is unclear"),
    36: ("Relevant", "Hindi", "Favour", "Expresses concern and reports planting over 1,000 trees"),
    37: ("Relevant", "English", "Favour", "Calls for developed countries to share renewable-energy technology"),
    38: ("Irrelevant", "English", "None", "Generic praise of a climatology video"),
    39: ("Relevant", "Hinglish", "Favour", "Suggests banning cars and air conditioners"),
    40: ("Uncertain", "Hindi", "None", "Discusses rainfall and plants; climate relevance is unclear"),
    41: ("Relevant", "Hinglish", "None", "Asks why the dairy industry's contribution was not discussed"),
    42: ("Relevant", "English", "Favour", "Explicitly calls global warming a very big problem"),
    43: ("Relevant", "Hindi", "Favour", "Advocates limiting childbirth as an environmental measure"),
    44: ("Relevant", "English", "None", "Praises the channel's climate and nature videos without stating a position"),
    45: ("Uncertain", "English", "None", "Single vague word; meaning unclear"),
    46: ("Uncertain", "Uncertain", "None", "External Google Drive link without explanatory text"),
    47: ("Relevant", "Hindi", "Favour", "Argues population control is necessary to protect resources and Earth"),
    48: ("Uncertain", "Uncertain", "None", "External video link without explanatory text"),
    49: ("Relevant", "Marathi", "Favour", "Romanized Marathi; says population growth has damaged nature"),
    50: ("Relevant", "Marathi", "Favour", "Romanized Marathi; says humans are responsible for destroying nature"),
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

print("Batch 07 annotations saved.")

print("\nRelevance:")
print(df["relevance"].value_counts(dropna=False))

print("\nLanguage:")
print(df["confirmed_language"].value_counts(dropna=False))

print("\nStance:")
print(df["stance"].value_counts(dropna=False))

print("\nOutput:", path)
