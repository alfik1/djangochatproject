from django import forms
from .models import User,UserProfile
from django.contrib.auth.forms import UserCreationForm  


class RegistrationForm(UserCreationForm):
        
    password1  = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-floating border border-dark',"placeholder":"enter your password"}))
    password2  = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-floating border border-success', 'placeholder': 'Enter your password again'}))

    class Meta:
        model   = User
        fields  =('username', 'email')

        widgets = {
            "username":forms.TextInput(attrs={'class': 'form-control border border-dark', 'placecholder': 'enter your username'}),         
            "email":forms.EmailInput(attrs={'class':'form-control border border-dark','placeholder': 'Enter your email'}),
        }
        
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        user = UserProfile(user=user)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border  form-floating border-dark',"placeholder":"enter your password"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-floating border border-dark',"placeholder":"enter your password"}))
    

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}))

