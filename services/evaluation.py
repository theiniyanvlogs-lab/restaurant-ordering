import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

y_true = []
y_pred = []


def evaluate_chatbot(question, chatbot_answer):

    df = pd.read_csv("evaluation/evaluation_results.csv")

    expected = None

    for _, row in df.iterrows():

        if str(row["Question"]).strip().lower() == question.strip().lower():

            expected = str(row["Expected"]).strip()

            break

    if expected is None:

        expected = ""

    y_true.append(1)

    if expected.lower() == chatbot_answer.strip().lower():

        y_pred.append(1)

    else:

        y_pred.append(0)

    return {

        "expected": expected,

        "accuracy": round(accuracy_score(y_true, y_pred) * 100, 2),

        "precision": round(precision_score(y_true, y_pred, zero_division=0) * 100, 2),

        "recall": round(recall_score(y_true, y_pred, zero_division=0) * 100, 2),

        "f1_score": round(f1_score(y_true, y_pred, zero_division=0) * 100, 2),

        "correct": sum(y_pred),

        "incorrect": len(y_true) - sum(y_pred),

        "total_questions": len(y_true)

    }
