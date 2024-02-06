# Generated by Django 4.1.2 on 2024-02-06 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_users_custom_permissions_alter_role_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='users_role', to='authentication.role'),
        ),
    ]