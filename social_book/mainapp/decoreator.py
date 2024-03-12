from django.shortcuts import render, redirect
from functools import wraps
from .models import Book

def check_uploaded_books(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_uploaded_books = Book.objects.filter(user_id=request.user.id)
        if user_uploaded_books.exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('upload_book')
    return wrapper
