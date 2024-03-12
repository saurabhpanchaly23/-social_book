from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from sqlalchemy import create_engine
from .managers import CustomUserManager
from django.conf import settings
engine = create_engine('postgresql://root:root@localhost/king')

class CustomUser(AbstractBaseUser, PermissionsMixin):
    gender_choice = [
      ("Male", "Male"),
      ("Female", "Female"),
      ("Other","Other")
    ]
    user_choices=[
      ("Auther","Auther"),
      ("Sellers","Sellers")
    ]
    email = models.EmailField(_("email address"), unique=True)
    user_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(choices=gender_choice, max_length=255)
    user_type = models.CharField(choices = user_choices, max_length=50, blank=True,null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)  
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    public_visibility=models.BooleanField(default=True)    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
       
    def __str__(self):
      return self.emai
        
class Book(models.Model):
    user_id = models.IntegerField(null=True)
    title = models.CharField(max_length=100)
    cost=models.IntegerField( blank=True, null=True)  # price of the book
    author = models.CharField(max_length=100)
    file = models.FileField(upload_to='Book/')  # Assuming you want to upload PDF 
    visibility=models.BooleanField(default=True)

    def __str__(self):
        return self.title