# Generated by Django 4.1.2 on 2024-02-06 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_remove_permissionlog_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='description',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]