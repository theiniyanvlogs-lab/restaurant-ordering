from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# Store evaluation history
y_true = []
y_pred = []


def evaluate_chatbot(expected, predicted):

    expected = str(expected).strip().lower()
    predicted = str(predicted).strip().lower()

    y_true.append(1)

    if expected == predicted:
        y_pred.append(1)
    else:
        y_pred.append(0)

    accuracy = accuracy_score(y_true, y_pred) * 100
    precision = precision_score(y_true, y_pred, zero_division=0) * 100
    recall = recall_score(y_true, y_pred, zero_division=0) * 100
    f1 = f1_score(y_true, y_pred, zero_division=0) * 100

    return {
        "accuracy": round(accuracy, 2),
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1_score": round(f1, 2),
        "total_questions": len(y_true),
        "correct": sum(y_pred),
        "incorrect": len(y_true) - sum(y_pred)
    }
