from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from .forms import UserForm, UserProfileForm, UserProfile

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        from django.contrib.auth.models import User
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('dashboard')

        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # encrypt password
            user.save()
            messages.success(request, "Registration successful! You can now login.")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
@login_required
def profile(request):

    user = request.user

    # ✅ ensure profile exists
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":

        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, "profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })

