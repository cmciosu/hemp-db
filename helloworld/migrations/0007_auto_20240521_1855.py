# Generated by Django 3.2.25 on 2024-05-21 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0006_alter_resources_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='resources',
            name='text',
            field=models.CharField(blank=True, max_length=2048),
        ),
        migrations.AlterField(
            model_name='resources',
            name='url',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
