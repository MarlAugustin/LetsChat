# Generated by Django 5.1.2 on 2024-10-29 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_message_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='file',
        ),
    ]
