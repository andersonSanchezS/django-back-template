# Generated by Django 4.1.2 on 2024-01-31 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_activitylog_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='changes',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
