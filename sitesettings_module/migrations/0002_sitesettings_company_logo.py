# Generated by Django 4.2.9 on 2024-01-26 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitesettings_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='company_logo',
            field=models.ImageField(null=True, upload_to='images/company-logo'),
        ),
    ]