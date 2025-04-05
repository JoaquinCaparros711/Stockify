# Generated by Django 5.1.7 on 2025-04-03 20:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('tax_id', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='sucursal',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='movimientostock',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='movimientostock',
            name='sucursal',
        ),
        migrations.RemoveField(
            model_name='movimientostock',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='stocksucursal',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='stocksucursal',
            name='sucursal',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='sucursal',
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.company')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_stock', models.IntegerField(default=0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.company')),
            ],
        ),
        migrations.CreateModel(
            name='BranchStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_stock', models.IntegerField(default=0)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.product')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('employee', 'Employee')], max_length=8)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='control.branch')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.company')),
            ],
        ),
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')], max_length=9)),
                ('quantity', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Empresa',
        ),
        migrations.DeleteModel(
            name='MovimientoStock',
        ),
        migrations.DeleteModel(
            name='Producto',
        ),
        migrations.DeleteModel(
            name='StockSucursal',
        ),
        migrations.DeleteModel(
            name='Sucursal',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
