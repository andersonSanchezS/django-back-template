# Generated by Django 4.1.2 on 2024-03-06 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0023_menu_url'),
        ('request', '0003_shoppinggroup_shoppinggrouplog'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('state', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at_unix', models.BigIntegerField(editable=False)),
                ('updated_at_unix', models.BigIntegerField(editable=False, null=True)),
                ('code', models.CharField(blank=True, error_messages={'unique': 'Ya existe un centro de costo con este código'}, max_length=10, null=True, unique=True)),
                ('description', models.CharField(error_messages={'unique': 'Ya existe un centro de costo con este nombre'}, max_length=255, unique=True)),
                ('user_created_at', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_at', to='authentication.users')),
                ('user_updated_at', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_at', to='authentication.users')),
            ],
            options={
                'verbose_name': 'cost_center',
                'verbose_name_plural': 'cost_centers',
                'db_table': 'cost_centers',
            },
        ),
        migrations.CreateModel(
            name='CostCenterLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(max_length=255)),
                ('previousValues', models.JSONField(blank=True, null=True)),
                ('newValues', models.JSONField(blank=True, null=True)),
                ('costCenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.costcenter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.users')),
            ],
            options={
                'verbose_name': 'cost_center_log',
                'verbose_name_plural': 'cost_centers_log',
                'db_table': 'cost_centers_log',
            },
        ),
    ]
