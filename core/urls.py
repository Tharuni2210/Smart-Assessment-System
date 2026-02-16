<<<<<<< HEAD
from django.contrib import admin
from django.urls import path
from dashboard.views import home
from users.views import register
from users.views import register, user_login, user_logout
from users.views import profile
from quizzes.views import category_list, subcategory_list
from quizzes.views import quiz_settings, start_quiz
from dashboard.views import dashboard
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),  # ← ADD THIS
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('categories/', category_list, name='categories'),
    path('categories/<int:category_id>/', subcategory_list, name='subcategories'),
    path('quiz-settings/<int:subcategory_id>/', quiz_settings, name='quiz_settings'),
    path('start-quiz/', start_quiz, name='start_quiz'),
]

if settings.DEBUG:
=======
from django.contrib import admin
from django.urls import path
from dashboard.views import home
from users.views import register
from users.views import register, user_login, user_logout
from users.views import profile
from quizzes.views import category_list, subcategory_list
from quizzes.views import quiz_settings, start_quiz
from dashboard.views import dashboard
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),  # ← ADD THIS
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('categories/', category_list, name='categories'),
    path('categories/<int:category_id>/', subcategory_list, name='subcategories'),
    path('quiz-settings/<int:subcategory_id>/', quiz_settings, name='quiz_settings'),
    path('start-quiz/', start_quiz, name='start_quiz'),
]

if settings.DEBUG:
>>>>>>> a86c6a1 (1st commit)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)