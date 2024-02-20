# forms.py a Django form to handle file uploads
from django import forms
from helloworld.models import Company
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length = 100)
    username = forms.CharField(max_length = 100)
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password1', 'password2']
