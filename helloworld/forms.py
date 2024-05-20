from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company
from .models import PendingCompany
from .models import Category
from .models import Solution
from .models import stakeholderGroups
from .models import Stage
from .models import ProductGroup
from .models import Grower
from .models import Industry
from .models import Status

class UploadFileForm(forms.Form):
    file = forms.FileField()

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search by Name'}))

class CompanyForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Company
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PendingCompanyForm(forms.ModelForm):
    required_css_class = 'required'
    Solutions = forms.ModelMultipleChoiceField(
            queryset=Solution.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False)
    Category = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False)
    stakeholderGroup = forms.ModelMultipleChoiceField(
            queryset=stakeholderGroups.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False)
    Stage = forms.ModelMultipleChoiceField(
            queryset=Stage.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False)
    productGroup = forms.ModelMultipleChoiceField(
            queryset=ProductGroup.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False)

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

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length = 100)
    username = forms.CharField(max_length = 100)
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password1', 'password2']

class GrowerForm(forms.ModelForm): 

    class Meta:
        model = Grower
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StatusForm(forms.ModelForm): 

    class Meta:
        model = Status
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class IndustryForm(forms.ModelForm): 

    class Meta:
        model = Industry
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)