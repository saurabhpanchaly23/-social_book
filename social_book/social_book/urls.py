"""
URL configuration for social_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainapp import views as mainapp
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.user_login, name='login'),
    path('index/', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('seller/', views.seller, name='seller'),
    path('upload_book/', views.upload_book, name='upload_book'),
    path('view_book/', views.view_book, name='view_book'),
    path('view_user_books/',views.view_user_books, name='view_user_books'),
    path('fetch_data/',views.fetch_data, name='fetch_data'),
    path('logout/', views.logout_view, name='logout'), 
    path('verify_otp/',views.verify_otp, name='verify_otp'),
    #api 
    path('api/', include('api.urls')),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)