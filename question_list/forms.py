from django import forms
from .models import User, Question, Answer, Tag 

class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(attrs=
    {'rows': 5, 'cols': 120, 'class': "form-control", 'id': "questionBody", 'placeholder': "Type here..."}), 
    max_length=200, label='' )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={ 
        'type':"login", 
        'class':"form-control col-md-6", 
        'id':"userEmail", 
        'aria-describedby':"emailHelp", 
        'placeholder':"Enter username" 
        }), max_length=30, label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 
        'type':"password", 
        'class':"form-control col-md-6", 
        'id':"userEmail", 
        'aria-describedby':"emailHelp", 
        'placeholder':"Enter password" 
        }), max_length=16, label='')
    labels = { 'login': (''), 'password': ('') }
    error_messages = {
        'username': {
            'required': ("Please, enter a username!"),
        },
        'password': {
            'required': ("Please, enter a password!"),
        },
    }

# attrs={'type':"email", 'class':"form-control, col-md-10", 'id':"userEmail", 'aria-describedby':"emailHelp", 'placeholder':"Enter email"}


class EditForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={ 
        'type':"login", 
        'class':"form-control col-md-6", 
        'id':"userEmail", 
        'aria-describedby':"emailHelp", 
        'placeholder':"Enter new username" 
        }), max_length=30, label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 
        'type':"password", 
        'class':"form-control col-md-6", 
        'id':"userEmail", 
        'aria-describedby':"emailHelp", 
        'placeholder':"Enter new password" 
        }), max_length=16, label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 
        'type':"password", 
        'class':"form-control col-md-6", 
        'id':"userEmail", 
        'aria-describedby':"emailHelp", 
        'placeholder':"Repeat new password" 
        }), max_length=16, label='')
    email = forms.CharField(widget=forms.TextInput(attrs={ 
        'type':"email", 
        'class':"form-control col-md-6", 
        'id':"userEmail", 
        'aria-describedby':"emailHelp", 
        'placeholder':"Enter new email" 
        }), max_length=100, label='')
    labels = { 'login': 'Username', 'password': 'Password', 'email': 'Email' }
    error_messages = {
        'username': {
            'required': ("Please, enter a username!"),
        },
        'password': {
            'required': ("Please, enter a password!"),
        },
    }