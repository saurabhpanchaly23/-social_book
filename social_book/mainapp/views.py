from django.shortcuts import render, HttpResponse, redirect
from .forms import CustomUserCreationForm, BookUploadForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser, Book
from .models import engine
from sqlalchemy.sql import text
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .decoreator import check_uploaded_books
import random
from django.core.mail import send_mail
from django.conf import settings
from mainapp.emails import *

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            send_otp(request, user.email)
            request.session['email'] = email
            login(request, user)
            return redirect('verify_otp') 
        else:
            messages.success(request, 'Invalid email or password')
            form = CustomUserCreationForm()
    return render(request, 'login.html')

@login_required
def verify_otp(request):
    if request.method == 'POST':
        user_entered_otp = request.POST.get('otp')
        user_entered_otp=int(user_entered_otp)
        seesion_otp=request.session.get('otp')
        seesion_otp=int(seesion_otp)
        email1 = 'saurabhpanchaly23@gmail.com'
        if (seesion_otp == user_entered_otp):
            login_detected(request,email1)
            return redirect('index') 
        else:
            messages.success(request, 'wrong OPT')
    return render(request, 'verify_otp.html')

@check_uploaded_books
def user_logout(request):
    logout(request)
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}!')
            return redirect('login')  # Redirect to login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required(    login_url='login')
def index(request):
    view_books = Book.objects.all()
    return render(request, 'index.html', {'view_books': view_books})

@login_required(login_url='login')
def authors(request):
    authors = CustomUser.objects.filter(public_visibility=True, user_type='Auther')
    return render(request, 'authors.html', {'authors': authors})

@login_required(login_url="login")
def seller(request):
    Seller=CustomUser.objects.filter(public_visibility=True, user_type='Sellers')
    return render(request, 'seller.html', {'Seller': Seller})

@login_required()
def upload_book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            if request.user.is_authenticated:
                book.user_id = request.user.id
            book.save()
            messages.success(request, 'Book uploaded successfully!')
            return redirect('upload_book')  # Redirect to a success URL
    else:
        form = BookUploadForm()
    return render(request, 'upload_book.html', {'form': form})
    
@login_required(login_url="login")
def view_book(request):
    view_books = Book.objects.all()
    return render(request, 'view_book.html', {'view_books': view_books})
    
@login_required()
@check_uploaded_books
def view_user_books(request):
    view_books = Book.objects.filter(visibility=True,user_id=request.user.id)    
    return render(request, 'view_user_books.html', { 'view_books': view_books})

@login_required(login_url="login")
def fetch_data(request):
    with engine.connect() as connection:
        sql_query = text("SELECT * FROM public.mainapp_book")
        result = connection.execute(sql_query)
        view_books = result.fetchall()
    return render(request, 'engine_data.html', {'view_books': view_books})

def logout_view(request):
    logout(request)
    return redirect('login')