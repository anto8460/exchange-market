from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=320)
    password = forms.CharField(label='Password', max_length=20)
