from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import Company
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required

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

@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies': companies})

@login_required
def companies(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/companies')  # Redirect to a success page
    else:
        form = FileUploadForm()

    return render(request, 'companies.html', {'form': form, 'companies': companies})

def remove_companies(request, id):
    company = Company.objects.get(id = id)
    company.delete()
    return redirect('/companies')