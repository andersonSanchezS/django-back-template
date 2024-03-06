# Generated by Django 4.1.2 on 2024-03-06 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0018_rename_sub_category_subcategorylog_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='code',
            field=models.CharField(error_messages={'unique': 'Ya existe una categoría con este código'}, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(error_messages={'unique': 'Ya existe una categoría con este nombre'}, max_length=255, unique=True),
        ),
    ]
