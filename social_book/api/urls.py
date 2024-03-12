from django.contrib import admin
from django.urls import path,include
from .views import RegisterView
from .views import  LoginView, UserView, BookView, BookUploadAPIView,BookListView,LogoutView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('books/', BookView.as_view()),
    path('upload/', BookUploadAPIView.as_view(), name='book-upload'),
    
    path('books/', BookListView.as_view()),
    path('logout/', LogoutView.as_view()),
    
]
