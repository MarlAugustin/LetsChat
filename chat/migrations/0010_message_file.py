# Generated by Django 5.1.2 on 2024-10-29 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_remove_message_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.ImageField(blank=True, upload_to='files/'),
        ),
    ]
