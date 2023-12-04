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
