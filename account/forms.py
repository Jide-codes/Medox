from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from blog.models import  CustomUser

class CustomUserCreationForm(UserCreationForm):
     
     password1 = forms.CharField(label='Password',  widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', }))
     password2 = forms.CharField(label='Enter Password Again',  widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))


     class Meta:
          model = CustomUser
          fields = ('email', 'username' )
          widgets = {
               'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your mail address....'}),
               'username':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Please choose a username '}),
               
          }
