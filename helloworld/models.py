from django.db import models

# Create your models here.

class Company(models.Model):
    Name = models.CharField(max_length=250)
    Industry = models.CharField(max_length=255)
    Status = models.CharField(max_length=255)
    Info = models.CharField(max_length=255)
    Headquarters = models.CharField(max_length=255)
    Sales = models.CharField(max_length=255)
    Product = models.CharField(max_length=255)
    # Add more fields as needed
    class Meta:
        db_table = "Companies"

