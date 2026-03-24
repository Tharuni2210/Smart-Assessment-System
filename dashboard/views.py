<<<<<<< HEAD
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quizzes.models import QuizAttempt, QuizResult
from django.db.models import Avg, Max


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):

    user = request.user

    # ✅ Completed quizzes
    attempts = QuizResult.objects.filter(user=user)

    total_quizzes = attempts.count()
    avg_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
    best_score = attempts.aggregate(Max('score'))['score__max'] or 0

    # ✅ Performance label
    if avg_score >= 80:
        performance = "Excellent"
    elif avg_score >= 60:
        performance = "Good"
    else:
        performance = "Needs Improvement"

    # ✅ Recent quizzes (for bar chart)
    recent = attempts.order_by('-created_at')[:5]

    scores = [(a.score / a.total_questions) * 100 for a in recent]
    labels = [f"Quiz {i+1}" for i in range(len(recent))]

    # ✅ Pie chart data
    correct = sum(a.score for a in attempts)
    total_questions = sum(a.total_questions for a in attempts)
    wrong = total_questions - correct
   
    # ✅ Incomplete quizzes
    incomplete = QuizAttempt.objects.filter(user=user, status='in_progress')

    return render(request, 'dashboard.html', {
        'total_quizzes': total_quizzes,
        'avg_score': round(avg_score, 2),
        'best_score': best_score,
        'performance': performance,
        'scores': scores[::-1],
        'labels': labels[::-1],
        'correct': correct,
        'wrong': wrong,
        'incomplete': incomplete
    })
=======

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from quizzes.models import Category

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    from quizzes.models import Category
    categories = Category.objects.all()

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from quizzes.models import Category

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    from quizzes.models import Category
    categories = Category.objects.all()

    return render(request, 'dashboard.html', {'categories': categories})
>>>>>>> 9ef381430e7e615d936ccef98338886139338377
