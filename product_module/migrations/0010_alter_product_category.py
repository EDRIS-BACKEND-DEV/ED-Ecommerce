# Generated by Django 5.0.1 on 2024-02-11 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0009_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='product_module.productcategory'),
        ),
    ]
