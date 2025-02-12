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
from .forms import UploadFileForm
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
from .models import UploadIndex
from .tokens import account_activation_token
from .notifications import email_admins
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.forms.models import model_to_dict
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

import csv
import geocoder
from decimal import Decimal
from copy import deepcopy
import pandas as pd
import numpy as np

# Used for Pagination Bar on /companies
PAGE_INDEX=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

@staff_member_required
def upload_wizard(request: HttpRequest) -> HttpResponse:
    """
    Staff Route. Presents the user with all uploaded companies, indicating duplicates, and more.
    Once approved, companies will be uploaded to Companies

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response redirecting to companies page table
    """
    index = UploadIndex.objects.all().values_list("pendingID")
    companies = PendingCompany.objects.filter(pk__in = index)
    message = ""
    if request.method == "POST":
        # Add all companies
        if "add-all" in request.POST:
            for company in companies:
                new_company = Company()
                for field in company._meta.fields:
                    if not field.primary_key:
                        setattr(new_company, field.name, getattr(company, field.name))
                new_company.save()
                company.delete()
            message = "Uploaded All Companies"
        # Add only unique companies
        elif "add-unique" in request.POST:
            for company in companies:
                dup = Company.objects.filter(Name = company.Name).all()
                if not dup:
                    new_company = Company()
                    for field in company._meta.fields:
                        if not field.primary_key:
                            setattr(new_company, field.name, getattr(company, field.name))
                    new_company.save()
                company.delete()
            message = "Uploaded Unique Companies"
        # Upload Nothing
        elif "cancel" in request.POST:
            companies.delete()
            message = "Canceled File Upload"

        UploadIndex.objects.all().delete()
        messages.info(request, message)
        return redirect("/companies")
    data = []
    for company in companies:
        record = {}
        record["company"] = company
        dup = Company.objects.filter(Name = company.Name).all()
        record["duplicate"] = True if dup else False
        data.append(record)

    return render(request, "upload_wizard.html", {"data": data})

@staff_member_required
def upload_file(request: HttpRequest) -> HttpResponse:
    """
    Staff route. Should only be used in emergencies (not secure). 
    Uses pandas to parse uploaded file, saves company data straight to Companies table

    Parameters:
    request (HttpRequest): incoming HTTP request containing file

    Returns:
    response (HttpResponse): HTTP response redirecting to companies page template
    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                file = request.FILES["file"]
                df = pd.read_csv(file)
                df = df.replace({np.nan: ''})
                frames = df.to_dict("records")
                for frame in frames:
                    frame["Status"] = Status.objects.get(id = frame["Status"])
                    frame["Industry"] = Industry.objects.get(id = frame["Industry"])
                    frame["Grower"] = Grower.objects.get(id = frame["Grower"])
                    model = PendingCompany(**frame)
                    model.save()
                    if (model.id):
                        upload = UploadIndex(pendingID = model.id)
                        upload.save()
                return redirect("/upload_wizard")
        except:  # noqa: E722
            messages.error(request, 'There was an error with the file upload') 
            return redirect("/companies")
                
    else:
        form = UploadFileForm()

    return render(request, "upload.html", {"form": form})

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

    return render(request, 'home.html', {'articles': articles, 
                                         'title': title.title if title else "", 
                                         'home_text': home_text.text if home_text else "" })

def about(request: HttpRequest) -> HttpResponse:
    """
    Renders about page template

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing about page template
    """
    about = Resources.objects.filter(type="about").first()

    return render(request, 'about.html', {'about': about.text if about else ""})

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



    return render(request, 'contribute.html', {'text': text.text if text else "", 
                                               'contact': contact.text if contact else ""})
    
def activate(request, uidb64, token):
    """
    Handles account activation and rerouting for when Activate Now button in their email
    If the user exists then mark the user as active and save the user to the db
    Then 
    Parameters:
    

    Returns:
    
    """
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
        print(f"Error decoding uid or retrieving user: {e}")
                
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Successfully Activated Account")
    #print(user)
    return redirect('/')

def activate_email(request: HttpRequest, user, to_email):
    """
    Builds and sends an email for user verification

    Parameters:
    

    Returns:
    
    """
    mail_subjet = "Activate User Account"
    message = render_to_string(
        "activate_user.html", {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http'
        }
    )
    
    email = EmailMessage(mail_subjet, message, to=[to_email])
    email.content_subtype = "html"
    if email.send():
        messages.success(request, f'Dear {user.username}, please go to {to_email} inbox/spam & click on recieved activation link to confirm and complete the registration.')
    else:
        messages.error(request, f'Error sending authentication email to {to_email}, double check spelling of email.')

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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email = form.cleaned_data.get('email')
            activate_email(request, user, email)
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
    try:
        page = int(request.GET.get('page', 1))
        page = page if abs(page) < len(PAGE_INDEX)+1 else 1
    except ValueError: 
        page = 1
    companies = Company.objects.filter(Name__istartswith=PAGE_INDEX[page-1]).select_related('Industry', 'Status').prefetch_related('Solutions', 'Category', 'stakeholderGroup', 'productGroup', 'Stage')
    solutions = [company.Solutions.all()[:1][0] if len(company.Solutions.all()[:1]) > 0 else "--" for company in companies]
    categories = [company.Category.all()[:1][0] if len(company.Category.all()[:1]) > 0 else "--" for company in companies]
    productGroups = [company.productGroup.all()[:1][0] if len(company.productGroup.all()[:1]) > 0 else "--" for company in companies]
    stakeholderGroups = [company.stakeholderGroup.all()[:1][0] if len(company.stakeholderGroup.all()[:1]) > 0 else "--" for company in companies]
    stages = [company.Stage.all()[:1][0] if len(company.Stage.all()[:1]) > 0 else "--" for company in companies]
    
    if request.method == 'POST':
        form = PendingCompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False) # Don't save to DB yet

            if not company.Latitude and not company.Longitude:
                lat, lng = geocode_location(company.Address, company.City, company.State, company.Country)
                company.Latitude = lat
                company.Longitude = lng

            company.save() # Save instance as Pending Company
            form.save_m2m() # Save many-to-many form data
            messages.info(request, 'Company successfully submitted')
            pending_change = PendingChanges.objects.create(companyId=company.id, changeType='create')
            email_admins(action='created', company_name=company.Name, pending_change_id=pending_change.id)
            return redirect('/companies')  # Redirect to a success page
    else:
        form = PendingCompanyForm()
        uploadForm = UploadFileForm()
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
                                              'uploadForm': uploadForm,
                                              'companies': data,
                                              'num_companies': companies.count(),
                                              'searchForm': searchForm, 
                                              'cur_page': page,
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
    original_company = deepcopy(company) # Deep copy original data for location comparison
    form = PendingCompanyForm(request.POST, instance=company)
    if request.POST and form.is_valid():
        company_edit = form.save(commit=False)
        new_company = PendingCompany()
        for field in new_company._meta.fields:
            if not field.primary_key:
                setattr(new_company, field.name, getattr(company_edit, field.name))

        # If location fields have changed, geocode new lat/lng
        location_changed = check_if_location_edited(original_company, new_company)
        if location_changed:
            lat, lng = geocode_location(new_company.Address, new_company.City, new_company.State, new_company.Country)
            new_company.Latitude = lat
            new_company.Longitude = lng

        new_company.save()
        
        # Save the m2m values from the form to the PendingCompany instance (new_company)
        for field_name, field_value in form.cleaned_data.items():

            # If the field is an M2M field
            if field_name in [field.name for field in new_company._meta.many_to_many]:
                # Get the M2M field from the new_company PendingCompany instance
                m2m_field = getattr(new_company, field_name)
                # Update it's value with updated value(s) from form
                m2m_field.set(field_value)

        messages.info(request, 'Company successfully edited')
        pending_change = PendingChanges.objects.create(companyId=new_company.id, changeType='edit', editId=company.id)
        email_admins(action='edited', company_name=new_company.Name, pending_change_id=pending_change.id)
        return redirect('/companies')  # Redirect to a success page
    else: 
        form = PendingCompanyForm(instance=company)

    return render(request, 'edit_companies.html', {'form': form, 'company': company})

def check_if_location_edited(company: Company, new_company: PendingCompany) -> bool:
    """
    Given a company and it's pending company (edits made), checks if
    the Address, City, State, or Country were changed. If any of these
    have changed and the Latitude and Longitude were NOT changed,
    returns True. Otherwise False.

    Helper function for determining if latitude/longitude
    lookup needs to be made after a company is edited.

    Parameters:
    company (Company): original company that is being edited
    new_company (PendingCompany): model representing original company but with edits

    Returns:
    bool: True if user changed any location field without updating latitude/longitude
          False if user changed latitude/longitude, or didn't edit any location fields
    """
    location_fields = ['Address', 'City', 'State', 'Country']
    lat_lng_fields = ['Latitude', 'Longitude']
    a = b = False

    # Check if any location fields were changed in the edit
    for field in location_fields:
        if getattr(company, field) != getattr(new_company, field):
            a = True
            break

    # Check if latitude or longitude were changed
    for field in lat_lng_fields:
        if getattr(company, field) != getattr(new_company, field):
            b = True
            break

    if a and not b:
        return True # User changed location without updating lat/long
    
    return False # User changed lat/long, or did not edit any location fields

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
    company = Company.objects.select_related('Industry', 'Status', 'Grower').get(id = id)
    obj = model_to_dict(company)
    # Manually add FK values
    obj["Status"] = company.Status.status
    obj["Industry"] = company.Industry.industry
    obj["Grower"] = company.Grower.grower

    return render(request, 'company_view.html', {'company': company, 'obj': obj})

@staff_member_required
def view_company_pending(request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Shows all column values for a single pending company, 
    as well as its change type

    Parameters:
    request (HttpRequest): incoming HTTP request
    id (int): id of change being viewed

    Returns:
    response (HttpResponse): HTTP response containing company view page template and company data as dict
    """
    change = PendingChanges.objects.get(id=id)
    if change.changeType == 'deletion':
        company = Company.objects.get(id = change.companyId)
    if change.changeType == 'create' or change.changeType == 'edit':
        company = PendingCompany.objects.select_related('Industry', 'Status', 'Grower').get(id = change.companyId)    
    obj = model_to_dict(company)
    # Manually add FK values
    obj["Status"] = company.Status.status
    obj["Industry"] = company.Industry.industry
    obj["Grower"] = company.Grower.grower
        
    return render(request, 'company_view_pending.html', {'company': company, 'obj': obj, 'change': change})

@staff_member_required
def view_company_approve(_request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Handles approval of a PendingChange for companies
    if changeType is deletion, company is deleted from PendingCompanies
    if changeType is create, company is copied from PendingCompanies into Companies table
    if changeType is edit, company in Companies table is edited with all values from PendingCompany
    PendingChange and PendingCompany records are deleted (cleanup)

    Parameters:
    request (HttpRequest): incoming HTTP request (unused)
    id (int): id of pending change

    Returns:
    response (HttpResponse): HTTP response redirecting to /companies view
    """
    change = PendingChanges.objects.get(id=id)
    if change.changeType == 'deletion':
        company = Company.objects.get(id = change.companyId)
        company.delete()
        change.delete()

        return redirect('/companies')
    
    pendingCompany = PendingCompany.objects.get(id = change.companyId)
    if change.changeType == 'create':
        new_company = Company()
        for field in pendingCompany._meta.fields:
            if not field.primary_key:
                setattr(new_company, field.name, getattr(pendingCompany, field.name))
        new_company.save()

        # Copy over m2m values
        for field in pendingCompany._meta.many_to_many:
            m2m_values = getattr(pendingCompany, field.name).all()
            getattr(new_company, field.name).set(m2m_values)

    if change.changeType == 'edit':
        company = Company.objects.get(id = change.editId)
        for field in pendingCompany._meta.fields:
            if not field.primary_key:
                setattr(company, field.name, getattr(pendingCompany, field.name))
        company.save()

        # Copy over m2m values
        for field in pendingCompany._meta.many_to_many:
            m2m_values = getattr(pendingCompany, field.name).all()
            getattr(company, field.name).set(m2m_values)

    change.delete()
    pendingCompany.delete()

    return redirect('/companies')

@staff_member_required
def view_company_reject(_request: HttpRequest, id: int) -> HttpResponse:
    """
    Staff Route. Triggered when admin clicks "Reject" in company_view_pending

    Parameters:
    request (HttpRequest): incoming HTTP request
    id (int): id of pending change

    Returns:
    response (HttpResponse): HTTP response redirecting to PendingChanges view
    """
    change = PendingChanges.objects.get(id=id)
    if change.changeType == 'create' or change.changeType == 'edit':
        company = PendingCompany.objects.get(id=change.companyId)
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
        companies = companies.filter(Name__icontains=query.value())
    
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
    company = Company.objects.get(id=id)
    pending_change = PendingChanges.objects.create(companyId=id, changeType='deletion')

    messages.info(request, 'Deletion of Company requested')
    email_admins(action='deleted', company_name=company.Name, pending_change_id=pending_change.id)

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
    Public route. Passes data about each company to map.html
    where a map of markers is rendered using LeafletJS.

    Parameters:
    request (HttpRequest): incoming HTTP request

    Returns:
    response (HttpResponse): HTTP response containing company location data
    """
    # Select all companies who have a latitude and longitude and are not inactive
    companies = list(
        Company.objects
        .exclude(Latitude__isnull=True)
        .exclude(Longitude__isnull=True)
        .exclude(Status__id=2)
        .values(
            'id', 'Name', 'Website', 'Phone',
            'Latitude', 'Longitude',
            'Address', 'City', 'State', 'Country'            
        )
    )

    empty = ['', 'n/a', '--', 'nan', 'none', None]

    # Cleanup data before sending
    for company in companies:

        # Construct one location string from all present location fields
        location_parts = []
        for field in ['Address', 'City', 'State', 'Country']:
            if company[field].lower() not in empty:
                location_parts.append(company[field])
        company['Location'] = ', '.join(location_parts)

        # Delete redundant fields from being sent
        del company['Address']
        del company['City']
        del company['State']
        del company['Country']

        # Only send Website and Phone if they exist
        if company['Website'].lower() in empty:
            del company['Website']
        if company['Phone'].lower() in empty:
            del company['Phone']

    return render(request, 'map.html', {'companies': companies})

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

def geocode_location(address: str, city: str, state: str, country: str) -> tuple[Decimal, Decimal]:
    """
    Takes in address components, cleans them, constructs a geocoding query,
    and returns the latitude and longitude using geocoder.arcgis(). Returns
    (None, None) upon a failure.

    Parameters:
    address (str): Company/PendingCompany.Address
    city (str): Company/PendingCompany..City
    state (str): Company/PendingCompany.State
    country (str): Company/PendingCompany.Country

    Returns:
    tuple[float, float]: A tuple containing latitude and longitude for 
        database insertion. Returns (None, None) if geocoding fails.
    """
    def clean_value(value: str) -> str:
        """Clean unwanted values and standardize missing data indicators."""
        value = str(value).strip()
        if value.lower() in ['', 'n/a', '--', 'nan', 'none']:
            return None
        return value

    # Clean the input values
    cleaned_address = clean_value(address)
    cleaned_city = clean_value(city)
    cleaned_state = clean_value(state)
    cleaned_country = clean_value(country)

    # Construct the geocoding query
    query_parts = []
    if cleaned_address:
        query_parts.append(cleaned_address)
    if cleaned_city:
        query_parts.append(cleaned_city)
    if cleaned_state:
        query_parts.append(cleaned_state)
    if cleaned_country:
        query_parts.append(cleaned_country)

    query = ', '.join(query_parts) if query_parts else None
    if not query:
        return None, None

    # Use geocoder as wrapper for arcgis query to get latitude and longitude
    try:
        g = geocoder.arcgis(query)
        if g.ok:
            lat = round(Decimal(g.lat), 6)
            lng = round(Decimal(g.lng), 6)
            return lat, lng
    except Exception:
        pass
    return None, None