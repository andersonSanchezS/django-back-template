# Generated by Django 4.1.2 on 2024-02-14 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_requestlog_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestlog',
            name='client',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
