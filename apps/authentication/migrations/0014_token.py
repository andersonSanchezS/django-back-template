# Generated by Django 4.2.2 on 2024-02-08 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_remove_users_code_remove_users_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('token', models.TextField()),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_user_auth', to='authentication.users')),
            ],
            options={
                'verbose_name': 'token',
                'verbose_name_plural': 'tokens',
                'db_table': 'tokens',
            },
        ),
    ]
