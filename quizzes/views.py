from django.shortcuts import render, get_object_or_404
from .models import Category
from .forms import QuizSettingsForm
from .models import Subcategory
from django.shortcuts import redirect

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()

    return render(request, 'subcategories.html', {
        'category': category,
        'subcategories': subcategories
})

def quiz_settings(request, subcategory_id):
    subcategory = Subcategory.objects.get(id=subcategory_id)

    if request.method == 'POST':
        form = QuizSettingsForm(request.POST)
        if form.is_valid():
            # Store in session
            request.session['quiz_settings'] = {
                'subcategory_id': subcategory.id,
                'subcategory_name': subcategory.name,
                'difficulty': form.cleaned_data['difficulty'],
                'question_count': form.cleaned_data['question_count'],
                'timer_enabled': form.cleaned_data['timer_enabled'],
            }
            return redirect('start_quiz')
    else:
        form = QuizSettingsForm()

    return render(request, 'quiz_settings.html', {
        'form': form,
        'subcategory': subcategory
    })

def start_quiz(request):
    settings = request.session.get('quiz_settings')

    if not settings:
        return redirect('categories')

    return render(request, 'start_quiz.html', {'settings': settings})

