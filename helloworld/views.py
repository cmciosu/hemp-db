from django.shortcuts import render, redirect
from .forms import CompanyForm
from .models import Company
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

class CompanyListView(ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'

class CompanyCreateView(CreateView):
    model = Company
    template_name = 'company_form.html'
    fields = ['name', 'industry']
    success_url = '/companies/'  # Redirect to the list view after successful creation

def index(request):
    return render(request, 'home.html')

def view_company(request, id):
    company = Company.objects.get(id = id)
    # fields = Company._meta.get_fields()
    obj = model_to_dict(company)

    return render(request, 'company_view.html', {'company': company, 'obj': obj})

@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies': companies})

@login_required
def companies(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/companies')  # Redirect to a success page
    else:
        form = CompanyForm()

    return render(request, 'companies.html', {'form': form, 'companies': companies})

def remove_companies(request, id):
    company = Company.objects.get(id = id)
    company.delete()
    return redirect('/companies')
