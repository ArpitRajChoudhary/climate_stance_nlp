import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

path = Path("data/processed/romanized_language_review.csv")

if not path.exists():
    raise FileNotFoundError(f"File not found: {path}")

df = pd.read_csv(path, keep_default_na=False)

required_columns = {
    "review_number",
    "verified_language",
    "language_review_decision",
    "comment_text",
    "stance"
}

missing = required_columns - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {missing}")

if len(df) != 104:
    raise ValueError(f"Expected 104 rows, found {len(df)}")

if df["review_number"].duplicated().any():
    raise ValueError("Duplicate review numbers found.")

# Language decisions from our 104-comment review
decisions = {}

def assign(numbers, language):
    for number in numbers:
        if number in decisions:
            raise ValueError(f"Duplicate decision for comment {number}")
        decisions[number] = language

assign([1], "Bengali_Romanized")
assign(range(2, 17), "Hindi_Romanized")
assign([17], "Hindi")
assign([18], "Bengali")
assign([19, 20, 21], "Bengali_Romanized")
assign([22, 23, 24, 25, 26], "Bengali")
assign([27], "Bengali_Romanized")
assign([28, 29], "Bengali")
assign([30], "Bengali_Romanized")
assign([31], "Bengali")
assign([32, 33], "Hindi")
assign(range(34, 39), "Hindi_Romanized")
assign([39], "Hindi")
assign([40, 41], "Hindi_Romanized")
assign([42], "Hindi")
assign([43, 44, 45], "Hindi_Romanized")
assign([46], "Hindi")
assign([47, 48], "Hindi_Romanized")
assign([49], "Hindi")
assign([50], "Hindi_Romanized")
assign([51], "Hindi")
assign([52, 53], "Hindi_Romanized")
assign([54], "Hindi")
assign([55], "Hindi_Romanized")
assign([56], "Hindi")
assign([57, 58, 59], "Hindi_Romanized")
assign([60], "Hindi")
assign(range(61, 66), "Hindi_Romanized")
assign([66], "Hindi_Romanized")
assign([67], "Hindi")
assign([68], "Hindi_Romanized")
assign([69, 70], "Hindi")
assign(range(71, 77), "Hindi_Romanized")
assign([77, 78], "Hindi")
assign([79, 80, 81], "Hindi_Romanized")
assign([82], "Hindi")
assign(range(83, 94), "Hindi_Romanized")
assign([94], "Bengali_Romanized")
assign([95, 96], "Bengali")
assign([97, 98], "Hindi_Romanized")
assign([99], "Hindi")
assign(range(100, 105), "Hindi_Romanized")

expected = set(range(1, 105))

if set(decisions) != expected:
    missing_numbers = sorted(expected - set(decisions))
    extra_numbers = sorted(set(decisions) - expected)
    raise ValueError(
        f"Decision mapping mismatch. Missing: {missing_numbers}; "
        f"Extra: {extra_numbers}"
    )

# Make sure every review number matches exactly one row
for number, language in decisions.items():
    mask = df["review_number"].astype(int) == number
    df.loc[mask, "verified_language"] = language

# Keep these decisions identifiable as assistant-reviewed,
# pending final validation.
df["language_review_decision"] = "AssistantReviewed_PendingValidation"

# Create a timestamped backup before saving
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = path.with_name(
    f"romanized_language_review_backup_{timestamp}.csv"
)
shutil.copy2(path, backup)

# Save updated review file
df.to_csv(path, index=False)

# Reload and verify
check = pd.read_csv(path, keep_default_na=False)

assert len(check) == 104
assert check["verified_language"].ne("").all()
assert check["language_review_decision"].eq(
    "AssistantReviewed_PendingValidation"
).all()

print("\nLANGUAGE REVIEW UPDATE SUCCESSFUL")
print("---------------------------------")
print("Total records:", len(check))
print("Backup created:", backup)
print("\nVerified language distribution:")
print(check["verified_language"].value_counts().to_string())
print("\nDecision status:")
print(check["language_review_decision"].value_counts().to_string())
print("\nOriginal stance column preserved.")
print("Updated file:", path)
