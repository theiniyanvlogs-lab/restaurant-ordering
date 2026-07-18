import json
import re
import pandas as pd

from services.gemini_service import ask_gemini

# ==========================================================
# Global Statistics
# ==========================================================

total_questions = 0
correct_answers = 0


# ==========================================================
# Extract JSON safely from Gemini response
# ==========================================================

def extract_json(text):

    try:
        return json.loads(text)
    except Exception:
        pass

    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return None


# ==========================================================
# Manual Metric Calculation
# ==========================================================

def calculate_metrics():

    global total_questions
    global correct_answers

    incorrect_answers = total_questions - correct_answers

    accuracy = (
        (correct_answers / total_questions) * 100
        if total_questions > 0 else 0
    )

    tp = correct_answers
    fp = incorrect_answers
    fn = incorrect_answers

    precision = (
        (tp / (tp + fp)) * 100
        if (tp + fp) > 0 else 0
    )

    recall = (
        (tp / (tp + fn)) * 100
        if (tp + fn) > 0 else 0
    )

    f1 = (
        (2 * precision * recall) / (precision + recall)
        if (precision + recall) > 0 else 0
    )

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

    # ------------------------------------------------------
    # Read Evaluation Dataset
    # ------------------------------------------------------

    df = pd.read_csv("evaluation/evaluation_results.csv")

    question_bank = ""

    for _, row in df.iterrows():

        question_bank += (
            f"Question: {row['Question']}\n"
            f"Expected: {row['Expected']}\n\n"
        )

    # ------------------------------------------------------
    # Semantic Question Matching
    # ------------------------------------------------------

    matching_prompt = f"""
You are an intelligent evaluator.

Below is the evaluation dataset.

{question_bank}

User Question:
{question}

Find the SINGLE BEST matching question.

Match based on meaning.

Return ONLY JSON.

{{
    "matched_question":"...",
    "expected_answer":"..."
}}

Do not return markdown.

Do not explain anything.
"""

    matching_response = ask_gemini(
        matching_prompt,
        evaluation=True
    )

    expected = ""
    matched_question = ""

    try:

        result = extract_json(matching_response)

        if result:

            matched_question = result.get(
                "matched_question",
                ""
            )

            expected = result.get(
                "expected_answer",
                ""
            )

    except Exception:
        pass

    # ------------------------------------------------------
    # Question not found
    # ------------------------------------------------------

    if expected == "":

        total_questions += 1

        metrics = calculate_metrics()

        metrics["expected"] = "Question not found in evaluation dataset."
        metrics["confidence"] = 0
        metrics["reason"] = "No semantic match found."

        return metrics

    # ------------------------------------------------------
    # Semantic Answer Evaluation
    # ------------------------------------------------------

    evaluation_prompt = f"""
You are an AI evaluator.

Question:
{question}

Matched Question:
{matched_question}

Expected Answer:
{expected}

Chatbot Answer:
{chatbot_answer}

Compare both answers.

Ignore wording differences.

Judge only semantic meaning.

Return ONLY JSON.

{{
    "correct": true,
    "confidence": 95,
    "reason": "Short explanation"
}}

Do not return markdown.

Do not explain anything.
"""

    evaluation_response = ask_gemini(
        evaluation_prompt,
        evaluation=True
    )

    is_correct = False
    confidence = 0
    reason = "Unable to evaluate."

    try:

        result = extract_json(evaluation_response)

        if result:

            is_correct = bool(
                result.get("correct", False)
            )

            confidence = float(
                result.get("confidence", 0)
            )

            reason = result.get(
                "reason",
                ""
            )

    except Exception:
        pass

    # ------------------------------------------------------
    # Update Statistics
    # ------------------------------------------------------

    total_questions += 1

    if is_correct:
        correct_answers += 1

    metrics = calculate_metrics()

    metrics["expected"] = expected
    metrics["matched_question"] = matched_question
    metrics["confidence"] = confidence
    metrics["reason"] = reason

    return metrics
