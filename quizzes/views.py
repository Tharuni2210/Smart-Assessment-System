from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from .models import Category, Subcategory, QuizResult, UserAnswer
from .forms import QuizSettingsForm
from .services.openai_service import generate_quiz_questions, generate_explanation
import requests, random
from .models import QuizAttempt, Quiz
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import Category, Subcategory



def category_list(request):
    categories = Category.objects.all()
    return render(request, "categories.html", {"categories": categories})

def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)

    return render(request, 'subcategories.html', {
        'category': category,
        'subcategories': subcategories
    })

@login_required
def generate_ai(request, subcategory_id):

    difficulty = request.POST.get("difficulty")
    count = int(request.POST.get("question_count"))
    duration = int(request.POST.get("duration"))

    subcategory = Subcategory.objects.get(id=subcategory_id)
    topic = subcategory.name

    questions = generate_quiz_questions(topic, difficulty, count)

    # ✅ HANDLE EMPTY
    if not questions:
        print("No questions generated")
        return redirect("categories")

    # 🔥 CREATE QUIZ (MAIN FIX)
    quiz = Quiz.objects.create(
        user=request.user,
        topic=topic,
        total_questions=len(questions)
    )

    # 🔥 STORE QUIZ ID
    request.session["quiz_id"] = quiz.id

    # ✅ SAVE QUIZ SESSION
    request.session["quiz"] = {
        "questions": questions,
        "current": 0,
        "score": 0,
        "answers": [],
        "end_time": (timezone.now() + timedelta(seconds=duration)).isoformat()
    }

    request.session.modified = True

    return redirect("start_quiz")

def quiz_settings(request, subcategory_id):

    subcategory = Subcategory.objects.get(id=subcategory_id)

    if request.method == "POST":
        form = QuizSettingsForm(request.POST)

        if form.is_valid():

            request.session["quiz_settings"] = {
                "subcategory_id": subcategory.id,
                "subcategory_name": subcategory.name,
                "difficulty": form.cleaned_data["difficulty"],
                "question_count": form.cleaned_data["question_count"],
                "timer_enabled": form.cleaned_data["timer_enabled"],
            }

            return redirect("start_quiz")

    else:
        form = QuizSettingsForm()

    return render(request, "quiz_settings.html", {
        "form": form,
        "subcategory": subcategory
    })


@login_required
def start_quiz(request):

    quiz = request.session.get("quiz")

    if not quiz:
        return redirect("categories")

    index = quiz.get("current", 0)

    # ✅ END CONDITION
    if index >= len(quiz["questions"]):
        return redirect("quiz_result")

    question = quiz["questions"][index]

    return render(request, "quiz.html", {
        "question": question,
        "index": index + 1,
        "total": len(quiz["questions"])
    })

@login_required
def quiz_result(request):

    quiz = request.session.get("quiz")

    print("QUIZ SESSION:", quiz)

    if not quiz:
        return redirect("categories")

    score = quiz.get("score", 0)
    questions = quiz.get("questions", [])
    answers_data = quiz.get("answers", [])

    total = len(questions)

    # ✅ SAFE percentage
    percentage = (score / total) * 100 if total > 0 else 0

    # ✅ SAFE time calculation
    start_time = quiz.get("start_time")
    try:
        if start_time:
            start = timezone.datetime.fromisoformat(start_time)
        else:
            start = timezone.now()
    except:
        start = timezone.now()

    end = timezone.now()
    time_taken = int((end - start).total_seconds())

    # ✅ SAFE DB SAVE
    try:
       result = QuizResult.objects.create(
           user=request.user,
           topic=quiz.get("topic", "General"),   # ✅ VERY IMPORTANT
           score=score,
           total_questions=total
            
         )    
       correct_count = 0
       wrong_count = 0

       for ans in answers_data:

            is_correct = ans.get("selected") == ans.get("correct")

            if is_correct:
                correct_count += 1
            else:
                wrong_count += 1

            UserAnswer.objects.create(
                user=request.user,
                quiz=result,
                question_text=ans.get("question"),
                selected_answer=ans.get("selected"),
                correct_answer=ans.get("correct"),
                is_correct=is_correct,
                explanation=ans.get("explanation", "")
            )

            answers = UserAnswer.objects.filter(quiz=result)

    except Exception as e:
        print("DB ERROR:", e)

        # fallback (no DB)
        correct_count = sum(1 for a in answers_data if a.get("selected") == a.get("correct"))
        wrong_count = total - correct_count
        answers = answers_data
        result = None

    # ✅ clear session safely
    request.session.pop("quiz", None)

    return render(request, "quiz_result.html", {
    "result": result,
    "answers": answers,
    "correct": correct_count,
    "wrong": wrong_count,
    "total": total,
    "percentage": round(percentage, 2),   # ✅ FIX
    "time_taken": time_taken,
    "score": score
})
@login_required

def submit_answer(request):

    quiz = request.session.get("quiz")

    if not quiz:
        return redirect("categories")

    selected = request.POST.get("answer")  # ✅ must match HTML

    if not selected:
        return redirect("start_quiz")

    index = quiz.get("current", 0)
    question = quiz["questions"][index]

    correct = question["correct"]

    # ✅ CHECK CORRECT
    is_correct = selected == correct

    # 🔥 MAP TEXT (for result page)
    options_map = {
        "A": question["option_a"],
        "B": question["option_b"],
        "C": question["option_c"],
        "D": question["option_d"],
    }

    # ✅ SAVE ANSWERS
    quiz["answers"].append({
        "question": question["text"],
        "selected": options_map[selected],
        "correct": options_map[correct],
        "is_correct": is_correct
    })

    # ✅ SCORE
    if is_correct:
        quiz["score"] += 1

    # 🔥 NEXT QUESTION (KEY LINE)
    quiz["current"] = index + 1

    request.session["quiz"] = quiz
    request.session.modified = True

    # ✅ FINISH
    if quiz["current"] >= len(quiz["questions"]):
        return redirect("quiz_result")

    return redirect("start_quiz")
@login_required
def quiz_history(request):
    quizzes = Quiz.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "quiz_history.html", {
        "quizzes": quizzes
    })


def generate_quiz_questions(topic, difficulty, count):

    import requests
    import random
    import html

    category_map = {
        "Physics": 17,
        "Mathematics": 19,
        "Chemistry": 17,
        "English": 10,
        "Movies": 11,
        "Sports": 21,
        "Games": 15,
        "TV Shows": 14,
        "History": 23,
        "Geography": 22,
        "Current Affairs": 9
    }

    category_id = category_map.get(topic, 9)

    url = f"https://opentdb.com/api.php?amount={count}&category={category_id}&difficulty={difficulty.lower()}&type=multiple"

    response = requests.get(url)
    data = response.json()

    questions = []

    if data.get("response_code") != 0:
        return []

    for item in data.get("results", []):

        correct = html.unescape(item.get("correct_answer"))
        incorrect = [html.unescape(i) for i in item.get("incorrect_answers", [])]

        # ✅ SAFETY CHECK
        if len(incorrect) != 3:
            continue

        options = incorrect + [correct]
        random.shuffle(options)

        correct_letter = ["A", "B", "C", "D"][options.index(correct)]

        questions.append({
            "text": html.unescape(item.get("question")),
            "option_a": options[0],
            "option_b": options[1],
            "option_c": options[2],
            "option_d": options[3],
            "correct": correct_letter
        })

    return questions

def incomplete_quizzes(request):
    attempts = QuizAttempt.objects.filter(user=request.user, status='completed')

    labels = [a.updated_at.strftime("%d-%b") for a in attempts]
    scores = [a.score for a in attempts]

    correct = sum([a.score for a in attempts])
    wrong = sum([a.total_questions - a.score for a in attempts])

    incomplete_quizzes = QuizAttempt.objects.filter(user=request.user, status='incomplete')

    return render(request, "dashboard.html", {
      "labels": labels,
      "scores": scores,
      "correct": correct,
      "wrong": wrong,
   })

from .models import Quiz

def resume_quiz(request, attempt_id):

    try:
        quiz = Quiz.objects.get(id=attempt_id, user=request.user)
    except Quiz.DoesNotExist:
        return redirect("history")

    # ✅ Restore quiz session (basic)
    request.session["quiz_id"] = quiz.id

    # ⚠️ You need to reload questions if stored
    # If not stored, just redirect
    return redirect("start_quiz")


def abandon_quiz(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    attempt.status = 'abandoned'
    attempt.save()
    return redirect('dashboard')

def leaderboard(request):

    leaders = (
        QuizResult.objects
        .values('user__username')
        .annotate(avg_score=Avg('score'))
        .order_by('-avg_score')[:10]
    )

    # ✅ ADD MEDALS
    for i, user in enumerate(leaders):
        if i == 0:
            user['medal'] = '🥇 Gold'
        elif i == 1:
            user['medal'] = '🥈 Silver'
        elif i == 2:
            user['medal'] = '🥉 Bronze'
        else:
            user['medal'] = ''

    return render(request, 'leaderboard.html', {
        'leaders': leaders
    })

def retake_quiz(request, quiz_id):

    quiz = Quiz.objects.get(id=quiz_id)

    # reset session
    request.session["quiz"] = {
        "questions": [],  # regenerate later
        "current": 0,
        "score": 0,
        "topic": quiz.topic,
        "answers": []
    }

    return redirect("start_quiz")

from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, QuizAttempt, Category


def category_detail(request, category_id):
    # existing code
    pass


# ✅ PASTE HERE
def submit_quiz(request, category_id):
    if request.method == "POST":

        category = get_object_or_404(Category, id=category_id)
        questions = Question.objects.filter(category=category)

        score = 0
        total = questions.count()

        for q in questions:
            selected = request.POST.get(f"q{q.id}")
            if selected == q.correct_answer:
                score += 1

        percentage = (score / total) * 100 if total > 0 else 0

        QuizAttempt.objects.create(
            user=request.user,
            score=percentage,
            status='completed'
        )

        return redirect('dashboard')