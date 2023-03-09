from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import models
from . models import UserInfo

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass


 
class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('consultantName', 'clientName1','clientName2','clientName3')
        labels={
           'consultantName':'コンサルタントの名前',
           'clientName1':'クライアント1の名前',
           'clientName2':'クライアント2の名前',
           'clientName3':'クライアント3の名前',
           }


