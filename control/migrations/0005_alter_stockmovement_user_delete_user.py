# Generated by Django 5.2 on 2025-04-16 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0004_remove_user_branch_remove_user_company'),
        ('user_control', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockmovement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_control.users'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
