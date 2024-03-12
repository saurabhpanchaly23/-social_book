from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import  forms   
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .models import Book
class CustomUserCreationForm(forms.ModelForm):
    
    gender_choice = [
      ("Male", "Male"),
      ("Female", "Female"),
      ("Other","Other"),
    ]
    gender = forms.ChoiceField(
        choices = gender_choice,
        widget=forms.Select(attrs={
            'class':'form-control'
        })
    )
    user_choices=[
      ("Auther","Auther"),
      ("Sellers","Sellers")
    ] 
    user_type = forms.ChoiceField(
        choices = user_choices,
        widget=forms.Select(attrs={
            'class':'form-control'
        })
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'user_name', 'full_name', 'gender', 'user_type', 'city', 'state', 'password', 'public_visibility', ]
        widgets = {
            'password': forms.PasswordInput(),
            'public_visibility':forms.CheckboxInput(attrs={'class':'form-check-input'}),   
   
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'cost', 'author', 'file', 'visibility']
        
        
    # def clean_user_name(self):
    #     user_name = self.cleaned_data.get('user_name')
    #     if len(user_name) < 3:
    #         raise forms.ValidationError('Username must be at least 3 characters long.')
    #     return user_name

    # def check_pasword(self):
    #     password = self.cleaned_data.get('password')
    #     if len(password) < 8:
    #         raise forms.ValidationError('password must be at least 8 characters long.')
    #     return password

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user