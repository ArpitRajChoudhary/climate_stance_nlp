import fasttext
from langdetect import detect, detect_langs, DetectorFactory
from huggingface_hub import hf_hub_download

DetectorFactory.seed = 42

model_path = hf_hub_download(
    repo_id="mira-iitjmu/MIRA-IndicLID",
    filename="mira_indic_lid.ftz"
)
model = fasttext.load_model(model_path)

samples = [
    "Global warming is a serious concern",
    "Climate change is affecting our planet",
    "Jalvayu parivartan ek gambhir samasya hai",
    "India mein global warming ka asar dikh raha hai",
    "Mujhe lagta hai climate change bahut serious hai",
    "This is completely false",
    "जलवायु परिवर्तन एक गंभीर समस्या है",
    "জলবায়ু পরিবর্তন একটি গুরুতর সমস্যা",
]

for text in samples:
    labels, probabilities = model.predict(text, k=3)

    try:
        lang = str(detect_langs(text))
    except Exception:
        lang = "Unable to detect"

    print("\nText:", text)
    print("MIRA:", [
        (label.replace("__label__", ""), round(float(prob), 4))
        for label, prob in zip(labels, probabilities)
    ])
    print("Langdetect:", lang)
