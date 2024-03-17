## Django
from django.db import models

class Solution(models.Model):
    solution = models.CharField(max_length=250)
    
    def __str__(self):
        return "Solution: " + self.solution

    class Meta:
        db_table = "Solutions"

class Category(models.Model):
    category = models.CharField(max_length=250)

    def __str__(self):
        return "Category: " + self.category

    class Meta:
        db_table = "Categories"

class stakeholderGroups(models.Model):
    stakeholderGroup = models.CharField(max_length=250)

    def __str__(self):
        return "Stakeholder Group: " + self.stakeholderGroup
    
    class Meta:
        db_table = "Groups"

class Stage(models.Model):
    stage = models.CharField(max_length=250)

    def __str__(self):
        return "Stage: " + self.stage

    class Meta:
        db_table = "Stage"

class ProductGroup(models.Model):
    productGroup = models.CharField(max_length=250)

    def __str__(self):
        return "Product Group: " + self.productGroup

    class Meta:
        db_table = "ProductGroup"

class ProcessingFocus(models.Model):
    processingFocus = models.CharField(max_length=250)

    def __str__(self):
        return "Processing Focus: " + self.processingFocus

    class Meta:
        db_table = "ProcessingFocus"

class ExtractionType(models.Model):
    extractionType = models.CharField(max_length=250)

    def __str__(self):
        return "Extraction Type: " + self.extractionType

    class Meta:
        db_table = "ExtractionType"

class Company(models.Model):
    Name = models.CharField(max_length=250)
    Industry = models.CharField(max_length=255)
    Status = models.CharField(max_length=255)
    Info = models.CharField(max_length=255)
    Headquarters = models.CharField(max_length=255)
    Sales = models.CharField(max_length=255)
    Product = models.CharField(max_length=255)
    City = models.CharField(max_length=250)
    State = models.CharField(max_length=250)
    Country = models.CharField(max_length=250)
    Solutions = models.ForeignKey(Solution, on_delete=models.CASCADE)
    Website = models.CharField(max_length=250)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stakeholderGroup = models.ForeignKey(stakeholderGroups, on_delete=models.CASCADE)
    Stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    productGroup = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    Products = models.CharField(max_length=250)
    sasContact = models.CharField(max_length=250)
    Description = models.CharField(max_length=250)
    pubPriv = models.CharField(max_length=250)
    Ticker = models.CharField(max_length=250)
    Naics = models.CharField(max_length=250)
    Phone = models.CharField(max_length=250)
    Email = models.CharField(max_length=250)
    Stakeholder = models.CharField(max_length=250)
    Principal = models.CharField(max_length=250)
    Founded = models.CharField(max_length=250)
    Employees = models.CharField(max_length=250)
    parentCompany = models.CharField(max_length=250)
    onMarket = models.CharField(max_length=250)
    productName = models.CharField(max_length=250)
    SKU = models.CharField(max_length=250)
    Notes = models.CharField(max_length=250)
    salesRev = models.CharField(max_length=250)
    processingFocus = models.ForeignKey(ProcessingFocus, on_delete=models.CASCADE)
    facilitySize = models.CharField(max_length=250)
    biomassCap = models.CharField(max_length=250)
    extractionType = models.ForeignKey(ExtractionType, on_delete=models.CASCADE)
    GMP = models.CharField(max_length=250)
    news = models.CharField(max_length=250)
    reviews = models.CharField(max_length=250)

    class Meta:
        db_table = "Companies"

class PendingCompany(models.Model):
    Name = models.CharField(max_length=250)
    Industry = models.CharField(max_length=255)
    Status = models.CharField(max_length=255)
    Info = models.CharField(max_length=255)
    Headquarters = models.CharField(max_length=255)
    Sales = models.CharField(max_length=255)
    Product = models.CharField(max_length=255)
    City = models.CharField(max_length=250)
    State = models.CharField(max_length=250)
    Country = models.CharField(max_length=250)
    Solutions = models.ForeignKey(Solution, on_delete=models.CASCADE)
    Website = models.CharField(max_length=250)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stakeholderGroup = models.ForeignKey(stakeholderGroups, on_delete=models.CASCADE)
    Stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    productGroup = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    Products = models.CharField(max_length=250)
    sasContact = models.CharField(max_length=250)
    Description = models.CharField(max_length=250)
    pubPriv = models.CharField(max_length=250)
    Ticker = models.CharField(max_length=250)
    Naics = models.CharField(max_length=250)
    Phone = models.CharField(max_length=250)
    Email = models.CharField(max_length=250)
    Stakeholder = models.CharField(max_length=250)
    Principal = models.CharField(max_length=250)
    Founded = models.CharField(max_length=250)
    Employees = models.CharField(max_length=250)
    parentCompany = models.CharField(max_length=250)
    onMarket = models.CharField(max_length=250)
    productName = models.CharField(max_length=250)
    SKU = models.CharField(max_length=250)
    Notes = models.CharField(max_length=250)
    salesRev = models.CharField(max_length=250)
    processingFocus = models.ForeignKey(ProcessingFocus, on_delete=models.CASCADE)
    facilitySize = models.CharField(max_length=250)
    biomassCap = models.CharField(max_length=250)
    extractionType = models.ForeignKey(ExtractionType, on_delete=models.CASCADE)
    GMP = models.CharField(max_length=250)
    news = models.CharField(max_length=250)
    reviews = models.CharField(max_length=250)

    class Meta:
        db_table = "PendingCompanies"