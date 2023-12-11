from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import Company

# Create your views here.
def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

from django.views.generic import ListView, CreateView
from .models import Company

def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies': companies})


class CompanyListView(ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'


class CompanyCreateView(CreateView):
    model = Company
    template_name = 'company_form.html'
    fields = ['name', 'industry']
    success_url = '/companies/'  # Redirect to the list view after successful creation

# uploading file to db
# import pandas as pd

# def upload_file(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Handle the uploaded file
#             file = request.FILES['file']

#             # Read the CSV/Excel file using pandas
#             df = pd.read_excel(file)  # Use read_csv for CSV files

#             # Validate and save data to the database
#             for index, row in df.iterrows():
#                 company = Company(
#                     name = row['Company Name'],
#                     industry = row['Industry'],
#                     status = row['Status'],
#                     info = row['Info'],
#                     headquarters = row['Headquarters'],
#                     sales = row['Sales'],
#                     product = row['Product'],
#                     # Add other fields
#                 )
#                 company.save()

#             return redirect('companies')  # Redirect to a success page
#     else:
#         form = FileUploadForm()

#     return render(request, 'upload_file.html', {'form': form})

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