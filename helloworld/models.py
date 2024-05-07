## Django
from django.db import models

class Solution(models.Model):
    solution = models.CharField(max_length=1024)
    
    def __str__(self):
        return "Solution: " + self.solution

    class Meta:
        db_table = "Solutions"

class Category(models.Model):
    category = models.CharField(max_length=1024)

    def __str__(self):
        return "Category: " + self.category

    class Meta:
        db_table = "Categories"

class stakeholderGroups(models.Model):
    stakeholderGroup = models.CharField(max_length=1024)

    def __str__(self):
        return "Stakeholder Group: " + self.stakeholderGroup
    
    class Meta:
        db_table = "Groups"

class Stage(models.Model):
    stage = models.CharField(max_length=1024)

    def __str__(self):
        return "Stage: " + self.stage

    class Meta:
        db_table = "Stage"

class ProductGroup(models.Model):
    productGroup = models.CharField(max_length=1024)

    def __str__(self):
        return "Product Group: " + self.productGroup

    class Meta:
        db_table = "ProductGroup"

class ProcessingFocus(models.Model):
    processingFocus = models.CharField(max_length=1024)

    def __str__(self):
        return "Processing Focus: " + self.processingFocus

    class Meta:
        db_table = "ProcessingFocus"

class ExtractionType(models.Model):
    extractionType = models.CharField(max_length=1024)

    def __str__(self):
        return "Extraction Type: " + self.extractionType

    class Meta:
        db_table = "ExtractionType"

class Company(models.Model):
    SrcKey = models.CharField(max_length=255, default=None, blank=True)
    Name = models.CharField(max_length=250)
    Industry = models.CharField(max_length=255)
    Status = models.CharField(max_length=255)
    Grower = models.CharField(max_length=255, default=None, blank=True)
    Info = models.CharField(max_length=255)
    Headquarters = models.CharField(max_length=255, blank=True)
    Address = models.CharField(max_length=512, default=None, blank=True)
    Sales = models.CharField(max_length=255, blank=True)
    Product = models.CharField(max_length=255, blank=True)
    City = models.CharField(max_length=250, blank=True)
    State = models.CharField(max_length=250, blank=True)
    Country = models.CharField(max_length=250)
    Solutions = models.ForeignKey(Solution, on_delete=models.CASCADE)
    Website = models.CharField(max_length=250, blank=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stakeholderGroup = models.ForeignKey(stakeholderGroups, on_delete=models.CASCADE)
    Stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    productGroup = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    Products = models.CharField(max_length=250, blank=True)
    sasContact = models.CharField(max_length=250, blank=True)
    Description = models.CharField(max_length=250, blank=True)
    pubPriv = models.CharField(max_length=250, blank=True)
    Ticker = models.CharField(max_length=250, blank=True)
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
    Notes = models.CharField(max_length=250, blank=True)
    processingFocus = models.ForeignKey(ProcessingFocus, on_delete=models.CASCADE)
    facilitySize = models.CharField(max_length=250, blank=True)
    biomassCap = models.CharField(max_length=250, blank=True)
    extractionType = models.ForeignKey(ExtractionType, on_delete=models.CASCADE)
    GMP = models.CharField(max_length=250, blank=True)
    news = models.CharField(max_length=250, blank=True)
    reviews = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = "Companies"

class PendingCompany(models.Model):
    SrcKey = models.CharField(max_length=255, default=None, blank=True)
    Name = models.CharField(max_length=250)
    Industry = models.CharField(max_length=255)
    Status = models.CharField(max_length=255)
    Grower = models.CharField(max_length=255, default=None, blank=True)
    Info = models.CharField(max_length=255)
    Headquarters = models.CharField(max_length=255, blank=True)
    Address = models.CharField(max_length=512, default=None, blank=True)
    Sales = models.CharField(max_length=255, blank=True)
    Product = models.CharField(max_length=255, blank=True)
    City = models.CharField(max_length=250, blank=True)
    State = models.CharField(max_length=250, blank=True)
    Country = models.CharField(max_length=250)
    Solutions = models.ForeignKey(Solution, on_delete=models.CASCADE)
    Website = models.CharField(max_length=250, blank=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stakeholderGroup = models.ForeignKey(stakeholderGroups, on_delete=models.CASCADE)
    Stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    productGroup = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    Products = models.CharField(max_length=250, blank=True)
    sasContact = models.CharField(max_length=250, blank=True)
    Description = models.CharField(max_length=250, blank=True)
    pubPriv = models.CharField(max_length=250, blank=True)
    Ticker = models.CharField(max_length=250, blank=True)
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
    Notes = models.CharField(max_length=250, blank=True)
    processingFocus = models.ForeignKey(ProcessingFocus, on_delete=models.CASCADE)
    facilitySize = models.CharField(max_length=250, blank=True)
    biomassCap = models.CharField(max_length=250, blank=True)
    extractionType = models.ForeignKey(ExtractionType, on_delete=models.CASCADE)
    GMP = models.CharField(max_length=250, blank=True)
    news = models.CharField(max_length=250, blank=True)
    reviews = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = "PendingCompanies"

class PendingChanges(models.Model):
    companyId = models.CharField(max_length=250)
    changeType = models.CharField(max_length=250)
    editId = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = "PendingChanges"