# Generated by Django 3.2.25 on 2024-05-10 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='Description',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='company',
            name='Products',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='company',
            name='news',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='company',
            name='reviews',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='pendingcompany',
            name='Description',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='pendingcompany',
            name='news',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='pendingcompany',
            name='reviews',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]