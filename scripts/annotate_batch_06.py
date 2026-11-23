
import pandas as pd

path = "data/processed/annotation_batch_06.csv"
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
    1: ("Irrelevant", "Hinglish", "None", "Requests previous-year exam preparation advice"),
    2: ("Irrelevant", "Hinglish", "None", "Thanks and praises the explanation"),
    3: ("Irrelevant", "Hinglish", "None", "Asks about availability of a textbook"),
    4: ("Irrelevant", "English", "None", "Requests another academic subject video"),
    5: ("Irrelevant", "English", "None", "Requests important exam questions"),
    6: ("Irrelevant", "Hinglish", "None", "Requests question-related videos"),
    7: ("Irrelevant", "Hinglish", "None", "Requests exam questions"),
    8: ("Irrelevant", "Hinglish", "None", "Requests videos for academic subjects"),
    9: ("Irrelevant", "Hinglish", "None", "Criticizes the presentation style"),
    10: ("Irrelevant", "Hinglish", "None", "Agrees to a video suggestion"),
    11: ("Irrelevant", "Hinglish", "None", "Requests important question-answer videos"),
    12: ("Irrelevant", "Hinglish", "None", "Praises the teaching"),
    13: ("Irrelevant", "English", "None", "Praises the video and requests exam assistance"),
    14: ("Irrelevant", "Hinglish", "None", "Thanks and requests more chapter videos"),
    15: ("Irrelevant", "English", "None", "Praises educational videos"),
    16: ("Irrelevant", "Hinglish", "None", "Thanks for academic exam preparation videos"),
    17: ("Irrelevant", "Hinglish", "None", "Requests an academic subject video"),
    18: ("Irrelevant", "English", "None", "Requests exam questions"),
    19: ("Irrelevant", "Hinglish", "None", "Requests solved previous-year papers"),
    20: ("Relevant", "Hindi", "Favour", "Supports reuse of old vehicles and reducing excessive car sales; environmental argument"),
    21: ("Relevant", "English", "Favour", "Attributes environmental problems to non-vegetarian food consumption"),
    22: ("Relevant", "Hindi", "Favour", "Asks whether planting more trees can help the Earth"),
    23: ("Irrelevant", "Uncertain", "None", "Heart emoji only"),
    24: ("Relevant", "English", "Favour", "Explicitly associates overpopulation with climate crisis"),
    25: ("Relevant", "Hinglish", "Against", "Dismisses the seriousness of the concern and suggests everything is fine"),
    26: ("Uncertain", "Hindi", "None", "Meaning and context unclear"),
    27: ("Relevant", "Hinglish", "None", "Mentions the Industrial Revolution without expressing a clear stance"),
    28: ("Relevant", "Hinglish", "Favour", "Identifies population as the biggest problem"),
    29: ("Irrelevant", "Hinglish", "None", "Generic praise of another channel's explanation"),
    30: ("Uncertain", "Hindi", "None", "Proverb without enough context to establish a climate stance"),
    31: ("Relevant", "Hindi", "None", "Discusses old vehicles, government policy and consumer constraints"),
    32: ("Relevant", "Hinglish", "Favour", "Criticizes pollution and environmental damage caused by bombs and powerful countries"),
    33: ("Irrelevant", "Hindi", "None", "Thanks the presenter for information about nature"),
    34: ("Uncertain", "English", "None", "Asks for correction without identifying the issue"),
    35: ("Relevant", "English", "Favour", "Says the government is more responsible"),
    36: ("Relevant", "English", "Favour", "Supports efforts to save humanity and Earth"),
    37: ("Relevant", "Hindi", "Favour", "Attributes greenhouse-gas emissions and deforestation to mining and meat consumption"),
    38: ("Uncertain", "English", "None", "Refers to the age of the video; meaning unclear"),
    39: ("Relevant", "Hindi", "None", "Challenges the explanation of the greenhouse effect, not necessarily climate change itself"),
    40: ("Relevant", "English", "Against", "Questions the existence or evidence of global warming and the ozone hole"),
    41: ("Uncertain", "Uncertain", "None", "Only a video link; comment meaning unavailable"),
    42: ("Relevant", "Hinglish", "Favour", "Says human existence may be threatened"),
    43: ("Irrelevant", "English", "None", "Generic personal message"),
    44: ("Irrelevant", "English", "None", "Expresses affection for a person"),
    45: ("Relevant", "Hinglish", "Favour", "Explicitly says humans are responsible for global warming"),
    46: ("Relevant", "Hindi", "Favour", "Expresses frustration about people not planting trees"),
    47: ("Relevant", "Hindi", "Favour", "Criticizes focus on small actions while highlighting emissions by wealthy people"),
    48: ("Relevant", "Marathi", "None", "Discusses farming, groundwater extraction and water pollution; no clear climate stance"),
    49: ("Irrelevant", "Uncertain", "None", "Heart emoji only"),
    50: ("Relevant", "Hindi", "Favour", "Describes nature as being close to destruction"),
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

print("Batch 06 annotations saved.")

print("\nRelevance:")
print(df["relevance"].value_counts(dropna=False))

print("\nLanguage:")
print(df["confirmed_language"].value_counts(dropna=False))

print("\nStance:")
print(df["stance"].value_counts(dropna=False))

print("\nOutput:", path)
