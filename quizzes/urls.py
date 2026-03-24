from django.urls import path
from . import views

urlpatterns = [

    # ✅ Category & Subcategory
    path('categories/', views.category_list, name="categories"),
    path('categories/<int:category_id>/', views.subcategory_list, name="subcategories"),

    # ✅ Quiz Setup & AI
    path('quiz-settings/', views.quiz_settings, name="quiz_settings"),
    path('generate/', views.generate_ai, name="generate_ai"),

    # ✅ Quiz Flow
    path('start/', views.start_quiz, name='start_quiz'),
    path("submit-answer/", views.submit_answer, name="submit_answer"),
    path('result/', views.quiz_result, name="quiz_result"),

    # ✅ Dashboard Features
    path('history/', views.quiz_history, name='history'),
    path('incomplete/', views.incomplete_quizzes, name='incomplete'),
    path('resume/<int:attempt_id>/', views.resume_quiz, name='resume_quiz'),
    path('abandon/<int:attempt_id>/', views.abandon_quiz, name='abandon_quiz'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('retake/<int:quiz_id>/', views.retake_quiz, name='retake_quiz'),

]