## Forms
from .forms import PendingCompanyForm
from .forms import CategoryForm
from .forms import SolutionForm
from .forms import stakeholderGroupsForm
from .forms import StageForm
from .forms import ProductGroupForm
from .forms import UserRegisterForm
from .forms import SearchForm
from .forms import GrowerForm
from .forms import IndustryForm
from .forms import StatusForm
## Models
from .models import Company
from .models import PendingCompany
from .models import Category
from .models import Solution
from .models import stakeholderGroups
from .models import Stage
from .models import ProductGroup
from .models import PendingChanges
from .models import Grower
from .models import Industry
from .models import Status
## Django 
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.contrib import messages
from django.http import HttpResponse

import csv

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

## About
# path("about/", views.about)

def about(request):
    return render(request, 'about.html')

## Contribute
# path("contribute/", views.contribute)

def contribute(request):
    return render(request, 'contribute.html')
  
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
# path('export/', views.export_companies, name='export-companies'),

@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies': companies})

@login_required
def companies(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        form = PendingCompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            messages.info(request, 'Company successfully submitted')
            PendingChanges.objects.create(companyId=company.id, changeType='create')
            return redirect('/companies')  # Redirect to a success page
    else:
        form = PendingCompanyForm()
        searchForm = SearchForm()

    return render(request, 'companies.html', {'form': form, 'companies': companies, 'searchForm': searchForm})

@login_required
def edit_company(request, id):
    company = Company.objects.get(id = id)
    form = PendingCompanyForm(request.POST, instance=company)
    if request.POST and form.is_valid():
        company_edit = form.save(commit=False)
        new_company = PendingCompany()
        for field in new_company._meta.fields:
            if not field.primary_key:
                setattr(new_company, field.name, getattr(company_edit, field.name))
        new_company.save()
        messages.info(request, 'Company successfully edited')
        PendingChanges.objects.create(companyId=new_company.id, changeType='edit', editId=company.id)
        return redirect('/companies')  # Redirect to a success page
    else: 
        form = PendingCompanyForm(instance=company)

    return render(request, 'edit_companies.html', {'form': form, 'company': company})

def view_company(request, id):
    company = Company.objects.get(id = id)
    # fields = Company._meta.get_fields()
    obj = model_to_dict(company)

    return render(request, 'company_view.html', {'company': company, 'obj': obj})

def view_company_pending(request, changeType, id):
    if changeType == 'deletion':
        company = Company.objects.get(id = id)
    if changeType == 'create' or changeType == 'edit':
        company = PendingCompany.objects.get(id = id)    
    obj = model_to_dict(company)
        
    return render(request, 'company_view_pending.html', {'company': company, 'obj': obj, 'changeType': changeType})

def view_company_approve(_, changeType, id):
    if changeType == 'deletion':
        # Delete Company and Change
        company = Company.objects.get(id = id)
        company.delete()
        change = PendingChanges.objects.get(companyId = id, changeType = changeType)
        change.delete()

        return redirect('/companies')
    
    pendingCompany = PendingCompany.objects.get(id = id)
    change = PendingChanges.objects.get(companyId = id, changeType = changeType)
    if changeType == 'create':
        # Create new Company, copy over fields
        new_company = Company()
        for field in pendingCompany._meta.fields:
            if not field.primary_key:
                setattr(new_company, field.name, getattr(pendingCompany, field.name))
        new_company.save()
    if changeType == 'edit':
        # Find company to edit, copy over fields
        company = Company.objects.get(id = change.editId)
        for field in pendingCompany._meta.fields:
            if not field.primary_key:
                setattr(company, field.name, getattr(pendingCompany, field.name))
        company.save()

    # Delete change and pending company
    change.delete()
    pendingCompany.delete()

    return redirect('/companies')

def view_company_reject(_, changeType, id):
    change = PendingChanges.objects.get(companyId = id, changeType = changeType)
    if changeType == 'create' or changeType == 'edit':
        company = PendingCompany.objects.get(id=id)
        company.delete()
    change.delete()

    return redirect('/changes')

def companies_filtered(request):
    form = SearchForm(request.POST)
    query = form['q']
    companies = Company.objects.filter(Name__contains=query.value())
    
    form = PendingCompanyForm()
    searchForm = SearchForm()
    return render(request, 'companies.html', {'form': form, 'companies': companies, 'searchForm': searchForm, 'query': query.value()})

def remove_companies(request, id):
    # Add deletion to pending changes
    PendingChanges.objects.create(companyId=id, changeType='deletion')
    messages.info(request, 'Deletion of Company requested')
    return redirect('/companies')

def export_companies(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="companies.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.Company.')[1] for field in Company._meta.fields])

    companies = Company.objects.all().values_list()
    for company in companies:
        writer.writerow(company)

    return response

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

## Status
# path('status/', views.status, name="status"),
# path('remove_status/<int:id>', views.remove_status),

@login_required
def status_list(request):
    status = Status.objects.all()
    return render(request, 'status.html', {'status': status})

@login_required
def status(request):
    status = Status.objects.all()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/status')  # Redirect to a success page
    else:
        form = StatusForm()

    return render(request, 'status.html', {'form': form, 'status': status})

def remove_status(_, id):
    status = Status.objects.get(id = id)
    status.delete()
    return redirect('/status')

## Grower
# path('grower/', views.grower, name="grower"),
# path('remove_grower/<int:id>', views.remove_grower),

@login_required
def grower_list(request):
    growers = Grower.objects.all()
    return render(request, 'grower.html', {'growers': growers})

@login_required
def grower(request):
    growers = Grower.objects.all()
    if request.method == 'POST':
        form = GrowerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/grower')  # Redirect to a success page
    else:
        form = GrowerForm()

    return render(request, 'grower.html', {'form': form, 'growers': growers})

def remove_grower(_, id):
    grower = Grower.objects.get(id = id)
    grower.delete()
    return redirect('/grower')

## Industry
# path('industry/', views.industry, name="industry"),
# path('remove_industry/<int:id>', views.remove_industry),

@login_required
def industry_list(request):
    industries = Industry.objects.all()
    return render(request, 'industry.html', {'industries': industries})

@login_required
def industry(request):
    industries = Industry.objects.all()
    if request.method == 'POST':
        form = IndustryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/industry')  # Redirect to a success page
    else:
        form = IndustryForm()

    return render(request, 'industry.html', {'form': form, 'industries': industries})

def remove_industry(_, id):
    industry = Industry.objects.get(id = id)
    industry.delete()
    return redirect('/industry')

## Changes
# path('changes/', views.changes),

@login_required
def dbChanges(request):
    changes = PendingChanges.objects.all()
    
    return render(request, 'companies_pending.html', {'changes': changes})
