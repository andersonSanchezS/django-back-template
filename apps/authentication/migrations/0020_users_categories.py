# Generated by Django 4.1.2 on 2024-02-21 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0014_category_categorylog'),
        ('authentication', '0019_alter_users_first_name_alter_users_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='users_category', to='misc.category'),
        ),
    ]
