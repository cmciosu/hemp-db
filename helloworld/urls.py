from django.urls import path
from . import views
from .views import CompanyListView, CompanyCreateView


urlpatterns = [
    path("", views.index, name="index"),
    path("companies", views.database1, name="companies"),

    # List view for all companies
    path('companies/', CompanyListView.as_view(), name='company-list'),

    # Create view for a new company
    path('companies/create/', CompanyCreateView.as_view(), name='company-create'),

    # Update view for a specific company
    # path('companies/<int:pk>/update/', CompanyUpdateView.as_view(), name='company-update'),

    # Delete view for a specific company
    # path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company-delete'),
]
