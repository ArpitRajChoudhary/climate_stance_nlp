import joblib
import pandas as pd

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)

DATA = Path("data/final/climate_stance_dataset.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

CLASSES = ["Against", "Favour", "None"]

# Load dataset without treating the literal label "None" as missing.
df = pd.read_csv(DATA, keep_default_na=False)

df = df[
    df["stance"].isin(CLASSES)
    & df["comment_text"].str.strip().ne("")
].copy()

df["model_text"] = (
    "[LANG_" + df["language"] + "] " + df["comment_text"]
)

X = df["model_text"]
y = df["stance"]
groups = df["video_id"]

print("========== BASELINE MODEL ==========")
print("Comments:", len(df))
print("Videos:", groups.nunique())

print("\nClass distribution:")
print(y.value_counts())

groups_per_class = {
    label: groups[y == label].nunique()
    for label in CLASSES
}

print("\nVideos containing each class:")
print(groups_per_class)

n_splits = min(5, min(groups_per_class.values()))

if n_splits < 2:
    raise ValueError(
        "A stance class occurs in fewer than two videos. "
        "Video-grouped cross-validation is not reliable."
    )

print(f"\nUsing {n_splits}-fold grouped cross-validation.")

def make_model():
    features = FeatureUnion([
        ("word", TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            max_features=30000,
            sublinear_tf=True
        )),
        ("character", TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5),
            max_features=50000,
            sublinear_tf=True
        ))
    ])

    return Pipeline([
        ("features", features),
        ("classifier", LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            C=1.0,
            random_state=42
        ))
    ])

cv = StratifiedGroupKFold(
    n_splits=n_splits,
    shuffle=True,
    random_state=42
)

predictions = pd.Series("", index=df.index, dtype=str)
fold_results = []

for fold, (train_idx, test_idx) in enumerate(
    cv.split(X, y, groups), start=1
):
    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    model = make_model()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    predictions.iloc[test_idx] = y_pred

    accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(
        y_test,
        y_pred,
        labels=CLASSES,
        average="macro",
        zero_division=0
    )

    fold_results.append({
        "fold": fold,
        "train_videos": groups.iloc[train_idx].nunique(),
        "test_videos": groups.iloc[test_idx].nunique(),
        "test_comments": len(test_idx),
        "accuracy": accuracy,
        "macro_f1": macro_f1
    })

    print(
        f"\nFold {fold}: "
        f"Accuracy={accuracy:.4f}, "
        f"Macro F1={macro_f1:.4f}, "
        f"Test comments={len(test_idx)}"
    )

results = pd.DataFrame(fold_results)

print("\n========== CROSS-VALIDATION RESULTS ==========")
print(results.to_string(index=False))

print("\nMean Accuracy:", round(results["accuracy"].mean(), 4))
print("Mean Macro F1:", round(results["macro_f1"].mean(), 4))

print("\n========== CLASSIFICATION REPORT ==========")
print(classification_report(
    y,
    predictions,
    labels=CLASSES,
    zero_division=0
))

print("========== CONFUSION MATRIX ==========")
print(pd.DataFrame(
    confusion_matrix(y, predictions, labels=CLASSES),
    index=CLASSES,
    columns=CLASSES
))

# Save out-of-fold predictions.
output = df[
    ["comment_id", "video_id", "language", "stance"]
].copy()

output["predicted_stance"] = predictions.values

output.to_csv(
    "data/final/baseline_oof_predictions.csv",
    index=False
)

results.to_csv(
    "data/final/baseline_fold_results.csv",
    index=False
)

# Train final model on all available data.
final_model = make_model()
final_model.fit(X, y)

joblib.dump(
    final_model,
    MODEL_DIR / "baseline_tfidf_logreg.joblib"
)

print("\n========== SAVED FILES ==========")
print("models/baseline_tfidf_logreg.joblib")
print("data/final/baseline_oof_predictions.csv")
print("data/final/baseline_fold_results.csv")
