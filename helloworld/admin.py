from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import Company
from .models import PendingCompany
from .models import PendingChanges
from .models import Resources
from .models import Solution
from .models import Category
from .models import stakeholderGroups
from .models import Stage
from .models import ProductGroup
from .models import Status
from .models import Industry
from .models import Grower

from .forms import ResourceForm

# Customize Django Administration header/title
admin.site.site_header = "HempDB Administration"
admin.site.site_title = "HempDB Admin Portal"
# admin.site.index_title = "HempDB Admin"

# Enables the Log Entries ModelAdmin object for viewing
admin.site.register(LogEntry)

# Register DB models here for staff access
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

@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    form = ResourceForm
    list_display = ["type", "title"]

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(stakeholderGroups)
class stakeholderGroupsAdmin(admin.ModelAdmin):
    pass

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    pass

@admin.register(Grower)
class GrowerAdmin(admin.ModelAdmin):
    pass