
from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=320)
    password = forms.CharField(label='Password', max_length=20)

class RegisterForm(forms.Form):
    name = forms.CharField(label="Name", max_length=20)
    country = forms.CharField(label="Name", max_length=20)
    username = forms.CharField(label="User Name", max_length=20)
    email = forms.CharField(label='Email', max_length=320)
    password = forms.CharField(label='Password', max_length=20)
    repeat_password = forms.CharField(label='Password', max_length=20)

class CreateItemForm(forms.Form):
    name = forms.CharField(label="Name", max_length=20)
    description = forms.CharField(label="Name", max_length=20)
    image = forms.FileInput()
    check = forms.BooleanField(label="List Item for Free", required=False)