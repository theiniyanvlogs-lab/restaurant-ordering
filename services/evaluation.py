import json
import pandas as pd

from services.gemini_service import ask_gemini

# ==========================================================
# Global Statistics
# ==========================================================

total_questions = 0
correct_answers = 0


# ==========================================================
# Manual Metric Calculation
# ==========================================================

def calculate_metrics():

    global total_questions
    global correct_answers

    incorrect_answers = total_questions - correct_answers

    if total_questions == 0:
        accuracy = 0
    else:
        accuracy = (correct_answers / total_questions) * 100

    # Binary classification (manual)
    tp = correct_answers
    fp = incorrect_answers
    fn = incorrect_answers

    if (tp + fp) == 0:
        precision = 0
    else:
        precision = (tp / (tp + fp)) * 100

    if (tp + fn) == 0:
        recall = 0
    else:
        recall = (tp / (tp + fn)) * 100

    if (precision + recall) == 0:
        f1 = 0
    else:
        f1 = (2 * precision * recall) / (precision + recall)

    return {
        "accuracy": round(accuracy, 2),
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1_score": round(f1, 2),
        "total_questions": total_questions,
        "correct": correct_answers,
        "incorrect": incorrect_answers
    }


# ==========================================================
# Evaluate Chatbot
# ==========================================================

def evaluate_chatbot(question, chatbot_answer):

    global total_questions
    global correct_answers

    # Read Evaluation Dataset
    df = pd.read_csv("evaluation/evaluation_results.csv")

    expected = ""

    # Find matching question
    for _, row in df.iterrows():

        if str(row["Question"]).strip().lower() == question.strip().lower():

            expected = str(row["Expected"]).strip()
            break

    # If no expected answer found
    if expected == "":

        total_questions += 1

        metrics = calculate_metrics()

        metrics["expected"] = "Question not found in evaluation dataset."
        metrics["confidence"] = 0
        metrics["reason"] = "No matching question found."

        return metrics

    # ======================================================
    # Gemini Semantic Evaluation
    # ======================================================

    evaluation_prompt = f"""
You are an AI evaluator.

Question:
{question}

Expected Answer:
{expected}

Chatbot Answer:
{chatbot_answer}

Compare the chatbot answer with the expected answer.

Judge semantic meaning.

Ignore wording differences.

If both answers mean the same thing,
return correct=true.

Return ONLY valid JSON.

{{
    "correct": true,
    "confidence": 95,
    "reason": "Short explanation"
}}
"""

    response = ask_gemini(
    evaluation_prompt,
    evaluation=True
)

    try:

        result = json.loads(response)

        is_correct = bool(result.get("correct", False))
        confidence = float(result.get("confidence", 0))
        reason = result.get("reason", "")

    except Exception:

        is_correct = False
        confidence = 0
        reason = "Unable to evaluate."

    # Update Statistics

    total_questions += 1

    if is_correct:
        correct_answers += 1

    metrics = calculate_metrics()

    metrics["expected"] = expected
    metrics["confidence"] = confidence
    metrics["reason"] = reason

    return metrics
