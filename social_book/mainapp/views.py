from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login
from django.contrib import  messages
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import BookUploadForm

def user_login(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        pwd=request.POST.get('password')
        user = authenticate(request, email=email, password=pwd)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse("Invalid Credentials")
    return render (request, 'Login.html')

def register(request):
    if request.method == 'POST':
        form= CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email=form.cleaned_data['email']
            messages.success(request, f'Account created for {email}!')
            return redirect('login')
    else:
        form= CustomUserCreationForm()
    return render (request, 'register.html', {'form': form})
    
def index(request):
    return render (request,'index.html')  

def authers_sellers(request):
    auther = CustomUser.objects.filter(public_visibility=True, user_type='Auther')
    sellers = CustomUser.objects.filter(public_visibility=True, user_type='Sellers')
    return render(request, 'index.html', {'authors': auther, 'sellers': sellers})

def upload_book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_books')
    else:
        form = BookUploadForm()
    return render(request, 'upload_books.html', {'form': form})