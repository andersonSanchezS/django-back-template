# Generated by Django 4.1.2 on 2024-02-01 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0008_rename_updatedfields_typedocumentlog_newvalues_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typedocumentlog',
            name='description',
        ),
    ]
