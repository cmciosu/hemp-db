from django.shortcuts import render, redirect
from .forms import CompanyForm
from .forms import UserRegisterForm
from .models import Company
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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

def index(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password=form.cleaned_data.get('password1')

            messages.success(request, 'Account Created')
            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies': companies})

@login_required
def companies(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
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