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
from .forms import FilterStatusForm
from .forms import FilterIndustryForm
from .forms import FilterCategoryForm
from .forms import FilterStakeholderGroupForm
from .forms import FilterStageForm
from .forms import FilterProductGroupForm
from .forms import FilterSolutionForm
from .forms import ResourceForm
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
from .models import Resources
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.forms.models import model_to_dict
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
import csv

PAGE_INDEX=['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def index(request: HttpRequest) -> HttpResponse:
    """
    Root path. Renders home page template

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing home page template
    """
    articles = Resources.objects.filter(type="article").all()
    title = Resources.objects.filter(type="home_title").first()
    home_text = Resources.objects.filter(type="home_text").first()

    return render(request, 'home.html', {'articles': articles, 'title': title.title, 'home_text': home_text.text })

def about(request: HttpRequest) -> HttpResponse:
    """
    Renders about page template

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing about page template
    """
    about = Resources.objects.filter(type="about").first()

    return render(request, 'about.html', {'about': about.text})

def contribute(request: HttpRequest) -> HttpResponse:
    """
    Renders contribute page template

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing contribute page template
    """
    text = Resources.objects.filter(type="contribute").first()
    contact = Resources.objects.filter(type="contribute_contact").first()

    return render(request, 'contribute.html', {'text': text.text, 'contact': contact.text})

def register(request: HttpRequest) -> HttpResponse:
    """
    Handles User Registration via UserRegisterForm. Form is saved for POST requests,
    rendered for GET requests. Upon account creation, user is logged in and redirected to home

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing registration page template and UserRegisterForm
    """
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

@login_required
def companies(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Renders Company data for page specified in URL params
    on POST request, saves form data to PendingCompany, creates PendingChange object with 'create' type
    on GET request, renders SearchForm, PendingCompanyForm, companies template
    We pre-fetch all the m2m tables, which results in one big query being run, rather than hundreds of small ones
    After prefetch_related, all company.___.all() queries don't hit the db, resulting in near instant response time

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing companies page template, PendingCompanyForm, SearchForm
    """


    page = int(request.GET.get('page', 1))
    
    companies = Company.objects.filter(Name__istartswith=PAGE_INDEX[page-1]).select_related('Industry', 'Status').prefetch_related('Solutions', 'Category', 'stakeholderGroup', 'productGroup', 'Stage')
    solutions = [company.Solutions.all()[:1][0] if len(company.Solutions.all()[:1]) > 0 else "--" for company in companies]
    categories = [company.Category.all()[:1][0] if len(company.Category.all()[:1]) > 0 else "--" for company in companies]
    productGroups = [company.productGroup.all()[:1][0] if len(company.productGroup.all()[:1]) > 0 else "--" for company in companies]
    stakeholderGroups = [company.stakeholderGroup.all()[:1][0] if len(company.stakeholderGroup.all()[:1]) > 0 else "--" for company in companies]
    stages = [company.Stage.all()[:1][0] if len(company.Stage.all()[:1]) > 0 else "--" for company in companies]
    
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
        filterStatusForm = FilterStatusForm()
        filterIndustryForm = FilterIndustryForm()
        filterCategoryForm = FilterCategoryForm()
        filterStakeholderGroupForm = FilterStakeholderGroupForm()
        filterStageForm = FilterStageForm()
        filterProductGroupForm = FilterProductGroupForm()
        filterSolutionForm = FilterSolutionForm()

    data = zip(companies, solutions, categories, productGroups, stakeholderGroups, stages)

    return render(request, 'companies.html', {'form': form,
                                              'companies': data,
                                              'searchForm': searchForm, 
                                              'page': page,
                                              'page_index': PAGE_INDEX,
                                              'filterStatusForm': filterStatusForm,
                                              'filterIndustryForm': filterIndustryForm,
                                              'filterCategoryForm': filterCategoryForm,
                                              'filterStakeholderGroupForm': filterStakeholderGroupForm,
                                              'filterStageForm': filterStageForm,
                                              'filterProductGroupForm': filterProductGroupForm,
                                              'filterSolutionForm': filterSolutionForm
                                              })

@staff_member_required
def edit_company(request: HttpRequest, id: int) -> HttpResponse:
    """
    Protected Route. Handles edit action for Companies
    for POST requests, saves form data as PendingCompany, creates PendingChange with type 'edit'
    for GET requests, returns edit form, company data, edit_companies template

    Parameters:
    request (HttpRequest): incoming HTTP request
    id (int): id of company to be edited

    Returns:
    response (HttpResponse): HTTP response containing company editpage template and PendingCompanyForm
    """
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

@login_required
def view_company(request: HttpRequest, id: int) -> HttpResponse:
    """
    Protected Route. Shows all column values for a single company

    Parameters:
    request (HttpRequest): incoming HTTP request
    id (int): id of company being viewed

    Returns:
    response (HttpResponse): HTTP response containing company view page template and company data as dict
    """
    company = Company.objects.get(id = id)
    obj = model_to_dict(company)

    return render(request, 'company_view.html', {'company': company, 'obj': obj})

@staff_member_required
def view_company_pending(request: HttpRequest, changeType: str, id: int) -> HttpResponse:
    """
    Staff Route. Shows all column values for a single pending company, 
    as well as its change type

    Parameters:
    request (HttpRequest): incoming HTTP request
    changeType (str): change type for affected company (one of ['edit', 'create', 'deletion'])
    id (int): id of company being viewed

    Returns:
    response (HttpResponse): HTTP response containing company view page template and company data as dict
    """
    if changeType == 'deletion':
        company = Company.objects.get(id = id)
    if changeType == 'create' or changeType == 'edit':
        company = PendingCompany.objects.get(id = id)    
    obj = model_to_dict(company)
        
    return render(request, 'company_view_pending.html', {'company': company, 'obj': obj, 'changeType': changeType})

@staff_member_required
def view_company_approve(_request: HttpRequest, changeType: str, id: int) -> HttpResponse:
    """
    Staff Route. Handles approval of a PendingChange for companies
    if changeType is deletion, company is deleted from PendingCompanies
    if changeType is create, company is copied from PendingCompanies into Companies table
    if changeType is edit, company in Companies table is edited with all values from PendingCompany
    PendingChange and PendingCompany records are deleted (cleanup)

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    changeType (str): change type for affected company (one of ['edit', 'create', 'deletion'])
    id (int): id of approved company

    Returns:
    response (HttpResponse): HTTP response redirecting to /companies view
    """
    if changeType == 'deletion':
        company = Company.objects.get(id = id)
        company.delete()
        change = PendingChanges.objects.get(companyId = id, changeType = changeType)
        change.delete()

        return redirect('/companies')
    
    pendingCompany = PendingCompany.objects.get(id = id)
    change = PendingChanges.objects.get(companyId = id, changeType = changeType)
    if changeType == 'create':
        new_company = Company()
        for field in pendingCompany._meta.fields:
            if not field.primary_key:
                setattr(new_company, field.name, getattr(pendingCompany, field.name))
        new_company.save()
    if changeType == 'edit':
        company = Company.objects.get(id = change.editId)
        for field in pendingCompany._meta.fields:
            if not field.primary_key:
                setattr(company, field.name, getattr(pendingCompany, field.name))
        company.save()

    change.delete()
    pendingCompany.delete()

    return redirect('/companies')

@staff_member_required
def view_company_reject(_request: HttpRequest, changeType: str, id: int) -> HttpResponse:
    """
    Staff Route. Rejects a PendingChange

    Parameters:
    request (HttpRequest): incoming HTTP request
    changeType (str): change type for affected company (one of ['edit', 'create', 'deletion'])
    id (int): id of rejected company

    Returns:
    response (HttpResponse): HTTP response redirecting to PendingChanges view
    """
    change = PendingChanges.objects.get(companyId = id, changeType = changeType)
    if changeType == 'create' or changeType == 'edit':
        company = PendingCompany.objects.get(id=id)
        company.delete()
    change.delete()

    return redirect('/changes')

@login_required
def companies_filtered(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Basically does the same thing as the /companies route, except 
    filters queryset based on SearchForm / Filter input.

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing company page template and filtered company data
    """
    query = None
    companies = Company.objects.select_related('Industry', 'Status').prefetch_related('Solutions', 'Category', 'stakeholderGroup', 'productGroup', 'Stage')
    if "item-filter" in request.POST:
        status_ids = request.POST.getlist("status")
        industry_ids = request.POST.getlist("industry")
        category_ids = request.POST.getlist("category")
        stakeholder_group_ids = request.POST.getlist("stakeholder_groups")
        stage_ids = request.POST.getlist("stage")
        product_ids = request.POST.getlist("product_group")
        solution_ids = request.POST.getlist("solution")
        filter_lists = [
            (status_ids, "Status"), 
            (industry_ids, "Industry"), 
            (category_ids, "Category"), 
            (stakeholder_group_ids, "stakeholderGroup"),
            (stage_ids, "Stage"),
            (product_ids, "productGroup"),
            (solution_ids, "Solutions")
        ]
        for lst, field in filter_lists:
            if lst:
                companies = companies.filter(**{f"{field}__in": lst})

    if "company-search" in request.POST:
        form = SearchForm(request.POST)
        query = form["q"]
        companies = companies.filter(Name__contains=query.value())
    
    solutions = [company.Solutions.all()[:1][0] if len(company.Solutions.all()[:1]) > 0 else "--" for company in companies]
    categories = [company.Category.all()[:1][0] if len(company.Category.all()[:1]) > 0 else "--" for company in companies]
    productGroups = [company.productGroup.all()[:1][0] if len(company.productGroup.all()[:1]) > 0 else "--" for company in companies]
    stakeholderGroups = [company.stakeholderGroup.all()[:1][0] if len(company.stakeholderGroup.all()[:1]) > 0 else "--" for company in companies]
    stages = [company.Stage.all()[:1][0] if len(company.Stage.all()[:1]) > 0 else "--" for company in companies]

    form = PendingCompanyForm()
    searchForm = SearchForm()
    filterStatusForm = FilterStatusForm()
    filterIndustryForm = FilterIndustryForm()
    filterCategoryForm = FilterCategoryForm()
    filterStakeholderGroupForm = FilterStakeholderGroupForm()
    filterStageForm = FilterStageForm()
    filterProductGroupForm = FilterProductGroupForm()
    filterSolutionForm = FilterSolutionForm()

    data = zip(companies, solutions, categories, productGroups, stakeholderGroups, stages)

    return render(request, 'companies.html', {'form': form, 
                                              'companies': data, 
                                              'searchForm': searchForm, 
                                              'query': query.value() if query else None, 
                                              'page_index': PAGE_INDEX,
                                              'filterStatusForm': filterStatusForm,
                                              'filterIndustryForm': filterIndustryForm,
                                              'filterCategoryForm': filterCategoryForm,
                                              'filterStakeholderGroupForm': filterStakeholderGroupForm,
                                              'filterStageForm': filterStageForm,
                                              'filterProductGroupForm': filterProductGroupForm,
                                              'filterSolutionForm': filterSolutionForm
                                              })

@staff_member_required
def remove_companies(request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Adds deletion to PendingChanges

    Parameters:
    request (HttpRequest): incoming HTTP request
    id (int): id of company to be deleted

    Returns:
    response (HttpResponse): HTTP response redirecting to /companies
    """
    PendingChanges.objects.create(companyId=id, changeType='deletion')
    messages.info(request, 'Deletion of Company requested')

    return redirect('/companies')

@staff_member_required
def export_companies(_request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Exports all data from Company table

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)

    Returns:
    response (HttpResponse): HTTP response containing company data in csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="companies.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.Company.')[1] for field in Company._meta.fields])

    companies = Company.objects.all().values_list()
    for company in companies:
        writer.writerow(company)

    return response

@login_required
def categories(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Shows all categories from Category table
    for POST requests, saves form data to Category table

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing category data
    """
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/categories')  # Redirect to a success page
    else:
        form = CategoryForm()

    return render(request, 'categories.html', {'form': form, 'data': categories, 'type': 'category', 'delete_url': 'remove_categories'})

@staff_member_required
def remove_categories(_request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Removes a category

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    id (int): id of category to be deleted 

    Returns:
    response (HttpResponse): HTTP response redirecting to categories view
    """
    category = Category.objects.get(id = id)
    category.delete()
    return redirect('/categories')

@staff_member_required
def export_categories(_request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Exports all entries in Category table to csv

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing category data in csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="categories.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.Category.')[1] for field in Category._meta.fields])

    categories = Category.objects.all().values_list()
    for category in categories:
        writer.writerow(category)

    return response

@login_required
def solutions(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Shows all solutions from Solution table
    for POST requests, saves form data to Solution table

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing solution data
    """
    solutions = Solution.objects.all()
    if request.method == 'POST':
        form = SolutionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/solutions')  # Redirect to a success page
    else:
        form = SolutionForm()

    return render(request, 'solutions.html', {'form': form, 'data': solutions, 'type': 'solution', 'delete_url': 'remove_solutions'})

@staff_member_required
def remove_solutions(_request: HttpRequest, id: int):
    """
    Staff Route. Removes a solution

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    id (int): id of solution to be deleted 

    Returns:
    response (HttpResponse): HTTP response redirecting to solution view
    """
    solution = Solution.objects.get(id = id)
    solution.delete()
    return redirect('/solutions')

@staff_member_required
def export_solutions(_request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Exports all entries in Solutions table to csv

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing solution data in csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="solutions.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.Solution.')[1] for field in Solution._meta.fields])

    solutions = Solution.objects.all().values_list()
    for solution in solutions:
        writer.writerow(solution)

    return response

@login_required
def StakeholderGroups(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Shows all entries from stakeholderGroups table
    for POST requests, saves form data to stakeholderGroups table

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing stakeholderGroups data
    """
    groups = stakeholderGroups.objects.all()
    if request.method == 'POST':
        form = stakeholderGroupsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/stakeholder-groups')  # Redirect to a success page
    else:
        form = stakeholderGroupsForm()

    return render(request, 'stakeholderGroups.html', {'form': form, 'type': 'stakeholderGroup', 'data': groups, 'delete_url': 'remove_stakeholder_groups' })

@staff_member_required
def remove_stakeholder_groups(_request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Removes a stakeholderGroups

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    id (int): id of stakeholderGroups to be deleted 

    Returns:
    response (HttpResponse): HTTP response redirecting to stakeholderGroups view
    """
    group = stakeholderGroups.objects.get(id = id)
    group.delete()
    return redirect('/stakeholder-groups')

@staff_member_required
def export_stakeholder_groups(_request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Exports all entries in stakeholderGroups table to csv

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing stakeholderGroups data in csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stakeholder_groups.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.stakeholderGroups.')[1] for field in stakeholderGroups._meta.fields])

    StakeholderGroups = stakeholderGroups.objects.all().values_list()
    for group in StakeholderGroups:
        writer.writerow(group)

    return response

@login_required
def stages(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Shows all entries from Stage table
    for POST requests, saves form data to Stage table

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing Stage data
    """
    stages = Stage.objects.all()
    if request.method == 'POST':
        form = StageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/stages')  # Redirect to a success page
    else:
        form = StageForm()

    return render(request, 'stages.html', {'form': form, 'data': stages, 'type': 'stage', 'delete_url': 'remove_stages'})

@staff_member_required
def remove_stages(_request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Removes a Stage

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    id (int): id of Stage to be deleted 

    Returns:
    response (HttpResponse): HTTP response redirecting to Stage view
    """
    stage = Stage.objects.get(id = id)
    stage.delete()
    return redirect('/stages')

@staff_member_required
def export_stages(_request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Exports all entries in Stage table to csv

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing Stage data in csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stages.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.Stage.')[1] for field in Stage._meta.fields])

    stages = Stage.objects.all().values_list()
    for stage in stages:
        writer.writerow(stage)

    return response

@login_required
def productGroups(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Shows all entries from productGroup table
    for POST requests, saves form data to productGroup table

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing productGroup data
    """
    groups = ProductGroup.objects.all()
    if request.method == 'POST':
        form = ProductGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/product-groups')  # Redirect to a success page
    else:
        form = ProductGroupForm()

    return render(request, 'productGroups.html', {'form': form, 'data': groups, 'type': 'productGroups', 'delete_url': 'remove_product_group'})

@staff_member_required
def remove_product_groups(_request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Removes a ProductGroup

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    id (int): id of ProductGroup to be deleted 

    Returns:
    response (HttpResponse): HTTP response redirecting to ProductGroup view
    """
    group = ProductGroup.objects.get(id = id)
    group.delete()
    return redirect('/product-groups')

@staff_member_required
def export_product_groups(_request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Exports all entries in ProductGroup table to csv

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing ProductGroup data in csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product_groups.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.ProductGroup.')[1] for field in ProductGroup._meta.fields])

    productGroups = ProductGroup.objects.all().values_list()
    for group in productGroups:
        writer.writerow(group)

    return response

@login_required
def status(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Shows all entries from Status table
    for POST requests, saves form data to Status table

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing Status data
    """
    status = Status.objects.all()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/status')  # Redirect to a success page
    else:
        form = StatusForm()

    return render(request, 'status.html', {'form': form, 'data': status, 'type': 'status', 'delete_url': 'remove_status'})

@staff_member_required
def remove_status(_request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Removes a Status

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    id (int): id of Status to be deleted 

    Returns:
    response (HttpResponse): HTTP response redirecting to Status view
    """
    status = Status.objects.get(id = id)
    status.delete()
    return redirect('/status')

@staff_member_required
def export_status(_request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Exports all entries in Status table to csv

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing Status data in csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="status.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.Status.')[1] for field in Status._meta.fields])

    status = Status.objects.all().values_list()
    for data in status:
        writer.writerow(data)

    return response

@login_required
def grower(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Shows all entries from Grower table
    for POST requests, saves form data to Grower table

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing Grower data
    """
    growers = Grower.objects.all()
    if request.method == 'POST':
        form = GrowerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/grower')  # Redirect to a success page
    else:
        form = GrowerForm()

    return render(request, 'grower.html', {'form': form, 'data': growers, 'delete_url': 'remove_grower', 'type': 'grower'})

@staff_member_required
def remove_grower(_request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Removes a Grower

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    id (int): id of Grower to be deleted 

    Returns:
    response (HttpResponse): HTTP response redirecting to Grower view
    """
    grower = Grower.objects.get(id = id)
    grower.delete()
    return redirect('/grower')

@staff_member_required
def export_grower(_request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Exports all entries in Grower table to csv

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing Grower data in csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="grower.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.Grower.')[1] for field in Grower._meta.fields])

    grower = Grower.objects.all().values_list()
    for data in grower:
        writer.writerow(data)

    return response

@login_required
def industry(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Shows all entries from Industry table
    for POST requests, saves form data to Industry table

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing Industry data
    """
    industries = Industry.objects.all()
    if request.method == 'POST':
        form = IndustryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/industry')  # Redirect to a success page
    else:
        form = IndustryForm()

    return render(request, 'industry.html', {'form': form, 'data': industries, 'type': 'industries', 'delete_url': 'remove_industry'})

@staff_member_required
def remove_industry(_request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Removes an Industry

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    id (int): id of Industry to be deleted 

    Returns:
    response (HttpResponse): HTTP response redirecting to Industry view
    """
    industry = Industry.objects.get(id = id)
    industry.delete()
    return redirect('/industry')

def export_industry(_request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Exports all entries in Industry table to csv

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing Industry data in csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="industry.csv"'

    writer = csv.writer(response)
    writer.writerow([str(field).split('helloworld.Industry.')[1] for field in Industry._meta.fields])

    industry = Industry.objects.all().values_list()
    for data in industry:
        writer.writerow(data)

    return response

@staff_member_required
def dbChanges(request: HttpRequest) -> HttpResponse:
    """
    Protected Route. Shows all entries from PendingChanges table

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing PendingChanges data
    """
    changes = PendingChanges.objects.all()
    
    return render(request, 'companies_pending.html', {'changes': changes})

def map(request: HttpRequest) -> HttpResponse:
    """
    Public route. Shows the Hemp Map made by Cherish Despain

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response rendering map template
    """

    return render(request, 'map.html')

@staff_member_required
def admin_tools(request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Logic for letting site admins control content displayed on common pages
      - About
      - Contribute
      - Home Page

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response rendering admin tools template
    """
    resources = Resources.objects.order_by("type").all()
    
    if request.method == "POST":
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin_tools')
    
    form = ResourceForm()

    return render(request, 'admin_tools.html', {'data': resources, 'form': form})

@staff_member_required
def remove_resource(request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Delete a resource from the Resources table

    Parameters:
    request (HttpRequest): incoming HTTP request
    id (int): id of Resource to be deleted

    Returns:
    response (HttpResponse): HTTP response redirecting admin tools remplate
    """

    resource = Resources.objects.get(id = id)
    resource.delete()
    messages.info(request, 'Resource successfully deleted')

    return redirect('/admin_tools')

@staff_member_required
def edit_resource(request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Edit a resource from the Resources table

    Parameters:
    request (HttpRequest): incoming HTTP request
    id (int): id of Resource to be edited

    Returns:
    response (HttpResponse): HTTP response redirecting admin tools remplate
    """

    resource = Resources.objects.get(id = id)
    form = ResourceForm(request.POST, instance=resource)
    if request.POST and form.is_valid():
        resource_edit = form.save(commit=False)
        for field in resource._meta.fields:
            if not field.primary_key:
                setattr(resource, field.name, getattr(resource_edit, field.name))
        resource.save()
        messages.info(request, 'Resource successfully edited')
        return redirect('/admin_tools')  # Redirect to a success page
    else:
        form = ResourceForm(instance=resource)
    
    return render(request, 'edit_resource.html', {'form': form, 'resource': resource})