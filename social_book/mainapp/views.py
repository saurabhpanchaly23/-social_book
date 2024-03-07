from django.shortcuts import render, HttpResponse, redirect
from .forms import CustomUserCreationForm, BookUploadForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser, Book

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index') 
        else:
            return HttpResponse("Invalid email or password.")
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def authors(request):
    # Fetch authors based on certain criteria
    authors = CustomUser.objects.filter(public_visibility=True, user_type='Author')
    return render(request, 'authors.html', {'authors': authors})

def sellers(request):
    # Fetch sellers based on certain criteria
    sellers = CustomUser.objects.filter(public_visibility=True, user_type='Seller')
    return render(request, 'sellers.html', {'sellers': sellers})

def Book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book uploaded successfully!')
            return redirect('Book')
    else:
        form = BookUploadForm()
    return render(request, 'Book.html', {'form': form})

def view_book(request):
    # Fetch books based on certain criteria
    view_books = Book.objects.filter(visibility=True)
    return render(request, 'view_book.html', {'view_books': view_books})