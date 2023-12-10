from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    Company_ID = models.CharField(max_length=255)
    Company_Name = models.CharField(max_length=255)
    Status = models.CharField(max_length=255)
    Info = models.CharField(max_length=255)
    Headquarters = models.CharField(max_length=255)
    Sales = models.CharField(max_length=255)
    Product = models.CharField(max_length=255)
    # Add more fields as needed

    def __str__(self):
        return self.name
