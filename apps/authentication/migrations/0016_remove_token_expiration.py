# Generated by Django 4.2.2 on 2024-02-08 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_token_expiration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='expiration',
        ),
    ]