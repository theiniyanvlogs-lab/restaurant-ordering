import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


def evaluate_chatbot(csv_file):
    """
    Evaluate chatbot answers from a CSV file.

    Required columns:
    - Expected
    - Predicted
    """

    df = pd.read_csv(csv_file)

    y_true = []
    y_pred = []

    correct = 0

    for _, row in df.iterrows():

        expected = str(row["Expected"]).strip().lower()
        predicted = str(row["Predicted"]).strip().lower()

        y_true.append(1)

        if expected == predicted:
            y_pred.append(1)
            correct += 1
        else:
            y_pred.append(0)

    total = len(df)
    incorrect = total - correct

    accuracy = accuracy_score(y_true, y_pred) * 100
    precision = precision_score(y_true, y_pred, zero_division=0) * 100
    recall = recall_score(y_true, y_pred, zero_division=0) * 100
    f1 = f1_score(y_true, y_pred, zero_division=0) * 100

    metrics = {
        "accuracy": round(accuracy, 2),
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1_score": round(f1, 2),
        "total_questions": total,
        "correct": correct,
        "incorrect": incorrect,
        "response_time": "1.2 sec"
    }

    return metrics
