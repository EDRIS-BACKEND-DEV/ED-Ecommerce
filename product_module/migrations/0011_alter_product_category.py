# Generated by Django 5.0.1 on 2024-02-11 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0010_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='categories_products', to='product_module.productcategory'),
        ),
    ]
