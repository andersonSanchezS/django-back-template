# Generated by Django 4.1.2 on 2024-03-14 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0021_alter_holyday_day_alter_holyday_description_and_more'),
        ('request', '0014_alter_solcot_limit_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solcot',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='solcot',
            name='sub_categories',
            field=models.ManyToManyField(related_name='solcot_sub_categories', to='misc.subcategory'),
        ),
    ]