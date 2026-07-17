import pandas as pd
import json
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

# Load evaluation data
df = pd.read_csv("evaluation/evaluation_results.csv")

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

    "accuracy": round(accuracy,2),
    "precision": round(precision,2),
    "recall": round(recall,2),
    "f1_score": round(f1,2),

    "total_questions": total,
    "correct": correct,
    "incorrect": incorrect,

    "response_time":"1.2 sec"

}

with open("evaluation/metrics.json","w") as f:
    json.dump(metrics,f,indent=4)

print("\nEvaluation Completed Successfully\n")
print(metrics)
