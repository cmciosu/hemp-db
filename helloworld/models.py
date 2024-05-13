## Django
from django.db import models

class Solution(models.Model):
    solution = models.CharField(max_length=1024)
    
    def __str__(self):
        return self.solution

    class Meta:
        db_table = "Solutions"

class Category(models.Model):
    category = models.CharField(max_length=1024)

    def __str__(self):
        return self.category

    class Meta:
        db_table = "Categories"

class stakeholderGroups(models.Model):
    stakeholderGroup = models.CharField(max_length=1024)
    category = models.IntegerField()

    def __str__(self):
        return self.stakeholderGroup
    
    class Meta:
        db_table = "Groups"

class Stage(models.Model):
    stage = models.CharField(max_length=1024)
    category = models.IntegerField()

    def __str__(self):
        return self.stage

    class Meta:
        db_table = "Stage"

class ProductGroup(models.Model):
    productGroup = models.CharField(max_length=1024)

    def __str__(self):
        return self.productGroup

    class Meta:
        db_table = "ProductGroup"

class Status(models.Model):
    status = models.CharField(max_length=250)

    def __str__(self):
        return "Status: " + self.status

    class Meta:
        db_table = "Status"

class Industry(models.Model):
    industry = models.CharField(max_length=250)

    def __str__(self):
        return "Industry: " + self.industry

    class Meta:
        db_table = "Industry"

class Grower(models.Model):
    grower = models.CharField(max_length=250)

    def __str__(self):
        return "Grower: " + self.grower

    class Meta:
        db_table = "Grower"

class Company(models.Model):
    SrcKey = models.CharField(max_length=128, default=None, blank=True)
    Name = models.CharField(max_length=250)
    Industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    Status = models.ForeignKey(Status, on_delete=models.CASCADE)
    Grower = models.ForeignKey(Grower, on_delete=models.CASCADE)
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
        db_table = "Companies"

class PendingCompany(models.Model):
    SrcKey = models.CharField(max_length=128, default=None, blank=True)
    Name = models.CharField(max_length=250)
    Industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    Status = models.ForeignKey(Status, on_delete=models.CASCADE)
    Grower = models.ForeignKey(Grower, on_delete=models.CASCADE)
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
        db_table = "PendingCompanies"

class PendingChanges(models.Model):
    companyId = models.CharField(max_length=250)
    changeType = models.CharField(max_length=250)
    editId = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = "PendingChanges"