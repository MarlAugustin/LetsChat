# Generated by Django 5.1.2 on 2024-10-29 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_file_alter_message_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='files/'),
        ),
    ]
