## Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
## Models
from .models import Company
from .models import Category
from .models import Solution
from .models import stakeholderGroups
from .models import Stage
from .models import ProductGroup
from .models import ProcessingFocus
from .models import ExtractionType
from .models import PendingCompany

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search by Name'}))

class CompanyForm(forms.ModelForm):

    class Meta:
        model = PendingCompany
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CategoryForm(forms.ModelForm): 

    class Meta:
        model = Category
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SolutionForm(forms.ModelForm): 

    class Meta:
        model = Solution
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class stakeholderGroupsForm(forms.ModelForm): 

    class Meta:
        model = stakeholderGroups
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StageForm(forms.ModelForm): 

    class Meta:
        model = Stage
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProductGroupForm(forms.ModelForm): 

    class Meta:
        model = ProductGroup
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProcessingFocusForm(forms.ModelForm): 

    class Meta:
        model = ProcessingFocus
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ExtractionTypeForm(forms.ModelForm): 

    class Meta:
        model = ExtractionType
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
