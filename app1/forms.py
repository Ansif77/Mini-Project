from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model =User
        fields=['email','username','password1','password2']


class EmailLoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email= self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')

        user=authenticate(username=email,password=password)
        if not user:
            raise forms.ValidationError('Invalid login details')
        self.user=user
        return self.cleaned_data
    
    def get_user(self):
        return self.user
