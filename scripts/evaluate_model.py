import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    matthews_corrcoef,
    cohen_kappa_score,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "data/final/baseline_oof_predictions.csv"
OUTPUT_DIR = PROJECT_DIR / "reports/evaluation"

LABELS = ["Against", "Favour", "None"]


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate stance classification out-of-fold predictions."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="CSV containing true and predicted labels."
    )
    parser.add_argument(
        "--true-column",
        default="stance_final",
        help="Column containing actual labels."
    )
    parser.add_argument(
        "--pred-column",
        default="predicted_stance",
        help="Column containing predicted labels."
    )
    parser.add_argument(
        "--name",
        default="baseline",
        help="Name used for output report files."
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = PROJECT_DIR / input_path

    if not input_path.exists():
        raise FileNotFoundError(f"Prediction file not found: {input_path}")

    # Preserve the literal label "None" rather than treating it as missing.
    df = pd.read_csv(input_path, keep_default_na=False)

    required = [args.true_column, args.pred_column]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )

    df = df[required].copy()
    df[args.true_column] = df[args.true_column].astype(str).str.strip()
    df[args.pred_column] = df[args.pred_column].astype(str).str.strip()

    # Exclude rows with empty labels.
    df = df[
        (df[args.true_column] != "") &
        (df[args.pred_column] != "")
    ]

    if df.empty:
        raise ValueError("No valid prediction rows found.")

    y_true = df[args.true_column]
    y_pred = df[args.pred_column]

    unknown_true = sorted(set(y_true) - set(LABELS))
    unknown_pred = sorted(set(y_pred) - set(LABELS))

    if unknown_true or unknown_pred:
        raise ValueError(
            f"Unexpected labels found.\n"
            f"Actual labels: {unknown_true}\n"
            f"Predicted labels: {unknown_pred}\n"
            f"Expected labels: {LABELS}"
        )

    metrics = {
        "model": args.name,
        "evaluated_samples": len(df),
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(
            y_true, y_pred, labels=LABELS, average="macro", zero_division=0
        ),
        "recall_macro": recall_score(
            y_true, y_pred, labels=LABELS, average="macro", zero_division=0
        ),
        "f1_macro": f1_score(
            y_true, y_pred, labels=LABELS, average="macro", zero_division=0
        ),
        "precision_weighted": precision_score(
            y_true, y_pred, labels=LABELS, average="weighted", zero_division=0
        ),
        "recall_weighted": recall_score(
            y_true, y_pred, labels=LABELS, average="weighted", zero_division=0
        ),
        "f1_weighted": f1_score(
            y_true, y_pred, labels=LABELS, average="weighted", zero_division=0
        ),
        "matthews_correlation_coefficient": matthews_corrcoef(y_true, y_pred),
        "cohen_kappa": cohen_kappa_score(y_true, y_pred, labels=LABELS),
    }

    report = classification_report(
        y_true,
        y_pred,
        labels=LABELS,
        target_names=LABELS,
        output_dict=True,
        zero_division=0,
    )

    report_df = pd.DataFrame(report).transpose()
    matrix = confusion_matrix(y_true, y_pred, labels=LABELS)
    matrix_df = pd.DataFrame(
        matrix,
        index=[f"Actual_{label}" for label in LABELS],
        columns=[f"Predicted_{label}" for label in LABELS],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    metrics_path = OUTPUT_DIR / f"{args.name}_metrics.json"
    report_path = OUTPUT_DIR / f"{args.name}_classification_report.csv"
    matrix_path = OUTPUT_DIR / f"{args.name}_confusion_matrix.csv"

    with open(metrics_path, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)

    report_df.to_csv(report_path)
    matrix_df.to_csv(matrix_path)

    print("\n" + "=" * 55)
    print(f"MODEL EVALUATION: {args.name}")
    print("=" * 55)

    print(f"\nEvaluated samples: {len(df)}")

    print("\n===== OVERALL METRICS =====")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key.replace('_', ' ').title():40s}: {value:.4f} ({value * 100:.2f}%)")
        else:
            print(f"{key.replace('_', ' ').title():40s}: {value}")

    print("\n===== CLASSIFICATION REPORT =====")
    print(classification_report(
        y_true,
        y_pred,
        labels=LABELS,
        target_names=LABELS,
        zero_division=0,
    ))

    print("===== CONFUSION MATRIX =====")
    print(matrix_df.to_string())

    print("\n===== SAVED REPORTS =====")
    print(metrics_path)
    print(report_path)
    print(matrix_path)


if __name__ == "__main__":
    main()
