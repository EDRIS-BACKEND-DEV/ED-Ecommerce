# Generated by Django 5.0.1 on 2024-02-15 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0012_productgallery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productgallery',
            options={'verbose_name': 'Product Gallery', 'verbose_name_plural': 'Product Galleries'},
        ),
    ]