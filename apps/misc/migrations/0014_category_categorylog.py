# Generated by Django 4.1.2 on 2024-02-21 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_alter_users_first_name_alter_users_last_name'),
        ('misc', '0013_typedocument_abbreviation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('state', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at_unix', models.BigIntegerField(editable=False)),
                ('updated_at_unix', models.BigIntegerField(editable=False, null=True)),
                ('description', models.CharField(max_length=255, unique=True)),
                ('user_created_at', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_at', to='authentication.users')),
                ('user_updated_at', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_at', to='authentication.users')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(max_length=255)),
                ('previousValues', models.JSONField(blank=True, null=True)),
                ('newValues', models.JSONField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='misc.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.users')),
            ],
            options={
                'verbose_name': 'category_log',
                'verbose_name_plural': 'categories_log',
                'db_table': 'categories_log',
            },
        ),
    ]