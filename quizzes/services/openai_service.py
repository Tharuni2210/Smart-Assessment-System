import os
from openai import OpenAI
import requests
import random

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CATEGORY_MAP = {
    "movies": 50,
    "tv shows": 50,
    "games": 50,
    "sports": 50,
    "history": 50,
    "geography": 50,
    "physics": 50,
    "chemistry": 50,
    "english": 50,
    "maths": 50,
    "currentaffairs": 50
}


def generate_quiz_questions(topic, difficulty, count):

    print("Generating quiz for:", topic)

    url = f"https://opentdb.com/api.php?amount={count}&type=multiple"

    response = requests.get(url)

    data = response.json()

    print("API RESPONSE:", data)

    questions = []

    if data["response_code"] != 0:
        return questions

    for item in data["results"]:

        options = item["incorrect_answers"]
        options.append(item["correct_answer"])

        random.shuffle(options)

        questions.append({
            "question": item["question"],
            "options": options,
            "correct_answer": item["correct_answer"]
        })

    return questions
    
def generate_explanation(question, correct_answer):
    try:
        return (
            f"The correct answer is '{correct_answer}' because it directly addresses the question: "
            f"'{question}'. This option is accurate based on the concept involved, while the other "
            f"options do not correctly satisfy the requirement of the question."
        )
    except Exception:
        return f"The correct answer is '{correct_answer}'."