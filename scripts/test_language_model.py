import fasttext
from huggingface_hub import hf_hub_download

print("Downloading MIRA-IndicLID model...")

model_path = hf_hub_download(
    repo_id="mira-iitjmu/MIRA-IndicLID",
    filename="mira_indic_lid.ftz"
)

print("Loading model...")
model = fasttext.load_model(model_path)

samples = [
    "जलवायु परिवर्तन एक गंभीर समस्या है",
    "জলবায়ু পরিবর্তন একটি গুরুতর সমস্যা",
    "Jalvayu parivartan ek gambhir samasya hai",
    "Global warming is a serious concern"
]

for sample in samples:
    labels, probabilities = model.predict(sample, k=3)

    print(f"\nText: {sample}")

    for label, probability in zip(labels, probabilities):
        print(f"{label.replace('__label__', '')}: {probability:.4f}")

print("\nMIRA-IndicLID test completed!")
