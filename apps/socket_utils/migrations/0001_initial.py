# Generated by Django 4.1.2 on 2024-03-21 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0023_menu_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('state', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at_unix', models.BigIntegerField(editable=False)),
                ('updated_at_unix', models.BigIntegerField(editable=False, null=True)),
                ('type', models.CharField(choices=[('NEW_SOLCOT', 'NEW_SOLCOT'), ('NEW_MESSAGE', 'NEW_MESSAGE')], default='NEW_SOLCOT', help_text='Hace referencia al tipo de notificación', max_length=255)),
                ('title', models.CharField(help_text='Hace referencia al titulo de la notificación', max_length=255)),
                ('message', models.TextField(help_text='Hace referencia al mensaje de la notificación')),
                ('button_text', models.CharField(help_text='Hace referencia al texto del botón de la notificación', max_length=255)),
                ('button_link', models.CharField(help_text='Hace referencia al link del botón de la notificación', max_length=255)),
                ('icon', models.CharField(help_text='Hace referencia al icono de la notificación', max_length=255)),
                ('viewed', models.BooleanField(default=False, help_text='Hace referencia a si la notificación fue vista o no')),
                ('receiving_user', models.ForeignKey(help_text='Hace referencia a el usuario receptor', on_delete=django.db.models.deletion.CASCADE, related_name='notifications_received', to='authentication.users')),
                ('sender_user', models.ForeignKey(help_text='Hace referencia a el usuario remitente', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications_sent', to='authentication.users')),
                ('user_created_at', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_at', to='authentication.users')),
                ('user_updated_at', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_at', to='authentication.users')),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'db_table': 'notifications',
            },
        ),
    ]
