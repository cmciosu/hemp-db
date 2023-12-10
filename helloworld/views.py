from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


def database1(request):
    template = loader.get_template('companies.html')
    return HttpResponse(template.render())

from django.views.generic import ListView, CreateView
from .models import Company

class CompanyListView(ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'

class CompanyCreateView(CreateView):
    model = Company
    template_name = 'company_form.html'
    fields = ['name', 'industry']
    success_url = '/companies/'  # Redirect to the list view after successful creation
