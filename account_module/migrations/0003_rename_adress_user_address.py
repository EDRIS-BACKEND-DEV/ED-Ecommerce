# Generated by Django 5.0.1 on 2024-01-31 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0002_user_adress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='adress',
            new_name='address',
        ),
    ]