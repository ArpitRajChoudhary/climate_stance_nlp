import pandas as pd
from pathlib import Path

source = Path("data/processed/annotations_all.csv")
output = Path("data/processed/adjudication_overrides.csv")

df = pd.read_csv(source, keep_default_na=False)

comment_ids = [
    "UgySZcaDsE_Nxt7tJQJ4AaABAg",
    "UgzQakML-NQYzPiBTKd4AaABAg"
]

selected = df[df["comment_id"].isin(comment_ids)].copy()

if len(selected) != 2:
    raise ValueError(f"Expected 2 records, found {len(selected)}")

if selected["comment_text"].nunique() != 1:
    raise ValueError("Comments are not identical")

if not (selected["relevance"] == "Relevant").all():
    raise ValueError("Unexpected original relevance labels")

overrides = selected[["comment_id", "relevance", "stance"]].copy()

overrides.rename(columns={
    "relevance": "original_relevance",
    "stance": "original_stance"
}, inplace=True)

overrides["relevance_override"] = "Irrelevant"
overrides["reason"] = (
    "Does not meaningfully discuss the target climate-change claim."
)
overrides["review_status"] = "Proposed_Manual_Adjudication"

overrides.to_csv(output, index=False)

print("Adjudication override file created successfully.")
print("Records:", len(overrides))
print("Saved to:", output)
print("\nOriginal annotation file was not modified.")
