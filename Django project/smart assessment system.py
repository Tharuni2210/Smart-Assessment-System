from django.db import models
from django.contrib.auth.models import User
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings
from django.conf.urls.static import static

# ================= MODELS =================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

# ================= FORMS =================
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

# ================= VIEWS =================
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(**form.cleaned_data)
            Profile.objects.create(user=user)
            login(request,user)
            return redirect('dashboard')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method=="POST":
        user=authenticate(request,
                          username=request.POST['username'],
                          password=request.POST['password'])
        if user:
            login(request,user)
            return redirect('dashboard')
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    categories=Category.objects.all()
    return render(request,'dashboard.html',{'categories':categories})

@login_required
def profile(request):
    profile=Profile.objects.get(user=request.user)
    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
    else:
        form=ProfileForm(instance=profile)
    return render(request,'profile.html',{'form':form,'profile':profile})

@login_required
def subcategories(request,id):
    subs=SubCategory.objects.filter(category_id=id)
    return render(request,'subcategories.html',{'subs':subs})

# ================= URLS =================
urlpatterns=[
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
    path('profile/',profile,name='profile'),
    path('sub/<int:id>/',subcategories,name='sub'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)