# Generated by Django 4.2.20 on 2025-04-13 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_rename_tax_id_company_cuit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company',
        ),
    ]
