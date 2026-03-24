from django.contrib import admin
from django.urls import path
from dashboard.views import home, dashboard
from users.views import register, user_login, user_logout, profile
from quizzes.views import category_list, subcategory_list, quiz_settings, start_quiz, generate_ai, quiz_history, leaderboard
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path("quiz/", include("quizzes.urls")),
    path('', home, name='home'),
    path('dashboard/', include('dashboard.urls')),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('quiz/', include('quizzes.urls')),
    path('quiz-settings/<int:subcategory_id>/', quiz_settings, name='quiz_settings'),
    path('start-quiz/', start_quiz, name='start_quiz'),
    path('generate-ai/<int:subcategory_id>/', generate_ai, name='generate_ai'),
    path('history/', quiz_history, name='history'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
