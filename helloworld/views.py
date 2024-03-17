## Forms
from .forms import CompanyForm
from .forms import CategoryForm
from .forms import SolutionForm
from .forms import stakeholderGroupsForm
from .forms import StageForm
from .forms import ProductGroupForm
from .forms import ProcessingFocusForm
from .forms import ExtractionTypeForm
from .forms import UserRegisterForm
from .forms import SearchForm
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
## Django 
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.contrib import messages

class CompanyListView(ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'

class CompanyCreateView(CreateView):
    model = Company
    template_name = 'company_form.html'
    fields = ['name', 'industry']
    success_url = '/companies/'  # Redirect to the list view after successful creation

## Root
# path("", views.index, name="index"),

def index(request):
    return render(request, 'home.html')

  
## User Registration
# path('user/register', views.register),

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')

            messages.success(request, 'Account Created')
            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

## Companies
# path('companies/', views.companies, name="companies"),
# path('companies/create/', CompanyCreateView.as_view(), name='company-create'),
# path('companies/<int:id>', views.view_company, name='company-view'),
# path('companies_pending/<int:id>', views.view_company_pending, name='company-view-pending'),
# path('companies_approve/<int:id>', views.view_company_approve, name='company-pending-approve'),
# path('companies_reject/<int:id>', views.view_company_reject, name='company-pending-reject'),
# path('companies/search/', views.companies_filtered, name='company-filtered'),
# path('remove_companies/<int:id>', views.remove_companies),

@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies': companies})

@login_required
def companies(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/companies')  # Redirect to a success page
    else:
        form = CompanyForm()
        searchForm = SearchForm()

    return render(request, 'companies.html', {'form': form, 'companies': companies, 'searchForm': searchForm})

def view_company(request, id):
    company = Company.objects.get(id = id)
    # fields = Company._meta.get_fields()
    obj = model_to_dict(company)

    return render(request, 'company_view.html', {'company': company, 'obj': obj})

def view_company_pending(request, id):
    company = PendingCompany.objects.get(id = id)
    obj = model_to_dict(company)

    return render(request, 'company_view_pending.html', {'company': company, 'obj': obj})

def view_company_approve(request, id):
    company = PendingCompany.objects.get(id = id)
    new_company = Company()
    for field in company._meta.fields:
        if not field.primary_key:
            setattr(new_company, field.name, getattr(company, field.name))
    new_company.save()
    company.delete()

    return redirect('/companies')

def view_company_reject(request, id):
    company = PendingCompany.objects.get(id = id)
    company.delete()

    return redirect('/changes')
    
def company_approve(request, id):
    return

def companies_filtered(request):
    form = SearchForm(request.POST)
    query = form['q']
    companies = Company.objects.filter(Name__contains=query.value())
    
    form = CompanyForm()
    searchForm = SearchForm()
    return render(request, 'companies.html', {'form': form, 'companies': companies, 'searchForm': searchForm, 'query': query.value()})

def remove_companies(request, id):
    company = Company.objects.get(id = id)
    company.delete()
    return redirect('/companies')

## Categories
# path('categories/', views.categories, name="categories"),
# path('remove_categories/<int:id>', views.remove_categories),

@login_required
def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

@login_required
def categories(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/categories')  # Redirect to a success page
    else:
        form = CategoryForm()

    return render(request, 'categories.html', {'form': form, 'categories': categories})

def remove_categories(request, id):
    category = Category.objects.get(id = id)
    category.delete()
    return redirect('/categories')

## Solutions 
# path('solutions/', views.solutions, name="solutions"),
# path('remove_solutions/<int:id>', views.remove_solutions),

@login_required
def solutions(request):
    solutions = Solution.objects.all()
    if request.method == 'POST':
        form = SolutionForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/solutions')  # Redirect to a success page
    else:
        form = SolutionForm()

    return render(request, 'solutions.html', {'form': form, 'solutions': solutions})

def remove_solutions(request, id):
    solution = Solution.objects.get(id = id)
    solution.delete()
    return redirect('/solutions')

## Stakeholder Groups
# path('stakeholder-groups/', views.stakeholderGroups, name="groups"),
# path('remove_groups/<int:id>', views.remove_stakeholder_groups),

@login_required
def StakeholderGroups(request):
    groups = stakeholderGroups.objects.all()
    if request.method == 'POST':
        form = stakeholderGroupsForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/stakeholder-groups')  # Redirect to a success page
    else:
        form = stakeholderGroupsForm()

    return render(request, 'stakeholderGroups.html', {'form': form, 'groups': groups})

def remove_stakeholder_groups(request, id):
    group = stakeholderGroups.objects.get(id = id)
    group.delete()
    return redirect('/stakeholder-groups')

## Stage
# path('stage/', views.stages, name="stages"),
# path('remove_stages/<int:id>', views.remove_stages),

@login_required
def stages(request):
    stages = Stage.objects.all()
    if request.method == 'POST':
        form = StageForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/stages')  # Redirect to a success page
    else:
        form = StageForm()

    return render(request, 'stages.html', {'form': form, 'stages': stages})

def remove_stages(request, id):
    stage = Stage.objects.get(id = id)
    stage.delete()
    return redirect('/stages')

## Product Group
# path('product-groups/', views.productGroups, name="productGroups"),
# path('remove_groups/<int:id>', views.remove_product_groups),

@login_required
def productGroups(request):
    groups = ProductGroup.objects.all()
    if request.method == 'POST':
        form = ProductGroupForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/product-groups')  # Redirect to a success page
    else:
        form = ProductGroupForm()

    return render(request, 'productGroups.html', {'form': form, 'productGroups': groups})

def remove_product_groups(request, id):
    group = ProductGroup.objects.get(id = id)
    group.delete()
    return redirect('/product-groups')

## Processing Focus
# path('processing-focus/', views.processingFocus, name="processingFocus"),
# path('remove_focus/<int:id>', views.remove_processing_focus),

@login_required
def processingFocus(request):
    focus = ProcessingFocus.objects.all()
    if request.method == 'POST':
        form = ProcessingFocusForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/processing-focus')  # Redirect to a success page
    else:
        form = ProcessingFocusForm()

    return render(request, 'processingFocus.html', {'form': form, 'processingFocus': focus})

def remove_processing_focus(request, id):
    focus = ProcessingFocus.objects.get(id = id)
    focus.delete()
    return redirect('/processing-focus')

## Extraction Type
# path('extraction-types/', views.extractionTypes, name="extractionTypes"),
# path('remove_type/<int:id>', views.remove_extraction_type),

@login_required
def extractionTypes(request):
    types = ExtractionType.objects.all()
    if request.method == 'POST':
        form = ExtractionTypeForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/extraction-types')  # Redirect to a success page
    else:
        form = ExtractionTypeForm()

    return render(request, 'extractionTypes.html', {'form': form, 'types': types})

def remove_extraction_type(request, id):
    _type = ExtractionType.objects.get(id = id)
    _type.delete()
    return redirect('/extraction-types')

## Changes
# path('changes/', views.changes),

@login_required
def dbChanges(request):
    changes = PendingCompany.objects.all()
    
    return render(request, 'companies_pending.html', {'companies': changes})
