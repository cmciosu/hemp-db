from django.contrib import admin
from .models import Company, PendingCompany, PendingChanges

# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["Name", "id"]
    search_fields = ["Name"]

@admin.register(PendingCompany)
class PendingCompanyAdmin(admin.ModelAdmin):
    pass

@admin.register(PendingChanges)
class PendingChangesAdmin(admin.ModelAdmin):
    pass