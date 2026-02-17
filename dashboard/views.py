
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
