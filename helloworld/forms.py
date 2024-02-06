# forms.py a Django form to handle file uploads
from django import forms
from helloworld.models import Company

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)