from django.db import models

# Django strongly encourages using lowercase table names using MySQL
# https://docs.djangoproject.com/en/5.1/ref/models/options/
# This will also restrict us to using snake_case so words are preserved.
# For consistency, singular names will also be implemented.

# TODO / Nice to have: Update Django model class and field names to also 
# follow these naming conventions. Will need carefully reviewed
# Django migrations to prevent data loss.
# 
# Naming Convention Rules:
# lowercase
# snake_case
# singular 

class UploadIndex(models.Model):
    pendingID = models.CharField(max_length=255)

    class Meta:
        db_table = "upload_index"

        verbose_name = "Upload Index"
        verbose_name_plural = "Upload Indexes"

class Resources(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=1024, blank=True)
    text = models.CharField(max_length=2048, blank=True)
    image = models.CharField(max_length=1024, blank=True)

    class Meta:
        db_table = "resource"

        verbose_name = "Resource"
        verbose_name_plural = "Resources"

class Solution(models.Model):
    solution = models.CharField(max_length=1024)
    
    def __str__(self):
        return self.solution

    class Meta:
        db_table = "solution"

        verbose_name = "Solution"
        verbose_name_plural = "Solutions"

class Category(models.Model):
    category = models.CharField(max_length=1024)

    def __str__(self):
        return self.category

    class Meta:
        db_table = "category"

        verbose_name = "Category"
        verbose_name_plural = "Categories"

class stakeholderGroups(models.Model):
    stakeholderGroup = models.CharField(max_length=1024)
    category = models.IntegerField()

    def __str__(self):
        return self.stakeholderGroup
    
    class Meta:
        db_table = "stakeholder_group"

        verbose_name = "Stakeholder Group"
        verbose_name_plural = "Stakeholder Groups"

class Stage(models.Model):
    stage = models.CharField(max_length=1024)
    category = models.IntegerField()

    def __str__(self):
        return self.stage

    class Meta:
        db_table = "stage"

        verbose_name = "Stage"
        verbose_name_plural = "Stages"

class ProductGroup(models.Model):
    productGroup = models.CharField(max_length=1024)

    def __str__(self):
        return self.productGroup

    class Meta:
        db_table = "product_group"

        verbose_name = "Product Group"
        verbose_name_plural = "Product Groups"

class Status(models.Model):
    status = models.CharField(max_length=250)

    def __str__(self):
        return "Status: " + self.status

    class Meta:
        db_table = "status"

        verbose_name = "Status"
        verbose_name_plural = "Statuses"

class Industry(models.Model):
    industry = models.CharField(max_length=250)

    def __str__(self):
        return "Industry: " + self.industry

    class Meta:
        db_table = "industry"

        verbose_name = "Industry"
        verbose_name_plural = "Industries"

class Grower(models.Model):
    grower = models.CharField(max_length=250)

    def __str__(self):
        return "Grower: " + self.grower

    class Meta:
        db_table = "grower"

        verbose_name = "Grower"
        verbose_name_plural = "Growers"

# Abstract base model for company-data related models.
# Altering this model will effect all models that inherit it,
# allowing for simpler implementation of features that allow staff users ways to
# manipulate (add/edit/delete) data fields through an interface (not programmatically)
#
# Also allows for easier development, avoiding redundant, duplicate code.
class CompanyDetail(models.Model):
    SrcKey = models.CharField(max_length=128, default=None, blank=True)
    Name = models.CharField(max_length=250)
    Industry = models.ForeignKey(Industry, null=True, on_delete=models.SET_NULL)
    Status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL)
    Grower = models.ForeignKey(Grower, null=True, on_delete=models.SET_NULL)
    Headquarters = models.CharField(max_length=255, blank=True)
    Address = models.CharField(max_length=512, default=None, blank=True)
    Sales = models.CharField(max_length=255, blank=True)
    Product = models.CharField(max_length=255, blank=True)
    City = models.CharField(max_length=250, blank=True)
    State = models.CharField(max_length=250, blank=True)
    Country = models.CharField(max_length=250)
    Solutions = models.ManyToManyField(Solution, blank=True)
    Website = models.CharField(max_length=512, blank=True)
    Category = models.ManyToManyField(Category, blank=True)
    stakeholderGroup = models.ManyToManyField(stakeholderGroups, blank=True)
    Stage = models.ManyToManyField(Stage, blank=True)
    productGroup = models.ManyToManyField(ProductGroup, blank=True)
    Products = models.CharField(max_length=250, blank=True)
    sasContact = models.CharField(max_length=250, blank=True)
    Description = models.CharField(max_length=2048, blank=True)
    pubPriv = models.CharField(max_length=128, blank=True)
    Ticker = models.CharField(max_length=128, blank=True)
    Naics = models.CharField(max_length=250, blank=True)
    Phone = models.CharField(max_length=250, blank=True)
    Email = models.CharField(max_length=250, blank=True)
    Stakeholder = models.CharField(max_length=250, blank=True)
    Principal = models.CharField(max_length=250, blank=True)
    Founded = models.CharField(max_length=250, blank=True)
    Employees = models.CharField(max_length=250, blank=True)
    parentCompany = models.CharField(max_length=250, blank=True)
    onMarket = models.CharField(max_length=250, blank=True)
    productName = models.CharField(max_length=250, blank=True)
    SKU = models.CharField(max_length=250, blank=True)
    Notes = models.CharField(max_length=1024, blank=True)
    processingFocus = models.CharField(max_length=1024, blank=True)
    facilitySize = models.CharField(max_length=250, blank=True)
    biomassCap = models.CharField(max_length=250, blank=True)
    extractionType = models.CharField(max_length=1024, blank=True)
    GMP = models.CharField(max_length=250, blank=True)
    news = models.CharField(max_length=1024, blank=True)
    reviews = models.CharField(max_length=512, blank=True)

    class Meta:
        abstract = True

class Company(CompanyDetail):

    class Meta:
        db_table = "company"

        verbose_name = "Company"
        verbose_name_plural = "Companies"

class PendingCompany(CompanyDetail):

    class Meta:
        db_table = "pending_company"

        verbose_name = "Pending Company"
        verbose_name_plural = "Pending Companies"

class PendingChanges(models.Model):
    companyId = models.CharField(max_length=250)
    changeType = models.CharField(max_length=250)
    editId = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = "pending_change"

        verbose_name = "Pending Change"
        verbose_name_plural = "Pending Changes"