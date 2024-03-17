## Django
from django.urls import path
## Views
from . import views
from .views import CompanyCreateView


urlpatterns = [
    # Root
    path("", views.index, name="index"),

    # Companies
    path('companies/', views.companies, name="companies"),
    path('companies/create/', CompanyCreateView.as_view(), name='company-create'),
    path('companies/<int:id>', views.view_company, name='company-view'),
    path('companies_pending/<int:id>', views.view_company_pending, name='company-view-pending'),
    path('companies_approve/<int:id>', views.view_company_approve, name='company-pending-approve'),
    path('companies_reject/<int:id>', views.view_company_reject, name='company-pending-reject'),
    path('companies/search/', views.companies_filtered, name='company-filtered'),
    path('remove_companies/<int:id>', views.remove_companies),

    # Categories
    path('categories/', views.categories, name="categories"),
    path('remove_categories/<int:id>', views.remove_categories),

    # Solutions 
    path('solutions/', views.solutions, name="solutions"),
    path('remove_solutions/<int:id>', views.remove_solutions),

    # Stakeholder Groups
    path('stakeholder-groups/', views.StakeholderGroups, name="StakeholderGroups"),
    path('remove_groups/<int:id>', views.remove_stakeholder_groups),

    # Stage
    path('stages/', views.stages, name="stages"),
    path('remove_stages/<int:id>', views.remove_stages),

    # Product Group
    path('product-groups/', views.productGroups, name="productGroups"),
    path('remove_product_group/<int:id>', views.remove_product_groups),

    # Processing Focus
    path('processing-focus/', views.processingFocus, name="processingFocus"),
    path('remove_focus/<int:id>', views.remove_processing_focus),

    # Extraction Type
    path('extraction-types/', views.extractionTypes, name="extractionTypes"),
    path('remove_type/<int:id>', views.remove_extraction_type),

    # User Registration
    path('user/register', views.register),

    # Changes
    path('changes/', views.dbChanges),
]