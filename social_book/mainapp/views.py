from django.shortcuts import render, HttpResponse, redirect
from .forms import CustomUserCreationForm, BookUploadForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser, Book
from .models import engine
from sqlalchemy.sql import text
from django.shortcuts import redirect
from django.contrib.auth import logout

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
            return redirect('login')  # Redirect to login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def index(request):
    view_books = Book.objects.all()
    return render(request, 'index.html', {'view_books': view_books})


def authors(request):

    authors = CustomUser.objects.filter(public_visibility=True, user_type='Auther')
    return render(request, 'authors.html', {'authors': authors})

def seller(request):
    Seller=CustomUser.objects.filter(public_visibility=True, user_type='Sellers')
    return render(request, 'seller.html', {'Seller': Seller})

def upload_book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_book.html')  # Redirect to view_book
    else:
        form = BookUploadForm()
    return render(request, 'upload_book.html', {'form': form})

def view_book(request):
    view_books = Book.objects.all()
    return render(request, 'view_book.html', {'view_books': view_books})

def view_user_books(request):
    user_id = request.user.id
    view_books = Book.objects.filter(visibility=True, author_id=user_id)
    return render(request, 'view_user_books.html', {'view_books': view_books})

def fetch_data(request):
    with engine.connect() as connection:
        sql_query = text("SELECT * FROM public.mainapp_book")
        result = connection.execute(sql_query)
        view_books = result.fetchall()
    return render(request, 'engine_data.html', {'view_books': view_books})

def logout_view(request):
    logout(request)
    return redirect('index')