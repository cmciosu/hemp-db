from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import Resources, Solution, Category, stakeholderGroups, Stage, ProductGroup, Status, Industry, Grower

from .forms import ResourceForm

# Customize Django Administration header/title
admin.site.site_header = "HempDB Administration"
admin.site.site_title = "HempDB Admin Portal"
# admin.site.index_title = "HempDB Admin"

# Enables the Log Entries ModelAdmin object for viewing
admin.site.register(LogEntry)

# Register DB models here for staff access
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
